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
from PC_Vista import IDENTICO_VALORE
from 예제되돌림서버 import eco_schermo_Server
from Esegui_comando import azione_radice


def test_Lingua(Lingua,eco_schermo_server_voce,KR_dati):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));trasferimento_di_file_numero_di_porta=임시자원.getsockname()[1]
    Processi=subprocess.Popen(['python3',str(azione_radice/'strumenti/Esegui_comando.py'),'--desktop','--network','--port','0','--ftp-port',str(trasferimento_di_file_numero_di_porta)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    selettore=selectors.DefaultSelector();selettore.register(Processi.stdout,selectors.EVENT_READ)
    trascrizione=bytearray();client=None;trasferimento_di_file_connessione=None
    def ricevere_documento(marcatore,avvia=0):
        chiudere_SCARTO=time.monotonic()+60
        while marcatore not in trascrizione[avvia:]:
            if time.monotonic()>chiudere_SCARTO or Processi.poll() is not None:raise AssertionError(trascrizione[avvia:].decode('utf-8','replace'))
            for 누름값,_ in selettore.select(.1):
                dati=누름값.fileobj.read(65536)
                if dati:trascrizione.extend(dati)
        return trascrizione[avvia:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simbolo_VALORE,누르는중=True):client.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbolo_VALORE))
    def START_SCARTO(riga_di_ingresso):
        avvia=len(trascrizione)
        for punto_di_codice in riga_di_ingresso+'\n':
            simbolo_VALORE=0xff0d if punto_di_codice=='\n' else ord(punto_di_codice) if ord(punto_di_codice)<256 else 0x1000000|ord(punto_di_codice)
            누름값(simbolo_VALORE);누름값(simbolo_VALORE,False)
        return avvia
    def Shell(riga_di_ingresso):return ricevere_documento(b'jkoros-native> ',START_SCARTO(riga_di_ingresso))
    def Esegui_comando(riga_di_ingresso,예상결과):
        testo=Shell(riga_di_ingresso);assert 예상결과 in testo and 'exit 0' in testo,(riga_di_ingresso,testo)
        return testo
    def 화소들():
        client.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            Valore_categoria=IDENTICO_VALORE(client,1)[0]
            if Valore_categoria==2:continue
            if Valore_categoria==3:
                articolo_CONTA_NUMERI=struct.unpack('>I',IDENTICO_VALORE(client,7)[3:])[0];IDENTICO_VALORE(client,articolo_CONTA_NUMERI);continue
            assert Valore_categoria==0,Valore_categoria
            voce_CONTA_NUMERI=struct.unpack('>H',IDENTICO_VALORE(client,3)[1:])[0]
            for _ in range(voce_CONTA_NUMERI):
                coordinata_x,Y_coordinata,너비값,richiesto_altezza_VALORE,set_di_caratteri=struct.unpack('>HHHHi',IDENTICO_VALORE(client,12));assert set_di_caratteri==0,set_di_caratteri
                dati=IDENTICO_VALORE(client,너비값*richiesto_altezza_VALORE*4)
                for riga_funzione in range(richiesto_altezza_VALORE):
                    for colonna_funzione in range(너비값):
                        원본자료=(riga_funzione*너비값+colonna_funzione)*4;target=((Y_coordinata+riga_funzione)*640+coordinata_x+colonna_funzione)*3
                        빛삼원색[target:target+3]=bytes((dati[원본자료+2],dati[원본자료+1],dati[원본자료]))
            if voce_CONTA_NUMERI:return 빛삼원색
    try:
        ricevere_documento(b'TERMINAL READY');ricevere_documento(b'jkoros-native> ',trascrizione.rfind(b'TERMINAL READY'))
        numero_di_porta=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',trascrizione).group(1))
        client=socket.create_connection(('127.0.0.1',numero_di_porta),timeout=10)
        assert IDENTICO_VALORE(client,12)==b'RFB 003.008\n';client.sendall(b'RFB 003.008\n')
        assert 1 in IDENTICO_VALORE(client,IDENTICO_VALORE(client,1)[0]);client.sendall(b'\x01');assert IDENTICO_VALORE(client,4)==b'\0'*4
        client.sendall(b'\x01');초기값=IDENTICO_VALORE(client,24);IDENTICO_VALORE(client,struct.unpack('>I',초기값[20:])[0])
        client.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        client.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in Shell('ftpd start')
        trasferimento_di_file_connessione=ftplib.FTP();trasferimento_di_file_connessione.encoding='utf-8';trasferimento_di_file_connessione.connect('127.0.0.1',trasferimento_di_file_numero_di_porta,timeout=20);trasferimento_di_file_connessione.login()
        payload_dati=('GUI와 FTP 동시 usare_VALORE '+Lingua+' 😀\n').encode()
        trasferimento_di_file_connessione.storbinary('STOR 함께.txt',io.BytesIO(payload_dati))
        assert payload_dati.decode().strip() in Shell('cat /함께.txt')
        RICEV_SCAD_CONTA_NUMERI=bytearray();trasferimento_di_file_connessione.retrbinary('RETR 함께.txt',RICEV_SCAD_CONTA_NUMERI.extend);assert RICEV_SCAD_CONTA_NUMERI==payload_dati;trasferimento_di_file_connessione.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        inviare_elenco=Shell('ls /example')
        assert all(Nome in inviare_elenco for Nome in ('java/','c/','python/','README.md')),inviare_elenco
        if Lingua=='java':
            aggregare_manifesto=json.loads((azione_radice/'build/examples/manifest.json').read_text())
            for percorso,punto_di_ingresso in aggregare_manifesto.items():
                Shell('cp '+percorso+' /example-check.bin')
                Contenuto_VALORE=bytearray();trasferimento_di_file_connessione.retrbinary('RETR example-check.bin',Contenuto_VALORE.extend)
                assert len(Contenuto_VALORE)==punto_di_ingresso['bytes'] and hashlib.sha256(Contenuto_VALORE).hexdigest()==punto_di_ingresso['sha256'],percorso
            trasferimento_di_file_connessione.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            base_2=bytes(range(256))*64
            trasferimento_di_file_connessione.storbinary('STOR boundary.bin',io.BytesIO(base_2))
            Contenuto_VALORE=bytearray();trasferimento_di_file_connessione.retrbinary('RETR boundary.bin',Contenuto_VALORE.extend)
            assert Contenuto_VALORE==base_2 and 'boundary.bin' in trasferimento_di_file_connessione.nlst()
            Shell('cp /boundary.bin /boundary-copy.bin')
            Contenuto_VALORE=bytearray();trasferimento_di_file_connessione.retrbinary('RETR boundary-copy.bin',Contenuto_VALORE.extend)
            assert Contenuto_VALORE==base_2
            trasferimento_di_file_connessione.delete('boundary.bin');trasferimento_di_file_connessione.delete('boundary-copy.bin')
        assert 'EsempioUscita' in Shell('ls /example/'+Lingua)
        Shell('cd /example/'+Lingua)
        nome_tabella={'java':'JAVA','c':'C','python':'PYTHON'}[Lingua]
        예상파일=nome_tabella+' file: 한글 dati 😀\n'
        if Lingua=='java':
            Esegui_comando('javac EsempioUscita.java','Compiled:');Esegui_comando('java EsempioUscita','JAVA uscitaTesto: 안녕하세요 😀')
            Esegui_comando('javac EsempioFile.java','Compiled:');Esegui_comando('java EsempioFile',예상파일)
            Esegui_comando('java EsempioRete {} {}'.format(eco_schermo_server_voce.porta_TCP,eco_schermo_server_voce.UDP_porta),'JAVA 네트워크 verificare: TCP UDP 한글')
            grafica_comando='java EsempioDisegno'
        elif Lingua=='c':
            for Nome,전달값,예상결과 in [('uscitaTesto','', 'C uscitaTesto: 안녕하세요 😀'),('file','',예상파일),
                    ('네트워크',' '+str(eco_schermo_server_voce.UDP_porta),'C 네트워크 verificare: UDP 한글')]:
                Esegui_comando('cc '+Nome+'예제.c -o Esegui_comando','Compiled native ARM64 ELF:')
                Esegui_comando('./Esegui_comando'+전달값,예상결과)
            Esegui_comando('cc EsempioDisegno.c -o Esegui_comando','Compiled native ARM64 ELF:');grafica_comando='./Esegui_comando'
        else:
            for Nome,전달값,예상결과 in [('uscitaTesto','','PYTHON uscitaTesto: 안녕하세요 😀'),('file','',예상파일),
                    ('네트워크',' '+str(eco_schermo_server_voce.UDP_porta),'PYTHON 네트워크 verificare: UDP 한글')]:
                Esegui_comando('python '+Nome+'예제.py'+전달값,예상결과)
            grafica_comando='python EsempioDisegno.py'
        START_disegno=START_SCARTO(grafica_comando)
        testo=ricevere_documento('그림을 확인한 BACK_VALORE Enter를 누르세요.\r\n'.encode(),START_disegno)
        assert nome_tabella+' 그래픽: 빨강 초록 파랑' in testo and 'exit 0' not in testo,testo
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        trasferimento_di_file_connessione.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RICEV_SCAD_CONTA_NUMERI=bytearray();trasferimento_di_file_connessione.retrbinary('RETR 도중.txt',RICEV_SCAD_CONTA_NUMERI.extend);assert RICEV_SCAD_CONTA_NUMERI==b'FTP DURING GRAPHICS';trasferimento_di_file_connessione.delete('도중.txt')
        빛삼원색=화소들()
        for Y_coordinata,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            SCARTO_VALORE=(Y_coordinata*640+610)*3;assert tuple(빛삼원색[SCARTO_VALORE:SCARTO_VALORE+3])==색상,(Lingua,Y_coordinata,tuple(빛삼원색[SCARTO_VALORE:SCARTO_VALORE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_dati/(Lingua+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in ricevere_documento(b'jkoros-native> ',START_disegno)
        if Lingua=='java':
            START_finestra=START_SCARTO('java EsempioFinestra')
            ricevere_documento('GUI 예제 Prepara: EsempioFinestra'.encode(),START_finestra)
            def clic_VALORE(가로,Verticale_funzione):
                for pulsante in (1,0):client.sendall(struct.pack('>BBHH',5,pulsante,가로,Verticale_funzione))
            time.sleep(.3)
            Indietro_foto=Image.frombytes('RGB',(640,480),bytes(화소들()))
            clic_VALORE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for carattere_VALORE in '한글':누름값(0x1000000|ord(carattere_VALORE));누름값(0x1000000|ord(carattere_VALORE),False)
            for ripetizione_CONTA_NUMERI in (1,2):
                avvia=len(trascrizione);clic_VALORE(180,242)
                ricevere_documento(('GUI messaggio_di_saluto_ae353e94: 안녕하세요, 한글님! ('+str(ripetizione_CONTA_NUMERI)+')').encode(),avvia)
            time.sleep(.3)
            finestra_disegno=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert Indietro_foto.crop((110,272,530,300)).tobytes()!=finestra_disegno.crop((110,272,530,300)).tobytes()
            finestra_disegno.save(str(KR_dati/'java-swing.png'))
            avvia=len(trascrizione);clic_VALORE(535,105)
            assert 'exit 0' in ricevere_documento(b'jkoros-native> ',avvia)
        # Download the guest-created bytes through FTP in the same GUI VM.
        File_voce_nome={'java':'java.txt','c':'c.txt','python':'python.txt'}[Lingua]
        Shell('cp '+File_voce_nome+' /convalidare.txt')
        RICEV_SCAD_CONTA_NUMERI=bytearray();trasferimento_di_file_connessione.retrbinary('RETR convalidare.txt',RICEV_SCAD_CONTA_NUMERI.extend);assert RICEV_SCAD_CONTA_NUMERI==예상파일.encode()
        Shell('echo preserved > EsempioUscita.'+('py' if Lingua=='python' else Lingua))
        assert 'EXAMPLES READY' in Shell('example '+Lingua)
        assert '\npreserved\n' in Shell('cat EsempioUscita.'+('py' if Lingua=='python' else Lingua))
        assert '한/zero_operando tasto_VALORE, Shift+Space 또는 F9' in Shell('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in Shell('echo GUI NETWORK TOGETHER')
        trasferimento_di_file_connessione.quit();trasferimento_di_file_connessione=None;assert 'FTP stopped' in Shell('ftpd stop')
        print('PASS '+Lingua+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if trasferimento_di_file_connessione:
            try:trasferimento_di_file_connessione.close()
            except OSError:pass
        if client:client.close()
        Processi.terminate()
        try:Processi.wait(timeout=8)
        except subprocess.TimeoutExpired:Processi.kill();Processi.wait()
        selettore.close();Processi.stdout.close();(KR_dati/(Lingua+'-serial.log')).write_bytes(trascrizione)


def avvia():
    KR_dati=azione_radice/'build/verification/examples';KR_dati.mkdir(parents=True,exist_ok=True)
    convalida_Report={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((azione_radice/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with eco_schermo_Server() as eco_schermo_server_voce:
            for Lingua in ('java','c','python'):
                test_Lingua(Lingua,eco_schermo_server_voce,KR_dati);convalida_Report['languages'].append(Lingua)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert eco_schermo_server_voce.수신됨==[(Valore_categoria,dati.encode()) for Valore_categoria,dati in 예상결과],eco_schermo_server_voce.수신됨
            convalida_Report['host_network_payloads']=[{'protocol':Valore_categoria,'text':dati.decode()} for Valore_categoria,dati in eco_schermo_server_voce.수신됨]
        convalida_Report.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_dati/'report.json').write_text(json.dumps(convalida_Report,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':avvia()
