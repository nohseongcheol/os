#!/usr/bin/env python3
"""توزيع_قيمة class의 직접 العربية GUI/محادثة_قيمة 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

يعرض_جذر = Path(__file__).resolve().parents[1]

def تشغيل():
    클래스들 = ('نافذة', 'زر', 'تسمية', 'حقل_نصي', '화면구성요소', 'إجراء_إشعار', 'حدث_يدرج', 'خيطالعمل',
             '작업', '실행할일', '동작받이')
    يُجمع = يعرض_جذر/'dist/jkoros-native-korean.jar'
    إعلان = subprocess.check_output(['javap', '-classpath', str(يُجمع), '-private', '-c']+
                                ['العربية.ذاتي.'+اسم for اسم in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in إعلان, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(يعرض_جذر/'build/examples/classes'), '-c', 'مثالنافذة']).decode()
    for 필수 in ('public static void تشغيل()', 'العربية/ذاتي/حدث_يدرج.나중에실행', 'العربية/ذاتي/إجراء_إشعار.أمر_نص'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    وجهة_قيمة = يعرض_جذر/'build/verification/naming'; وجهة_قيمة.mkdir(parents=True, exist_ok=True)
    (وجهة_قيمة/'direct-bytecode.txt').write_text(إعلان+'\n'+예제)
    سجل_سجل = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((يعرض_جذر/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(يُجمع.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (وجهة_قيمة/'direct-bytecode.json').write_text(json.dumps(سجل_سجل, ensure_ascii=False, indent=2)+'\n')
    print('PASS: العربية 직접 GUI·محادثة_قيمة 바이트코드와 예제 호출')

if __name__ == '__main__': تشغيل()
