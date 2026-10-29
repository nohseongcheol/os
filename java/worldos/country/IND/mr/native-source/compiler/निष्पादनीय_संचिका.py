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


def वर्ग_प्रविष्टी_नाव(path):
    """Read this_class, accepting all current constant-pool tags."""
    from संकलक import डेटा_वाचा, विसंकेतन_सुधारित_युनिकोडसंकेतन_8, संकलन_त्रुटी
    r = डेटा_वाचा(Path(path).read_bytes())
    if r.संख्या('I') != 0xcafebabe:
        raise संकलन_त्रुटी('Java वर्ग_मूल्य 표식이 아님: ' + str(path))
    r.वाचन(4)
    pool = [None] * r.संख्या('H')
    i = 1
    while i < len(pool):
        tag = r.संख्या('B')
        if tag == 1:
            pool[i] = विसंकेतन_सुधारित_युनिकोडसंकेतन_8(r.वाचन(r.संख्या('H')))
        elif tag in (7, 8, 16, 19, 20):
            pool[i] = r.संख्या('H')
        elif tag in (3, 4, 9, 10, 11, 12, 17, 18):
            r.वाचन(4)
        elif tag in (5, 6):
            r.वाचन(8)
            i += 1
        elif tag == 15:
            r.वाचन(3)
        else:
            raise संकलन_त्रुटी('알 संख्या 없는 स्थिरांक_मूल्य प्रकार_मूल्य: ' + str(tag))
        i += 1
    r.वाचन(2)
    try:
        name = pool[pool[r.संख्या('H')]]
    except (IndexError, TypeError):
        raise संकलन_त्रुटी('잘못된 वर्ग_मूल्य नाव संदर्भ')
    if not isinstance(name, str) or any(p in ('', '.', '..') for p in name.split('/')) or '\\' in name:
        raise संकलन_त्रुटी('잘못된 वर्ग_मूल्य नाव')
    return name


def सी_स्ट्रींग(text):
    # All bytes use fixed-width octal escapes: neither C nor the shell sees
    # untrusted quotes, escapes or command substitutions.
    return '"' + ''.join('\\%03o' % b for b in text.encode('utf-8')) + '"'


def प्रविष्टी_तयार_करा(args):
    from संकलक import संकलन_त्रुटी
    output = Path(args.output).absolute()
    if ':' in str(output):
        raise संकलन_त्रुटी('आज्ञा_कार्यवाही_करा फाइल 경로에는 Java वर्ग_मूल्य मार्ग 구분자인 콜론(:)을 사용할 संख्या अनुपस्थित_पद्धत')
    if output.is_symlink():
        raise संकलन_त्रुटी('출력은 심볼릭 링크일 संख्या अनुपस्थित_पद्धत')
    inputs = [Path(p).resolve() for p in args.sources]
    dependencies = [Path(p).resolve() for p in args.classpath]
    if output.resolve() in inputs + dependencies:
        raise संकलन_त्रुटी('출력이 입력과 समान_मजकूर')
    for p in inputs + dependencies:
        if not p.exists():
            raise संकलन_त्रुटी('입력이 अनुपस्थित_पद्धत: ' + str(p))
    if args.export:
        raise संकलन_त्रुटी('openjdk आज्ञा_कार्यवाही_करा 파일은 स्वकीय गाभा_मूल्य ABI 내보내기를 지원하지 않음')
    if not args.entry or args.entry.startswith('-') or '/' in args.entry:
        raise संकलन_त्रुटी('진입점은 public static void main(String[])을 가진 वर्ग_मूल्य नाव')
    output.parent.mkdir(parents=True, exist_ok=True)
    bundle = output.with_name(output.name + '.app')
    if bundle.exists() and not (bundle / 'jkoros-application.json').is_file():
        raise संकलन_त्रुटी('프로젝트가 생성하지 않은 디렉터리가 이미 있음: ' + str(bundle))
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
                    raise संकलन_त्रुटी('आउटपुट 디렉터리를 포함한 आदान_मूल्य 디렉터리는 사용할 संख्या अनुपस्थित_पद्धत')
                dest = lib / ('dependency-' + str(i))
                shutil.copytree(str(p), str(dest), symlinks=False)
                paths.append(str(dest.relative_to(app)))
            elif p.suffix == '.java' and p in inputs:
                sources.append(p)
            elif p.suffix == '.class':
                dest = classes / (वर्ग_प्रविष्टी_नाव(p) + '.class')
                dest.parent.mkdir(parents=True, exist_ok=True)
                if dest.exists() and dest.read_bytes() != p.read_bytes():
                    raise संकलन_त्रुटी('중복 वर्ग_मूल्य: ' + str(dest))
                shutil.copy2(str(p), str(dest))
            elif p.suffix in ('.jar', '.zip'):
                with zipfile.ZipFile(str(p)) as jar:
                    if jar.testzip() is not None:
                        raise संकलन_त्रुटी('손상된 JAR: ' + str(p))
                dest = lib / ('dependency-{}.jar'.format(i))
                shutil.copy2(str(p), str(dest))
                paths.append(str(dest.relative_to(app)))
            else:
                raise संकलन_त्रुटी('समर्थन_मूल्य आदान_मूल्य: .java, .class, .jar, वर्ग_मूल्य/리소스 디렉터리')
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
            raise संकलन_त्रुटी('प्रविष्टी_गुण_मूल्य 클래스를 찾을 संख्या अनुपस्थित_पद्धत: ' + args.entry)
        if args.bundle_runtime:
            runtime = Path(args.bundle_runtime).resolve()
            if not (runtime / 'bin/java').is_file():
                raise संकलन_त्रुटी('JDK/JRE의 bin/java가 अनुपस्थित_पद्धत')
            shutil.copytree(str(runtime), str(app / 'runtime'), symlinks=True)
        template = Path(__file__).with_name('अनुप्रयोग_चालक.c').read_text()
        template = template.replace('@ENTRY@', सी_स्ट्रींग(args.entry))
        template = template.replace('@CLASSPATH@', ', '.join(सी_स्ट्रींग(p) for p in paths))
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
    print('OpenJDK आज्ञा_कार्यवाही_करा फाइल तयार_करा: {} (함께 हलवा_मूल्य: {})'.format(output, bundle))
