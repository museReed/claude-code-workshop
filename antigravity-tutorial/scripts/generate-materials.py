#!/usr/bin/env python3
from pathlib import Path
import json
import mimetypes
import sys

if len(sys.argv) != 3:
    raise SystemExit('usage: generate-materials.py <source-repo> <out-js>')

SRC = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()

include_roots = [
    '課程練習素材',
    '.claude/skills',
]
include_files = [
    'README.md',
    'faq.md',
    'setup.md',
    'github-setup.md',
    'panel-setup.md',
    'onboarding.md',
    '學生閱讀資料/faq.md',
    '學生閱讀資料/onboarding.md',
    '給AI_Agent的環境安裝文件/github-setup.md',
    '給AI_Agent的環境安裝文件/to_CLI_AI_Agent_setup.md',
    '給AI_Agent的環境安裝文件/to_IDE_AI_Agent_setup.md',
    '給AI_Agent的環境安裝文件/ClaudeCodeSkill/panel-setup.md',
]
exclude_parts = {'.git', '.obsidian'}

def wanted(path: Path) -> bool:
    rel = path.relative_to(SRC).as_posix()
    parts = set(path.relative_to(SRC).parts)
    if parts & exclude_parts:
        return False
    if rel in include_files:
        return True
    return any(rel == root or rel.startswith(root + '/') for root in include_roots)

def file_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {'.md', '.markdown'}:
        return 'md'
    if suffix in {'.txt', '.json', '.yml', '.yaml', '.js', '.css', '.html'}:
        return 'text'
    if suffix == '.csv':
        return 'csv'
    mime, _ = mimetypes.guess_type(path.name)
    if mime and not mime.startswith('text'):
        return 'binary'
    try:
        path.read_text(encoding='utf-8')
        return 'text'
    except UnicodeDecodeError:
        return 'binary'

def read_content(path: Path, typ: str) -> str:
    if typ == 'binary':
        return '(二進位檔，不顯示)'
    return path.read_text(encoding='utf-8')

all_files = sorted([p for p in SRC.rglob('*') if p.is_file() and wanted(p)], key=lambda p: p.relative_to(SRC).as_posix())
files = {}
for path in all_files:
    rel = path.relative_to(SRC).as_posix()
    typ = file_type(path)
    files[rel] = {'type': typ, 'content': read_content(path, typ)}

class Node(dict):
    pass

root = []
node_by_path = {'': root}
for rel in files:
    parts = rel.split('/')
    current_children = root
    current_path = ''
    for i, part in enumerate(parts):
        path = '/'.join(parts[:i+1])
        is_file = i == len(parts) - 1
        existing = next((n for n in current_children if n['name'] == part), None)
        if existing is None:
            existing = {'name': part, 'path': path, 'folder': not is_file}
            if not is_file:
                existing['children'] = []
            current_children.append(existing)
        if not is_file:
            current_children = existing['children']

materials = {
    'tree': root,
    'files': files,
    'meta': {
        'source': 'https://github.com/museReed/claude-code-workshop-jr-student.git',
        'included': list(files.keys()),
        'excluded': ['.git/**', '.obsidian/**', 'binary file contents'],
    }
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text('window.MATERIALS = ' + json.dumps(materials, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
print(f'wrote {OUT} with {len(files)} files')
for rel in files:
    print(rel)
