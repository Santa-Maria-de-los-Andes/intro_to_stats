// supabase/functions/grade-reflexion/index.ts
//
// Califica celdas "💭 Reflexiona" de la Mision 2 (nb3_correlacion.ipynb /
// nb4_correlacion.ipynb, y su variante nb3_lite/nb4_lite para la ruta de
// interpretacion) via DeepSeek (deepseek-chat). La clave de DeepSeek vive
// solo aca (Supabase secret DEEPSEEK_API_KEY) -- nunca en el notebook,
// igual que `submissions` nunca expuso una clave con alcance real (solo el
// anon key, restringido por RLS).
//
// Contrato: POST {dni, notebook, curso, reflexion_id, student_text, grado}
//           -> {score, comment, max_pts}  |  {error: "..."} (4xx/5xx)
//
// El caller (autograder_nb3.py / autograder_nb4.py / *_lite.py) NO debe
// interpretar un error como "el alumno saco 0" -- debe reintentar/pedir de
// nuevo, nunca calificar en base a un fallo de esta funcion.
//
// 2026-08-21 (diagnostico en vivo, SOFIA/ATLAS): EXPECTED_NOTEBOOK era un
// string unico hardcodeado a "nb3_semana3" -- el notebook_id de ANTES del
// rename explicito del usuario a "nb3"/"nb4" y de la reestructuracion que
// agrego Seccion C + Mini-Proyecto. Cualquier request desde los notebooks
// actuales (nb3, nb4, y la ruta nb3_lite/nb4_lite que subclasea los
// autograders principales) recibia 400 unexpected_notebook_or_curso de
// inmediato, y el notebook lo mostraba como "problema de conexion" -- no
// era un fallo de red, era este allowlist desactualizado. Corregido a un
// Set con los cuatro notebook_id validos actuales. Recordatorio para quien
// agregue un notebook nuevo que reuse este patron: sumarlo aca tambien, no
// asumir que el string por defecto alcanza.

const DEEPSEEK_API_KEY = Deno.env.get("DEEPSEEK_API_KEY")!;
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

const EXPECTED_NOTEBOOKS = new Set(["nb3", "nb4", "nb3_lite", "nb4_lite"]);
const EXPECTED_CURSO = "STAT_2026";

// 2026-08-24: bajo carga concurrente de clase (varios alumnos calificando
// reflexiones en simultaneo, misma DEEPSEEK_API_KEY compartida) se vieron
// 502 intermitentes -- ver WORKFORCE_HANDOFF.md, diagnostico en vivo con
// logs reales de Supabase. Un solo intento de 15s no distingue entre
// "DeepSeek tardo un poco mas de la cuenta" y "DeepSeek realmente fallo",
// asi que ahora se reintenta una vez con una pausa corta antes de rendirse.
// El caller (autograder_nb3.py/_nb4.py) tiene que esperar al menos
// DEEPSEEK_TIMEOUT_MS*DEEPSEEK_MAX_ATTEMPTS + pausas -- su propio timeout
// se subio a 55s para dejar margen (ver esos archivos).
const DEEPSEEK_TIMEOUT_MS = 20000;
const DEEPSEEK_MAX_ATTEMPTS = 2;
const DEEPSEEK_RETRY_DELAY_MS = 1500;

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

type ReflexionSpec = {
  question: string;
  grounding: string;
  grading_notes: string;
  max_pts: number;
};

