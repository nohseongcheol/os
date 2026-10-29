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
from Plocha_pohled import STEJNÉ_HODNOTA
from 예제되돌림서버 import zobrazení_výsledků_Servery
from Provést_příkaz import akce_kořen


def test_Jazyk(Jazyk,zobrazení_výsledků_server_položka,KV_data):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));přenos_souborů_číslo_portu=임시자원.getsockname()[1]
    Proces=subprocess.Popen(['python3',str(akce_kořen/'nástroje/Provést_příkaz.py'),'--desktop','--network','--port','0','--ftp-port',str(přenos_souborů_číslo_portu)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    selektor=selectors.DefaultSelector();selektor.register(Proces.stdout,selectors.EVENT_READ)
    přepis=bytearray();klient=None;přenos_souborů_kontakt=None
    def dostat_e_mail(značka,Spustit_2=0):
        konec_POSUN=time.monotonic()+60
        while značka not in přepis[Spustit_2:]:
            if time.monotonic()>konec_POSUN or Proces.poll() is not None:raise AssertionError(přepis[Spustit_2:].decode('utf-8','replace'))
            for 누름값,_ in selektor.select(.1):
                data=누름값.fileobj.read(65536)
                if data:přepis.extend(data)
        return přepis[Spustit_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(symbol_HODNOTA,누르는중=True):klient.sendall(struct.pack('>BBHI',4,int(누르는중),0,symbol_HODNOTA))
    def START_POSUN(vstupní_řádek):
        Spustit_2=len(přepis)
        for bod_kódu in vstupní_řádek+'\n':
            symbol_HODNOTA=0xff0d if bod_kódu=='\n' else ord(bod_kódu) if ord(bod_kódu)<256 else 0x1000000|ord(bod_kódu)
            누름값(symbol_HODNOTA);누름값(symbol_HODNOTA,False)
        return Spustit_2
    def prostředí(vstupní_řádek):return dostat_e_mail(b'jkoros-native> ',START_POSUN(vstupní_řádek))
    def Provést_příkaz(vstupní_řádek,예상결과):
        text=prostředí(vstupní_řádek);assert 예상결과 in text and 'exit 0' in text,(vstupní_řádek,text)
        return text
    def 화소들():
        klient.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            oblast_HODNOTA=STEJNÉ_HODNOTA(klient,1)[0]
            if oblast_HODNOTA==2:continue
            if oblast_HODNOTA==3:
                zboží_POČET=struct.unpack('>I',STEJNÉ_HODNOTA(klient,7)[3:])[0];STEJNÉ_HODNOTA(klient,zboží_POČET);continue
            assert oblast_HODNOTA==0,oblast_HODNOTA
            položka_POČET=struct.unpack('>H',STEJNÉ_HODNOTA(klient,3)[1:])[0]
            for _ in range(položka_POČET):
                souřadnice_x,Y_souřadnice,너비값,vyžádáno_výška_HODNOTA,znaková_sada=struct.unpack('>HHHHi',STEJNÉ_HODNOTA(klient,12));assert znaková_sada==0,znaková_sada
                data=STEJNÉ_HODNOTA(klient,너비값*vyžádáno_výška_HODNOTA*4)
                for ŘÁDEK_pozice in range(vyžádáno_výška_HODNOTA):
                    for SLOUPEC_pozice in range(너비값):
                        원본자료=(ŘÁDEK_pozice*너비값+SLOUPEC_pozice)*4;cílová_úroveň=((Y_souřadnice+ŘÁDEK_pozice)*640+souřadnice_x+SLOUPEC_pozice)*3
                        빛삼원색[cílová_úroveň:cílová_úroveň+3]=bytes((data[원본자료+2],data[원본자료+1],data[원본자료]))
            if položka_POČET:return 빛삼원색
    try:
        dostat_e_mail(b'TERMINAL READY');dostat_e_mail(b'jkoros-native> ',přepis.rfind(b'TERMINAL READY'))
        číslo_portu=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',přepis).group(1))
        klient=socket.create_connection(('127.0.0.1',číslo_portu),timeout=10)
        assert STEJNÉ_HODNOTA(klient,12)==b'RFB 003.008\n';klient.sendall(b'RFB 003.008\n')
        assert 1 in STEJNÉ_HODNOTA(klient,STEJNÉ_HODNOTA(klient,1)[0]);klient.sendall(b'\x01');assert STEJNÉ_HODNOTA(klient,4)==b'\0'*4
        klient.sendall(b'\x01');초기값=STEJNÉ_HODNOTA(klient,24);STEJNÉ_HODNOTA(klient,struct.unpack('>I',초기값[20:])[0])
        klient.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klient.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in prostředí('ftpd start')
        přenos_souborů_kontakt=ftplib.FTP();přenos_souborů_kontakt.encoding='utf-8';přenos_souborů_kontakt.connect('127.0.0.1',přenos_souborů_číslo_portu,timeout=20);přenos_souborů_kontakt.login()
        vytížení_data=('GUI와 FTP 동시 použít_HODNOTA '+Jazyk+' 😀\n').encode()
        přenos_souborů_kontakt.storbinary('STOR 함께.txt',io.BytesIO(vytížení_data))
        assert vytížení_data.decode().strip() in prostředí('cat /함께.txt')
        RECEIVED_POČET=bytearray();přenos_souborů_kontakt.retrbinary('RETR 함께.txt',RECEIVED_POČET.extend);assert RECEIVED_POČET==vytížení_data;přenos_souborů_kontakt.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        poslat_Seznam=prostředí('ls /example')
        assert all(Název in poslat_Seznam for Název in ('java/','c/','python/','README.md')),poslat_Seznam
        if Jazyk=='java':
            sada_manifest=json.loads((akce_kořen/'build/examples/manifest.json').read_text())
            for cesta_2,vstupní_bod in sada_manifest.items():
                prostředí('cp '+cesta_2+' /example-check.bin')
                Obsah_HODNOTA=bytearray();přenos_souborů_kontakt.retrbinary('RETR example-check.bin',Obsah_HODNOTA.extend)
                assert len(Obsah_HODNOTA)==vstupní_bod['bytes'] and hashlib.sha256(Obsah_HODNOTA).hexdigest()==vstupní_bod['sha256'],cesta_2
            přenos_souborů_kontakt.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binary=bytes(range(256))*64
            přenos_souborů_kontakt.storbinary('STOR boundary.bin',io.BytesIO(binary))
            Obsah_HODNOTA=bytearray();přenos_souborů_kontakt.retrbinary('RETR boundary.bin',Obsah_HODNOTA.extend)
            assert Obsah_HODNOTA==binary and 'boundary.bin' in přenos_souborů_kontakt.nlst()
            prostředí('cp /boundary.bin /boundary-copy.bin')
            Obsah_HODNOTA=bytearray();přenos_souborů_kontakt.retrbinary('RETR boundary-copy.bin',Obsah_HODNOTA.extend)
            assert Obsah_HODNOTA==binary
            přenos_souborů_kontakt.delete('boundary.bin');přenos_souborů_kontakt.delete('boundary-copy.bin')
        assert 'UkázkaVýstupu' in prostředí('ls /example/'+Jazyk)
        prostředí('cd /example/'+Jazyk)
        název_tabulka={'java':'JAVA','c':'C','python':'PYTHON'}[Jazyk]
        예상파일=název_tabulka+' název_souboru: 한글 data 😀\n'
        if Jazyk=='java':
            Provést_příkaz('javac UkázkaVýstupu.java','Compiled:');Provést_příkaz('java UkázkaVýstupu','JAVA výstupní_pozice: 안녕하세요 😀')
            Provést_příkaz('javac UkázkaSouboru.java','Compiled:');Provést_příkaz('java UkázkaSouboru',예상파일)
            Provést_příkaz('java UkázkaSítě {} {}'.format(zobrazení_výsledků_server_položka.port_TCP,zobrazení_výsledků_server_položka.protokol_UDP_port),'JAVA 네트워크 ověřit: TCP UDP 한글')
            grafika_příkaz='java UkázkaKreslení'
        elif Jazyk=='c':
            for Název,전달값,예상결과 in [('výstupní_pozice','', 'C výstupní_pozice: 안녕하세요 😀'),('název_souboru','',예상파일),
                    ('네트워크',' '+str(zobrazení_výsledků_server_položka.protokol_UDP_port),'C 네트워크 ověřit: UDP 한글')]:
                Provést_příkaz('cc '+Název+'예제.c -o Provést_příkaz','Compiled native ARM64 ELF:')
                Provést_příkaz('./Provést_příkaz'+전달값,예상결과)
            Provést_příkaz('cc UkázkaKreslení.c -o Provést_příkaz','Compiled native ARM64 ELF:');grafika_příkaz='./Provést_příkaz'
        else:
            for Název,전달값,예상결과 in [('výstupní_pozice','','PYTHON výstupní_pozice: 안녕하세요 😀'),('název_souboru','',예상파일),
                    ('네트워크',' '+str(zobrazení_výsledků_server_položka.protokol_UDP_port),'PYTHON 네트워크 ověřit: UDP 한글')]:
                Provést_příkaz('python '+Název+'예제.py'+전달값,예상결과)
            grafika_příkaz='python UkázkaKreslení.py'
        START_kreslení=START_POSUN(grafika_příkaz)
        text=dostat_e_mail('그림을 확인한 BACK_HODNOTA Enter를 누르세요.\r\n'.encode(),START_kreslení)
        assert název_tabulka+' 그래픽: 빨강 초록 파랑' in text and 'exit 0' not in text,text
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        přenos_souborů_kontakt.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_POČET=bytearray();přenos_souborů_kontakt.retrbinary('RETR 도중.txt',RECEIVED_POČET.extend);assert RECEIVED_POČET==b'FTP DURING GRAPHICS';přenos_souborů_kontakt.delete('도중.txt')
        빛삼원색=화소들()
        for Y_souřadnice,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            POSUN_HODNOTA=(Y_souřadnice*640+610)*3;assert tuple(빛삼원색[POSUN_HODNOTA:POSUN_HODNOTA+3])==색상,(Jazyk,Y_souřadnice,tuple(빛삼원색[POSUN_HODNOTA:POSUN_HODNOTA+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KV_data/(Jazyk+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in dostat_e_mail(b'jkoros-native> ',START_kreslení)
        if Jazyk=='java':
            START_okno=START_POSUN('java UkázkaOkna')
            dostat_e_mail('GUI 예제 Připravit: UkázkaOkna'.encode(),START_okno)
            def klepnout_HODNOTA(가로,Svislá_pozice):
                for tlačítko in (1,0):klient.sendall(struct.pack('>BBHH',5,tlačítko,가로,Svislá_pozice))
            time.sleep(.3)
            Předchozí_image=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klepnout_HODNOTA(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for znak_HODNOTA in '한글':누름값(0x1000000|ord(znak_HODNOTA));누름값(0x1000000|ord(znak_HODNOTA),False)
            for opakování_POČET in (1,2):
                Spustit_2=len(přepis);klepnout_HODNOTA(180,242)
                dostat_e_mail(('GUI 인사: 안녕하세요, 한글님! ('+str(opakování_POČET)+')').encode(),Spustit_2)
            time.sleep(.3)
            okno_kreslení=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert Předchozí_image.crop((110,272,530,300)).tobytes()!=okno_kreslení.crop((110,272,530,300)).tobytes()
            okno_kreslení.save(str(KV_data/'java-swing.png'))
            Spustit_2=len(přepis);klepnout_HODNOTA(535,105)
            assert 'exit 0' in dostat_e_mail(b'jkoros-native> ',Spustit_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Soubor_položka_název={'java':'java.txt','c':'c.txt','python':'python.txt'}[Jazyk]
        prostředí('cp '+Soubor_položka_název+' /ověřit_5fb2b747.txt')
        RECEIVED_POČET=bytearray();přenos_souborů_kontakt.retrbinary('RETR ověřit_5fb2b747.txt',RECEIVED_POČET.extend);assert RECEIVED_POČET==예상파일.encode()
        prostředí('echo preserved > UkázkaVýstupu.'+('py' if Jazyk=='python' else Jazyk))
        assert 'EXAMPLES READY' in prostředí('example '+Jazyk)
        assert '\npreserved\n' in prostředí('cat UkázkaVýstupu.'+('py' if Jazyk=='python' else Jazyk))
        assert '한/nula_operand Klíč_HODNOTA, Shift+Space 또는 F9' in prostředí('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in prostředí('echo GUI NETWORK TOGETHER')
        přenos_souborů_kontakt.quit();přenos_souborů_kontakt=None;assert 'FTP stopped' in prostředí('ftpd stop')
        print('PASS '+Jazyk+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if přenos_souborů_kontakt:
            try:přenos_souborů_kontakt.close()
            except OSError:pass
        if klient:klient.close()
        Proces.terminate()
        try:Proces.wait(timeout=8)
        except subprocess.TimeoutExpired:Proces.kill();Proces.wait()
        selektor.close();Proces.stdout.close();(KV_data/(Jazyk+'-serial.log')).write_bytes(přepis)


def Spustit_2():
    KV_data=akce_kořen/'build/verification/examples';KV_data.mkdir(parents=True,exist_ok=True)
    ověření_Zpráva={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akce_kořen/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with zobrazení_výsledků_Servery() as zobrazení_výsledků_server_položka:
            for Jazyk in ('java','c','python'):
                test_Jazyk(Jazyk,zobrazení_výsledků_server_položka,KV_data);ověření_Zpráva['languages'].append(Jazyk)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert zobrazení_výsledků_server_položka.수신됨==[(oblast_HODNOTA,data.encode()) for oblast_HODNOTA,data in 예상결과],zobrazení_výsledků_server_položka.수신됨
            ověření_Zpráva['host_network_payloads']=[{'protocol':oblast_HODNOTA,'text':data.decode()} for oblast_HODNOTA,data in zobrazení_výsledků_server_položka.수신됨]
        ověření_Zpráva.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KV_data/'report.json').write_text(json.dumps(ověření_Zpráva,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Spustit_2()
