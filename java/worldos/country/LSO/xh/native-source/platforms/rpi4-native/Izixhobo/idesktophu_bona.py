#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, iqhosha_ixabiso 입력은 자체 ikheneli_ixabiso UART로 전달한다. localhost 전용, 단일 isilawuli_ixabiso 클라이언트.
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
from ukwenza_umyalelo import Umyalelo
from local_input import create


def 정확한값(소켓, Ubukhulu):
    iingcombolo = bytearray()
    while len(iingcombolo) < Ubukhulu:
        조각 = 소켓.recv(Ubukhulu - len(iingcombolo))
        if not 조각: raise EOFError()
        iingcombolo.extend(조각)
    return bytes(iingcombolo)


class ikhibhodi:
    def __init__(자신, thumela, 입력방식알림=None):
        자신.바이트전송 = thumela; 자신.iqhosha_elisisilungisi = set(); 자신.indawo_yogcino_ixabiso = b''
        자신.한글조합기 = create(thumela, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.tshintshela_iqhosha = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def thumela(자신, iingcombolo):
        자신.한글조합기.조합확정()
        자신.바이트전송(iingcombolo)

    def tshintshela_imo(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, iqhosha_isimboli):
        if iqhosha_isimboli in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.iqhosha_elisisilungisi.add(iqhosha_isimboli)
            else: 자신.iqhosha_elisisilungisi.discard(iqhosha_isimboli)
            return
        if not 누르는중:
            자신.tshintshela_iqhosha.discard(iqhosha_isimboli)
            return
        i_CTRL = bool(자신.iqhosha_elisisilungisi & {0xffe3, 0xffe4})
        iqhosha_le_SHIFT = bool(자신.iqhosha_elisisilungisi & {0xffe1, 0xffe2})
        if i_CTRL and iqhosha_le_SHIFT and iqhosha_isimboli in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if iqhosha_isimboli in (32,0xff0d):
                try:
                    ixabiso=int(자신.유니코드입력,16)
                    if 32<=ixabiso<=0x10ffff and not 0xd800<=ixabiso<=0xdfff: 자신.thumela(chr(ixabiso).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif iqhosha_isimboli==0xff1b: 자신.유니코드입력=None
            elif iqhosha_isimboli==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif iqhosha_isimboli<128 and chr(iqhosha_isimboli) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(iqhosha_isimboli)
            return
        if iqhosha_isimboli in (0xff31,0xffc6) or iqhosha_isimboli==32 and iqhosha_le_SHIFT and not i_CTRL:
            if iqhosha_isimboli not in 자신.tshintshela_iqhosha: 자신.tshintshela_imo()
            자신.tshintshela_iqhosha.add(iqhosha_isimboli)
            return
        if iqhosha_isimboli==0xff08 and 자신.한글여부 and not i_CTRL and 자신.한글조합기.앞글자지우기(): return
        if i_CTRL and iqhosha_le_SHIFT and iqhosha_isimboli in (ord('t'),ord('T')):
            자신.thumela(bytes([30,2,1,0,0,0,0])); return
        if iqhosha_isimboli==0xffc3: 자신.thumela(bytes([30,2,2,0,0,0,0])); return
        if iqhosha_isimboli==0xffc9: 자신.thumela(bytes([30,2,3,0,0,0,0])); return
        if i_CTRL and iqhosha_le_SHIFT and iqhosha_isimboli in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.thumela(자신.indawo_yogcino_ixabiso); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if iqhosha_isimboli in 특수글쇠: 자신.thumela(특수글쇠[iqhosha_isimboli]); return
        ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi = iqhosha_isimboli & 0xffffff if iqhosha_isimboli & 0xff000000 == 0x01000000 else iqhosha_isimboli
        if ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi > 0x10ffff or 0xd800 <= ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi <= 0xdfff or iqhosha_isimboli >= 0xff00 and iqhosha_isimboli < 0x1000000: return
        if i_CTRL and 0x40 <= ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi <= 0x7f: 자신.thumela(bytes([ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi & 31])); return
        if ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi < 32: return
        if 자신.한글여부 and 자신.iqhosha_elisisilungisi & {0xffea,0xfe03,0xff7e} and not i_CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ufido_iqhosha(chr(ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi), altgr=True): return
        앞부분 = b'\x1b' if 자신.iqhosha_elisisilungisi & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not i_CTRL and not 앞부분 and 32<=ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi<127:
            ikharakhtha_iingcombolo=chr(ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi).upper() if iqhosha_le_SHIFT else chr(ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi)
            if 자신.한글조합기.ufido_iqhosha(ikharakhtha_iingcombolo): return
        자신.thumela(앞부분 + chr(ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi).encode('utf-8'))


class I_Connect_idesktophu:
    def __init__(자신, Inkqubo):
        자신.Inkqubo=Inkqubo; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.i_Terminal=False; 자신.시작화면=False; 자신.닫힘=False

    def thumela(자신, iingcombolo):
        if not iingcombolo or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Inkqubo.stdin.write(iingcombolo); 자신.Inkqubo.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                iingcombolo=자신.Inkqubo.stdout.read(4096)
                if not iingcombolo: break
                sys.stdout.buffer.write(iingcombolo); sys.stdout.buffer.flush()
                끝부분=(끝부분+iingcombolo)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.i_Terminal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.thumela(b'terminal\n')
        finally: 자신.닫힘=True

    def iklayenti(자신, iklayenti, INDLELA):
        iseva_ixabiso=socket.socket(socket.AF_UNIX); iseva_ixabiso.settimeout(10); iklayenti.settimeout(10)
        ikhibhodi_ufako_nkcukacha=ikhibhodi(자신.thumela,lambda 한글여부:자신.thumela(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            iseva_ixabiso.connect(str(INDLELA))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            iklayenti.sendall(정확한값(iseva_ixabiso,12))
            판번호=정확한값(iklayenti,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            iseva_ixabiso.sendall(판번호)
            개수=정확한값(iseva_ixabiso,1);iklayenti.sendall(개수+정확한값(iseva_ixabiso,개수[0]))
            Ukhuseleko=정확한값(iklayenti,1)
            if Ukhuseleko!=b'\x01': raise ValueError('unexpected security type')
            iseva_ixabiso.sendall(Ukhuseleko)
            if 판번호==b'RFB 003.008\n':iklayenti.sendall(정확한값(iseva_ixabiso,4))
            iseva_ixabiso.sendall(정확한값(iklayenti,1))
            초기값=정확한값(iseva_ixabiso,24)
            iklayenti.sendall(초기값+정확한값(iseva_ixabiso,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            iklayenti.settimeout(None);iseva_ixabiso.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        udidi_ixabiso=정확한값(iseva_ixabiso,1)[0]
                        if udidi_ixabiso==0:
                            머리=정확한값(iseva_ixabiso,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 kude_ixabiso 포인터의 중복을 피한다.
                            efihliweyo_ixabiso=포인터지원
                            if efihliweyo_ixabiso:iklayenti.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            iklayenti.sendall(bytes([udidi_ixabiso])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(iseva_ixabiso,12);가로,세로,폭,높이,ujiko_nkcukacha_zibe_ziikhowudi_ixabiso=struct.unpack('>HHHHi',사각형)
                                if ujiko_nkcukacha_zibe_ziikhowudi_ixabiso!=0:raise ValueError('unexpected framebuffer encoding: '+str(ujiko_nkcukacha_zibe_ziikhowudi_ixabiso))
                                iklayenti.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    iingcombolo=정확한값(iseva_ixabiso,min(남음,65536));iklayenti.sendall(iingcombolo);남음-=len(iingcombolo)
                        elif udidi_ixabiso==1:
                            머리=정확한값(iseva_ixabiso,5);개수=struct.unpack('>H',머리[3:])[0]
                            iklayenti.sendall(bytes([udidi_ixabiso])+머리+정확한값(iseva_ixabiso,개수*6))
                        elif udidi_ixabiso==2:iklayenti.sendall(bytes([udidi_ixabiso]))
                        elif udidi_ixabiso==3:
                            머리=정확한값(iseva_ixabiso,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            iklayenti.sendall(bytes([udidi_ixabiso])+머리+정확한값(iseva_ixabiso,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(udidi_ixabiso))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:iklayenti.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                udidi_ixabiso=정확한값(iklayenti,1)[0]
                if udidi_ixabiso==4:
                    isiqu_sombhalo=정확한값(iklayenti,7); ikhibhodi_ufako_nkcukacha.누름값(isiqu_sombhalo[0]!=0,struct.unpack('>I',isiqu_sombhalo[3:])[0]); continue
                if udidi_ixabiso==255:
                    isiqu_sombhalo=정확한값(iklayenti,11)
                    if isiqu_sombhalo[0]!=0: raise ValueError('unsupported QEMU input extension')
                    ikhibhodi_ufako_nkcukacha.누름값(struct.unpack('>H',isiqu_sombhalo[1:3])[0]!=0,struct.unpack('>I',isiqu_sombhalo[3:7])[0]); continue
                if udidi_ixabiso==5:
                    isiqu_sombhalo=정확한값(iklayenti,5); 단추들,isilungelelanisi_x,세로좌표=struct.unpack('>BHH',isiqu_sombhalo)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: ikhibhodi_ufako_nkcukacha.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=isilungelelanisi_x<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.thumela(bytes([ord('1')+색인]))
                    else: 자신.thumela(bytes([30,1,단추들,isilungelelanisi_x&255,isilungelelanisi_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if udidi_ixabiso==6:
                    isiqu_sombhalo=정확한값(iklayenti,7); ubude_ixabiso=struct.unpack('>i',isiqu_sombhalo[3:])[0]
                    if abs(ubude_ixabiso)>65536: raise ValueError('clipboard too large')
                    Umbhalo=정확한값(iklayenti,abs(ubude_ixabiso))
                    if ubude_ixabiso>=0:
                        try: ikhibhodi_ufako_nkcukacha.indawo_yogcino_ixabiso=Umbhalo.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: ikhibhodi_ufako_nkcukacha.indawo_yogcino_ixabiso=Umbhalo.decode('latin-1').encode('utf-8')
                        ikhibhodi_ufako_nkcukacha.indawo_yogcino_ixabiso=ikhibhodi_ufako_nkcukacha.indawo_yogcino_ixabiso[:65536].decode('utf-8','ignore').encode('utf-8')
                    iseva_ixabiso.sendall(bytes([udidi_ixabiso])+isiqu_sombhalo+Umbhalo); continue
                if udidi_ixabiso==0:
                    isiqu_sombhalo=정확한값(iklayenti,19)
                    if isiqu_sombhalo[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=isiqu_sombhalo[3]//8
                elif udidi_ixabiso==2:
                    isiqu_sombhalo=정확한값(iklayenti,3); 항목수=struct.unpack('>H',isiqu_sombhalo[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(iklayenti,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 ixabiso_elisisiseko Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    isiqu_sombhalo=struct.pack('>BHi',0,1,0)
                elif udidi_ixabiso in (3,150): isiqu_sombhalo=정확한값(iklayenti,9)
                elif udidi_ixabiso==248:
                    isiqu_sombhalo=정확한값(iklayenti,8)
                    if isiqu_sombhalo[7]>64: raise ValueError('fence too large')
                    isiqu_sombhalo+=정확한값(iklayenti,isiqu_sombhalo[7])
                elif udidi_ixabiso==250: isiqu_sombhalo=정확한값(iklayenti,3)
                elif udidi_ixabiso==251:
                    isiqu_sombhalo=정확한값(iklayenti,7)
                    if isiqu_sombhalo[5]>16: raise ValueError('too many screens')
                    isiqu_sombhalo+=정확한값(iklayenti,isiqu_sombhalo[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(udidi_ixabiso))
                iseva_ixabiso.sendall(bytes([udidi_ixabiso])+isiqu_sombhalo)
        except (OSError,EOFError,ValueError) as Impazamo:
            if str(Impazamo): print('VNC client:',Impazamo,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (iklayenti,iseva_ixabiso):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def i_run_idesktophu(접속번호=5902, Inethiwekhi=False, 파일전송접속번호=2121, 전달규칙들=(), isisombululo_ixabiso=(640, 480), undwendwe_idilesi=None, umsingathi_idilesi='127.0.0.1'):
    with ExitStack() as Izixhobo_50487cae, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Inethiwekhi_ibhulorho_ufako_nkcukacha = None
        if Inethiwekhi:
            from Inethiwekhi_ibhulorho import Inethiwekhi_ibhulorho
            Inethiwekhi_ibhulorho_ufako_nkcukacha = Izixhobo_50487cae.enter_context(Inethiwekhi_ibhulorho(파일전송접속번호, 전달규칙들, undwendwe_idilesi=undwendwe_idilesi, umsingathi_idilesi=umsingathi_idilesi))
        INDLELA=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Inethiwekhi_ibhulorho_ufako_nkcukacha and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and umsingathi==원격화면접속번호 for 통신규약,umsingathi,_ in Inethiwekhi_ibhulorho_ufako_nkcukacha.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Inkqubo=subprocess.Popen(Umyalelo(isisombululo_ixabiso)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(INDLELA)]+(Inethiwekhi_ibhulorho_ufako_nkcukacha.전달인수() if Inethiwekhi_ibhulorho_ufako_nkcukacha else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ibhulorho=I_Connect_idesktophu(Inkqubo); Umfundi=threading.Thread(target=ibhulorho.직렬입출력,daemon=True); Umfundi.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Inethiwekhi_ibhulorho_ufako_nkcukacha: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(umsingathi_idilesi,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Inkqubo.poll() is None:
                    try: iklayenti,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): iklayenti.close(); continue
                    if not INDLELA.exists(): iklayenti.close(); continue
                    처리작업=threading.Thread(target=ibhulorho.iklayenti,args=(iklayenti,INDLELA),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ibhulorho.닫힘=True
                if Inethiwekhi_ibhulorho_ufako_nkcukacha: Inethiwekhi_ibhulorho_ufako_nkcukacha.nqumama_umcimbi.set()
                if Inkqubo.poll() is None:
                    Inkqubo.terminate()
                    try: Inkqubo.wait(timeout=5)
                    except subprocess.TimeoutExpired: Inkqubo.kill(); Inkqubo.wait()
                Umfundi.join(timeout=2); Inkqubo.stdin.close(); Inkqubo.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Inethiwekhi_ibhulorho_ufako_nkcukacha and Inethiwekhi_ibhulorho_ufako_nkcukacha.Impazamo: raise RuntimeError('network bridge: '+Inethiwekhi_ibhulorho_ufako_nkcukacha.Impazamo)
            return 0 if 가로채기됨 else Inkqubo.returncode


if __name__=='__main__':
    from ukwenza_umyalelo import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    isiniki_myalelo_ULUHLU=인수해석기.parse_args()
    if isiniki_myalelo_ULUHLU.forward and not isiniki_myalelo_ULUHLU.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(i_run_idesktophu(isiniki_myalelo_ULUHLU.port,Inethiwekhi=isiniki_myalelo_ULUHLU.network,파일전송접속번호=isiniki_myalelo_ULUHLU.ftp_port,전달규칙들=isiniki_myalelo_ULUHLU.forward,isisombululo_ixabiso=isiniki_myalelo_ULUHLU.resolution))