// Preguntas, valores reales (verificados contra 2019_es.csv, nunca
// estimados -- misma disciplina que el resto del notebook) y criterio de
// calificacion por celda. Orden = orden de aparicion en el notebook.
//
// 2026-08-21: ronda1/concepto (nb3) y subgrupos/interpretacion/metodologica
// (nb4) son nuevas -- agregadas cuando el notebook se reestructuro para
// fundir grafica+calculo en un solo ejercicio y agregar Seccion C +
// Mini-Proyecto (ver WORKFORCE_HANDOFF.md Done log 2026-08-20/21). a1/a2/
// guiado/corrupcion/esperanza/ronda4/ronda5/explora/causacion quedan de la
// version anterior (Seccion A/B separadas) -- ya no las envia ningun
// notebook actual, se dejan sin usar en vez de borrarlas por si algo las
// referencia todavia.
const GRADING_NOTES: Record<string, ReflexionSpec> = {
  ronda1: {
    question:
      'En una frase: ¿tu ojo acerto en fuerza y direccion para "Percepción de corrupción", o te sorprendio algo del resultado?',
    grounding:
      "r real (Percepción de corrupción vs Puntaje) = 0.386 -- relacion positiva pero debil-a-moderada. A diferencia de la version anterior de esta celda, aqui el estudiante YA calculo el numero (el ejercicio funde grafica+calculo en un solo paso), asi que puede referirse a el directamente.",
    grading_notes:
      "Credito si compara su prediccion (celda PREDICE anterior) contra lo que realmente encontro -- fuerza y/o direccion -- de forma especifica, no generica. Sin credito si esta vacia, copia la pregunta, o no hace ninguna comparacion real.",
    max_pts: 5,
  },
  concepto: {
    question:
      'En 2-3 oraciones, sin usar ningun par de columnas como ejemplo: ¿que te dice el coeficiente de correlacion, y que es lo que NUNCA te dice por si solo?',
    grounding:
      "Pregunta puramente conceptual -- no requiere ningun dato del dataset. Respuesta esperada cubre dos mitades: (1) que SI resume (fuerza y direccion de una relacion lineal) y (2) que NUNCA prueba por si solo (causalidad).",
    grading_notes:
      "Credito completo solo si cubre ambas mitades (que mide + que nunca prueba). Penaliza si usa un ejemplo de columnas del dataset (la instruccion pide evitarlo explicitamente), si solo cubre una mitad, o si la respuesta es vacia/generica.",
    max_pts: 5,
  },
  pbi_apoyo: {
    question:
      '"PBI per cápita" te volvió a dar un r fuerte (~0.75), esta vez con "Apoyo social" -- la segunda vez hoy que el PBI produce una relación fuerte con una variable distinta. En 1-2 oraciones: ¿qué tienen en común estas dos relaciones fuertes, y te parece razonable que el PBI de un país se relacione consistentemente fuerte con variables tan distintas entre sí?',
    grounding:
      "r real (PBI per cápita vs Apoyo social) = 0.755 -- fuerte y positivo, la segunda relación más fuerte entre las seis variables (después de PBI vs Esperanza de vida saludable, r=0.835, visto en Ronda 3). Ambas comparten el PBI como variable común: países con mayor producción económica tienden a tener tanto mejor esperanza de vida saludable como mayor apoyo social percibido -- consistente con la idea de que la riqueza de un país financia tanto salud pública como redes de protección social, sin que eso pruebe una relación causal directa.",
    grading_notes:
      "Credito si identifica el PBI como el factor común entre ambas relaciones fuertes (no solo repite que ambas son fuertes) y ofrece una explicación razonable (ej. más recursos/infraestructura). Credito parcial si solo dice que 'tiene sentido' sin explicar por qué. Sin credito si esta vacia/generica o si afirma que el PBI causa directamente estas variables sin ningun matiz.",
    max_pts: 5,
  },
  generosidad_corrupcion: {
    question:
      'Hasta ahora, "Generosidad" te dio un r cercano a 0 con casi todo lo que probaste hoy (r≈0.08 con "Puntaje" en la Apertura). Pero con "Percepción de corrupción" el r ya no es tan chico. En 1-2 oraciones: ¿te parece razonable que Generosidad casi no se relacione con nada, excepto con esta variable en particular? ¿Qué explicación se te ocurre?',
    grounding:
      "r real (Generosidad vs Percepción de corrupción) = 0.327 -- débil a moderado, notablemente más alto que Generosidad vs Puntaje (0.076), Generosidad vs PBI (-0.080), Generosidad vs Apoyo social (-0.048) o Generosidad vs Esperanza de vida saludable (-0.030), todas prácticamente nulas. Generosidad es, de las seis variables, la que menos se relaciona con el resto -- excepto con esta.",
    grading_notes:
      "Credito si reconoce el contraste (Generosidad casi no se relaciona con nada más, pero aquí sí hay algo, aunque moderado -- no fuerte) y propone una explicación plausible (ej. sociedades con menos corrupción percibida generan más confianza, lo que facilita donar/ayudar). Sin credito si no reconoce el contraste, describe el r como fuerte, o la respuesta esta vacia/generica.",
    max_pts: 5,
  },
  subgrupos: {
    question:
      'El r general de "Generosidad" vs. "Puntaje" era casi 0. Pero acabas de ver que dentro de Europa es positivo, y dentro de América es negativo. En 2-3 oraciones: ¿que te dice esto sobre confiar en "el patron general" de todo un dataset sin mirar los subgrupos?',
    grounding:
      "r real: Generosidad vs Puntaje general = 0.076 (casi nulo); dentro de Europa = 0.530 (positivo, moderado); dentro de América = -0.211 (negativo). El patron general esconde signos opuestos por subgrupo, confirmado contra el dataset real.",
    grading_notes:
      "Credito si articula que el patron general (todos los paises juntos) puede esconder relaciones distintas u opuestas dentro de cada subgrupo -- no es sustituto de mirar los subgrupos. Sin credito si concluye que el patron general siempre es confiable, o si la respuesta esta vacia/generica.",
    max_pts: 5,
  },
  interpretacion: {
    question:
      'Mira el resultado que imprimiste arriba (tus dos variables y tu r). Sin usar la palabra "causa" ni ninguna variante: ¿que te dice ese r sobre la relacion entre tus dos variables? ¿Y que es lo que NO te dice?',
    grounding:
      "Reflexion sobre el PAR PROPIO que el estudiante eligio en el mini-proyecto -- no hay un r fijo esperado aqui, cada estudiante trabaja con un par y numero distintos. Evalua consistencia interna (su interpretacion coincide con la fuerza/direccion que ellos mismos reportaron), no un valor exacto.",
    grading_notes:
      "Credito completo si interpreta fuerza y direccion de su PROPIO r de forma coherente con lo que reportaron, evita activamente lenguaje causal, y menciona explicitamente algo que el numero NO prueba. Penaliza si usa 'causa'/equivalente directo, si no menciona ninguna limitacion, o si la respuesta es vacia/generica.",
    max_pts: 5,
  },
  metodologica: {
    question:
      'Miraste una matriz con muchisimos pares posibles y elegiste uno. Si hubieras probado 20 pares al azar, es esperable que alguno salga con un r alto solo por casualidad. En 2-3 oraciones: ¿por que no deberias confiar automaticamente en "el par con el r mas alto que encontre" solo porque salio alto?',
    grounding:
      "Pregunta conceptual sobre el riesgo de correlacion espuria/comparaciones multiples -- no depende del par especifico que el estudiante eligio, evalua si entiende el riesgo metodologico en general.",
    grading_notes:
      "Credito completo si articula que explorar muchos pares aumenta la probabilidad de encontrar un r alto por puro azar (razonamiento de comparaciones multiples), no solo repite 'correlacion no es causalidad'. Credito parcial si solo dice que hace falta una hipotesis/razon sin explicar el mecanismo de azar. Sin credito si esta vacia o no aborda el riesgo en absoluto.",
    max_pts: 5,
  },
  a1: {
    question:
      'En una frase: ¿tu ojo acerto en fuerza y direccion para "Percepción de corrupción", o te sorprendio algo del scatter que acabas de construir?',
    grounding:
      "r real (Percepción de corrupción vs Puntaje) = 0.386 -- pero este numero TODAVIA NO se revela en esta parte de la leccion (observacion visual antes de calcular). No penalices una 'lectura' del scatter que no coincida con el numero real -- el punto es la honestidad de la observacion, no acertar el numero.",
    grading_notes:
      "Credito si describe genuinamente algo que vio en su propio scatter (fuerza, direccion, dispersion, algo que le sorprendio) -- no una frase generica que serviria para cualquier grafico. Sin credito si esta vacia, copia la pregunta, o es una palabra suelta sin ninguna observacion concreta.",
    max_pts: 5,
  },
  a2: {
    question:
      'En una frase: comparando los dos scatter que construiste hoy ("Percepción de corrupción" y "Esperanza de vida saludable"), ¿en cual de los dos los puntos siguen un patron mas apretado (menos dispersos)?',
    grounding:
      "r real: Percepción de corrupción vs Puntaje = 0.386; Esperanza de vida saludable vs Puntaje = 0.780 -- Esperanza es visualmente la relacion mas fuerte. Igual que en a1, es observacion pre-calculo -- no penalices si 'vio' distinto, solo evalua si comparo genuinamente los dos graficos.",
    grading_notes:
      "Credito si compara explicitamente los dos scatters (no solo describe uno). Sin credito si esta vacia, es generica, o no hace una comparacion real entre los dos.",
    max_pts: 5,
  },
  guiado: {
    question:
      'En una frase, sin decir que una "causa" la otra: ¿que te dice un r ≈ 0.78 sobre la relacion entre "Apoyo social" y "Puntaje"?',
    grounding:
      "r real (Apoyo social vs Puntaje) = 0.777, ya revelado en el enunciado (~0.78) -- relacion fuerte y positiva.",
    grading_notes:
      "Credito si interpreta el numero como una relacion fuerte y positiva SIN usar lenguaje causal directo ('mas apoyo produce/genera/causa mas felicidad' pierde puntos). Sin credito si usa 'causa' o un equivalente directo, o si la respuesta es vacia/generica.",
    max_pts: 5,
  },
  corrupcion: {
    question:
      '¿Que tan cerca estuvo tu prediccion del Ejercicio 1 del "r_corrupcion" real? Y en tus propias palabras: ¿que dice este numero sobre la relacion entre percepcion de corrupcion y felicidad?',
    grounding:
      "r real (Percepción de corrupción vs Puntaje) = 0.386 -- relacion positiva pero DEBIL A MODERADA, no fuerte. Una reflexion que la describe como 'fuerte' o 'muy alta' es factualmente incorrecta.",
    grading_notes:
      "Credito si caracteriza correctamente la relacion como debil-a-moderada (no fuerte) y positiva, y compara honestamente con su prediccion del Ejercicio 1. Penaliza si la describe como fuerte, o si no compara con su prediccion en absoluto.",
    max_pts: 5,
  },
  esperanza: {
    question:
      '"r_apoyo_social" y "r_esperanza" resultan casi identicos en fuerza (ambos cerca de 0.78) aunque son variables completamente distintas. ¿Te parece casualidad, o tiene sentido que ambas se relacionen con la felicidad de manera parecida? Explica en 1-2 oraciones.',
    grounding:
      "r real: Apoyo social vs Puntaje = 0.777; Esperanza de vida saludable vs Puntaje = 0.780 -- efectivamente casi identicos, ambos fuertes.",
    grading_notes:
      "Credito si ofrece una explicacion razonada (casualidad vs. mecanismo compartido, ej. paises ricos/estables tienden a tener ambos altos) en vez de solo 'si' o 'no' sin justificar. Sin credito si no justifica, o si la respuesta es vacia/generica.",
    max_pts: 5,
  },
  ronda3: {
    question:
      '"PBI per cápita" y "Esperanza de vida saludable" salio con el r mas alto que calculaste en toda la clase -- mas alto incluso que cualquiera de los dos con "Puntaje". ¿Por que crees que estas dos variables en particular se mueven tan juntas?',
    grounding:
      "r real (PBI per cápita vs Esperanza de vida saludable) = 0.835 -- el par mas fuerte de todo el dataset, confirmado.",
    grading_notes:
      "Credito si propone un mecanismo plausible (ej. paises con mas PBI invierten mas en salud publica/nutricion/acceso medico) en vez de solo repetir que 'estan relacionados'. Sin credito si esta vacia o no intenta explicar el porque.",
    max_pts: 5,
  },
  ronda4: {
    question:
      'Compara el r de esta ronda con el r de la Ronda 3. Ambos pares comparten "Esperanza de vida saludable", pero dan numeros distintos. ¿Que te dice eso sobre generalizar "esta variable siempre se relaciona igual de fuerte con todo"?',
    grounding:
      "r real: Ronda 3 (PBI vs Esperanza) = 0.835; Ronda 4 (Apoyo social vs Esperanza) = 0.719 -- distintos, ambos fuertes pero no iguales.",
    grading_notes:
      "Credito si concluye que la fuerza de una correlacion depende del PAR especifico, no es una propiedad fija de una variable (la leccion central de esta ronda). Sin credito si concluye lo opuesto, o si no compara los dos numeros en absoluto.",
    max_pts: 5,
  },
  ronda5: {
    question:
      'Este par dio un r notablemente mas chico que las Rondas 3 y 4. En tus propias palabras: ¿que significa "una relacion real, pero mucho menos consistente"?',
    grounding:
      "r real (Libertad para tomar decisiones vs Percepción de corrupción) = 0.439 -- moderado, notablemente mas bajo que Ronda 3 (0.835) y Ronda 4 (0.719), pero no cero.",
    grading_notes:
      "Credito si explica que la relacion existe (no es casualidad/cero) pero hay mas dispersion/excepciones que en un r mas alto -- no la confunde con 'no hay relacion'. Sin credito si concluye que no hay relacion en absoluto, o si la respuesta esta vacia.",
    max_pts: 5,
  },
  ronda6: {
    question:
      'De las seis variables economicas y sociales del dataset, "PBI per cápita" y "Generosidad" dieron el r mas cercano a 0 de las cuatro rondas nuevas. ¿Te parece razonable que el dinero de un pais casi no prediga que tan generosa es su gente? ¿Por que si o por que no?',
    grounding:
      "r real (PBI per cápita vs Generosidad) = -0.080 -- practicamente nulo, confirmado. Una reflexion que describe esto como una relacion real (positiva o negativa) es factualmente incorrecta.",
    grading_notes:
      "Credito si reconoce que casi-cero significa 'no hay relacion lineal detectable' y da una razon plausible (generosidad depende de cultura/valores, no solo de riqueza). Penaliza si afirma que SI hay una relacion clara en cualquier direccion.",
    max_pts: 5,
  },
  explora: {
    question:
      "De las seis variables que exploraste, ¿cual resultado te sorprendio mas -- una que esperabas fuerte y salio debil, o al reves? ¿Por que crees que pasa eso?",
    grounding:
      "Los seis r reales de esta seccion: Apoyo social vs Puntaje=0.777, Esperanza vs Puntaje=0.780, PBI vs Esperanza=0.835, Apoyo social vs Esperanza=0.719, Libertad vs Corrupcion=0.439, PBI vs Generosidad=-0.080.",
    grading_notes:
      "Credito si identifica un resultado especifico (no generico) y da una razon, aunque sea simple. Sin credito si no menciona ningun resultado especifico o esta vacia.",
    max_pts: 5,
  },
  causacion: {
    question:
      '"PBI per cápita" y "Puntaje" tienen r ≈ 0.79 -- una relacion fuerte y positiva. ¿Significa esto que tener mas dinero produce felicidad? Escribe 2-3 oraciones: si no estas seguro de que la respuesta sea "si," ¿que otra explicacion se te ocurre para esa relacion?',
    grounding:
      "r real (PBI per cápita vs Puntaje) = 0.794, confirmado. Esta es la celda de critica de causalidad -- la mas importante de las 11 para exigir precision.",
    grading_notes:
      "Credito completo solo si la respuesta EVITA activamente afirmar causalidad directa (no dice 'el dinero produce/causa felicidad' sin matizar) Y propone al menos una explicacion alternativa plausible (variable de confusion, causalidad inversa, o correlacion sin causacion explicita). 'No se sabe' sin ninguna alternativa concreta merece credito parcial, no completo.",
    max_pts: 5,
  },
};

