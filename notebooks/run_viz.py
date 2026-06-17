"""
run_viz.py — Execute quick_viz_4.ipynb selected cells and export HTML

Usage:
    python run_viz.py

What it does:
    1. Loads quick_viz_4.ipynb
    2. Skips all cells beginning with %%script false
    3. Executes every other code cell in sequence in a shared namespace
    4. Collects Plotly HTML divs via the plotly_capture() helper
    5. Writes visualisations/quick_viz_4.html

Run from the project root:
    cd MedicalPlatform_FA_Snapshot
    python notebooks/run_viz.py
"""

import json
import sys
import traceback
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# ---- Paths (relative to this script -- works on any machine) ----
# Script lives at: MedicalPlatform_FA_Snapshot/notebooks/run_viz.py
# parent.parent resolves to MedicalPlatform_FA_Snapshot/ on every machine
BASE_DIR  = Path(__file__).resolve().parent.parent   # MedicalPlatform_FA_Snapshot/
NB_PATH   = BASE_DIR / 'notebooks'      / 'quick_viz_4.ipynb'
HTML_PATH = BASE_DIR / 'visualisations' / 'quick_viz_4.html'
DATA_DIR  = BASE_DIR / 'data'
HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
print(f'Project root : {BASE_DIR}')

# ---- Load notebook ----
print(f'Loading {NB_PATH.name}...')
with open(NB_PATH, encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
code_cells = [c for c in cells if c['cell_type'] == 'code']
selected   = [c for c in code_cells
              if not ''.join(c['source']).startswith('%%script false')]

print(f'  Total code cells : {len(code_cells)}')
print(f'  Disabled (skipped): {len(code_cells) - len(selected)}')
print(f'  Will execute      : {len(selected)}')
print()

# ---- Shared execution namespace ----
# matplotlib in non-interactive mode so plt.show() does not block
import matplotlib
matplotlib.use('Agg')

ns = {'__name__': '__main__', 'BASE_DIR': BASE_DIR}

# Patch %matplotlib inline — safe no-op in script context
import builtins
_real_exec = builtins.__dict__.get('exec', exec)

def _safe_exec(src, globs, locs=None):
    # Strip IPython magic lines before executing
    cleaned = '\n'.join(
        line for line in src.splitlines()
        if not line.strip().startswith('%')
    )
    _real_exec(cleaned, globs, locs)

# ---- Execute cells ----
errors = []
for idx, cell in enumerate(selected, start=1):
    src = ''.join(cell['source'])

    # Strip IPython magics
    src_clean = '\n'.join(
        line for line in src.splitlines()
        if not line.strip().startswith('%')
    )

    # Identify cell by first non-blank line
    first_line = next((l.strip() for l in src.splitlines() if l.strip()), f'cell {idx}')
    label = first_line[:80]

    try:
        exec(compile(src_clean, f'<cell {idx}>', 'exec'), ns)
        print(f'  [{idx:02d}/{len(selected)}] OK   {label}')
    except Exception as e:
        print(f'  [{idx:02d}/{len(selected)}] FAIL {label}')
        print(f'         {type(e).__name__}: {e}')
        errors.append((idx, label, traceback.format_exc()))

print()

# ---- Report errors ----
if errors:
    print(f'Completed with {len(errors)} error(s):\n')
    for i, label, tb in errors:
        print(f'  Cell {i}: {label}')
        print(f'  {tb.splitlines()[-1]}')
        print()
else:
    print('All cells executed successfully.')
    print()

# ---- Build HTML from collected Plotly divs ----
HTML_DIVS = ns.get('HTML_DIVS', [])
print(f'Plotly charts captured: {len(HTML_DIVS)}')

if not HTML_DIVS:
    print('No charts captured — check that plotly_capture() ran correctly.')
    sys.exit(1)

# Selected chart numbers for the output (matches approved selection)
# All charts in HTML_DIVS are already the filtered set since disabled cells
# are skipped, so we export all of them.
# Topic map: chart title prefix -> topic label
TOPIC_MAP = {
    '0.': 'Topic 0 -- Business Overview',
    '1.': 'Topic 1 -- Revenue Analysis',
    '2.': 'Topic 2 -- Pricing Analysis',
    '3.': 'Topic 3 -- Volume & Cancellation',
    '4.': 'Topic 4 -- Cost Analysis',
    '5.': 'Topic 5 -- Margin Analysis',
    '7.': 'Topic 7 -- Doctor Economics',
    '8.': 'Topic 8 -- Patient Economics',
}

def get_topic(title):
    for prefix, label in TOPIC_MAP.items():
        if title.lstrip().startswith(prefix):
            return label
    return ''

# Group charts by topic for the header breakdown
from collections import OrderedDict
topic_groups = OrderedDict()
for i, (title, _) in enumerate(HTML_DIVS):
    t = get_topic(title)
    if t not in topic_groups:
        topic_groups[t] = []
    topic_groups[t].append((i+1, title.split('(')[0].strip()))

# Build topic breakdown section
breakdown = ''
for topic, items in topic_groups.items():
    links = ' '.join(f'<a href="#chart{n}">{n}</a>' for n, _ in items)
    breakdown += f'<div class="topic-row"><span class="topic-label">{topic}</span><span class="topic-links">{links}</span></div>'

# Build cards with topic badge above each topic group
prev_topic = None
cards = ''
for i, (title, div) in enumerate(HTML_DIVS):
    t = get_topic(title)
    if t != prev_topic:
        cards += f'<div class="topic-divider" id="topic-{i+1}"><span>{t}</span></div>\n'
        prev_topic = t
    cards += f'<div class="card" id="chart{i+1}"><div class="topic-badge">{t}</div><h3>{i+1}. {title}</h3>{div}</div>\n'

nav = ''.join(
    f'<a href="#chart{i+1}">{i+1}. {title.split("(")[0].strip()}</a>'
    for i, (title, _) in enumerate(HTML_DIVS)
)

df_done = ns.get('df_done')
df_all  = ns.get('df_all')
n_done  = f'{len(df_done):,}' if df_done is not None else '—'
n_all   = f'{len(df_all):,}'  if df_all  is not None else '—'

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Medical Platform — Financial Analysis v4</title>
<style>
  body   {{font-family:Arial,sans-serif;background:#f4f6f9;margin:0;padding:20px;color:#2c3e50}}
  header {{background:#27AE60;color:white;padding:24px 32px;border-radius:8px;margin-bottom:20px}}
  header h1 {{margin:0 0 6px;font-size:1.5em}}
  header p  {{margin:0;opacity:.85;font-size:.9em}}
  nav    {{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:22px;padding:12px 16px;
            background:white;border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,.07)}}
  nav a  {{background:#f0faf5;border:1px solid #b2dfce;border-radius:16px;
            padding:4px 12px;font-size:.78em;text-decoration:none;color:#27AE60;white-space:nowrap}}
  nav a:hover {{background:#27AE60;color:white}}
  .card  {{background:white;border-radius:8px;padding:18px 22px;
            box-shadow:0 2px 8px rgba(0,0,0,.08);margin-bottom:18px}}
  .card h3 {{margin:0 0 8px;color:#27AE60;font-size:.95em}}
  .topic-badge {{font-size:.72em;font-weight:500;color:#fff;background:#2E86AB;
                 padding:2px 10px;border-radius:9px;display:inline-block;margin-bottom:8px}}
  .topic-divider {{background:var(--c,#2E86AB);color:white;padding:8px 22px;font-size:.9em;
                   font-weight:500;border-radius:8px;margin-bottom:6px;margin-top:18px}}
  .topic-row {{display:flex;align-items:center;gap:12px;padding:6px 0;
               border-bottom:0.5px solid #e0e0e0}}
  .topic-label {{font-size:.82em;font-weight:500;color:#2c3e50;min-width:260px}}
  .topic-links a {{font-size:.78em;padding:2px 8px;background:#f0faf5;
                   border:1px solid #b2dfce;border-radius:12px;
                   text-decoration:none;color:#27AE60}}
  .breakdown {{background:white;border-radius:8px;padding:14px 20px;
               margin-bottom:20px;box-shadow:0 2px 6px rgba(0,0,0,.07)}}
  .breakdown h2 {{margin:0 0 10px;font-size:1em;color:#2c3e50}}
  footer {{text-align:center;margin-top:28px;color:#95a5a6;font-size:.82em}}
</style>
</head>
<body>
<header>
  <h1>Medical Consultation Platform — Financial Analysis v4</h1>
  <p>Source: crm_stage_finished + crm_selected_translated_column
     &nbsp;|&nbsp; Completed: {n_done}
     &nbsp;|&nbsp; All records: {n_all}
     &nbsp;|&nbsp; Charts: {len(HTML_DIVS)}</p>
</header>
<div class="breakdown"><h2>Content by topic</h2>{breakdown}</div>
<nav>{nav}</nav>
{cards}
<footer>Generated by run_viz.py from quick_viz_4.ipynb &nbsp;|&nbsp; Plotly interactive charts</footer>
</body>
</html>"""

HTML_PATH.write_text(html, encoding='utf-8')
size_kb = HTML_PATH.stat().st_size / 1024
print(f'\nHTML saved → {HTML_PATH}')
print(f'File size : {size_kb:.0f} KB')
print(f'Open      : file:///{str(HTML_PATH).replace(chr(92), "/")}')
