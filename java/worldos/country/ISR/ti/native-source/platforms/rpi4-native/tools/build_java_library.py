#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'ርእሲ_ዋጋ', 'sources': '원문목록', 'i': '순번', 'info': 'ናይ_ስርዓት_ሓበሬታ', 'payload': 'ጽዕነት_ክፍሊት_ሓበሬታ', 'src': '원본주소', 'run': 'ተግብር_ትእዛዝ', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'ክፍሊ_መገዲ', 'dist': '배포경로', 'archive': 'ሰንድ', 'output': '출력결과', 'root': '뿌리주소', 'name': 'ሽም', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
