/**
 * Caso 1 — Abriendo el Caso — Semana 1 (Google Sheets)
 * Autograder + envio a Supabase. Construido por ATLAS siguiendo el contrato de
 * ATLAS_Handoff_Caso1_Semana1_API_DB.md, verificado contra el .xlsx real
 * (Caso1_Semana1_AbriendoElCaso_v4.xlsx), no solo contra la prosa del handoff.
 *
 * INSTALACION (una vez por copia del Sheet):
 *   1. Abre el Google Sheet -> Extensiones -> Apps Script.
 *   2. Borra el contenido de Codigo.gs y pega este archivo completo.
 *   3. Guarda (Ctrl+S) y recarga el Sheet -> aparece el menu "🕵️ Caso 1".
 *   4. Corre "🔒 Proteger hoja (una sola vez)" desde el menu -- pide autorizacion
 *      la primera vez (protege 🔒 Clave y las columnas D/E de 🧩 Tu Caso).
 *   5. El boton "Enviar para calificar" del Sheet es solo un marcador visual
 *      (ver 🧩 Tu Caso!A70) -- el envio real ocurre por el menu, no por ese botón.
 *
 * DECISIONES DE PRODUCTO YA TOMADAS (ver conversacion con el usuario, no re-abrir):
 *   - Trigger: menu personalizado (onOpen), no dibujo ni onEdit.
 *   - Reenvios: libres, sin gating -- cada click en "Enviar" recalifica todo
 *     desde el estado actual del Sheet y hace un INSERT nuevo en `submissions`
 *     (tabla ya diseñada como historial de intentos, no upsert).
 *   - Dashboard/UI: fuera de alcance de este archivo -- otro agente la construye.
 *     Este script solo garantiza que el payload en Supabase sigue el mismo
 *     contrato de columnas que autograder_nb1_semana1.py (mismo proyecto/tabla).
 *
 * HALLAZGOS DE AUDITORIA (ATLAS) -- no corregidos aqui, documentados para SOFIA/usuario:
 *   1. 🗂️ Configuración!C8 trae "EST1_2026" hardcodeado en el .xlsx entregado, pero
 *      WORKFORCE_HANDOFF.md (2026-08-07) fijo "STAT_2026" como el unico curso id
 *      valido para Estadistica (coincide con `courses` seed en supabase_schema.sql).
 *      Este script IGNORA la celda y usa CURSO_ID hardcodeado abajo -- la celda del
 *      archivo maestro deberia corregirse para no confundir a quien la lea a mano.
 *   2. ex5 (fila 23): la formula visible del Sheet usa COUNTIF sobre la columna Día,
 *      y COUNTIF en Sheets compara texto sin distinguir mayusculas/minusculas -- por
 *      lo tanto la condicion "estandariza a exactamente 'Viernes'/'Sábado'" NUNCA
 *      puede fallar por casing (ya pasa incluso con "VIERNES"/"sábado" mezclados);
 *      el unico gate real de ex5 es heredado de ex4 (COUNTA=90). Este script REPLICA
 *      ese mismo comportamiento case-insensitive a proposito, para no crear un
 *      desfase entre el ✓ que el alumno ve en el Sheet y lo que el backend califica
 *      -- pero es una falla de diseño del ejercicio (SOFIA/GAUSS deberian revisarla,
 *      no es un bug de este script).
 */

// ─── Configuracion ────────────────────────────────────────────
var CURSO_ID          = 'STAT_2026'; // ver hallazgo #1 arriba -- no leer de la celda
var NOTEBOOK_ID        = 'sheets_caso1_semana1';
var SUPABASE_URL        = 'https://uwykikwutjtkpffwmdiq.supabase.co';
var SUPABASE_ANON_KEY   = 'sb_publishable_aBG6GD4wn9CgpSE-47fagQ_sNhnzznu';

var CORE_MAX  = 95; // 20 (ex1+ex2+t1+debug1) + 30 (ex4+ex5+ex6) + 5 (t2) + 30 (ex10+ex11+t3) + 10 (ex3+ex9 manual)
var BONUS_MAX = 10; // reto1, no cuenta para pct/level -- solo va en score_breakdown

var SH = {
  CONFIG: '🗂️ Configuración',
  CASE:   '🧩 Tu Caso',
  DATA:   '📊 Datos',
  KEY:    '🔒 Clave',
};

// Rango fijo de 108 filas -- se mantiene fijo a proposito (igual que las formulas
// originales del Sheet): cuando el alumno ELIMINA filas de verdad, Sheets recorre
// todo hacia arriba y deja vacio el final del rango fijo, en vez de acortarlo.
var DATA_FIRST_ROW = 5;
var DATA_LAST_ROW  = 112;

