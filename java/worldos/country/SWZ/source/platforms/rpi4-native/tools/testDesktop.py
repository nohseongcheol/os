#!/usr/bin/env python3
"""actualData RFB 클라이언트로 QEMU 창의 hangulText/keyValue/클립보드/마우스와 Screen 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from desktopView import exactValue
from executeCommand import projectRoot


def run():
    output=projectRoot/'build/verification/desktop'; output.mkdir(parents=True,exist_ok=True)
    process=subprocess.Popen(['python3',str(projectRoot/'tools/desktopView.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    readinessMonitor=selectors.DefaultSelector(); readinessMonitor.register(process.stdout,selectors.EVENT_READ)
    transcript=bytearray(); validationReport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projectRoot/'build/kernel8.img').read_bytes()).hexdigest()}
    def until(marker,run=0):
        deadlineTime=time.monotonic()+45
        while marker not in transcript[run:]:
            if time.monotonic()>deadlineTime or process.poll() is not None: raise AssertionError(transcript[run:].decode('utf-8','replace'))
            for pressedValue,_ in readinessMonitor.select(.1):
                data=pressedValue.fileobj.read(4096)
                if data: transcript.extend(data)
        return bytes(transcript[run:])
    try:
        until(b'TERMINAL READY')
        portNumber=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transcript).group(1))
        with socket.create_connection(('127.0.0.1',portNumber),timeout=10) as client:
            assert exactValue(client,12)==b'RFB 003.008\n'; client.sendall(b'RFB 003.008\n')
            assert 1 in exactValue(client,exactValue(client,1)[0]); client.sendall(b'\x01'); assert exactValue(client,4)==b'\0'*4
            client.sendall(b'\x01'); initialValue=exactValue(client,24); assert struct.unpack('>HH',initialValue[:4])==(640,480); exactValue(client,struct.unpack('>I',initialValue[20:])[0])
            client.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            client.sendall(struct.pack('>BBHi',2,0,1,0))
            def pressedValue(symbolValue,isPressing=True): client.sendall(struct.pack('>BBHI',4,int(isPressing),0,symbolValue))
            def typedCharacter(text):
                for characterData in text:
                    symbol=0xff0d if characterData=='\n' else ord(characterData) if ord(characterData)<256 else 0x01000000|ord(characterData)
                    pressedValue(symbol); pressedValue(symbol,False)
            def pressKey(symbolValue): pressedValue(symbolValue); pressedValue(symbolValue,False)
            # Start with English keys only, as delivered without a host IME.
            offsetValue=len(transcript); typedCharacter('echo '); pressKey(0xffc6)
            typedCharacter('dkssudgktpdy gksrmf'); pressKey(0xffc6); typedCharacter('\n')
            until('\r\n안녕하세요 hangulText\r\njkoros-native> '.encode(),offsetValue)
            offsetValue=len(transcript); typedCharacter('echo ')
            pressedValue(0xffe1); pressKey(32); pressedValue(0xffe1,False)
            typedCharacter('dlfr'); pressKey(0xff08); pressKey(0xff08); typedCharacter('fr')
            pressKey(0xff31); typedCharacter(' EN\n')
            until('\r\n읽 EN\r\njkoros-native> '.encode(),offsetValue)
            offsetValue=len(transcript); typedCharacter('echo '); pressKey(0xff31)
            typedCharacter('rhk rkqtk RkRnd'); pressKey(0xff31); typedCharacter('\n')
            until('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),offsetValue)
            # The same composition edits UTF-8 text in the native vi editor.
            offsetValue=len(transcript); typedCharacter('vi hangulInput.txt\n'); until(b'NORMAL',offsetValue)
            typedCharacter('i'); pressKey(0xffc6); typedCharacter('gksrmf dlfr'); pressKey(0xffc6)
            pressKey(0xff1b); typedCharacter(':wq\n'); until(b'jkoros-native> ',offsetValue)
            offsetValue=len(transcript); typedCharacter('cat hangulInput.txt\n')
            until('hangulText 읽'.encode(),offsetValue); until(b'jkoros-native> ',offsetValue)
            offsetValue=len(transcript); typedCharacter('help ko\n')
            until('한/zeroOperand keyValue, Shift+Space 또는 F9'.encode(),offsetValue); until(b'jkoros-native> ',offsetValue)
            offsetValue=len(transcript); typedCharacter('clear\necho "VNC hangulText inputValue 😀"\n'); until('VNC hangulText inputValue 😀\r\n'.encode(),offsetValue)
            offsetValue=len(transcript); pressedValue(0xffe3); pressedValue(ord('u')); pressedValue(ord('u'),False); pressedValue(0xffe3,False); typedCharacter('echo CONTROL_OK\n'); until(b'\r\nCONTROL_OK\r\n',offsetValue)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            clipboardValue='echo "pasteValue isComplete"\n'.encode(); offsetValue=len(transcript)
            client.sendall(struct.pack('>B3xI',6,len(clipboardValue))+clipboardValue)
            for event,_ in readinessMonitor.select(.15):
                dataBlock=event.fileobj.read(4096)
                if dataBlock: transcript.extend(dataBlock)
            assert 'pasteValue isComplete'.encode() not in transcript[offsetValue:]
            pressedValue(0xffe3); pressedValue(0xffe1); pressedValue(ord('v')); pressedValue(ord('v'),False); pressedValue(0xffe1,False); pressedValue(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            until('\r\n붙여넣기 isComplete\r\njkoros-native> '.encode(),offsetValue)
            client.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            rgbColour=bytearray(640*480*3); seenEntries=False
            while not seenEntries:
                noticeText=exactValue(client,1)[0]
                if noticeText==2: continue
                if noticeText==3:
                    size=struct.unpack('>I',exactValue(client,7)[3:])[0]; exactValue(client,size); continue
                assert noticeText==0,noticeText
                rectanglesList=struct.unpack('>H',exactValue(client,3)[1:])[0]
                for _ in range(rectanglesList):
                    xCoordinate,yCoordinate,requestedWidthValue,requestedHeightValue,characterSet=struct.unpack('>HHHHi',exactValue(client,12)); assert characterSet==0,characterSet
                    pixelsList=exactValue(client,requestedWidthValue*requestedHeightValue*4)
                    for innerOrdinal in range(requestedHeightValue):
                        for ordinalIndex in range(requestedWidthValue):
                            originalAddress=(innerOrdinal*requestedWidthValue+ordinalIndex)*4; destinationAddress=((yCoordinate+innerOrdinal)*640+xCoordinate+ordinalIndex)*3
                            rgbColour[destinationAddress:destinationAddress+3]=bytes((pixelsList[originalAddress+2],pixelsList[originalAddress+1],pixelsList[originalAddress]))
                    seenEntries=True
            assert rgbColour[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (output/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+rgbColour)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(rgbColour)).save(str(output/'vnc-terminal.png'))
            offsetValue=len(transcript)
            pressedValue(0xffe3); pressedValue(0xffe1); pressedValue(ord('t')); pressedValue(ord('t'),False); pressedValue(0xffe1,False); pressedValue(0xffe3,False)
            until(b'TERMINAL FOCUS 2',offsetValue)
            offsetValue=len(transcript); typedCharacter('echo SECOND_VNC_WINDOW\n'); until(b'\r\nSECOND_VNC_WINDOW\r\n',offsetValue)
            offsetValue=len(transcript); client.sendall(struct.pack('>BBHH',5,1,576,81)); client.sendall(struct.pack('>BBHH',5,0,576,81)); until(b'TERMINAL FOCUS 1',offsetValue)
            offsetValue=len(transcript); typedCharacter('python -c \'print("x"*9000)\'\n'); until(b'\r\njkoros-native> ',offsetValue)
            assert len(transcript)-offsetValue>8192,'exercise output longer than bridge status buffer'
            offsetValue=len(transcript); client.sendall(struct.pack('>BBHH',5,1,560,63)); client.sendall(struct.pack('>BBHH',5,0,560,63)); until(b'TERMINAL FOCUS 1',offsetValue)
            offsetValue=len(transcript); client.sendall(struct.pack('>BBHH',5,1,80,16)); client.sendall(struct.pack('>BBHH',5,0,80,16)); until(b'TERMINAL FOCUS 1',offsetValue)
            offsetValue=len(transcript); typedCharacter('echo REOPENED_VNC_WINDOW\n'); until(b'\r\nREOPENED_VNC_WINDOW\r\n',offsetValue)
            offsetValue=len(transcript); typedCharacter('gui\n'); until(b'GUI READY:',offsetValue)
            offsetValue=len(transcript); client.sendall(struct.pack('>BBHH',5,1,80,332)); client.sendall(struct.pack('>BBHH',5,0,80,332)); until(b'TERMINAL READY',offsetValue)
            validationReport.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if process.poll() is None:
            process.terminate()
            try: process.wait(timeout=8)
            except subprocess.TimeoutExpired: process.kill(); process.wait()
        readinessMonitor.close(); process.stdout.close()
        (output/'serial.log').write_bytes(transcript)
        (output/'report.json').write_text(json.dumps(validationReport,indent=2)+'\n')


if __name__=='__main__': run()
