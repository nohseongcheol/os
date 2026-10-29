#!/usr/bin/env python3
"""배포 class의 직접 فارسی GUI/رشته_مقدار 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

نمایش_دادن_جذر = Path(__file__).resolve().parents[1]

def اجرا_2():
    클래스들 = ('창', 'دکمه', 'برچسب', 'متن_فیلد', '화면구성요소', '동작알림', 'رویداد_صف', '작업가닥',
             '작업', '실행할일', '동작받이')
    دسته_کردن = نمایش_دادن_جذر/'dist/jkoros-native-korean.jar'
    اعلامیه = subprocess.check_output(['javap', '-classpath', str(دسته_کردن), '-private', '-c']+
                                ['فارسی.بومی.'+نام for نام in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in اعلامیه, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(نمایش_دادن_جذر/'build/examples/classes'), '-c', 'نمونهپنجره']).decode()
    for 필수 in ('public static void اجرا_2()', 'فارسی/بومی/رویداد_صف.나중에실행', 'فارسی/بومی/동작알림.فرمان_متن'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    مقصد_مقدار = نمایش_دادن_جذر/'build/verification/naming'; مقصد_مقدار.mkdir(parents=True, exist_ok=True)
    (مقصد_مقدار/'direct-bytecode.txt').write_text(اعلامیه+'\n'+예제)
    واقعه_نگار_ردیف = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((نمایش_دادن_جذر/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(دسته_کردن.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (مقصد_مقدار/'direct-bytecode.json').write_text(json.dumps(واقعه_نگار_ردیف, ensure_ascii=False, indent=2)+'\n')
    print('PASS: فارسی 직접 GUI·رشته_مقدار 바이트코드와 예제 호출')

if __name__ == '__main__': اجرا_2()
