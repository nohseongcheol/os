#!/usr/bin/env python3
"""actualData raspi4b machine_boot, UART inputValue, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from executeCommand import projectRoot, command


def run():
    output = projectRoot / 'build/verification'
    output.mkdir(parents=True, exist_ok=True)
    transcript = bytearray()
    validationReport = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as workingPath:
        qmpPath = Path(workingPath) / 'qmp.sock'
        commandArguments = command() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(qmpPath),
                           '-vnc', 'unix:{}'.format(Path(workingPath) / 'vnc.sock')]
        validationReport['command'] = commandArguments
        process = subprocess.Popen(commandArguments, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)
        def receiveUntil(marker, offsetValue=0, executionTimeout=45):
            deadlineTime = time.monotonic() + executionTimeout
            while marker not in transcript[offsetValue:]:
                if time.monotonic() > deadlineTime:
                    raise AssertionError('UART timeout: ' + repr(marker))
                for pressedValue, _ in selector.select(0.2):
                    dataBlock = pressedValue.fileobj.read(4096)
                    if dataBlock:
                        transcript.extend(dataBlock)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', transcript):
                    raise AssertionError('kernel failure')
                if process.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(process.returncode))
        try:
            receiveUntil(b'jkoros-native> ')
            markers = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for marker in markers:
                assert marker in transcript, marker
            # GTK 없는 currentItem 호스트에서도 VNC로 actualData GUI를 볼 number 있어야 한다.
            with socket.socket(socket.AF_UNIX) as screenClient:
                screenClient.settimeout(5); screenClient.connect(str(Path(workingPath) / 'vnc.sock'))
                def exactValue(size):
                    result = b''
                    while len(result) < size:
                        fragmentValue = screenClient.recv(size - len(result))
                        if not fragmentValue: raise AssertionError('VNC disconnected')
                        result += fragmentValue
                    return result
                assert exactValue(12) == b'RFB 003.008\n'
                screenClient.sendall(b'RFB 003.008\n')
                assert 1 in exactValue(exactValue(1)[0]); screenClient.sendall(b'\x01')
                assert exactValue(4) == b'\x00\x00\x00\x00'; screenClient.sendall(b'\x01')
                serverValue = exactValue(24)
                assert int.from_bytes(serverValue[:2], 'big') == 640 and int.from_bytes(serverValue[2:4], 'big') == 480
                exactValue(int.from_bytes(serverValue[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for commandByte, marker in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'tests.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                offsetValue = len(transcript)
                process.stdin.write(commandByte + b'\n')
                process.stdin.flush()
                receiveUntil(b'jkoros-native> ', offsetValue)
                assert marker in transcript[offsetValue:], marker
            def shell(line, expected):
                offsetValue = len(transcript)
                process.stdin.write(line.encode('utf-8') + b'\n'); process.stdin.flush()
                receiveUntil(b'jkoros-native> ', offsetValue)
                response = bytes(transcript[offsetValue:])
                for text in expected:
                    assert text.encode('utf-8') in response, (line, text, response)
                return response
            def enter(line, prompt):
                offsetValue = len(transcript)
                process.stdin.write(line.encode('utf-8') + b'\n'); process.stdin.flush()
                receiveUntil(prompt, offsetValue)
                return bytes(transcript[offsetValue:])
            def editValue(name, contentValue, cancelOperation=False):
                enter('edit ' + name, b'edit> ')
                for line in contentValue.splitlines(): enter(line, b'edit> ')
                if cancelOperation:
                    offsetValue = len(transcript)
                    process.stdin.write(b'\x03'); process.stdin.flush()
                    receiveUntil(b'jkoros-native> ', offsetValue)
                    assert b'EDIT CANCELLED' in transcript[offsetValue:]
                else:
                    assert b'SAVED' in enter('.', b'jkoros-native> ')
            def uploadFiles(name, data):
                assert len(data) <= 16384
                enter('load ' + name, b'hex> ')
                for ordinalIndex in range(0, len(data), 64): enter(data[ordinalIndex:ordinalIndex+64].hex(), b'hex> ')
                assert b'LOADED' in enter('.', b'jkoros-native> ')
            def download(name):
                response = shell('hex ' + name, ['HEX BEGIN', 'HEX END'])
                isEqual = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', response, re.S)
                data = bytes.fromhex(''.join(isEqual.group(2).decode('ascii').split()))
                assert len(data) == int(isEqual.group(1)); return data
            shell('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            shell('java -version', ['not OpenJDK', 'exit 0'])
            shell('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            shell('java Hello "hangulText arguments 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', 'hangulText arguments 😀', 'exit 0'])
            shell('python --version', ['MicroPython 1.24.1', 'exit 0'])
            shell('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', 'hangulText file', 'exit 0'])
            shell('cat python.txt', ['hangulText file'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            javaClass = output / 'Hello.class'; javaClass.write_bytes(download('Hello.class'))
            expected = subprocess.check_output(['java', '-Xverify:all', '-cp', str(output), 'Hello', 'hangulText arguments 😀']).decode('utf-8')
            assert expected.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', 'hangulText arguments 😀'], expected
            editValue('Greeting.java', 'public class Greeting { public static void main(String[] args) { int value = 7; System.out.println("hangulText=" + value); } }')
            shell('javac Greeting.java', ['Compiled: Greeting.class', 'exit 0'])
            shell('java Greeting', ['hangulText=7', 'exit 0'])
            (output / 'Greeting.class').write_bytes(download('Greeting.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(output), 'Greeting']).decode().strip() == 'hangulText=7'
            editValue('Hello.java', 'broken', cancelOperation=True)
            shell('javac Hello.java', ['Compiled:', 'exit 0'])
            editValue('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            shell('javac Broken.java', ['javac error:', 'exit 1'])
            uploadFiles('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            shell('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            shell('rm Broken.java', [])
            imported = output / 'Imported.java'
            imported.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS hangulText 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(imported)])
            uploadFiles('Imported.class', (output / 'Imported.class').read_bytes())
            shell('java Imported', ['HOST CLASS hangulText 😀', '81', 'exit 0'])
            shell('rm Imported.class', [])
            editValue('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            shell('javac Loop.java', ['Compiled:', 'exit 0'])
            response = shell('java Loop', ['exit '])
            assert b'instruction limit' in response or b'exit -1004' in response
            shell('rm Loop.java', []); shell('rm Loop.class', [])
            # CPython-independent Python runtime: Unicode, big integers, closures/classes,
            # GC roots, file imports, exceptions and UDP queues are exercised in the guest.
            pythonChecks = """import gc, jkoros
