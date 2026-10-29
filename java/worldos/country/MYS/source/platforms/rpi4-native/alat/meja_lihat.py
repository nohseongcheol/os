#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Kunci_VALUE 입력은 Asli kernel_VALUE UART로 전달한다. localhost 전용, 단일 kawalan_VALUE 클라이언트.
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
from laksanakan_perintah import Perintah
from local_input import create


def EXACT_VALUE(소켓, Saiz):
    data = bytearray()
    while len(data) < Saiz:
        조각 = 소켓.recv(Saiz - len(data))
        if not 조각: raise EOFError()
        data.extend(조각)
    return bytes(data)


class papan_kekunci:
    def __init__(자신, e_mel_9aee63bd, 입력방식알림=None):
        자신.바이트전송 = e_mel_9aee63bd; 자신.kekunci_pengubah_suai = set(); 자신.papan_klip_VALUE = b''
        자신.한글조합기 = create(e_mel_9aee63bd, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.tukar_Kunci = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def e_mel_9aee63bd(자신, data):
        자신.한글조합기.조합확정()
        자신.바이트전송(data)

    def tukar_mod(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Kunci_simbol):
        if Kunci_simbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.kekunci_pengubah_suai.add(Kunci_simbol)
            else: 자신.kekunci_pengubah_suai.discard(Kunci_simbol)
            return
        if not 누르는중:
            자신.tukar_Kunci.discard(Kunci_simbol)
            return
        CTRL = bool(자신.kekunci_pengubah_suai & {0xffe3, 0xffe4})
        kekunci_SHIFT = bool(자신.kekunci_pengubah_suai & {0xffe1, 0xffe2})
        if CTRL and kekunci_SHIFT and Kunci_simbol in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Kunci_simbol in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.e_mel_9aee63bd(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Kunci_simbol==0xff1b: 자신.유니코드입력=None
            elif Kunci_simbol==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Kunci_simbol<128 and chr(Kunci_simbol) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Kunci_simbol)
            return
        if Kunci_simbol in (0xff31,0xffc6) or Kunci_simbol==32 and kekunci_SHIFT and not CTRL:
            if Kunci_simbol not in 자신.tukar_Kunci: 자신.tukar_mod()
            자신.tukar_Kunci.add(Kunci_simbol)
            return
        if Kunci_simbol==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and kekunci_SHIFT and Kunci_simbol in (ord('t'),ord('T')):
            자신.e_mel_9aee63bd(bytes([30,2,1,0,0,0,0])); return
        if Kunci_simbol==0xffc3: 자신.e_mel_9aee63bd(bytes([30,2,2,0,0,0,0])); return
        if Kunci_simbol==0xffc9: 자신.e_mel_9aee63bd(bytes([30,2,3,0,0,0,0])); return
        if CTRL and kekunci_SHIFT and Kunci_simbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.e_mel_9aee63bd(자신.papan_klip_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Kunci_simbol in 특수글쇠: 자신.e_mel_9aee63bd(특수글쇠[Kunci_simbol]); return
        pengekodan_aksara = Kunci_simbol & 0xffffff if Kunci_simbol & 0xff000000 == 0x01000000 else Kunci_simbol
        if pengekodan_aksara > 0x10ffff or 0xd800 <= pengekodan_aksara <= 0xdfff or Kunci_simbol >= 0xff00 and Kunci_simbol < 0x1000000: return
        if CTRL and 0x40 <= pengekodan_aksara <= 0x7f: 자신.e_mel_9aee63bd(bytes([pengekodan_aksara & 31])); return
        if pengekodan_aksara < 32: return
        if 자신.한글여부 and 자신.kekunci_pengubah_suai & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.suapan_Kunci(chr(pengekodan_aksara), altgr=True): return
        앞부분 = b'\x1b' if 자신.kekunci_pengubah_suai & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=pengekodan_aksara<127:
            data_aksara=chr(pengekodan_aksara).upper() if kekunci_SHIFT else chr(pengekodan_aksara)
            if 자신.한글조합기.suapan_Kunci(data_aksara): return
        자신.e_mel_9aee63bd(앞부분 + chr(pengekodan_aksara).encode('utf-8'))


class CONNECT_meja:
    def __init__(자신, Proses):
        자신.Proses=Proses; 자신.kunci_VALUE=threading.Lock(); 자신.준비완료=False; 자신.Terminal=False; 자신.시작화면=False; 자신.닫힘=False

    def e_mel_9aee63bd(자신, data):
        if not data or 자신.닫힘: return
        with 자신.kunci_VALUE:
            try: 자신.Proses.stdin.write(data); 자신.Proses.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                data=자신.Proses.stdout.read(4096)
                if not data: break
                sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
                끝부분=(끝부분+data)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.e_mel_9aee63bd(b'terminal\n')
        finally: 자신.닫힘=True

    def klien(자신, klien, LALUAN):
        pelayan_VALUE=socket.socket(socket.AF_UNIX); pelayan_VALUE.settimeout(10); klien.settimeout(10)
        papan_kekunci_pemasukan=papan_kekunci(자신.e_mel_9aee63bd,lambda 한글여부:자신.e_mel_9aee63bd(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            pelayan_VALUE.connect(str(LALUAN))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            klien.sendall(EXACT_VALUE(pelayan_VALUE,12))
            nombor_versi=EXACT_VALUE(klien,12)
            if nombor_versi not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            pelayan_VALUE.sendall(nombor_versi)
            item_COUNT=EXACT_VALUE(pelayan_VALUE,1);klien.sendall(item_COUNT+EXACT_VALUE(pelayan_VALUE,item_COUNT[0]))
            Keselamatan=EXACT_VALUE(klien,1)
            if Keselamatan!=b'\x01': raise ValueError('unexpected security type')
            pelayan_VALUE.sendall(Keselamatan)
            if nombor_versi==b'RFB 003.008\n':klien.sendall(EXACT_VALUE(pelayan_VALUE,4))
            pelayan_VALUE.sendall(EXACT_VALUE(klien,1))
            초기값=EXACT_VALUE(pelayan_VALUE,24)
            klien.sendall(초기값+EXACT_VALUE(pelayan_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klien.settimeout(None);pelayan_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        bidang_VALUE=EXACT_VALUE(pelayan_VALUE,1)[0]
                        if bidang_VALUE==0:
                            머리=EXACT_VALUE(pelayan_VALUE,3);pemasukan_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 jauh_VALUE 포인터의 중복을 피한다.
                            Tersembunyi_VALUE=포인터지원
                            if Tersembunyi_VALUE:klien.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klien.sendall(bytes([bidang_VALUE])+머리)
                            for _ in range(pemasukan_COUNT):
                                segi_empat_tepat=EXACT_VALUE(pelayan_VALUE,12);가로,Menegak_jawatan,폭,높이,pengekodan_VALUE=struct.unpack('>HHHHi',segi_empat_tepat)
                                if pengekodan_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(pengekodan_VALUE))
                                klien.sendall(segi_empat_tepat)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    data=EXACT_VALUE(pelayan_VALUE,min(남음,65536));klien.sendall(data);남음-=len(data)
                        elif bidang_VALUE==1:
                            머리=EXACT_VALUE(pelayan_VALUE,5);item_COUNT=struct.unpack('>H',머리[3:])[0]
                            klien.sendall(bytes([bidang_VALUE])+머리+EXACT_VALUE(pelayan_VALUE,item_COUNT*6))
                        elif bidang_VALUE==2:klien.sendall(bytes([bidang_VALUE]))
                        elif bidang_VALUE==3:
                            머리=EXACT_VALUE(pelayan_VALUE,7);item_COUNT=struct.unpack('>I',머리[3:])[0]
                            if item_COUNT>1048576:raise ValueError('server clipboard too large')
                            klien.sendall(bytes([bidang_VALUE])+머리+EXACT_VALUE(pelayan_VALUE,item_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(bidang_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klien.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                bidang_VALUE=EXACT_VALUE(klien,1)[0]
                if bidang_VALUE==4:
                    teks_jasad=EXACT_VALUE(klien,7); papan_kekunci_pemasukan.누름값(teks_jasad[0]!=0,struct.unpack('>I',teks_jasad[3:])[0]); continue
                if bidang_VALUE==255:
                    teks_jasad=EXACT_VALUE(klien,11)
                    if teks_jasad[0]!=0: raise ValueError('unsupported QEMU input extension')
                    papan_kekunci_pemasukan.누름값(struct.unpack('>H',teks_jasad[1:3])[0]!=0,struct.unpack('>I',teks_jasad[3:7])[0]); continue
                if bidang_VALUE==5:
                    teks_jasad=EXACT_VALUE(klien,5); 단추들,koordinat_x,Y_koordinat=struct.unpack('>BHH',teks_jasad)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: papan_kekunci_pemasukan.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=koordinat_x<576 and 112<=Y_koordinat<372:
                        Carian_INDEX=(Y_koordinat-112)//52
                        if (Y_koordinat-112)%52<40 and Carian_INDEX<5: 자신.e_mel_9aee63bd(bytes([ord('1')+Carian_INDEX]))
                    else: 자신.e_mel_9aee63bd(bytes([30,1,단추들,koordinat_x&255,koordinat_x>>8,Y_koordinat&255,Y_koordinat>>8]))
                    continue
                if bidang_VALUE==6:
                    teks_jasad=EXACT_VALUE(klien,7); kepanjangan_VALUE=struct.unpack('>i',teks_jasad[3:])[0]
                    if abs(kepanjangan_VALUE)>65536: raise ValueError('clipboard too large')
                    Teks=EXACT_VALUE(klien,abs(kepanjangan_VALUE))
                    if kepanjangan_VALUE>=0:
                        try: papan_kekunci_pemasukan.papan_klip_VALUE=Teks.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: papan_kekunci_pemasukan.papan_klip_VALUE=Teks.decode('latin-1').encode('utf-8')
                        papan_kekunci_pemasukan.papan_klip_VALUE=papan_kekunci_pemasukan.papan_klip_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    pelayan_VALUE.sendall(bytes([bidang_VALUE])+teks_jasad+Teks); continue
                if bidang_VALUE==0:
                    teks_jasad=EXACT_VALUE(klien,19)
                    if teks_jasad[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=teks_jasad[3]//8
                elif bidang_VALUE==2:
                    teks_jasad=EXACT_VALUE(klien,3); pemasukan_COUNT=struct.unpack('>H',teks_jasad[1:])[0]
                    if pemasukan_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(pemasukan_COUNT)+'i',EXACT_VALUE(klien,pemasukan_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 nilai_lalai Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    teks_jasad=struct.pack('>BHi',0,1,0)
                elif bidang_VALUE in (3,150): teks_jasad=EXACT_VALUE(klien,9)
                elif bidang_VALUE==248:
                    teks_jasad=EXACT_VALUE(klien,8)
                    if teks_jasad[7]>64: raise ValueError('fence too large')
                    teks_jasad+=EXACT_VALUE(klien,teks_jasad[7])
                elif bidang_VALUE==250: teks_jasad=EXACT_VALUE(klien,3)
                elif bidang_VALUE==251:
                    teks_jasad=EXACT_VALUE(klien,7)
                    if teks_jasad[5]>16: raise ValueError('too many screens')
                    teks_jasad+=EXACT_VALUE(klien,teks_jasad[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(bidang_VALUE))
                pelayan_VALUE.sendall(bytes([bidang_VALUE])+teks_jasad)
        except (OSError,EOFError,ValueError) as RALAT:
            if str(RALAT): print('VNC client:',RALAT,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (klien,pelayan_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def jalankan_meja(nombor_port=5902, rangkaian=False, pemindahan_fail_nombor_port=2121, 전달규칙들=(), resolusi_VALUE=(640, 480), tetamu_e_mel=None, hos_e_mel='127.0.0.1'):
    with ExitStack() as Sumber, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        rangkaian_penghubung_pemasukan = None
        if rangkaian:
            from rangkaian_penghubung import rangkaian_penghubung
            rangkaian_penghubung_pemasukan = Sumber.enter_context(rangkaian_penghubung(pemindahan_fail_nombor_port, 전달규칙들, tetamu_e_mel=tetamu_e_mel, hos_e_mel=hos_e_mel))
        LALUAN=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',nombor_port)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if rangkaian_penghubung_pemasukan and (원격화면접속번호==pemindahan_fail_nombor_port or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and hos==원격화면접속번호 for 통신규약,hos,_ in rangkaian_penghubung_pemasukan.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proses=subprocess.Popen(Perintah(resolusi_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(LALUAN)]+(rangkaian_penghubung_pemasukan.전달인수() if rangkaian_penghubung_pemasukan else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            penghubung=CONNECT_meja(Proses); Pembaca=threading.Thread(target=penghubung.직렬입출력,daemon=True); Pembaca.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if rangkaian_penghubung_pemasukan: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(hos_e_mel,pemindahan_fail_nombor_port),flush=True)
            def batal(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,batal)
            pemprosesan_tugas=None; 가로채기됨=False
            try:
                while Proses.poll() is None:
                    try: klien,_=수신창구.accept()
                    except socket.timeout: continue
                    if pemprosesan_tugas is not None and pemprosesan_tugas.is_alive(): klien.close(); continue
                    if not LALUAN.exists(): klien.close(); continue
                    pemprosesan_tugas=threading.Thread(target=penghubung.klien,args=(klien,LALUAN),daemon=True); pemprosesan_tugas.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                penghubung.닫힘=True
                if rangkaian_penghubung_pemasukan: rangkaian_penghubung_pemasukan.Jeda_acara.set()
                if Proses.poll() is None:
                    Proses.terminate()
                    try: Proses.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
                Pembaca.join(timeout=2); Proses.stdin.close(); Proses.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if rangkaian_penghubung_pemasukan and rangkaian_penghubung_pemasukan.RALAT: raise RuntimeError('network bridge: '+rangkaian_penghubung_pemasukan.RALAT)
            return 0 if 가로채기됨 else Proses.returncode


if __name__=='__main__':
    from laksanakan_perintah import 해상도읽기
    penghurai=argparse.ArgumentParser(description=__doc__); penghurai.add_argument('--port',type=int,default=5902)
    penghurai.add_argument('--resolution',type=해상도읽기,default=(640,480))
    penghurai.add_argument('--network',action='store_true'); penghurai.add_argument('--ftp-port',type=int,default=2121)
    penghurai.add_argument('--forward',action='append',default=[])
    argumen_ARRAY=penghurai.parse_args()
    if argumen_ARRAY.forward and not argumen_ARRAY.network: penghurai.error('--forward requires --network')
    raise SystemExit(jalankan_meja(argumen_ARRAY.port,rangkaian=argumen_ARRAY.network,pemindahan_fail_nombor_port=argumen_ARRAY.ftp_port,전달규칙들=argumen_ARRAY.forward,resolusi_VALUE=argumen_ARRAY.resolution))
