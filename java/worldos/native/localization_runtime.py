"""Allow UTF-8 names in built-in JVM resources without changing disk formats.

The filesystem keeps its existing limits. Built-in classes are looked up after
an unsuccessful filesystem open and need larger names independently of it.
Patches are shared by fresh generation and existing-edition migrations.
"""
import json
import re
from source_names import make_renamer, rename_source

PATCHES = {
    'platforms/rpi4-native/도구/예제빌드.py': [
        ('if len(내용)>16384: raise ValueError(\'Python library exceeds native VFS limit: \'+대상)',
         'if len(내용)>16384 or len(대상.encode(\'utf-8\'))>63: raise ValueError(\'Python library exceeds native VFS limit: \'+대상)')],
    'platforms/rpi4-native/도구/자바라이브러리빌드.py': [
        ("len(이름.encode('utf-8')) > 63", "len(이름.encode('utf-8')) > 511")],
    'platforms/rpi4-native/사용자/자바연결.c': [
        ('char 결과자료[64]', 'char 결과자료[512]'),
        ('사용량 + 개수 > 63', '사용량 + 개수 > 511'),
        ('char 자료위치[64]', 'char 자료위치[512]')],
    'platforms/rpi4-native/사용자/자바/자바가상기계.java': [
        ('파일명 = new int[64]', '파일명 = new int[512]'),
        ('길이 > 57 || 종수 == 16', '길이 > 505 || 종수 == 16')],
    'platforms/rpi4-native/사용자/꾸러미.c': [
        ('이름길이>255', '이름길이>511')],
}


def patches(mapping):
    rename = make_renamer(mapping)
    return {rename(path): [(rename_source(path, old, rename), rename_source(path, new, rename))
                            for old, new in edits] for path, edits in PATCHES.items()}


def update(text, edits):
    for before, after in edits:
        if before in text:
            text = text.replace(before, after)
        elif after not in text:
            raise ValueError('JVM name-limit patch does not match the owned source: ' + before)
    return text


def repair_input_help(text, mapping, help_text, details=None):
    """Keep human prose out of package/identifier alias substitutions."""
    method = make_renamer(mapping)('한글도움말')
    if details is not None:
        pattern = re.compile(r'(static\s+void\s+' + re.escape(method) +
                             r'\s*\(\s*\)\s*\{)\s*([^\s(]+)\(.*?\n    }', re.S)
        result, count = pattern.subn(lambda m: m.group(1)+'\n'+''.join(
            '        '+m.group(2)+'('+json.dumps(line+'\n', ensure_ascii=False)+');\n'
            for line in details)+'    }', text, count=1)
        if count != 1:
            raise ValueError('Missing generated input-help body: ' + method)
        return result
    pattern = re.compile(r'(\bstatic\s+void\s+' + re.escape(method) +
                         r'\s*\(\s*\)\s*\{\s*[^\s(]+\s*\()\s*"(?:\\.|[^"\\])*"')
    result, count = pattern.subn(lambda m: m.group(1) + json.dumps(help_text + '\n', ensure_ascii=False), text, count=1)
    if count != 1:
        raise ValueError('Missing generated input-help method: ' + method)
    return result