const GRADO_STRICTNESS: Record<string, string> = {
  "3ro":
    "Nivel 3ro de secundaria: se leniente. Otorga credito completo por un compromiso genuino y basico con la pregunta, aunque el razonamiento sea simple o incompleto. No penalices lenguaje sencillo ni una justificacion corta.",
  "4to":
    "Nivel 4to de secundaria: nivel moderado. Espera que la respuesta conecte claramente el numero/hallazgo con el concepto preguntado. Una imprecision menor esta bien.",
  "5to":
    "Nivel 5to de secundaria: se estricto. Espera un razonamiento preciso y completo. En preguntas sobre correlacion vs. causalidad en particular, una respuesta que solo insinua incertidumbre sin evitar activamente el lenguaje causal debe perder puntos, no solo una que se equivoca de concepto.",
};

function jsonResponse(body: unknown, status: number): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

type DeepSeekOutcome =
  | { ok: true; score: number; comment: string }
  | { ok: false; failReason: string };

// Un solo intento contra DeepSeek. Nunca lanza -- toda falla (red, timeout,
// status no-2xx, forma de respuesta invalida) vuelve como
// {ok:false, failReason} para que el caller decida si reintentar y para que
// quede logueado con detalle real (antes de este cambio, los tres casos
// eran indistinguibles: todos devolvian el mismo 502 generico).
async function callDeepSeekOnce(
  systemPrompt: string,
  studentText: string,
  // deno-lint-ignore no-explicit-any
  tool: any,
  maxPts: number,
): Promise<DeepSeekOutcome> {
  let dsResp: Response;
  try {
    dsResp = await fetch("https://api.deepseek.com/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${DEEPSEEK_API_KEY}`,
      },
      body: JSON.stringify({
        model: "deepseek-chat",
        temperature: 0.3,
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: studentText },
        ],
        tools: [tool],
        tool_choice: { type: "function", function: { name: "submit_grade" } },
      }),
      signal: AbortSignal.timeout(DEEPSEEK_TIMEOUT_MS),
    });
  } catch (err) {
    const isTimeout = err instanceof Error && err.name === "TimeoutError";
    const msg = err instanceof Error ? err.message : String(err);
    return {
      ok: false,
      failReason: isTimeout ? "deepseek_timeout" : `deepseek_network_error:${msg}`,
    };
  }

  if (!dsResp.ok) {
    let bodySnippet = "";
    try {
      bodySnippet = (await dsResp.text()).slice(0, 300);
    } catch {
      // el status por si solo ya sirve para el log si esto tambien falla
    }
    return { ok: false, failReason: `deepseek_http_${dsResp.status}:${bodySnippet}` };
  }

  // deno-lint-ignore no-explicit-any
  let deepseekJson: any;
  try {
    deepseekJson = await dsResp.json();
  } catch {
    return { ok: false, failReason: "deepseek_bad_json" };
  }

  // Enforcement, capa 2: no confiar en la forma solo porque DeepSeek
  // devolvio 200 -- validar tipo/rango antes de usar nada.
  try {
    const toolCall = deepseekJson?.choices?.[0]?.message?.tool_calls?.[0];
    if (toolCall?.function?.name === "submit_grade") {
      const args = JSON.parse(toolCall.function.arguments);
      if (
        typeof args.score === "number" &&
        Number.isInteger(args.score) &&
        typeof args.comment === "string" &&
        args.comment.trim().length > 0
      ) {
        return {
          ok: true,
          score: Math.max(0, Math.min(maxPts, Math.round(args.score))),
          comment: args.comment,
        };
      }
    }
    return { ok: false, failReason: "deepseek_invalid_tool_call_shape" };
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    return { ok: false, failReason: `deepseek_parse_error:${msg}` };
  }
}

