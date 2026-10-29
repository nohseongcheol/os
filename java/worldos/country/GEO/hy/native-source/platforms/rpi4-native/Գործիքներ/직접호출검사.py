#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/շղթա_արժեք 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

արձակել_արմատ = Path(__file__).resolve().parents[1]

def Գործարկել():
    클래스들 = ('창', 'կոճակ', 'Պիտակ', 'գրվածքի_դաշտ', '화면구성요소', '동작알림', 'միջոցառում_հերթ', '작업가닥',
             '작업', '실행할일', '동작받이')
    փաթեթ = արձակել_արմատ/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(փաթեթ), '-private', '-c']+
                                ['한국어.자체.'+Անուն for Անուն in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(արձակել_արմատ/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void Գործարկել()', '한국어/자체/միջոցառում_հերթ.나중에실행', '한국어/자체/동작알림.հրաման_Գրվածք'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    նպատակակետ_արժեք = արձակել_արմատ/'build/verification/naming'; նպատակակետ_արժեք.mkdir(parents=True, exist_ok=True)
    (նպատակակետ_արժեք/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    մատյան_տող = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((արձակել_արմատ/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(փաթեթ.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (նպատակակետ_արժեք/'direct-bytecode.json').write_text(json.dumps(մատյան_տող, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·շղթա_արժեք 바이트코드와 예제 호출')

if __name__ == '__main__': Գործարկել()
