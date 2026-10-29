#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Kunci_VALUE 입력은 Asli kernel_VALUE UART로 전달한다. localhost 전용, 단일 kontrol_VALUE 클라이언트.
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
from Jalankan_perintah import perintah
from local_input import create


def EXACT_VALUE(소켓, Ukuran):
    data = bytearray()
    while len(data) < Ukuran:
        조각 = 소켓.recv(Ukuran - len(data))
        if not 조각: raise EOFError()
        data.extend(조각)
    return bytes(data)


class keyboard:
    def __init__(자신, kirim, 입력방식알림=None):
        자신.바이트전송 = kirim; 자신.kunci_modifikasi = set(); 자신.clipboard_VALUE = b''
        자신.한글조합기 = create(kirim, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Kunci = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def kirim(자신, data):
        자신.한글조합기.조합확정()
        자신.바이트전송(data)

    def SWITCH_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Kunci_simbol):
        if Kunci_simbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.kunci_modifikasi.add(Kunci_simbol)
            else: 자신.kunci_modifikasi.discard(Kunci_simbol)
            return
        if not 누르는중:
            자신.SWITCH_Kunci.discard(Kunci_simbol)
            return
        CTRL = bool(자신.kunci_modifikasi & {0xffe3, 0xffe4})
        tombol_SHIFT = bool(자신.kunci_modifikasi & {0xffe1, 0xffe2})
        if CTRL and tombol_SHIFT and Kunci_simbol in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Kunci_simbol in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.kirim(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Kunci_simbol==0xff1b: 자신.유니코드입력=None
            elif Kunci_simbol==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Kunci_simbol<128 and chr(Kunci_simbol) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Kunci_simbol)
            return
        if Kunci_simbol in (0xff31,0xffc6) or Kunci_simbol==32 and tombol_SHIFT and not CTRL:
            if Kunci_simbol not in 자신.SWITCH_Kunci: 자신.SWITCH_MODE()
            자신.SWITCH_Kunci.add(Kunci_simbol)
            return
        if Kunci_simbol==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and tombol_SHIFT and Kunci_simbol in (ord('t'),ord('T')):
            자신.kirim(bytes([30,2,1,0,0,0,0])); return
        if Kunci_simbol==0xffc3: 자신.kirim(bytes([30,2,2,0,0,0,0])); return
        if Kunci_simbol==0xffc9: 자신.kirim(bytes([30,2,3,0,0,0,0])); return
        if CTRL and tombol_SHIFT and Kunci_simbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.kirim(자신.clipboard_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Kunci_simbol in 특수글쇠: 자신.kirim(특수글쇠[Kunci_simbol]); return
        pengodean_karakter = Kunci_simbol & 0xffffff if Kunci_simbol & 0xff000000 == 0x01000000 else Kunci_simbol
        if pengodean_karakter > 0x10ffff or 0xd800 <= pengodean_karakter <= 0xdfff or Kunci_simbol >= 0xff00 and Kunci_simbol < 0x1000000: return
        if CTRL and 0x40 <= pengodean_karakter <= 0x7f: 자신.kirim(bytes([pengodean_karakter & 31])); return
        if pengodean_karakter < 32: return
        if 자신.한글여부 and 자신.kunci_modifikasi & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.feed_Kunci(chr(pengodean_karakter), altgr=True): return
        앞부분 = b'\x1b' if 자신.kunci_modifikasi & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=pengodean_karakter<127:
            data_karakter=chr(pengodean_karakter).upper() if tombol_SHIFT else chr(pengodean_karakter)
            if 자신.한글조합기.feed_Kunci(data_karakter): return
        자신.kirim(앞부분 + chr(pengodean_karakter).encode('utf-8'))


class CONNECT_desktop:
    def __init__(자신, Proses):
        자신.Proses=Proses; 자신.kunci_VALUE=threading.Lock(); 자신.준비완료=False; 자신.terminal=False; 자신.시작화면=False; 자신.닫힘=False

    def kirim(자신, data):
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
                    자신.terminal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.kirim(b'terminal\n')
        finally: 자신.닫힘=True

    def klien(자신, klien, jalur):
        server_VALUE=socket.socket(socket.AF_UNIX); server_VALUE.settimeout(10); klien.settimeout(10)
        keyboard_entri=keyboard(자신.kirim,lambda 한글여부:자신.kirim(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_VALUE.connect(str(jalur))
            # keadaan_awal 협상은 순서대로 끝낸다. 이후 keluaranTeks 가닥만 클라이언트에 쓴다.
            klien.sendall(EXACT_VALUE(server_VALUE,12))
            nomor_versi=EXACT_VALUE(klien,12)
            if nomor_versi not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_VALUE.sendall(nomor_versi)
            item_COUNT=EXACT_VALUE(server_VALUE,1);klien.sendall(item_COUNT+EXACT_VALUE(server_VALUE,item_COUNT[0]))
            Keamanan=EXACT_VALUE(klien,1)
            if Keamanan!=b'\x01': raise ValueError('unexpected security type')
            server_VALUE.sendall(Keamanan)
            if nomor_versi==b'RFB 003.008\n':klien.sendall(EXACT_VALUE(server_VALUE,4))
            server_VALUE.sendall(EXACT_VALUE(klien,1))
            초기값=EXACT_VALUE(server_VALUE,24)
            klien.sendall(초기값+EXACT_VALUE(server_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klien.settimeout(None);server_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        area_VALUE=EXACT_VALUE(server_VALUE,1)[0]
                        if area_VALUE==0:
                            kepala_VALUE=EXACT_VALUE(server_VALUE,3);entri_COUNT=struct.unpack('>H',kepala_VALUE[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 jarak_jauh_VALUE 포인터의 중복을 피한다.
                            Tersembunyi_VALUE=포인터지원
                            if Tersembunyi_VALUE:klien.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klien.sendall(bytes([area_VALUE])+kepala_VALUE)
                            for _ in range(entri_COUNT):
                                persegi=EXACT_VALUE(server_VALUE,12);가로,Vertikal_posisi,폭,높이,pengodean_VALUE=struct.unpack('>HHHHi',persegi)
                                if pengodean_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(pengodean_VALUE))
                                klien.sendall(persegi)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    data=EXACT_VALUE(server_VALUE,min(남음,65536));klien.sendall(data);남음-=len(data)
                        elif area_VALUE==1:
                            kepala_VALUE=EXACT_VALUE(server_VALUE,5);item_COUNT=struct.unpack('>H',kepala_VALUE[3:])[0]
                            klien.sendall(bytes([area_VALUE])+kepala_VALUE+EXACT_VALUE(server_VALUE,item_COUNT*6))
                        elif area_VALUE==2:klien.sendall(bytes([area_VALUE]))
                        elif area_VALUE==3:
                            kepala_VALUE=EXACT_VALUE(server_VALUE,7);item_COUNT=struct.unpack('>I',kepala_VALUE[3:])[0]
                            if item_COUNT>1048576:raise ValueError('server clipboard too large')
                            klien.sendall(bytes([area_VALUE])+kepala_VALUE+EXACT_VALUE(server_VALUE,item_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(area_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klien.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            tugasLatar=threading.Thread(target=출력결과,daemon=True);tugasLatar.start()
            while not 자신.닫힘:
                area_VALUE=EXACT_VALUE(klien,1)[0]
                if area_VALUE==4:
                    teks_isi=EXACT_VALUE(klien,7); keyboard_entri.누름값(teks_isi[0]!=0,struct.unpack('>I',teks_isi[3:])[0]); continue
                if area_VALUE==255:
                    teks_isi=EXACT_VALUE(klien,11)
                    if teks_isi[0]!=0: raise ValueError('unsupported QEMU input extension')
                    keyboard_entri.누름값(struct.unpack('>H',teks_isi[1:3])[0]!=0,struct.unpack('>I',teks_isi[3:7])[0]); continue
                if area_VALUE==5:
                    teks_isi=EXACT_VALUE(klien,5); 단추들,koordinat_x,Y_koordinat=struct.unpack('>BHH',teks_isi)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: keyboard_entri.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=koordinat_x<576 and 112<=Y_koordinat<372:
                        LOOKUP_INDEX=(Y_koordinat-112)//52
                        if (Y_koordinat-112)%52<40 and LOOKUP_INDEX<5: 자신.kirim(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.kirim(bytes([30,1,단추들,koordinat_x&255,koordinat_x>>8,Y_koordinat&255,Y_koordinat>>8]))
                    continue
                if area_VALUE==6:
                    teks_isi=EXACT_VALUE(klien,7); panjang_VALUE=struct.unpack('>i',teks_isi[3:])[0]
                    if abs(panjang_VALUE)>65536: raise ValueError('clipboard too large')
                    teks=EXACT_VALUE(klien,abs(panjang_VALUE))
                    if panjang_VALUE>=0:
                        try: keyboard_entri.clipboard_VALUE=teks.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: keyboard_entri.clipboard_VALUE=teks.decode('latin-1').encode('utf-8')
                        keyboard_entri.clipboard_VALUE=keyboard_entri.clipboard_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_VALUE.sendall(bytes([area_VALUE])+teks_isi+teks); continue
                if area_VALUE==0:
                    teks_isi=EXACT_VALUE(klien,19)
                    if teks_isi[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=teks_isi[3]//8
                elif area_VALUE==2:
                    teks_isi=EXACT_VALUE(klien,3); entri_COUNT=struct.unpack('>H',teks_isi[1:])[0]
                    if entri_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(entri_COUNT)+'i',EXACT_VALUE(klien,entri_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 nilai_default Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    teks_isi=struct.pack('>BHi',0,1,0)
                elif area_VALUE in (3,150): teks_isi=EXACT_VALUE(klien,9)
                elif area_VALUE==248:
                    teks_isi=EXACT_VALUE(klien,8)
                    if teks_isi[7]>64: raise ValueError('fence too large')
                    teks_isi+=EXACT_VALUE(klien,teks_isi[7])
                elif area_VALUE==250: teks_isi=EXACT_VALUE(klien,3)
                elif area_VALUE==251:
                    teks_isi=EXACT_VALUE(klien,7)
                    if teks_isi[5]>16: raise ValueError('too many screens')
                    teks_isi+=EXACT_VALUE(klien,teks_isi[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(area_VALUE))
                server_VALUE.sendall(bytes([area_VALUE])+teks_isi)
        except (OSError,EOFError,ValueError) as galat:
            if str(galat): print('VNC client:',galat,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (klien,server_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def eksekusi_desktop(nomor_port=5902, jaringan=False, transfer_file_nomor_port=2121, 전달규칙들=(), resolusi_VALUE=(640, 480), tamu_surel=None, host_surel='127.0.0.1'):
    with ExitStack() as Referensi_50487cae, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        jaringan_bridge_entri = None
        if jaringan:
            from jaringan_bridge import jaringan_bridge
            jaringan_bridge_entri = Referensi_50487cae.enter_context(jaringan_bridge(transfer_file_nomor_port, 전달규칙들, tamu_surel=tamu_surel, host_surel=host_surel))
        jalur=Path(작업경로)/'display.sock'
        with socket.socket() as terima_port:
            terima_port.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            terima_port.bind(('127.0.0.1',nomor_port)); terima_port.listen(1); terima_port.settimeout(.2)
            원격화면접속번호=terima_port.getsockname()[1]
            if jaringan_bridge_entri and (원격화면접속번호==transfer_file_nomor_port or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and host==원격화면접속번호 for 통신규약,host,_ in jaringan_bridge_entri.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proses=subprocess.Popen(perintah(resolusi_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(jalur)]+(jaringan_bridge_entri.전달인수() if jaringan_bridge_entri else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            bridge=CONNECT_desktop(Proses); Pembaca=threading.Thread(target=bridge.직렬입출력,daemon=True); Pembaca.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(terima_port.getsockname()[1]),flush=True)
            if jaringan_bridge_entri: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(host_surel,transfer_file_nomor_port),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            pemrosesan_tugas=None; 가로채기됨=False
            try:
                while Proses.poll() is None:
                    try: klien,_=terima_port.accept()
                    except socket.timeout: continue
                    if pemrosesan_tugas is not None and pemrosesan_tugas.is_alive(): klien.close(); continue
                    if not jalur.exists(): klien.close(); continue
                    pemrosesan_tugas=threading.Thread(target=bridge.klien,args=(klien,jalur),daemon=True); pemrosesan_tugas.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                bridge.닫힘=True
                if jaringan_bridge_entri: jaringan_bridge_entri.Jeda_acara.set()
                if Proses.poll() is None:
                    Proses.terminate()
                    try: Proses.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
                Pembaca.join(timeout=2); Proses.stdin.close(); Proses.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if jaringan_bridge_entri and jaringan_bridge_entri.galat: raise RuntimeError('network bridge: '+jaringan_bridge_entri.galat)
            return 0 if 가로채기됨 else Proses.returncode


if __name__=='__main__':
    from Jalankan_perintah import 해상도읽기
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--port',type=int,default=5902)
    parser.add_argument('--resolution',type=해상도읽기,default=(640,480))
    parser.add_argument('--network',action='store_true'); parser.add_argument('--ftp-port',type=int,default=2121)
    parser.add_argument('--forward',action='append',default=[])
    argumen_ARRAY=parser.parse_args()
    if argumen_ARRAY.forward and not argumen_ARRAY.network: parser.error('--forward requires --network')
    raise SystemExit(eksekusi_desktop(argumen_ARRAY.port,jaringan=argumen_ARRAY.network,transfer_file_nomor_port=argumen_ARRAY.ftp_port,전달규칙들=argumen_ARRAY.forward,resolusi_VALUE=argumen_ARRAY.resolution))
