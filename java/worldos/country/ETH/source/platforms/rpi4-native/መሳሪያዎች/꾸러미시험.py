#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 자체 커널에서 검사한다."""
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
from 꾸러미중계 import ቀርቅብ_ማከማቻ, 압축풀기
from ፈጽም_ትእዛዝ import አሳይ_ስር


def 시험휠(ስም, 파일들, ስራ_እሴት_102996da='Root-Is-Purelib: true\n', 의존성=''):
    ውሂብ = io.BytesIO()
    with zipfile.ZipFile(ውሂብ, 'w', zipfile.ZIP_DEFLATED) as ቀርቅብ:
        ቀርቅብ.writestr(ስም + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + ስራ_እሴት_102996da)
        ቀርቅብ.writestr(ስም + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + ስም + '\nVersion: 1.0\n' + 의존성)
        for መተላለፊያ, ይዘት_እሴት in 파일들.items():
            ቀርቅብ.writestr(መተላለፊያ, ይዘት_እሴት)
    return ውሂብ.getvalue()


def ቼክ_አዘጋጅ():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'እሴት=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'እሴት=42\n'.encode()}
    for ውሂብ in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', ውሂብ, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel መተላለፊያ·መጠን·C ቅጥያ_እሴት·의존성 አትቀበል_እሴት')


