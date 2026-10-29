#!/usr/bin/env python3
"""fiili_veri RFB 클라이언트로 QEMU 창의 한글/tuş_değer/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from Masaüstü_Görünüm import ÖZDEŞ_değer
from yürütmek_komut import işlem_kök


def çalıştır():
    çıktı=işlem_kök/'build/verification/desktop'; çıktı.mkdir(parents=True,exist_ok=True)
    Süreç=subprocess.Popen(['python3',str(işlem_kök/'araçlar/Masaüstü_Görünüm.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Süreç.stdout,selectors.EVENT_READ)
    döküm=bytearray(); doğrulama_Rapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((işlem_kök/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(işaret,çalıştır=0):
        son_tarih_saat=time.monotonic()+45
        while işaret not in döküm[çalıştır:]:
            if time.monotonic()>son_tarih_saat or Süreç.poll() is not None: raise AssertionError(döküm[çalıştır:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                veri=누름값.fileobj.read(4096)
                if veri: döküm.extend(veri)
        return bytes(döküm[çalıştır:])
    try:
        까지(b'TERMINAL READY')
        bağlantı_noktası_numarası=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',döküm).group(1))
        with socket.create_connection(('127.0.0.1',bağlantı_noktası_numarası),timeout=10) as istemci:
            assert ÖZDEŞ_değer(istemci,12)==b'RFB 003.008\n'; istemci.sendall(b'RFB 003.008\n')
            assert 1 in ÖZDEŞ_değer(istemci,ÖZDEŞ_değer(istemci,1)[0]); istemci.sendall(b'\x01'); assert ÖZDEŞ_değer(istemci,4)==b'\0'*4
            istemci.sendall(b'\x01'); 초기값=ÖZDEŞ_değer(istemci,24); assert struct.unpack('>HH',초기값[:4])==(640,480); ÖZDEŞ_değer(istemci,struct.unpack('>I',초기값[20:])[0])
            istemci.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            istemci.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(simge_değer,누르는중=True): istemci.sendall(struct.pack('>BBHI',4,int(누르는중),0,simge_değer))
            def 글자입력(metin):
                for karakter_verileri in metin:
                    simge=0xff0d if karakter_verileri=='\n' else ord(karakter_verileri) if ord(karakter_verileri)<256 else 0x01000000|ord(karakter_verileri)
                    누름값(simge); 누름값(simge,False)
            def bas_tuş(simge_değer): 누름값(simge_değer); 누름값(simge_değer,False)
            # Start with English keys only, as delivered without a host IME.
            Ofset_değer=len(döküm); 글자입력('echo '); bas_tuş(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); bas_tuş(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Ofset_değer)
            Ofset_değer=len(döküm); 글자입력('echo ')
            누름값(0xffe1); bas_tuş(32); 누름값(0xffe1,False)
            글자입력('dlfr'); bas_tuş(0xff08); bas_tuş(0xff08); 글자입력('fr')
            bas_tuş(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),Ofset_değer)
            Ofset_değer=len(döküm); 글자입력('echo '); bas_tuş(0xff31)
            글자입력('rhk rkqtk RkRnd'); bas_tuş(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),Ofset_değer)
            # The same composition edits UTF-8 text in the native vi editor.
            Ofset_değer=len(döküm); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',Ofset_değer)
            글자입력('i'); bas_tuş(0xffc6); 글자입력('gksrmf dlfr'); bas_tuş(0xffc6)
            bas_tuş(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',Ofset_değer)
            Ofset_değer=len(döküm); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),Ofset_değer); 까지(b'jkoros-native> ',Ofset_değer)
            Ofset_değer=len(döküm); 글자입력('help ko\n')
            까지('한/sıfır_işlenen tuş_değer, Shift+Space 또는 F9'.encode(),Ofset_değer); 까지(b'jkoros-native> ',Ofset_değer)
            Ofset_değer=len(döküm); 글자입력('clear\necho "VNC 한글 artış_değer 😀"\n'); 까지('VNC 한글 artış_değer 😀\r\n'.encode(),Ofset_değer)
            Ofset_değer=len(döküm); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',Ofset_değer)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            pano_değer='echo "yapıştırmak_değer 완료"\n'.encode(); Ofset_değer=len(döküm)
            istemci.sendall(struct.pack('>B3xI',6,len(pano_değer))+pano_değer)
            for Olay,_ in 준비살피미.select(.15):
                veri_bloğu=Olay.fileobj.read(4096)
                if veri_bloğu: döküm.extend(veri_bloğu)
            assert 'yapıştırmak_değer 완료'.encode() not in döküm[Ofset_değer:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),Ofset_değer)
            istemci.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                uyarı_SMS=ÖZDEŞ_değer(istemci,1)[0]
                if uyarı_SMS==2: continue
                if uyarı_SMS==3:
                    Boyut=struct.unpack('>I',ÖZDEŞ_değer(istemci,7)[3:])[0]; ÖZDEŞ_değer(istemci,Boyut); continue
                assert uyarı_SMS==0,uyarı_SMS
                사각형들=struct.unpack('>H',ÖZDEŞ_değer(istemci,3)[1:])[0]
                for _ in range(사각형들):
                    x_koordinatı,Y_koordinat,너비값,높이값,karakter_kümesi=struct.unpack('>HHHHi',ÖZDEŞ_değer(istemci,12)); assert karakter_kümesi==0,karakter_kümesi
                    화소들=ÖZDEŞ_değer(istemci,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; hedef_ADRES_08bbd577=((Y_koordinat+안쪽순번)*640+x_koordinatı+순번)*3
                            빛삼원색[hedef_ADRES_08bbd577:hedef_ADRES_08bbd577+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (çıktı/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(çıktı/'vnc-terminal.png'))
            Ofset_değer=len(döküm)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',Ofset_değer)
            Ofset_değer=len(döküm); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',Ofset_değer)
            Ofset_değer=len(döküm); istemci.sendall(struct.pack('>BBHH',5,1,576,81)); istemci.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',Ofset_değer)
            Ofset_değer=len(döküm); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',Ofset_değer)
            assert len(döküm)-Ofset_değer>8192,'exercise output longer than bridge status buffer'
            Ofset_değer=len(döküm); istemci.sendall(struct.pack('>BBHH',5,1,560,63)); istemci.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',Ofset_değer)
            Ofset_değer=len(döküm); istemci.sendall(struct.pack('>BBHH',5,1,80,16)); istemci.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',Ofset_değer)
            Ofset_değer=len(döküm); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',Ofset_değer)
            Ofset_değer=len(döküm); 글자입력('gui\n'); 까지(b'GUI READY:',Ofset_değer)
            Ofset_değer=len(döküm); istemci.sendall(struct.pack('>BBHH',5,1,80,332)); istemci.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',Ofset_değer)
            doğrulama_Rapor.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Süreç.poll() is None:
            Süreç.terminate()
            try: Süreç.wait(timeout=8)
            except subprocess.TimeoutExpired: Süreç.kill(); Süreç.wait()
        준비살피미.close(); Süreç.stdout.close()
        (çıktı/'serial.log').write_bytes(döküm)
        (çıktı/'report.json').write_text(json.dumps(doğrulama_Rapor,indent=2)+'\n')


if __name__=='__main__': çalıştır()
