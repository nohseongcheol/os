#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, kër_xëyma 입력은 자체 xoox_xëyma UART로 전달한다. localhost 전용, 단일 Saytu_doxinu_ordinateur_xëyma 클라이언트.
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
from def_ndigel import ndigel
from local_input import create


def 정확한값(소켓, tolluwaay):
    mbir = bytearray()
    while len(mbir) < tolluwaay:
        조각 = 소켓.recv(tolluwaay - len(mbir))
        if not 조각: raise EOFError()
        mbir.extend(조각)
    return bytes(mbir)


class arafukaay:
    def __init__(자신, Yónnee, 입력방식알림=None):
        자신.바이트전송 = Yónnee; 자신.këru_soppali = set(); 자신.Ndencandi_xëyma = b''
        자신.한글조합기 = create(Yónnee, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.jalantu_kër = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def Yónnee(자신, mbir):
        자신.한글조합기.조합확정()
        자신.바이트전송(mbir)

    def jalantu_anam(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, kër_sembóol):
        if kër_sembóol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.këru_soppali.add(kër_sembóol)
            else: 자신.këru_soppali.discard(kër_sembóol)
            return
        if not 누르는중:
            자신.jalantu_kër.discard(kër_sembóol)
            return
        CTRL = bool(자신.këru_soppali & {0xffe3, 0xffe4})
        caabi_Maj = bool(자신.këru_soppali & {0xffe1, 0xffe2})
        if CTRL and caabi_Maj and kër_sembóol in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if kër_sembóol in (32,0xff0d):
                try:
                    xëyma=int(자신.유니코드입력,16)
                    if 32<=xëyma<=0x10ffff and not 0xd800<=xëyma<=0xdfff: 자신.Yónnee(chr(xëyma).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif kër_sembóol==0xff1b: 자신.유니코드입력=None
            elif kër_sembóol==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif kër_sembóol<128 and chr(kër_sembóol) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(kër_sembóol)
            return
        if kër_sembóol in (0xff31,0xffc6) or kër_sembóol==32 and caabi_Maj and not CTRL:
            if kër_sembóol not in 자신.jalantu_kër: 자신.jalantu_anam()
            자신.jalantu_kër.add(kër_sembóol)
            return
        if kër_sembóol==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and caabi_Maj and kër_sembóol in (ord('t'),ord('T')):
            자신.Yónnee(bytes([30,2,1,0,0,0,0])); return
        if kër_sembóol==0xffc3: 자신.Yónnee(bytes([30,2,2,0,0,0,0])); return
        if kër_sembóol==0xffc9: 자신.Yónnee(bytes([30,2,3,0,0,0,0])); return
        if CTRL and caabi_Maj and kër_sembóol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.Yónnee(자신.Ndencandi_xëyma); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if kër_sembóol in 특수글쇠: 자신.Yónnee(특수글쇠[kër_sembóol]); return
        Araf_nëbbin_ci_lim = kër_sembóol & 0xffffff if kër_sembóol & 0xff000000 == 0x01000000 else kër_sembóol
        if Araf_nëbbin_ci_lim > 0x10ffff or 0xd800 <= Araf_nëbbin_ci_lim <= 0xdfff or kër_sembóol >= 0xff00 and kër_sembóol < 0x1000000: return
        if CTRL and 0x40 <= Araf_nëbbin_ci_lim <= 0x7f: 자신.Yónnee(bytes([Araf_nëbbin_ci_lim & 31])); return
        if Araf_nëbbin_ci_lim < 32: return
        if 자신.한글여부 and 자신.këru_soppali & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.yebeef_kër(chr(Araf_nëbbin_ci_lim), altgr=True): return
        앞부분 = b'\x1b' if 자신.këru_soppali & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=Araf_nëbbin_ci_lim<127:
            Araf_mbir=chr(Araf_nëbbin_ci_lim).upper() if caabi_Maj else chr(Araf_nëbbin_ci_lim)
            if 자신.한글조합기.yebeef_kër(Araf_mbir): return
        자신.Yónnee(앞부분 + chr(Araf_nëbbin_ci_lim).encode('utf-8'))


class JOKKOO_Biro:
    def __init__(자신, yokkute):
        자신.yokkute=yokkute; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def Yónnee(자신, mbir):
        if not mbir or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.yokkute.stdin.write(mbir); 자신.yokkute.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                mbir=자신.yokkute.stdout.read(4096)
                if not mbir: break
                sys.stdout.buffer.write(mbir); sys.stdout.buffer.flush()
                끝부분=(끝부분+mbir)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.Yónnee(b'terminal\n')
        finally: 자신.닫힘=True

    def lëkkalekat(자신, lëkkalekat, Yoonu_jëmale):
        dëggu_xëyma=socket.socket(socket.AF_UNIX); dëggu_xëyma.settimeout(10); lëkkalekat.settimeout(10)
        arafukaay_dugal_xabaar=arafukaay(자신.Yónnee,lambda 한글여부:자신.Yónnee(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            dëggu_xëyma.connect(str(Yoonu_jëmale))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            lëkkalekat.sendall(정확한값(dëggu_xëyma,12))
            판번호=정확한값(lëkkalekat,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            dëggu_xëyma.sendall(판번호)
            개수=정확한값(dëggu_xëyma,1);lëkkalekat.sendall(개수+정확한값(dëggu_xëyma,개수[0]))
            kaarànge=정확한값(lëkkalekat,1)
            if kaarànge!=b'\x01': raise ValueError('unexpected security type')
            dëggu_xëyma.sendall(kaarànge)
            if 판번호==b'RFB 003.008\n':lëkkalekat.sendall(정확한값(dëggu_xëyma,4))
            dëggu_xëyma.sendall(정확한값(lëkkalekat,1))
            초기값=정확한값(dëggu_xëyma,24)
            lëkkalekat.sendall(초기값+정확한값(dëggu_xëyma,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            lëkkalekat.settimeout(None);dëggu_xëyma.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        ngiir_xëyma=정확한값(dëggu_xëyma,1)[0]
                        if ngiir_xëyma==0:
                            머리=정확한값(dëggu_xëyma,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 lu_soree_xëyma 포인터의 중복을 피한다.
                            nëmbu_xëyma=포인터지원
                            if nëmbu_xëyma:lëkkalekat.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            lëkkalekat.sendall(bytes([ngiir_xëyma])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(dëggu_xëyma,12);가로,세로,폭,높이,nëbbin_ci_lim_xëyma=struct.unpack('>HHHHi',사각형)
                                if nëbbin_ci_lim_xëyma!=0:raise ValueError('unexpected framebuffer encoding: '+str(nëbbin_ci_lim_xëyma))
                                lëkkalekat.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    mbir=정확한값(dëggu_xëyma,min(남음,65536));lëkkalekat.sendall(mbir);남음-=len(mbir)
                        elif ngiir_xëyma==1:
                            머리=정확한값(dëggu_xëyma,5);개수=struct.unpack('>H',머리[3:])[0]
                            lëkkalekat.sendall(bytes([ngiir_xëyma])+머리+정확한값(dëggu_xëyma,개수*6))
                        elif ngiir_xëyma==2:lëkkalekat.sendall(bytes([ngiir_xëyma]))
                        elif ngiir_xëyma==3:
                            머리=정확한값(dëggu_xëyma,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            lëkkalekat.sendall(bytes([ngiir_xëyma])+머리+정확한값(dëggu_xëyma,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(ngiir_xëyma))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:lëkkalekat.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                ngiir_xëyma=정확한값(lëkkalekat,1)[0]
                if ngiir_xëyma==4:
                    yaxub_mool=정확한값(lëkkalekat,7); arafukaay_dugal_xabaar.누름값(yaxub_mool[0]!=0,struct.unpack('>I',yaxub_mool[3:])[0]); continue
                if ngiir_xëyma==255:
                    yaxub_mool=정확한값(lëkkalekat,11)
                    if yaxub_mool[0]!=0: raise ValueError('unsupported QEMU input extension')
                    arafukaay_dugal_xabaar.누름값(struct.unpack('>H',yaxub_mool[1:3])[0]!=0,struct.unpack('>I',yaxub_mool[3:7])[0]); continue
                if ngiir_xëyma==5:
                    yaxub_mool=정확한값(lëkkalekat,5); 단추들,rëddu_iks_yi,세로좌표=struct.unpack('>BHH',yaxub_mool)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: arafukaay_dugal_xabaar.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=rëddu_iks_yi<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.Yónnee(bytes([ord('1')+색인]))
                    else: 자신.Yónnee(bytes([30,1,단추들,rëddu_iks_yi&255,rëddu_iks_yi>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if ngiir_xëyma==6:
                    yaxub_mool=정확한값(lëkkalekat,7); diir_xëyma=struct.unpack('>i',yaxub_mool[3:])[0]
                    if abs(diir_xëyma)>65536: raise ValueError('clipboard too large')
                    Tekst=정확한값(lëkkalekat,abs(diir_xëyma))
                    if diir_xëyma>=0:
                        try: arafukaay_dugal_xabaar.Ndencandi_xëyma=Tekst.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: arafukaay_dugal_xabaar.Ndencandi_xëyma=Tekst.decode('latin-1').encode('utf-8')
                        arafukaay_dugal_xabaar.Ndencandi_xëyma=arafukaay_dugal_xabaar.Ndencandi_xëyma[:65536].decode('utf-8','ignore').encode('utf-8')
                    dëggu_xëyma.sendall(bytes([ngiir_xëyma])+yaxub_mool+Tekst); continue
                if ngiir_xëyma==0:
                    yaxub_mool=정확한값(lëkkalekat,19)
                    if yaxub_mool[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=yaxub_mool[3]//8
                elif ngiir_xëyma==2:
                    yaxub_mool=정확한값(lëkkalekat,3); 항목수=struct.unpack('>H',yaxub_mool[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(lëkkalekat,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 xayma_bi_teew Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    yaxub_mool=struct.pack('>BHi',0,1,0)
                elif ngiir_xëyma in (3,150): yaxub_mool=정확한값(lëkkalekat,9)
                elif ngiir_xëyma==248:
                    yaxub_mool=정확한값(lëkkalekat,8)
                    if yaxub_mool[7]>64: raise ValueError('fence too large')
                    yaxub_mool+=정확한값(lëkkalekat,yaxub_mool[7])
                elif ngiir_xëyma==250: yaxub_mool=정확한값(lëkkalekat,3)
                elif ngiir_xëyma==251:
                    yaxub_mool=정확한값(lëkkalekat,7)
                    if yaxub_mool[5]>16: raise ValueError('too many screens')
                    yaxub_mool+=정확한값(lëkkalekat,yaxub_mool[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ngiir_xëyma))
                dëggu_xëyma.sendall(bytes([ngiir_xëyma])+yaxub_mool)
        except (OSError,EOFError,ValueError) as njumte:
            if str(njumte): print('VNC client:',njumte,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (lëkkalekat,dëggu_xëyma):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def daw_Biro(접속번호=5902, mbaal=False, 파일전송접속번호=2121, 전달규칙들=(), Sottal_xëyma=(640, 480), gan_dëkkuwaay=None, dalal_dëkkuwaay='127.0.0.1'):
    with ExitStack() as costéef_yi, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        mbaal_poŋ_dugal_xabaar = None
        if mbaal:
            from mbaal_poŋ import mbaal_poŋ
            mbaal_poŋ_dugal_xabaar = costéef_yi.enter_context(mbaal_poŋ(파일전송접속번호, 전달규칙들, gan_dëkkuwaay=gan_dëkkuwaay, dalal_dëkkuwaay=dalal_dëkkuwaay))
        Yoonu_jëmale=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if mbaal_poŋ_dugal_xabaar and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and dalal==원격화면접속번호 for 통신규약,dalal,_ in mbaal_poŋ_dugal_xabaar.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            yokkute=subprocess.Popen(ndigel(Sottal_xëyma)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Yoonu_jëmale)]+(mbaal_poŋ_dugal_xabaar.전달인수() if mbaal_poŋ_dugal_xabaar else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            poŋ=JOKKOO_Biro(yokkute); jangkat=threading.Thread(target=poŋ.직렬입출력,daemon=True); jangkat.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if mbaal_poŋ_dugal_xabaar: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(dalal_dëkkuwaay,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while yokkute.poll() is None:
                    try: lëkkalekat,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): lëkkalekat.close(); continue
                    if not Yoonu_jëmale.exists(): lëkkalekat.close(); continue
                    처리작업=threading.Thread(target=poŋ.lëkkalekat,args=(lëkkalekat,Yoonu_jëmale),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                poŋ.닫힘=True
                if mbaal_poŋ_dugal_xabaar: mbaal_poŋ_dugal_xabaar.Ajandi_xewxew.set()
                if yokkute.poll() is None:
                    yokkute.terminate()
                    try: yokkute.wait(timeout=5)
                    except subprocess.TimeoutExpired: yokkute.kill(); yokkute.wait()
                jangkat.join(timeout=2); yokkute.stdin.close(); yokkute.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if mbaal_poŋ_dugal_xabaar and mbaal_poŋ_dugal_xabaar.njumte: raise RuntimeError('network bridge: '+mbaal_poŋ_dugal_xabaar.njumte)
            return 0 if 가로채기됨 else yokkute.returncode


if __name__=='__main__':
    from def_ndigel import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    Tegtal_TABLO=인수해석기.parse_args()
    if Tegtal_TABLO.forward and not Tegtal_TABLO.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(daw_Biro(Tegtal_TABLO.port,mbaal=Tegtal_TABLO.network,파일전송접속번호=Tegtal_TABLO.ftp_port,전달규칙들=Tegtal_TABLO.forward,Sottal_xëyma=Tegtal_TABLO.resolution))
