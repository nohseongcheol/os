#!/usr/bin/env python3
"""actualData QEMU/VNC에서 Screen size·boundaryValue·window moveValue·Swing·언어별 그리기를 검사한다."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from PIL import Image
from desktopView import exactValue
from executeCommand import projectRoot


def ResolutionTest(widthValue, heightValue, resultPath):
    with socket.socket() as temporaryValue:
        temporaryValue.bind(('127.0.0.1', 0)); portNumber = temporaryValue.getsockname()[1]
    sizeText = '{}x{}'.format(widthValue, heightValue)
    processValue = subprocess.Popen(['python3', str(projectRoot/'tools/executeCommand.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(portNumber), '--resolution', sizeText], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Selector = selectors.DefaultSelector(); Selector.register(processValue.stdout, selectors.EVENT_READ)
    logRecord = bytearray(); remoteValue = None; transferValue = None

    def await(showValue, run=0):
        deadlineValue = time.monotonic() + 60
        while showValue not in logRecord[run:]:
            if time.monotonic() > deadlineValue or processValue.poll() is not None or b'HALTED' in logRecord or b'PANIC:' in logRecord:
                raise AssertionError(logRecord[run:].decode('utf-8', 'replace'))
            for event, _ in Selector.select(.1):
                data = event.fileobj.read(65536)
                if data: logRecord.extend(data)
        return logRecord[run:].decode('utf-8', 'replace')

    def clickButton(symbol, isPressed=True): remoteValue.sendall(struct.pack('>BBHI', 4, int(isPressed), 0, symbol))

    def sendText(text):
        run = len(logRecord)
        for characterValue in text:
            symbol = 0xff0d if characterValue == '\n' else ord(characterValue) if ord(characterValue) < 256 else 0x1000000 | ord(characterValue)
            clickButton(symbol); clickButton(symbol, False)
        return run

    def shell(text): return await(b'\r\n__RESOLUTION_DONE__\r\n', sendText(text+'; echo __RESOLUTION_DONE__\n'))

    def pointAt(horizontalPosition, verticalPosition, isPressed): remoteValue.sendall(struct.pack('>BBHH', 5, isPressed, horizontalPosition, verticalPosition))

    def clickValue(horizontalPosition, verticalPosition): pointAt(horizontalPosition, verticalPosition, 1); pointAt(horizontalPosition, verticalPosition, 0)

    def bitmapImage():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 actualData 너비를 쓴다.
        remoteValue.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, widthValue, heightValue))
        drawingValue = Image.new('RGB', (widthValue, heightValue)); areaValue = 0
        while True:
            kindValue = exactValue(remoteValue, 1)[0]
            if kindValue == 2: continue
            if kindValue == 3:
                lengthValue = struct.unpack('>I', exactValue(remoteValue, 7)[3:])[0]; exactValue(remoteValue, lengthValue); continue
            assert kindValue == 0, kindValue
            itemCount = struct.unpack('>H', exactValue(remoteValue, 3)[1:])[0]
            for _ in range(itemCount):
                horizontalPosition, verticalPosition, widthSpan, lengthValue, encodingValue = struct.unpack('>HHHHi', exactValue(remoteValue, 12))
                assert encodingValue == 0 and horizontalPosition+widthSpan <= widthValue and verticalPosition+lengthValue <= heightValue
                drawingValue.paste(Image.frombytes('RGB', (widthSpan, lengthValue), exactValue(remoteValue, widthSpan*lengthValue*4), 'raw', 'BGRX'), (horizontalPosition, verticalPosition))
                areaValue += widthSpan*lengthValue
            if areaValue:
                assert areaValue == widthValue*heightValue, areaValue
                return drawingValue

    def checkPixel(coordinateValue, colourValue):
        deadlineValue = time.monotonic()+10
        while True:
            drawingValue = bitmapImage()
            if drawingValue.getpixel(coordinateValue) == colourValue: return drawingValue
            if time.monotonic() > deadlineValue: raise AssertionError((coordinateValue, drawingValue.getpixel(coordinateValue), colourValue))

    def uploadFiles(name, data): transferValue.storbinary('STOR '+name, io.BytesIO(data))

    try:
        await(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+sizeText+' RGB32').encode() in logRecord
        print('BOOT:', sizeText, flush=True)
        remoteNumber = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', logRecord).group(1))
        remoteValue = socket.create_connection(('127.0.0.1', remoteNumber), timeout=20)
        assert exactValue(remoteValue, 12) == b'RFB 003.008\n'; remoteValue.sendall(b'RFB 003.008\n')
        assert 1 in exactValue(remoteValue, exactValue(remoteValue, 1)[0]); remoteValue.sendall(b'\x01')
        assert exactValue(remoteValue, 4) == b'\0'*4; remoteValue.sendall(b'\x01')
        initialState = exactValue(remoteValue, 24); assert struct.unpack('>HH', initialState[:4]) == (widthValue, heightValue)
        exactValue(remoteValue, struct.unpack('>I', initialState[20:])[0])
        remoteValue.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        remoteValue.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        checkPixel((widthValue-1, heightValue-1), (24, 32, 48))
        # Screen right 아래까지 이동한다. previousItem 640×480 boundaryValue 밖에서 X를 누른다.
        pointAt(40, 60, 1); pointAt(widthValue-568+28, heightValue-360+12, 1); pointAt(widthValue-568+28, heightValue-360+12, 0)
        checkPixel((widthValue-568, heightValue-360), (32, 80, 144))
        run = len(logRecord); clickValue(widthValue-20, heightValue-345); await(b'TERMINAL FOCUS 1', run)
        checkPixel((widthValue-568, heightValue-360), (24, 32, 48))
        run = len(logRecord); clickValue(80, 16); await(b'TERMINAL FOCUS 1', run)
        shell('ftpd start')
        transferValue = ftplib.FTP(); transferValue.encoding = 'utf-8'; transferValue.connect('127.0.0.1', portNumber, timeout=20); transferValue.login()
        # C boundaryValue 검사는 32비트 unsigned negativeValue convertValue·clip 밖·빈 사각형을 포함한다.
        source = '''#include <ScreenABI.h>
#include <FileABI.h>
int main(void) {
    unsigned widthValue=screenWidth(), heightValue=screenHeight();
    if(widthValue!=WIDTH || heightValue!=HEIGHT) return 1;
    if(drawRectangle(widthValue,heightValue,0,0,0)) return 2;
    if(drawRectangle(widthValue,heightValue-1,1,1,0)!=-22) return 3;
    if(drawRectangle(widthValue-1,heightValue,1,1,0)!=-22) return 4;
    if(drawRectangle(-1,0,1,1,0)!=-22) return 5;
    if(drawRectangle(0,0,-1,1,0)!=-22) return 6;
    if(drawRectangle(widthValue-1,heightValue-1,1,1,0x332211)) return 7;
    writeFileData(1,"C RESOLUTION PASS\\n",18);
    waitForDrawing(); return 0;
}
'''.replace('WIDTH', str(widthValue)).replace('HEIGHT', str(heightValue))
        uploadFiles('testScreen.c', source.encode())
        assert 'exit 0' in shell('cc /testScreen.c -o /testScreen')
        await(b'C RESOLUTION PASS', sendText('run /testScreen\n'))
        checkPixel((widthValue-1, heightValue-1), (17, 34, 51))
        await(b'jkoros-native> ', sendText('q'))
        source = '''from English import screenSize, drawRectangle, waitForDrawing, Output, SystemError
widthValue, heightValue = screenSize()
assert (widthValue, heightValue) == (WIDTH, HEIGHT)
try:
    drawRectangle(widthValue, heightValue-1, 1, 1, 0)
    raise AssertionError("boundary")
except SystemError as error:
    assert error.index == 22
drawRectangle(widthValue-1, heightValue-1, 1, 1, 0x665544)
Output("PYTHON RESOLUTION PASS")
waitForDrawing()
'''.replace('WIDTH', str(widthValue)).replace('HEIGHT', str(heightValue))
        uploadFiles('testScreen.py', source.encode())
        await(b'PYTHON RESOLUTION PASS', sendText('python /testScreen.py\n'))
        checkPixel((widthValue-1, heightValue-1), (68, 85, 102))
        await(b'jkoros-native> ', sendText('q'))
        source = '''import English.Native.*;
public class ResolutionTest {
    public static void main(String[] arguments) {
        int widthValue=Screen.widthValue(), heightValue=Screen.heightValue();
        if (widthValue!=WIDTH || heightValue!=HEIGHT) throw new StateException("size");
        try { Screen.rectangle(widthValue,heightValue-1,1,1,0); throw new StateException("clip"); }
        catch (InvalidArgumentException error) { }
        Screen.eraseEntry(0x302018);
        Screen.rectangle(widthValue-1,heightValue-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        Screen.await();
    }
}
'''.replace('WIDTH', str(widthValue)).replace('HEIGHT', str(heightValue))
        # exception 처리는 Host javac 결과를 Native JVM에 올려 검사한다.
        boundarySource = resultPath/'해상도경계시험.java'
        boundarySource.write_text(source.replace('class ResolutionTest', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(projectRoot/'dist/jkoros-native-korean.jar'), '-d', str(resultPath), str(boundarySource)])
        uploadFiles('해상도경계시험.class', (resultPath/'해상도경계시험.class').read_bytes())
        await(b'JAVA RESOLUTION PASS', sendText('java 해상도경계시험\n'))
        checkPixel((widthValue-1, heightValue-1), (119, 136, 153))
        await(b'jkoros-native> ', sendText('q'))
        # 게스트 javac의 supportValue 문법으로 size queryValue·eraseEntry·다섯 arguments 그리기를 컴파일한다.
        source = '''public class ResolutionTest {
    public static void main(String[] arguments) {
        int widthValue=English.Native.Screen.widthValue();
        int heightValue=English.Native.Screen.heightValue();
        if (widthValue!=WIDTH || heightValue!=HEIGHT) return;
        English.Native.Screen.eraseEntry(3153944);
        English.Native.Screen.rectangle(widthValue-1,heightValue-1,1,1,10061943);
        English.Native.Output.writeLine("JAVA RESOLUTION PASS");
        English.Native.Screen.await();
    }
}
'''.replace('WIDTH', str(widthValue)).replace('HEIGHT', str(heightValue))
        uploadFiles('ResolutionTest.java', source.encode())
        result = shell('javac ResolutionTest.java'); assert 'exit 0' in result, result
        await(b'JAVA RESOLUTION PASS', sendText('java ResolutionTest\n'))
        checkPixel((widthValue-1, heightValue-1), (119, 136, 153))
        await(b'jkoros-native> ', sendText('q'))
        uploadFiles('SwingTest.class', (resultPath/'SwingTest.class').read_bytes())
        await(b'SWING READY', sendText('java SwingTest\n'))
        horizontalPosition, verticalPosition = (widthValue-400)//2, (heightValue-280)//2
        drawingValue = checkPixel((horizontalPosition, verticalPosition), (32, 80, 144))
        drawingValue.save(str(resultPath/(sizeText+'.png')))
        run = len(logRecord); clickValue(horizontalPosition+80, verticalPosition+155)
        await('SWING CLICK name'.encode(), run)
        run = len(logRecord); clickValue(horizontalPosition+385, verticalPosition+15); await(b'jkoros-native> ', run)
        assert 'AFTER_RESOLUTION' in shell('echo AFTER_RESOLUTION')
        print('PASS:', sizeText, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if transferValue: transferValue.close()
        if remoteValue: remoteValue.close()
        if processValue.poll() is None:
            processValue.terminate()
            try: processValue.wait(timeout=8)
            except subprocess.TimeoutExpired: processValue.kill(); processValue.wait()
        Selector.close(); processValue.stdout.close()
        (resultPath/(sizeText+'.log')).write_bytes(logRecord)


def run():
    resultPath = projectRoot/'build/verification/resolution'; resultPath.mkdir(parents=True, exist_ok=True)
    logRecord = {'passed': False, 'kernel_sha256': hashlib.sha256((projectRoot/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for invalidValue in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            result = subprocess.run(['python3', str(projectRoot/'tools/executeCommand.py'), '--resolution', invalidValue], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert result.returncode == 2 and b'--resolution' in result.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(resultPath), str(projectRoot/'tests/Java/SwingTest.java')])
        for widthValue, heightValue in ((1920,1080), (1280,720), (640,480)):
            ResolutionTest(widthValue, heightValue, resultPath); logRecord['resolutions'].append([widthValue, heightValue])
        logRecord.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (resultPath/'report.json').write_text(json.dumps(logRecord, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': run()
