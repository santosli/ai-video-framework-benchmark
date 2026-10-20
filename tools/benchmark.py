#!/usr/bin/env python3
"""Offline preparation and validation of the published prompt/input kit. Python 3.10+."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
FRAMEWORKS = ('remotion', 'hyperframes')

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def scene(scene_id):
    return next((s for s in load(ROOT / 'scenes/index.json') if s['id'] == scene_id), None)

def safe_file(base, relative):
    path = (base / relative).resolve()
    if not path.is_relative_to(base.resolve()):
        raise ValueError('Path leaves its input directory: ' + relative)
    return path

def check_input(directory, exact=False):
    missing, changed = [], []
    for item in load(directory / 'input-manifest.json')['files']:
        path = safe_file(directory, item['path'])
        if not path.is_file():
            missing.append(item['path'])
        elif item['included'] or exact:
            if digest(path) != item['sha256']:
                changed.append(item['path'])
    return {'ready': not missing and not changed, 'missing': missing, 'changed': changed,
            'mode': 'historical-hashes' if exact else 'included-source-hashes-and-external-presence',
            'note': 'External file presence alone does not verify dimensions, timing, licensing or equivalence.'}

def prompt(scene_id, framework, phase, original=False):
    info = scene(scene_id)
    if not info or (phase == 'revision' and info['batch'] != 1):
        raise ValueError('Unknown scene or phase')
    text = (ROOT / f'prompts/original/{scene_id}-{framework}-r1-{phase}.md').read_text(encoding='utf-8')
    if original:
        return text
    lines = []
    for line in text.splitlines():
        if line.startswith('沙箱内不启动 Chrome'):
            lines.append('在已准备的本地环境使用本框架的官方命令进行预览抽帧和完整导出，记录实际命令、浏览器版本、退出码、等待时间及文件 SHA-256。不要等待 .render-results 响应，本复现包不提供原实验的外部渲染服务。')
        elif line.startswith('outputs 名称须逐项对应'):
            lines.append(line.replace('预览与导出命令由外部服务执行，', '在本机执行预览与导出，'))
        elif line.startswith('首次实现交回后执行器保存'):
            lines.append('保存首次实现、必要纠错与可交付版的独立快照，由复现者按统一模板反馈技术问题；不追加审美指导。不能完成时保留原始错误，不删步骤或更换输入。')
        else:
            lines.append(line)
    return '# 便携复现适配提示词（非原始提示词）\n\n' + '\n'.join(lines) + '\n'

def prepare(args):
    info = scene(args.scene)
    if not info:
        raise ValueError('Unknown scene')
    version = 'v1' if args.phase == 'initial' else 'v2'
    source = ROOT / f'scenes/{args.scene}/{version}'
    if not source.is_dir():
        raise ValueError('This scene has no revision phase')
    out = Path(args.out).resolve()
    if out.exists() or out.is_relative_to(ROOT):
        raise ValueError('Choose a nonexistent output directory outside this repository')
    baseline = None
    if args.phase == 'revision':
        if not args.baseline_dir:
            raise ValueError('Revision requires --baseline-dir with this framework\'s corresponding initial project')
        baseline = Path(args.baseline_dir).resolve()
        if not baseline.is_dir() or out.is_relative_to(baseline):
            raise ValueError('Invalid baseline or output nested inside baseline')
        if not (baseline / 'input/expected.json').is_file():
            raise ValueError('Baseline must contain its completed v1 input directory')
        if load(baseline / 'input/expected.json').get('case_id') != args.scene:
            raise ValueError('Baseline belongs to a different scene')
        dependencies = load(baseline / 'package.json').get('dependencies', {})
        if args.framework not in dependencies:
            raise ValueError('Baseline belongs to a different framework')
        shutil.copytree(baseline, out, ignore=shutil.ignore_patterns('.git', 'node_modules', 'input', 'baseline-input', 'official-skills', '.render-requests', '.render-results', '__pycache__'))
        if (baseline / 'input').is_dir():
            shutil.copytree(baseline / 'input', out / 'baseline-input')
        else:
            raise ValueError('Baseline must contain its completed v1 input directory')
    else:
        out.mkdir(parents=True)
    shutil.copytree(source, out / 'input')
    for name in ('package.json', 'package-lock.json'):
        shutil.copy2(ROOT / f'environments/{args.framework}' / name, out / name)
    shutil.copy2(ROOT / 'tools/read_skill.py', out / 'read_skill.py')
    (out / 'TASK.md').write_text(prompt(args.scene, args.framework, args.phase), encoding='utf-8')
    (out / 'task-config.json').write_text(json.dumps({
        'phase': args.phase, 'authoring_seconds': 1200 if args.phase == 'initial' else 600,
        'technical_fixes_max': 2 if args.phase == 'initial' else 1, 'first_export_seconds': 900,
        'expected': load(source / 'expected.json')}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'workspace': str(out), 'input_check': check_input(out / 'input'),
                      'next': 'See docs/reproduce.md: supply assets, npm ci, fetch pinned official skills, then start a fresh AI context.'}, ensure_ascii=False, indent=2))

def validate():
    scenes = load(ROOT / 'scenes/index.json')
    assert len(scenes) == 36 and len({s['id'] for s in scenes}) == 36
    assert sum(s['batch'] == 1 for s in scenes) == 18
    assert sum(len(s['versions']) for s in scenes) == 54
    hashes = load(ROOT / 'docs/prompt-provenance.json')['runs']
    assert len(hashes) == 108
    for run in hashes:
        assert digest(ROOT / f"prompts/original/{run['run_id']}.md") == run['task_sha256'], run['run_id']
    included = external = 0
    for s in scenes:
        for v in s['versions']:
            folder = ROOT / v['directory']
            result = check_input(folder)
            assert not result['changed'], (s['id'], result)
            for f in load(folder / 'input-manifest.json')['files']:
                if f['included']:
                    assert safe_file(folder, f['path']).is_file(), f['path']
                    included += 1
                else:
                    external += 1
            if s['batch'] == 2:
                events = load(folder / 'events.json')
                assert events.get('timing_given') is False
    files = [f for f in ROOT.rglob('*') if f.is_file() and not any(x in f.parts for x in ('.git', '__pycache__'))]
    leaks = re.compile('/' + r'Users/[^\s]+|-----BEGIN [A-Z ]*PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16}')
    for file in files:
        assert file.stat().st_size < 5 * 1024 * 1024, file
        assert not file.is_symlink(), file
        assert not leaks.search(file.read_text(encoding='utf-8')), file
    print(json.dumps({'status': 'PASS', 'scenes': 36, 'input_versions': 54, 'original_prompts': 108,
                      'included_input_files': included, 'external_asset_occurrences': external,
                      'verified': 'source package integrity; not 108 AI generation runs'}, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list')
    sub.add_parser('validate')
    for name in ('prompt', 'prepare'):
        p = sub.add_parser(name)
        p.add_argument('scene')
        p.add_argument('framework', choices=FRAMEWORKS)
        p.add_argument('--phase', choices=('initial', 'revision'), default='initial')
        if name == 'prompt':
            p.add_argument('--original', action='store_true')
        else:
            p.add_argument('--out', required=True)
            p.add_argument('--baseline-dir')
    p = sub.add_parser('check-input')
    p.add_argument('directory', type=Path)
    p.add_argument('--exact', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'list':
            for s in load(ROOT / 'scenes/index.json'):
                print(f"{s['id']}\t批次 {s['batch']}\t{s['category']}\t{s['name']}")
        elif args.command == 'prompt':
            print(prompt(args.scene, args.framework, args.phase, args.original), end='')
        elif args.command == 'prepare':
            prepare(args)
        elif args.command == 'check-input':
            result = check_input(args.directory.resolve(), args.exact)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result['ready'] else 2
        elif args.command == 'validate':
            validate()
    except (ValueError, AssertionError, FileNotFoundError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
