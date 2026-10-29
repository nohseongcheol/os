#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/ፈጽም_ፋይል.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('ፈጽም_ፋይል', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ፈጽም_ፋይል')
    대응 = {'timeout': '시간제한', 's': 'ኅብረቁምፊ_ውሂብ', 'i': '순번', 'match': '일치', 'files': 'ፋይል_ዝርዝር', 'program': 'ፕሮግራም', 'executable': '실행가능파일', 'args': 'ነጋሪ_እሴት_ድርድር', 'chunk': '조각', 'data': 'ውሂብ', 'proc': 'ሂደቶች', 'send': 'ላክ', 'main': 'ማስኬጃ', 'marker': '확인표시', 'command': 'ትእዛዝ', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'ፈጽም_ትእዛዝ', 'p': 'ውሂብ_በቦታ_አስቀመጠ', 'parser': 'አግልሎ_ማስቀመጥ', 'options': 'አማራጮች', 'kind': 'ምድብ_እሴት', 'selector': 'መራጭ', 'upload_data': 'መጫን_ውሂብ', 'end': 'ጨርስ_ዝንፍ', 'n': '개수', 'd': 'መድረሻ_ውሂብ', 'key': '누름값', 'output': '출력결과', 'line': 'መስመር', 'name': 'ስም', 'upload_name': 'መጫን_ስም', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
