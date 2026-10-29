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
from escriptori_visualitzar import IGUAL_VALOR
from 예제되돌림서버 import eco_Servidors
from Executa_ordre import Project_rel


def test_언어(Idioma,eco_servidor_introducció,mesura_dades):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));transferència_de_fitxers_número_de_port=임시자원.getsockname()[1]
    Procés=subprocess.Popen(['python3',str(Project_rel/'Eines/Executa_ordre.py'),'--desktop','--network','--port','0','--ftp-port',str(transferència_de_fitxers_número_de_port)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비선택기=selectors.DefaultSelector();준비선택기.register(Procés.stdout,selectors.EVENT_READ)
    대화기록=bytearray();client=None;transferència_de_fitxers_connexió=None
    def rebre_correu(확인표시,Executa_2=0):
        finalitzar_DESPLAÇAMENT=time.monotonic()+60
        while 확인표시 not in 대화기록[Executa_2:]:
            if time.monotonic()>finalitzar_DESPLAÇAMENT or Procés.poll() is not None:raise AssertionError(대화기록[Executa_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비선택기.select(.1):
                dades=누름값.fileobj.read(65536)
                if dades:대화기록.extend(dades)
        return 대화기록[Executa_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(símbol_VALOR,누르는중=True):client.sendall(struct.pack('>BBHI',4,int(누르는중),0,símbol_VALOR))
    def Inici_DESPLAÇAMENT(línia):
        Executa_2=len(대화기록)
        for codi_de_caràcter in línia+'\n':
            símbol_VALOR=0xff0d if codi_de_caràcter=='\n' else ord(codi_de_caràcter) if ord(codi_de_caràcter)<256 else 0x1000000|ord(codi_de_caràcter)
            누름값(símbol_VALOR);누름값(símbol_VALOR,False)
        return Executa_2
    def shell(línia):return rebre_correu(b'jkoros-native> ',Inici_DESPLAÇAMENT(línia))
    def Executa_ordre(línia,예상결과):
        SMS=shell(línia);assert 예상결과 in SMS and 'exit 0' in SMS,(línia,SMS)
        return SMS
    def 화소들():
        client.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            Categoria_VALOR=IGUAL_VALOR(client,1)[0]
            if Categoria_VALOR==2:continue
            if Categoria_VALOR==3:
                element_COMPT=struct.unpack('>I',IGUAL_VALOR(client,7)[3:])[0];IGUAL_VALOR(client,element_COMPT);continue
            assert Categoria_VALOR==0,Categoria_VALOR
            introducció_COMPT=struct.unpack('>H',IGUAL_VALOR(client,3)[1:])[0]
            for _ in range(introducció_COMPT):
                X_coordenada,Y_coordenada,너비값,높이값,joc_de_caràcters=struct.unpack('>HHHHi',IGUAL_VALOR(client,12));assert joc_de_caràcters==0,joc_de_caràcters
                dades=IGUAL_VALOR(client,너비값*높이값*4)
                for FILA_càrrec in range(높이값):
                    for COLUMNA_càrrec in range(너비값):
                        원본자료=(FILA_càrrec*너비값+COLUMNA_càrrec)*4;objectiu=((Y_coordenada+FILA_càrrec)*640+X_coordenada+COLUMNA_càrrec)*3
                        빛삼원색[objectiu:objectiu+3]=bytes((dades[원본자료+2],dades[원본자료+1],dades[원본자료]))
            if introducció_COMPT:return 빛삼원색
    try:
        rebre_correu(b'TERMINAL READY');rebre_correu(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        número_de_port=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        client=socket.create_connection(('127.0.0.1',número_de_port),timeout=10)
        assert IGUAL_VALOR(client,12)==b'RFB 003.008\n';client.sendall(b'RFB 003.008\n')
        assert 1 in IGUAL_VALOR(client,IGUAL_VALOR(client,1)[0]);client.sendall(b'\x01');assert IGUAL_VALOR(client,4)==b'\0'*4
        client.sendall(b'\x01');초기값=IGUAL_VALOR(client,24);IGUAL_VALOR(client,struct.unpack('>I',초기값[20:])[0])
        client.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        client.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in shell('ftpd start')
        transferència_de_fitxers_connexió=ftplib.FTP();transferència_de_fitxers_connexió.encoding='utf-8';transferència_de_fitxers_connexió.connect('127.0.0.1',transferència_de_fitxers_número_de_port,timeout=20);transferència_de_fitxers_connexió.login()
        càrrega_dades=('GUI와 FTP 동시 ús_VALOR '+Idioma+' 😀\n').encode()
        transferència_de_fitxers_connexió.storbinary('STOR 함께.txt',io.BytesIO(càrrega_dades))
        assert càrrega_dades.decode().strip() in shell('cat /함께.txt')
        CANTIDAD_RECIBIDA_COMPT=bytearray();transferència_de_fitxers_connexió.retrbinary('RETR 함께.txt',CANTIDAD_RECIBIDA_COMPT.extend);assert CANTIDAD_RECIBIDA_COMPT==càrrega_dades;transferència_de_fitxers_connexió.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        enviar_Llista=shell('ls /example')
        assert all(Nom in enviar_Llista for Nom in ('java/','c/','python/','README.md')),enviar_Llista
        if Idioma=='java':
            꾸러미명세=json.loads((Project_rel/'build/examples/manifest.json').read_text())
            for Camí,introducció_p in 꾸러미명세.items():
                shell('cp '+Camí+' /example-check.bin')
                contingut_VALOR=bytearray();transferència_de_fitxers_connexió.retrbinary('RETR example-check.bin',contingut_VALOR.extend)
                assert len(contingut_VALOR)==introducció_p['bytes'] and hashlib.sha256(contingut_VALOR).hexdigest()==introducció_p['sha256'],Camí
            transferència_de_fitxers_connexió.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binari=bytes(range(256))*64
            transferència_de_fitxers_connexió.storbinary('STOR boundary.bin',io.BytesIO(binari))
            contingut_VALOR=bytearray();transferència_de_fitxers_connexió.retrbinary('RETR boundary.bin',contingut_VALOR.extend)
            assert contingut_VALOR==binari and 'boundary.bin' in transferència_de_fitxers_connexió.nlst()
            shell('cp /boundary.bin /boundary-copy.bin')
            contingut_VALOR=bytearray();transferència_de_fitxers_connexió.retrbinary('RETR boundary-copy.bin',contingut_VALOR.extend)
            assert contingut_VALOR==binari
            transferència_de_fitxers_connexió.delete('boundary.bin');transferència_de_fitxers_connexió.delete('boundary-copy.bin')
        assert 'ExempleSortida' in shell('ls /example/'+Idioma)
        shell('cd /example/'+Idioma)
        nom_taula={'java':'JAVA','c':'C','python':'PYTHON'}[Idioma]
        예상파일=nom_taula+' Fitxer: 한글 dades 😀\n'
        if Idioma=='java':
            Executa_ordre('javac ExempleSortida.java','Compiled:');Executa_ordre('java ExempleSortida','JAVA Sortida: 안녕하세요 😀')
            Executa_ordre('javac ExempleFitxer.java','Compiled:');Executa_ordre('java ExempleFitxer',예상파일)
            Executa_ordre('java ExempleXarxa {} {}'.format(eco_servidor_introducció.TCP_port,eco_servidor_introducció.UDP_port),'JAVA 네트워크 verificar: TCP UDP 한글')
            gràfics_ordre='java ExempleDibuix'
        elif Idioma=='c':
            for Nom,전달값,예상결과 in [('Sortida','', 'C Sortida: 안녕하세요 😀'),('Fitxer','',예상파일),
                    ('네트워크',' '+str(eco_servidor_introducció.UDP_port),'C 네트워크 verificar: UDP 한글')]:
                Executa_ordre('cc '+Nom+'예제.c -o Executa_ordre','Compiled native ARM64 ELF:')
                Executa_ordre('./Executa_ordre'+전달값,예상결과)
            Executa_ordre('cc ExempleDibuix.c -o Executa_ordre','Compiled native ARM64 ELF:');gràfics_ordre='./Executa_ordre'
        else:
            for Nom,전달값,예상결과 in [('Sortida','','PYTHON Sortida: 안녕하세요 😀'),('Fitxer','',예상파일),
                    ('네트워크',' '+str(eco_servidor_introducció.UDP_port),'PYTHON 네트워크 verificar: UDP 한글')]:
                Executa_ordre('python '+Nom+'예제.py'+전달값,예상결과)
            gràfics_ordre='python ExempleDibuix.py'
        Inici_dibuix=Inici_DESPLAÇAMENT(gràfics_ordre)
        SMS=rebre_correu('그림을 확인한 ENRERE_VALOR Enter를 누르세요.\r\n'.encode(),Inici_dibuix)
        assert nom_taula+' 그래픽: 빨강 초록 파랑' in SMS and 'exit 0' not in SMS,SMS
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        transferència_de_fitxers_connexió.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        CANTIDAD_RECIBIDA_COMPT=bytearray();transferència_de_fitxers_connexió.retrbinary('RETR 도중.txt',CANTIDAD_RECIBIDA_COMPT.extend);assert CANTIDAD_RECIBIDA_COMPT==b'FTP DURING GRAPHICS';transferència_de_fitxers_connexió.delete('도중.txt')
        빛삼원색=화소들()
        for Y_coordenada,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            DESPLAÇAMENT_VALOR=(Y_coordenada*640+610)*3;assert tuple(빛삼원색[DESPLAÇAMENT_VALOR:DESPLAÇAMENT_VALOR+3])==색상,(Idioma,Y_coordenada,tuple(빛삼원색[DESPLAÇAMENT_VALOR:DESPLAÇAMENT_VALOR+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(mesura_dades/(Idioma+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in rebre_correu(b'jkoros-native> ',Inici_dibuix)
        if Idioma=='java':
            Inici_finestra=Inici_DESPLAÇAMENT('java ExempleFinestra')
            rebre_correu('GUI 예제 Prepara: ExempleFinestra'.encode(),Inici_finestra)
            def clic_VALOR(가로,Vertical_càrrec):
                for Botó in (1,0):client.sendall(struct.pack('>BBHH',5,Botó,가로,Vertical_càrrec))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            clic_VALOR(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for caràcter_VALOR in '한글':누름값(0x1000000|ord(caràcter_VALOR));누름값(0x1000000|ord(caràcter_VALOR),False)
            for 횟수 in (1,2):
                Executa_2=len(대화기록);clic_VALOR(180,242)
                rebre_correu(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Executa_2)
            time.sleep(.3)
            finestra_dibuix=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=finestra_dibuix.crop((110,272,530,300)).tobytes()
            finestra_dibuix.save(str(mesura_dades/'java-swing.png'))
            Executa_2=len(대화기록);clic_VALOR(535,105)
            assert 'exit 0' in rebre_correu(b'jkoros-native> ',Executa_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        arxiu_introducció_nom={'java':'java.txt','c':'c.txt','python':'python.txt'}[Idioma]
        shell('cp '+arxiu_introducció_nom+' /validar.txt')
        CANTIDAD_RECIBIDA_COMPT=bytearray();transferència_de_fitxers_connexió.retrbinary('RETR validar.txt',CANTIDAD_RECIBIDA_COMPT.extend);assert CANTIDAD_RECIBIDA_COMPT==예상파일.encode()
        shell('echo preserved > ExempleSortida.'+('py' if Idioma=='python' else Idioma))
        assert 'EXAMPLES READY' in shell('example '+Idioma)
        assert '\npreserved\n' in shell('cat ExempleSortida.'+('py' if Idioma=='python' else Idioma))
        assert '한/영 Clau_VALOR, Shift+Space 또는 F9' in shell('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in shell('echo GUI NETWORK TOGETHER')
        transferència_de_fitxers_connexió.quit();transferència_de_fitxers_connexió=None;assert 'FTP stopped' in shell('ftpd stop')
        print('PASS '+Idioma+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if transferència_de_fitxers_connexió:
            try:transferència_de_fitxers_connexió.close()
            except OSError:pass
        if client:client.close()
        Procés.terminate()
        try:Procés.wait(timeout=8)
        except subprocess.TimeoutExpired:Procés.kill();Procés.wait()
        준비선택기.close();Procés.stdout.close();(mesura_dades/(Idioma+'-serial.log')).write_bytes(대화기록)


def Executa_2():
    mesura_dades=Project_rel/'build/verification/examples';mesura_dades.mkdir(parents=True,exist_ok=True)
    validació_informe={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rel/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with eco_Servidors() as eco_servidor_introducció:
            for Idioma in ('java','c','python'):
                test_언어(Idioma,eco_servidor_introducció,mesura_dades);validació_informe['languages'].append(Idioma)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert eco_servidor_introducció.수신됨==[(Categoria_VALOR,dades.encode()) for Categoria_VALOR,dades in 예상결과],eco_servidor_introducció.수신됨
            validació_informe['host_network_payloads']=[{'protocol':Categoria_VALOR,'text':dades.decode()} for Categoria_VALOR,dades in eco_servidor_introducció.수신됨]
        validació_informe.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(mesura_dades/'report.json').write_text(json.dumps(validació_informe,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Executa_2()