def ባዶ_የወደብ_ቁጥር():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def ማስኬጃ():
    አግልሎ_ማስቀመጥ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--host-only', action='store_true')
    인수 = አግልሎ_ማስቀመጥ_48ee4b1b.parse_args()
    ቼክ_አዘጋጅ()
    if 인수.host_only:
        return
    ልኬት_ዱካ = አሳይ_ስር/'build/verification/pip'
    ልኬት_ዱካ.mkdir(parents=True, exist_ok=True)
    ማከማቻ_ዱካ_02e62bb7 = ልኬት_ዱካ/'cache'
    ማከማቻ_ዱካ_02e62bb7.mkdir(exist_ok=True)
    # ትክክለኛ_ውሂብ PyPI 배포 ፋይል. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    ቀርቅብ_ማከማቻ(አሳይ_ስር/'build/pip-cache').አዘጋጅ_9ce364fc('micropython-bisect==3.3.3')
    for ጭራ_እሴት in ('.archive', '.json'):
        shutil.copyfile(str(አሳይ_ስር/'build/pip-cache'/('micropython-bisect==3.3.3'+ጭራ_እሴት)), str(ማከማቻ_ዱካ_02e62bb7/('micropython-bisect==3.3.3'+ጭራ_እሴት)))
    실물기록 = json.loads((ማከማቻ_ዱካ_02e62bb7/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for ስም, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'እሴት=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ውሂብ = 시험휠(ስም, 파일들)
        (ማከማቻ_ዱካ_02e62bb7/(ስም+'==1.0.archive')).write_bytes(ውሂብ)
        (ማከማቻ_ዱካ_02e62bb7/(ስም+'==1.0.json')).write_text(json.dumps({'name': ስም, 'version': '1.0',
            'filename': ስም.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ውሂብ).hexdigest()}))
    ትክክለኛነት_አረጋግጥ = {'passed': False, 'kernel_sha256': hashlib.sha256((አሳይ_ስር/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    የወደብ_ቁጥር = ባዶ_የወደብ_ቁጥር()
    ሂደቶች = subprocess.Popen(['python3', str(አሳይ_ስር/'መሳሪያዎች/ፈጽም_ትእዛዝ.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(የወደብ_ቁጥር), '--pip-cache', str(ማከማቻ_ዱካ_02e62bb7), '--ftp-port', str(ባዶ_የወደብ_ቁጥር())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    መራጭ_a916db4e = selectors.DefaultSelector()
    መራጭ_a916db4e.register(ሂደቶች.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(አሳይ_እሴት=b'jkoros-native> '):
        ይዘት_እሴት = bytearray()
        끝 = time.monotonic()+120
        while አሳይ_እሴት not in ይዘት_እሴት:
            if time.monotonic() > 끝 or ሂደቶች.poll() is not None:
                raise AssertionError('게스트 መልስ 없음: '+ይዘት_እሴት.decode('utf-8','replace'))
            for ምዝግብ_እሴት, _ in መራጭ_a916db4e.select(.1):
                조각 = ምዝግብ_እሴት.fileobj.read(4096)
                ይዘት_እሴት.extend(조각)
                대화기록.extend(조각)
        return ይዘት_እሴት.decode('utf-8', 'replace').replace('\r\n','\n')
    def ሼል(ትእዛዝ, አሳይ_እሴት=b'jkoros-native> '):
        ሂደቶች.stdin.write(ትእዛዝ.encode()+b'\n')
        ሂደቶች.stdin.flush()
        return 기다리기(አሳይ_እሴት)
    def ፈጽም_ትእዛዝ(ትእዛዝ, 예상, ዞን_እሴት=0):
        ይዘት_እሴት = ሼል(ትእዛዝ)
        assert 예상 in ይዘት_እሴት and '\nexit '+str(ዞን_እሴት)+'\n' in ይዘት_እሴት, ይዘት_እሴት
        ትክክለኛነት_አረጋግጥ['checks'].append(ትእዛዝ)
        return ይዘት_እሴት
    def መጫን_ፋይሎች(ስም, ውሂብ):
        ሼል('load '+ስም, b'hex> ')
        for በቦታ_አስቀመጠ_መረጃ_ጠቆመ in range(0, len(ውሂብ), 64):
            ሼል(ውሂብ[በቦታ_አስቀመጠ_መረጃ_ጠቆመ:በቦታ_አስቀመጠ_መረጃ_ጠቆመ+64].hex(), b'hex> ')
        assert 'LOADED' in ሼል('.')
    try:
        기다리기()
        ፈጽም_ትእዛዝ('pip --help', 'MicroPython ምንጭ_ዛፍ 설치기')
        መጫን_ፋይሎች('오류시험.py', (አሳይ_ስር/'시험/파이썬/한국어오류시험.py').read_bytes())
        ፈጽም_ትእዛዝ('python 오류시험.py', 'አማርኛ ፋይል ልዩነት አረጋግጥ')
        ፈጽም_ትእዛዝ('pip install micropython-bisect==3.3.3 --port '+str(የወደብ_ቁጥር), 'ጫን_እሴት 완료: micropython-bisect 3.3.3')
        ፈጽም_ትእዛዝ('python -c \'from bisect import insort as 순서대로넣기; እሴት=[1,5]; 순서대로넣기(እሴት,3); print(እሴት)\'', '[1, 3, 5]')
        ፈጽም_ትእዛዝ('python -m pip list', 'micropython-bisect 3.3.3')
        ፈጽም_ትእዛዝ('pip install micropython-bisect==3.3.3 --port '+str(የወደብ_ቁጥር), '이미 설치됨:')
        ፈጽም_ትእዛዝ('pip install jkoros-fixture==1.0 --port '+str(የወደብ_ቁጥር), 'ጫን_እሴት 완료: jkoros-fixture')
        ፈጽም_ትእዛዝ('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        ፈጽም_ትእዛዝ('pip install jkoros-syntax==1.0 --port '+str(የወደብ_ቁጥር), 'ቀርቅብ ስህተት:', 1)
        ፈጽም_ትእዛዝ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ስህተት 보존")\'', '구문 ስህተት 보존')
        መጫን_ፋይሎች('공간시험.py', (አሳይ_ስር/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        ፈጽም_ትእዛዝ('python 공간시험.py '+str(የወደብ_ቁጥር), 'ቀርቅብ 공간 부족 되돌림 አረጋግጥ')
        ፈጽም_ትእዛዝ('pip uninstall jkoros-fixture', 'አስወግድ_ምዝግብ 완료: jkoros-fixture')
        ፈጽም_ትእዛዝ('pip uninstall micropython-bisect', 'አስወግድ_ምዝግብ 완료: micropython-bisect')
        ፈጽም_ትእዛዝ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("አስወግድ_ምዝግብ አረጋግጥ")\'', 'አስወግድ_ምዝግብ አረጋግጥ')
        ትክክለኛነት_አረጋግጥ['passed'] = True
        print('PASS: PyPI 실물 ጫን_እሴት·import·ፈጽም_ትእዛዝ, አማርኛ ልዩነት, 패키지 ማውጫ_እሴት, ተስኖት_እሴት 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 ውጣ_ፕሮግራም 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            ሂደቶች.stdin.write(b'\x01x')
            ሂደቶች.stdin.flush()
            ሂደቶች.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            ሂደቶች.terminate()
            try:
                ሂደቶች.wait(timeout=8)
            except subprocess.TimeoutExpired:
                ሂደቶች.kill()
                ሂደቶች.wait()
        if ሂደቶች.poll() is None:
            ሂደቶች.kill()
            ሂደቶች.wait()
        መራጭ_a916db4e.close()
        ሂደቶች.stdin.close()
        ሂደቶች.stdout.close()
        (ልኬት_ዱካ/'serial.log').write_bytes(대화기록)
        (ልኬት_ዱካ/'report.json').write_text(json.dumps(ትክክለኛነት_አረጋግጥ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ማስኬጃ()
