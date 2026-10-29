#!/usr/bin/env python3
"""actualData OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import tempfile
import threading
import time
import selectors
from Crypto.Cipher import DES
from executeCommand import projectRoot, command
from networkBridge import networkBridge


def run():
    Parser = argparse.ArgumentParser(description=__doc__)
    Parser.add_argument('--kernel', type=Path, default=projectRoot / 'build/kernel8.img')
    Parser.add_argument('--access', type=Path, default=projectRoot / 'build/remote/access.json')
    Parser.add_argument('--output', type=Path, default=projectRoot / 'build/verification/native-remote')
    arguments = Parser.parse_args()
    Output = arguments.output
    Output.mkdir(parents=True, exist_ok=True)
    settings = json.loads(arguments.access.read_text())
    reportValue = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(arguments.kernel.read_bytes()).hexdigest(), 'checks': []}
    def emptyPort():
        with socket.socket() as connect:
            connect.bind(('127.0.0.5', 0))
            return connect.getsockname()[1]
    shellPort, screenPort, filePort = emptyPort(), emptyPort(), emptyPort()
    logRecord = bytearray()
    processValue = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as temporaryValue, networkBridge(filePort,
                ['tcp:{}:22'.format(shellPort), 'tcp:{}:5900'.format(screenPort)], hostAddress='127.0.0.5') as bridgeValue:
            Arguments = command()
            Arguments[Arguments.index('-kernel') + 1] = str(arguments.kernel.resolve())
            processValue = subprocess.Popen(Arguments + ['-display','none','-monitor','none','-serial','stdio'] + bridgeValue.forwardedArgument(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def gatherValues():
                while True:
                    data = processValue.stdout.read(4096)
                    if not data: break
                    logRecord.extend(data)
            threadValue = threading.Thread(target=gatherValues, daemon=True)
            threadValue.start()
            def waitState(wordText, initialItem=0, limitValue=60):
                ending = time.monotonic() + limitValue
                while wordText not in logRecord[initialItem:]:
                    if time.monotonic()>ending or processValue.poll() is not None:
                        raise AssertionError('Missing '+repr(wordText)+'\n'+logRecord[initialItem:].decode('utf-8','replace'))
                    time.sleep(.02)
            waitState(b'jkoros-native> ')
            helperValue = Path(temporaryValue)/'askpass'
            helperValue.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            helperValue.chmod(0o700)
            environment = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(helperValue), SSH_ASKPASS_REQUIRE='force')
            def secureShell(passwordValue, instructionValue, appendEntry=()):
                environment['JKOROS_TEST_PASSWORD']=passwordValue
                arguments=['ssh','-v']+list(appendEntry)+['-p',str(shellPort),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(temporaryValue)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',instructionValue]
                result=subprocess.run(arguments,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=environment,start_new_session=True,timeout=50)
                return result
            result=secureShell('!' + settings['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Output/'ssh-rejected.log').write_bytes(result.stderr)
            assert result.returncode!=0 and b'Permission denied' in result.stderr and b'SHOULD_NOT_RUN' not in logRecord, result.stderr
            reportValue['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            result=secureShell(settings['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Output/'ssh.log').write_bytes(result.stderr)
            (Output/'ssh-output.txt').write_bytes(result.stdout)
            assert result.returncode==0 and b'SSH_NATIVE_PASS' in result.stdout, (result.returncode,result.stdout,result.stderr)
            reportValue['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in result.stderr, result.stderr
            reportValue['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            result=secureShell(settings['ssh_password'], 'cd /example/java; java OutputExample; cd /')
            assert result.returncode==0 and 'JAVA Output: 안녕하세요 😀'.encode() in result.stdout,result.stdout
            reportValue['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            result=secureShell(settings['ssh_password'], 'missing_remote_command')
            assert result.returncode==127,result.returncode
            reportValue['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            result=secureShell(settings['ssh_password'], 'cat /example/java/WindowExample.java', ('-o', 'RekeyLimit=1K'))
            (Output/'ssh-rekey.log').write_bytes(result.stderr)
            assert result.returncode==0 and 'class WindowExample'.encode() in result.stdout, (result.returncode,result.stdout,result.stderr)
            assert result.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, result.stderr
            reportValue['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            interactiveArguments=['ssh','-tt','-p',str(shellPort),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(temporaryValue)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interactiveSession=subprocess.Popen(interactiveArguments,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=environment,start_new_session=True,bufsize=0)
            transcript=bytearray();selectionValue=selectors.DefaultSelector();selectionValue.register(interactiveSession.stdout,selectors.EVENT_READ)
            def readInteractive(showValue):
                deadlineValue=time.monotonic()+30
                while showValue not in transcript:
                    if time.monotonic()>deadlineValue or interactiveSession.poll() is not None:raise AssertionError('SSH interactive missing '+repr(showValue)+' '+repr(bytes(transcript)))
                    for entryValue,_ in selectionValue.select(.1):
                        fragmentValue=entryValue.fileobj.read(4096)
                        if fragmentValue:transcript.extend(fragmentValue)
            try:
                readInteractive(b'shared native console')
                interactiveSession.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interactiveSession.stdin.flush();readInteractive(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interactiveSession.stdin.write(b'\x04');interactiveSession.stdin.flush();remainderValue,error=interactiveSession.communicate(timeout=15)
                assert interactiveSession.returncode==0 and b'PTY allocation request failed' not in error,(interactiveSession.returncode,error)
                (Output/'ssh-interactive.txt').write_bytes(transcript+remainderValue)
            finally:
                selectionValue.close()
                if interactiveSession.poll() is None:interactiveSession.kill();interactiveSession.wait()
            reportValue['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def exactlyValue(connect, number):
                data=bytearray()
                while len(data)<number:
                    chunkValue=connect.recv(number-len(data))
                    if not chunkValue: raise AssertionError('RFB EOF')
                    data.extend(chunkValue)
                return bytes(data)
            def screenAuthentication(passwordValue):
                connect=socket.create_connection(('127.0.0.5',screenPort),10);connect.settimeout(30)
                assert exactlyValue(connect,12)==b'RFB 003.008\n'
                connect.sendall(b'RFB 003.008\n');assert exactlyValue(connect,2)==b'\x01\x02'
                connect.sendall(b'\x02');challengeValue=exactlyValue(connect,16)
                inputPassword=passwordValue.encode('ascii')[:8].ljust(8, b'\0')
                keyMaterial=bytes(int('{:08b}'.format(number)[::-1],2) for number in inputPassword)
                connect.sendall(DES.new(keyMaterial,DES.MODE_ECB).encrypt(challengeValue))
                stateValue=struct.unpack('!I',exactlyValue(connect,4))[0]
                return connect,stateValue
            invalidPassword='!' if not settings['vnc_password'].startswith('!') else '?'
            connect,stateValue=screenAuthentication(invalidPassword);assert stateValue==1;connect.close();time.sleep(.6)
            reportValue['checks'].append('VNC incorrect password rejected')
            connect,stateValue=screenAuthentication(settings['vnc_password']);assert stateValue==0
            with connect:
                connect.sendall(b'\x01');initialState=exactlyValue(connect,24);widthValue,heightValue=struct.unpack('!HH',initialState[:4]);name=exactlyValue(connect,struct.unpack('!I',initialState[20:24])[0])
                assert (widthValue,heightValue)==(640,480) and b'jkoros native'==name
                def Screen(incrementStep=0):
                    connect.sendall(struct.pack('!BBHHHH',3,incrementStep,0,0,widthValue,heightValue));headValue=exactlyValue(connect,4);number=struct.unpack('!H',headValue[2:])[0];totalValue=0
                    drawingValue=bytearray(widthValue*heightValue*4)
                    for _ in range(number):
                        xCoordinate,yCoordinate,regionWidth,regionHeight,methodMode=struct.unpack('!HHHHi',exactlyValue(connect,12));assert methodMode==0 and xCoordinate+regionWidth<=widthValue and yCoordinate+regionHeight<=heightValue
                        pixel=exactlyValue(connect,regionWidth*regionHeight*4);totalValue+=len(pixel)
                        for line in range(regionHeight):drawingValue[((yCoordinate+line)*widthValue+xCoordinate)*4:((yCoordinate+line)*widthValue+xCoordinate+regionWidth)*4]=pixel[line*regionWidth*4:(line+1)*regionWidth*4]
                    if not incrementStep:
                        from PIL import Image
                        Image.frombytes('RGB',(widthValue,heightValue),bytes(drawingValue),'raw','BGRX').save(str(Output/'native-vnc.png'))
                    return number,totalValue
                number,totalValue=Screen();assert number>0 and totalValue==widthValue*heightValue*4
                reportValue['checks'].append('Native framebuffer RFB full update {} bytes'.format(totalValue))
                number,totalValue=Screen(1);assert totalValue<widthValue*heightValue*4
                reportValue['checks'].append('RFB incremental update')
                initialItem=len(logRecord)
                for characterValue in 'echo VNC_NATIVE_PASS\r':
                    symbol=0xff0d if characterValue=='\r' else ord(characterValue)
                    connect.sendall(struct.pack('!BBHI',4,1,0,symbol));connect.sendall(struct.pack('!BBHI',4,0,0,symbol))
                waitState(b'VNC_NATIVE_PASS',initialItem)
                reportValue['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def keyStroke(symbol,pressValue=1):connect.sendall(struct.pack('!BBHI',4,pressValue,0,symbol))
                initialItem=len(logRecord)
                for characterValue in 'echo ':keyStroke(ord(characterValue))
                keyStroke(0xffc6)
                for characterValue in 'gksrmf':keyStroke(ord(characterValue))
                keyStroke(0xffc6);keyStroke(0xff0d)
                waitState('\r\n한글\r\n'.encode(),initialItem)
                reportValue['checks'].append('Native VNC F9 two-set Hangul composition')
                connect.sendall(struct.pack('!BBHH',5,0,120,100))
                reportValue['checks'].append('VNC pointer input accepted')
            processValue.stdin.write(b'poweroff\n');processValue.stdin.flush();processValue.wait(timeout=15);assert processValue.returncode==0
            reportValue['passed']=True
    finally:
        if processValue and processValue.poll() is None:
            processValue.terminate()
            try: processValue.wait(timeout=5)
            except subprocess.TimeoutExpired: processValue.kill();processValue.wait()
        (Output/'serial.log').write_bytes(logRecord)
        (Output/'report.json').write_text(json.dumps(reportValue,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(reportValue,ensure_ascii=False,indent=2))


if __name__=='__main__': run()
