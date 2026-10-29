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


def کلاس_ورودی_نام(path):
    """Read this_class, accepting all current constant-pool tags."""
    from 컴파일러 import 자료읽기, 수정유티에프해독, 컴파일오류
    r = 자료읽기(Path(path).read_bytes())
    if r.수('I') != 0xcafebabe:
        raise 컴파일오류('Java کلاس_مقدار 표식이 아님: ' + str(path))
    r.خواندن(4)
    pool = [None] * r.수('H')
    i = 1
    while i < len(pool):
        tag = r.수('B')
        if tag == 1:
            pool[i] = 수정유티에프해독(r.خواندن(r.수('H')))
        elif tag in (7, 8, 16, 19, 20):
            pool[i] = r.수('H')
        elif tag in (3, 4, 9, 10, 11, 12, 17, 18):
            r.خواندن(4)
        elif tag in (5, 6):
            r.خواندن(8)
            i += 1
        elif tag == 15:
            r.خواندن(3)
        else:
            raise 컴파일오류('알 수 없는 ثابت_مقدار 종류: ' + str(tag))
        i += 1
    r.خواندن(2)
    try:
        name = pool[pool[r.수('H')]]
    except (IndexError, TypeError):
        raise 컴파일오류('잘못된 کلاس_مقدار نام مرجع')
    if not isinstance(name, str) or any(p in ('', '.', '..') for p in name.split('/')) or '\\' in name:
        raise 컴파일오류('잘못된 کلاس_مقدار نام')
    return name


def c문자열(text):
    # All bytes use fixed-width octal escapes: neither C nor the shell sees
    # untrusted quotes, escapes or command substitutions.
    return '"' + ''.join('\\%03o' % b for b in text.encode('utf-8')) + '"'


def ایجاد_ورودی(args):
    from 컴파일러 import 컴파일오류
    output = Path(args.output).absolute()
    if ':' in str(output):
        raise 컴파일오류('اجرا_فرمان پرونده 경로에는 Java کلاس_مقدار مسیر 구분자인 콜론(:)을 사용할 수 없음')
    if output.is_symlink():
        raise 컴파일오류('출력은 심볼릭 링크일 수 없음')
    inputs = [Path(p).resolve() for p in args.sources]
    dependencies = [Path(p).resolve() for p in args.classpath]
    if output.resolve() in inputs + dependencies:
        raise 컴파일오류('출력이 입력과 같음')
    for p in inputs + dependencies:
        if not p.exists():
            raise 컴파일오류('입력이 없음: ' + str(p))
    if args.export:
        raise 컴파일오류('openjdk اجرا_فرمان 파일은 بومی هسته_مقدار ABI 내보내기를 지원하지 않음')
    if not args.entry or args.entry.startswith('-') or '/' in args.entry:
        raise 컴파일오류('진입점은 public static void main(String[])을 가진 کلاس_مقدار نام')
    output.parent.mkdir(parents=True, exist_ok=True)
    bundle = output.with_name(output.name + '.app')
    if bundle.exists() and not (bundle / 'jkoros-application.json').is_file():
        raise 컴파일오류('프로젝트가 생성하지 않은 디렉터리가 이미 있음: ' + str(bundle))
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
                    raise 컴파일오류('خروجی 디렉터리를 포함한 입력 디렉터리는 사용할 수 없음')
                dest = lib / ('dependency-' + str(i))
                shutil.copytree(str(p), str(dest), symlinks=False)
                paths.append(str(dest.relative_to(app)))
            elif p.suffix == '.java' and p in inputs:
                sources.append(p)
            elif p.suffix == '.class':
                dest = classes / (کلاس_ورودی_نام(p) + '.class')
                dest.parent.mkdir(parents=True, exist_ok=True)
                if dest.exists() and dest.read_bytes() != p.read_bytes():
                    raise 컴파일오류('중복 کلاس_مقدار: ' + str(dest))
                shutil.copy2(str(p), str(dest))
            elif p.suffix in ('.jar', '.zip'):
                with zipfile.ZipFile(str(p)) as jar:
                    if jar.testzip() is not None:
                        raise 컴파일오류('손상된 JAR: ' + str(p))
                dest = lib / ('dependency-{}.jar'.format(i))
                shutil.copy2(str(p), str(dest))
                paths.append(str(dest.relative_to(app)))
            else:
                raise 컴파일오류('پشتیبان_مقدار 입력: .java, .class, .jar, کلاس_مقدار/리소스 디렉터리')
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
            raise 컴파일오류('ورودی_نقطه_مقدار 클래스를 찾을 수 없음: ' + args.entry)
        if args.bundle_runtime:
            runtime = Path(args.bundle_runtime).resolve()
            if not (runtime / 'bin/java').is_file():
                raise 컴파일오류('JDK/JRE의 bin/java가 없음')
            shutil.copytree(str(runtime), str(app / 'runtime'), symlinks=True)
        template = Path(__file__).with_name('برنامه_راه_انداز.c').read_text()
        template = template.replace('@ENTRY@', c문자열(args.entry))
        template = template.replace('@CLASSPATH@', ', '.join(c문자열(p) for p in paths))
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
    print('OpenJDK اجرا_فرمان پرونده ایجاد: {} (함께 انتقال_مقدار: {})'.format(output, bundle))
