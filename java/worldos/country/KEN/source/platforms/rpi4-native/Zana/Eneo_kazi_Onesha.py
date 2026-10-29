#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Kitufe_thamani 입력은 자체 kiini_thamani_0611a8a8 UART로 전달한다. localhost 전용, 단일 udhibiti_thamani 클라이언트.
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
from tekeleza_amri import amri
from local_input import create


def 정확한값(소켓, panga_ukubwa):
    data = bytearray()
    while len(data) < panga_ukubwa:
        조각 = 소켓.recv(panga_ukubwa - len(data))
        if not 조각: raise EOFError()
        data.extend(조각)
    return bytes(data)


class kibodi:
    def __init__(자신, tuma, 입력방식알림=None):
        자신.바이트전송 = tuma; 자신.kibonye_rekebishi = set(); 자신.ubao_nakili_thamani = b''
        자신.한글조합기 = create(tuma, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.badili_Kitufe = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def tuma(자신, data):
        자신.한글조합기.조합확정()
        자신.바이트전송(data)

    def badili_hali_tumizi(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Kitufe_ishara):
        if Kitufe_ishara in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.kibonye_rekebishi.add(Kitufe_ishara)
            else: 자신.kibonye_rekebishi.discard(Kitufe_ishara)
            return
        if not 누르는중:
            자신.badili_Kitufe.discard(Kitufe_ishara)
            return
        Ctrl = bool(자신.kibonye_rekebishi & {0xffe3, 0xffe4})
        kibonye_SHIFT = bool(자신.kibonye_rekebishi & {0xffe1, 0xffe2})
        if Ctrl and kibonye_SHIFT and Kitufe_ishara in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Kitufe_ishara in (32,0xff0d):
                try:
                    thamani=int(자신.유니코드입력,16)
                    if 32<=thamani<=0x10ffff and not 0xd800<=thamani<=0xdfff: 자신.tuma(chr(thamani).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Kitufe_ishara==0xff1b: 자신.유니코드입력=None
            elif Kitufe_ishara==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Kitufe_ishara<128 and chr(Kitufe_ishara) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Kitufe_ishara)
            return
        if Kitufe_ishara in (0xff31,0xffc6) or Kitufe_ishara==32 and kibonye_SHIFT and not Ctrl:
            if Kitufe_ishara not in 자신.badili_Kitufe: 자신.badili_hali_tumizi()
            자신.badili_Kitufe.add(Kitufe_ishara)
            return
        if Kitufe_ishara==0xff08 and 자신.한글여부 and not Ctrl and 자신.한글조합기.앞글자지우기(): return
        if Ctrl and kibonye_SHIFT and Kitufe_ishara in (ord('t'),ord('T')):
            자신.tuma(bytes([30,2,1,0,0,0,0])); return
        if Kitufe_ishara==0xffc3: 자신.tuma(bytes([30,2,2,0,0,0,0])); return
        if Kitufe_ishara==0xffc9: 자신.tuma(bytes([30,2,3,0,0,0,0])); return
        if Ctrl and kibonye_SHIFT and Kitufe_ishara in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.tuma(자신.ubao_nakili_thamani); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Kitufe_ishara in 특수글쇠: 자신.tuma(특수글쇠[Kitufe_ishara]); return
        kibambo_usimbaji = Kitufe_ishara & 0xffffff if Kitufe_ishara & 0xff000000 == 0x01000000 else Kitufe_ishara
        if kibambo_usimbaji > 0x10ffff or 0xd800 <= kibambo_usimbaji <= 0xdfff or Kitufe_ishara >= 0xff00 and Kitufe_ishara < 0x1000000: return
        if Ctrl and 0x40 <= kibambo_usimbaji <= 0x7f: 자신.tuma(bytes([kibambo_usimbaji & 31])); return
        if kibambo_usimbaji < 32: return
        if 자신.한글여부 and 자신.kibonye_rekebishi & {0xffea,0xfe03,0xff7e} and not Ctrl and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.mlisho_Kitufe(chr(kibambo_usimbaji), altgr=True): return
        앞부분 = b'\x1b' if 자신.kibonye_rekebishi & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not Ctrl and not 앞부분 and 32<=kibambo_usimbaji<127:
            kibambo_data=chr(kibambo_usimbaji).upper() if kibonye_SHIFT else chr(kibambo_usimbaji)
            if 자신.한글조합기.mlisho_Kitufe(kibambo_data): return
        자신.tuma(앞부분 + chr(kibambo_usimbaji).encode('utf-8'))


class UNGANISHA_Eneo_kazi:
    def __init__(자신, Mchakato):
        자신.Mchakato=Mchakato; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def tuma(자신, data):
        if not data or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Mchakato.stdin.write(data); 자신.Mchakato.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                data=자신.Mchakato.stdout.read(4096)
                if not data: break
                sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
                끝부분=(끝부분+data)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.tuma(b'terminal\n')
        finally: 자신.닫힘=True

    def teja(자신, teja, njia):
        seva_thamani=socket.socket(socket.AF_UNIX); seva_thamani.settimeout(10); teja.settimeout(10)
        kibodi_ingizo=kibodi(자신.tuma,lambda 한글여부:자신.tuma(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            seva_thamani.connect(str(njia))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            teja.sendall(정확한값(seva_thamani,12))
            판번호=정확한값(teja,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            seva_thamani.sendall(판번호)
            개수=정확한값(seva_thamani,1);teja.sendall(개수+정확한값(seva_thamani,개수[0]))
            Usalama=정확한값(teja,1)
            if Usalama!=b'\x01': raise ValueError('unexpected security type')
            seva_thamani.sendall(Usalama)
            if 판번호==b'RFB 003.008\n':teja.sendall(정확한값(seva_thamani,4))
            seva_thamani.sendall(정확한값(teja,1))
            초기값=정확한값(seva_thamani,24)
            teja.sendall(초기값+정확한값(seva_thamani,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            teja.settimeout(None);seva_thamani.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        kategoria_thamani=정확한값(seva_thamani,1)[0]
                        if kategoria_thamani==0:
                            머리=정확한값(seva_thamani,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 kwa_mbali_thamani 포인터의 중복을 피한다.
                            fiche_thamani=포인터지원
                            if fiche_thamani:teja.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            teja.sendall(bytes([kategoria_thamani])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(seva_thamani,12);가로,세로,폭,높이,usimbaji_thamani=struct.unpack('>HHHHi',사각형)
                                if usimbaji_thamani!=0:raise ValueError('unexpected framebuffer encoding: '+str(usimbaji_thamani))
                                teja.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    data=정확한값(seva_thamani,min(남음,65536));teja.sendall(data);남음-=len(data)
                        elif kategoria_thamani==1:
                            머리=정확한값(seva_thamani,5);개수=struct.unpack('>H',머리[3:])[0]
                            teja.sendall(bytes([kategoria_thamani])+머리+정확한값(seva_thamani,개수*6))
                        elif kategoria_thamani==2:teja.sendall(bytes([kategoria_thamani]))
                        elif kategoria_thamani==3:
                            머리=정확한값(seva_thamani,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            teja.sendall(bytes([kategoria_thamani])+머리+정확한값(seva_thamani,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(kategoria_thamani))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:teja.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                kategoria_thamani=정확한값(teja,1)[0]
                if kategoria_thamani==4:
                    Matini_kiini=정확한값(teja,7); kibodi_ingizo.누름값(Matini_kiini[0]!=0,struct.unpack('>I',Matini_kiini[3:])[0]); continue
                if kategoria_thamani==255:
                    Matini_kiini=정확한값(teja,11)
                    if Matini_kiini[0]!=0: raise ValueError('unsupported QEMU input extension')
                    kibodi_ingizo.누름값(struct.unpack('>H',Matini_kiini[1:3])[0]!=0,struct.unpack('>I',Matini_kiini[3:7])[0]); continue
                if kategoria_thamani==5:
                    Matini_kiini=정확한값(teja,5); 단추들,jira_x,Kitufe_cha_Y_kiratibu=struct.unpack('>BHH',Matini_kiini)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: kibodi_ingizo.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=jira_x<576 and 112<=Kitufe_cha_Y_kiratibu<372:
                        색인=(Kitufe_cha_Y_kiratibu-112)//52
                        if (Kitufe_cha_Y_kiratibu-112)%52<40 and 색인<5: 자신.tuma(bytes([ord('1')+색인]))
                    else: 자신.tuma(bytes([30,1,단추들,jira_x&255,jira_x>>8,Kitufe_cha_Y_kiratibu&255,Kitufe_cha_Y_kiratibu>>8]))
                    continue
                if kategoria_thamani==6:
                    Matini_kiini=정확한값(teja,7); urefu_thamani=struct.unpack('>i',Matini_kiini[3:])[0]
                    if abs(urefu_thamani)>65536: raise ValueError('clipboard too large')
                    SMS=정확한값(teja,abs(urefu_thamani))
                    if urefu_thamani>=0:
                        try: kibodi_ingizo.ubao_nakili_thamani=SMS.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: kibodi_ingizo.ubao_nakili_thamani=SMS.decode('latin-1').encode('utf-8')
                        kibodi_ingizo.ubao_nakili_thamani=kibodi_ingizo.ubao_nakili_thamani[:65536].decode('utf-8','ignore').encode('utf-8')
                    seva_thamani.sendall(bytes([kategoria_thamani])+Matini_kiini+SMS); continue
                if kategoria_thamani==0:
                    Matini_kiini=정확한값(teja,19)
                    if Matini_kiini[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=Matini_kiini[3]//8
                elif kategoria_thamani==2:
                    Matini_kiini=정확한값(teja,3); 항목수=struct.unpack('>H',Matini_kiini[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(teja,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 hali_ya_chaguo_msingi Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    Matini_kiini=struct.pack('>BHi',0,1,0)
                elif kategoria_thamani in (3,150): Matini_kiini=정확한값(teja,9)
                elif kategoria_thamani==248:
                    Matini_kiini=정확한값(teja,8)
                    if Matini_kiini[7]>64: raise ValueError('fence too large')
                    Matini_kiini+=정확한값(teja,Matini_kiini[7])
                elif kategoria_thamani==250: Matini_kiini=정확한값(teja,3)
                elif kategoria_thamani==251:
                    Matini_kiini=정확한값(teja,7)
                    if Matini_kiini[5]>16: raise ValueError('too many screens')
                    Matini_kiini+=정확한값(teja,Matini_kiini[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(kategoria_thamani))
                seva_thamani.sendall(bytes([kategoria_thamani])+Matini_kiini)
        except (OSError,EOFError,ValueError) as kosa:
            if str(kosa): print('VNC client:',kosa,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (teja,seva_thamani):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def endesha_Eneo_kazi(namba_ya_kituo=5902, Mtandao=False, faili_hamisha_namba_ya_kituo=2121, 전달규칙들=(), mwonekano_thamani=(640, 480), mgeni_anwani=None, mwenyeji_anwani='127.0.0.1'):
    with ExitStack() as Rasilimali, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Mtandao_daraja_ingizo = None
        if Mtandao:
            from Mtandao_daraja import Mtandao_daraja
            Mtandao_daraja_ingizo = Rasilimali.enter_context(Mtandao_daraja(faili_hamisha_namba_ya_kituo, 전달규칙들, mgeni_anwani=mgeni_anwani, mwenyeji_anwani=mwenyeji_anwani))
        njia=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',namba_ya_kituo)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Mtandao_daraja_ingizo and (원격화면접속번호==faili_hamisha_namba_ya_kituo or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and mwenyeji==원격화면접속번호 for 통신규약,mwenyeji,_ in Mtandao_daraja_ingizo.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Mchakato=subprocess.Popen(amri(mwonekano_thamani)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(njia)]+(Mtandao_daraja_ingizo.전달인수() if Mtandao_daraja_ingizo else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            daraja=UNGANISHA_Eneo_kazi(Mchakato); msomaji=threading.Thread(target=daraja.직렬입출력,daemon=True); msomaji.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Mtandao_daraja_ingizo: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(mwenyeji_anwani,faili_hamisha_namba_ya_kituo),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Mchakato.poll() is None:
                    try: teja,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): teja.close(); continue
                    if not njia.exists(): teja.close(); continue
                    처리작업=threading.Thread(target=daraja.teja,args=(teja,njia),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                daraja.닫힘=True
                if Mtandao_daraja_ingizo: Mtandao_daraja_ingizo.sitisha_tukio.set()
                if Mchakato.poll() is None:
                    Mchakato.terminate()
                    try: Mchakato.wait(timeout=5)
                    except subprocess.TimeoutExpired: Mchakato.kill(); Mchakato.wait()
                msomaji.join(timeout=2); Mchakato.stdin.close(); Mchakato.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Mtandao_daraja_ingizo and Mtandao_daraja_ingizo.kosa: raise RuntimeError('network bridge: '+Mtandao_daraja_ingizo.kosa)
            return 0 if 가로채기됨 else Mchakato.returncode


if __name__=='__main__':
    from tekeleza_amri import 해상도읽기
    kichanganuzi=argparse.ArgumentParser(description=__doc__); kichanganuzi.add_argument('--port',type=int,default=5902)
    kichanganuzi.add_argument('--resolution',type=해상도읽기,default=(640,480))
    kichanganuzi.add_argument('--network',action='store_true'); kichanganuzi.add_argument('--ftp-port',type=int,default=2121)
    kichanganuzi.add_argument('--forward',action='append',default=[])
    hoja_ARRAY=kichanganuzi.parse_args()
    if hoja_ARRAY.forward and not hoja_ARRAY.network: kichanganuzi.error('--forward requires --network')
    raise SystemExit(endesha_Eneo_kazi(hoja_ARRAY.port,Mtandao=hoja_ARRAY.network,faili_hamisha_namba_ya_kituo=hoja_ARRAY.ftp_port,전달규칙들=hoja_ARRAY.forward,mwonekano_thamani=hoja_ARRAY.resolution))
