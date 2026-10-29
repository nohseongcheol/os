#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, bọ́tìnnì_iye 입력은 자체 kánẹ́ẹ̀lì_iye UART로 전달한다. localhost 전용, 단일 ìdarí_iye 클라이언트.
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
from ṣiṣẹ́_àṣẹ import Àṣẹ
from local_input import create


def 정확한값(소켓, Ìwọ̀n):
    détà = bytearray()
    while len(détà) < Ìwọ̀n:
        조각 = 소켓.recv(Ìwọ̀n - len(détà))
        if not 조각: raise EOFError()
        détà.extend(조각)
    return bytes(détà)


class àtẹ_ìtẹ̀wé:
    def __init__(자신, í_meèlì, 입력방식알림=None):
        자신.바이트전송 = í_meèlì; 자신.bọ́tìnnì_aṣàtúnṣe = set(); 자신.aka_ọlọ́pọ́n_iye = b''
        자신.한글조합기 = create(í_meèlì, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.ṣèpapòdà_bọ́tìnnì = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def í_meèlì(자신, détà):
        자신.한글조합기.조합확정()
        자신.바이트전송(détà)

    def ṣèpapòdà_móòdù(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, bọ́tìnnì_àmì):
        if bọ́tìnnì_àmì in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.bọ́tìnnì_aṣàtúnṣe.add(bọ́tìnnì_àmì)
            else: 자신.bọ́tìnnì_aṣàtúnṣe.discard(bọ́tìnnì_àmì)
            return
        if not 누르는중:
            자신.ṣèpapòdà_bọ́tìnnì.discard(bọ́tìnnì_àmì)
            return
        CTRL = bool(자신.bọ́tìnnì_aṣàtúnṣe & {0xffe3, 0xffe4})
        bọ́tìnnì_SHIFT = bool(자신.bọ́tìnnì_aṣàtúnṣe & {0xffe1, 0xffe2})
        if CTRL and bọ́tìnnì_SHIFT and bọ́tìnnì_àmì in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if bọ́tìnnì_àmì in (32,0xff0d):
                try:
                    iye=int(자신.유니코드입력,16)
                    if 32<=iye<=0x10ffff and not 0xd800<=iye<=0xdfff: 자신.í_meèlì(chr(iye).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif bọ́tìnnì_àmì==0xff1b: 자신.유니코드입력=None
            elif bọ́tìnnì_àmì==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif bọ́tìnnì_àmì<128 and chr(bọ́tìnnì_àmì) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(bọ́tìnnì_àmì)
            return
        if bọ́tìnnì_àmì in (0xff31,0xffc6) or bọ́tìnnì_àmì==32 and bọ́tìnnì_SHIFT and not CTRL:
            if bọ́tìnnì_àmì not in 자신.ṣèpapòdà_bọ́tìnnì: 자신.ṣèpapòdà_móòdù()
            자신.ṣèpapòdà_bọ́tìnnì.add(bọ́tìnnì_àmì)
            return
        if bọ́tìnnì_àmì==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and bọ́tìnnì_SHIFT and bọ́tìnnì_àmì in (ord('t'),ord('T')):
            자신.í_meèlì(bytes([30,2,1,0,0,0,0])); return
        if bọ́tìnnì_àmì==0xffc3: 자신.í_meèlì(bytes([30,2,2,0,0,0,0])); return
        if bọ́tìnnì_àmì==0xffc9: 자신.í_meèlì(bytes([30,2,3,0,0,0,0])); return
        if CTRL and bọ́tìnnì_SHIFT and bọ́tìnnì_àmì in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.í_meèlì(자신.aka_ọlọ́pọ́n_iye); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if bọ́tìnnì_àmì in 특수글쇠: 자신.í_meèlì(특수글쇠[bọ́tìnnì_àmì]); return
        ẹyọ_ọ̀rọ̀_pípàrokò = bọ́tìnnì_àmì & 0xffffff if bọ́tìnnì_àmì & 0xff000000 == 0x01000000 else bọ́tìnnì_àmì
        if ẹyọ_ọ̀rọ̀_pípàrokò > 0x10ffff or 0xd800 <= ẹyọ_ọ̀rọ̀_pípàrokò <= 0xdfff or bọ́tìnnì_àmì >= 0xff00 and bọ́tìnnì_àmì < 0x1000000: return
        if CTRL and 0x40 <= ẹyọ_ọ̀rọ̀_pípàrokò <= 0x7f: 자신.í_meèlì(bytes([ẹyọ_ọ̀rọ̀_pípàrokò & 31])); return
        if ẹyọ_ọ̀rọ̀_pípàrokò < 32: return
        if 자신.한글여부 and 자신.bọ́tìnnì_aṣàtúnṣe & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.àkóónú_níṣókí_bọ́tìnnì(chr(ẹyọ_ọ̀rọ̀_pípàrokò), altgr=True): return
        앞부분 = b'\x1b' if 자신.bọ́tìnnì_aṣàtúnṣe & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=ẹyọ_ọ̀rọ̀_pípàrokò<127:
            ẹyọ_ọ̀rọ̀_détà=chr(ẹyọ_ọ̀rọ̀_pípàrokò).upper() if bọ́tìnnì_SHIFT else chr(ẹyọ_ọ̀rọ̀_pípàrokò)
            if 자신.한글조합기.àkóónú_níṣókí_bọ́tìnnì(ẹyọ_ọ̀rọ̀_détà): return
        자신.í_meèlì(앞부분 + chr(ẹyọ_ọ̀rọ̀_pípàrokò).encode('utf-8'))


class SOMỌ́_àtẹ_iṣẹ́:
    def __init__(자신, Ìlànà):
        자신.Ìlànà=Ìlànà; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def í_meèlì(자신, détà):
        if not détà or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Ìlànà.stdin.write(détà); 자신.Ìlànà.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                détà=자신.Ìlànà.stdout.read(4096)
                if not détà: break
                sys.stdout.buffer.write(détà); sys.stdout.buffer.flush()
                끝부분=(끝부분+détà)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.í_meèlì(b'terminal\n')
        finally: 자신.닫힘=True

    def aṣojú(자신, aṣojú, ọ̀nà):
        apèsè_iye=socket.socket(socket.AF_UNIX); apèsè_iye.settimeout(10); aṣojú.settimeout(10)
        àtẹ_ìtẹ̀wé_ìgbéwọlé=àtẹ_ìtẹ̀wé(자신.í_meèlì,lambda 한글여부:자신.í_meèlì(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            apèsè_iye.connect(str(ọ̀nà))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            aṣojú.sendall(정확한값(apèsè_iye,12))
            판번호=정확한값(aṣojú,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            apèsè_iye.sendall(판번호)
            개수=정확한값(apèsè_iye,1);aṣojú.sendall(개수+정확한값(apèsè_iye,개수[0]))
            Ààbò=정확한값(aṣojú,1)
            if Ààbò!=b'\x01': raise ValueError('unexpected security type')
            apèsè_iye.sendall(Ààbò)
            if 판번호==b'RFB 003.008\n':aṣojú.sendall(정확한값(apèsè_iye,4))
            apèsè_iye.sendall(정확한값(aṣojú,1))
            초기값=정확한값(apèsè_iye,24)
            aṣojú.sendall(초기값+정확한값(apèsè_iye,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            aṣojú.settimeout(None);apèsè_iye.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        ìsọ̀rí_iye=정확한값(apèsè_iye,1)[0]
                        if ìsọ̀rí_iye==0:
                            머리=정확한값(apèsè_iye,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 Ìjìnnà_iye 포인터의 중복을 피한다.
                            tó_farasin_iye=포인터지원
                            if tó_farasin_iye:aṣojú.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            aṣojú.sendall(bytes([ìsọ̀rí_iye])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(apèsè_iye,12);가로,세로,폭,높이,pípàrokò_iye=struct.unpack('>HHHHi',사각형)
                                if pípàrokò_iye!=0:raise ValueError('unexpected framebuffer encoding: '+str(pípàrokò_iye))
                                aṣojú.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    détà=정확한값(apèsè_iye,min(남음,65536));aṣojú.sendall(détà);남음-=len(détà)
                        elif ìsọ̀rí_iye==1:
                            머리=정확한값(apèsè_iye,5);개수=struct.unpack('>H',머리[3:])[0]
                            aṣojú.sendall(bytes([ìsọ̀rí_iye])+머리+정확한값(apèsè_iye,개수*6))
                        elif ìsọ̀rí_iye==2:aṣojú.sendall(bytes([ìsọ̀rí_iye]))
                        elif ìsọ̀rí_iye==3:
                            머리=정확한값(apèsè_iye,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            aṣojú.sendall(bytes([ìsọ̀rí_iye])+머리+정확한값(apèsè_iye,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(ìsọ̀rí_iye))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:aṣojú.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                ìsọ̀rí_iye=정확한값(aṣojú,1)[0]
                if ìsọ̀rí_iye==4:
                    kókó_ọ̀rọ̀_ìkọ=정확한값(aṣojú,7); àtẹ_ìtẹ̀wé_ìgbéwọlé.누름값(kókó_ọ̀rọ̀_ìkọ[0]!=0,struct.unpack('>I',kókó_ọ̀rọ̀_ìkọ[3:])[0]); continue
                if ìsọ̀rí_iye==255:
                    kókó_ọ̀rọ̀_ìkọ=정확한값(aṣojú,11)
                    if kókó_ọ̀rọ̀_ìkọ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    àtẹ_ìtẹ̀wé_ìgbéwọlé.누름값(struct.unpack('>H',kókó_ọ̀rọ̀_ìkọ[1:3])[0]!=0,struct.unpack('>I',kókó_ọ̀rọ̀_ìkọ[3:7])[0]); continue
                if ìsọ̀rí_iye==5:
                    kókó_ọ̀rọ̀_ìkọ=정확한값(aṣojú,5); 단추들,ibi_ìtọ́kasí_x,세로좌표=struct.unpack('>BHH',kókó_ọ̀rọ̀_ìkọ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: àtẹ_ìtẹ̀wé_ìgbéwọlé.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=ibi_ìtọ́kasí_x<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.í_meèlì(bytes([ord('1')+색인]))
                    else: 자신.í_meèlì(bytes([30,1,단추들,ibi_ìtọ́kasí_x&255,ibi_ìtọ́kasí_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if ìsọ̀rí_iye==6:
                    kókó_ọ̀rọ̀_ìkọ=정확한값(aṣojú,7); gígùn_iye=struct.unpack('>i',kókó_ọ̀rọ̀_ìkọ[3:])[0]
                    if abs(gígùn_iye)>65536: raise ValueError('clipboard too large')
                    SMS=정확한값(aṣojú,abs(gígùn_iye))
                    if gígùn_iye>=0:
                        try: àtẹ_ìtẹ̀wé_ìgbéwọlé.aka_ọlọ́pọ́n_iye=SMS.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: àtẹ_ìtẹ̀wé_ìgbéwọlé.aka_ọlọ́pọ́n_iye=SMS.decode('latin-1').encode('utf-8')
                        àtẹ_ìtẹ̀wé_ìgbéwọlé.aka_ọlọ́pọ́n_iye=àtẹ_ìtẹ̀wé_ìgbéwọlé.aka_ọlọ́pọ́n_iye[:65536].decode('utf-8','ignore').encode('utf-8')
                    apèsè_iye.sendall(bytes([ìsọ̀rí_iye])+kókó_ọ̀rọ̀_ìkọ+SMS); continue
                if ìsọ̀rí_iye==0:
                    kókó_ọ̀rọ̀_ìkọ=정확한값(aṣojú,19)
                    if kókó_ọ̀rọ̀_ìkọ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=kókó_ọ̀rọ̀_ìkọ[3]//8
                elif ìsọ̀rí_iye==2:
                    kókó_ọ̀rọ̀_ìkọ=정확한값(aṣojú,3); 항목수=struct.unpack('>H',kókó_ọ̀rọ̀_ìkọ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(aṣojú,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 àdáwọ̀ Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    kókó_ọ̀rọ̀_ìkọ=struct.pack('>BHi',0,1,0)
                elif ìsọ̀rí_iye in (3,150): kókó_ọ̀rọ̀_ìkọ=정확한값(aṣojú,9)
                elif ìsọ̀rí_iye==248:
                    kókó_ọ̀rọ̀_ìkọ=정확한값(aṣojú,8)
                    if kókó_ọ̀rọ̀_ìkọ[7]>64: raise ValueError('fence too large')
                    kókó_ọ̀rọ̀_ìkọ+=정확한값(aṣojú,kókó_ọ̀rọ̀_ìkọ[7])
                elif ìsọ̀rí_iye==250: kókó_ọ̀rọ̀_ìkọ=정확한값(aṣojú,3)
                elif ìsọ̀rí_iye==251:
                    kókó_ọ̀rọ̀_ìkọ=정확한값(aṣojú,7)
                    if kókó_ọ̀rọ̀_ìkọ[5]>16: raise ValueError('too many screens')
                    kókó_ọ̀rọ̀_ìkọ+=정확한값(aṣojú,kókó_ọ̀rọ̀_ìkọ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ìsọ̀rí_iye))
                apèsè_iye.sendall(bytes([ìsọ̀rí_iye])+kókó_ọ̀rọ̀_ìkọ)
        except (OSError,EOFError,ValueError) as àṣìṣe:
            if str(àṣìṣe): print('VNC client:',àṣìṣe,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (aṣojú,apèsè_iye):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ṣiṣẹ́_àtẹ_iṣẹ́(접속번호=5902, Alásopọ̀=False, 파일전송접속번호=2121, 전달규칙들=(), ìmúsí_àwòrán_iye=(640, 480), àlejò_àdírẹ́ẹ̀sì=None, olùpèsè_àdírẹ́ẹ̀sì='127.0.0.1'):
    with ExitStack() as àwọn_ohun_èlò, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Alásopọ̀_afará_ìgbéwọlé = None
        if Alásopọ̀:
            from Alásopọ̀_afará import Alásopọ̀_afará
            Alásopọ̀_afará_ìgbéwọlé = àwọn_ohun_èlò.enter_context(Alásopọ̀_afará(파일전송접속번호, 전달규칙들, àlejò_àdírẹ́ẹ̀sì=àlejò_àdírẹ́ẹ̀sì, olùpèsè_àdírẹ́ẹ̀sì=olùpèsè_àdírẹ́ẹ̀sì))
        ọ̀nà=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Alásopọ̀_afará_ìgbéwọlé and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and olùpèsè==원격화면접속번호 for 통신규약,olùpèsè,_ in Alásopọ̀_afará_ìgbéwọlé.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Ìlànà=subprocess.Popen(Àṣẹ(ìmúsí_àwòrán_iye)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ọ̀nà)]+(Alásopọ̀_afará_ìgbéwọlé.전달인수() if Alásopọ̀_afará_ìgbéwọlé else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            afará=SOMỌ́_àtẹ_iṣẹ́(Ìlànà); akàwé=threading.Thread(target=afará.직렬입출력,daemon=True); akàwé.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Alásopọ̀_afará_ìgbéwọlé: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(olùpèsè_àdírẹ́ẹ̀sì,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Ìlànà.poll() is None:
                    try: aṣojú,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): aṣojú.close(); continue
                    if not ọ̀nà.exists(): aṣojú.close(); continue
                    처리작업=threading.Thread(target=afará.aṣojú,args=(aṣojú,ọ̀nà),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                afará.닫힘=True
                if Alásopọ̀_afará_ìgbéwọlé: Alásopọ̀_afará_ìgbéwọlé.dúró_díẹ̀_ìgbéṣẹ̀.set()
                if Ìlànà.poll() is None:
                    Ìlànà.terminate()
                    try: Ìlànà.wait(timeout=5)
                    except subprocess.TimeoutExpired: Ìlànà.kill(); Ìlànà.wait()
                akàwé.join(timeout=2); Ìlànà.stdin.close(); Ìlànà.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Alásopọ̀_afará_ìgbéwọlé and Alásopọ̀_afará_ìgbéwọlé.àṣìṣe: raise RuntimeError('network bridge: '+Alásopọ̀_afará_ìgbéwọlé.àṣìṣe)
            return 0 if 가로채기됨 else Ìlànà.returncode


if __name__=='__main__':
    from ṣiṣẹ́_àṣẹ import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    ágúmẹ́ntì_ÀRÉÈ=인수해석기.parse_args()
    if ágúmẹ́ntì_ÀRÉÈ.forward and not ágúmẹ́ntì_ÀRÉÈ.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(ṣiṣẹ́_àtẹ_iṣẹ́(ágúmẹ́ntì_ÀRÉÈ.port,Alásopọ̀=ágúmẹ́ntì_ÀRÉÈ.network,파일전송접속번호=ágúmẹ́ntì_ÀRÉÈ.ftp_port,전달규칙들=ágúmẹ́ntì_ÀRÉÈ.forward,ìmúsí_àwòrán_iye=ágúmẹ́ntì_ÀRÉÈ.resolution))
