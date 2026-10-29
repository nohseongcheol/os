#!/usr/bin/env python3
"""Native Java localScope 이름을 바꾼다. stringValue·주석·externalValue 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

projectRoot = Path(__file__).resolve().parents[1]
mappingValue = json.loads((projectRoot / 'naming/javaNames.json').read_text())
chunkExpression = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
logRecord = []
for directoryValue in ('source', 'User/Java', 'NativeJava'):
    for path in sorted((projectRoot / directoryValue).rglob('*.java')):
        source = path.read_text()
        chunksList = list(chunkExpression.finditer(source))
        usedName = {chunkEntry.group() for chunkEntry in chunksList if re.search('[firstOperand-힣]', chunkEntry.group())}
        fileMapping = {}
        for previousItem, afterValue in mappingValue.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            newName = afterValue
            while newName in usedName: newName = 'localScope' + newName
            fileMapping[previousItem] = newName
        modifyValue = []
        previousChunk = ''
        for chunkEntry in chunksList:
            lexicalWord = chunkEntry.group()
            if lexicalWord.startswith(('//', '/*', '"', "'")): continue
            if lexicalWord in fileMapping and previousChunk != '.':
                modifyValue.append((chunkEntry.start(), chunkEntry.end(), fileMapping[lexicalWord]))
                logRecord.append((str(path.relative_to(projectRoot)), lexicalWord, fileMapping[lexicalWord]))
            previousChunk = lexicalWord
        for run, ending, newName in reversed(modifyValue): source = source[:run] + newName + source[ending:]
        if modifyValue: path.write_text(source)
(projectRoot / 'naming/javaNameMapping.tsv').write_text('file\t이전\t이후\n' + ''.join('\t'.join(entryValue)+'\n' for entryValue in sorted(set(logRecord))))
print('Java name reference changeValue:', len(logRecord))
