/**
 * Collect the STAT 3ro-5to Colab notebooks (NB1-NB5) shared with you and drop
 * them into this spreadsheet, one row per student, one column per notebook.
 *
 *   NB1  nb1_semana1_recuperacion_datos   (Liga Pokemon de Datos)
 *   NB2  nb1_semana2_recuperacion_datos   (Juegos Olimpicos de Datos)
 *   NB3  nb3_correlacion / nb3_lite_correlacion
 *   NB4  nb4_correlacion / nb4_lite_correlacion
 *   NB5  nb5_regresion                    (El Oraculo de Datos)
 *
 * Notebooks are identified by their CONTENTS: every copy keeps the setup cell that
 * downloads its autograder (autograder_nb3.py, autograder_nb4_lite.py, ...), so a file
 * renamed "Tarea Juan final.ipynb" is still recognised. Only if that fails (file can't
 * be read, setup cell deleted) does it fall back to the file name; those cells get a "*".
 * Each cell is a clickable link labelled with the last-edit date; "(lite)" marks the
 * lite version. If a student shared more than one copy of the same notebook, the most
 * recently edited one goes in the column and the rest go to "Duplicados".
 * Colab files that can't be identified (or are other notebooks, e.g. nb6) go to
 * "Sin clasificar".
 *
 * Reading every notebook is slow, so results are cached per file version: the first
 * run may stop early with a "run it again" message; later runs are fast.
 *
 * SETUP:
 * 1. Open your tracker Google Sheet.
 * 2. Extensions > Apps Script.
 * 3. Delete any placeholder code, paste this whole file in.
 * 4. Click "Run" (the ▶ button) with collectSharedColabLinks selected.
 * 5. First run: it'll ask you to authorize Drive + Sheets access — approve it.
 * 6. Check the "Colab Links" tab that gets created in your spreadsheet.
 *
 * Re-run any time (e.g. after new notebooks are shared) — it clears and
 * rebuilds the tab so you don't get duplicates.
 */

// Autograder id found inside the notebook -> column.
const AUTOGRADER_TO_KEY = {
  nb1_semana1: 'NB1',
  nb1_semana2: 'NB2',
  nb3: 'NB3', nb3_lite: 'NB3',
  nb4: 'NB4', nb4_lite: 'NB4',
  nb5: 'NB5',
};

// Fallback when the contents don't say which notebook it is.
// Order matters: semana2 is checked before semana1 because both names contain "nb1".
const NOTEBOOKS = [
  { key: 'NB2', pattern: /semana\s*_?2|ol[ií]mpic/i },
  { key: 'NB1', pattern: /semana\s*_?1|pok[eé]mon|\bnb1\b|nb1_/i },
  { key: 'NB3', pattern: /nb\s*_?3/i },
  { key: 'NB4', pattern: /nb\s*_?4/i },
  { key: 'NB5', pattern: /nb\s*_?5|regresi[oó]n|or[aá]culo/i },
];
const NB_KEYS = ['NB1', 'NB2', 'NB3', 'NB4', 'NB5'];

// Stop reading file contents after this long so the run finishes inside Apps
// Script's 6-minute limit; unread files fall back to the name for this run.
const CONTENT_BUDGET_MS = 4.5 * 60 * 1000;
const CACHE_SHEET = '_colab_cache'; // hidden tab: fileId | lastUpdated ms | autograder id

/**
 * Returns the autograder id ('nb3', 'nb4_lite', ...) the notebook loads, '' if it
 * loads none of ours, or null if the file couldn't be read.
 */
function readAutograderId_(file) {
  let text;
  try {
    text = file.getBlob().getDataAsString();
  } catch (e) {
    return null;
  }
  const ids = [];
  const re = /autograder_(nb\d(?:_semana\d)?(?:_lite)?)\.py/g;
  let m;
  while ((m = re.exec(text)) !== null) ids.push(m[1]);
  if (ids.length === 0) return '';
  // Lite notebooks also mention the full autograder; the lite one wins.
  return ids.find(id => /_lite$/.test(id)) || ids[0];
}

