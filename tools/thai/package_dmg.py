"""Package an already signed LightCraft app as a verified, plain Apple Silicon DMG."""
from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import plistlib
import subprocess
import tempfile


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def run(*args):
    subprocess.run(list(args), check=True)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--app', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--record', required=True, type=Path)
    args = parser.parse_args()
    source, output = args.app.resolve(), args.output.resolve()
    assert source.name == 'LightCraft.app' and source.is_dir()
    assert not output.exists(), 'Keep any previous package for inspection'
    assert not args.record.exists(), 'Keep the previous verification record'
    info = plistlib.loads((source / 'Contents/Info.plist').read_bytes())
    assert info['CFBundleExecutable'] == 'LightCraft'
    version = info['LightCraftVersion']
    executables = ['Contents/MacOS/LightCraft', 'Contents/MacOS/lightcraft-cli']
    original = {}
    for relative in executables:
        binary = source / relative
        assert subprocess.check_output(['lipo', '-archs', str(binary)], text=True).strip() == 'arm64'
        assert version in subprocess.check_output([str(binary), '--version'], text=True)
        original[relative] = digest(binary)
    run('codesign', '--verify', '--strict', '--deep', str(source))
    output.parent.mkdir(parents=True, exist_ok=True)
    record = {'startedAt': datetime.now(timezone.utc).isoformat(), 'thaiVersion': version,
              'sourceBuildCommit': info['LightCraftBuildCommit'],
              'recipe': 'tools/thai/package_dmg.py', 'recipeSha256': digest(Path(__file__).resolve()),
              'method': 'plain HFS+ DMG; internal temporary stage; metadata-free app copy; LightCraft Thai volume',
              'signature': 'ad-hoc', 'notarized': False}
    mount = None
    try:
        with tempfile.TemporaryDirectory(prefix='lightcraft-th-dmg-', dir='/private/tmp') as scratch:
            stage = Path(scratch) / 'stage'
            stage.mkdir()
            # Keep executable permissions and signed bytes, without inherited Finder/provenance metadata.
            # A plain internal stage avoids the decorated external-stage image creation failure on macOS.
            run('ditto', '--norsrc', '--noextattr', '--noqtn', str(source), str(stage / source.name))
            run('codesign', '--verify', '--strict', '--deep', str(stage / source.name))
            (stage / 'Applications').symlink_to('/Applications')
            run('hdiutil', 'create', '-fs', 'HFS+', '-format', 'UDZO', '-srcfolder', str(stage),
                '-volname', 'LightCraft Thai', str(output))
            run('codesign', '--force', '--sign', '-', '--timestamp=none', str(output))
            run('codesign', '--verify', '--strict', str(output))
            run('hdiutil', 'verify', str(output))
            attached = plistlib.loads(subprocess.check_output(['hdiutil', 'attach', '-readonly', '-nobrowse', '-plist', str(output)]))
            mount = Path(next(e['mount-point'] for e in attached['system-entities'] if 'mount-point' in e))
            packaged = mount / source.name
            run('codesign', '--verify', '--strict', '--deep', str(packaged))
            installed = Path(scratch) / 'installed' / source.name
            run('ditto', str(packaged), str(installed))
            run('codesign', '--verify', '--strict', '--deep', str(installed))
            for relative, expected in original.items():
                assert digest(packaged / relative) == digest(installed / relative) == expected
            record.update(status='passed', artifact=output.name, sha256=digest(output), bytes=output.stat().st_size,
                          mountedAndCopiedCodeSignaturesPassed=True, executableHashes=original)
            Path(str(output) + '.sha256').write_text(record['sha256'] + '  ' + output.name + '\n', encoding='ascii')
    except BaseException as exc:
        record.update(status='failed', reason=str(exc))
        raise
    finally:
        if mount is not None:
            run('hdiutil', 'detach', str(mount))
        record['finishedAt'] = datetime.now(timezone.utc).isoformat()
        args.record.parent.mkdir(parents=True, exist_ok=True)
        args.record.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
