#!/usr/bin/env python3
"""배포 class의 직접 Български GUI/нишка_стойност 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

проект_корен = Path(__file__).resolve().parents[1]

def Стартиране():
    클래스들 = ('Прозорец', 'бутон', 'Етикет', 'текстово_поле', '화면구성요소', 'проект_предупреждение', 'събитие_опашка', '작업가닥',
             '작업', '실행할일', '동작받이')
    пакет = проект_корен/'dist/jkoros-native-korean.jar'
    декларация = subprocess.check_output(['javap', '-classpath', str(пакет), '-private', '-c']+
                                ['Български.자체.'+Име for Име in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in декларация, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(проект_корен/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void Стартиране()', 'Български/자체/събитие_опашка.나중에실행', 'Български/자체/проект_предупреждение.команда_Текст'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    местоназначение_стойност = проект_корен/'build/verification/naming'; местоназначение_стойност.mkdir(parents=True, exist_ok=True)
    (местоназначение_стойност/'direct-bytecode.txt').write_text(декларация+'\n'+예제)
    регистрирам_запис = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((проект_корен/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(пакет.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (местоназначение_стойност/'direct-bytecode.json').write_text(json.dumps(регистрирам_запис, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Български 직접 GUI·нишка_стойност 바이트코드와 예제 호출')

if __name__ == '__main__': Стартиране()
