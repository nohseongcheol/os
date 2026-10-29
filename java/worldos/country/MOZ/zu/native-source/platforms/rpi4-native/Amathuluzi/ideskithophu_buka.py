#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, inkomba_inani 입력은 자체 ikhenela_inani UART로 전달한다. localhost 전용, 단일 isilawuli_inani 클라이언트.
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
from yenza_umyalo import Umlayelo
from local_input import create


def 정확한값(소켓, Ubungako):
    imininingwane = bytearray()
    while len(imininingwane) < Ubungako:
        조각 = 소켓.recv(Ubungako - len(imininingwane))
        if not 조각: raise EOFError()
        imininingwane.extend(조각)
    return bytes(imininingwane)


class ikhibhodi:
    def __init__(자신, Thumela, 입력방식알림=None):
        자신.바이트전송 = Thumela; 자신.Inkinobho_yokuguquguqula = set(); 자신.ibhodi_yokunamathisela_inani = b''
        자신.한글조합기 = create(Thumela, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.guqulela_kokunye_inkomba = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def Thumela(자신, imininingwane):
        자신.한글조합기.조합확정()
        자신.바이트전송(imininingwane)

    def guqulela_kokunye_inqubo(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, inkomba_uphawu):
        if inkomba_uphawu in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.Inkinobho_yokuguquguqula.add(inkomba_uphawu)
            else: 자신.Inkinobho_yokuguquguqula.discard(inkomba_uphawu)
            return
        if not 누르는중:
            자신.guqulela_kokunye_inkomba.discard(inkomba_uphawu)
            return
        i_CTRL = bool(자신.Inkinobho_yokuguquguqula & {0xffe3, 0xffe4})
        inkinobho_ye_SHIFT = bool(자신.Inkinobho_yokuguquguqula & {0xffe1, 0xffe2})
        if i_CTRL and inkinobho_ye_SHIFT and inkomba_uphawu in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if inkomba_uphawu in (32,0xff0d):
                try:
                    inani=int(자신.유니코드입력,16)
                    if 32<=inani<=0x10ffff and not 0xd800<=inani<=0xdfff: 자신.Thumela(chr(inani).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif inkomba_uphawu==0xff1b: 자신.유니코드입력=None
            elif inkomba_uphawu==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif inkomba_uphawu<128 and chr(inkomba_uphawu) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(inkomba_uphawu)
            return
        if inkomba_uphawu in (0xff31,0xffc6) or inkomba_uphawu==32 and inkinobho_ye_SHIFT and not i_CTRL:
            if inkomba_uphawu not in 자신.guqulela_kokunye_inkomba: 자신.guqulela_kokunye_inqubo()
            자신.guqulela_kokunye_inkomba.add(inkomba_uphawu)
            return
        if inkomba_uphawu==0xff08 and 자신.한글여부 and not i_CTRL and 자신.한글조합기.앞글자지우기(): return
        if i_CTRL and inkinobho_ye_SHIFT and inkomba_uphawu in (ord('t'),ord('T')):
            자신.Thumela(bytes([30,2,1,0,0,0,0])); return
        if inkomba_uphawu==0xffc3: 자신.Thumela(bytes([30,2,2,0,0,0,0])); return
        if inkomba_uphawu==0xffc9: 자신.Thumela(bytes([30,2,3,0,0,0,0])); return
        if i_CTRL and inkinobho_ye_SHIFT and inkomba_uphawu in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.Thumela(자신.ibhodi_yokunamathisela_inani); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if inkomba_uphawu in 특수글쇠: 자신.Thumela(특수글쇠[inkomba_uphawu]); return
        uhlamvusimo_ukubhala_ngokufihla = inkomba_uphawu & 0xffffff if inkomba_uphawu & 0xff000000 == 0x01000000 else inkomba_uphawu
        if uhlamvusimo_ukubhala_ngokufihla > 0x10ffff or 0xd800 <= uhlamvusimo_ukubhala_ngokufihla <= 0xdfff or inkomba_uphawu >= 0xff00 and inkomba_uphawu < 0x1000000: return
        if i_CTRL and 0x40 <= uhlamvusimo_ukubhala_ngokufihla <= 0x7f: 자신.Thumela(bytes([uhlamvusimo_ukubhala_ngokufihla & 31])); return
        if uhlamvusimo_ukubhala_ngokufihla < 32: return
        if 자신.한글여부 and 자신.Inkinobho_yokuguquguqula & {0xffea,0xfe03,0xff7e} and not i_CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.isifunzo_inkomba(chr(uhlamvusimo_ukubhala_ngokufihla), altgr=True): return
        앞부분 = b'\x1b' if 자신.Inkinobho_yokuguquguqula & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not i_CTRL and not 앞부분 and 32<=uhlamvusimo_ukubhala_ngokufihla<127:
            uhlamvusimo_imininingwane=chr(uhlamvusimo_ukubhala_ngokufihla).upper() if inkinobho_ye_SHIFT else chr(uhlamvusimo_ukubhala_ngokufihla)
            if 자신.한글조합기.isifunzo_inkomba(uhlamvusimo_imininingwane): return
        자신.Thumela(앞부분 + chr(uhlamvusimo_ukubhala_ngokufihla).encode('utf-8'))


class xhuma_ideskithophu:
    def __init__(자신, Inqubo):
        자신.Inqubo=Inqubo; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def Thumela(자신, imininingwane):
        if not imininingwane or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Inqubo.stdin.write(imininingwane); 자신.Inqubo.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                imininingwane=자신.Inqubo.stdout.read(4096)
                if not imininingwane: break
                sys.stdout.buffer.write(imininingwane); sys.stdout.buffer.flush()
                끝부분=(끝부분+imininingwane)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.Thumela(b'terminal\n')
        finally: 자신.닫힘=True

    def iklayenti(자신, iklayenti, Indlela_2):
        Iseva_inani=socket.socket(socket.AF_UNIX); Iseva_inani.settimeout(10); iklayenti.settimeout(10)
        ikhibhodi_okufakwayo=ikhibhodi(자신.Thumela,lambda 한글여부:자신.Thumela(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            Iseva_inani.connect(str(Indlela_2))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            iklayenti.sendall(정확한값(Iseva_inani,12))
            판번호=정확한값(iklayenti,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            Iseva_inani.sendall(판번호)
            개수=정확한값(Iseva_inani,1);iklayenti.sendall(개수+정확한값(Iseva_inani,개수[0]))
            ukuphepha=정확한값(iklayenti,1)
            if ukuphepha!=b'\x01': raise ValueError('unexpected security type')
            Iseva_inani.sendall(ukuphepha)
            if 판번호==b'RFB 003.008\n':iklayenti.sendall(정확한값(Iseva_inani,4))
            Iseva_inani.sendall(정확한값(iklayenti,1))
            초기값=정확한값(Iseva_inani,24)
            iklayenti.sendall(초기값+정확한값(Iseva_inani,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            iklayenti.settimeout(None);Iseva_inani.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        umunxa_inani=정확한값(Iseva_inani,1)[0]
                        if umunxa_inani==0:
                            머리=정확한값(Iseva_inani,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 kude_inani 포인터의 중복을 피한다.
                            kufihliwe_inani=포인터지원
                            if kufihliwe_inani:iklayenti.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            iklayenti.sendall(bytes([umunxa_inani])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(Iseva_inani,12);가로,세로,폭,높이,ukubhala_ngokufihla_inani=struct.unpack('>HHHHi',사각형)
                                if ukubhala_ngokufihla_inani!=0:raise ValueError('unexpected framebuffer encoding: '+str(ukubhala_ngokufihla_inani))
                                iklayenti.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    imininingwane=정확한값(Iseva_inani,min(남음,65536));iklayenti.sendall(imininingwane);남음-=len(imininingwane)
                        elif umunxa_inani==1:
                            머리=정확한값(Iseva_inani,5);개수=struct.unpack('>H',머리[3:])[0]
                            iklayenti.sendall(bytes([umunxa_inani])+머리+정확한값(Iseva_inani,개수*6))
                        elif umunxa_inani==2:iklayenti.sendall(bytes([umunxa_inani]))
                        elif umunxa_inani==3:
                            머리=정확한값(Iseva_inani,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            iklayenti.sendall(bytes([umunxa_inani])+머리+정확한값(Iseva_inani,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(umunxa_inani))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:iklayenti.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                umunxa_inani=정확한값(iklayenti,1)[0]
                if umunxa_inani==4:
                    umzimba_wombhalo=정확한값(iklayenti,7); ikhibhodi_okufakwayo.누름값(umzimba_wombhalo[0]!=0,struct.unpack('>I',umzimba_wombhalo[3:])[0]); continue
                if umunxa_inani==255:
                    umzimba_wombhalo=정확한값(iklayenti,11)
                    if umzimba_wombhalo[0]!=0: raise ValueError('unsupported QEMU input extension')
                    ikhibhodi_okufakwayo.누름값(struct.unpack('>H',umzimba_wombhalo[1:3])[0]!=0,struct.unpack('>I',umzimba_wombhalo[3:7])[0]); continue
                if umunxa_inani==5:
                    umzimba_wombhalo=정확한값(iklayenti,5); 단추들,okuxhumanisa_u_x,세로좌표=struct.unpack('>BHH',umzimba_wombhalo)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: ikhibhodi_okufakwayo.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=okuxhumanisa_u_x<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.Thumela(bytes([ord('1')+색인]))
                    else: 자신.Thumela(bytes([30,1,단추들,okuxhumanisa_u_x&255,okuxhumanisa_u_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if umunxa_inani==6:
                    umzimba_wombhalo=정확한값(iklayenti,7); ubude_inani=struct.unpack('>i',umzimba_wombhalo[3:])[0]
                    if abs(ubude_inani)>65536: raise ValueError('clipboard too large')
                    Itekisi=정확한값(iklayenti,abs(ubude_inani))
                    if ubude_inani>=0:
                        try: ikhibhodi_okufakwayo.ibhodi_yokunamathisela_inani=Itekisi.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: ikhibhodi_okufakwayo.ibhodi_yokunamathisela_inani=Itekisi.decode('latin-1').encode('utf-8')
                        ikhibhodi_okufakwayo.ibhodi_yokunamathisela_inani=ikhibhodi_okufakwayo.ibhodi_yokunamathisela_inani[:65536].decode('utf-8','ignore').encode('utf-8')
                    Iseva_inani.sendall(bytes([umunxa_inani])+umzimba_wombhalo+Itekisi); continue
                if umunxa_inani==0:
                    umzimba_wombhalo=정확한값(iklayenti,19)
                    if umzimba_wombhalo[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=umzimba_wombhalo[3]//8
                elif umunxa_inani==2:
                    umzimba_wombhalo=정확한값(iklayenti,3); 항목수=struct.unpack('>H',umzimba_wombhalo[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(iklayenti,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 inani_elimisiwe Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    umzimba_wombhalo=struct.pack('>BHi',0,1,0)
                elif umunxa_inani in (3,150): umzimba_wombhalo=정확한값(iklayenti,9)
                elif umunxa_inani==248:
                    umzimba_wombhalo=정확한값(iklayenti,8)
                    if umzimba_wombhalo[7]>64: raise ValueError('fence too large')
                    umzimba_wombhalo+=정확한값(iklayenti,umzimba_wombhalo[7])
                elif umunxa_inani==250: umzimba_wombhalo=정확한값(iklayenti,3)
                elif umunxa_inani==251:
                    umzimba_wombhalo=정확한값(iklayenti,7)
                    if umzimba_wombhalo[5]>16: raise ValueError('too many screens')
                    umzimba_wombhalo+=정확한값(iklayenti,umzimba_wombhalo[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(umunxa_inani))
                Iseva_inani.sendall(bytes([umunxa_inani])+umzimba_wombhalo)
        except (OSError,EOFError,ValueError) as Iphutha:
            if str(Iphutha): print('VNC client:',Iphutha,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (iklayenti,Iseva_inani):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def sebenzisa_ideskithophu(접속번호=5902, iNethiwekhi=False, 파일전송접속번호=2121, 전달규칙들=(), ukucaca_inani=(640, 480), isivakashi_ikheli=None, singatha_ikheli='127.0.0.1'):
    with ExitStack() as izinsiza, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        iNethiwekhi_ibhuloho_okufakwayo = None
        if iNethiwekhi:
            from iNethiwekhi_ibhuloho import iNethiwekhi_ibhuloho
            iNethiwekhi_ibhuloho_okufakwayo = izinsiza.enter_context(iNethiwekhi_ibhuloho(파일전송접속번호, 전달규칙들, isivakashi_ikheli=isivakashi_ikheli, singatha_ikheli=singatha_ikheli))
        Indlela_2=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if iNethiwekhi_ibhuloho_okufakwayo and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and singatha==원격화면접속번호 for 통신규약,singatha,_ in iNethiwekhi_ibhuloho_okufakwayo.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Inqubo=subprocess.Popen(Umlayelo(ukucaca_inani)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Indlela_2)]+(iNethiwekhi_ibhuloho_okufakwayo.전달인수() if iNethiwekhi_ibhuloho_okufakwayo else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ibhuloho=xhuma_ideskithophu(Inqubo); umfundi=threading.Thread(target=ibhuloho.직렬입출력,daemon=True); umfundi.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if iNethiwekhi_ibhuloho_okufakwayo: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(singatha_ikheli,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Inqubo.poll() is None:
                    try: iklayenti,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): iklayenti.close(); continue
                    if not Indlela_2.exists(): iklayenti.close(); continue
                    처리작업=threading.Thread(target=ibhuloho.iklayenti,args=(iklayenti,Indlela_2),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ibhuloho.닫힘=True
                if iNethiwekhi_ibhuloho_okufakwayo: iNethiwekhi_ibhuloho_okufakwayo.phumuza_isikhashana_isigameko.set()
                if Inqubo.poll() is None:
                    Inqubo.terminate()
                    try: Inqubo.wait(timeout=5)
                    except subprocess.TimeoutExpired: Inqubo.kill(); Inqubo.wait()
                umfundi.join(timeout=2); Inqubo.stdin.close(); Inqubo.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if iNethiwekhi_ibhuloho_okufakwayo and iNethiwekhi_ibhuloho_okufakwayo.Iphutha: raise RuntimeError('network bridge: '+iNethiwekhi_ibhuloho_okufakwayo.Iphutha)
            return 0 if 가로채기됨 else Inqubo.returncode


if __name__=='__main__':
    from yenza_umyalo import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    i_agumenti_AMALUNGU_AFANAYO=인수해석기.parse_args()
    if i_agumenti_AMALUNGU_AFANAYO.forward and not i_agumenti_AMALUNGU_AFANAYO.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(sebenzisa_ideskithophu(i_agumenti_AMALUNGU_AFANAYO.port,iNethiwekhi=i_agumenti_AMALUNGU_AFANAYO.network,파일전송접속번호=i_agumenti_AMALUNGU_AFANAYO.ftp_port,전달규칙들=i_agumenti_AMALUNGU_AFANAYO.forward,ukucaca_inani=i_agumenti_AMALUNGU_AFANAYO.resolution))
