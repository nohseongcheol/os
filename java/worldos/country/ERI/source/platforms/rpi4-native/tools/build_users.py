#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/ህነጽ_ተጠቃሚ_ቦታ.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('ህነጽ_ተጠቃሚ_ቦታ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ህነጽ_ተጠቃሚ_ቦታ')
    대응 = {'mode': 'ሜላ_ኹነት', 'header': 'ርእሲ_ዋጋ', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'ሰንድ_መሳርሒ', 'posix': '포직스경로', 'payload': 'ጽዕነት_ክፍሊት_ሓበሬታ', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'ሓበሬታ', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'ጽሑፍ', 'headers': 'ርእሲ_ዝርዝር', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'ህነጽ', 'build_users': 'ፍጠር_ተጠቃሚ_ቦታ', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'መተግበሪ_ርእሲ_ሽፋን', 'offset': 'ሽፋን_ዋጋ', 'text_address': 'ትእዛዝ_ኣድራሻ', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'ተግብር_ትእዛዝ', 'path': 'መገዲ', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'ኣቀማምጣታት_ዋጋ', 'index': '색인', 'classes': 'ክፍሊ_መገዲ', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'ሓበሬታ_ኣድራሻ', 'symbol': 'ምልክት_ዋጋ', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'ሽም', 'value': 'ዋጋ', 'fmt': 'ቅርጺ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
