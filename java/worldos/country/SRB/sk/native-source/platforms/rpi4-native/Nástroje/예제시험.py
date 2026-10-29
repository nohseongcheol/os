#!/usr/bin/env python3
"""Run all examples in the real combined VNC + SLIP/FTP native VM."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from počítač_zobraziť import EXACT_VALUE
from 예제되돌림서버 import ozvena_Servery
from Vykonať_príkaz import akcia_koreň


def test_Jazyky(Jazyky,ozvena_server_položka,KR_údaje):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));prenos_súborov_číslo_portu=임시자원.getsockname()[1]
    Proces=subprocess.Popen(['python3',str(akcia_koreň/'Nástroje/Vykonať_príkaz.py'),'--desktop','--network','--port','0','--ftp-port',str(prenos_súborov_číslo_portu)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    selektor=selectors.DefaultSelector();selektor.register(Proces.stdout,selectors.EVENT_READ)
    prepis=bytearray();klient=None;prenos_súborov_kontakt=None
    def dostať_e_mail(fixka,Spustiť_2=0):
        ukončiť_hovor_Posun=time.monotonic()+60
        while fixka not in prepis[Spustiť_2:]:
            if time.monotonic()>ukončiť_hovor_Posun or Proces.poll() is not None:raise AssertionError(prepis[Spustiť_2:].decode('utf-8','replace'))
            for 누름값,_ in selektor.select(.1):
                údaje=누름값.fileobj.read(65536)
                if údaje:prepis.extend(údaje)
        return prepis[Spustiť_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(symbol_VALUE,누르는중=True):klient.sendall(struct.pack('>BBHI',4,int(누르는중),0,symbol_VALUE))
    def START_Posun(riadok):
        Spustiť_2=len(prepis)
        for bod_kódu in riadok+'\n':
            symbol_VALUE=0xff0d if bod_kódu=='\n' else ord(bod_kódu) if ord(bod_kódu)<256 else 0x1000000|ord(bod_kódu)
            누름값(symbol_VALUE);누름값(symbol_VALUE,False)
        return Spustiť_2
    def 셸(riadok):return dostať_e_mail(b'jkoros-native> ',START_Posun(riadok))
    def Vykonať_príkaz(riadok,예상결과):
        Spracovanie_textu=셸(riadok);assert 예상결과 in Spracovanie_textu and 'exit 0' in Spracovanie_textu,(riadok,Spracovanie_textu)
        return Spracovanie_textu
    def 화소들():
        klient.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            oblasť_VALUE=EXACT_VALUE(klient,1)[0]
            if oblasť_VALUE==2:continue
            if oblasť_VALUE==3:
                položka_COUNT=struct.unpack('>I',EXACT_VALUE(klient,7)[3:])[0];EXACT_VALUE(klient,položka_COUNT);continue
            assert oblasť_VALUE==0,oblasť_VALUE
            položka_COUNT_8f7753a1=struct.unpack('>H',EXACT_VALUE(klient,3)[1:])[0]
            for _ in range(položka_COUNT_8f7753a1):
                X_súradnica,Y_súradnica,너비값,높이값,tabuľka_znakov=struct.unpack('>HHHHi',EXACT_VALUE(klient,12));assert tabuľka_znakov==0,tabuľka_znakov
                údaje=EXACT_VALUE(klient,너비값*높이값*4)
                for ROW_pozícia in range(높이값):
                    for COLUMN_pozícia in range(너비값):
                        원본자료=(ROW_pozícia*너비값+COLUMN_pozícia)*4;cieľová_hodnota=((Y_súradnica+ROW_pozícia)*640+X_súradnica+COLUMN_pozícia)*3
                        빛삼원색[cieľová_hodnota:cieľová_hodnota+3]=bytes((údaje[원본자료+2],údaje[원본자료+1],údaje[원본자료]))
            if položka_COUNT_8f7753a1:return 빛삼원색
    try:
        dostať_e_mail(b'TERMINAL READY');dostať_e_mail(b'jkoros-native> ',prepis.rfind(b'TERMINAL READY'))
        číslo_portu=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',prepis).group(1))
        klient=socket.create_connection(('127.0.0.1',číslo_portu),timeout=10)
        assert EXACT_VALUE(klient,12)==b'RFB 003.008\n';klient.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(klient,EXACT_VALUE(klient,1)[0]);klient.sendall(b'\x01');assert EXACT_VALUE(klient,4)==b'\0'*4
        klient.sendall(b'\x01');초기값=EXACT_VALUE(klient,24);EXACT_VALUE(klient,struct.unpack('>I',초기값[20:])[0])
        klient.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klient.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in 셸('ftpd start')
        prenos_súborov_kontakt=ftplib.FTP();prenos_súborov_kontakt.encoding='utf-8';prenos_súborov_kontakt.connect('127.0.0.1',prenos_súborov_číslo_portu,timeout=20);prenos_súborov_kontakt.login()
        údajová_časť_údaje=('GUI와 FTP 동시 používať_VALUE '+Jazyky+' 😀\n').encode()
        prenos_súborov_kontakt.storbinary('STOR 함께.txt',io.BytesIO(údajová_časť_údaje))
        assert údajová_časť_údaje.decode().strip() in 셸('cat /함께.txt')
        RECEIVED_COUNT=bytearray();prenos_súborov_kontakt.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==údajová_časť_údaje;prenos_súborov_kontakt.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        odoslať_Zoznam=셸('ls /example')
        assert all(Názov in odoslať_Zoznam for Názov in ('java/','c/','python/','README.md')),odoslať_Zoznam
        if Jazyky=='java':
            zväzok_manifest_zostáv=json.loads((akcia_koreň/'build/examples/manifest.json').read_text())
            for Cesta,položka_bod in zväzok_manifest_zostáv.items():
                셸('cp '+Cesta+' /example-check.bin')
                obsah_VALUE=bytearray();prenos_súborov_kontakt.retrbinary('RETR example-check.bin',obsah_VALUE.extend)
                assert len(obsah_VALUE)==položka_bod['bytes'] and hashlib.sha256(obsah_VALUE).hexdigest()==položka_bod['sha256'],Cesta
            prenos_súborov_kontakt.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            Binary=bytes(range(256))*64
            prenos_súborov_kontakt.storbinary('STOR boundary.bin',io.BytesIO(Binary))
            obsah_VALUE=bytearray();prenos_súborov_kontakt.retrbinary('RETR boundary.bin',obsah_VALUE.extend)
            assert obsah_VALUE==Binary and 'boundary.bin' in prenos_súborov_kontakt.nlst()
            셸('cp /boundary.bin /boundary-copy.bin')
            obsah_VALUE=bytearray();prenos_súborov_kontakt.retrbinary('RETR boundary-copy.bin',obsah_VALUE.extend)
            assert obsah_VALUE==Binary
            prenos_súborov_kontakt.delete('boundary.bin');prenos_súborov_kontakt.delete('boundary-copy.bin')
        assert 'UkážkaVýstupu' in 셸('ls /example/'+Jazyky)
        셸('cd /example/'+Jazyky)
        názov_tabuľka={'java':'JAVA','c':'C','python':'PYTHON'}[Jazyky]
        예상파일=názov_tabuľka+' Súbor: 한글 údaje 😀\n'
        if Jazyky=='java':
            Vykonať_príkaz('javac UkážkaVýstupu.java','Compiled:');Vykonať_príkaz('java UkážkaVýstupu','JAVA Výstup: 안녕하세요 😀')
            Vykonať_príkaz('javac UkážkaSúboru.java','Compiled:');Vykonať_príkaz('java UkážkaSúboru',예상파일)
            Vykonať_príkaz('java UkážkaSiete {} {}'.format(ozvena_server_položka.TCP_port,ozvena_server_položka.UDP_port),'JAVA 네트워크 overiť: TCP UDP 한글')
            grafické_prvky_príkaz='java UkážkaKreslenia'
        elif Jazyky=='c':
            for Názov,전달값,예상결과 in [('Výstup','', 'C Výstup: 안녕하세요 😀'),('Súbor','',예상파일),
                    ('네트워크',' '+str(ozvena_server_položka.UDP_port),'C 네트워크 overiť: UDP 한글')]:
                Vykonať_príkaz('cc '+Názov+'예제.c -o Vykonať_príkaz','Compiled native ARM64 ELF:')
                Vykonať_príkaz('./Vykonať_príkaz'+전달값,예상결과)
            Vykonať_príkaz('cc UkážkaKreslenia.c -o Vykonať_príkaz','Compiled native ARM64 ELF:');grafické_prvky_príkaz='./Vykonať_príkaz'
        else:
            for Názov,전달값,예상결과 in [('Výstup','','PYTHON Výstup: 안녕하세요 😀'),('Súbor','',예상파일),
                    ('네트워크',' '+str(ozvena_server_položka.UDP_port),'PYTHON 네트워크 overiť: UDP 한글')]:
                Vykonať_príkaz('python '+Názov+'예제.py'+전달값,예상결과)
            grafické_prvky_príkaz='python UkážkaKreslenia.py'
        START_kresba=START_Posun(grafické_prvky_príkaz)
        Spracovanie_textu=dostať_e_mail('그림을 확인한 BACK_VALUE Enter를 누르세요.\r\n'.encode(),START_kresba)
        assert názov_tabuľka+' 그래픽: 빨강 초록 파랑' in Spracovanie_textu and 'exit 0' not in Spracovanie_textu,Spracovanie_textu
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        prenos_súborov_kontakt.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();prenos_súborov_kontakt.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';prenos_súborov_kontakt.delete('도중.txt')
        빛삼원색=화소들()
        for Y_súradnica,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Posun_VALUE=(Y_súradnica*640+610)*3;assert tuple(빛삼원색[Posun_VALUE:Posun_VALUE+3])==색상,(Jazyky,Y_súradnica,tuple(빛삼원색[Posun_VALUE:Posun_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_údaje/(Jazyky+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in dostať_e_mail(b'jkoros-native> ',START_kresba)
        if Jazyky=='java':
            START_okno=START_Posun('java UkážkaOkna')
            dostať_e_mail('GUI 예제 Pripraviť: UkážkaOkna'.encode(),START_okno)
            def kliknúť_VALUE(가로,vertikála_pozícia):
                for Tlačidlo in (1,0):klient.sendall(struct.pack('>BBHH',5,Tlačidlo,가로,vertikála_pozícia))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            kliknúť_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for znak_VALUE in '한글':누름값(0x1000000|ord(znak_VALUE));누름값(0x1000000|ord(znak_VALUE),False)
            for 횟수 in (1,2):
                Spustiť_2=len(prepis);kliknúť_VALUE(180,242)
                dostať_e_mail(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Spustiť_2)
            time.sleep(.3)
            okno_kresba=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=okno_kresba.crop((110,272,530,300)).tobytes()
            okno_kresba.save(str(KR_údaje/'java-swing.png'))
            Spustiť_2=len(prepis);kliknúť_VALUE(535,105)
            assert 'exit 0' in dostať_e_mail(b'jkoros-native> ',Spustiť_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Súbor_položka_názov={'java':'java.txt','c':'c.txt','python':'python.txt'}[Jazyky]
        셸('cp '+Súbor_položka_názov+' /overiť_5fb2b747.txt')
        RECEIVED_COUNT=bytearray();prenos_súborov_kontakt.retrbinary('RETR overiť_5fb2b747.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        셸('echo preserved > UkážkaVýstupu.'+('py' if Jazyky=='python' else Jazyky))
        assert 'EXAMPLES READY' in 셸('example '+Jazyky)
        assert '\npreserved\n' in 셸('cat UkážkaVýstupu.'+('py' if Jazyky=='python' else Jazyky))
        assert '한/영 Kľúč_VALUE, Shift+Space 또는 F9' in 셸('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in 셸('echo GUI NETWORK TOGETHER')
        prenos_súborov_kontakt.quit();prenos_súborov_kontakt=None;assert 'FTP stopped' in 셸('ftpd stop')
        print('PASS '+Jazyky+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if prenos_súborov_kontakt:
            try:prenos_súborov_kontakt.close()
            except OSError:pass
        if klient:klient.close()
        Proces.terminate()
        try:Proces.wait(timeout=8)
        except subprocess.TimeoutExpired:Proces.kill();Proces.wait()
        selektor.close();Proces.stdout.close();(KR_údaje/(Jazyky+'-serial.log')).write_bytes(prepis)


def Spustiť_2():
    KR_údaje=akcia_koreň/'build/verification/examples';KR_údaje.mkdir(parents=True,exist_ok=True)
    overenie_správa={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akcia_koreň/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with ozvena_Servery() as ozvena_server_položka:
            for Jazyky in ('java','c','python'):
                test_Jazyky(Jazyky,ozvena_server_položka,KR_údaje);overenie_správa['languages'].append(Jazyky)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert ozvena_server_položka.수신됨==[(oblasť_VALUE,údaje.encode()) for oblasť_VALUE,údaje in 예상결과],ozvena_server_položka.수신됨
            overenie_správa['host_network_payloads']=[{'protocol':oblasť_VALUE,'text':údaje.decode()} for oblasť_VALUE,údaje in ozvena_server_položka.수신됨]
        overenie_správa.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_údaje/'report.json').write_text(json.dumps(overenie_správa,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Spustiť_2()
