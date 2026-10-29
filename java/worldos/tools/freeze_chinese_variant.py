#!/usr/bin/env python3
"""Freeze the explicitly selected Traditional Chinese script and vocabulary.

This converts written Mandarin forms, not Japanese, Cantonese or another
language. Regionally familiar technical roots are selected explicitly below.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def converter():
    tree = {}
    hashes = {}
    for name in ('STCharacters.txt', 'STPhrases.txt'):
        path = ROOT / 'native/inputs/chinese-script-data' / name
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        for line in path.read_text().splitlines():
            if line.startswith('#') or '\t' not in line:
                continue
            source, targets = line.split('\t', 1)
            node = tree
            for char in source:
                node = node.setdefault(char, {})
            node[None] = targets.split()[0]

    def convert(text):
        result = []
        start = 0
        while start < len(text):
            node = tree
            end = start
            found = None
            while end < len(text) and text[end] in node:
                node = node[text[end]]
                end += 1
                if None in node:
                    found = (end, node[None])
            if found:
                start, value = found
                result.append(value)
            else:
                result.append(text[start])
                start += 1
        return ''.join(result)
    return convert, hashes


def main():
    convert, hashes = converter()
    source = ROOT / 'native/inputs/chinese-role-words.tsv'
    words = {r['word']: convert(r['proposal']) for r in csv.DictReader(source.open(), delimiter='\t')}
    words.update({'memory': '記憶體', 'file': '檔案', 'files': '檔案集',
                  'source': '原始碼', 'sources': '原始碼列', 'data': '資料',
                  'byte': '位元組', 'bytes': '位元組列', 'bit': '位元', 'bits': '位元列',
                  'array': '陣列', 'arrays': '陣列集', 'thread': '執行緒', 'threads': '執行緒集',
                  'process': '程序', 'processes': '程序列', 'program': '程式', 'programs': '程式列',
                  'protocol': '通訊協定', 'network': '網路', 'net': '網路層',
                  'socket': '通訊端', 'port': '埠', 'ports': '埠列', 'buffer': '緩衝區',
                  'cache': '快取', 'object': '物件', 'objects': '物件集',
                  'parameter': '形式參數', 'argument': '實際參數', 'character': '字元',
                  'characters': '字元列', 'class': '類別', 'classes': '類別集',
                  'call': '呼叫', 'example': '範例', 'examples': '範例集',
                  'header': '標頭', 'headers': '標頭集', 'column': '欄', 'columns': '欄集',
                  'row': '列', 'rows': '列集', 'code': '程式碼', 'virtual': '虛擬'})
    target = ROOT / 'native/inputs/traditional-chinese-role-words.tsv'
    target.write_text('word\tproposal\n' + ''.join(k+'\t'+v+'\n' for k, v in sorted(words.items())))
    correction = ROOT / 'native/inputs/reviewed-roles/zh_Hans.json'
    document = json.loads(correction.read_text())
    document['language'] = 'zh_Hant'
    document['names'] = {k: convert(v) for k, v in document['names'].items()}
    document['names'].update({
        '원문': '原始碼', '원문목록': '原始碼列表', '원천': '基礎原始碼',
        '자체': '內建', '한국어자바': '中文Java', '문자': '字元', '문자단말': '字元終端',
        '문자이름규칙': '識別字字元規則', '파일': '檔案', '파일보존': '檔案持久化',
        '파일서술자관리': '檔案描述子管理', '주기억파일체계': '主記憶體檔案系統',
        '기억공간': '記憶體空間', '기억': '記憶體', '주기억': '主記憶體',
        '자료': '資料', '자료되돌리기': '資料復原', '자바파일묶기': 'Java檔案打包',
        '자바파일시험': 'Java檔案測試', '파일예제': '檔案例', '네트워크예제': '網路例',
        '예제': '範例', '예제규약': '範例約定', '프로그램': '程式', '체계호출': '系統呼叫',
        '가상기계': '虛擬機器', '자바가상기계': 'Java虛擬機器', '네트워크': '網路連接',
        '통신사용': '使用網路', '사용자안내': '使用者指南', '사용자': '使用者',
    })
    document['references'].append('https://github.com/BYVoid/OpenCC/tree/8cf737a4e193db27d675b2ce9867d84aace33745')
    document['script_conversion'] = {'upstream_commit': '8cf737a4e193db27d675b2ce9867d84aace33745',
                                     'files_sha256': hashes,
                                     'scope': 'Mandarin written forms only; technical vocabulary choices above are explicit modern proposals.'}
    (ROOT / 'native/inputs/reviewed-roles/zh_Hant.json').write_text(json.dumps(document, ensure_ascii=False, indent=2)+'\n')
    (ROOT / 'native/inputs/chinese-script-data/provenance.json').write_text(json.dumps(document['script_conversion'], ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    main()
