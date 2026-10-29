#!/usr/bin/env python3
"""Run all examples in the real combined VNC + SLIP/FTP native VM."""
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
from pathlib import Path
from desktopView import exactValue
from exampleEcho import EchoServers
from executeCommand import projectRoot


def testLanguage(language,echoServerEntry,resultData):
    with socket.socket() as temporary:
        temporary.bind(('127.0.0.1',0));fileTransferPortNumber=temporary.getsockname()[1]
    process=subprocess.Popen(['python3',str(projectRoot/'tools/executeCommand.py'),'--desktop','--network','--port','0','--ftp-port',str(fileTransferPortNumber)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    selector=selectors.DefaultSelector();selector.register(process.stdout,selectors.EVENT_READ)
    transcript=bytearray();client=None;fileTransferConnection=None
    def receiveMessage(marker,run=0):
        endOffset=time.monotonic()+60
        while marker not in transcript[run:]:
            if time.monotonic()>endOffset or process.poll() is not None:raise AssertionError(transcript[run:].decode('utf-8','replace'))
            for pressedValue,_ in selector.select(.1):
                data=pressedValue.fileobj.read(65536)
                if data:transcript.extend(data)
        return transcript[run:].decode('utf-8','replace').replace('\r\n','\n')
    def pressedValue(symbolValue,isPressing=True):client.sendall(struct.pack('>BBHI',4,int(isPressing),0,symbolValue))
    def startOffset(line):
        run=len(transcript)
        for characterCode in line+'\n':
            symbolValue=0xff0d if characterCode=='\n' else ord(characterCode) if ord(characterCode)<256 else 0x1000000|ord(characterCode)
            pressedValue(symbolValue);pressedValue(symbolValue,False)
        return run
    def shell(line):return receiveMessage(b'jkoros-native> ',startOffset(line))
    def executeCommand(line,expected):
        text=shell(line);assert expected in text and 'exit 0' in text,(line,text)
        return text
    def pixelsList():
        client.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        rgbColour=bytearray(640*480*3)
        while True:
            categoryValue=exactValue(client,1)[0]
            if categoryValue==2:continue
            if categoryValue==3:
                itemCount=struct.unpack('>I',exactValue(client,7)[3:])[0];exactValue(client,itemCount);continue
            assert categoryValue==0,categoryValue
            entryCount=struct.unpack('>H',exactValue(client,3)[1:])[0]
            for _ in range(entryCount):
                xCoordinate,yCoordinate,requestedWidthValue,requestedHeightValue,characterSet=struct.unpack('>HHHHi',exactValue(client,12));assert characterSet==0,characterSet
                data=exactValue(client,requestedWidthValue*requestedHeightValue*4)
                for rowPosition in range(requestedHeightValue):
                    for columnPosition in range(requestedWidthValue):
                        originalData=(rowPosition*requestedWidthValue+columnPosition)*4;targetValue=((yCoordinate+rowPosition)*640+xCoordinate+columnPosition)*3
                        rgbColour[targetValue:targetValue+3]=bytes((data[originalData+2],data[originalData+1],data[originalData]))
            if entryCount:return rgbColour
    try:
        receiveMessage(b'TERMINAL READY');receiveMessage(b'jkoros-native> ',transcript.rfind(b'TERMINAL READY'))
        portNumber=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transcript).group(1))
        client=socket.create_connection(('127.0.0.1',portNumber),timeout=10)
        assert exactValue(client,12)==b'RFB 003.008\n';client.sendall(b'RFB 003.008\n')
        assert 1 in exactValue(client,exactValue(client,1)[0]);client.sendall(b'\x01');assert exactValue(client,4)==b'\0'*4
        client.sendall(b'\x01');initialValue=exactValue(client,24);exactValue(client,struct.unpack('>I',initialValue[20:])[0])
        client.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        client.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in shell('ftpd start')
        fileTransferConnection=ftplib.FTP();fileTransferConnection.encoding='utf-8';fileTransferConnection.connect('127.0.0.1',fileTransferPortNumber,timeout=20);fileTransferConnection.login()
        payloadData=('GUI와 FTP 동시 useValue '+language+' 😀\n').encode()
        fileTransferConnection.storbinary('STOR 함께.txt',io.BytesIO(payloadData))
        assert payloadData.decode().strip() in shell('cat /함께.txt')
        receivedCount=bytearray();fileTransferConnection.retrbinary('RETR 함께.txt',receivedCount.extend);assert receivedCount==payloadData;fileTransferConnection.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        sendList=shell('ls /example')
        assert all(name in sendList for name in ('java/','c/','python/','README.md')),sendList
        if language=='java':
            bundleManifest=json.loads((projectRoot/'build/examples/manifest.json').read_text())
            for path,entryPoint in bundleManifest.items():
                shell('cp '+path+' /example-check.bin')
                contentValue=bytearray();fileTransferConnection.retrbinary('RETR example-check.bin',contentValue.extend)
                assert len(contentValue)==entryPoint['bytes'] and hashlib.sha256(contentValue).hexdigest()==entryPoint['sha256'],path
            fileTransferConnection.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binary=bytes(range(256))*64
            fileTransferConnection.storbinary('STOR boundary.bin',io.BytesIO(binary))
            contentValue=bytearray();fileTransferConnection.retrbinary('RETR boundary.bin',contentValue.extend)
            assert contentValue==binary and 'boundary.bin' in fileTransferConnection.nlst()
            shell('cp /boundary.bin /boundary-copy.bin')
            contentValue=bytearray();fileTransferConnection.retrbinary('RETR boundary-copy.bin',contentValue.extend)
            assert contentValue==binary
            fileTransferConnection.delete('boundary.bin');fileTransferConnection.delete('boundary-copy.bin')
        assert 'OutputExample' in shell('ls /example/'+language)
        shell('cd /example/'+language)
        nameTable={'java':'JAVA','c':'C','python':'PYTHON'}[language]
        expectedFile=nameTable+' file: hangulText data 😀\n'
        if language=='java':
            executeCommand('javac OutputExample.java','Compiled:');executeCommand('java OutputExample','JAVA Output: 안녕하세요 😀')
            executeCommand('javac FileExample.java','Compiled:');executeCommand('java FileExample',expectedFile)
            executeCommand('java NetworkExample {} {}'.format(echoServerEntry.tcpPort,echoServerEntry.udpPort),'JAVA 네트워크 verify: TCP UDP hangulText')
            graphicsCommand='java GraphicsExample'
        elif language=='c':
            for name,forwardedValue,expected in [('Output','', 'C Output: 안녕하세요 😀'),('file','',expectedFile),
                    ('네트워크',' '+str(echoServerEntry.udpPort),'C 네트워크 verify: UDP hangulText')]:
                executeCommand('cc '+name+'examples.c -o executeCommand','Compiled native ARM64 ELF:')
                executeCommand('./executeCommand'+forwardedValue,expected)
            executeCommand('cc GraphicsExample.c -o executeCommand','Compiled native ARM64 ELF:');graphicsCommand='./executeCommand'
        else:
            for name,forwardedValue,expected in [('Output','','PYTHON Output: 안녕하세요 😀'),('file','',expectedFile),
                    ('네트워크',' '+str(echoServerEntry.udpPort),'PYTHON 네트워크 verify: UDP hangulText')]:
                executeCommand('python '+name+'examples.py'+forwardedValue,expected)
            graphicsCommand='python GraphicsExample.py'
        startDrawing=startOffset(graphicsCommand)
        text=receiveMessage('그림을 확인한 backValue Enter를 누르세요.\r\n'.encode(),startDrawing)
        assert nameTable+' 그래픽: 빨강 초록 파랑' in text and 'exit 0' not in text,text
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        fileTransferConnection.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        receivedCount=bytearray();fileTransferConnection.retrbinary('RETR 도중.txt',receivedCount.extend);assert receivedCount==b'FTP DURING GRAPHICS';fileTransferConnection.delete('도중.txt')
        rgbColour=pixelsList()
        for yCoordinate,pixelColour in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            offsetValue=(yCoordinate*640+610)*3;assert tuple(rgbColour[offsetValue:offsetValue+3])==pixelColour,(language,yCoordinate,tuple(rgbColour[offsetValue:offsetValue+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(rgbColour)).save(str(resultData/(language+'-graphics.png')))
        pressedValue(0xff0d);pressedValue(0xff0d,False)
        assert 'exit 0' in receiveMessage(b'jkoros-native> ',startDrawing)
        if language=='java':
            startWindow=startOffset('java WindowExample')
            receiveMessage('GUI examples prepare: WindowExample'.encode(),startWindow)
            def clickValue(horizontalPosition,verticalPosition):
                for button in (1,0):client.sendall(struct.pack('>BBHH',5,button,horizontalPosition,verticalPosition))
            time.sleep(.3)
            previousImage=Image.frombytes('RGB',(640,480),bytes(pixelsList()))
            clickValue(160,196)
            for _ in range(2):pressedValue(0xff08);pressedValue(0xff08,False)
            for characterValue in 'hangulText':pressedValue(0x1000000|ord(characterValue));pressedValue(0x1000000|ord(characterValue),False)
            for repetitionCount in (1,2):
                run=len(transcript);clickValue(180,242)
                receiveMessage(('GUI Greeting: 안녕하세요, 한글님! ('+str(repetitionCount)+')').encode(),run)
            time.sleep(.3)
            windowDrawing=Image.frombytes('RGB',(640,480),bytes(pixelsList()))
            assert previousImage.crop((110,272,530,300)).tobytes()!=windowDrawing.crop((110,272,530,300)).tobytes()
            windowDrawing.save(str(resultData/'java-swing.png'))
            run=len(transcript);clickValue(535,105)
            assert 'exit 0' in receiveMessage(b'jkoros-native> ',run)
        # Download the guest-created bytes through FTP in the same GUI VM.
        fileEntryName={'java':'java.txt','c':'c.txt','python':'python.txt'}[language]
        shell('cp '+fileEntryName+' /validate.txt')
        receivedCount=bytearray();fileTransferConnection.retrbinary('RETR validate.txt',receivedCount.extend);assert receivedCount==expectedFile.encode()
        shell('echo preserved > OutputExample.'+('py' if language=='python' else language))
        assert 'EXAMPLES READY' in shell('example '+language)
        assert '\npreserved\n' in shell('cat OutputExample.'+('py' if language=='python' else language))
        assert '한/zeroOperand keyValue, Shift+Space 또는 F9' in shell('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in shell('echo GUI NETWORK TOGETHER')
        fileTransferConnection.quit();fileTransferConnection=None;assert 'FTP stopped' in shell('ftpd stop')
        print('PASS '+language+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if fileTransferConnection:
            try:fileTransferConnection.close()
            except OSError:pass
        if client:client.close()
        process.terminate()
        try:process.wait(timeout=8)
        except subprocess.TimeoutExpired:process.kill();process.wait()
        selector.close();process.stdout.close();(resultData/(language+'-serial.log')).write_bytes(transcript)


def run():
    resultData=projectRoot/'build/verification/examples';resultData.mkdir(parents=True,exist_ok=True)
    validationReport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projectRoot/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with EchoServers() as echoServerEntry:
            for language in ('java','c','python'):
                testLanguage(language,echoServerEntry,resultData);validationReport['languages'].append(language)
            expected=[('tcp','JAVA TCP hangulText\n'),('udp','JAVA UDP hangulText'),('udp','C UDP hangulText'),('udp','PYTHON UDP hangulText')]
            assert echoServerEntry.hasReceived==[(categoryValue,data.encode()) for categoryValue,data in expected],echoServerEntry.hasReceived
            validationReport['host_network_payloads']=[{'protocol':categoryValue,'text':data.decode()} for categoryValue,data in echoServerEntry.hasReceived]
        validationReport.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(resultData/'report.json').write_text(json.dumps(validationReport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':run()
