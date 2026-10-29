#!/usr/bin/env python3
"""PyPI भौतिक_हार्डवेअर 배포와 부정 आदान_मूल्य·RAM 되돌림을 स्वकीय 커널에서 검사한다."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import selectors
import shutil
import socket
import subprocess
import time
import zipfile
from बंडल_संदेशमध्यस्थ import बंडल_भांडार, विसंपीडनकरा
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ


def व्हील_चाचणी(नाव, संचिका_नोंदी, काम_मूल्य='Root-Is-Purelib: true\n', अवलंबने=''):
    डेटा = io.BytesIO()
    with zipfile.ZipFile(डेटा, 'w', zipfile.ZIP_DEFLATED) as बंडल:
        बंडल.writestr(नाव + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + काम_मूल्य)
        बंडल.writestr(नाव + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + नाव + '\nVersion: 1.0\n' + अवलंबने)
        for मार्ग, सामुग्री_मूल्य in संचिका_नोंदी.items():
            बंडल.writestr(मार्ग, सामुग्री_मूल्य)
    return डेटा.getvalue()


def होस्ट_तपासा():
    आहे_सामान्य = व्हील_चाचणी('jkoros-fixture', {'mod.py': 'मूल्य=42\n'})
    assert विसंपीडनकरा('jkoros_fixture-1.0-py3-none-any.whl', आहे_सामान्य, 'jkoros-fixture', '1.0') == {'mod.py': 'मूल्य=42\n'.encode()}
    for डेटा in (
            व्हील_चाचणी('jkoros-fixture', {'../escape.py': ''}),
            व्हील_चाचणी('jkoros-fixture', {'/abs.py': ''}),
            व्हील_चाचणी('jkoros-fixture', {'big.py': 'x' * 16385}),
            व्हील_चाचणी('jkoros-fixture', {'mod.so': ''}),
            व्हील_चाचणी('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            व्हील_चाचणी('jkoros-fixture', {'mod.py': ''}, अवलंबने='Requires-Dist: requests\n')):
        try:
            विसंपीडनकरा('jkoros_fixture-1.0-py3-none-any.whl', डेटा, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel मार्ग·आकार·C एक्सटेंशन_मूल्य·अवलंबने अस्वीकृत_करा_मूल्य')


def रिक्त_पोर्ट_नंबर():
    with socket.socket() as संचारद्वार_मूल्य:
        संचारद्वार_मूल्य.bind(('127.0.0.1', 0))
        return संचारद्वार_मूल्य.getsockname()[1]


def सुरू_करा():
    व्याकरणविश्लेषक_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    व्याकरणविश्लेषक_48ee4b1b.add_argument('--host-only', action='store_true')
    बाबी = व्याकरणविश्लेषक_48ee4b1b.parse_args()
    होस्ट_तपासा()
    if बाबी.host_only:
        return
    मोजमाप_पथ = प्रोजेक्ट_मूळ/'build/verification/pip'
    मोजमाप_पथ.mkdir(parents=True, exist_ok=True)
    संग्रह_पथ = मोजमाप_पथ/'cache'
    संग्रह_पथ.mkdir(exist_ok=True)
    # वास्तविक_डेटा PyPI वितरण_मूल्य फाइल. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    बंडल_भांडार(प्रोजेक्ट_मूळ/'build/pip-cache').तयार_करणे('micropython-bisect==3.3.3')
    for टेल_मूल्य in ('.archive', '.json'):
        shutil.copyfile(str(प्रोजेक्ट_मूळ/'build/pip-cache'/('micropython-bisect==3.3.3'+टेल_मूल्य)), str(संग्रह_पथ/('micropython-bisect==3.3.3'+टेल_मूल्य)))
    हार्डवेअर_लॉग = json.loads((संग्रह_पथ/'micropython-bisect==3.3.3.json').read_text())
    assert हार्डवेअर_लॉग['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for नाव, संचिका_नोंदी in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .गणना import जोडा_मूल्ये\n', '검증꾸러미/गणना.py': 'def जोडा_मूल्ये(पहिले_संकार्य,दुसरे_संकार्य):\n return पहिले_संकार्य+दुसरे_संकार्य\n'}),
            ('jkoros-space', {'space%d.py' % संख्या: 'मूल्य=1\n' for संख्या in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        डेटा = व्हील_चाचणी(नाव, संचिका_नोंदी)
        (संग्रह_पथ/(नाव+'==1.0.archive')).write_bytes(डेटा)
        (संग्रह_पथ/(नाव+'==1.0.json')).write_text(json.dumps({'name': नाव, 'version': '1.0',
            'filename': नाव.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(डेटा).hexdigest()}))
    प्रमाणित = {'passed': False, 'kernel_sha256': hashlib.sha256((प्रोजेक्ट_मूळ/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': हार्डवेअर_लॉग, 'checks': []}
    पोर्ट_नंबर = रिक्त_पोर्ट_नंबर()
    प्रक्रिया = subprocess.Popen(['python3', str(प्रोजेक्ट_मूळ/'साधने/आज्ञा_कार्यवाही_करा.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(पोर्ट_नंबर), '--pip-cache', str(संग्रह_पथ), '--ftp-port', str(रिक्त_पोर्ट_नंबर())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    निवडक_a916db4e = selectors.DefaultSelector()
    निवडक_a916db4e.register(प्रक्रिया.stdout, selectors.EVENT_READ)
    सत्रलेख = bytearray()
    def प्रतीक्षाकरा(मूल्य_शो=b'jkoros-native> '):
        सामुग्री_मूल्य = bytearray()
        शेवट = time.monotonic()+120
        while मूल्य_शो not in सामुग्री_मूल्य:
            if time.monotonic() > शेवट or प्रक्रिया.poll() is not None:
                raise AssertionError('게스트 प्रत्युत्तर_द्या अनुपस्थित_पद्धत: '+सामुग्री_मूल्य.decode('utf-8','replace'))
            for प्रविष्टी_मूल्य, _ in निवडक_a916db4e.select(.1):
                तुकडा_मूल्य = प्रविष्टी_मूल्य.fileobj.read(4096)
                सामुग्री_मूल्य.extend(तुकडा_मूल्य)
                सत्रलेख.extend(तुकडा_मूल्य)
        return सामुग्री_मूल्य.decode('utf-8', 'replace').replace('\r\n','\n')
    def शेल(आदेश, मूल्य_शो=b'jkoros-native> '):
        प्रक्रिया.stdin.write(आदेश.encode()+b'\n')
        प्रक्रिया.stdin.flush()
        return प्रतीक्षाकरा(मूल्य_शो)
    def आज्ञा_कार्यवाही_करा(आदेश, अपेक्षित_मूल्ये, राज्य_मूल्य=0):
        सामुग्री_मूल्य = शेल(आदेश)
        assert अपेक्षित_मूल्ये in सामुग्री_मूल्य and '\nexit '+str(राज्य_मूल्य)+'\n' in सामुग्री_मूल्य, सामुग्री_मूल्य
        प्रमाणित['checks'].append(आदेश)
        return सामुग्री_मूल्य
    def अपलोड_करा_संचिका(नाव, डेटा):
        शेल('load '+नाव, b'hex> ')
        for स्थान_अनुक्रमणिका in range(0, len(डेटा), 64):
            शेल(डेटा[स्थान_अनुक्रमणिका:स्थान_अनुक्रमणिका+64].hex(), b'hex> ')
        assert 'LOADED' in शेल('.')
    try:
        प्रतीक्षाकरा()
        आज्ञा_कार्यवाही_करा('pip --help', 'MicroPython स्रोत_ट्री 설치기')
        अपलोड_करा_संचिका('오류시험.py', (प्रोजेक्ट_मूळ/'चाचण्या/पायथन/कोरियन_त्रुटी_चाचणी.py').read_bytes())
        आज्ञा_कार्यवाही_करा('python 오류시험.py', 'मराठी फाइल अपवाद पडताळा')
        आज्ञा_कार्यवाही_करा('pip install micropython-bisect==3.3.3 --port '+str(पोर्ट_नंबर), 'स्थापित_करा_मूल्य आहे_पूर्ण: micropython-bisect 3.3.3')
        आज्ञा_कार्यवाही_करा('python -c \'from bisect import insort as 순서대로넣기; मूल्य=[1,5]; 순서대로넣기(मूल्य,3); print(मूल्य)\'', '[1, 3, 5]')
        आज्ञा_कार्यवाही_करा('python -m pip list', 'micropython-bisect 3.3.3')
        आज्ञा_कार्यवाही_करा('pip install micropython-bisect==3.3.3 --port '+str(पोर्ट_नंबर), '이미 설치됨:')
        आज्ञा_कार्यवाही_करा('pip install jkoros-fixture==1.0 --port '+str(पोर्ट_नंबर), 'स्थापित_करा_मूल्य आहे_पूर्ण: jkoros-fixture')
        आज्ञा_कार्यवाही_करा('python -c \'from 검증꾸러미 import जोडा_मूल्ये; print(जोडा_मूल्ये(20,22))\'', '\n42\n')
        आज्ञा_कार्यवाही_करा('pip install jkoros-syntax==1.0 --port '+str(पोर्ट_नंबर), 'बंडल त्रुटी:', 1)
        आज्ञा_कार्यवाही_करा('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 त्रुटी 보존")\'', '구문 त्रुटी 보존')
        अपलोड_करा_संचिका('공간시험.py', (प्रोजेक्ट_मूळ/'चाचण्या/पायथन/बंडल_नामक्षेत्र_चाचणी.py').read_bytes())
        आज्ञा_कार्यवाही_करा('python 공간시험.py '+str(पोर्ट_नंबर), 'बंडल पत्ता_प्रदेश 부족 परतकरा_ब्रिज पडताळा')
        आज्ञा_कार्यवाही_करा('pip uninstall jkoros-fixture', 'प्रविष्टी_काढणे आहे_पूर्ण: jkoros-fixture')
        आज्ञा_कार्यवाही_करा('pip uninstall micropython-bisect', 'प्रविष्टी_काढणे आहे_पूर्ण: micropython-bisect')
        आज्ञा_कार्यवाही_करा('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("प्रविष्टी_काढणे पडताळा")\'', 'प्रविष्टी_काढणे पडताळा')
        प्रमाणित['passed'] = True
        print('PASS: PyPI भौतिक_हार्डवेअर स्थापित_करा_मूल्य·import·आज्ञा_कार्यवाही_करा, मराठी अपवाद, 패키지 निर्देशिका_मूल्य, बिघाड_मूल्य परतकरा_ब्रिज, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 निर्गमन_करा_अनुप्रयोग 키로 QEMU를 끝내면 실행기의 संदेशमध्यस्थ_मूल्य 문맥도 정리된다.
            प्रक्रिया.stdin.write(b'\x01x')
            प्रक्रिया.stdin.flush()
            प्रक्रिया.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            प्रक्रिया.terminate()
            try:
                प्रक्रिया.wait(timeout=8)
            except subprocess.TimeoutExpired:
                प्रक्रिया.kill()
                प्रक्रिया.wait()
        if प्रक्रिया.poll() is None:
            प्रक्रिया.kill()
            प्रक्रिया.wait()
        निवडक_a916db4e.close()
        प्रक्रिया.stdin.close()
        प्रक्रिया.stdout.close()
        (मोजमाप_पथ/'serial.log').write_bytes(सत्रलेख)
        (मोजमाप_पथ/'report.json').write_text(json.dumps(प्रमाणित, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    सुरू_करा()
