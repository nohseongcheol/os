"""Whole-sentence Java comments and library messages, shared by both workflows.

Only explicitly translated prose is replaced. Literal test data, author
attribution and unreviewed language editions retain their original bytes.
"""
import json
from functools import lru_cache
from pathlib import Path
import re
from source_names import make_renamer, rename_source

INPUT = Path(__file__).resolve().parent / 'inputs/localized-java-prose.json'
TOKENS = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')


@lru_cache(maxsize=1)
def document():
    return json.loads(INPUT.read_text())


@lru_cache(maxsize=64)
def replacements(language, items, native_name=''):
    data = document()
    rename = make_renamer(dict(items))
    result = {}
    for original, translation in data.get('comments', {}).get(language, {}).items():
        value=translation.replace('{echo_tool}',rename('도구/예제되돌림.py'))
        result[rename_source('comment.java', original, rename)] = value
        if native_name:
            result[rename_source('comment.java',original.replace('한글',native_name),rename)] = value
    template = data.get('exception_templates', {}).get(language)
    if template:
        for name in data['exception_roles']:
            original = '/** 한국어로 선언·던지기·잡기를 할 수 있는 ' + name + '. */'
            result[rename_source('comment.java', original, rename)] = template.format(type=rename(name))
    # Older independent editions can retain a previously reviewed wording of
    # a whole comment. Recognize exact recorded variants, never loose words.
    for alias, canonical in data.get('comment_aliases', {}).get(language, {}).items():
        key=rename_source('comment.java',canonical,rename)
        assert key in result, 'Unknown canonical comment for '+language
        result[alias]=result[key]
    return result


@lru_cache(maxsize=64)
def library_context(language, items):
    rename=make_renamer(dict(items))
    prefix='/'+rename('platforms/rpi4-native/한국어자바')+'/'
    messages={rename_source('message.java',json.dumps(k,ensure_ascii=False),rename):json.dumps(v,ensure_ascii=False)
              for k,v in document().get('library_messages',{}).get(language,{}).items()}
    return prefix,messages


def localize_java_comments(path, text, language, mapping, native_name=''):
    if not str(path).endswith('.java') or language == 'ko':
        return text
    items=tuple(sorted(mapping.items()))
    table = replacements(language, items, native_name)
    if not table:
        return text
    library,messages=library_context(language,items)
    normalized='/'+str(path).replace('\\','/')
    is_library=(library in normalized or '/platforms/rpi4-native/한국어자바/' in normalized)
    if not is_library:messages={}
    def replace(match):
        value=match.group()
        if value.startswith(('//','/*')):return table.get(value,value)
        return messages.get(value,value)
    return TOKENS.sub(replace,text)