function collectSharedColabLinks() {
  const SHEET_NAME = 'Colab Links';
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const tz = ss.getSpreadsheetTimeZone();

  // Create or clear the output tab
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (sheet) {
    sheet.clear();
  } else {
    sheet = ss.insertSheet(SHEET_NAME);
  }

  // Colab notebooks shared with me. Native Colab files have the colaboratory
  // mimeType; .ipynb files uploaded straight to Drive have the json one.
  const query =
    "(mimeType = 'application/vnd.google.colaboratory' or mimeType = 'application/x-ipynb+json')" +
    " and sharedWithMe = true and trashed = false";
  const files = DriveApp.searchFiles(query);

  // fileId -> { v: lastUpdated ms, id: autograder id or '' }. Only re-read a file
  // when it has been edited since the last run.
  let cacheSheet = ss.getSheetByName(CACHE_SHEET);
  if (!cacheSheet) {
    cacheSheet = ss.insertSheet(CACHE_SHEET);
    cacheSheet.hideSheet();
  }
  const oldCache = {};
  if (cacheSheet.getLastRow() > 0) {
    cacheSheet.getRange(1, 1, cacheSheet.getLastRow(), 3).getValues()
      .forEach(([id, v, ag]) => (oldCache[id] = { v: Number(v), id: String(ag) }));
  }
  const newCache = {};
  const started = Date.now();
  let skippedReads = 0;

  // email -> { name, slots: {NB1: [nb, ...], ...}, unmatched: [nb, ...] }
  const byOwner = {};

  while (files.hasNext()) {
    const file = files.next();
    const owner = file.getOwner();
    const ownerEmail = owner ? owner.getEmail() : 'Unknown';
    const ownerName = owner ? owner.getName() : 'Unknown';

    if (!byOwner[ownerEmail]) {
      byOwner[ownerEmail] = { name: ownerName, slots: {}, unmatched: [] };
      NB_KEYS.forEach(k => (byOwner[ownerEmail].slots[k] = []));
    }

    const title = file.getName();
    const lastUpdated = file.getLastUpdated();
    const fileId = file.getId();

    // 1) Contents (cached per version)
    let agId = null;
    const cached = oldCache[fileId];
    if (cached && cached.v === lastUpdated.getTime()) {
      agId = cached.id;
    } else if (Date.now() - started < CONTENT_BUDGET_MS) {
      agId = readAutograderId_(file);
    } else {
      skippedReads++;
    }
    if (agId !== null) newCache[fileId] = { v: lastUpdated.getTime(), id: agId };

    const nb = { title: title, url: file.getUrl(), lastUpdated: lastUpdated, byName: false };
    let key = agId ? AUTOGRADER_TO_KEY[agId] : null;
    if (key) {
      nb.lite = /_lite$/.test(agId);
    } else if (!agId) {
      // 2) File name, only when contents gave nothing (an nb6 notebook is
      //    identified as nb6 and correctly left out, even if renamed "nb5").
      const match = NOTEBOOKS.find(n => n.pattern.test(title));
      if (match) {
        key = match.key;
        nb.lite = /lite/i.test(title);
        nb.byName = true;
      }
    }

    if (key) {
      byOwner[ownerEmail].slots[key].push(nb);
    } else {
      byOwner[ownerEmail].unmatched.push(nb);
    }
  }

  const cacheRows = Object.keys(newCache).map(id => [id, newCache[id].v, newCache[id].id]);
  cacheSheet.clear();
  if (cacheRows.length > 0) {
    cacheSheet.getRange(1, 1, cacheRows.length, 3).setNumberFormat('@').setValues(cacheRows);
  }

  const header = ['Student', 'Email'].concat(NB_KEYS, ['Entregados', 'Duplicados', 'Sin clasificar']);
  const emails = Object.keys(byOwner).sort((a, b) =>
    byOwner[a].name.localeCompare(byOwner[b].name)
  );

  // Build every cell as a RichTextValue so one cell can hold several links
  // (needed for the Duplicados / Sin clasificar columns).
  const plain = text => SpreadsheetApp.newRichTextValue().setText(String(text)).build();
  const links = (items, labelFn) => {
    if (items.length === 0) return plain('');
    const labels = items.map(labelFn);
    const builder = SpreadsheetApp.newRichTextValue().setText(labels.join(', '));
    let pos = 0;
    items.forEach((item, i) => {
      builder.setLinkUrl(pos, pos + labels[i].length, item.url);
      pos += labels[i].length + 2;
    });
    return builder.build();
  };
  const fmtDate = d => Utilities.formatDate(d, tz, 'dd/MM');
  const nbLabel = (key, nb) =>
    `${key}${nb.lite ? ' (lite)' : ''} · ${fmtDate(nb.lastUpdated)}${nb.byName ? ' *' : ''}`;

  const rows = [header.map(plain)];
  emails.forEach(email => {
    const student = byOwner[email];
    const row = [plain(student.name), plain(email)];
    const duplicates = [];
    let delivered = 0;

    NB_KEYS.forEach(key => {
      // Newest copy first; the newest one is the one that counts.
      const copies = student.slots[key].sort((a, b) => b.lastUpdated - a.lastUpdated);
      if (copies.length > 0) delivered++;
      row.push(links(copies.slice(0, 1), nb => nbLabel(key, nb)));
      copies.slice(1).forEach(nb => duplicates.push({ url: nb.url, key: key, nb: nb }));
    });

    row.push(plain(`${delivered}/${NB_KEYS.length}`));
    row.push(links(duplicates, d => nbLabel(d.key, d.nb)));
    row.push(links(student.unmatched, nb => nb.title.replace(/\.ipynb$/i, '')));
    rows.push(row);
  });

  sheet.getRange(1, 1, rows.length, header.length).setRichTextValues(rows);
  sheet.getRange(1, 1, 1, header.length).setFontWeight('bold');
  sheet.setFrozenRows(1);
  sheet.setFrozenColumns(1);
  sheet.autoResizeColumns(1, header.length);

  sheet.getRange(1, 3).setNote('* = identified by file name only (contents unreadable or setup cell deleted). Check it.');

  let msg = `Done! Found ${emails.length} student(s) with shared Colab notebooks.`;
  if (skippedReads > 0) {
    msg += `\n\n${skippedReads} notebook(s) weren't opened yet (time limit) and were sorted by ` +
           `file name for now. Run it again to finish — opened notebooks are remembered.`;
  }
  SpreadsheetApp.getUi().alert(msg);
}
