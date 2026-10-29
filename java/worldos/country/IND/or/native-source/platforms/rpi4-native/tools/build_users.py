#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/ବିଲ୍ଡ୍_ଉପଭୋକ୍ତା_ସ୍ଥାନ.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('ବିଲ୍ଡ୍_ଉପଭୋକ୍ତା_ସ୍ଥାନ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ବିଲ୍ଡ୍_ଉପଭୋକ୍ତା_ସ୍ଥାନ')
    대응 = {'mode': 'ପଦ୍ଧତି_ମୋଡ୍', 'header': 'ଶୀର୍ଷକ_ମୂଲ୍ୟ', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'ଅଭିଲେଖାଗାର_ଉପକରଣ', 'posix': '포직스경로', 'payload': 'ପେଲୋଡ୍_ଡାଟା', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'ଡାଟା', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'ପାଠ୍ଯ', 'headers': 'ଶୀର୍ଷକ_ତାଲିକା', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'ବିଲ୍ଡ୍', 'build_users': 'ସୃଷ୍ଟି_ଉପଭୋକ୍ତା_ସ୍ଥାନ', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'ଅନୁପ୍ରୟୋଗ_ଶୀର୍ଷକ_ଅଫ୍_ସେଟ୍', 'offset': 'ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ', 'text_address': 'ନିର୍ଦ୍ଦେଶ_ଠିକଣା', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ', 'path': 'ପଥ', 'p': 'ଡାଟା_ସ୍ଥିତି', 'changed': '바뀐자료', 'n': '개수', 'flag': 'ସେଟିଂସ୍_ମୂଲ୍ୟ', 'index': 'ଦୃଷ୍ଟିପାତ_ଅନୁକ୍ରମଣିକା', 'classes': 'ଶ୍ରେଣୀ_ପଥ', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'ଡାଟା_ଠିକଣା', 'symbol': 'ସଙ୍କେତ_ମୂଲ୍ୟ', 'root': 'ରୁଟ୍_ଠିକଣା', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'ନାମ', 'value': 'ମୂଲ୍ୟ', 'fmt': 'ଫର୍ମାଟ୍_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