// ─── Menu ─────────────────────────────────────────────────────

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('🕵️ Caso 1')
    .addItem('📤 Enviar para calificar', 'submitCase')
    .addSeparator()
    .addItem('🔒 Proteger hoja (una sola vez)', 'protectSheet')
    .addToUi();
}

// ─── Envio principal ────────────────────────────────────────────

function submitCase() {
  var ui = SpreadsheetApp.getUi();
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  var config = readConfig_(ss);
  if (!config.nombre || !config.dni || !config.grado) {
    ui.alert('Faltan datos', 'Completa Nombre, DNI y Grado en 🗂️ Configuración antes de enviar.', ui.ButtonSet.OK);
    return;
  }

  var clave = readClave_(ss);
  var datos = readDatosRaw_(ss);
  var result = gradeAll_(ss, clave, datos);

  var payload = {
    email:           config.dni,
    dni:             config.dni,
    nombre:          config.nombre,
    grado:           config.grado,
    curso:           CURSO_ID,
    notebook:        NOTEBOOK_ID,
    earned:          result.earned,
    possible:        CORE_MAX,
    pct:             result.pct,
    level_num:       result.levelNum,
    level_name:      result.levelName,
    achievements:    result.achievements,
    streak:          result.streak,
    score_breakdown: result.breakdown,
  };

  var postResult = postToSupabase_(payload);

  var summary = buildSummaryText_(result);
  if (postResult.ok) {
    ui.alert('✅ Enviado', summary, ui.ButtonSet.OK);
  } else {
    ui.alert('⚠️ Calificado pero no se pudo enviar',
      summary + '\n\nError de red/Supabase: ' + postResult.error, ui.ButtonSet.OK);
  }
}

// ─── Lectura de datos crudos ─────────────────────────────────

function readConfig_(ss) {
  var sh = ss.getSheetByName(SH.CONFIG);
  return {
    nombre: String(sh.getRange('C4').getValue() || '').trim(),
    dni:    String(sh.getRange('C5').getValue() || '').trim(),
    grado:  String(sh.getRange('C6').getValue() || '').trim(),
  };
}

function readClave_(ss) {
  var sh = ss.getSheetByName(SH.KEY);
  var lastRow = sh.getLastRow();
  var vals = sh.getRange(2, 1, lastRow - 1, 2).getValues();
  var map = {};
  vals.forEach(function (row) {
    var k = row[0];
    if (k) map[String(k).trim()] = row[1];
  });
  return map;
}

function readDatosRaw_(ss) {
  var sh = ss.getSheetByName(SH.DATA);
  var vals = sh.getRange(DATA_FIRST_ROW, 1, DATA_LAST_ROW - DATA_FIRST_ROW + 1, 4).getValues();
  return vals.map(function (r) {
    return { comprador: r[0], boletos: r[1], dia: r[2], estado: r[3] };
  });
}

// ─── Helpers de comparacion ──────────────────────────────────

function normEq_(a, b) {
  return String(a == null ? '' : a).trim().toLowerCase() ===
         String(b == null ? '' : b).trim().toLowerCase();
}

function strictEq_(a, b) {
  return String(a == null ? '' : a).trim() === String(b == null ? '' : b).trim();
}

function isBlank_(v) {
  return v === '' || v === null || v === undefined;
}

function toNumber_(v) {
  var n = Number(v);
  return isNaN(n) ? null : n;
}

// ─── Calificacion ────────────────────────────────────────────

