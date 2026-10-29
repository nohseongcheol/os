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
from Asztal_Nézet import AZONOS_ÉRTÉK
from 예제되돌림서버 import visszhang_Kiszolgálók
from végrehajt_parancs import teendő_gyök


def teszt_Nyelv(Nyelv,visszhang_kiszolgáló_bejegyzés,KR_adat):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));fájlátvitel_portszám=임시자원.getsockname()[1]
    Folyamat=subprocess.Popen(['python3',str(teendő_gyök/'Eszközök/végrehajt_parancs.py'),'--desktop','--network','--port','0','--ftp-port',str(fájlátvitel_portszám)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    szelektor=selectors.DefaultSelector();szelektor.register(Folyamat.stdout,selectors.EVENT_READ)
    átirat=bytearray();kliens=None;fájlátvitel_ismerős=None
    def fogad_e_mail(jelölő,Futtatás=0):
        megszüntet_Ofszet=time.monotonic()+60
        while jelölő not in átirat[Futtatás:]:
            if time.monotonic()>megszüntet_Ofszet or Folyamat.poll() is not None:raise AssertionError(átirat[Futtatás:].decode('utf-8','replace'))
            for 누름값,_ in szelektor.select(.1):
                adat=누름값.fileobj.read(65536)
                if adat:átirat.extend(adat)
        return átirat[Futtatás:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(szimbólum_ÉRTÉK,누르는중=True):kliens.sendall(struct.pack('>BBHI',4,int(누르는중),0,szimbólum_ÉRTÉK))
    def START_Ofszet(Vonal):
        Futtatás=len(átirat)
        for kódpont in Vonal+'\n':
            szimbólum_ÉRTÉK=0xff0d if kódpont=='\n' else ord(kódpont) if ord(kódpont)<256 else 0x1000000|ord(kódpont)
            누름값(szimbólum_ÉRTÉK);누름값(szimbólum_ÉRTÉK,False)
        return Futtatás
    def felület(Vonal):return fogad_e_mail(b'jkoros-native> ',START_Ofszet(Vonal))
    def végrehajt_parancs(Vonal,예상결과):
        Szöveg=felület(Vonal);assert 예상결과 in Szöveg and 'exit 0' in Szöveg,(Vonal,Szöveg)
        return Szöveg
    def 화소들():
        kliens.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            terület_ÉRTÉK=AZONOS_ÉRTÉK(kliens,1)[0]
            if terület_ÉRTÉK==2:continue
            if terület_ÉRTÉK==3:
                cikk_DARAB=struct.unpack('>I',AZONOS_ÉRTÉK(kliens,7)[3:])[0];AZONOS_ÉRTÉK(kliens,cikk_DARAB);continue
            assert terület_ÉRTÉK==0,terület_ÉRTÉK
            bejegyzés_DARAB=struct.unpack('>H',AZONOS_ÉRTÉK(kliens,3)[1:])[0]
            for _ in range(bejegyzés_DARAB):
                x_koordináta,Y_koordináta,너비값,높이값,karakterkészlet=struct.unpack('>HHHHi',AZONOS_ÉRTÉK(kliens,12));assert karakterkészlet==0,karakterkészlet
                adat=AZONOS_ÉRTÉK(kliens,너비값*높이값*4)
                for SOR_pozíció in range(높이값):
                    for OSZLOP_pozíció in range(너비값):
                        원본자료=(SOR_pozíció*너비값+OSZLOP_pozíció)*4;cél=((Y_koordináta+SOR_pozíció)*640+x_koordináta+OSZLOP_pozíció)*3
                        빛삼원색[cél:cél+3]=bytes((adat[원본자료+2],adat[원본자료+1],adat[원본자료]))
            if bejegyzés_DARAB:return 빛삼원색
    try:
        fogad_e_mail(b'TERMINAL READY');fogad_e_mail(b'jkoros-native> ',átirat.rfind(b'TERMINAL READY'))
        portszám=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',átirat).group(1))
        kliens=socket.create_connection(('127.0.0.1',portszám),timeout=10)
        assert AZONOS_ÉRTÉK(kliens,12)==b'RFB 003.008\n';kliens.sendall(b'RFB 003.008\n')
        assert 1 in AZONOS_ÉRTÉK(kliens,AZONOS_ÉRTÉK(kliens,1)[0]);kliens.sendall(b'\x01');assert AZONOS_ÉRTÉK(kliens,4)==b'\0'*4
        kliens.sendall(b'\x01');초기값=AZONOS_ÉRTÉK(kliens,24);AZONOS_ÉRTÉK(kliens,struct.unpack('>I',초기값[20:])[0])
        kliens.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        kliens.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in felület('ftpd start')
        fájlátvitel_ismerős=ftplib.FTP();fájlátvitel_ismerős.encoding='utf-8';fájlátvitel_ismerős.connect('127.0.0.1',fájlátvitel_portszám,timeout=20);fájlátvitel_ismerős.login()
        teher_adat=('GUI와 FTP 동시 használ_ÉRTÉK '+Nyelv+' 😀\n').encode()
        fájlátvitel_ismerős.storbinary('STOR 함께.txt',io.BytesIO(teher_adat))
        assert teher_adat.decode().strip() in felület('cat /함께.txt')
        KAPOTT_DARAB=bytearray();fájlátvitel_ismerős.retrbinary('RETR 함께.txt',KAPOTT_DARAB.extend);assert KAPOTT_DARAB==teher_adat;fájlátvitel_ismerős.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        küld_Lista=felület('ls /example')
        assert all(Név in küld_Lista for Név in ('java/','c/','python/','README.md')),küld_Lista
        if Nyelv=='java':
            köteg_jegyzékfájl=json.loads((teendő_gyök/'build/examples/manifest.json').read_text())
            for ÚTVONAL,belépési_pont in köteg_jegyzékfájl.items():
                felület('cp '+ÚTVONAL+' /example-check.bin')
                Tartalom_ÉRTÉK=bytearray();fájlátvitel_ismerős.retrbinary('RETR example-check.bin',Tartalom_ÉRTÉK.extend)
                assert len(Tartalom_ÉRTÉK)==belépési_pont['bytes'] and hashlib.sha256(Tartalom_ÉRTÉK).hexdigest()==belépési_pont['sha256'],ÚTVONAL
            fájlátvitel_ismerős.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            bináris=bytes(range(256))*64
            fájlátvitel_ismerős.storbinary('STOR boundary.bin',io.BytesIO(bináris))
            Tartalom_ÉRTÉK=bytearray();fájlátvitel_ismerős.retrbinary('RETR boundary.bin',Tartalom_ÉRTÉK.extend)
            assert Tartalom_ÉRTÉK==bináris and 'boundary.bin' in fájlátvitel_ismerős.nlst()
            felület('cp /boundary.bin /boundary-copy.bin')
            Tartalom_ÉRTÉK=bytearray();fájlátvitel_ismerős.retrbinary('RETR boundary-copy.bin',Tartalom_ÉRTÉK.extend)
            assert Tartalom_ÉRTÉK==bináris
            fájlátvitel_ismerős.delete('boundary.bin');fájlátvitel_ismerős.delete('boundary-copy.bin')
        assert 'KimenetiPélda' in felület('ls /example/'+Nyelv)
        felület('cd /example/'+Nyelv)
        név_tábla={'java':'JAVA','c':'C','python':'PYTHON'}[Nyelv]
        예상파일=név_tábla+' Fájl: 한글 adat 😀\n'
        if Nyelv=='java':
            végrehajt_parancs('javac KimenetiPélda.java','Compiled:');végrehajt_parancs('java KimenetiPélda','JAVA Kimenet: 안녕하세요 😀')
            végrehajt_parancs('javac FájlPélda.java','Compiled:');végrehajt_parancs('java FájlPélda',예상파일)
            végrehajt_parancs('java HálózatiPélda {} {}'.format(visszhang_kiszolgáló_bejegyzés.TCP_port,visszhang_kiszolgáló_bejegyzés.UDP_port),'JAVA 네트워크 igazol: TCP UDP 한글')
            grafika_parancs='java RajzPélda'
        elif Nyelv=='c':
            for Név,전달값,예상결과 in [('Kimenet','', 'C Kimenet: 안녕하세요 😀'),('Fájl','',예상파일),
                    ('네트워크',' '+str(visszhang_kiszolgáló_bejegyzés.UDP_port),'C 네트워크 igazol: UDP 한글')]:
                végrehajt_parancs('cc '+Név+'예제.c -o végrehajt_parancs','Compiled native ARM64 ELF:')
                végrehajt_parancs('./végrehajt_parancs'+전달값,예상결과)
            végrehajt_parancs('cc RajzPélda.c -o végrehajt_parancs','Compiled native ARM64 ELF:');grafika_parancs='./végrehajt_parancs'
        else:
            for Név,전달값,예상결과 in [('Kimenet','','PYTHON Kimenet: 안녕하세요 😀'),('Fájl','',예상파일),
                    ('네트워크',' '+str(visszhang_kiszolgáló_bejegyzés.UDP_port),'PYTHON 네트워크 igazol: UDP 한글')]:
                végrehajt_parancs('python '+Név+'예제.py'+전달값,예상결과)
            grafika_parancs='python RajzPélda.py'
        START_rajz=START_Ofszet(grafika_parancs)
        Szöveg=fogad_e_mail('그림을 확인한 BACK_ÉRTÉK Enter를 누르세요.\r\n'.encode(),START_rajz)
        assert név_tábla+' 그래픽: 빨강 초록 파랑' in Szöveg and 'exit 0' not in Szöveg,Szöveg
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        fájlátvitel_ismerős.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        KAPOTT_DARAB=bytearray();fájlátvitel_ismerős.retrbinary('RETR 도중.txt',KAPOTT_DARAB.extend);assert KAPOTT_DARAB==b'FTP DURING GRAPHICS';fájlátvitel_ismerős.delete('도중.txt')
        빛삼원색=화소들()
        for Y_koordináta,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Ofszet_ÉRTÉK=(Y_koordináta*640+610)*3;assert tuple(빛삼원색[Ofszet_ÉRTÉK:Ofszet_ÉRTÉK+3])==색상,(Nyelv,Y_koordináta,tuple(빛삼원색[Ofszet_ÉRTÉK:Ofszet_ÉRTÉK+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_adat/(Nyelv+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in fogad_e_mail(b'jkoros-native> ',START_rajz)
        if Nyelv=='java':
            START_ablak=START_Ofszet('java AblakPélda')
            fogad_e_mail('GUI 예제 Előkészítés: AblakPélda'.encode(),START_ablak)
            def kattint_ÉRTÉK(가로,szektor_pozíció):
                for gomb in (1,0):kliens.sendall(struct.pack('>BBHH',5,gomb,가로,szektor_pozíció))
            time.sleep(.3)
            Előző_KÉP=Image.frombytes('RGB',(640,480),bytes(화소들()))
            kattint_ÉRTÉK(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for karakter_ÉRTÉK in '한글':누름값(0x1000000|ord(karakter_ÉRTÉK));누름값(0x1000000|ord(karakter_ÉRTÉK),False)
            for 횟수 in (1,2):
                Futtatás=len(átirat);kattint_ÉRTÉK(180,242)
                fogad_e_mail(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Futtatás)
            time.sleep(.3)
            ablak_rajz=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert Előző_KÉP.crop((110,272,530,300)).tobytes()!=ablak_rajz.crop((110,272,530,300)).tobytes()
            ablak_rajz.save(str(KR_adat/'java-swing.png'))
            Futtatás=len(átirat);kattint_ÉRTÉK(535,105)
            assert 'exit 0' in fogad_e_mail(b'jkoros-native> ',Futtatás)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Fájl_bejegyzés_név={'java':'java.txt','c':'c.txt','python':'python.txt'}[Nyelv]
        felület('cp '+Fájl_bejegyzés_név+' /ellenőriz.txt')
        KAPOTT_DARAB=bytearray();fájlátvitel_ismerős.retrbinary('RETR ellenőriz.txt',KAPOTT_DARAB.extend);assert KAPOTT_DARAB==예상파일.encode()
        felület('echo preserved > KimenetiPélda.'+('py' if Nyelv=='python' else Nyelv))
        assert 'EXAMPLES READY' in felület('example '+Nyelv)
        assert '\npreserved\n' in felület('cat KimenetiPélda.'+('py' if Nyelv=='python' else Nyelv))
        assert '한/nulla_operandus Kulcs_ÉRTÉK, Shift+Space 또는 F9' in felület('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in felület('echo GUI NETWORK TOGETHER')
        fájlátvitel_ismerős.quit();fájlátvitel_ismerős=None;assert 'FTP stopped' in felület('ftpd stop')
        print('PASS '+Nyelv+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if fájlátvitel_ismerős:
            try:fájlátvitel_ismerős.close()
            except OSError:pass
        if kliens:kliens.close()
        Folyamat.terminate()
        try:Folyamat.wait(timeout=8)
        except subprocess.TimeoutExpired:Folyamat.kill();Folyamat.wait()
        szelektor.close();Folyamat.stdout.close();(KR_adat/(Nyelv+'-serial.log')).write_bytes(átirat)


def Futtatás():
    KR_adat=teendő_gyök/'build/verification/examples';KR_adat.mkdir(parents=True,exist_ok=True)
    ellenőrzés_jelent={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((teendő_gyök/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with visszhang_Kiszolgálók() as visszhang_kiszolgáló_bejegyzés:
            for Nyelv in ('java','c','python'):
                teszt_Nyelv(Nyelv,visszhang_kiszolgáló_bejegyzés,KR_adat);ellenőrzés_jelent['languages'].append(Nyelv)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert visszhang_kiszolgáló_bejegyzés.수신됨==[(terület_ÉRTÉK,adat.encode()) for terület_ÉRTÉK,adat in 예상결과],visszhang_kiszolgáló_bejegyzés.수신됨
            ellenőrzés_jelent['host_network_payloads']=[{'protocol':terület_ÉRTÉK,'text':adat.decode()} for terület_ÉRTÉK,adat in visszhang_kiszolgáló_bejegyzés.수신됨]
        ellenőrzés_jelent.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_adat/'report.json').write_text(json.dumps(ellenőrzés_jelent,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Futtatás()
