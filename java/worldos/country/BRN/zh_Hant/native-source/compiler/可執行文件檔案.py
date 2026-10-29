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


def 類別條目名稱(path):
    """Read this_class, accepting all current constant-pool tags."""
    from 編譯器 import 讀取資料, 解碼已修改UTF8, 編譯過程錯誤
    r = 讀取資料(Path(path).read_bytes())
    if r.數('I') != 0xcafebabe:
        raise 編譯過程錯誤('Java 類別值 표식이 아님: ' + str(path))
    r.讀取(4)
    pool = [None] * r.數('H')
    i = 1
    while i < len(pool):
        tag = r.數('B')
        if tag == 1:
            pool[i] = 解碼已修改UTF8(r.讀取(r.數('H')))
        elif tag in (7, 8, 16, 19, 20):
            pool[i] = r.數('H')
        elif tag in (3, 4, 9, 10, 11, 12, 17, 18):
            r.讀取(4)
        elif tag in (5, 6):
            r.讀取(8)
            i += 1
        elif tag == 15:
            r.讀取(3)
        else:
            raise 編譯過程錯誤('알 數 없는 常量值 種類值: ' + str(tag))
        i += 1
    r.讀取(2)
    try:
        name = pool[pool[r.數('H')]]
    except (IndexError, TypeError):
        raise 編譯過程錯誤('잘못된 類別值 名稱 引用')
    if not isinstance(name, str) or any(p in ('', '.', '..') for p in name.split('/')) or '\\' in name:
        raise 編譯過程錯誤('잘못된 類別值 名稱')
    return name


def C字符串(text):
    # All bytes use fixed-width octal escapes: neither C nor the shell sees
    # untrusted quotes, escapes or command substitutions.
    return '"' + ''.join('\\%03o' % b for b in text.encode('utf-8')) + '"'


def 創建條目(args):
    from 編譯器 import 編譯過程錯誤
    output = Path(args.output).absolute()
    if ':' in str(output):
        raise 編譯過程錯誤('執行命令 檔案 경로에는 Java 類別值 路徑 구분자인 콜론(:)을 사용할 數 缺失方法')
    if output.is_symlink():
        raise 編譯過程錯誤('출력은 심볼릭 링크일 數 缺失方法')
    inputs = [Path(p).resolve() for p in args.sources]
    dependencies = [Path(p).resolve() for p in args.classpath]
    if output.resolve() in inputs + dependencies:
        raise 編譯過程錯誤('출력이 입력과 相等文本')
    for p in inputs + dependencies:
        if not p.exists():
            raise 編譯過程錯誤('입력이 缺失方法: ' + str(p))
    if args.export:
        raise 編譯過程錯誤('openjdk 執行命令 파일은 內建 內核值 ABI 내보내기를 지원하지 않음')
    if not args.entry or args.entry.startswith('-') or '/' in args.entry:
        raise 編譯過程錯誤('진입점은 public static void main(String[])을 가진 類別值 名稱')
    output.parent.mkdir(parents=True, exist_ok=True)
    bundle = output.with_name(output.name + '.app')
    if bundle.exists() and not (bundle / 'jkoros-application.json').is_file():
        raise 編譯過程錯誤('프로젝트가 생성하지 않은 디렉터리가 이미 있음: ' + str(bundle))
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
                    raise 編譯過程錯誤('輸出 디렉터리를 포함한 輸入值 디렉터리는 사용할 數 缺失方法')
                dest = lib / ('dependency-' + str(i))
                shutil.copytree(str(p), str(dest), symlinks=False)
                paths.append(str(dest.relative_to(app)))
            elif p.suffix == '.java' and p in inputs:
                sources.append(p)
            elif p.suffix == '.class':
                dest = classes / (類別條目名稱(p) + '.class')
                dest.parent.mkdir(parents=True, exist_ok=True)
                if dest.exists() and dest.read_bytes() != p.read_bytes():
                    raise 編譯過程錯誤('중복 類別值: ' + str(dest))
                shutil.copy2(str(p), str(dest))
            elif p.suffix in ('.jar', '.zip'):
                with zipfile.ZipFile(str(p)) as jar:
                    if jar.testzip() is not None:
                        raise 編譯過程錯誤('손상된 JAR: ' + str(p))
                dest = lib / ('dependency-{}.jar'.format(i))
                shutil.copy2(str(p), str(dest))
                paths.append(str(dest.relative_to(app)))
            else:
                raise 編譯過程錯誤('支持值 輸入值: .java, .class, .jar, 類別值/리소스 디렉터리')
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
            raise 編譯過程錯誤('條目分值 클래스를 찾을 數 缺失方法: ' + args.entry)
        if args.bundle_runtime:
            runtime = Path(args.bundle_runtime).resolve()
            if not (runtime / 'bin/java').is_file():
                raise 編譯過程錯誤('JDK/JRE의 bin/java가 缺失方法')
            shutil.copytree(str(runtime), str(app / 'runtime'), symlinks=True)
        template = Path(__file__).with_name('運行器.c').read_text()
        template = template.replace('@ENTRY@', C字符串(args.entry))
        template = template.replace('@CLASSPATH@', ', '.join(C字符串(p) for p in paths))
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
    print('OpenJDK 執行命令 檔案 生成: {} (함께 移動值: {})'.format(output, bundle))
