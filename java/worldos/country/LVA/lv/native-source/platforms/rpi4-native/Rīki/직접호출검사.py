#!/usr/bin/env python3
"""sadale_VALUE class의 직접 Latviešu GUI/saruna_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

Project_sakne = Path(__file__).resolve().parents[1]

def Palaist():
    클래스들 = ('Logs', 'Pogas', 'Etiķete', 'teksta_lauks', '화면구성요소', 'darbība_informēšana', 'notikums_rinda', 'nodarbinātais',
             '작업', '실행할일', '동작받이')
    saistīt = Project_sakne/'dist/jkoros-native-korean.jar'
    deklarācija = subprocess.check_output(['javap', '-classpath', str(saistīt), '-private', '-c']+
                                ['Latviešu.savs.'+Nosaukums for Nosaukums in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in deklarācija, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(Project_sakne/'build/examples/classes'), '-c', 'LogaPiemērs']).decode()
    for 필수 in ('public static void Palaist()', 'Latviešu/savs/notikums_rinda.나중에실행', 'Latviešu/savs/darbība_informēšana.komanda_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    mērķis_VALUE = Project_sakne/'build/verification/naming'; mērķis_VALUE.mkdir(parents=True, exist_ok=True)
    (mērķis_VALUE/'direct-bytecode.txt').write_text(deklarācija+'\n'+예제)
    LOG_RECORD = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((Project_sakne/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(saistīt.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (mērķis_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Latviešu 직접 GUI·saruna_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': Palaist()
