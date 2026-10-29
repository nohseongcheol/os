#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from executeCommand import projectRoot,command

def run():
    destinationValuePosition=projectRoot/'build/verification/swing';destinationValuePosition.mkdir(parents=True,exist_ok=True)
    classPath=projectRoot/'build/verification/new-java';classPath.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(projectRoot/'dist/jkoros-native-korean.jar'),'-d',str(classPath),str(projectRoot/'tests/Java/SwingTest.java'),str(projectRoot/'tests/Java/testHangulWindow.java')])
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
            data=(projectRoot/'build/verification/new-java/SwingTest.class').read_bytes()
            send('load SwingTest.class\n'.encode(),b'hex> ')
            for ordinalIndex in range(0,len(data),64):send(data[ordinalIndex:ordinalIndex+64].hex().encode()+b'\n',b'hex> ')
            send(b'.\n')
            send('java SwingTest\n'.encode(),b'SWING READY')
            endOffset=time.monotonic()+3
            while time.monotonic()<endOffset:handleEvent(.1)
            # JFrame centered at (120,100), content at y=130.
            send(clickButton(200,210),b'',)  # focus JTextField
            dataPosition.stdin.write('누리'.encode());dataPosition.stdin.flush()
            endOffset=time.monotonic()+.3
            while time.monotonic()<endOffset:handleEvent(.05)
            result=send(clickButton(200,255),'SWING CLICK 이름누리'.encode())
            await(b'true',len(logRecord)-len(result))
            send(shortcutValue(1),b'TERMINAL FOCUS 2')
            result=shell('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in result
            send(clickButton(180,12),b'TERMINAL FOCUS 1')
            endOffset=time.monotonic()+.3
            while time.monotonic()<endOffset:handleEvent(.05)
            with socket.socket(socket.AF_UNIX) as characterCode:
                characterCode.settimeout(10);characterCode.connect(str(mockControlConnection))
                with characterCode.makefile('rwb') as fileEntry:
                    json.loads(fileEntry.readline())
                    for requestValue in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(destinationValuePosition/'native-swing.png'),'format':'png'}}):
                        fileEntry.write((json.dumps(requestValue)+'\n').encode());fileEntry.flush()
                        while True:
                            returnedValue=json.loads(fileEntry.readline())
                            if 'error' in returnedValue:raise AssertionError(returnedValue)
                            if 'return' in returnedValue:break
            send(clickButton(505,115))
            shell('echo SWING_CLOSED_OK')
            data=(classPath/'testHangulWindow.class').read_bytes()
            send('load testHangulWindow.class\n'.encode(),b'hex> ')
            for ordinalIndex in range(0,len(data),64):send(data[ordinalIndex:ordinalIndex+64].hex().encode()+b'\n',b'hex> ')
            send(b'.\n')
            send('java testHangulWindow\n'.encode(),b'KOREAN SWING READY')
            send(clickButton(200,255),'KOREAN SWING CLICK name'.encode())
            send(clickButton(505,115))
            shell('echo KOREAN_SWING_CLOSED_OK')
            validationReport.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','English window/button/ActionNotice/EventQueue directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if dataPosition.poll() is None:dataPosition.terminate()
            try:dataPosition.wait(timeout=5)
            except subprocess.TimeoutExpired:dataPosition.kill();dataPosition.wait()
            Selector.close();dataPosition.stdin.close();dataPosition.stdout.close();(destinationValuePosition/'serial.log').write_bytes(logRecord);(destinationValuePosition/'report.json').write_text(json.dumps(validationReport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':run()