function gradeAll_(ss, clave, rows) {
  var caseSh = ss.getSheetByName(SH.CASE);
  var C = function (row) { return caseSh.getRange(row, 3).getValue(); }; // columna C
  var E = function (row) { return caseSh.getRange(row, 5).getValue(); }; // columna E

  var breakdown = {};
  var earned = 0;

  function record(key, pts, max, extra) {
    breakdown[key] = Object.assign({ e: pts, p: max }, extra || {});
    earned += pts;
    return pts === max;
  }

  // ── Estatica vs 🔒 Clave (numerica) ──
  var ex1_ok  = toNumber_(C(8))  !== null && toNumber_(C(8))  === toNumber_(clave['ex1']);
  var ex2_ok  = toNumber_(C(9))  !== null && toNumber_(C(9))  === toNumber_(clave['ex2']);
  var dbg1_ok = toNumber_(C(11)) !== null && toNumber_(C(11)) === toNumber_(clave['debug1']);
  var perfect = {};
  perfect.ex1     = record('ex1',     ex1_ok  ? 5 : 0, 5);
  perfect.ex2     = record('ex2',     ex2_ok  ? 5 : 0, 5);
  perfect.debug1  = record('debug1',  dbg1_ok ? 5 : 0, 5);

  // ── Estatica vs 🔒 Clave (opcion multiple, case-insensitive) ──
  perfect.t1 = record('t1', normEq_(C(10), clave['t1']) ? 5 : 0, 5);
  perfect.t2 = record('t2', normEq_(C(25), clave['t2']) ? 5 : 0, 5);
  perfect.t3 = record('t3', normEq_(C(56), clave['t3']) ? 10 : 0, 10);

  // ── Live-check contra 📊 Datos (ver hallazgo #2 sobre ex5) ──
  var targetValid = toNumber_(clave['ex4_target_count']);
  var validCount  = rows.filter(function (r) { return !isBlank_(r.comprador); }).length;
  var canceladoCount = rows.filter(function (r) { return normEq_(r.estado, 'Cancelado'); }).length;
  perfect.ex4 = record('ex4', (canceladoCount === 0 && validCount === targetValid) ? 10 : 0, 10);

  var diaCanonicoCount = rows.filter(function (r) {
    return normEq_(r.dia, 'Viernes') || normEq_(r.dia, 'Sábado');
  }).length;
  perfect.ex5 = record('ex5', (validCount === targetValid && diaCanonicoCount === targetValid) ? 10 : 0, 10);

  var targetSum = toNumber_(clave['ex6_target_sum']);
  var missingBoletos = rows.filter(function (r) {
    return !isBlank_(r.comprador) && isBlank_(r.boletos);
  }).length;
  var sumBoletos = rows.reduce(function (acc, r) {
    return acc + (typeof r.boletos === 'number' ? r.boletos : 0);
  }, 0);
  perfect.ex6 = record('ex6', (missingBoletos === 0 && sumBoletos === targetSum) ? 10 : 0, 10);

  // ── Numerica vs SUMIFS en vivo ──
  function sumifsDia_(dia) {
    return rows.reduce(function (acc, r) {
      return acc + (normEq_(r.dia, dia) && typeof r.boletos === 'number' ? r.boletos : 0);
    }, 0);
  }
  var sumSabado  = sumifsDia_('Sábado');
  var sumViernes = sumifsDia_('Viernes');
  perfect.ex10 = record('ex10', (toNumber_(C(54)) === sumSabado)  ? 10 : 0, 10);
  perfect.ex11 = record('ex11', (toNumber_(C(55)) === sumViernes) ? 10 : 0, 10);

  // ── Revision del profesor (manual, sin gating -- lee lo que haya ahora mismo) ──
  var ex3Pts = Math.max(0, Math.min(5, toNumber_(E(21)) || 0));
  var ex9Pts = Math.max(0, Math.min(5, toNumber_(E(53)) || 0));
  record('ex3', ex3Pts, 5, { kind: 'teacher_review' });
  record('ex9', ex9Pts, 5, { kind: 'teacher_review' });

  // ── Bonus (no cuenta para earned/pct/level) ──
  var expectedReto1 = sumViernes === sumSabado ? 'Empate' : (sumViernes > sumSabado ? 'Viernes' : 'Sábado');
  var reto1Ok  = strictEq_(C(61), expectedReto1);
  var reto1Pts = reto1Ok ? BONUS_MAX : 0;
  breakdown['reto1'] = { e: reto1Pts, p: BONUS_MAX, kind: 'bonus' };

  var pct = Math.min(Math.round((earned / CORE_MAX) * 100), 100);
  var level = computeLevel_(pct);
  var achievements = computeAchievements_(perfect, pct);
  var streak = computeStreak_(perfect);

  return {
    earned: earned,
    pct: pct,
    levelNum: level.num,
    levelName: level.name,
    achievements: achievements,
    streak: streak,
    breakdown: breakdown,
  };
}

// ─── Nivel / logros / racha ──────────────────────────────────
// Nombres provisionales reusando el vocabulario que YA existe en el Sheet
// (Expediente/Agente/Detective/Caso) -- no es un tema nuevo de PIXEL, solo
// texto de placeholder consistente hasta que haya un Theme Brief formal.

var LEVELS = [
  [96, 6, '👑 Detective del Caso Resuelto'],
  [81, 5, '⭐ Detective Estrella'],
  [61, 4, '📁 Detective Senior'],
  [41, 3, '🕵️ Detective de Campo'],
  [21, 2, '🔍 Investigador Junior'],
  [0,  1, '🗒️ Agente en Entrenamiento'],
];

