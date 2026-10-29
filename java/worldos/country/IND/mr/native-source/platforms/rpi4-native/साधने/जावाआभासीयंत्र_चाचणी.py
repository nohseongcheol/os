#!/usr/bin/env python3
"""OpenJDK와 स्वकीय ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ


def सुरू_करा():
    प्रदान = प्रोजेक्ट_मूळ / 'build/verification/jvm'
    वर्ग_पथ = प्रदान / 'classes'; वर्ग_पथ.mkdir(parents=True, exist_ok=True)
    जावा_बंडल = प्रोजेक्ट_मूळ / 'dist/jkoros-native-korean.jar'
    स्रोतसूची = sorted((प्रोजेक्ट_मूळ / 'चाचण्या/जावा').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(जावा_बंडल), '-d', str(वर्ग_पथ)] + [str(स्ट्रींग_डेटा) for स्ट्रींग_डेटा in स्रोतसूची])
    यादी_चाचणी = [('वस्तू_चाचणी', ['वॉलपेपर_मूल्य', 'शाखा_मूल्य', 'शक्य_गणनाकरा']), ('अपवाद_चाचणी', []), ('संकलन_चाचणी', []),
             ('कार्यसूत्रे_चाचणी', ['काउंटर_मूल्य', 'कार्य_क्रिया', 'कार्यसूत्र_मूल्य_5b72a632']), ('हांगुल_चाचणी', []), ('संचारजाळे_चाचणी', []), ('कोरियन_संचारजाळे_चाचणी', []), ('कोरियन_अपवाद_चाचणी', []), ('हांगुल_स्रोत', []), ('सीमा_चाचणी', []), ('प्रमाणित.बंडल_चाचणी', []), ('प्रविष्टी_सुसंगती_चाचणी', [])]
    पडताळणी_अहवाल = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((प्रोजेक्ट_मूळ / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(जावा_बंडल.read_bytes()).hexdigest(), 'tests': []}
    try:
        for नाव, समावेश in यादी_चाचणी:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as तात्पुरते_पथ:
                अपेक्षित = subprocess.check_output(['java', '-Xverify:all', '-cp', str(वर्ग_पथ) + ':' + str(जावा_बंडल), नाव], cwd=तात्पुरते_पथ, timeout=15).decode('utf-8')
            आज्ञा_वितर्क = ['python3', str(प्रोजेक्ट_मूळ / 'साधने/संचिका_कार्यवाही_करा.py'), str(वर्ग_पथ / (नाव.replace('.', '/') + '.class'))]
            if '.' in नाव: आज्ञा_वितर्क += ['--class-name', नाव]
            for समाविष्टकरा in समावेश: आज्ञा_वितर्क += ['--include', str(वर्ग_पथ / (समाविष्टकरा + '.class'))]
            if नाव == 'हांगुल_स्रोत': आज्ञा_वितर्क[2] = str(प्रोजेक्ट_मूळ / 'चाचण्या/जावा/हांगुल_स्रोत.java')
            पूर्णझालेले_रक्कम = subprocess.run(आज्ञा_वितर्क, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            वास्तविक_मोजमाप = पूर्णझालेले_रक्कम.stdout.decode('utf-8').replace('\r\n', '\n')
            (प्रदान / (नाव + '.log')).write_text(वास्तविक_मोजमाप, encoding='utf-8')
            आहे_समान = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", वास्तविक_मोजमाप, re.S)
            assert पूर्णझालेले_रक्कम.returncode == 0 and आहे_समान, (नाव, वास्तविक_मोजमाप)
            मोजमाप = next(स्ट्रींग_डेटा for स्ट्रींग_डेटा in आहे_समान.groups() if स्ट्रींग_डेटा is not None) + '\n'
            assert मोजमाप == अपेक्षित, (नाव, अपेक्षित, मोजमाप)
            पडताळणी_अहवाल['tests'].append({'name': नाव, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', नाव, flush=True)
        # स्वकीय JVM에 직접 연결한 मराठी कार्यसूत्र_मूल्य_5b72a632/진입점은 OpenJDK용 래퍼가 아니다.
        पूर्णझालेले_रक्कम = subprocess.run(['python3', str(प्रोजेक्ट_मूळ/'साधने/संचिका_कार्यवाही_करा.py'), str(वर्ग_पथ/'कोरियन_कार्यसूत्रे_चाचणी.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        मोजमाप = पूर्णझालेले_रक्कम.stdout.decode('utf-8').replace('\r\n', '\n')
        (प्रदान/'कोरियन_कार्यसूत्रे_चाचणी.log').write_text(मोजमाप)
        assert पूर्णझालेले_रक्कम.returncode == 0 and 'मराठी 직접 कार्यसूत्र_मूल्य_5b72a632 उत्तीर्ण_मूल्य\n' in मोजमाप and '\nexit 0\n' in मोजमाप, मोजमाप
        पडताळणी_अहवाल['direct_korean_thread_and_entry'] = True
        print('PASS: मराठी 직접 कार्यसूत्र_मूल्य_5b72a632·कार्यान्वित_करा·सुरू_करा प्रविष्टी_गुण', flush=True)
        वैध = (वर्ग_पथ / 'वस्तू_चाचणी.class').read_bytes()
        काम_चाचणी = [('판거부', वैध[:6] + b'\x00\x35' + वैध[8:], 'supported class versions'),
                 ('잘린클래스', वैध[:24], 'truncated class file')]
        पडताळणी_अहवाल['rejection_tests'] = []
        for नाव, पेलोड_डेटा, सूचना_मजकूर in काम_चाचणी:
            डेटा_चाचणी = प्रदान / (नाव + '.class'); डेटा_चाचणी.write_bytes(पेलोड_डेटा)
            पूर्णझालेले_रक्कम = subprocess.run(['python3', str(प्रोजेक्ट_मूळ / 'साधने/संचिका_कार्यवाही_करा.py'), str(डेटा_चाचणी)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            पाठ्य = पूर्णझालेले_रक्कम.stdout.decode('utf-8').replace('\r\n', '\n')
            (प्रदान / (नाव + '.log')).write_text(पाठ्य, encoding='utf-8')
            assert पूर्णझालेले_रक्कम.returncode == 1 and सूचना_मजकूर in पाठ्य and 'exit 1\n' in पाठ्य, (नाव, पाठ्य)
            पडताळणी_अहवाल['rejection_tests'].append({'name': नाव, 'passed': True})
            print('PASS (rejected):', नाव, flush=True)
        पडताळणी_अहवाल['passed'] = True
    finally:
        (प्रदान / 'report.json').write_text(json.dumps(पडताळणी_अहवाल, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    सुरू_करा()
