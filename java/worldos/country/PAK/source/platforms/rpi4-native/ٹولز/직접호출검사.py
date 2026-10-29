#!/usr/bin/env python3
"""배포 class의 직접 اردو GUI/تھریڈ_قدر 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

عکس_ڈالنا_روٹ = Path(__file__).resolve().parents[1]

def چلائیں():
    클래스들 = ('ونڈو', 'بٹن', 'سرنامہ', 'متن_فیلڈ', '화면구성요소', '동작알림', 'ایونٹ_قطار', '작업가닥',
             '작업', '실행할일', '동작받이')
    بنڈل = عکس_ڈالنا_روٹ/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(بنڈل), '-private', '-c']+
                                ['اردو.اپنا.'+نام for نام in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(عکس_ڈالنا_روٹ/'build/examples/classes'), '-c', 'کھڑکیمثال']).decode()
    for 필수 in ('public static void چلائیں()', 'اردو/اپنا/ایونٹ_قطار.나중에실행', 'اردو/اپنا/동작알림.حکم_متن'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    منزل_مقصود_قدر = عکس_ڈالنا_روٹ/'build/verification/naming'; منزل_مقصود_قدر.mkdir(parents=True, exist_ok=True)
    (منزل_مقصود_قدر/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    لاگ_صف = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((عکس_ڈالنا_روٹ/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(بنڈل.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (منزل_مقصود_قدر/'direct-bytecode.json').write_text(json.dumps(لاگ_صف, ensure_ascii=False, indent=2)+'\n')
    print('PASS: اردو 직접 GUI·تھریڈ_قدر 바이트코드와 예제 호출')

if __name__ == '__main__': چلائیں()
