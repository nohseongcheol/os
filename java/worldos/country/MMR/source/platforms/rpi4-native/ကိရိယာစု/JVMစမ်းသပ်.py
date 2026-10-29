#!/usr/bin/env python3
"""OpenJDK와 ကိုယ်ပိုင် ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from စက်မောင်း import စီမံကိန်းအမြစ်


def လုပ်ဆောင်():
    출력결과 = စီမံကိန်းအမြစ် / 'build/verification/jvm'
    အတန်းလမ်းကြောင်း = 출력결과 / 'classes'; အတန်းလမ်းကြောင်း.mkdir(parents=True, exist_ok=True)
    Javaအထုပ် = စီမံကိန်းအမြစ် / 'dist/jkoros-native-korean.jar'
    မူရင်းကုဒ်စာရင်း = sorted((စီမံကိန်းအမြစ် / 'စမ်းသပ်မှု/Java').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Javaအထုပ်), '-d', str(အတန်းလမ်းကြောင်း)] + [str(အက္ခရာစဉ်ဒေတာ) for အက္ခရာစဉ်ဒေတာ in မူရင်းကုဒ်စာရင်း])
    စာရင်းစမ်းသပ် = [('အရာဝတ္ထုစမ်းသပ်', ['နောက်ခံတန်ဖိုး', 'အခွဲတန်ဖိုး', 'နိုင်တွက်']), ('ခြွင်းချက်များစမ်းသပ်', []), ('အစုစမ်းသပ်', []),
             ('အလုပ်ကြိုးများစမ်းသပ်', ['ရေတွက်သူတန်ဖိုး', 'အလုပ်လုပ်ဆောင်ချက်', 'အလုပ်ကြိုးတန်ဖိုး']), ('ဟန်ဂုစမ်းသပ်', []), ('ဆက်သွယ်မှုစမ်းသပ်', []), ('မြန်မာကွန်ရက်စမ်းသပ်', []), ('မြန်မာခြွင်းချက်စမ်းသပ်', []), ('ဟန်ဂုမူရင်းကုဒ်', []), ('နယ်နိမိတ်စမ်းသပ်', []), ('မှန်ကန်ကြောင်းစစ်.အထုပ်စမ်းသပ်', []), ('အချက်လိုက်ဖက်မှုစမ်းသပ်', [])]
    검증기록 = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((စီမံကိန်းအမြစ် / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(Javaအထုပ်.read_bytes()).hexdigest(), 'tests': []}
    try:
        for အမည်, 포함인수 in စာရင်းစမ်းသပ်:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as ယာယီလမ်းကြောင်း:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(အတန်းလမ်းကြောင်း) + ':' + str(Javaအထုပ်), အမည်], cwd=ယာယီလမ်းကြောင်း, timeout=15).decode('utf-8')
            အမိန့်ပေးအချက်များ = ['python3', str(စီမံကိန်းအမြစ် / 'ကိရိယာစု/ဖိုင်လုပ်ဆောင်.py'), str(အတန်းလမ်းကြောင်း / (အမည်.replace('.', '/') + '.class'))]
            if '.' in အမည်: အမိန့်ပေးအချက်များ += ['--class-name', အမည်]
            for ပါဝင်စေ in 포함인수: အမိန့်ပေးအချက်များ += ['--include', str(အတန်းလမ်းကြောင်း / (ပါဝင်စေ + '.class'))]
            if အမည် == 'ဟန်ဂုမူရင်းကုဒ်': အမိန့်ပေးအချက်များ[2] = str(စီမံကိန်းအမြစ် / 'စမ်းသပ်မှု/Java/ဟန်ဂုမူရင်းကုဒ်.java')
            완료량 = subprocess.run(အမိန့်ပေးအချက်များ, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            실제결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (အမည် + '.log')).write_text(실제결과, encoding='utf-8')
            ဖြစ်သောညီ = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", 실제결과, re.S)
            assert 완료량.returncode == 0 and ဖြစ်သောညီ, (အမည်, 실제결과)
            ရလဒ် = next(အက္ခရာစဉ်ဒေတာ for အက္ခရာစဉ်ဒေတာ in ဖြစ်သောညီ.groups() if အက္ခရာစဉ်ဒေတာ is not None) + '\n'
            assert ရလဒ် == 예상결과, (အမည်, 예상결과, ရလဒ်)
            검증기록['tests'].append({'name': အမည်, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', အမည်, flush=True)
        # ကိုယ်ပိုင် JVM에 직접 연결한 မြန်မာ အလုပ်ကြိုးတန်ဖိုး/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(စီမံကိန်းအမြစ်/'ကိရိယာစု/ဖိုင်လုပ်ဆောင်.py'), str(အတန်းလမ်းကြောင်း/'မြန်မာအလုပ်ကြိုးစမ်းသပ်.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        ရလဒ် = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'မြန်မာအလုပ်ကြိုးစမ်းသပ်.log').write_text(ရလဒ်)
        assert 완료량.returncode == 0 and 'မြန်မာ 직접 အလုပ်ကြိုးတန်ဖိုး အောင်တန်ဖိုး\n' in ရလဒ် and '\nexit 0\n' in ရလဒ်, ရလဒ်
        검증기록['direct_korean_thread_and_entry'] = True
        print('PASS: မြန်မာ 직접 အလုပ်ကြိုးတန်ဖိုး·အလုပ်လုပ်ဆောင်·လုပ်ဆောင် အချက်အမှတ်တစ်ခု', flush=True)
        မှန်ကန် = (အတန်းလမ်းကြောင်း / 'အရာဝတ္ထုစမ်းသပ်.class').read_bytes()
        ကိစ္စစမ်းသပ် = [('판거부', မှန်ကန်[:6] + b'\x00\x35' + မှန်ကန်[8:], 'supported class versions'),
                 ('잘린클래스', မှန်ကန်[:24], 'truncated class file')]
        검증기록['rejection_tests'] = []
        for အမည်, 내용자료, 알림문 in ကိစ္စစမ်းသပ်:
            ဒေတာစမ်းသပ် = 출력결과 / (အမည် + '.class'); ဒေတာစမ်းသပ်.write_bytes(내용자료)
            완료량 = subprocess.run(['python3', str(စီမံကိန်းအမြစ် / 'ကိရိယာစု/ဖိုင်လုပ်ဆောင်.py'), str(ဒေတာစမ်းသပ်)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            စာသား = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (အမည် + '.log')).write_text(စာသား, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in စာသား and 'exit 1\n' in စာသား, (အမည်, စာသား)
            검증기록['rejection_tests'].append({'name': အမည်, 'passed': True})
            print('PASS (rejected):', အမည်, flush=True)
        검증기록['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(검증기록, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    လုပ်ဆောင်()
