#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/ህነጽ_ስርዓት.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('ህነጽ_ስርዓት', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ህነጽ_ስርዓት')
    대응 = {'network': 'ማሕበራዊ_ኔትወርክ', 'BUILD': 'ህነጽ_መገዲ', 'ar': 'ሰንድ_መሳርሒ', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ቅርጺ_ፊደል_ሓበሬታ', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'ሓባሪ_ቁጽሪ_ተርታ', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'ሜላ_ምእታው', 'main': 'ኣኺድ', 'objcopy': 'ነገር_ፋይል_ለዋጢ', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'ፍጠር_ተጠቃሚ_ቦታ', 'f': 'ፋይል_ምእታው', 'extra': '추가영역', 'exports': 'ስደድ_ሰሌዳ', 'jobs': '빌드작업', 'run': 'ተግብር_ትእዛዝ', 'path': 'መገዲ', 'REPO': '저장소', 'tool': 'መሳርሒታት', 'classes': 'ክፍሊ_መገዲ', 'output': '출력결과', 'samples': '예제들', 'symbol': 'ምልክት_ዋጋ', 'source': '원본자료', 'name': 'ሽም', 'build_network': 'ፍጠር_ማሕበራዊ_ኔትወርክ', 'font_info': 'ቅርጺ_ፊደል_ሓበሬታ_c16c0f1c', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
