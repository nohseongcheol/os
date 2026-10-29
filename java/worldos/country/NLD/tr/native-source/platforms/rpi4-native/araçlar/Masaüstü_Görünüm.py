#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, tuş_değer 입력은 Öz çekirdek_değer UART로 전달한다. localhost 전용, 단일 denetim_değer 클라이언트.
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
from yürütmek_komut import komut
from local_input import create


def ÖZDEŞ_değer(yuva_değer, Boyut):
    veri = bytearray()
    while len(veri) < Boyut:
        parça_değer = yuva_değer.recv(Boyut - len(veri))
        if not parça_değer: raise EOFError()
        veri.extend(parça_değer)
    return bytes(veri)


class klavye:
    def __init__(자신, göndermek, 입력방식알림=None):
        자신.바이트전송 = göndermek; 자신.değiştirici_tuş = set(); 자신.pano_değer = b''
        자신.한글조합기 = create(göndermek, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.geçiş_tuş = set()
        자신.UNICODE_artış = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def göndermek(자신, veri):
        자신.한글조합기.조합확정()
        자신.바이트전송(veri)

    def geçiş_mod(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, tuş_simge):
        if tuş_simge in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.değiştirici_tuş.add(tuş_simge)
            else: 자신.değiştirici_tuş.discard(tuş_simge)
            return
        if not 누르는중:
            자신.geçiş_tuş.discard(tuş_simge)
            return
        CTRL = bool(자신.değiştirici_tuş & {0xffe3, 0xffe4})
        SHIFT_tuşu = bool(자신.değiştirici_tuş & {0xffe1, 0xffe2})
        if CTRL and SHIFT_tuşu and tuş_simge in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.UNICODE_artış = ''; return
        if 자신.UNICODE_artış is not None:
            if tuş_simge in (32,0xff0d):
                try:
                    değer=int(자신.UNICODE_artış,16)
                    if 32<=değer<=0x10ffff and not 0xd800<=değer<=0xdfff: 자신.göndermek(chr(değer).encode('utf-8'))
                except ValueError: pass
                자신.UNICODE_artış=None
            elif tuş_simge==0xff1b: 자신.UNICODE_artış=None
            elif tuş_simge==0xff08: 자신.UNICODE_artış=자신.UNICODE_artış[:-1]
            elif tuş_simge<128 and chr(tuş_simge) in '0123456789abcdefABCDEF' and len(자신.UNICODE_artış)<6: 자신.UNICODE_artış+=chr(tuş_simge)
            return
        if tuş_simge in (0xff31,0xffc6) or tuş_simge==32 and SHIFT_tuşu and not CTRL:
            if tuş_simge not in 자신.geçiş_tuş: 자신.geçiş_mod()
            자신.geçiş_tuş.add(tuş_simge)
            return
        if tuş_simge==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and SHIFT_tuşu and tuş_simge in (ord('t'),ord('T')):
            자신.göndermek(bytes([30,2,1,0,0,0,0])); return
        if tuş_simge==0xffc3: 자신.göndermek(bytes([30,2,2,0,0,0,0])); return
        if tuş_simge==0xffc9: 자신.göndermek(bytes([30,2,3,0,0,0,0])); return
        if CTRL and SHIFT_tuşu and tuş_simge in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.göndermek(자신.pano_değer); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if tuş_simge in 특수글쇠: 자신.göndermek(특수글쇠[tuş_simge]); return
        karakter_kodlaması = tuş_simge & 0xffffff if tuş_simge & 0xff000000 == 0x01000000 else tuş_simge
        if karakter_kodlaması > 0x10ffff or 0xd800 <= karakter_kodlaması <= 0xdfff or tuş_simge >= 0xff00 and tuş_simge < 0x1000000: return
        if CTRL and 0x40 <= karakter_kodlaması <= 0x7f: 자신.göndermek(bytes([karakter_kodlaması & 31])); return
        if karakter_kodlaması < 32: return
        if 자신.한글여부 and 자신.değiştirici_tuş & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.akış_tuş(chr(karakter_kodlaması), altgr=True): return
        satır_aralığı_parça = b'\x1b' if 자신.değiştirici_tuş & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not satır_aralığı_parça and 32<=karakter_kodlaması<127:
            karakter_verileri=chr(karakter_kodlaması).upper() if SHIFT_tuşu else chr(karakter_kodlaması)
            if 자신.한글조합기.akış_tuş(karakter_verileri): return
        자신.göndermek(satır_aralığı_parça + chr(karakter_kodlaması).encode('utf-8'))


class bağla_Masaüstü:
    def __init__(자신, Süreç):
        자신.Süreç=Süreç; 자신.kilit_değer=threading.Lock(); 자신.준비완료=False; 자신.uçbirim=False; 자신.시작화면=False; 자신.bilgi_teknolojisi_kapalı=False

    def göndermek(자신, veri):
        if not veri or 자신.bilgi_teknolojisi_kapalı: return
        with 자신.kilit_değer:
            try: 자신.Süreç.stdin.write(veri); 자신.Süreç.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                veri=자신.Süreç.stdout.read(4096)
                if not veri: break
                sys.stdout.buffer.write(veri); sys.stdout.buffer.flush()
                끝부분=(끝부분+veri)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); bilgi_teknolojisi_kapalı=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,bilgi_teknolojisi_kapalı,그림화면,종료됨)>=0:
                    자신.uçbirim=열림>max(bilgi_teknolojisi_kapalı,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,bilgi_teknolojisi_kapalı,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.göndermek(b'terminal\n')
        finally: 자신.bilgi_teknolojisi_kapalı=True

    def istemci(자신, istemci, yol):
        sunucu_değer=socket.socket(socket.AF_UNIX); sunucu_değer.settimeout(10); istemci.settimeout(10)
        klavye_girdi=klavye(자신.göndermek,lambda 한글여부:자신.göndermek(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            sunucu_değer.connect(str(yol))
            # başlangıç_durumu 협상은 순서대로 끝낸다. 이후 metinÇıktısı 가닥만 클라이언트에 쓴다.
            istemci.sendall(ÖZDEŞ_değer(sunucu_değer,12))
            sürüm_numarası=ÖZDEŞ_değer(istemci,12)
            if sürüm_numarası not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            sunucu_değer.sendall(sürüm_numarası)
            öğe_BAĞ_DEĞ_SAY=ÖZDEŞ_değer(sunucu_değer,1);istemci.sendall(öğe_BAĞ_DEĞ_SAY+ÖZDEŞ_değer(sunucu_değer,öğe_BAĞ_DEĞ_SAY[0]))
            Güvenlik=ÖZDEŞ_değer(istemci,1)
            if Güvenlik!=b'\x01': raise ValueError('unexpected security type')
            sunucu_değer.sendall(Güvenlik)
            if sürüm_numarası==b'RFB 003.008\n':istemci.sendall(ÖZDEŞ_değer(sunucu_değer,4))
            sunucu_değer.sendall(ÖZDEŞ_değer(istemci,1))
            초기값=ÖZDEŞ_değer(sunucu_değer,24)
            istemci.sendall(초기값+ÖZDEŞ_değer(sunucu_değer,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            istemci.settimeout(None);sunucu_değer.settimeout(None)
            def çıktı():
                try:
                    while True:
                        alan_değer=ÖZDEŞ_değer(sunucu_değer,1)[0]
                        if alan_değer==0:
                            머리=ÖZDEŞ_değer(sunucu_değer,3);girdi_BAĞ_DEĞ_SAY=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 uzak_değer 포인터의 중복을 피한다.
                            Gizli_değer=포인터지원
                            if Gizli_değer:istemci.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            istemci.sendall(bytes([alan_değer])+머리)
                            for _ in range(girdi_BAĞ_DEĞ_SAY):
                                dikdörtgen=ÖZDEŞ_değer(sunucu_değer,12);가로,Dikey_konum,폭,높이,kodlama_değer=struct.unpack('>HHHHi',dikdörtgen)
                                if kodlama_değer!=0:raise ValueError('unexpected framebuffer encoding: '+str(kodlama_değer))
                                istemci.sendall(dikdörtgen)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    veri=ÖZDEŞ_değer(sunucu_değer,min(남음,65536));istemci.sendall(veri);남음-=len(veri)
                        elif alan_değer==1:
                            머리=ÖZDEŞ_değer(sunucu_değer,5);öğe_BAĞ_DEĞ_SAY=struct.unpack('>H',머리[3:])[0]
                            istemci.sendall(bytes([alan_değer])+머리+ÖZDEŞ_değer(sunucu_değer,öğe_BAĞ_DEĞ_SAY*6))
                        elif alan_değer==2:istemci.sendall(bytes([alan_değer]))
                        elif alan_değer==3:
                            머리=ÖZDEŞ_değer(sunucu_değer,7);öğe_BAĞ_DEĞ_SAY=struct.unpack('>I',머리[3:])[0]
                            if öğe_BAĞ_DEĞ_SAY>1048576:raise ValueError('server clipboard too large')
                            istemci.sendall(bytes([alan_değer])+머리+ÖZDEŞ_değer(sunucu_değer,öğe_BAĞ_DEĞ_SAY))
                        else:raise ValueError('unexpected RFB server message: '+str(alan_değer))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:istemci.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            arkaPlanGörevi=threading.Thread(target=çıktı,daemon=True);arkaPlanGörevi.start()
            while not 자신.bilgi_teknolojisi_kapalı:
                alan_değer=ÖZDEŞ_değer(istemci,1)[0]
                if alan_değer==4:
                    gövde_metni=ÖZDEŞ_değer(istemci,7); klavye_girdi.누름값(gövde_metni[0]!=0,struct.unpack('>I',gövde_metni[3:])[0]); continue
                if alan_değer==255:
                    gövde_metni=ÖZDEŞ_değer(istemci,11)
                    if gövde_metni[0]!=0: raise ValueError('unsupported QEMU input extension')
                    klavye_girdi.누름값(struct.unpack('>H',gövde_metni[1:3])[0]!=0,struct.unpack('>I',gövde_metni[3:7])[0]); continue
                if alan_değer==5:
                    gövde_metni=ÖZDEŞ_değer(istemci,5); 단추들,x_koordinatı,Y_koordinat=struct.unpack('>BHH',gövde_metni)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: klavye_girdi.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_koordinatı<576 and 112<=Y_koordinat<372:
                        ARA_Dizin=(Y_koordinat-112)//52
                        if (Y_koordinat-112)%52<40 and ARA_Dizin<5: 자신.göndermek(bytes([ord('1')+ARA_Dizin]))
                    else: 자신.göndermek(bytes([30,1,단추들,x_koordinatı&255,x_koordinatı>>8,Y_koordinat&255,Y_koordinat>>8]))
                    continue
                if alan_değer==6:
                    gövde_metni=ÖZDEŞ_değer(istemci,7); süre_değer=struct.unpack('>i',gövde_metni[3:])[0]
                    if abs(süre_değer)>65536: raise ValueError('clipboard too large')
                    metin=ÖZDEŞ_değer(istemci,abs(süre_değer))
                    if süre_değer>=0:
                        try: klavye_girdi.pano_değer=metin.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: klavye_girdi.pano_değer=metin.decode('latin-1').encode('utf-8')
                        klavye_girdi.pano_değer=klavye_girdi.pano_değer[:65536].decode('utf-8','ignore').encode('utf-8')
                    sunucu_değer.sendall(bytes([alan_değer])+gövde_metni+metin); continue
                if alan_değer==0:
                    gövde_metni=ÖZDEŞ_değer(istemci,19)
                    if gövde_metni[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=gövde_metni[3]//8
                elif alan_değer==2:
                    gövde_metni=ÖZDEŞ_değer(istemci,3); girdi_BAĞ_DEĞ_SAY=struct.unpack('>H',gövde_metni[1:])[0]
                    if girdi_BAĞ_DEĞ_SAY>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(girdi_BAĞ_DEĞ_SAY)+'i',ÖZDEŞ_değer(istemci,girdi_BAĞ_DEĞ_SAY*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 varsayılan_değer Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    gövde_metni=struct.pack('>BHi',0,1,0)
                elif alan_değer in (3,150): gövde_metni=ÖZDEŞ_değer(istemci,9)
                elif alan_değer==248:
                    gövde_metni=ÖZDEŞ_değer(istemci,8)
                    if gövde_metni[7]>64: raise ValueError('fence too large')
                    gövde_metni+=ÖZDEŞ_değer(istemci,gövde_metni[7])
                elif alan_değer==250: gövde_metni=ÖZDEŞ_değer(istemci,3)
                elif alan_değer==251:
                    gövde_metni=ÖZDEŞ_değer(istemci,7)
                    if gövde_metni[5]>16: raise ValueError('too many screens')
                    gövde_metni+=ÖZDEŞ_değer(istemci,gövde_metni[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(alan_değer))
                sunucu_değer.sendall(bytes([alan_değer])+gövde_metni)
        except (OSError,EOFError,ValueError) as hata:
            if str(hata): print('VNC client:',hata,file=sys.stderr,flush=True)
        finally:
            for yuva_değer in (istemci,sunucu_değer):
                try: yuva_değer.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                yuva_değer.close()


def çalıştırma_Masaüstü(bağlantı_noktası_numarası=5902, ağ=False, dosya_aktarımı_bağlantı_noktası_numarası=2121, 전달규칙들=(), çözme_değer=(640, 480), konuk_ADRES=None, konak_ADRES='127.0.0.1'):
    with ExitStack() as Kaynaklar, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        köprü_girdi = None
        if ağ:
            from köprü_3de4fe3a import köprü_3de4fe3a
            köprü_girdi = Kaynaklar.enter_context(köprü_3de4fe3a(dosya_aktarımı_bağlantı_noktası_numarası, 전달규칙들, konuk_ADRES=konuk_ADRES, konak_ADRES=konak_ADRES))
        yol=Path(작업경로)/'display.sock'
        with socket.socket() as almak_taşımak:
            almak_taşımak.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            almak_taşımak.bind(('127.0.0.1',bağlantı_noktası_numarası)); almak_taşımak.listen(1); almak_taşımak.settimeout(.2)
            원격화면접속번호=almak_taşımak.getsockname()[1]
            if köprü_girdi and (원격화면접속번호==dosya_aktarımı_bağlantı_noktası_numarası or 50000<=원격화면접속번호<=50007 or any(ağ_ABI=='tcp' and konak==원격화면접속번호 for ağ_ABI,konak,_ in köprü_girdi.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Süreç=subprocess.Popen(komut(çözme_değer)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(yol)]+(köprü_girdi.전달인수() if köprü_girdi else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            köprü=bağla_Masaüstü(Süreç); Okuyucu=threading.Thread(target=köprü.직렬입출력,daemon=True); Okuyucu.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(almak_taşımak.getsockname()[1]),flush=True)
            if köprü_girdi: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(konak_ADRES,dosya_aktarımı_bağlantı_noktası_numarası),flush=True)
            def sonlandırmak(신호번호,yürütme_kare): raise KeyboardInterrupt()
            Önceki=signal.signal(signal.SIGTERM,sonlandırmak)
            işleniyor_Görev=None; 가로채기됨=False
            try:
                while Süreç.poll() is None:
                    try: istemci,_=almak_taşımak.accept()
                    except socket.timeout: continue
                    if işleniyor_Görev is not None and işleniyor_Görev.is_alive(): istemci.close(); continue
                    if not yol.exists(): istemci.close(); continue
                    işleniyor_Görev=threading.Thread(target=köprü.istemci,args=(istemci,yol),daemon=True); işleniyor_Görev.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                köprü.bilgi_teknolojisi_kapalı=True
                if köprü_girdi: köprü_girdi.Duraklat_olay.set()
                if Süreç.poll() is None:
                    Süreç.terminate()
                    try: Süreç.wait(timeout=5)
                    except subprocess.TimeoutExpired: Süreç.kill(); Süreç.wait()
                Okuyucu.join(timeout=2); Süreç.stdin.close(); Süreç.stdout.close(); signal.signal(signal.SIGTERM,Önceki)
            if köprü_girdi and köprü_girdi.hata: raise RuntimeError('network bridge: '+köprü_girdi.hata)
            return 0 if 가로채기됨 else Süreç.returncode


if __name__=='__main__':
    from yürütmek_komut import 해상도읽기
    ayrıştırıcı=argparse.ArgumentParser(description=__doc__); ayrıştırıcı.add_argument('--port',type=int,default=5902)
    ayrıştırıcı.add_argument('--resolution',type=해상도읽기,default=(640,480))
    ayrıştırıcı.add_argument('--network',action='store_true'); ayrıştırıcı.add_argument('--ftp-port',type=int,default=2121)
    ayrıştırıcı.add_argument('--forward',action='append',default=[])
    bağımsız_değişken_DİZİ=ayrıştırıcı.parse_args()
    if bağımsız_değişken_DİZİ.forward and not bağımsız_değişken_DİZİ.network: ayrıştırıcı.error('--forward requires --network')
    raise SystemExit(çalıştırma_Masaüstü(bağımsız_değişken_DİZİ.port,ağ=bağımsız_değişken_DİZİ.network,dosya_aktarımı_bağlantı_noktası_numarası=bağımsız_değişken_DİZİ.ftp_port,전달규칙들=bağımsız_değişken_DİZİ.forward,çözme_değer=bağımsız_değişken_DİZİ.resolution))