assert len('hangulText😀') == 3
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
            editValue('checks.py', pythonChecks)
            shell('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            shell('rm checks.py', [])
            editValue('helper.py', 'value = 321')
            shell("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            shell('rm helper.py', [])
            shell("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            shell("python -c 'while True: pass'", ['exit -1004'])
            for ordinalIndex in range(4):
                shell('python hello.py', ['hangulText file', 'exit 0'])
                shell('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            uploadFiles('app.elf', (projectRoot / 'build/user/demo.elf').read_bytes())
            assert download('app.elf') == (projectRoot / 'build/user/demo.elf').read_bytes()
            shell('run app.elf', ['EL0 C++', 'exit 0'])
            uploadFiles('app.elf', b'not an ELF')
            shell('run app.elf', ['exit -8'])
            shell('rm app.elf', [])
            shell('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            drawingPath = output / 'java-framebuffer'; drawingPath.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(projectRoot / 'dist/jkoros-native-korean.jar'), '-d', str(drawingPath), str(projectRoot / 'tests/Java/testScreen.java')])
            uploadFiles('testScreen.class', (drawingPath / 'testScreen.class').read_bytes())
            shell('java testScreen', ['Screen clip rejectValue', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            shell('rm testScreen.class', [])
            with socket.socket(socket.AF_UNIX) as client:
                client.settimeout(10)
                client.connect(str(qmpPath))
                with client.makefile('rwb') as streamValue:
                    Greeting = json.loads(streamValue.readline())
                    def mockControlConnection(executeTask, forwardedArgument=None):
                        networkMessage = {'execute': executeTask}
                        if forwardedArgument: networkMessage['arguments'] = forwardedArgument
                        streamValue.write((json.dumps(networkMessage) + '\n').encode())
                        streamValue.flush()
                        while True:
                            reply = json.loads(streamValue.readline())
                            if 'error' in reply: raise AssertionError(reply)
                            if 'return' in reply: return reply['return']
                    mockControlConnection('qmp_capabilities')
                    screenshot = output / 'framebuffer.ppm'
                    mockControlConnection('screendump', {'filename': str(screenshot), 'format': 'ppm'})
                    def exampleEntries(path, points):
                        with path.open('rb') as pixelFile:
                            assert pixelFile.readline().strip() == b'P6'
                            assert pixelFile.readline().strip() == b'640 480'
                            assert pixelFile.readline().strip() == b'255'
                            pixelData = pixelFile.read()
                        assert len(pixelData) == 640 * 480 * 3
                        return [list(pixelData[(yCoordinate * 640 + xCoordinate) * 3:(yCoordinate * 640 + xCoordinate) * 3 + 3]) for xCoordinate, yCoordinate in points]
                    assert exampleEntries(screenshot, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert exampleEntries(screenshot, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def send(pressedValue, marker):
                        offsetValue = len(transcript)
                        process.stdin.write(pressedValue); process.stdin.flush()
                        receiveUntil(marker, offsetValue)
                    send(b'gui\n', b'GUI READY:')
                    firstGui = output / 'gui-programs.ppm'
                    mockControlConnection('screendump', {'filename': str(firstGui), 'format': 'ppm'})
                    mockControlConnection('screendump', {'filename': str(output / 'gui-programs.png'), 'format': 'png'})
                    assert exampleEntries(firstGui, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    send(b'\r', b'GUI ACTION 0 RESULT 0')
                    send(b'\t', b'GUI FOCUS 1')
                    send(b'\r', b'GUI ACTION 1 RESULT 0')
                    secondGui = output / 'gui-network.ppm'
                    mockControlConnection('screendump', {'filename': str(secondGui), 'format': 'ppm'})
                    mockControlConnection('screendump', {'filename': str(output / 'gui-network.png'), 'format': 'png'})
                    assert exampleEntries(secondGui, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    send(b'\t', b'GUI FOCUS 2')
                    send(b'\r', b'GUI ACTION 2 RESULT 0')
                    send(b'\t', b'GUI FOCUS 3')
                    send(b'\r', b'GUI ACTION 3 RESULT 0')
                    mockControlConnection('screendump', {'filename': str(output / 'gui-python.png'), 'format': 'png'})
                    send(b'q', b'jkoros-native> ')
                    validationReport['qemu'] = Greeting['QMP']['version']
                    mockControlConnection('quit')
            process.wait(timeout=10)
            # framebuffer 응답뿐 아니라 actualData scanout 픽셀도 확인한다.
            with screenshot.open('rb') as fileEntry:
                assert fileEntry.readline().strip() == b'P6'
                dimensionsValue = fileEntry.readline().strip()
                assert dimensionsValue == b'640 480', dimensionsValue
                assert fileEntry.readline().strip() == b'255'
                pixelsList = fileEntry.read()
            assert len(pixelsList) == 640 * 480 * 3
            def pixel(xCoordinate, yCoordinate): return list(pixelsList[(yCoordinate * 640 + xCoordinate) * 3:(yCoordinate * 640 + xCoordinate) * 3 + 3])
            exampleEntries = {'background': pixel(5, 5), 'panel': pixel(45, 85), 'tile': pixel(65, 115)}
            assert exampleEntries == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, exampleEntries
            validationReport.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=exampleEntries, kernel_sha256=hashlib.sha256((projectRoot / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if process.poll() is None:
                process.terminate()
                try: process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill(); process.wait(timeout=5)
            selector.close()
            process.stdin.close(); process.stdout.close()
            (output / 'serial.log').write_bytes(transcript)
            (output / 'report.json').write_text(json.dumps(validationReport, indent=2) + '\n')


if __name__ == '__main__':
    run()
