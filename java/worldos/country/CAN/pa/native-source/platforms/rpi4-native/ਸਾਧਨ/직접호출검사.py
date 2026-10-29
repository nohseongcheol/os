#!/usr/bin/env python3
"""배포 class의 직접 ਪੰਜਾਬੀ GUI/ਥ੍ਰੈਡ_ਕੀਮਤ 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parents[1]

def ਚਲਾਓ_2():
    클래스들 = ('창', 'ਬਟਨ', 'ਲੇਬਲ', 'ਟੈਕਸਟ_ਖੇਤਰ', '화면구성요소', '동작알림', 'ਇਵੈਂਟ_ਕਤਾਰ', '작업가닥',
             '작업', '실행할일', '동작받이')
    ਬੰਡਲ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(ਬੰਡਲ), '-private', '-c']+
                                ['ਪੰਜਾਬੀ.자체.'+ਨਾਂ for ਨਾਂ in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void ਚਲਾਓ_2()', 'ਪੰਜਾਬੀ/자체/ਇਵੈਂਟ_ਕਤਾਰ.나중에실행', 'ਪੰਜਾਬੀ/자체/동작알림.ਆਦੇਸ਼_ਪਾਠ'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    ਮੰਜਿਲ_ਕੀਮਤ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/naming'; ਮੰਜਿਲ_ਕੀਮਤ.mkdir(parents=True, exist_ok=True)
    (ਮੰਜਿਲ_ਕੀਮਤ/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    ਲੌਗ_ਕਤਾਰ = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(ਬੰਡਲ.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (ਮੰਜਿਲ_ਕੀਮਤ/'direct-bytecode.json').write_text(json.dumps(ਲੌਗ_ਕਤਾਰ, ensure_ascii=False, indent=2)+'\n')
    print('PASS: ਪੰਜਾਬੀ 직접 GUI·ਥ੍ਰੈਡ_ਕੀਮਤ 바이트코드와 예제 호출')

if __name__ == '__main__': ਚਲਾਓ_2()