// Reintenta callDeepSeekOnce hasta DEEPSEEK_MAX_ATTEMPTS veces, con una
// pausa corta entre intentos -- absorbe rate-limit/latencia transitoria de
// DeepSeek bajo carga concurrente de clase sin duplicar la logica de arriba.
// Cada intento fallido se loguea con su motivo real (console.error, visible
// en los logs de Supabase) en vez de perderse en un 502 generico.
async function gradeWithRetry(
  systemPrompt: string,
  studentText: string,
  // deno-lint-ignore no-explicit-any
  tool: any,
  maxPts: number,
): Promise<
  { score: number; comment: string; failReasons: string[] } |
  { score: undefined; comment: undefined; failReasons: string[] }
> {
  const failReasons: string[] = [];
  for (let attempt = 1; attempt <= DEEPSEEK_MAX_ATTEMPTS; attempt++) {
    const outcome = await callDeepSeekOnce(systemPrompt, studentText, tool, maxPts);
    if (outcome.ok) {
      if (failReasons.length > 0) {
        console.log(
          `grade-reflexion: intento ${attempt}/${DEEPSEEK_MAX_ATTEMPTS} OK tras ${failReasons.length} fallo(s) previo(s): ${failReasons.join(" | ")}`,
        );
      }
      return { score: outcome.score, comment: outcome.comment, failReasons };
    }
    failReasons.push(outcome.failReason);
    console.error(
      `grade-reflexion: intento ${attempt}/${DEEPSEEK_MAX_ATTEMPTS} fallo: ${outcome.failReason}`,
    );
    if (attempt < DEEPSEEK_MAX_ATTEMPTS) {
      await sleep(DEEPSEEK_RETRY_DELAY_MS);
    }
  }
  return { score: undefined, comment: undefined, failReasons };
}

