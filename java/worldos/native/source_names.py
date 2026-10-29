"""Rename symbolic text without changing literal Unicode character values."""
from pathlib import Path
from functools import lru_cache
import io
import re
import tokenize
import unicodedata


def legal_text(name):
    path = Path(name)
    value = path.name.lower()
    return path.suffix in ('', '.md', '.txt') and (
        value in ('license', 'copying', 'third_party_notices.md') or
        'cosl' in value or 'license' in value or '라이선스' in value or
        value in ('다시연결.md', 'relink.md'))


def rename_legal_paths(text, rename):
    # Legal clauses, author names and grants remain verbatim. Only actual
    # filename/path references follow files moved by the naming operation.
    pattern = re.compile(r'https?://[^\s`<>()[\]{};,]+|(?:[\w.-]+/)+[\w.\-/]+|[\w-]+\.(?:md|sh|py|mk|tsv|json|h|c)\b', re.UNICODE)
    return pattern.sub(lambda match: match.group() if match.group().startswith(('http://','https://')) else rename(match.group()), text)


def identifier_part(char):
    return char in '_$' or unicodedata.category(char)[0] in 'LMN' or unicodedata.category(char) in ('Pc', 'Cf')


def make_renamer(changes):
    if not changes:
        return lambda text: text
    tree = {}
    for key in changes:
        node = tree
        for char in key:
            node = node.setdefault(char, {})
        node[None] = {}
    def expression(node):
        branches = [re.escape(char) + expression(child) for char, child in sorted(
            (char, child) for char, child in node.items() if char is not None)]
        if None in node:
            branches.append('')
        return branches[0] if len(branches) == 1 else '(?:' + '|'.join(branches) + ')'
    pattern = re.compile(expression(tree))
    def rename(text):
        def replace(match):
            start, end = match.span()
            if end < len(text) and identifier_part(text[end]):
                return match.group()
            if start and identifier_part(text[start - 1]):
                # Only the immediately adjacent JVM descriptor prefix matters.
                # Searching the entire preceding file for each rejected suffix
                # made large dictionaries quadratic on ordinary prose.
                prefix = start - 1
                if text[prefix] != 'L':
                    return match.group()
                while prefix and text[prefix - 1] in 'VZBCSIJDF':
                    prefix -= 1
                if prefix and identifier_part(text[prefix - 1]):
                    return match.group()
            return changes[match.group()]
        return pattern.sub(replace, text)
    return rename


def rename_java_local_alias(text, changes):
    """Rename known local variables without rewriting Java API calls/strings."""
    quoted = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
    rename = make_renamer(changes)

    def code(part):
        # A boolean local cannot be invoked or qualified as an object member.
        tokens = re.compile('|'.join(re.escape(k) for k in sorted(changes, key=len, reverse=True)))
        def replace(match):
            start, end = match.span()
            if start and (identifier_part(part[start-1]) or part[start-1] == '.'):
                return match.group()
            if end < len(part) and identifier_part(part[end]):
                return match.group()
            if part[end:].lstrip().startswith('('):
                return match.group()
            return rename(match.group())
        return tokens.sub(replace, part)
    result = []
    offset = 0
    for match in quoted.finditer(text):
        result.extend((code(text[offset:match.start()]), match.group()))
        offset = match.end()
    result.append(code(text[offset:]))
    return ''.join(result)


@lru_cache(maxsize=4096)
def escape_python_byte_literals(text):
    """Keep translated byte literals valid without changing their UTF-8 data."""
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    edits = []
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type != tokenize.STRING:
            continue
        prefix = re.match(r'([bBrRuUfF]*)([\'\"])', token.string).group(1)
        if 'b' not in prefix.lower() or all(ord(char) < 128 for char in token.string):
            continue
        value = token.string[len(prefix):]
        if 'r' in prefix.lower():
            value = value.replace('\\', '\\\\')
        value = ''.join(char if ord(char) < 128 else ''.join('\\x%02x' % byte for byte in char.encode('utf-8')) for char in value)
        start = offsets[token.start[0]-1] + token.start[1]
        end = offsets[token.end[0]-1] + token.end[1]
        edits.append((start, end, 'b' + value))
    for start, end, value in reversed(edits):
        text = text[:start] + value + text[end:]
    return text


def rename_source(name, text, rename):
    if legal_text(name):
        return rename_legal_paths(text, rename)
    ordinary_rename = rename
    packages = r'(?:lang|io|util|net|nio|math|security|time|text|awt|beans|sql|swing|crypto|naming|xml|sound|management|print|annotation|tools|rmi|accessibility)'
    external = re.compile(r'\b(?:java|javax)\.' + packages + r'\.[\w.]+(?:\*)?|(?<![\w/])L?(?:java|javax)/' + packages + r'/[\w/$]+|\b(?:Integer|Long|Short|Byte|Boolean|Character|Double|Float|String|Object|System|Math|Stream)\b|(?<!\w)charset(?==)')
    def rename(piece):
        # These external identities also occur inside generated test sources
        # and HTTP string literals, not just ordinary Java imports.
        parts, offset = [], 0
        for match in external.finditer(piece):
            parts.extend((ordinary_rename(piece[offset:match.start()]), match.group()))
            offset = match.end()
        parts.append(ordinary_rename(piece[offset:]))
        return ''.join(parts)
    suffix = Path(name).suffix
    def literal_rename(value):
        option = re.compile(r'(?<![\w-])--?[A-Za-z][A-Za-z0-9_-]*(?![\w-])')
        pieces, start = [], 0
        for match in option.finditer(value):
            pieces.extend((rename(value[start:match.start()]), match.group()))
            start = match.end()
        pieces.append(rename(value[start:]))
        return ''.join(pieces)
    path = '/' + str(name).replace('\\', '/')
    symbolic = ('/tools/' in path or '/명명/' in path or
                path.endswith('/사용자/자바/자바가상기계.java'))
    if suffix not in ('.java', '.c', '.h', '.cpp', '.py', '.json'):
        return literal_rename(text)
    pattern = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
    parts = []
    offset = 0
    for match in pattern.finditer(text):
        parts.append(rename(text[offset:match.start()]))
        value = match.group()
        literal = value.startswith(('"', "'"))
        character = not symbolic and literal and len(value) == 3 and '\uac00' <= value[1] <= '\ud7a3'
        legal_notice = value.startswith(('//','/*')) and re.search(r'copyright|spdx-license|licensed under|저작권', value, re.I)
        if legal_notice or character or (suffix == '.java' and value.startswith(('java.', 'javax.'))) or (suffix in ('.java', '.c', '.h', '.cpp') and value.startswith("'")):
            parts.append(value)
        elif literal:
            if symbolic:
                parts.append(literal_rename(value))
                offset = match.end()
                continue
            # This text is used by charAt, UTF-8 and length fixtures. Equally
            # spelled local variables can still receive a functional name.
            parts.append('한글'.join(literal_rename(piece) for piece in re.split(r'(?<!\w)한글(?!\w)', value)))
        else:
            parts.append(rename(value))
        offset = match.end()
    parts.append(rename(text[offset:]))
    result = ''.join(parts)
    return escape_python_byte_literals(result) if suffix == '.py' else result