function computeLevel_(pct) {
  for (var i = 0; i < LEVELS.length; i++) {
    if (pct >= LEVELS[i][0]) return { num: LEVELS[i][1], name: LEVELS[i][2] };
  }
  return { num: 1, name: LEVELS[LEVELS.length - 1][2] };
}

function computeAchievements_(perfect, pct) {
  var ach = [];
  if (perfect.ex1 || perfect.ex2 || perfect.t1 || perfect.debug1 ||
      perfect.ex4 || perfect.ex5 || perfect.ex6 || perfect.t2 ||
      perfect.ex10 || perfect.ex11 || perfect.t3) {
    ach.push('primer_indicio');
  }
  if (perfect.ex4 && perfect.ex5 && perfect.ex6) ach.push('caso_limpio');
  if (perfect.ex10 && perfect.ex11 && perfect.t3) ach.push('filtro_perfecto');
  if (pct >= 100) ach.push('expediente_resuelto');
  return ach;
}

function computeStreak_(perfect) {
  // Racha = corrida final de items perfectos en orden del Sheet (ex3/ex9 excluidos
  // a proposito: son de revision manual, no deberian romper la racha del alumno
  // mientras el profesor todavia no las califica).
  var order = ['ex1', 'ex2', 't1', 'debug1', 'ex4', 'ex5', 'ex6', 't2', 'ex10', 'ex11', 't3'];
  var streak = 0;
  order.forEach(function (key) {
    if (perfect[key]) streak++; else streak = 0;
  });
  return streak;
}

// ─── Supabase ────────────────────────────────────────────────

function postToSupabase_(payload) {
  try {
    var response = UrlFetchApp.fetch(SUPABASE_URL + '/rest/v1/submissions', {
      method: 'post',
      contentType: 'application/json',
      headers: {
        apikey: SUPABASE_ANON_KEY,
        Authorization: 'Bearer ' + SUPABASE_ANON_KEY,
        Prefer: 'return=minimal',
      },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true,
    });
    var code = response.getResponseCode();
    if (code >= 200 && code < 300) return { ok: true };
    return { ok: false, error: 'HTTP ' + code + ': ' + response.getContentText() };
  } catch (err) {
    return { ok: false, error: String(err) };
  }
}

// ─── Resumen para el usuario ─────────────────────────────────

function buildSummaryText_(result) {
  var lines = [];
  lines.push('XP: ' + result.earned + ' / ' + CORE_MAX + ' (' + result.pct + '%)');
  lines.push('Nivel: ' + result.levelName);
  if (result.achievements.length) lines.push('Logros: ' + result.achievements.join(', '));
  if (result.streak >= 2) lines.push('Racha: x' + result.streak);
  var bonus = result.breakdown['reto1'];
  if (bonus) lines.push('Bonus (reto1): ' + bonus.e + ' / ' + bonus.p);
  return lines.join('\n');
}

// ─── Proteccion (§6.3 del handoff) ───────────────────────────

function protectSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var ui = SpreadsheetApp.getUi();

  var keySh = ss.getSheetByName(SH.KEY);
  var existing = keySh.getProtections(SpreadsheetApp.ProtectionType.SHEET);
  if (existing.length === 0) {
    var p = keySh.protect().setDescription('Clave de respuestas -- no editar');
    p.removeEditors(p.getEditors());
    if (p.canDomainEdit()) p.setDomainEdit(false);
  }
  keySh.hideSheet();

  var caseSh = ss.getSheetByName(SH.CASE);
  var lastRow = caseSh.getMaxRows();
  var existingRangeProtections = caseSh.getProtections(SpreadsheetApp.ProtectionType.RANGE);
  var alreadyProtectedCols = existingRangeProtections.map(function (p) {
    return p.getRange().getColumn();
  });
  ['D', 'E'].forEach(function (col) {
    var colIndex = caseSh.getRange(col + '1').getColumn();
    if (alreadyProtectedCols.indexOf(colIndex) !== -1) return; // ya protegida, evita duplicados
    var range = caseSh.getRange(col + '1:' + col + lastRow);
    var p = range.protect();
    p.setDescription('Resultado/XP calculado -- no editar');
    p.removeEditors(p.getEditors());
    if (p.canDomainEdit()) p.setDomainEdit(false);
  });

  ui.alert('🔒 Protegido', '🔒 Clave protegida y oculta. Columnas D/E de 🧩 Tu Caso protegidas.', ui.ButtonSet.OK);
}
