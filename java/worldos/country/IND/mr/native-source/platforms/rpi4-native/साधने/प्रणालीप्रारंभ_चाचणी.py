#!/usr/bin/env python3
"""वास्तविक_डेटा raspi4b प्रणालीप्रारंभ, UART आदान_मूल्य, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ, आदेश


def सुरू_करा():
    प्रदान = प्रोजेक्ट_मूळ / 'build/verification'
    प्रदान.mkdir(parents=True, exist_ok=True)
    सत्रलेख = bytearray()
    पडताळणी_अहवाल = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as कार्यरत_पथ:
        क्यूएमयूनियंत्रण_पथ = Path(कार्यरत_पथ) / 'qmp.sock'
        आज्ञा_वितर्क = आदेश() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(क्यूएमयूनियंत्रण_पथ),
                           '-vnc', 'unix:{}'.format(Path(कार्यरत_पथ) / 'vnc.sock')]
        पडताळणी_अहवाल['command'] = आज्ञा_वितर्क
        प्रक्रिया = subprocess.Popen(आज्ञा_वितर्क, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        निवडक = selectors.DefaultSelector()
        निवडक.register(प्रक्रिया.stdout, selectors.EVENT_READ)
        def पर्यंत_स्वीकारा(खूण, ऑफसेट_मूल्य=0, निष्पादन_प्रतीक्षामर्यादा=45):
            अंतिमवेळ_वेळ = time.monotonic() + निष्पादन_प्रतीक्षामर्यादा
            while खूण not in सत्रलेख[ऑफसेट_मूल्य:]:
                if time.monotonic() > अंतिमवेळ_वेळ:
                    raise AssertionError('UART timeout: ' + repr(खूण))
                for दाबलेले_मूल्य, _ in निवडक.select(0.2):
                    डेटा_अवरोधित_करा = दाबलेले_मूल्य.fileobj.read(4096)
                    if डेटा_अवरोधित_करा:
                        सत्रलेख.extend(डेटा_अवरोधित_करा)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', सत्रलेख):
                    raise AssertionError('kernel failure')
                if प्रक्रिया.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(प्रक्रिया.returncode))
        try:
            पर्यंत_स्वीकारा(b'jkoros-native> ')
            खुणा = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for खूण in खुणा:
                assert खूण in सत्रलेख, खूण
            # GTK 없는 सध्याचे_आयटम 호스트에서도 VNC로 वास्तविक_डेटा GUI를 볼 संख्या 있어야 한다.
            with socket.socket(socket.AF_UNIX) as पडदा_क्लायंट:
                पडदा_क्लायंट.settimeout(5); पडदा_क्लायंट.connect(str(Path(कार्यरत_पथ) / 'vnc.sock'))
                def तंतोतंत_मूल्य(आकार):
                    मोजमाप = b''
                    while len(मोजमाप) < आकार:
                        तुकडा_मूल्य = पडदा_क्लायंट.recv(आकार - len(मोजमाप))
                        if not तुकडा_मूल्य: raise AssertionError('VNC disconnected')
                        मोजमाप += तुकडा_मूल्य
                    return मोजमाप
                assert तंतोतंत_मूल्य(12) == b'RFB 003.008\n'
                पडदा_क्लायंट.sendall(b'RFB 003.008\n')
                assert 1 in तंतोतंत_मूल्य(तंतोतंत_मूल्य(1)[0]); पडदा_क्लायंट.sendall(b'\x01')
                assert तंतोतंत_मूल्य(4) == b'\x00\x00\x00\x00'; पडदा_क्लायंट.sendall(b'\x01')
                सर्व्हर_मूल्य = तंतोतंत_मूल्य(24)
                assert int.from_bytes(सर्व्हर_मूल्य[:2], 'big') == 640 and int.from_bytes(सर्व्हर_मूल्य[2:4], 'big') == 480
                तंतोतंत_मूल्य(int.from_bytes(सर्व्हर_मूल्य[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for आज्ञा_बाइट, खूण in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'चाचण्या.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ऑफसेट_मूल्य = len(सत्रलेख)
                प्रक्रिया.stdin.write(आज्ञा_बाइट + b'\n')
                प्रक्रिया.stdin.flush()
                पर्यंत_स्वीकारा(b'jkoros-native> ', ऑफसेट_मूल्य)
                assert खूण in सत्रलेख[ऑफसेट_मूल्य:], खूण
            def शेल(ओळ, अपेक्षित):
                ऑफसेट_मूल्य = len(सत्रलेख)
                प्रक्रिया.stdin.write(ओळ.encode('utf-8') + b'\n'); प्रक्रिया.stdin.flush()
                पर्यंत_स्वीकारा(b'jkoros-native> ', ऑफसेट_मूल्य)
                प्रतिसाद = bytes(सत्रलेख[ऑफसेट_मूल्य:])
                for पाठ्य in अपेक्षित:
                    assert पाठ्य.encode('utf-8') in प्रतिसाद, (ओळ, पाठ्य, प्रतिसाद)
                return प्रतिसाद
            def प्रविष्ठ_करणे(ओळ, संकेत):
                ऑफसेट_मूल्य = len(सत्रलेख)
                प्रक्रिया.stdin.write(ओळ.encode('utf-8') + b'\n'); प्रक्रिया.stdin.flush()
                पर्यंत_स्वीकारा(संकेत, ऑफसेट_मूल्य)
                return bytes(सत्रलेख[ऑफसेट_मूल्य:])
            def संपादन_मूल्य(नाव, सामुग्री_मूल्य, रद्द_करा_क्रिया=False):
                प्रविष्ठ_करणे('edit ' + नाव, b'edit> ')
                for ओळ in सामुग्री_मूल्य.splitlines(): प्रविष्ठ_करणे(ओळ, b'edit> ')
                if रद्द_करा_क्रिया:
                    ऑफसेट_मूल्य = len(सत्रलेख)
                    प्रक्रिया.stdin.write(b'\x03'); प्रक्रिया.stdin.flush()
                    पर्यंत_स्वीकारा(b'jkoros-native> ', ऑफसेट_मूल्य)
                    assert b'EDIT CANCELLED' in सत्रलेख[ऑफसेट_मूल्य:]
                else:
                    assert b'SAVED' in प्रविष्ठ_करणे('.', b'jkoros-native> ')
            def अपलोड_करा_संचिका(नाव, डेटा):
                assert len(डेटा) <= 16384
                प्रविष्ठ_करणे('load ' + नाव, b'hex> ')
                for क्रमांक_अनुक्रमणिका in range(0, len(डेटा), 64): प्रविष्ठ_करणे(डेटा[क्रमांक_अनुक्रमणिका:क्रमांक_अनुक्रमणिका+64].hex(), b'hex> ')
                assert b'LOADED' in प्रविष्ठ_करणे('.', b'jkoros-native> ')
            def डाउनलोड(नाव):
                प्रतिसाद = शेल('hex ' + नाव, ['HEX BEGIN', 'HEX END'])
                आहे_समान = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', प्रतिसाद, re.S)
                डेटा = bytes.fromhex(''.join(आहे_समान.group(2).decode('ascii').split()))
                assert len(डेटा) == int(आहे_समान.group(1)); return डेटा
            शेल('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            शेल('java -version', ['not OpenJDK', 'exit 0'])
            शेल('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            शेल('java Hello "한글 बाबी 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 बाबी 😀', 'exit 0'])
            शेल('python --version', ['MicroPython 1.24.1', 'exit 0'])
            शेल('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 फाइल', 'exit 0'])
            शेल('cat python.txt', ['한글 फाइल'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            जावा_वर्ग = प्रदान / 'Hello.class'; जावा_वर्ग.write_bytes(डाउनलोड('Hello.class'))
            अपेक्षित = subprocess.check_output(['java', '-Xverify:all', '-cp', str(प्रदान), 'Hello', '한글 बाबी 😀']).decode('utf-8')
            assert अपेक्षित.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 बाबी 😀'], अपेक्षित
            संपादन_मूल्य('अभिवादन_ae353e94.java', 'public class अभिवादन_ae353e94 { public static void main(String[] args) { int मूल्य = 7; System.out.println("한글=" + मूल्य); } }')
            शेल('javac अभिवादन_ae353e94.java', ['Compiled: अभिवादन_ae353e94.class', 'exit 0'])
            शेल('java अभिवादन_ae353e94', ['한글=7', 'exit 0'])
            (प्रदान / 'अभिवादन_ae353e94.class').write_bytes(डाउनलोड('अभिवादन_ae353e94.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(प्रदान), 'अभिवादन_ae353e94']).decode().strip() == '한글=7'
            संपादन_मूल्य('Hello.java', 'broken', रद्द_करा_क्रिया=True)
            शेल('javac Hello.java', ['Compiled:', 'exit 0'])
            संपादन_मूल्य('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            शेल('javac Broken.java', ['javac error:', 'exit 1'])
            अपलोड_करा_संचिका('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            शेल('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            शेल('rm Broken.java', [])
            आयातित = प्रदान / 'Imported.java'
            आयातित.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(आयातित)])
            अपलोड_करा_संचिका('Imported.class', (प्रदान / 'Imported.class').read_bytes())
            शेल('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            शेल('rm Imported.class', [])
            संपादन_मूल्य('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            शेल('javac Loop.java', ['Compiled:', 'exit 0'])
            प्रतिसाद = शेल('java Loop', ['exit '])
            assert b'instruction limit' in प्रतिसाद or b'exit -1004' in प्रतिसाद
            शेल('rm Loop.java', []); शेल('rm Loop.class', [])
            # CPython-independent Python runtime: Unicode, big integers, closures/classes,
            # GC roots, file imports, exceptions and UDP queues are exercised in the guest.
            पायथन_पडताळण्या = """import gc, jkoros
