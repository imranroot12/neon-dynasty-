#!/usr/bin/env python3
import json, os, shutil, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
math_root=os.environ.get('ENGINE_MATH_SDK')
web_root=os.environ.get('ENGINE_WEB_SDK')
math_game=Path(os.environ.get('NEON_MATH_GAME', (Path(math_root)/'games'/'neon_dynasty') if math_root else root/'math'/'neon_dynasty'))
web_game=Path(os.environ.get('NEON_WEB_GAME', (Path(web_root)/'apps'/'neon-dynasty') if web_root else root/'web'/'neon-dynasty'))
checks=[]
def check(name, ok, detail): checks.append({'name':name,'ok':bool(ok),'detail':detail})
check('python', sys.version_info >= (3,12), sys.version.split()[0])
check('node', shutil.which('node') is not None, shutil.which('node') or 'missing')
check('zstd', shutil.which('zstd') is not None, shutil.which('zstd') or 'missing')
check('cargo', shutil.which('cargo') is not None, shutil.which('cargo') or 'missing')
check('pnpm', shutil.which('pnpm') is not None, shutil.which('pnpm') or 'missing')
for mode in ('base','basic','super','mystery'):
    p=math_game/'library'/'publish_files'/f'books_{mode}.jsonl.zst'
    check(f'publication_book_{mode}', p.is_file(), str(p))
# A production run must have 100k rows per mode. zstd CLI is used so this gate
# does not depend on the local compatibility shim.
for mode in ('base','basic','super','mystery'):
    p=math_game/'library'/'publish_files'/f'books_{mode}.jsonl.zst'
    if p.is_file() and shutil.which('zstd'):
        import subprocess
        try:
            raw=subprocess.check_output(['zstd','-dc',str(p)], text=True)
            lines=[line for line in raw.splitlines() if line.strip()]
            rows=len(lines)
            check(f'100k_rows_{mode}', rows >= 100000, f'{rows} rows')
            if lines:
                import json as _json
                vals=[float(_json.loads(line).get('payoutMultiplier', 0.0)) for line in lines]
                max_x=max(vals)/100.0
                check(f'max_win_{mode}', max_x <= 20000.0 + 1e-9, f'max {max_x:.2f}x mode-relative')
        except Exception as e: check(f'100k_rows_{mode}', False, str(e))
    else: check(f'100k_rows_{mode}', False, 'book unavailable')
# Require a built frontend artifact in the official workspace.
frontend_candidates=[web_game/'.svelte-kit'/'output', web_game/'build', web_game/'dist']
existing=[str(p) for p in frontend_candidates if p.exists()]
check('web_build_artifact', bool(existing), '; '.join(existing) if existing else 'missing')
# Ensure our source tree contains no known sample asset filenames.
sample_tokens=('mm_', 'miningfont_', 'clusterpay', 'reelhouse_glow', 'transition.atlas', 'symbols3', 'sample_provider', 'sample_lines')
sample=[]
for p in (root/'web').rglob('*'):
    if p.is_file() and any(t.lower() in p.name.lower() for t in sample_tokens): sample.append(str(p.relative_to(root)))
check('sample_asset_quarantine', not sample, '; '.join(sample[:12]) if sample else 'clean')
report={'checks':checks,'ready':all(x['ok'] for x in checks)}
(root/'RELEASE_GATE_BUILD_59.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2)); sys.exit(0 if report['ready'] else 2)
