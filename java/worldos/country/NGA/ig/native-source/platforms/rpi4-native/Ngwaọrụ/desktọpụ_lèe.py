#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, ọtụgwo_valuu 입력은 자체 mkpụrụobī_kọmpùta_valuu UART로 전달한다. localhost 전용, 단일 njizi_valuu 클라이언트.
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
from mee_nnyemiwu import Ntiiwu
from local_input import create


def 정확한값(소켓, Ụhara):
    datà = bytearray()
    while len(datà) < Ụhara:
        조각 = 소켓.recv(Ụhara - len(datà))
        if not 조각: raise EOFError()
        datà.extend(조각)
    return bytes(datà)


class ụgbọọtụgwo:
    def __init__(자신, zìga, 입력방식알림=None):
        자신.바이트전송 = zìga; 자신.ọtụgwo_kèmmegharị = set(); 자신.bọọd_ntipanye_valuu = b''
        자신.한글조합기 = create(zìga, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.ngbanwụ_ọtụgwo = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def zìga(자신, datà):
        자신.한글조합기.조합확정()
        자신.바이트전송(datà)

    def ngbanwụ_moòdù(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, ọtụgwo_adimara):
        if ọtụgwo_adimara in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.ọtụgwo_kèmmegharị.add(ọtụgwo_adimara)
            else: 자신.ọtụgwo_kèmmegharị.discard(ọtụgwo_adimara)
            return
        if not 누르는중:
            자신.ngbanwụ_ọtụgwo.discard(ọtụgwo_adimara)
            return
        CTRL = bool(자신.ọtụgwo_kèmmegharị & {0xffe3, 0xffe4})
        ọtụgwo_SHIFT = bool(자신.ọtụgwo_kèmmegharị & {0xffe1, 0xffe2})
        if CTRL and ọtụgwo_SHIFT and ọtụgwo_adimara in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if ọtụgwo_adimara in (32,0xff0d):
                try:
                    valuu=int(자신.유니코드입력,16)
                    if 32<=valuu<=0x10ffff and not 0xd800<=valuu<=0xdfff: 자신.zìga(chr(valuu).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif ọtụgwo_adimara==0xff1b: 자신.유니코드입력=None
            elif ọtụgwo_adimara==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif ọtụgwo_adimara<128 and chr(ọtụgwo_adimara) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(ọtụgwo_adimara)
            return
        if ọtụgwo_adimara in (0xff31,0xffc6) or ọtụgwo_adimara==32 and ọtụgwo_SHIFT and not CTRL:
            if ọtụgwo_adimara not in 자신.ngbanwụ_ọtụgwo: 자신.ngbanwụ_moòdù()
            자신.ngbanwụ_ọtụgwo.add(ọtụgwo_adimara)
            return
        if ọtụgwo_adimara==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and ọtụgwo_SHIFT and ọtụgwo_adimara in (ord('t'),ord('T')):
            자신.zìga(bytes([30,2,1,0,0,0,0])); return
        if ọtụgwo_adimara==0xffc3: 자신.zìga(bytes([30,2,2,0,0,0,0])); return
        if ọtụgwo_adimara==0xffc9: 자신.zìga(bytes([30,2,3,0,0,0,0])); return
        if CTRL and ọtụgwo_SHIFT and ọtụgwo_adimara in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.zìga(자신.bọọd_ntipanye_valuu); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if ọtụgwo_adimara in 특수글쇠: 자신.zìga(특수글쇠[ọtụgwo_adimara]); return
        mkpụrụedemede_ntinye_koòdù = ọtụgwo_adimara & 0xffffff if ọtụgwo_adimara & 0xff000000 == 0x01000000 else ọtụgwo_adimara
        if mkpụrụedemede_ntinye_koòdù > 0x10ffff or 0xd800 <= mkpụrụedemede_ntinye_koòdù <= 0xdfff or ọtụgwo_adimara >= 0xff00 and ọtụgwo_adimara < 0x1000000: return
        if CTRL and 0x40 <= mkpụrụedemede_ntinye_koòdù <= 0x7f: 자신.zìga(bytes([mkpụrụedemede_ntinye_koòdù & 31])); return
        if mkpụrụedemede_ntinye_koòdù < 32: return
        if 자신.한글여부 and 자신.ọtụgwo_kèmmegharị & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.nri_ọtụgwo(chr(mkpụrụedemede_ntinye_koòdù), altgr=True): return
        앞부분 = b'\x1b' if 자신.ọtụgwo_kèmmegharị & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=mkpụrụedemede_ntinye_koòdù<127:
            mkpụrụedemede_datà=chr(mkpụrụedemede_ntinye_koòdù).upper() if ọtụgwo_SHIFT else chr(mkpụrụedemede_ntinye_koòdù)
            if 자신.한글조합기.nri_ọtụgwo(mkpụrụedemede_datà): return
        자신.zìga(앞부분 + chr(mkpụrụedemede_ntinye_koòdù).encode('utf-8'))


class JIKỌ_desktọpụ:
    def __init__(자신, ùsòrò):
        자신.ùsòrò=ùsòrò; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def zìga(자신, datà):
        if not datà or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.ùsòrò.stdin.write(datà); 자신.ùsòrò.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                datà=자신.ùsòrò.stdout.read(4096)
                if not datà: break
                sys.stdout.buffer.write(datà); sys.stdout.buffer.flush()
                끝부분=(끝부분+datà)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.zìga(b'terminal\n')
        finally: 자신.닫힘=True

    def klayènt(자신, klayènt, ụzọ_ozi):
        savà_valuu=socket.socket(socket.AF_UNIX); savà_valuu.settimeout(10); klayènt.settimeout(10)
        ụgbọọtụgwo_ndebà=ụgbọọtụgwo(자신.zìga,lambda 한글여부:자신.zìga(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            savà_valuu.connect(str(ụzọ_ozi))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            klayènt.sendall(정확한값(savà_valuu,12))
            판번호=정확한값(klayènt,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            savà_valuu.sendall(판번호)
            개수=정확한값(savà_valuu,1);klayènt.sendall(개수+정확한값(savà_valuu,개수[0]))
            Nche=정확한값(klayènt,1)
            if Nche!=b'\x01': raise ValueError('unexpected security type')
            savà_valuu.sendall(Nche)
            if 판번호==b'RFB 003.008\n':klayènt.sendall(정확한값(savà_valuu,4))
            savà_valuu.sendall(정확한값(klayènt,1))
            초기값=정확한값(savà_valuu,24)
            klayènt.sendall(초기값+정확한값(savà_valuu,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klayènt.settimeout(None);savà_valuu.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        otu_valuu_4b6d6445=정확한값(savà_valuu,1)[0]
                        if otu_valuu_4b6d6445==0:
                            머리=정확한값(savà_valuu,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 ebe_dị̀anyā_valuu 포인터의 중복을 피한다.
                            nzòròèzo_valuu=포인터지원
                            if nzòròèzo_valuu:klayènt.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klayènt.sendall(bytes([otu_valuu_4b6d6445])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(savà_valuu,12);가로,세로,폭,높이,ntinye_koòdù_valuu=struct.unpack('>HHHHi',사각형)
                                if ntinye_koòdù_valuu!=0:raise ValueError('unexpected framebuffer encoding: '+str(ntinye_koòdù_valuu))
                                klayènt.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    datà=정확한값(savà_valuu,min(남음,65536));klayènt.sendall(datà);남음-=len(datà)
                        elif otu_valuu_4b6d6445==1:
                            머리=정확한값(savà_valuu,5);개수=struct.unpack('>H',머리[3:])[0]
                            klayènt.sendall(bytes([otu_valuu_4b6d6445])+머리+정확한값(savà_valuu,개수*6))
                        elif otu_valuu_4b6d6445==2:klayènt.sendall(bytes([otu_valuu_4b6d6445]))
                        elif otu_valuu_4b6d6445==3:
                            머리=정확한값(savà_valuu,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            klayènt.sendall(bytes([otu_valuu_4b6d6445])+머리+정확한값(savà_valuu,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(otu_valuu_4b6d6445))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klayènt.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                otu_valuu_4b6d6445=정확한값(klayènt,1)[0]
                if otu_valuu_4b6d6445==4:
                    àhụngwè=정확한값(klayènt,7); ụgbọọtụgwo_ndebà.누름값(àhụngwè[0]!=0,struct.unpack('>I',àhụngwè[3:])[0]); continue
                if otu_valuu_4b6d6445==255:
                    àhụngwè=정확한값(klayènt,11)
                    if àhụngwè[0]!=0: raise ValueError('unsupported QEMU input extension')
                    ụgbọọtụgwo_ndebà.누름값(struct.unpack('>H',àhụngwè[1:3])[0]!=0,struct.unpack('>I',àhụngwè[3:7])[0]); continue
                if otu_valuu_4b6d6445==5:
                    àhụngwè=정확한값(klayènt,5); 단추들,ngakọrịta_x,세로좌표=struct.unpack('>BHH',àhụngwè)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: ụgbọọtụgwo_ndebà.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=ngakọrịta_x<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.zìga(bytes([ord('1')+색인]))
                    else: 자신.zìga(bytes([30,1,단추들,ngakọrịta_x&255,ngakọrịta_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if otu_valuu_4b6d6445==6:
                    àhụngwè=정확한값(klayènt,7); ogologo_valuu=struct.unpack('>i',àhụngwè[3:])[0]
                    if abs(ogologo_valuu)>65536: raise ValueError('clipboard too large')
                    SMS=정확한값(klayènt,abs(ogologo_valuu))
                    if ogologo_valuu>=0:
                        try: ụgbọọtụgwo_ndebà.bọọd_ntipanye_valuu=SMS.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: ụgbọọtụgwo_ndebà.bọọd_ntipanye_valuu=SMS.decode('latin-1').encode('utf-8')
                        ụgbọọtụgwo_ndebà.bọọd_ntipanye_valuu=ụgbọọtụgwo_ndebà.bọọd_ntipanye_valuu[:65536].decode('utf-8','ignore').encode('utf-8')
                    savà_valuu.sendall(bytes([otu_valuu_4b6d6445])+àhụngwè+SMS); continue
                if otu_valuu_4b6d6445==0:
                    àhụngwè=정확한값(klayènt,19)
                    if àhụngwè[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=àhụngwè[3]//8
                elif otu_valuu_4b6d6445==2:
                    àhụngwè=정확한값(klayènt,3); 항목수=struct.unpack('>H',àhụngwè[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(klayènt,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 Ngwa_ihe_dịadị Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    àhụngwè=struct.pack('>BHi',0,1,0)
                elif otu_valuu_4b6d6445 in (3,150): àhụngwè=정확한값(klayènt,9)
                elif otu_valuu_4b6d6445==248:
                    àhụngwè=정확한값(klayènt,8)
                    if àhụngwè[7]>64: raise ValueError('fence too large')
                    àhụngwè+=정확한값(klayènt,àhụngwè[7])
                elif otu_valuu_4b6d6445==250: àhụngwè=정확한값(klayènt,3)
                elif otu_valuu_4b6d6445==251:
                    àhụngwè=정확한값(klayènt,7)
                    if àhụngwè[5]>16: raise ValueError('too many screens')
                    àhụngwè+=정확한값(klayènt,àhụngwè[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(otu_valuu_4b6d6445))
                savà_valuu.sendall(bytes([otu_valuu_4b6d6445])+àhụngwè)
        except (OSError,EOFError,ValueError) as mmejọ:
            if str(mmejọ): print('VNC client:',mmejọ,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (klayènt,savà_valuu):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def mee_desktọpụ(접속번호=5902, Netwọọkụ=False, 파일전송접속번호=2121, 전달규칙들=(), ụcha_ngosịpụta_valuu=(640, 480), 게스트주소=None, usu_àdreèsì='127.0.0.1'):
    with ExitStack() as Iheejiarụ_gasị, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if Netwọọkụ:
            from 통신다리 import 통신다리
            통신다리항목 = Iheejiarụ_gasị.enter_context(통신다리(파일전송접속번호, 전달규칙들, 게스트주소=게스트주소, usu_àdreèsì=usu_àdreèsì))
        ụzọ_ozi=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and usu==원격화면접속번호 for 통신규약,usu,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            ùsòrò=subprocess.Popen(Ntiiwu(ụcha_ngosịpụta_valuu)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ụzọ_ozi)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=JIKỌ_desktọpụ(ùsòrò); Ọgụụ=threading.Thread(target=연결다리.직렬입출력,daemon=True); Ọgụụ.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(usu_àdreèsì,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while ùsòrò.poll() is None:
                    try: klayènt,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): klayènt.close(); continue
                    if not ụzọ_ozi.exists(): klayènt.close(); continue
                    처리작업=threading.Thread(target=연결다리.klayènt,args=(klayènt,ụzọ_ozi),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.chèretụ_mmèrème.set()
                if ùsòrò.poll() is None:
                    ùsòrò.terminate()
                    try: ùsòrò.wait(timeout=5)
                    except subprocess.TimeoutExpired: ùsòrò.kill(); ùsòrò.wait()
                Ọgụụ.join(timeout=2); ùsòrò.stdin.close(); ùsòrò.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.mmejọ: raise RuntimeError('network bridge: '+통신다리항목.mmejọ)
            return 0 if 가로채기됨 else ùsòrò.returncode


if __name__=='__main__':
    from mee_nnyemiwu import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    agụment_MKPOKỌTA=인수해석기.parse_args()
    if agụment_MKPOKỌTA.forward and not agụment_MKPOKỌTA.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(mee_desktọpụ(agụment_MKPOKỌTA.port,Netwọọkụ=agụment_MKPOKỌTA.network,파일전송접속번호=agụment_MKPOKỌTA.ftp_port,전달규칙들=agụment_MKPOKỌTA.forward,ụcha_ngosịpụta_valuu=agụment_MKPOKỌTA.resolution))