Deno.serve(async (req: Request) => {
  if (req.method !== "POST") {
    return jsonResponse({ error: "method_not_allowed" }, 405);
  }

  let body: {
    dni?: string;
    notebook?: string;
    curso?: string;
    reflexion_id?: string;
    student_text?: string;
    grado?: string;
  };
  try {
    body = await req.json();
  } catch {
    return jsonResponse({ error: "bad_json" }, 400);
  }

  const { dni, notebook, curso, reflexion_id, student_text, grado } = body;

  if (!EXPECTED_NOTEBOOKS.has(notebook ?? "") || curso !== EXPECTED_CURSO) {
    return jsonResponse({ error: "unexpected_notebook_or_curso" }, 400);
  }

  const spec = reflexion_id ? GRADING_NOTES[reflexion_id] : undefined;
  if (!spec) {
    return jsonResponse({ error: "unknown_reflexion_id" }, 400);
  }

  if (typeof student_text !== "string" || student_text.trim().length === 0) {
    return jsonResponse({ error: "empty_student_text" }, 400);
  }

  // grado desconocido/ausente -> nunca rechazar la calificacion por esto,
  // caer al nivel medio.
  const strictness = GRADO_STRICTNESS[grado ?? ""] ?? GRADO_STRICTNESS["4to"];

  const systemPrompt = `Eres un asistente que califica reflexiones abiertas de estudiantes de secundaria en un curso de estadistica, en una leccion sobre correlacion. Responde SIEMPRE llamando a la funcion submit_grade -- nunca en texto libre.

Pregunta que se le hizo al estudiante:
"${spec.question}"

Contexto real (dato verificado contra el dataset -- no reveles el numero exacto en tu comentario a menos que la propia respuesta del estudiante ya lo mencione):
${spec.grounding}

Que evaluar:
${spec.grading_notes}

Calibracion de estrictez para este estudiante:
${strictness}

Califica de 0 a ${spec.max_pts} puntos enteros. El comentario debe ser 1-2 oraciones en español, especifico a lo que el estudiante escribio, cordial pero honesto -- nunca generico tipo "bien hecho".`;

  const tool = {
    type: "function",
    function: {
      name: "submit_grade",
      description: "Registra la calificacion final para esta reflexion.",
      parameters: {
        type: "object",
        properties: {
          score: {
            type: "integer",
            minimum: 0,
            maximum: spec.max_pts,
            description: `Puntaje entero de 0 a ${spec.max_pts}.`,
          },
          comment: {
            type: "string",
            description: "1-2 oraciones en español, especificas a la respuesta del estudiante.",
          },
        },
        required: ["score", "comment"],
        additionalProperties: false,
      },
    },
  };

  const { score, comment, failReasons } = await gradeWithRetry(
    systemPrompt,
    student_text,
    tool,
    spec.max_pts,
  );

  if (score === undefined || comment === undefined) {
    // 2026-08-24 (diagnostico en vivo tras 502s durante clase, ver
    // WORKFORCE_HANDOFF.md): antes esto siempre devolvia el mismo
    // {error:"grading_failed"} sin importar la causa real (DeepSeek
    // ratelimit/error, timeout, o forma de respuesta invalida), asi que ni
    // siquiera los logs de Supabase distinguian una causa de otra. Ahora se
    // loguea (console.error, mas abajo en gradeWithRetry) y se devuelve el
    // ultimo motivo real en el body -- el notebook lo sigue ignorando
    // (nunca debe interpretar un error como "el alumno saco 0"), pero
    // queda visible para quien mire los logs de la funcion.
    return jsonResponse(
      { error: "grading_failed", detail: failReasons.at(-1) ?? "unknown" },
      502,
    );
  }

  // Auditoria fire-and-forget -- nunca bloquear la respuesta al alumno por
  // esto ni fallar la calificacion si el insert falla.
  fetch(`${SUPABASE_URL}/rest/v1/llm_reflexion_grades`, {
    method: "POST",
    headers: {
      "apikey": SERVICE_ROLE_KEY,
      "Authorization": `Bearer ${SERVICE_ROLE_KEY}`,
      "Content-Type": "application/json",
      "Prefer": "return=minimal",
    },
    body: JSON.stringify({
      dni: dni ?? null,
      notebook,
      curso,
      reflexion_id,
      grado: grado ?? null,
      student_text,
      score,
      max_pts: spec.max_pts,
      comment,
      model: "deepseek-chat",
    }),
  }).catch(() => {});

  return jsonResponse({ score, comment, max_pts: spec.max_pts }, 200);
});
