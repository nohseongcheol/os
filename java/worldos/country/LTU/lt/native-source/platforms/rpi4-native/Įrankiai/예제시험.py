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
from darbalaukis_rodyti import EXACT_VALUE
from 예제되돌림서버 import aidas_Serveriai
from Vykdyti_komanda import Project_šaknis


def test_언어(Kalba,aidas_serveris_įrašas,KR_duomenys):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));failo_perdavimas_prievado_numeris=임시자원.getsockname()[1]
    Procesas=subprocess.Popen(['python3',str(Project_šaknis/'Įrankiai/Vykdyti_komanda.py'),'--desktop','--network','--port','0','--ftp-port',str(failo_perdavimas_prievado_numeris)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    išrinkiklis=selectors.DefaultSelector();išrinkiklis.register(Procesas.stdout,selectors.EVENT_READ)
    transkribavimas=bytearray();klientas=None;failo_perdavimas_ryšys=None
    def gauti_žinutė(žymeklis,Paleisti=0):
        baigti_pokalbį_OFFSET=time.monotonic()+60
        while žymeklis not in transkribavimas[Paleisti:]:
            if time.monotonic()>baigti_pokalbį_OFFSET or Procesas.poll() is not None:raise AssertionError(transkribavimas[Paleisti:].decode('utf-8','replace'))
            for 누름값,_ in išrinkiklis.select(.1):
                duomenys=누름값.fileobj.read(65536)
                if duomenys:transkribavimas.extend(duomenys)
        return transkribavimas[Paleisti:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simbolis_VALUE,누르는중=True):klientas.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbolis_VALUE))
    def Start_OFFSET(Eilutė):
        Paleisti=len(transkribavimas)
        for simbolio_kodas in Eilutė+'\n':
            simbolis_VALUE=0xff0d if simbolio_kodas=='\n' else ord(simbolio_kodas) if ord(simbolio_kodas)<256 else 0x1000000|ord(simbolio_kodas)
            누름값(simbolis_VALUE);누름값(simbolis_VALUE,False)
        return Paleisti
    def apvalkalas(Eilutė):return gauti_žinutė(b'jkoros-native> ',Start_OFFSET(Eilutė))
    def Vykdyti_komanda(Eilutė,예상결과):
        Tekstas=apvalkalas(Eilutė);assert 예상결과 in Tekstas and 'exit 0' in Tekstas,(Eilutė,Tekstas)
        return Tekstas
    def 화소들():
        klientas.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            sritis_VALUE=EXACT_VALUE(klientas,1)[0]
            if sritis_VALUE==2:continue
            if sritis_VALUE==3:
                prekė_COUNT=struct.unpack('>I',EXACT_VALUE(klientas,7)[3:])[0];EXACT_VALUE(klientas,prekė_COUNT);continue
            assert sritis_VALUE==0,sritis_VALUE
            įrašas_COUNT=struct.unpack('>H',EXACT_VALUE(klientas,3)[1:])[0]
            for _ in range(įrašas_COUNT):
                x_koordinatė,세로좌표,너비값,높이값,simbolių_rinkinys=struct.unpack('>HHHHi',EXACT_VALUE(klientas,12));assert simbolių_rinkinys==0,simbolių_rinkinys
                duomenys=EXACT_VALUE(klientas,너비값*높이값*4)
                for ROW_padėtis in range(높이값):
                    for COLUMN_padėtis in range(너비값):
                        원본자료=(ROW_padėtis*너비값+COLUMN_padėtis)*4;tikslas=((세로좌표+ROW_padėtis)*640+x_koordinatė+COLUMN_padėtis)*3
                        빛삼원색[tikslas:tikslas+3]=bytes((duomenys[원본자료+2],duomenys[원본자료+1],duomenys[원본자료]))
            if įrašas_COUNT:return 빛삼원색
    try:
        gauti_žinutė(b'TERMINAL READY');gauti_žinutė(b'jkoros-native> ',transkribavimas.rfind(b'TERMINAL READY'))
        prievado_numeris=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transkribavimas).group(1))
        klientas=socket.create_connection(('127.0.0.1',prievado_numeris),timeout=10)
        assert EXACT_VALUE(klientas,12)==b'RFB 003.008\n';klientas.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(klientas,EXACT_VALUE(klientas,1)[0]);klientas.sendall(b'\x01');assert EXACT_VALUE(klientas,4)==b'\0'*4
        klientas.sendall(b'\x01');초기값=EXACT_VALUE(klientas,24);EXACT_VALUE(klientas,struct.unpack('>I',초기값[20:])[0])
        klientas.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klientas.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in apvalkalas('ftpd start')
        failo_perdavimas_ryšys=ftplib.FTP();failo_perdavimas_ryšys.encoding='utf-8';failo_perdavimas_ryšys.connect('127.0.0.1',failo_perdavimas_prievado_numeris,timeout=20);failo_perdavimas_ryšys.login()
        mokamoji_krova_duomenys=('GUI와 FTP 동시 naudoti_VALUE '+Kalba+' 😀\n').encode()
        failo_perdavimas_ryšys.storbinary('STOR 함께.txt',io.BytesIO(mokamoji_krova_duomenys))
        assert mokamoji_krova_duomenys.decode().strip() in apvalkalas('cat /함께.txt')
        RECEIVED_COUNT=bytearray();failo_perdavimas_ryšys.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==mokamoji_krova_duomenys;failo_perdavimas_ryšys.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        siųsti_Sąrašas=apvalkalas('ls /example')
        assert all(Pavadinimas_2 in siųsti_Sąrašas for Pavadinimas_2 in ('java/','c/','python/','README.md')),siųsti_Sąrašas
        if Kalba=='java':
            꾸러미명세=json.loads((Project_šaknis/'build/examples/manifest.json').read_text())
            for KELIAS,įrašas_p in 꾸러미명세.items():
                apvalkalas('cp '+KELIAS+' /example-check.bin')
                Turinys_VALUE=bytearray();failo_perdavimas_ryšys.retrbinary('RETR example-check.bin',Turinys_VALUE.extend)
                assert len(Turinys_VALUE)==įrašas_p['bytes'] and hashlib.sha256(Turinys_VALUE).hexdigest()==įrašas_p['sha256'],KELIAS
            failo_perdavimas_ryšys.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            dvejetainis=bytes(range(256))*64
            failo_perdavimas_ryšys.storbinary('STOR boundary.bin',io.BytesIO(dvejetainis))
            Turinys_VALUE=bytearray();failo_perdavimas_ryšys.retrbinary('RETR boundary.bin',Turinys_VALUE.extend)
            assert Turinys_VALUE==dvejetainis and 'boundary.bin' in failo_perdavimas_ryšys.nlst()
            apvalkalas('cp /boundary.bin /boundary-copy.bin')
            Turinys_VALUE=bytearray();failo_perdavimas_ryšys.retrbinary('RETR boundary-copy.bin',Turinys_VALUE.extend)
            assert Turinys_VALUE==dvejetainis
            failo_perdavimas_ryšys.delete('boundary.bin');failo_perdavimas_ryšys.delete('boundary-copy.bin')
        assert 'IšvestiesPavyzdys' in apvalkalas('ls /example/'+Kalba)
        apvalkalas('cd /example/'+Kalba)
        pavadinimas_lentelė={'java':'JAVA','c':'C','python':'PYTHON'}[Kalba]
        예상파일=pavadinimas_lentelė+' Failas: 한글 duomenys 😀\n'
        if Kalba=='java':
            Vykdyti_komanda('javac IšvestiesPavyzdys.java','Compiled:');Vykdyti_komanda('java IšvestiesPavyzdys','JAVA Išvestis: 안녕하세요 😀')
            Vykdyti_komanda('javac FailoPavyzdys.java','Compiled:');Vykdyti_komanda('java FailoPavyzdys',예상파일)
            Vykdyti_komanda('java TinkloPavyzdys {} {}'.format(aidas_serveris_įrašas.TCP_jungtis,aidas_serveris_įrašas.UDP_jungtis),'JAVA 네트워크 patvirtinti: TCP UDP 한글')
            grafiniai_elementai_komanda='java PiešimoPavyzdys'
        elif Kalba=='c':
            for Pavadinimas_2,전달값,예상결과 in [('Išvestis','', 'C Išvestis: 안녕하세요 😀'),('Failas','',예상파일),
                    ('네트워크',' '+str(aidas_serveris_įrašas.UDP_jungtis),'C 네트워크 patvirtinti: UDP 한글')]:
                Vykdyti_komanda('cc '+Pavadinimas_2+'예제.c -o Vykdyti_komanda','Compiled native ARM64 ELF:')
                Vykdyti_komanda('./Vykdyti_komanda'+전달값,예상결과)
            Vykdyti_komanda('cc PiešimoPavyzdys.c -o Vykdyti_komanda','Compiled native ARM64 ELF:');grafiniai_elementai_komanda='./Vykdyti_komanda'
        else:
            for Pavadinimas_2,전달값,예상결과 in [('Išvestis','','PYTHON Išvestis: 안녕하세요 😀'),('Failas','',예상파일),
                    ('네트워크',' '+str(aidas_serveris_įrašas.UDP_jungtis),'PYTHON 네트워크 patvirtinti: UDP 한글')]:
                Vykdyti_komanda('python '+Pavadinimas_2+'예제.py'+전달값,예상결과)
            grafiniai_elementai_komanda='python PiešimoPavyzdys.py'
        Start_piešinys=Start_OFFSET(grafiniai_elementai_komanda)
        Tekstas=gauti_žinutė('그림을 확인한 ATGAL_VALUE Enter를 누르세요.\r\n'.encode(),Start_piešinys)
        assert pavadinimas_lentelė+' 그래픽: 빨강 초록 파랑' in Tekstas and 'exit 0' not in Tekstas,Tekstas
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        failo_perdavimas_ryšys.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();failo_perdavimas_ryšys.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';failo_perdavimas_ryšys.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(세로좌표*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(Kalba,세로좌표,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_duomenys/(Kalba+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in gauti_žinutė(b'jkoros-native> ',Start_piešinys)
        if Kalba=='java':
            Start_langas=Start_OFFSET('java LangoPavyzdys')
            gauti_žinutė('GUI 예제 Parengti: LangoPavyzdys'.encode(),Start_langas)
            def spustelėti_VALUE(가로,segmentas_padėtis):
                for mygtukas in (1,0):klientas.sendall(struct.pack('>BBHH',5,mygtukas,가로,segmentas_padėtis))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            spustelėti_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for simbolis_VALUE_068c2631 in '한글':누름값(0x1000000|ord(simbolis_VALUE_068c2631));누름값(0x1000000|ord(simbolis_VALUE_068c2631),False)
            for 횟수 in (1,2):
                Paleisti=len(transkribavimas);spustelėti_VALUE(180,242)
                gauti_žinutė(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Paleisti)
            time.sleep(.3)
            langas_piešinys=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=langas_piešinys.crop((110,272,530,300)).tobytes()
            langas_piešinys.save(str(KR_duomenys/'java-swing.png'))
            Paleisti=len(transkribavimas);spustelėti_VALUE(535,105)
            assert 'exit 0' in gauti_žinutė(b'jkoros-native> ',Paleisti)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Failas_įrašas_pavadinimas={'java':'java.txt','c':'c.txt','python':'python.txt'}[Kalba]
        apvalkalas('cp '+Failas_įrašas_pavadinimas+' /tikrinti.txt')
        RECEIVED_COUNT=bytearray();failo_perdavimas_ryšys.retrbinary('RETR tikrinti.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        apvalkalas('echo preserved > IšvestiesPavyzdys.'+('py' if Kalba=='python' else Kalba))
        assert 'EXAMPLES READY' in apvalkalas('example '+Kalba)
        assert '\npreserved\n' in apvalkalas('cat IšvestiesPavyzdys.'+('py' if Kalba=='python' else Kalba))
        assert '한/nulis_operandas Raktas_VALUE, Shift+Space 또는 F9' in apvalkalas('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in apvalkalas('echo GUI NETWORK TOGETHER')
        failo_perdavimas_ryšys.quit();failo_perdavimas_ryšys=None;assert 'FTP stopped' in apvalkalas('ftpd stop')
        print('PASS '+Kalba+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if failo_perdavimas_ryšys:
            try:failo_perdavimas_ryšys.close()
            except OSError:pass
        if klientas:klientas.close()
        Procesas.terminate()
        try:Procesas.wait(timeout=8)
        except subprocess.TimeoutExpired:Procesas.kill();Procesas.wait()
        išrinkiklis.close();Procesas.stdout.close();(KR_duomenys/(Kalba+'-serial.log')).write_bytes(transkribavimas)


def Paleisti():
    KR_duomenys=Project_šaknis/'build/verification/examples';KR_duomenys.mkdir(parents=True,exist_ok=True)
    tikrinimas_pranešti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_šaknis/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with aidas_Serveriai() as aidas_serveris_įrašas:
            for Kalba in ('java','c','python'):
                test_언어(Kalba,aidas_serveris_įrašas,KR_duomenys);tikrinimas_pranešti['languages'].append(Kalba)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert aidas_serveris_įrašas.수신됨==[(sritis_VALUE,duomenys.encode()) for sritis_VALUE,duomenys in 예상결과],aidas_serveris_įrašas.수신됨
            tikrinimas_pranešti['host_network_payloads']=[{'protocol':sritis_VALUE,'text':duomenys.decode()} for sritis_VALUE,duomenys in aidas_serveris_įrašas.수신됨]
        tikrinimas_pranešti.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_duomenys/'report.json').write_text(json.dumps(tikrinimas_pranešti,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Paleisti()
