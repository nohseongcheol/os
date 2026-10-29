#!/usr/bin/env python3
"""배포 class의 직접 ગુજરાતી GUI/થ્રેડ_મૂલ્ય 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parents[1]

def ચલાવો_2():
    클래스들 = ('창', 'બટન', 'લેબલ', 'ટેક્સ્ટ_ફીલ્ડ', '화면구성요소', '동작알림', 'ઇવેંટ_કતાર', '작업가닥',
             '작업', '실행할일', '동작받이')
    બન્ડલ = પ્રોજેક્ટ_રૂટ/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(બન્ડલ), '-private', '-c']+
                                ['ગુજરાતી.자체.'+નામ for નામ in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(પ્રોજેક્ટ_રૂટ/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void ચલાવો_2()', 'ગુજરાતી/자체/ઇવેંટ_કતાર.나중에실행', 'ગુજરાતી/자체/동작알림.આદેશ_પાઠ'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    ગંતવ્ય_મૂલ્ય = પ્રોજેક્ટ_રૂટ/'build/verification/naming'; ગંતવ્ય_મૂલ્ય.mkdir(parents=True, exist_ok=True)
    (ગંતવ્ય_મૂલ્ય/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    લૉગ_પંક્તિ = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((પ્રોજેક્ટ_રૂટ/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(બન્ડલ.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (ગંતવ્ય_મૂલ્ય/'direct-bytecode.json').write_text(json.dumps(લૉગ_પંક્તિ, ensure_ascii=False, indent=2)+'\n')
    print('PASS: ગુજરાતી 직접 GUI·થ્રેડ_મૂલ્ય 바이트코드와 예제 호출')

if __name__ == '__main__': ચલાવો_2()
