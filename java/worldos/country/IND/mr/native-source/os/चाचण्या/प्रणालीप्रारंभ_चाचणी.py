#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 अनुक्रमिक_मूल्य/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

जागा = Path(__file__).resolve().parents[1]


def प्रतीक्षाकरा(पडताळण्या, वर्णन, मर्यादा_मूल्य=15):
    शेवट = time.monotonic() + मर्यादा_मूल्य
    while time.monotonic() < शेवट:
        मोजमाप = पडताळण्या()
        if मोजमाप:
            return मोजमाप
        time.sleep(0.05)
    raise AssertionError('वेळ_मूल्य 초과: ' + वर्णन)


def चाचण्या(प्रकार_मूल्य):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as तात्पुरते_मूल्य:
        तात्पुरते_मूल्य = Path(तात्पुरते_मूल्य)
        अनुक्रमिक_पथ = तात्पुरते_मूल्य / 'serial.sock'
        मॉनिटर_पथ = तात्पुरते_मूल्य / 'monitor.sock'
        आदेश = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(अनुक्रमिक_पथ) + ',server,nowait',
                '-monitor', 'unix:' + str(मॉनिटर_पथ) + ',server,nowait']
        आदेश += ['-kernel', str(जागा / 'build/kernel.elf')] if प्रकार_मूल्य == 'elf' else [
            '-cdrom', str(जागा / 'build/kernel.iso'), '-boot', 'd']
        # अनुक्रमिक_मूल्य 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        आदेश += ['-S']
        प्रक्रिया_मूल्य = subprocess.Popen(आदेश, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        अनुक्रमिक_मूल्य = socket.socket(socket.AF_UNIX)
        मॉनिटर_मूल्य = socket.socket(socket.AF_UNIX)
        लॉग_नोंद = bytearray()
        try:
            def तयार_करणे_संचारद्वार():
                if प्रक्रिया_मूल्य.poll() is not None:
                    raise AssertionError(प्रक्रिया_मूल्य.stderr.read().decode('utf-8', 'replace'))
                return अनुक्रमिक_पथ.exists() and मॉनिटर_पथ.exists()
            प्रतीक्षाकरा(तयार_करणे_संचारद्वार, 'QEMU संचारद्वार_मूल्य')
            अनुक्रमिक_मूल्य.connect(str(अनुक्रमिक_पथ))
            मॉनिटर_मूल्य.connect(str(मॉनिटर_पथ))
            अनुक्रमिक_मूल्य.setblocking(False)
            मॉनिटर_मूल्य.sendall(b'cont\n')

            def घोषणाशीर्षे(स्ट्रींग_मूल्य, सुरू_करा=0):
                वाचन, _, _ = select.select([अनुक्रमिक_मूल्य], [], [], 0.1)
                if वाचन:
                    डेटा = अनुक्रमिक_मूल्य.recv(65536)
                    if not डेटा:
                        raise AssertionError('अनुक्रमिक_मूल्य जोडा निर्गमन_करा_अनुप्रयोग')
                    लॉग_नोंद.extend(डेटा)
                if प्रक्रिया_मूल्य.poll() is not None:
                    raise AssertionError('QEMU 비정상 निर्गमन_करा_अनुप्रयोग: ' + str(प्रक्रिया_मूल्य.returncode))
                return स्ट्रींग_मूल्य.encode('utf-8') in लॉग_नोंद[सुरू_करा:]

            def आदेश_चाचणी(आदान_मूल्य, अपेक्षा):
                सुरू_करा = len(लॉग_नोंद)
                अनुक्रमिक_मूल्य.sendall(आदान_मूल्य.encode('ascii'))
                प्रतीक्षाकरा(lambda: घोषणाशीर्षे(अपेक्षा, सुरू_करा), अपेक्षा)
                प्रतीक्षाकरा(lambda: घोषणाशीर्षे('jkoros> ', सुरू_करा), 'आदेश नंतर_राज्य 프롬프트')

            प्रतीक्षाकरा(lambda: घोषणाशीर्षे('READY'), प्रकार_मूल्य + ' प्रणालीप्रारंभ')
            assert b'JAVA SELFTEST PASS' in लॉग_नोंद
            assert 'जावा 기계어 गाभा_मूल्य सुरू_करा'.encode() in लॉग_नोंद
            आदेश_चाचणी('info\r\n', 'embedded subset JVM / polling kernel')
            आदेश_चाचणी('help\n', 'free N | echo TEXT')
            आदेश_चाचणी('mem\n', ' / 8 (각 4096바이트)')
            आदेश_चाचणी('echo natix\bve\n', 'native\r\n')
            for अनुक्रमणिका in range(8):
                आदेश_चाचणी('alloc\n', 'विभाग_मूल्य अनुक्रमणिका: ' + str(अनुक्रमणिका))
            आदेश_चाचणी('alloc\n', 'विभाग_मूल्य अनुक्रमणिका: -1')
            आदेश_चाचणी('free 3\n', '반환됨')
            आदेश_चाचणी('free 3\n', '할당되지 않은 विभाग_मूल्य')
            आदेश_चाचणी('free 99\n', '사용법: free 0..7')
            आदेश_चाचणी('alloc\n', 'विभाग_मूल्य अनुक्रमणिका: 3')
            आदेश_चाचणी('free 0\n', '반환됨')
            आदेश_चाचणी('test\n', 'JAVA SELFTEST PASS')
            आदेश_चाचणी('unknown\n', '알 संख्या 없는 명령입니다')
            आदेश_चाचणी('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            सुरू_करा = len(लॉग_नोंद)
            for कळ_मूल्य in ('i', 'n', 'f', 'o', 'ret'):
                मॉनिटर_मूल्य.sendall(('sendkey ' + कळ_मूल्य + ' 30\n').encode())
                time.sleep(0.09)
            प्रतीक्षाकरा(lambda: घोषणाशीर्षे('embedded subset JVM / polling kernel', सुरू_करा), 'PS/2 info आदान_मूल्य')
            आदेश_चाचणी('echo ' + 'a' * 150 + '\n', 'a' * 123)
            अनुक्रमिक_मूल्य.sendall(b'halt\n')
            प्रतीक्षाकरा(lambda: घोषणाशीर्षे('HALTED'), 'थांबवा_निष्पादन आदेश')
            assert b'PANIC' not in लॉग_नोंद and b'SELFTEST FAIL' not in लॉग_नोंद
            print('PASS: {} प्रणालीप्रारंभ, Java स्वकीय चाचण्या, अनुक्रमिक_मूल्य आदेश, PS/2 आदान_मूल्य, संग्रह_वाटप_करा/परतकरा_मोजमाप, थांबवा_निष्पादन'.format(प्रकार_मूल्य))
            return लॉग_नोंद.decode('utf-8', 'replace')
        finally:
            अनुक्रमिक_मूल्य.close()
            मॉनिटर_मूल्य.close()
            प्रक्रिया_मूल्य.terminate()
            try:
                प्रक्रिया_मूल्य.wait(timeout=3)
            except subprocess.TimeoutExpired:
                प्रक्रिया_मूल्य.kill()
                प्रक्रिया_मूल्य.wait()


if __name__ == '__main__':
    मोजमाप = {प्रकार_मूल्य: चाचण्या(प्रकार_मूल्य) for प्रकार_मूल्य in ('elf', 'iso')}
    (जागा / 'build/प्रणालीप्रारंभ_चाचणी.json').write_text(json.dumps(मोजमाप, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
