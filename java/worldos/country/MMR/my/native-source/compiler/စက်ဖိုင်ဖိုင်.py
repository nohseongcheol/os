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


def အတန်းအချက်အမည်(path):
    """Read this_class, accepting all current constant-pool tags."""
    from ဘာသာပြန်စက် import ဒေတာဖတ်, 수정유티에프해독, ဘာသာပြန်မှုအမှား
    r = ဒေတာဖတ်(Path(path).read_bytes())
    if r.ကိန်းတန်ဖိုး('I') != 0xcafebabe:
        raise ဘာသာပြန်မှုအမှား('Java အတန်းတန်ဖိုး 표식이 아님: ' + str(path))
    r.ဖတ်(4)
    pool = [None] * r.ကိန်းတန်ဖိုး('H')
    i = 1
    while i < len(pool):
        tag = r.ကိန်းတန်ဖိုး('B')
        if tag == 1:
            pool[i] = 수정유티에프해독(r.ဖတ်(r.ကိန်းတန်ဖိုး('H')))
        elif tag in (7, 8, 16, 19, 20):
            pool[i] = r.ကိန်းတန်ဖိုး('H')
        elif tag in (3, 4, 9, 10, 11, 12, 17, 18):
            r.ဖတ်(4)
        elif tag in (5, 6):
            r.ဖတ်(8)
            i += 1
        elif tag == 15:
            r.ဖတ်(3)
        else:
            raise ဘာသာပြန်မှုအမှား('알 ကိန်းတန်ဖိုး 없는 ကိန်းသေတန်ဖိုး အမျိုးအစားတန်ဖိုး: ' + str(tag))
        i += 1
    r.ဖတ်(2)
    try:
        name = pool[pool[r.ကိန်းတန်ဖိုး('H')]]
    except (IndexError, TypeError):
        raise ဘာသာပြန်မှုအမှား('잘못된 အတန်းတန်ဖိုး အမည် ကိုးကားချက်')
    if not isinstance(name, str) or any(p in ('', '.', '..') for p in name.split('/')) or '\\' in name:
        raise ဘာသာပြန်မှုအမှား('잘못된 အတန်းတန်ဖိုး အမည်')
    return name


def Cအက္ခရာစဉ်(text):
    # All bytes use fixed-width octal escapes: neither C nor the shell sees
    # untrusted quotes, escapes or command substitutions.
    return '"' + ''.join('\\%03o' % b for b in text.encode('utf-8')) + '"'


def အချက်ဖန်တီး(args):
    from ဘာသာပြန်စက် import ဘာသာပြန်မှုအမှား
    output = Path(args.output).absolute()
    if ':' in str(output):
        raise ဘာသာပြန်မှုအမှား('စက်မောင်း ဖိုင် 경로에는 Java အတန်းတန်ဖိုး လမ်း 구분자인 콜론(:)을 사용할 ကိန်းတန်ဖိုး 없음')
    if output.is_symlink():
        raise ဘာသာပြန်မှုအမှား('출력은 심볼릭 링크일 ကိန်းတန်ဖိုး 없음')
    inputs = [Path(p).resolve() for p in args.sources]
    dependencies = [Path(p).resolve() for p in args.classpath]
    if output.resolve() in inputs + dependencies:
        raise ဘာသာပြန်မှုအမှား('출력이 입력과 ညီစာသား')
    for p in inputs + dependencies:
        if not p.exists():
            raise ဘာသာပြန်မှုအမှား('입력이 없음: ' + str(p))
    if args.export:
        raise ဘာသာပြန်မှုအမှား('openjdk စက်မောင်း 파일은 ကိုယ်ပိုင် အူတိုင်တန်ဖိုး ABI 내보내기를 지원하지 않음')
    if not args.entry or args.entry.startswith('-') or '/' in args.entry:
        raise ဘာသာပြန်မှုအမှား('진입점은 public static void main(String[])을 가진 အတန်းတန်ဖိုး အမည်')
    output.parent.mkdir(parents=True, exist_ok=True)
    bundle = output.with_name(output.name + '.app')
    if bundle.exists() and not (bundle / 'jkoros-application.json').is_file():
        raise ဘာသာပြန်မှုအမှား('프로젝트가 생성하지 않은 디렉터리가 이미 있음: ' + str(bundle))
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
                    raise ဘာသာပြန်မှုအမှား('အထွက် 디렉터리를 포함한 ဝင်ဒေတာ 디렉터리는 사용할 ကိန်းတန်ဖိုး 없음')
                dest = lib / ('dependency-' + str(i))
                shutil.copytree(str(p), str(dest), symlinks=False)
                paths.append(str(dest.relative_to(app)))
            elif p.suffix == '.java' and p in inputs:
                sources.append(p)
            elif p.suffix == '.class':
                dest = classes / (အတန်းအချက်အမည်(p) + '.class')
                dest.parent.mkdir(parents=True, exist_ok=True)
                if dest.exists() and dest.read_bytes() != p.read_bytes():
                    raise ဘာသာပြန်မှုအမှား('중복 အတန်းတန်ဖိုး: ' + str(dest))
                shutil.copy2(str(p), str(dest))
            elif p.suffix in ('.jar', '.zip'):
                with zipfile.ZipFile(str(p)) as jar:
                    if jar.testzip() is not None:
                        raise ဘာသာပြန်မှုအမှား('손상된 JAR: ' + str(p))
                dest = lib / ('dependency-{}.jar'.format(i))
                shutil.copy2(str(p), str(dest))
                paths.append(str(dest.relative_to(app)))
            else:
                raise ဘာသာပြန်မှုအမှား('ထောက်ပံ့မှုတန်ဖိုး ဝင်ဒေတာ: .java, .class, .jar, အတန်းတန်ဖိုး/리소스 디렉터리')
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
            raise ဘာသာပြန်မှုအမှား('အချက်အမှတ်တစ်ခုတန်ဖိုး 클래스를 찾을 ကိန်းတန်ဖိုး 없음: ' + args.entry)
        if args.bundle_runtime:
            runtime = Path(args.bundle_runtime).resolve()
            if not (runtime / 'bin/java').is_file():
                raise ဘာသာပြန်မှုအမှား('JDK/JRE의 bin/java가 없음')
            shutil.copytree(str(runtime), str(app / 'runtime'), symlinks=True)
        template = Path(__file__).with_name('ပရိုဂရမ်စက်နှိုးကိရိယာ.c').read_text()
        template = template.replace('@ENTRY@', Cအက္ခရာစဉ်(args.entry))
        template = template.replace('@CLASSPATH@', ', '.join(Cအက္ခရာစဉ်(p) for p in paths))
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
    print('OpenJDK စက်မောင်း ဖိုင် ထုတ်လုပ်: {} (함께 ရွှေ့တန်ဖိုး: {})'.format(output, bundle))
