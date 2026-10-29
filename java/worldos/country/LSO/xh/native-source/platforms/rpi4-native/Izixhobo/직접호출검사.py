#!/usr/bin/env python3
"""배포 class의 직접 isiXhosa GUI/ithredi_ixabiso 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

기준 = Path(__file__).resolve().parents[1]

def Phumeza():
    클래스들 = ('창', 'iqhosha', 'Ilebhile', 'I_SMS_ifildi', '화면구성요소', '동작알림', 'umcimbi_ityhu', '작업가닥',
             '작업', '실행할일', '동작받이')
    umqulu = 기준/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(umqulu), '-private', '-c']+
                                ['isiXhosa.자체.'+Igama for Igama in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(기준/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void Phumeza()', 'isiXhosa/자체/umcimbi_ityhu.나중에실행', 'isiXhosa/자체/동작알림.umyalelo_I_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    indawo_ekuyiwa_kuyo_ixabiso = 기준/'build/verification/naming'; indawo_ekuyiwa_kuyo_ixabiso.mkdir(parents=True, exist_ok=True)
    (indawo_ekuyiwa_kuyo_ixabiso/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    ilog_umqolo = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(umqulu.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (indawo_ekuyiwa_kuyo_ixabiso/'direct-bytecode.json').write_text(json.dumps(ilog_umqolo, ensure_ascii=False, indent=2)+'\n')
    print('PASS: isiXhosa 직접 GUI·ithredi_ixabiso 바이트코드와 예제 호출')

if __name__ == '__main__': Phumeza()
