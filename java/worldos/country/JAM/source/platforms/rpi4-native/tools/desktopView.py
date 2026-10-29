#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, keyValue 입력은 Native kernelValue UART로 전달한다. localhost 전용, 단일 controlValue 클라이언트.
RFB 3.8: https://www.rfc-editor.org/rfc/rfc6143.html
"""
import argparse
from contextlib import ExitStack
from pathlib import Path
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
from executeCommand import command
from local_input import create


def exactValue(socketValue, size):
    data = bytearray()
    while len(data) < size:
        fragmentValue = socketValue.recv(size - len(data))
        if not fragmentValue: raise EOFError()
        data.extend(fragmentValue)
    return bytes(data)


class Keyboard:
    def __init__(selfValue, send, modeChanged=None):
        selfValue.transferBytes = send; selfValue.modifierKey = set(); selfValue.clipboardValue = b''
        selfValue.HangulComposer = create(send, Path(__file__).resolve().parents[1]); selfValue.korean = False; selfValue.switchKey = set()
        selfValue.unicodeInput = None
        selfValue.modeChanged = modeChanged
        if modeChanged: modeChanged(False)

    def send(selfValue, data):
        selfValue.HangulComposer.commitComposition()
        selfValue.transferBytes(data)

    def switchMode(selfValue):
        selfValue.HangulComposer.commitComposition(); selfValue.korean = not selfValue.korean
        if selfValue.modeChanged: selfValue.modeChanged(selfValue.korean)

    def pressedValue(selfValue, isPressing, keySymbol):
        if keySymbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if isPressing: selfValue.modifierKey.add(keySymbol)
            else: selfValue.modifierKey.discard(keySymbol)
            return
        if not isPressing:
            selfValue.switchKey.discard(keySymbol)
            return
        controlKey = bool(selfValue.modifierKey & {0xffe3, 0xffe4})
        shiftKey = bool(selfValue.modifierKey & {0xffe1, 0xffe2})
        if controlKey and shiftKey and keySymbol in (ord('u'),ord('U')):
            selfValue.HangulComposer.commitComposition(); selfValue.unicodeInput = ''; return
        if selfValue.unicodeInput is not None:
            if keySymbol in (32,0xff0d):
                try:
                    value=int(selfValue.unicodeInput,16)
                    if 32<=value<=0x10ffff and not 0xd800<=value<=0xdfff: selfValue.send(chr(value).encode('utf-8'))
                except ValueError: pass
                selfValue.unicodeInput=None
            elif keySymbol==0xff1b: selfValue.unicodeInput=None
            elif keySymbol==0xff08: selfValue.unicodeInput=selfValue.unicodeInput[:-1]
            elif keySymbol<128 and chr(keySymbol) in '0123456789abcdefABCDEF' and len(selfValue.unicodeInput)<6: selfValue.unicodeInput+=chr(keySymbol)
            return
        if keySymbol in (0xff31,0xffc6) or keySymbol==32 and shiftKey and not controlKey:
            if keySymbol not in selfValue.switchKey: selfValue.switchMode()
            selfValue.switchKey.add(keySymbol)
            return
        if keySymbol==0xff08 and selfValue.korean and not controlKey and selfValue.HangulComposer.backspace(): return
        if controlKey and shiftKey and keySymbol in (ord('t'),ord('T')):
            selfValue.send(bytes([30,2,1,0,0,0,0])); return
        if keySymbol==0xffc3: selfValue.send(bytes([30,2,2,0,0,0,0])); return
        if keySymbol==0xffc9: selfValue.send(bytes([30,2,3,0,0,0,0])); return
        if controlKey and shiftKey and keySymbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            selfValue.send(selfValue.clipboardValue); return
        specialKey = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if keySymbol in specialKey: selfValue.send(specialKey[keySymbol]); return
        characterEncoding = keySymbol & 0xffffff if keySymbol & 0xff000000 == 0x01000000 else keySymbol
        if characterEncoding > 0x10ffff or 0xd800 <= characterEncoding <= 0xdfff or keySymbol >= 0xff00 and keySymbol < 0x1000000: return
        if controlKey and 0x40 <= characterEncoding <= 0x7f: selfValue.send(bytes([characterEncoding & 31])); return
        if characterEncoding < 32: return
        if selfValue.korean and selfValue.modifierKey & {0xffea,0xfe03,0xff7e} and not controlKey and hasattr(selfValue.HangulComposer, 'profile'):
            if selfValue.HangulComposer.feedKey(chr(characterEncoding), altgr=True): return
        leadingPart = b'\x1b' if selfValue.modifierKey & {0xffe9, 0xffea} else b''
        if selfValue.korean and not controlKey and not leadingPart and 32<=characterEncoding<127:
            characterData=chr(characterEncoding).upper() if shiftKey else chr(characterEncoding)
            if selfValue.HangulComposer.feedKey(characterData): return
        selfValue.send(leadingPart + chr(characterEncoding).encode('utf-8'))


class connectDesktop:
    def __init__(selfValue, process):
        selfValue.process=process; selfValue.lockValue=threading.Lock(); selfValue.preparationComplete=False; selfValue.terminal=False; selfValue.initialScreen=False; selfValue.isClosed=False

    def send(selfValue, data):
        if not data or selfValue.isClosed: return
        with selfValue.lockValue:
            try: selfValue.process.stdin.write(data); selfValue.process.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def serialIo(selfValue):
        endingPart=b''
        try:
            while True:
                data=selfValue.process.stdout.read(4096)
                if not data: break
                sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
                endingPart=(endingPart+data)[-8192:]
                opened=endingPart.rfind(b'TERMINAL READY'); isClosed=endingPart.rfind(b'TERMINAL CLOSED'); drawingScreen=endingPart.rfind(b'GUI READY:'); hasExited=endingPart.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(opened,isClosed,drawingScreen,hasExited)>=0:
                    selfValue.terminal=opened>max(isClosed,drawingScreen,hasExited)
                    selfValue.initialScreen=drawingScreen>max(opened,isClosed,hasExited)
                if not selfValue.preparationComplete and b'jkoros-native> ' in endingPart:
                    selfValue.preparationComplete=True; selfValue.send(b'terminal\n')
        finally: selfValue.isClosed=True

    def client(selfValue, client, path):
        serverValue=socket.socket(socket.AF_UNIX); serverValue.settimeout(10); client.settimeout(10)
        keyboardEntry=Keyboard(selfValue.send,lambda korean:selfValue.send(bytes([30,3,int(korean),0,0,0,0])))
        previousButtons=0
        try:
            serverValue.connect(str(path))
            # initialState 협상은 순서대로 끝낸다. afterValue Output 가닥만 클라이언트에 쓴다.
            client.sendall(exactValue(serverValue,12))
            versionNumber=exactValue(client,12)
            if versionNumber not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            serverValue.sendall(versionNumber)
            itemCount=exactValue(serverValue,1);client.sendall(itemCount+exactValue(serverValue,itemCount[0]))
            security=exactValue(client,1)
            if security!=b'\x01': raise ValueError('unexpected security type')
            serverValue.sendall(security)
            if versionNumber==b'RFB 003.008\n':client.sendall(exactValue(serverValue,4))
            serverValue.sendall(exactValue(client,1))
            initialValue=exactValue(serverValue,24)
            client.sendall(initialValue+exactValue(serverValue,struct.unpack('>I',initialValue[20:])[0]))
            pixelBytes=initialValue[4]//8;pointerSupported=False
            client.settimeout(None);serverValue.settimeout(None)
            def output():
                try:
                    while True:
                        categoryValue=exactValue(serverValue,1)[0]
                        if categoryValue==0:
                            headValue=exactValue(serverValue,3);entryCount=struct.unpack('>H',headValue[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 remoteValue 포인터의 중복을 피한다.
                            hiddenValue=pointerSupported
                            if hiddenValue:client.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            client.sendall(bytes([categoryValue])+headValue)
                            for _ in range(entryCount):
                                rectangle=exactValue(serverValue,12);horizontalPosition,verticalPosition,widthSpan,heightValue,encodingValue=struct.unpack('>HHHHi',rectangle)
                                if encodingValue!=0:raise ValueError('unexpected framebuffer encoding: '+str(encodingValue))
                                client.sendall(rectangle)
                                remainderData=widthSpan*heightValue*pixelBytes
                                while remainderData:
                                    data=exactValue(serverValue,min(remainderData,65536));client.sendall(data);remainderData-=len(data)
                        elif categoryValue==1:
                            headValue=exactValue(serverValue,5);itemCount=struct.unpack('>H',headValue[3:])[0]
                            client.sendall(bytes([categoryValue])+headValue+exactValue(serverValue,itemCount*6))
                        elif categoryValue==2:client.sendall(bytes([categoryValue]))
                        elif categoryValue==3:
                            headValue=exactValue(serverValue,7);itemCount=struct.unpack('>I',headValue[3:])[0]
                            if itemCount>1048576:raise ValueError('server clipboard too large')
                            client.sendall(bytes([categoryValue])+headValue+exactValue(serverValue,itemCount))
                        else:raise ValueError('unexpected RFB server message: '+str(categoryValue))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:client.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            worker=threading.Thread(target=output,daemon=True);worker.start()
            while not selfValue.isClosed:
                categoryValue=exactValue(client,1)[0]
                if categoryValue==4:
                    bodyText=exactValue(client,7); keyboardEntry.pressedValue(bodyText[0]!=0,struct.unpack('>I',bodyText[3:])[0]); continue
                if categoryValue==255:
                    bodyText=exactValue(client,11)
                    if bodyText[0]!=0: raise ValueError('unsupported QEMU input extension')
                    keyboardEntry.pressedValue(struct.unpack('>H',bodyText[1:3])[0]!=0,struct.unpack('>I',bodyText[3:7])[0]); continue
                if categoryValue==5:
                    bodyText=exactValue(client,5); buttons,xCoordinate,yCoordinate=struct.unpack('>BHH',bodyText)
                    isPressed=buttons&~previousButtons; previousButtons=buttons
                    if isPressed: keyboardEntry.HangulComposer.commitComposition()
                    if isPressed&1 and selfValue.initialScreen and 64<=xCoordinate<576 and 112<=yCoordinate<372:
                        lookupIndex=(yCoordinate-112)//52
                        if (yCoordinate-112)%52<40 and lookupIndex<5: selfValue.send(bytes([ord('1')+lookupIndex]))
                    else: selfValue.send(bytes([30,1,buttons,xCoordinate&255,xCoordinate>>8,yCoordinate&255,yCoordinate>>8]))
                    continue
                if categoryValue==6:
                    bodyText=exactValue(client,7); lengthValue=struct.unpack('>i',bodyText[3:])[0]
                    if abs(lengthValue)>65536: raise ValueError('clipboard too large')
                    text=exactValue(client,abs(lengthValue))
                    if lengthValue>=0:
                        try: keyboardEntry.clipboardValue=text.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: keyboardEntry.clipboardValue=text.decode('latin-1').encode('utf-8')
                        keyboardEntry.clipboardValue=keyboardEntry.clipboardValue[:65536].decode('utf-8','ignore').encode('utf-8')
                    serverValue.sendall(bytes([categoryValue])+bodyText+text); continue
                if categoryValue==0:
                    bodyText=exactValue(client,19)
                    if bodyText[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    pixelBytes=bodyText[3]//8
                elif categoryValue==2:
                    bodyText=exactValue(client,3); entryCount=struct.unpack('>H',bodyText[1:])[0]
                    if entryCount>512: raise ValueError('too many encodings')
                    encodedValues=struct.unpack('>'+str(entryCount)+'i',exactValue(client,entryCount*4))
                    pointerSupported=-239 in encodedValues
                    # 로컬 Screen 중계는 defaultValue Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    bodyText=struct.pack('>BHi',0,1,0)
                elif categoryValue in (3,150): bodyText=exactValue(client,9)
                elif categoryValue==248:
                    bodyText=exactValue(client,8)
                    if bodyText[7]>64: raise ValueError('fence too large')
                    bodyText+=exactValue(client,bodyText[7])
                elif categoryValue==250: bodyText=exactValue(client,3)
                elif categoryValue==251:
                    bodyText=exactValue(client,7)
                    if bodyText[5]>16: raise ValueError('too many screens')
                    bodyText+=exactValue(client,bodyText[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(categoryValue))
                serverValue.sendall(bytes([categoryValue])+bodyText)
        except (OSError,EOFError,ValueError) as error:
            if str(error): print('VNC client:',error,file=sys.stderr,flush=True)
        finally:
            for socketValue in (client,serverValue):
                try: socketValue.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                socketValue.close()


def runDesktop(portNumber=5902, network=False, fileTransferPortNumber=2121, forwardingRules=(), resolutionValue=(640, 480), guestAddress=None, hostAddress='127.0.0.1'):
    with ExitStack() as resources, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as workingPath:
        networkBridgeEntry = None
        if network:
            from networkBridge import networkBridge
            networkBridgeEntry = resources.enter_context(networkBridge(fileTransferPortNumber, forwardingRules, guestAddress=guestAddress, hostAddress=hostAddress))
        path=Path(workingPath)/'display.sock'
        with socket.socket() as receivePort:
            receivePort.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            receivePort.bind(('127.0.0.1',portNumber)); receivePort.listen(1); receivePort.settimeout(.2)
            vncPort=receivePort.getsockname()[1]
            if networkBridgeEntry and (vncPort==fileTransferPortNumber or 50000<=vncPort<=50007 or any(NetworkABI=='tcp' and Host==vncPort for NetworkABI,Host,_ in networkBridgeEntry.forwardingRules)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            process=subprocess.Popen(command(resolutionValue)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(path)]+(networkBridgeEntry.forwardedArgument() if networkBridgeEntry else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            bridge=connectDesktop(process); reader=threading.Thread(target=bridge.serialIo,daemon=True); reader.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(receivePort.getsockname()[1]),flush=True)
            if networkBridgeEntry: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(hostAddress,fileTransferPortNumber),flush=True)
            def terminate(signalNumber,executionFrame): raise KeyboardInterrupt()
            previous=signal.signal(signal.SIGTERM,terminate)
            processingTask=None; interrupted=False
            try:
                while process.poll() is None:
                    try: client,_=receivePort.accept()
                    except socket.timeout: continue
                    if processingTask is not None and processingTask.is_alive(): client.close(); continue
                    if not path.exists(): client.close(); continue
                    processingTask=threading.Thread(target=bridge.client,args=(client,path),daemon=True); processingTask.start()
            except KeyboardInterrupt: interrupted=True
            finally:
                bridge.isClosed=True
                if networkBridgeEntry: networkBridgeEntry.pauseEvent.set()
                if process.poll() is None:
                    process.terminate()
                    try: process.wait(timeout=5)
                    except subprocess.TimeoutExpired: process.kill(); process.wait()
                reader.join(timeout=2); process.stdin.close(); process.stdout.close(); signal.signal(signal.SIGTERM,previous)
            if networkBridgeEntry and networkBridgeEntry.error: raise RuntimeError('network bridge: '+networkBridgeEntry.error)
            return 0 if interrupted else process.returncode


if __name__=='__main__':
    from executeCommand import readResolution
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--port',type=int,default=5902)
    parser.add_argument('--resolution',type=readResolution,default=(640,480))
    parser.add_argument('--network',action='store_true'); parser.add_argument('--ftp-port',type=int,default=2121)
    parser.add_argument('--forward',action='append',default=[])
    argumentArray=parser.parse_args()
    if argumentArray.forward and not argumentArray.network: parser.error('--forward requires --network')
    raise SystemExit(runDesktop(argumentArray.port,network=argumentArray.network,fileTransferPortNumber=argumentArray.ftp_port,forwardingRules=argumentArray.forward,resolutionValue=argumentArray.resolution))
