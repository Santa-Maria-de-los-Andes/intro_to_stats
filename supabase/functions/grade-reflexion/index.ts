// supabase/functions/grade-reflexion/index.ts
//
// Califica celdas "💭 Reflexiona" de nb3_semana3_correlacion.ipynb (y
// notebooks futuros que reusen el mismo patron) via DeepSeek (deepseek-chat).
// La clave de DeepSeek vive solo aca (Supabase secret DEEPSEEK_API_KEY) --
// nunca en el notebook, igual que `submissions` nunca expuso una clave con
// alcance real (solo el anon key, restringido por RLS).
//
// Contrato: POST {dni, notebook, curso, reflexion_id, student_text, grado}
//           -> {score, comment, max_pts}  |  {error: "..."} (4xx/5xx)
//
// El caller (autograder_nb3_semana3.py) NO debe interpretar un error como
// "el alumno saco 0" -- debe reintentar/pedir de nuevo, nunca calificar en
// base a un fallo de esta funcion.

const DEEPSEEK_API_KEY = Deno.env.get("DEEPSEEK_API_KEY")!;
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

const EXPECTED_NOTEBOOK = "nb3_semana3";
const EXPECTED_CURSO = "STAT_2026";

type ReflexionSpec = {
  question: string;
  grounding: string;
  grading_notes: string;
  max_pts: number;
};

// Preguntas, valores reales (verificados contra 2019_es.csv, nunca
// estimados -- misma disciplina que el resto del notebook) y criterio de
// calificacion por celda. Orden = orden de aparicion en el notebook.
const GRADING_NOTES: Record<string, ReflexionSpec> = {
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
      'En una frase: comparando los dos scatter que construiste hoy ("Percepción de corrupción" y "Esperanza de vida saludable"), ¿cual te parecio visualmente mas fuerte?',
    grounding:
      "r real: Percepción de corrupción vs Puntaje = 0.386; Esperanza de vida saludable vs Puntaje = 0.780 -- Esperanza es visualmente la relacion mas fuerte. Igual que en a1, es observacion pre-calculo -- no penalices si 'vio' distinto, solo evalua si comparo genuinamente los dos graficos.",
    grading_notes:
      "Credito si compara explicitamente los dos scatters (no solo describe uno). Sin credito si esta vacia, es generica, o no hace una comparacion real entre los dos.",
    max_pts: 5,
  },
  guiado: {
    question:
      'En una frase, y sin usar la palabra "causa": ¿que te dice un r ≈ 0.78 sobre la relacion entre "Apoyo social" y "Puntaje"?',
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

  if (notebook !== EXPECTED_NOTEBOOK || curso !== EXPECTED_CURSO) {
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

  // deno-lint-ignore no-explicit-any
  let deepseekJson: any;
  try {
    const dsResp = await fetch("https://api.deepseek.com/chat/completions", {
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
          { role: "user", content: student_text },
        ],
        tools: [tool],
        tool_choice: { type: "function", function: { name: "submit_grade" } },
      }),
      signal: AbortSignal.timeout(15000),
    });
    if (!dsResp.ok) {
      return jsonResponse({ error: "grading_failed" }, 502);
    }
    deepseekJson = await dsResp.json();
  } catch {
    return jsonResponse({ error: "grading_failed" }, 502);
  }

  // Enforcement, capa 2: no confiar en la forma solo porque DeepSeek
  // devolvio 200 -- validar tipo/rango antes de usar nada.
  let score: number | undefined;
  let comment: string | undefined;
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
        score = args.score;
        comment = args.comment;
      }
    }
  } catch {
    // score/comment quedan undefined -> tratado como fallo abajo
  }

  if (score === undefined || comment === undefined) {
    return jsonResponse({ error: "grading_failed" }, 502);
  }

  score = Math.max(0, Math.min(spec.max_pts, Math.round(score)));

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
