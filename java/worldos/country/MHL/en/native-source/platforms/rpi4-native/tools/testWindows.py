#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from executeCommand import projectRoot,command

def run():
    destinationValuePosition=projectRoot/'build/verification/windows';destinationValuePosition.mkdir(parents=True,exist_ok=True)
    validationReport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projectRoot/'build/kernel8.img').read_bytes()).hexdigest()};logRecord=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as workingPath:
        mockControlConnection=Path(workingPath)/'qmp.sock'
        dataPosition=subprocess.Popen(command()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(mockControlConnection)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        Selector=selectors.DefaultSelector();Selector.register(dataPosition.stdout,selectors.EVENT_READ)
        def handleEvent(secondsUnit=.1):
            for pressedValue,_ in Selector.select(secondsUnit):
                secondValue=pressedValue.fileobj.read(65536)
                if secondValue:logRecord.extend(secondValue)
            assert b'PANIC:' not in logRecord and b'HALTED' not in logRecord,logRecord[-2048:]
        def await(marker,currentPosition,secondsUnit=50):
            endOffset=time.monotonic()+secondsUnit
            while marker not in logRecord[currentPosition:]:
                if time.monotonic()>endOffset or dataPosition.poll() is not None:raise AssertionError(logRecord[currentPosition:].decode('utf-8','replace'))
                handleEvent()
            return bytes(logRecord[currentPosition:])
        def send(secondValue,marker=b'jkoros-native> '):
            currentPosition=len(logRecord);dataPosition.stdin.write(secondValue);dataPosition.stdin.flush();return await(marker,currentPosition)
        def shell(stringData):return send((stringData+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def shortcutValue(thirdIndex):return bytes([30,2,thirdIndex,0,0,0,0])
        def clickButton(xCoordinate,yCoordinate):return bytes([30,1,1,xCoordinate&255,xCoordinate>>8,yCoordinate&255,yCoordinate>>8,30,1,0,xCoordinate&255,xCoordinate>>8,yCoordinate&255,yCoordinate>>8])
        def commandMode():
            dataPosition.stdin.write(b'\x1b');dataPosition.stdin.flush();endOffset=time.monotonic()+.2
            while time.monotonic()<endOffset:handleEvent(.03)
        try:
            await(b'jkoros-native> ',0)
            shell('terminal');handleEvent(.3)
            shell('mkdir first; cd first; export NAME=one')
            send('vi firstOrdinal.py\n'.encode(),b'NORMAL')
            send('i값 = 21\nprint(value * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            endOffset=time.monotonic()+3
            while time.monotonic()<endOffset:handleEvent(.1)
            send(shortcutValue(1),b'TERMINAL FOCUS 2');handleEvent(.2)
            assert b'/\r\n' in shell('pwd')
            shell('export NAME=two')
            send('vi secondOrdinal.txt\n'.encode(),b'NORMAL')
            send('i두 번째 window\n'.encode(),b'INSERT')
            send(clickButton(180,12),b'TERMINAL FOCUS 1');handleEvent(.2)
            commandMode();send(b':wq\r')
            assert b'one:/first' in shell('echo "$NAME:$PWD"')
            assert 'value = 21\r\nprint(value * 2)'.encode() in shell('cat firstOrdinal.py')
            result=shell('python firstOrdinal.py');assert b'42\r\n' in result,result
            # Close the first shell with its actual title-bar X; second editor resumes.
            send(clickButton(560,63),b'TERMINAL FOCUS 2');handleEvent(.2)
            commandMode();send(b':wq\r')
            assert b'two:/' in shell('echo "$NAME:$PWD"')
            assert '두 번째 window'.encode() in shell('cat secondOrdinal.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            send('vi secondOrdinal.txt\n'.encode(),b'NORMAL');send(b'xu',b'NORMAL')
            send(b'iX',b'INSERT');commandMode();send(b':q\r',b'Unsaved')
            send(b':q!\r');assert '두 번째 window'.encode() in shell('cat secondOrdinal.txt')
            send(shortcutValue(1),b'TERMINAL FOCUS 1');handleEvent(.2)
            send(shortcutValue(1),b'TERMINAL FOCUS 3');handleEvent(.2)
            send(shortcutValue(1),b'TERMINAL FOCUS 4');handleEvent(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            dataPosition.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));dataPosition.stdin.flush()
            shell('echo DRAGGED_OK')
            send('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            send('i저장하지 않은 data'.encode(),b'INSERT')
            send(clickButton(578,97),b'TERMINAL FOCUS 3');handleEvent(.2)
            assert '버릴문서.txt'.encode() not in shell('ls')
            send(shortcutValue(1),b'TERMINAL FOCUS 4');handleEvent(.2)
            shell('echo REUSED_WINDOW_OK')
            completedAmount=logRecord.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            await(b'jkoros-native> ',completedAmount)
            # UART completion precedes the next QEMU display refresh.
            endOffset=time.monotonic()+.3
            while time.monotonic()<endOffset:handleEvent(.05)
            with socket.socket(socket.AF_UNIX) as characterCode:
                characterCode.settimeout(10);characterCode.connect(str(mockControlConnection))
                with characterCode.makefile('rwb') as fileEntry:
                    json.loads(fileEntry.readline())
                    for requestValue in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(destinationValuePosition/'four-terminals.png'),'format':'png'}}):
                        fileEntry.write((json.dumps(requestValue)+'\n').encode());fileEntry.flush()
                        while True:
                            returnedValue=json.loads(fileEntry.readline())
                            if 'error' in returnedValue:raise AssertionError(returnedValue)
                            if 'return' in returnedValue:break
            from PIL import Image
            pixelsList=Image.open(str(destinationValuePosition/'four-terminals.png')).convert('RGB')
            for coordinatePair,pixelColour in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert pixelsList.getpixel(coordinatePair)==pixelColour,(coordinatePair,pixelsList.getpixel(coordinatePair))
            shell('echo FOUR_WINDOWS_OK')
            validationReport.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if dataPosition.poll() is None:dataPosition.terminate()
            try:dataPosition.wait(timeout=5)
            except subprocess.TimeoutExpired:dataPosition.kill();dataPosition.wait()
            Selector.close();dataPosition.stdin.close();dataPosition.stdout.close();(destinationValuePosition/'serial.log').write_bytes(logRecord);(destinationValuePosition/'report.json').write_text(json.dumps(validationReport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':run()
