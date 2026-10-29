#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/ፈጽም_ትእዛዝ.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('ፈጽም_ትእዛዝ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ፈጽም_ትእዛዝ')
    대응 = {'supported': '지원목록', 'parser': 'አግልሎ_ማስቀመጥ', 'qemu': '모의기계', 'run_desktop': 'አሂድ_ዴስክቶፕ', 'main': 'ማስኬጃ', 'host': 'አዘጋጅ_b78e430d', 'status': 'ዞን_እሴት', 'NetworkBridge': 'መረብ_ድልድይ', 'ROOT': 'አሳይ_ስር', 'bridge': 'ድልድይ', 'loader': '적재기', 'base': 'ልጣፍ_እሴት', 'options': 'አማራጮች', 'binary': 'ባይነሪ', 'args': 'ነጋሪ_እሴት_ድርድር', 'command': 'ትእዛዝ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
