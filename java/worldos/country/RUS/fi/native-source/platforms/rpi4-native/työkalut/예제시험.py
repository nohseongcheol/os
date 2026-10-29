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
from työpöytä_Näkymä import VERTAA_ARVO
from 예제되돌림서버 import päivitys_Palvelimet
from Suorita_komento import aloite_juuri


def testi_Kieli(Kieli,päivitys_palvelin_merkintä,KR_data):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));tiedostonsiirto_portin_numero=임시자원.getsockname()[1]
    Prosessi=subprocess.Popen(['python3',str(aloite_juuri/'työkalut/Suorita_komento.py'),'--desktop','--network','--port','0','--ftp-port',str(tiedostonsiirto_portin_numero)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    valitsin=selectors.DefaultSelector();valitsin.register(Prosessi.stdout,selectors.EVENT_READ)
    transkriptio=bytearray();asiakas=None;tiedostonsiirto_yhteys=None
    def saada_sanoma(merkintä,Suorita_2=0):
        lopettaa_puhelu_SIIRTYMÄ=time.monotonic()+60
        while merkintä not in transkriptio[Suorita_2:]:
            if time.monotonic()>lopettaa_puhelu_SIIRTYMÄ or Prosessi.poll() is not None:raise AssertionError(transkriptio[Suorita_2:].decode('utf-8','replace'))
            for 누름값,_ in valitsin.select(.1):
                data=누름값.fileobj.read(65536)
                if data:transkriptio.extend(data)
        return transkriptio[Suorita_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(symboli_ARVO,누르는중=True):asiakas.sendall(struct.pack('>BBHI',4,int(누르는중),0,symboli_ARVO))
    def alku_SIIRTYMÄ(syöterivi):
        Suorita_2=len(transkriptio)
        for merkkikoodi in syöterivi+'\n':
            symboli_ARVO=0xff0d if merkkikoodi=='\n' else ord(merkkikoodi) if ord(merkkikoodi)<256 else 0x1000000|ord(merkkikoodi)
            누름값(symboli_ARVO);누름값(symboli_ARVO,False)
        return Suorita_2
    def liittymä(syöterivi):return saada_sanoma(b'jkoros-native> ',alku_SIIRTYMÄ(syöterivi))
    def Suorita_komento(syöterivi,예상결과):
        teksti=liittymä(syöterivi);assert 예상결과 in teksti and 'exit 0' in teksti,(syöterivi,teksti)
        return teksti
    def 화소들():
        asiakas.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            alue_ARVO=VERTAA_ARVO(asiakas,1)[0]
            if alue_ARVO==2:continue
            if alue_ARVO==3:
                kohde_LASKE=struct.unpack('>I',VERTAA_ARVO(asiakas,7)[3:])[0];VERTAA_ARVO(asiakas,kohde_LASKE);continue
            assert alue_ARVO==0,alue_ARVO
            merkintä_LASKE=struct.unpack('>H',VERTAA_ARVO(asiakas,3)[1:])[0]
            for _ in range(merkintä_LASKE):
                x_koordinaatti,Y_koordinaatti,너비값,높이값,merkistö=struct.unpack('>HHHHi',VERTAA_ARVO(asiakas,12));assert merkistö==0,merkistö
                data=VERTAA_ARVO(asiakas,너비값*높이값*4)
                for RIVI_toimi in range(높이값):
                    for SARAKE_toimi in range(너비값):
                        원본자료=(RIVI_toimi*너비값+SARAKE_toimi)*4;tavoite=((Y_koordinaatti+RIVI_toimi)*640+x_koordinaatti+SARAKE_toimi)*3
                        빛삼원색[tavoite:tavoite+3]=bytes((data[원본자료+2],data[원본자료+1],data[원본자료]))
            if merkintä_LASKE:return 빛삼원색
    try:
        saada_sanoma(b'TERMINAL READY');saada_sanoma(b'jkoros-native> ',transkriptio.rfind(b'TERMINAL READY'))
        portin_numero=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transkriptio).group(1))
        asiakas=socket.create_connection(('127.0.0.1',portin_numero),timeout=10)
        assert VERTAA_ARVO(asiakas,12)==b'RFB 003.008\n';asiakas.sendall(b'RFB 003.008\n')
        assert 1 in VERTAA_ARVO(asiakas,VERTAA_ARVO(asiakas,1)[0]);asiakas.sendall(b'\x01');assert VERTAA_ARVO(asiakas,4)==b'\0'*4
        asiakas.sendall(b'\x01');초기값=VERTAA_ARVO(asiakas,24);VERTAA_ARVO(asiakas,struct.unpack('>I',초기값[20:])[0])
        asiakas.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        asiakas.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in liittymä('ftpd start')
        tiedostonsiirto_yhteys=ftplib.FTP();tiedostonsiirto_yhteys.encoding='utf-8';tiedostonsiirto_yhteys.connect('127.0.0.1',tiedostonsiirto_portin_numero,timeout=20);tiedostonsiirto_yhteys.login()
        tiedot_data=('GUI와 FTP 동시 käyttö_ARVO '+Kieli+' 😀\n').encode()
        tiedostonsiirto_yhteys.storbinary('STOR 함께.txt',io.BytesIO(tiedot_data))
        assert tiedot_data.decode().strip() in liittymä('cat /함께.txt')
        SAATU_HINTA_LASKE=bytearray();tiedostonsiirto_yhteys.retrbinary('RETR 함께.txt',SAATU_HINTA_LASKE.extend);assert SAATU_HINTA_LASKE==tiedot_data;tiedostonsiirto_yhteys.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        lähettää_luettelo=liittymä('ls /example')
        assert all(Nimi in lähettää_luettelo for Nimi in ('java/','c/','python/','README.md')),lähettää_luettelo
        if Kieli=='java':
            nippu_kokoonpanotiedot=json.loads((aloite_juuri/'build/examples/manifest.json').read_text())
            for polku_2,aloituskohta in nippu_kokoonpanotiedot.items():
                liittymä('cp '+polku_2+' /example-check.bin')
                Sisältö_ARVO=bytearray();tiedostonsiirto_yhteys.retrbinary('RETR example-check.bin',Sisältö_ARVO.extend)
                assert len(Sisältö_ARVO)==aloituskohta['bytes'] and hashlib.sha256(Sisältö_ARVO).hexdigest()==aloituskohta['sha256'],polku_2
            tiedostonsiirto_yhteys.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binaarinen=bytes(range(256))*64
            tiedostonsiirto_yhteys.storbinary('STOR boundary.bin',io.BytesIO(binaarinen))
            Sisältö_ARVO=bytearray();tiedostonsiirto_yhteys.retrbinary('RETR boundary.bin',Sisältö_ARVO.extend)
            assert Sisältö_ARVO==binaarinen and 'boundary.bin' in tiedostonsiirto_yhteys.nlst()
            liittymä('cp /boundary.bin /boundary-copy.bin')
            Sisältö_ARVO=bytearray();tiedostonsiirto_yhteys.retrbinary('RETR boundary-copy.bin',Sisältö_ARVO.extend)
            assert Sisältö_ARVO==binaarinen
            tiedostonsiirto_yhteys.delete('boundary.bin');tiedostonsiirto_yhteys.delete('boundary-copy.bin')
        assert 'Tulostusesimerkki' in liittymä('ls /example/'+Kieli)
        liittymä('cd /example/'+Kieli)
        nimi_taulukko={'java':'JAVA','c':'C','python':'PYTHON'}[Kieli]
        예상파일=nimi_taulukko+' tiedoston_nimi: 한글 data 😀\n'
        if Kieli=='java':
            Suorita_komento('javac Tulostusesimerkki.java','Compiled:');Suorita_komento('java Tulostusesimerkki','JAVA tulostuspaikka: 안녕하세요 😀')
            Suorita_komento('javac Tiedostoesimerkki.java','Compiled:');Suorita_komento('java Tiedostoesimerkki',예상파일)
            Suorita_komento('java Verkkoesimerkki {} {}'.format(päivitys_palvelin_merkintä.TCP_portti,päivitys_palvelin_merkintä.UDP_portti),'JAVA 네트워크 tarkistaa: TCP UDP 한글')
            grafiikka_komento='java Piirtoesimerkki'
        elif Kieli=='c':
            for Nimi,전달값,예상결과 in [('tulostuspaikka','', 'C tulostuspaikka: 안녕하세요 😀'),('tiedoston_nimi','',예상파일),
                    ('네트워크',' '+str(päivitys_palvelin_merkintä.UDP_portti),'C 네트워크 tarkistaa: UDP 한글')]:
                Suorita_komento('cc '+Nimi+'예제.c -o Suorita_komento','Compiled native ARM64 ELF:')
                Suorita_komento('./Suorita_komento'+전달값,예상결과)
            Suorita_komento('cc Piirtoesimerkki.c -o Suorita_komento','Compiled native ARM64 ELF:');grafiikka_komento='./Suorita_komento'
        else:
            for Nimi,전달값,예상결과 in [('tulostuspaikka','','PYTHON tulostuspaikka: 안녕하세요 😀'),('tiedoston_nimi','',예상파일),
                    ('네트워크',' '+str(päivitys_palvelin_merkintä.UDP_portti),'PYTHON 네트워크 tarkistaa: UDP 한글')]:
                Suorita_komento('python '+Nimi+'예제.py'+전달값,예상결과)
            grafiikka_komento='python Piirtoesimerkki.py'
        alku_piirustus=alku_SIIRTYMÄ(grafiikka_komento)
        teksti=saada_sanoma('그림을 확인한 BACK_ARVO Enter를 누르세요.\r\n'.encode(),alku_piirustus)
        assert nimi_taulukko+' 그래픽: 빨강 초록 파랑' in teksti and 'exit 0' not in teksti,teksti
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        tiedostonsiirto_yhteys.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        SAATU_HINTA_LASKE=bytearray();tiedostonsiirto_yhteys.retrbinary('RETR 도중.txt',SAATU_HINTA_LASKE.extend);assert SAATU_HINTA_LASKE==b'FTP DURING GRAPHICS';tiedostonsiirto_yhteys.delete('도중.txt')
        빛삼원색=화소들()
        for Y_koordinaatti,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            SIIRTYMÄ_ARVO=(Y_koordinaatti*640+610)*3;assert tuple(빛삼원색[SIIRTYMÄ_ARVO:SIIRTYMÄ_ARVO+3])==색상,(Kieli,Y_koordinaatti,tuple(빛삼원색[SIIRTYMÄ_ARVO:SIIRTYMÄ_ARVO+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_data/(Kieli+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in saada_sanoma(b'jkoros-native> ',alku_piirustus)
        if Kieli=='java':
            alku_ikkuna=alku_SIIRTYMÄ('java Ikkunaesimerkki')
            saada_sanoma('GUI 예제 Valmistele: Ikkunaesimerkki'.encode(),alku_ikkuna)
            def osoittaa_ARVO(가로,toimiala_toimi):
                for painike in (1,0):asiakas.sendall(struct.pack('>BBHH',5,painike,가로,toimiala_toimi))
            time.sleep(.3)
            Edellinen_KUVA=Image.frombytes('RGB',(640,480),bytes(화소들()))
            osoittaa_ARVO(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for merkki_ARVO in '한글':누름값(0x1000000|ord(merkki_ARVO));누름값(0x1000000|ord(merkki_ARVO),False)
            for toisto_LASKE in (1,2):
                Suorita_2=len(transkriptio);osoittaa_ARVO(180,242)
                saada_sanoma(('GUI 인사: 안녕하세요, 한글님! ('+str(toisto_LASKE)+')').encode(),Suorita_2)
            time.sleep(.3)
            ikkuna_piirustus=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert Edellinen_KUVA.crop((110,272,530,300)).tobytes()!=ikkuna_piirustus.crop((110,272,530,300)).tobytes()
            ikkuna_piirustus.save(str(KR_data/'java-swing.png'))
            Suorita_2=len(transkriptio);osoittaa_ARVO(535,105)
            assert 'exit 0' in saada_sanoma(b'jkoros-native> ',Suorita_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Tiedosto_merkintä_nimi={'java':'java.txt','c':'c.txt','python':'python.txt'}[Kieli]
        liittymä('cp '+Tiedosto_merkintä_nimi+' /vahvista.txt')
        SAATU_HINTA_LASKE=bytearray();tiedostonsiirto_yhteys.retrbinary('RETR vahvista.txt',SAATU_HINTA_LASKE.extend);assert SAATU_HINTA_LASKE==예상파일.encode()
        liittymä('echo preserved > Tulostusesimerkki.'+('py' if Kieli=='python' else Kieli))
        assert 'EXAMPLES READY' in liittymä('example '+Kieli)
        assert '\npreserved\n' in liittymä('cat Tulostusesimerkki.'+('py' if Kieli=='python' else Kieli))
        assert '한/nolla_operandi Avain_ARVO, Shift+Space 또는 F9' in liittymä('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in liittymä('echo GUI NETWORK TOGETHER')
        tiedostonsiirto_yhteys.quit();tiedostonsiirto_yhteys=None;assert 'FTP stopped' in liittymä('ftpd stop')
        print('PASS '+Kieli+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if tiedostonsiirto_yhteys:
            try:tiedostonsiirto_yhteys.close()
            except OSError:pass
        if asiakas:asiakas.close()
        Prosessi.terminate()
        try:Prosessi.wait(timeout=8)
        except subprocess.TimeoutExpired:Prosessi.kill();Prosessi.wait()
        valitsin.close();Prosessi.stdout.close();(KR_data/(Kieli+'-serial.log')).write_bytes(transkriptio)


def Suorita_2():
    KR_data=aloite_juuri/'build/verification/examples';KR_data.mkdir(parents=True,exist_ok=True)
    vahvistus_raportti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((aloite_juuri/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with päivitys_Palvelimet() as päivitys_palvelin_merkintä:
            for Kieli in ('java','c','python'):
                testi_Kieli(Kieli,päivitys_palvelin_merkintä,KR_data);vahvistus_raportti['languages'].append(Kieli)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert päivitys_palvelin_merkintä.수신됨==[(alue_ARVO,data.encode()) for alue_ARVO,data in 예상결과],päivitys_palvelin_merkintä.수신됨
            vahvistus_raportti['host_network_payloads']=[{'protocol':alue_ARVO,'text':data.decode()} for alue_ARVO,data in päivitys_palvelin_merkintä.수신됨]
        vahvistus_raportti.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_data/'report.json').write_text(json.dumps(vahvistus_raportti,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Suorita_2()
