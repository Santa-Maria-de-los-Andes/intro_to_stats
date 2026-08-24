"""
Autograder — Bimestre 3, Mision 2: Buscando Patrones — SEMANA 3
RUTA DE INTERPRETACION (accesibilidad / inclusion)

Companion, not a replacement, for autograder_nb3.py: same dataset, same
narrative, same 7 preguntas de teoria (t1-t7) y las mismas 3 reflexiones
(ronda1, ronda3, concepto) -- ninguna de las cuales requiere escribir
codigo (confirmado contra autograder_nb3.py's _TEORIA dict antes de
construir esta ruta). Lo unico que se quita es check_ex1-ex4: en
nb3_lite_correlacion.ipynb las cuatro rondas de "Grafica y Calcula" se
presentan ya resueltas (celdas 👀 OBSERVA con el codigo de referencia ya
escrito) en vez de como ejercicios 🔨 CONSTRUYE en blanco.

SUBCLASA autograder_nb3.Autograder en vez de reescribir el motor de teoria/
reflexion/gamificacion/Supabase -- ese motor (formularios HTML, DeepSeek via
grade-reflexion, tarjetas de XP/logros, envio a Supabase) es identico para
esta ruta, no hay ninguna razon pedagogica o tecnica para duplicarlo.

Requiere que autograder_nb3.py este disponible en el runtime (el notebook
lo wget-ea igual que a este archivo, en la celda de setup) -- este archivo
hace `import autograder_nb3` y hereda de su clase Autograder.

Notas de scoring:
  t1-t7 (idem autograder_nb3.py) = 35 pts.
  3 reflexiones (ronda1, ronda3, concepto; idem autograder_nb3.py) = 15 pts.

  2026-08-23 -- se agrego el "Quiz de Cierre" (t8-t11) que se sumo a
  autograder_nb3.py el 2026-08-21, mismo pedido del usuario ("agrega las
  preguntas de cierre tambien a la version lite"). t9-t11 (los tres
  escenarios nuevos: helado/ahogamientos, zapatos/lectura, pares al azar)
  no mencionan el dataset en absoluto, asi que se heredan sin cambios. t8
  SI se sobreescribe: la version base pregunta por "Rondas 1 a 6" e incluye
  una opcion sobre la Ronda 6 (Generosidad vs. Percepcion de corrupcion),
  pero esta ruta solo tiene Rondas 1-4 (sin Ronda 5/6, que en nb3_correlacion
  son ejercicios 🔨 CONSTRUYE que no existen aqui) -- mismo patron que
  autograder_nb4_lite.py usa para su t11 (`_TEORIA = {**_base..., 8: dict(...)}`).
  _CORE_MAX = 70 (35 + 15 + 20). Sin check_ex, sin bonus.

NOTEBOOK_ID/_CORE_MAX: se reasignan como atributos del MODULO autograder_nb3
(no de este archivo) porque cada metodo heredado (_submit_to_supabase,
_totals, _award_reflexion...) resuelve esos nombres contra el __globals__ de
SU PROPIO modulo de definicion (autograder_nb3.py), no contra el de esta
subclase -- una asignacion local aqui seria invisible para ellos. Notebook id
distinto ("nb3_lite") para que estos envios no se mezclen ni se comparen por
porcentaje con la tabla de posiciones de la ruta con codigo.

⚠️ CONSECUENCIA DE ESE MISMO MECANISMO -- IMPORTANTE PARA QUIEN ESCRIBA TESTS:
importar este archivo MUTA in-place el modulo `autograder_nb3` ya cargado en
`sys.modules` (NOTEBOOK_ID/_CORE_MAX quedan en "nb3_lite"/50 para CUALQUIER
codigo que despues siga usando ese modulo en el MISMO proceso de Python,
incluido un `autograder_nb3.Autograder()` instanciado directamente). En
produccion esto nunca pasa -- cada notebook Colab es un kernel nuevo que
wget-ea e importa un solo autograder -- pero un script de validacion que
pruebe nb3.py y nb3_lite.py juntos en un solo proceso SI se ve afectado:
probar cada archivo en su propio subproceso (`python -c "..."` separado por
archivo), no con imports compartidos en un solo script.
"""
import autograder_nb3 as _base

_base.NOTEBOOK_ID = "nb3_lite"
_base._CORE_MAX   = 70   # 35 (t1-7) + 15 (3 reflexiones) + 20 (Quiz de Cierre t8-11)


