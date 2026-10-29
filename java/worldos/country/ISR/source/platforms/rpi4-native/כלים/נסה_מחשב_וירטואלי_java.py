#!/usr/bin/env python3
"""OpenJDK와 עצמי ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from לבצע_פקודה import לשקף_בסיס


def הפעלה():
    פלט = לשקף_בסיס / 'build/verification/jvm'
    כיתה_נתיב = פלט / 'classes'; כיתה_נתיב.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = לשקף_בסיס / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((לשקף_בסיס / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(כיתה_נתיב)] + [str(מחרוזת_נתונים) for מחרוזת_נתונים in 원문목록])
    רשימת_בדיקות = [('객체시험', ['טפט_ערך', 'ענף_ערך', '계산가능']), ('예외시험', []), ('אוסף_נסה', []),
             ('가닥시험', ['מונה_ערך', 'משימה_המלצה', 'שרשור_ערך']), ('한글시험', []), ('נסה_עבודה_ברשת', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('לאמת.נסה_חבילה', []), ('ערך_תאימות_נסה', [])]
    אימות_דוח = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((לשקף_בסיס / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for שם, 포함인수 in רשימת_בדיקות:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(כיתה_נתיב) + ':' + str(자바꾸러미), שם], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(לשקף_בסיס / 'כלים/לבצע_קובץ.py'), str(כיתה_נתיב / (שם.replace('.', '/') + '.class'))]
            if '.' in שם: 명령인수 += ['--class-name', שם]
            for לכלול in 포함인수: 명령인수 += ['--include', str(כיתה_נתיב / (לכלול + '.class'))]
            if שם == '한글소스': 명령인수[2] = str(לשקף_בסיס / '시험/자바/한글소스.java')
            הושלם_סכום = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            בפועל_תוצאה = הושלם_סכום.stdout.decode('utf-8').replace('\r\n', '\n')
            (פלט / (שם + '.log')).write_text(בפועל_תוצאה, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", בפועל_תוצאה, re.S)
            assert הושלם_סכום.returncode == 0 and 일치, (שם, בפועל_תוצאה)
            תוצאה = next(מחרוזת_נתונים for מחרוזת_נתונים in 일치.groups() if מחרוזת_נתונים is not None) + '\n'
            assert תוצאה == 예상결과, (שם, 예상결과, תוצאה)
            אימות_דוח['tests'].append({'name': שם, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', שם, flush=True)
        # עצמי JVM에 직접 연결한 עברית שרשור_ערך/진입점은 OpenJDK용 래퍼가 아니다.
        הושלם_סכום = subprocess.run(['python3', str(לשקף_בסיס/'כלים/לבצע_קובץ.py'), str(כיתה_נתיב/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        תוצאה = הושלם_סכום.stdout.decode('utf-8').replace('\r\n', '\n')
        (פלט/'한국어가닥시험.log').write_text(תוצאה)
        assert הושלם_סכום.returncode == 0 and 'עברית 직접 שרשור_ערך להעביר_ערך_07b9cb2b\n' in תוצאה and '\nexit 0\n' in תוצאה, תוצאה
        אימות_דוח['direct_korean_thread_and_entry'] = True
        print('PASS: עברית 직접 שרשור_ערך·בצע·הפעלה נקודת_כניסה', flush=True)
        유효함 = (כיתה_נתיב / '객체시험.class').read_bytes()
        מפרט_בדיקה = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        אימות_דוח['rejection_tests'] = []
        for שם, מטען_נתונים, הודעה_טקסט in מפרט_בדיקה:
            נסה_נתונים = פלט / (שם + '.class'); נסה_נתונים.write_bytes(מטען_נתונים)
            הושלם_סכום = subprocess.run(['python3', str(לשקף_בסיס / 'כלים/לבצע_קובץ.py'), str(נסה_נתונים)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            טקסט = הושלם_סכום.stdout.decode('utf-8').replace('\r\n', '\n')
            (פלט / (שם + '.log')).write_text(טקסט, encoding='utf-8')
            assert הושלם_סכום.returncode == 1 and הודעה_טקסט in טקסט and 'exit 1\n' in טקסט, (שם, טקסט)
            אימות_דוח['rejection_tests'].append({'name': שם, 'passed': True})
            print('PASS (rejected):', שם, flush=True)
        אימות_דוח['passed'] = True
    finally:
        (פלט / 'report.json').write_text(json.dumps(אימות_דוח, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    הפעלה()
