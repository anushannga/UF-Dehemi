"""Run the full Google Fonts profile with its licensing inputs included."""
from pathlib import Path
import argparse
import json
import subprocess

from build import OUT, PREFIX, ROOT, VERSION


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fontspector', default='fontspector')
    args = parser.parse_args()
    tool_version = subprocess.check_output(
        [args.fontspector, '--version'], text=True
    ).strip()
    if tool_version.splitlines()[0] != 'fontspector 1.9.0':
        raise SystemExit(f'Expected fontspector 1.9.0; found {tool_version}')

    fonts = [OUT / f'{PREFIX}-{style}.ttf' for style in ['Regular', 'Italic']]
    license_path = OUT / 'OFL.txt'
    if license_path.read_bytes() != (ROOT / 'OFL.txt').read_bytes():
        raise SystemExit('The bundled license differs from the project OFL.txt')
    report_path = Path('qa') / f'fontspector-{VERSION}.json'
    command = [
        args.fontspector, '-p', 'googlefonts',
        *[p.relative_to(ROOT).as_posix() for p in fonts],
        license_path.relative_to(ROOT).as_posix(),
        '--json', report_path.as_posix(),
        '--html', f'qa/fontspector-{VERSION}.html', '--succinct',
    ]
    # Fontspector's collection checks only see explicitly supplied inputs.
    # Use the complete profile: no check exclusions or severity overrides.
    subprocess.run(command, cwd=ROOT, check=True)
    report = json.loads((ROOT / report_path).read_text(encoding='utf8'))
    licensing = [
        result
        for sections in report['results'].values()
        for results in sections.values()
        for result in results
        if result['check_id'] in {
            'googlefonts/name/license_url', 'googlefonts/name/license',
            'googlefonts/family/has_license',
        }
    ]
    expected_counts = {
        'googlefonts/name/license_url': 2,
        'googlefonts/name/license': 1,
        'googlefonts/family/has_license': 1,
    }
    for check_id, count in expected_counts.items():
        results = [r for r in licensing if r['check_id'] == check_id]
        if len(results) != count or any(r['worst_status'] != 'PASS' for r in results):
            raise SystemExit(f'Licensing check did not pass: {check_id}')
    context = {
        'version': VERSION, 'fontspector': tool_version,
        'inputs': [p.relative_to(ROOT).as_posix() for p in [*fonts, license_path]],
        'profile': 'googlefonts', 'excluded_checks': [],
        'summary': report['summary'], 'required_licensing_checks_pass': True,
    }
    (ROOT / 'qa' / f'audit-context-{VERSION}.json').write_text(
        json.dumps(context, indent=2) + '\n', encoding='utf8'
    )
    print(json.dumps(context, indent=2))


if __name__ == '__main__':
    main()