class Autograder(_base.Autograder):
    """Misma teoria/reflexion que autograder_nb3.py -- sin check_ex1-6."""

    # t8 se reescribe para esta ruta (solo Rondas 1-4, sin Ronda 5/6) --
    # t9-t11 (los tres escenarios nuevos, sin dataset) se heredan tal cual.
    _TEORIA = {**_base.Autograder._TEORIA, 8: dict(
        title="Quiz de Cierre 1 — La correlación más fuerte de hoy",
        q=("De todos los pares que viste hoy (Rondas 1 a 4), ¿cuál tuvo el r "
           "más alto -- la relación más fuerte?"),
        opts={"a": "Percepción de corrupción vs. Puntaje (Ronda 1)",
              "b": "PBI per cápita vs. Esperanza de vida saludable (Ronda 3)",
              "c": "Esperanza de vida saludable vs. Puntaje (Ronda 2)",
              "d": "Apoyo social vs. Esperanza de vida saludable (Ronda 4)"},
        correct="b",
        why=("PBI per cápita vs. Esperanza de vida saludable dio r ≈ 0.835 en la "
             "Ronda 3 -- el r más alto de los pares que viste hoy."),
        pts=5,
    )}

    # ═══════════════════════════════════════════════════════════
    # CHECKPOINT -- fin de la Semana 3 (solo teoria; sin rondas de codigo)
    # ═══════════════════════════════════════════════════════════

    def check_mini_a(self):
        """Checkpoint — fin de la Semana 3, Clase 1 (ruta de interpretacion)"""
        self._checkpoints.add("mini_a")
        seccion = {
            "t1": ("T1 — Qué mide el coeficiente de correlación", 5),
            "t2": ("T2 — El rango de -1 a 1", 5),
            "t3": ("T3 — r cercano a 0", 5),
            "t4": ("T4 — Fuerza vs. dirección", 5),
            "t5": ("T5 — Correlación no es causalidad", 5),
            "t6": ("T6 — El límite de .corr()", 5),
            "t7": ("T7 — Ronda 3, antes de calcular", 5),
            "t8": ("Quiz de Cierre 1 — la correlación más fuerte de hoy", 5),
            "t9": ("Quiz de Cierre 2 — helado y ahogamientos", 5),
            "t10": ("Quiz de Cierre 3 — zapatos y lectura", 5),
            "t11": ("Quiz de Cierre 4 — probar muchos pares al azar", 5),
        }
        self._render_checkpoint("CHECKPOINT — FIN DE LA SEMANA 3", seccion, "#4aa8d8")

    # ═══════════════════════════════════════════════════════════
    # LOGROS -- mismas claves que autograder_nb3.py (resumen() hereda su
    # propio ach_display sin cambios, asi que reusar las claves existentes
    # es lo que evita tener que sobreescribir resumen() entero solo para
    # una tabla de etiquetas) -- las condiciones de desbloqueo se adaptan a
    # lo que esta ruta realmente califica (teoria + reflexion, no ex1-4).
    # ═══════════════════════════════════════════════════════════

    def _check_achievements(self, key):
        unlocked = []
        earned, possible, pct = self._totals()

        if any(e > 0 for e, _ in self._scores.values()) and self._unlock("primer_rayo"):
            unlocked.append(("☀️ Primer Rayo de Sol — ¡Tu primer punto de felicidad conquistado!", "#ff9e2c", "Chispa"))

        # Cazador de Patrones (reutilizado) -- las 7 preguntas de teoria de
        # Semana 3, perfectas (reemplaza el trigger original de ex1-4, que
        # no existe en esta ruta)
        t_rondas = ["t1", "t2", "t3", "t4", "t5", "t6", "t7"]
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1] for k in t_rondas)
                and self._unlock("cazador_patrones")):
            unlocked.append(("🗺️ Cazador de Patrones — Tus siete preguntas de teoría de Semana 3, perfectas", "#4aa8d8", "Rayo"))

        if (self._scores.get("refl_concepto", (0, 1))[0] == self._scores.get("refl_concepto", (0, 1))[1]
                and "refl_concepto" in self._scores and self._unlock("pensador_conceptual")):
            unlocked.append(("🧠 Pensador Conceptual — Explicaste el coeficiente sin apoyarte en ningún dataset", "#ffb703", "Amanecer"))

        if self._streak >= 5 and self._unlock("racha_bienestar"):
            unlocked.append(("🔥 Racha de Bienestar — Combo x5", "#4aa8d8", "Rayo"))

        if pct >= 100 and self._unlock("felicidad_plena"):
            unlocked.append(("🏆 Felicidad Plena — 100% de la Semana 3", "#ff9e2c", "Sol Pleno"))

        lvl_num, lvl_name = _base._level_info(pct)
        if lvl_num > self._prev_level and self._prev_level > 0:
            unlocked.append((f"⬆️ ¡SUBISTE DE NIVEL! — {lvl_name}", "#4aa8d8", "Nivel"))
        if lvl_num > self._prev_level:
            self._prev_level = lvl_num

        return unlocked
