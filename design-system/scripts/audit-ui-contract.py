#!/usr/bin/env python3
from pathlib import Path
import argparse
import re
import sys

DEFAULT_FORBIDDEN_EXISTING_DS = [
    'ds-card','ds-card-flat','ds-pill','ds-pill-accent','ds-pill-success',
    'ds-btn','ds-btn-primary','ds-btn-ghost','ds-btn-sm','ds-side-item',
    'ds-pbar','ds-pbar-fill','ds-duck','ds-term','ds-term-body','ds-term-chrome','ds-term-dot',
    'ds-nav','ds-container','ds-container-narrow','ds-callout','ds-tree','ds-quiz-q','ds-opts','ds-opt','ds-explain'
    ,'ds-step-block','ds-step-num','ds-step-title','ds-step-body','ds-step-note'
]

DEFAULT_ALLOWED_CUSTOM_DS = {
    'ds-callout--success','ds-callout--warn',
    'ds-check','ds-check-label',
    'ds-teleprompter','ds-shot'
}

parser = argparse.ArgumentParser(description='Audit app CSS/HTML against the claude2code design-system contract.')
parser.add_argument('--project', default='.', help='Project root to audit. Default: current directory')
parser.add_argument('--design-system', default=None, help='Path to design-system.css. Default: <project>/assets/css/design-system.css')
parser.add_argument('--app-css', default='assets/css/app.css', help='App CSS path relative to project root')
parser.add_argument('--files', nargs='*', default=['index.html', 'assets/js/app.js'], help='Files to scan for class usage, relative to project root')
parser.add_argument('--allow-custom', nargs='*', default=sorted(DEFAULT_ALLOWED_CUSTOM_DS), help='Allowed custom ds-* classes')
args = parser.parse_args()

root = Path(args.project).resolve()
app_css_path = root / args.app_css
ds_css_path = Path(args.design_system).resolve() if args.design_system else root / 'assets/css/design-system.css'
scan_files = [root / item for item in args.files]
allowed_custom_ds = set(args.allow_custom)
errors = []

if not app_css_path.exists():
    errors.append(f'app CSS not found: {app_css_path}')
if not ds_css_path.exists():
    errors.append(f'design-system CSS not found: {ds_css_path}')
for path in scan_files:
    if not path.exists():
        errors.append(f'scan file not found: {path}')
if errors:
    print('UI contract audit FAILED')
    for err in errors:
        print('- ' + err)
    sys.exit(1)

app_css = app_css_path.read_text()
ds_css = ds_css_path.read_text()

if re.search(r'#[0-9A-Fa-f]{3,8}|rgba?\(|hsla?\(', app_css):
    errors.append('app.css contains hard-coded color values')

raw_font_sizes = re.findall(r'font-size:(?!var\(|clamp\()[^;}]+', app_css)
if raw_font_sizes:
    errors.append('app.css contains non-token font-size declarations: ' + ', '.join(raw_font_sizes))

for cls in DEFAULT_FORBIDDEN_EXISTING_DS:
    if re.search(r'(^|[\s,{>+~])\.' + re.escape(cls) + r'([\s,{>+~:.#]|$)', app_css):
        errors.append(f'app.css directly overrides existing gallery component .{cls}')

defined_ds = set(re.findall(r'\.([A-Za-z0-9_-]+)', ds_css))
used_ds = set()
for path in scan_files:
    text = path.read_text()
    for m in re.finditer(r'class="([^"]+)"', text):
        for token in m.group(1).split():
            token = token.strip()
            if token.startswith('ds-') and '${' not in token:
                used_ds.add(token)

unknown = sorted(used_ds - defined_ds - allowed_custom_ds)
if unknown:
    errors.append('Unknown / unregistered ds-* classes used: ' + ', '.join(unknown))

joined = ''.join(path.read_text() for path in scan_files)
if 'ds-cmd' in joined or '.ds-cmd' in app_css:
    errors.append('ds-cmd is forbidden; command blocks must wrap gallery ds-term instead')

if errors:
    print('UI contract audit FAILED')
    for err in errors:
        print('- ' + err)
    sys.exit(1)

print('UI contract audit passed')
print(f'- project: {root}')
print(f'- design-system: {ds_css_path}')
print(f'- used ds classes: {len(used_ds)}')
print(f'- allowed custom ds classes: {len(allowed_custom_ds)}')
