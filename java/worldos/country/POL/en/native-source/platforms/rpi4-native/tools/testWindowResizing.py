#!/usr/bin/env python3
"""actualData QEMU/VNC에서 terminal cornerValue dragValue·pointer·동적 characterValue slotEntry·editValue contentValue 보존를 검사한다."""
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


def testWindowResizing(widthValue, heightValue, resultPath):
    with socket.socket() as temporaryValue:
        temporaryValue.bind(('127.0.0.1', 0)); portNumber = temporaryValue.getsockname()[1]
    sizeText = '{}x{}'.format(widthValue, heightValue)
    processValue = subprocess.Popen(['python3', str(projectRoot/'tools/executeCommand.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(portNumber), '--resolution', sizeText], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Selector = selectors.DefaultSelector(); Selector.register(processValue.stdout, selectors.EVENT_READ)
    logRecord = bytearray(); remoteValue = None; transferValue = None; pointerHidden=[False]

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

    def shell(text): return await(b'\r\n__RESIZE_DONE__\r\n', sendText(text+'; echo __RESIZE_DONE__\n'))

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
                if encodingValue == -239:
                    assert widthSpan==0 and lengthValue==0, 'remote cursor must be hidden'
                    pointerHidden[0]=True
                    continue
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
        remoteValue.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        checkPixel((widthValue-1, heightValue-1), (24, 32, 48))
        def pauseBriefly(secondsValue=.25):
            ending=time.monotonic()+secondsValue
            while time.monotonic()<ending:
                for event,_ in Selector.select(.02):
                    data=event.fileobj.read(65536)
                    if data:logRecord.extend(data)
        window=[12,48,568,360]
        def verifySize():
            columnValue,rowValue=(window[2]-24)//8,(window[3]-56)//16
            text=shell('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(columnValue,rowValue) in text,text
            # actualData window 테두리: 단지 size queryValue 값만 바뀐 것이 아닌지 확인한다.
            pointAt(widthValue-1,10,0);pauseBriefly()
            checkPixel((window[0],window[1]),(32,80,144))
            drawingValue=checkPixel((window[0]+window[2]-1,window[1]+window[3]-1),(39,49,64))
            return drawingValue
        def cornerValue(direction):
            return (window[0]+(3 if direction in (1,3) else window[2]-4),window[1]+(3 if direction<=2 else window[3]-4))
        def resizeDrag(direction,differenceValue,button=1):
            firstOperand,threeValue=cornerValue(direction);pointAt(firstOperand,threeValue,0);pauseBriefly()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            whitePixel=(firstOperand-7 if direction in (1,4) else firstOperand+7,threeValue-7)
            checkPixel(whitePixel,(255,255,255))
            pointAt(firstOperand,threeValue,button)
            endHorizontal=max(0,min(widthValue-1,firstOperand+differenceValue[0]));endVertical=max(0,min(heightValue-1,threeValue+differenceValue[1]))
            pointAt(endHorizontal,endVertical,button);pointAt(endHorizontal,endVertical,0);pauseBriefly()
            if button==1:
                leftValue,topValue,widthSpan,lengthValue=window;rightValue,bottomValue=leftValue+widthSpan,topValue+lengthValue
                if direction in (1,3):leftValue=max(0,min(rightValue-360,leftValue+endHorizontal-firstOperand))
                else:rightValue=max(leftValue+360,min(widthValue,rightValue+endHorizontal-firstOperand))
                if direction<=2:topValue=max(34,min(bottomValue-216,topValue+endVertical-threeValue))
                else:bottomValue=max(topValue+216,min(heightValue,bottomValue+endVertical-threeValue))
                window[:]=[leftValue,topValue,rightValue-leftValue,bottomValue-topValue]
        verifySize();assert pointerHidden[0]
        resizeDrag(4,(-100,-60),4);verifySize() # right 버튼은 크기를 바꾸지 않는다.
        for direction,differenceValue in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            resizeDrag(direction,differenceValue);verifySize()
        # inputValue 중인 긴 hangulText 명령은 newline/horizontalPosition 스크롤과 무관하게 그대로 실행된다.
        longText='크기가 바뀌어도 입력한 hangulText 명령이 그대로 남습니다 '*3
        sendText("echo '"+longText+"'");pauseBriefly()
        resizeDrag(4,(-1000,-1000));assert window[2:]==[360,216]
        resizeDrag(4,(widthValue,heightValue))
        run=sendText('\n');await(('\r\n'+longText+'\r\n').encode(),run);verifySize()
        # vi가 editValue 중에 Screen 크기를 retryValue 읽고, 저장하지 않은 한글도 유지한다.
        shell('ftpd start')
        transferValue=ftplib.FTP();transferValue.encoding='utf-8';transferValue.connect('127.0.0.1',portNumber,timeout=20);transferValue.login()
        await(b'NORMAL',sendText('vi /크기자료.txt\n'))
        await(b'INSERT',sendText('i미저장 hangulText data\n'));pauseBriefly()
        resizeDrag(4,(-widthValue,-heightValue))
        # ANSI rowValue 이동에 새 rowValue 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((window[3]-56)//16)).encode() in logRecord[-4096:]
        sendText('작은 창에서도 continuationValue write\n');pauseBriefly()
        resizeDrag(4,(widthValue,heightValue))
        sendText('큰 창에서도 continuationValue write\n');pauseBriefly()
        clickButton(0xff1b);clickButton(0xff1b,False);pauseBriefly()
        await(b'jkoros-native> ',sendText(':wq\n'))
        contentValue=bytearray();transferValue.retrbinary('RETR 크기자료.txt',contentValue.extend)
        assert contentValue=='미저장 hangulText data\n작은 창에서도 continuationValue write\n큰 창에서도 continuationValue write\n'.encode(),contentValue
        verifySize().save(str(resultPath/(sizeText+'-large.png')))
        # 두 번째 창은 defaultValue size, retryValue firstItem 창을 고르면 앞에서 바꾼 크기가 유지된다.
        run=len(logRecord);clickValue(70,16);await(b'TERMINAL FOCUS 2',run)
        assert 'TERMINAL SIZE 68x19' in shell('terminal size')
        run=len(logRecord);clickValue(180,16);await(b'TERMINAL FOCUS 1',run);verifySize()
        resizeDrag(4,(-widthValue,-heightValue));verifySize().save(str(resultPath/(sizeText+'-small.png')))
        # size changeValue backValue X 닫기도 새로운 right 가장자리를 사용한다.
        run=len(logRecord);clickValue(window[0]+window[2]-20,window[1]+15);await(b'TERMINAL FOCUS 2',run)
        assert 'RESIZE CLOSED' in shell('echo RESIZE CLOSED')
        print('PASS:',sizeText,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if transferValue:transferValue.close()
        if remoteValue:remoteValue.close()
        if processValue.poll() is None:
            processValue.terminate()
            try:processValue.wait(timeout=8)
            except subprocess.TimeoutExpired:processValue.kill();processValue.wait()
        Selector.close();processValue.stdout.close();(resultPath/(sizeText+'.log')).write_bytes(logRecord)


def run():
    resultPath=projectRoot/'build/verification/resize';resultPath.mkdir(parents=True,exist_ok=True)
    logRecord={'passed':False,'kernel_sha256':hashlib.sha256((projectRoot/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for widthValue,heightValue in ((640,480),(1920,1080)):
            testWindowResizing(widthValue,heightValue,resultPath);logRecord['resolutions'].append([widthValue,heightValue])
        logRecord.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(resultPath/'report.json').write_text(json.dumps(logRecord,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':run()
