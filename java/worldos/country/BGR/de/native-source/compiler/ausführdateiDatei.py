"""Full-JVM application packaging. The native launcher is not bytecode AOT."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import zipfile


def klasseEintragName(path):
    """Read this_class, accepting all current constant-pool tags."""
    from Übersetzer import datenLesen, verändertUTF8Dekodieren, ÜbersetzungsvorgangFehler
    r = datenLesen(Path(path).read_bytes())
    if r.Zahl('I') != 0xcafebabe:
        raise ÜbersetzungsvorgangFehler('Java klasseWert 표식이 아님: ' + str(path))
    r.lesen(4)
    pool = [None] * r.Zahl('H')
    i = 1
    while i < len(pool):
        tag = r.Zahl('B')
        if tag == 1:
            pool[i] = verändertUTF8Dekodieren(r.lesen(r.Zahl('H')))
        elif tag in (7, 8, 16, 19, 20):
            pool[i] = r.Zahl('H')
        elif tag in (3, 4, 9, 10, 11, 12, 17, 18):
            r.lesen(4)
        elif tag in (5, 6):
            r.lesen(8)
            i += 1
        elif tag == 15:
            r.lesen(3)
        else:
            raise ÜbersetzungsvorgangFehler('알 Zahl 없는 konstanteWert artWert: ' + str(tag))
        i += 1
    r.lesen(2)
    try:
        name = pool[pool[r.Zahl('H')]]
    except (IndexError, TypeError):
        raise ÜbersetzungsvorgangFehler('잘못된 klasseWert Name verweis')
    if not isinstance(name, str) or any(p in ('', '.', '..') for p in name.split('/')) or '\\' in name:
        raise ÜbersetzungsvorgangFehler('잘못된 klasseWert Name')
    return name


def cZeichenkette(text):
    # All bytes use fixed-width octal escapes: neither C nor the shell sees
    # untrusted quotes, escapes or command substitutions.
    return '"' + ''.join('\\%03o' % b for b in text.encode('utf-8')) + '"'


def eintragErstellen(args):
    from Übersetzer import ÜbersetzungsvorgangFehler
    output = Path(args.output).absolute()
    if ':' in str(output):
        raise ÜbersetzungsvorgangFehler('befehlAusführen Datei 경로에는 Java klasseWert pfad 구분자인 콜론(:)을 사용할 Zahl fehlendMethode')
    if output.is_symlink():
        raise ÜbersetzungsvorgangFehler('출력은 심볼릭 링크일 Zahl fehlendMethode')
    inputs = [Path(p).resolve() for p in args.sources]
    dependencies = [Path(p).resolve() for p in args.classpath]
    if output.resolve() in inputs + dependencies:
        raise ÜbersetzungsvorgangFehler('출력이 입력과 gleichText')
    for p in inputs + dependencies:
        if not p.exists():
            raise ÜbersetzungsvorgangFehler('입력이 fehlendMethode: ' + str(p))
    if args.export:
        raise ÜbersetzungsvorgangFehler('openjdk befehlAusführen 파일은 eigen betriebskernWert ABI 내보내기를 지원하지 않음')
    if not args.entry or args.entry.startswith('-') or '/' in args.entry:
        raise ÜbersetzungsvorgangFehler('진입점은 public static void main(String[])을 가진 klasseWert Name')
    output.parent.mkdir(parents=True, exist_ok=True)
    bundle = output.with_name(output.name + '.app')
    if bundle.exists() and not (bundle / 'jkoros-application.json').is_file():
        raise ÜbersetzungsvorgangFehler('프로젝트가 생성하지 않은 디렉터리가 이미 있음: ' + str(bundle))
    javac = str(Path(args.java_home) / 'bin/javac') if args.java_home else 'javac'
    with tempfile.TemporaryDirectory(prefix='.jkoros-package-', dir=str(output.parent)) as tmp:
        tmp = Path(tmp)
        app = tmp / 'app'
        lib = app / 'lib'
        classes = lib / 'classes'
        classes.mkdir(parents=True)
        paths = ['lib/classes']
        sources = []
        digests = {}
        for i, p in enumerate(inputs + dependencies):
            if p.is_dir():
                if p == output.parent or p in output.parents:
                    raise ÜbersetzungsvorgangFehler('Ausgabe 디렉터리를 포함한 Eingabewert 디렉터리는 사용할 Zahl fehlendMethode')
                dest = lib / ('dependency-' + str(i))
                shutil.copytree(str(p), str(dest), symlinks=False)
                paths.append(str(dest.relative_to(app)))
            elif p.suffix == '.java' and p in inputs:
                sources.append(p)
            elif p.suffix == '.class':
                dest = classes / (klasseEintragName(p) + '.class')
                dest.parent.mkdir(parents=True, exist_ok=True)
                if dest.exists() and dest.read_bytes() != p.read_bytes():
                    raise ÜbersetzungsvorgangFehler('중복 klasseWert: ' + str(dest))
                shutil.copy2(str(p), str(dest))
            elif p.suffix in ('.jar', '.zip'):
                with zipfile.ZipFile(str(p)) as jar:
                    if jar.testzip() is not None:
                        raise ÜbersetzungsvorgangFehler('손상된 JAR: ' + str(p))
                dest = lib / ('dependency-{}.jar'.format(i))
                shutil.copy2(str(p), str(dest))
                paths.append(str(dest.relative_to(app)))
            else:
                raise ÜbersetzungsvorgangFehler('unterstützungWert Eingabewert: .java, .class, .jar, klasseWert/리소스 디렉터리')
            if p.is_file():
                digests[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
        if sources:
            cp = os.pathsep.join(str(app / p) for p in paths)
            subprocess.run([javac, '-encoding', 'UTF-8', '-proc:none', '-classpath', cp,
                            '-d', str(classes)] + [str(p) for p in sources], check=True)
        entry_file = args.entry.replace('.', '/') + '.class'
        found = any((app / p / entry_file).is_file() for p in paths if (app / p).is_dir())
        for p in paths:
            if (app / p).is_file():
                with zipfile.ZipFile(str(app / p)) as z:
                    found = found or entry_file in z.namelist()
        if not found:
            raise ÜbersetzungsvorgangFehler('eintragPunktWert 클래스를 찾을 Zahl fehlendMethode: ' + args.entry)
        if args.bundle_runtime:
            runtime = Path(args.bundle_runtime).resolve()
            if not (runtime / 'bin/java').is_file():
                raise ÜbersetzungsvorgangFehler('JDK/JRE의 bin/java가 fehlendMethode')
            shutil.copytree(str(runtime), str(app / 'runtime'), symlinks=True)
        template = Path(__file__).with_name('ProgrammStarter.c').read_text()
        template = template.replace('@ENTRY@', cZeichenkette(args.entry))
        template = template.replace('@CLASSPATH@', ', '.join(cZeichenkette(p) for p in paths))
        (tmp / 'launcher.c').write_text(template)
        subprocess.run([args.cc, '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror',
                        '-o', str(tmp / 'launcher'), str(tmp / 'launcher.c')], check=True)
        manifest = {'format': 'native-launcher-with-openjdk', 'bytecode_aot': False,
                    'runtime_jvm': True, 'entry': args.entry, 'classpath': paths,
                    'bundled_runtime': bool(args.bundle_runtime), 'inputs': digests,
                    'compatibility': 'Requires matching OS/CPU, supported class version and all dependencies.'}
        (app / 'jkoros-application.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        old = tmp / 'previous'
        if bundle.exists():
            bundle.rename(old)
        try:
            app.rename(bundle)
            os.replace(str(tmp / 'launcher'), str(output))
        except BaseException:
            if bundle.exists():
                shutil.rmtree(str(bundle))
            if old.exists():
                old.rename(bundle)
            raise
    print('OpenJDK befehlAusführen Datei generieren: {} (함께 bewegenWert: {})'.format(output, bundle))