assert len('한글😀') == 3
assert 2**100 == 1267650600228229401496703205376
class Counter:
    def __init__(self, n): self.n = n
    def value(self): return self.n + 1
keep = Counter(41)
for i in range(300):
    garbage = [str(j) for j in range(80)]
    gc.collect()
assert keep.value() == 42
try:
    1 // 0
except ZeroDivisionError:
    print('PY EXCEPTION OK')
a = jkoros.udp_open(9401)
b = jkoros.udp_open(9402)
assert jkoros.udp_send(a, 9402, b'udp-python') == 10
assert jkoros.udp_recv(b) == (b'udp-python', 9401)
try:
    jkoros.udp_recv(b)
except OSError as e:
    assert e.args[0] == 11
jkoros.udp_close(a)
jkoros.udp_close(b)
print('PY GC UNICODE MPZ CLASS UDP OK')
"""
            संपादन_मूल्य('checks.py', पायथन_पडताळण्या)
            शेल('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            शेल('rm checks.py', [])
            संपादन_मूल्य('helper.py', 'value = 321')
            शेल("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            शेल('rm helper.py', [])
            शेल("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            शेल("python -c 'while True: pass'", ['exit -1004'])
            for क्रमांक_अनुक्रमणिका in range(4):
                शेल('python hello.py', ['한글 फाइल', 'exit 0'])
                शेल('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            अपलोड_करा_संचिका('app.elf', (प्रोजेक्ट_मूळ / 'build/user/demo.elf').read_bytes())
            assert डाउनलोड('app.elf') == (प्रोजेक्ट_मूळ / 'build/user/demo.elf').read_bytes()
            शेल('run app.elf', ['EL0 C++', 'exit 0'])
            अपलोड_करा_संचिका('app.elf', b'not an ELF')
            शेल('run app.elf', ['exit -8'])
            शेल('rm app.elf', [])
            शेल('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            रेखांकन_पथ = प्रदान / 'java-framebuffer'; रेखांकन_पथ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(प्रोजेक्ट_मूळ / 'dist/jkoros-native-korean.jar'), '-d', str(रेखांकन_पथ), str(प्रोजेक्ट_मूळ / 'चाचण्या/जावा/पडदा_चाचणी.java')])
            अपलोड_करा_संचिका('पडदा_चाचणी.class', (रेखांकन_पथ / 'पडदा_चाचणी.class').read_bytes())
            शेल('java पडदा_चाचणी', ['पडदा क्लिप अस्वीकृत_करा_मूल्य', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            शेल('rm पडदा_चाचणी.class', [])
            with socket.socket(socket.AF_UNIX) as क्लायंट:
                क्लायंट.settimeout(10)
                क्लायंट.connect(str(क्यूएमयूनियंत्रण_पथ))
                with क्लायंट.makefile('rwb') as प्रवाह_मूल्य:
                    अभिवादन_ae353e94 = json.loads(प्रवाह_मूल्य.readline())
                    def अनुकृती_नियंत्रण_कनेक्शन(कार्यान्वित_करा, अग्रेषित_वितर्क=None):
                        संचारजाळे_संदेश = {'execute': कार्यान्वित_करा}
                        if अग्रेषित_वितर्क: संचारजाळे_संदेश['arguments'] = अग्रेषित_वितर्क
                        प्रवाह_मूल्य.write((json.dumps(संचारजाळे_संदेश) + '\n').encode())
                        प्रवाह_मूल्य.flush()
                        while True:
                            प्रत्युत्तर_द्या = json.loads(प्रवाह_मूल्य.readline())
                            if 'error' in प्रत्युत्तर_द्या: raise AssertionError(प्रत्युत्तर_द्या)
                            if 'return' in प्रत्युत्तर_द्या: return प्रत्युत्तर_द्या['return']
                    अनुकृती_नियंत्रण_कनेक्शन('qmp_capabilities')
                    स्क्रीन_क्लिपिंग = प्रदान / 'framebuffer.ppm'
                    अनुकृती_नियंत्रण_कनेक्शन('screendump', {'filename': str(स्क्रीन_क्लिपिंग), 'format': 'ppm'})
                    def उदाहरण_नोंदी(मार्ग, बिंदू):
                        with मार्ग.open('rb') as पिक्सेल_संचिका:
                            assert पिक्सेल_संचिका.readline().strip() == b'P6'
                            assert पिक्सेल_संचिका.readline().strip() == b'640 480'
                            assert पिक्सेल_संचिका.readline().strip() == b'255'
                            पिक्सेल_डेटा = पिक्सेल_संचिका.read()
                        assert len(पिक्सेल_डेटा) == 640 * 480 * 3
                        return [list(पिक्सेल_डेटा[(उभे_समन्वयीत * 640 + आडवे_समन्वयीत) * 3:(उभे_समन्वयीत * 640 + आडवे_समन्वयीत) * 3 + 3]) for आडवे_समन्वयीत, उभे_समन्वयीत in बिंदू]
                    assert उदाहरण_नोंदी(स्क्रीन_क्लिपिंग, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert उदाहरण_नोंदी(स्क्रीन_क्लिपिंग, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def पाठवा(दाबलेले_मूल्य, खूण):
                        ऑफसेट_मूल्य = len(सत्रलेख)
                        प्रक्रिया.stdin.write(दाबलेले_मूल्य); प्रक्रिया.stdin.flush()
                        पर्यंत_स्वीकारा(खूण, ऑफसेट_मूल्य)
                    पाठवा(b'gui\n', b'GUI READY:')
                    पहिले_चित्रसंवाद = प्रदान / 'gui-programs.ppm'
                    अनुकृती_नियंत्रण_कनेक्शन('screendump', {'filename': str(पहिले_चित्रसंवाद), 'format': 'ppm'})
                    अनुकृती_नियंत्रण_कनेक्शन('screendump', {'filename': str(प्रदान / 'gui-programs.png'), 'format': 'png'})
                    assert उदाहरण_नोंदी(पहिले_चित्रसंवाद, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    पाठवा(b'\r', b'GUI ACTION 0 RESULT 0')
                    पाठवा(b'\t', b'GUI FOCUS 1')
                    पाठवा(b'\r', b'GUI ACTION 1 RESULT 0')
                    दुसरे_चित्रसंवाद = प्रदान / 'gui-network.ppm'
                    अनुकृती_नियंत्रण_कनेक्शन('screendump', {'filename': str(दुसरे_चित्रसंवाद), 'format': 'ppm'})
                    अनुकृती_नियंत्रण_कनेक्शन('screendump', {'filename': str(प्रदान / 'gui-network.png'), 'format': 'png'})
                    assert उदाहरण_नोंदी(दुसरे_चित्रसंवाद, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    पाठवा(b'\t', b'GUI FOCUS 2')
                    पाठवा(b'\r', b'GUI ACTION 2 RESULT 0')
                    पाठवा(b'\t', b'GUI FOCUS 3')
                    पाठवा(b'\r', b'GUI ACTION 3 RESULT 0')
                    अनुकृती_नियंत्रण_कनेक्शन('screendump', {'filename': str(प्रदान / 'gui-python.png'), 'format': 'png'})
                    पाठवा(b'q', b'jkoros-native> ')
                    पडताळणी_अहवाल['qemu'] = अभिवादन_ae353e94['QMP']['version']
                    अनुकृती_नियंत्रण_कनेक्शन('quit')
            प्रक्रिया.wait(timeout=10)
            # framebuffer 응답뿐 아니라 वास्तविक_डेटा scanout 픽셀도 확인한다.
            with स्क्रीन_क्लिपिंग.open('rb') as संचिका_प्रविष्टी:
                assert संचिका_प्रविष्टी.readline().strip() == b'P6'
                परिमाणे_मूल्य = संचिका_प्रविष्टी.readline().strip()
                assert परिमाणे_मूल्य == b'640 480', परिमाणे_मूल्य
                assert संचिका_प्रविष्टी.readline().strip() == b'255'
                चित्रबिंदू_यादी = संचिका_प्रविष्टी.read()
            assert len(चित्रबिंदू_यादी) == 640 * 480 * 3
            def पिक्सेल(आडवे_समन्वयीत, उभे_समन्वयीत): return list(चित्रबिंदू_यादी[(उभे_समन्वयीत * 640 + आडवे_समन्वयीत) * 3:(उभे_समन्वयीत * 640 + आडवे_समन्वयीत) * 3 + 3])
            उदाहरण_नोंदी = {'background': पिक्सेल(5, 5), 'panel': पिक्सेल(45, 85), 'tile': पिक्सेल(65, 115)}
            assert उदाहरण_नोंदी == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, उदाहरण_नोंदी
            पडताळणी_अहवाल.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
                'UTF-8 Korean/Japanese/Arabic/emoji UART', 'C++ direct RAM file API (21 runs)',
                'cooperative independent stacks (4 runs)', 'line shell/UTF-8/quotes/edit/cancel/hex upload/download',
                'guest Java compiler/JVM and OpenJDK two-way class verification',
                'Korean Java framebuffer library bounds and actual scanout pixels',
                'Korean Java identifiers, UTF-8 validation, malformed source and bounded execution',
                'MicroPython GC/classes/Unicode/MPZ/imports/exceptions/files/UDP and timeout recovery',
                'load and run custom ELF with malformed image rejection', 'RGB32 framebuffer pixels',
                'ELF64 rejection fixtures: 22', 'EL0 C++ constructors/RAII/FP/files/heap/pointer validation',
                'kernel/text/MMIO/guard/NX/privileged instruction protection', 'timer terminates EL0 infinite loop',
                'repeated EL0 program exit closes leaked descriptors', 'UDP loopback payload/peer/reply/truncation/queue/zero datagram/errors/cleanup',
                'GUI focus/keyboard activation/C++/UDP/Java/MicroPython launch/exit and framebuffer pixels'],
                vnc='RFB 3.8 / 640x480 / UART input',
                framebuffer=उदाहरण_नोंदी, kernel_sha256=hashlib.sha256((प्रोजेक्ट_मूळ / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if प्रक्रिया.poll() is None:
                प्रक्रिया.terminate()
                try: प्रक्रिया.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    प्रक्रिया.kill(); प्रक्रिया.wait(timeout=5)
            निवडक.close()
            प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close()
            (प्रदान / 'serial.log').write_bytes(सत्रलेख)
            (प्रदान / 'report.json').write_text(json.dumps(पडताळणी_अहवाल, indent=2) + '\n')


if __name__ == '__main__':
    सुरू_करा()
