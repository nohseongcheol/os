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
from escritorio_ver import EXACTO_VALOR
from 예제되돌림서버 import eco_Servidores
from executar_comando import Project_raíz


def test_언어(Idioma,eco_servidor_introdución,medida_datos):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));transferencia_de_ficheiros_número_do_porto=임시자원.getsockname()[1]
    Proceso=subprocess.Popen(['python3',str(Project_raíz/'Ferramentas/executar_comando.py'),'--desktop','--network','--port','0','--ftp-port',str(transferencia_de_ficheiros_número_do_porto)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비선택기=selectors.DefaultSelector();준비선택기.register(Proceso.stdout,selectors.EVENT_READ)
    대화기록=bytearray();cliente=None;transferencia_de_ficheiros_conexión=None
    def 수신하기(확인표시,Executar_2=0):
        finalizar_DESPRAZAMENTO=time.monotonic()+60
        while 확인표시 not in 대화기록[Executar_2:]:
            if time.monotonic()>finalizar_DESPRAZAMENTO or Proceso.poll() is not None:raise AssertionError(대화기록[Executar_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비선택기.select(.1):
                datos=누름값.fileobj.read(65536)
                if datos:대화기록.extend(datos)
        return 대화기록[Executar_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(símbolo_VALOR,누르는중=True):cliente.sendall(struct.pack('>BBHI',4,int(누르는중),0,símbolo_VALOR))
    def START_DESPRAZAMENTO(Liña):
        Executar_2=len(대화기록)
        for código_de_carácter in Liña+'\n':
            símbolo_VALOR=0xff0d if código_de_carácter=='\n' else ord(código_de_carácter) if ord(código_de_carácter)<256 else 0x1000000|ord(código_de_carácter)
            누름값(símbolo_VALOR);누름값(símbolo_VALOR,False)
        return Executar_2
    def shell(Liña):return 수신하기(b'jkoros-native> ',START_DESPRAZAMENTO(Liña))
    def executar_comando(Liña,예상결과):
        Texto=shell(Liña);assert 예상결과 in Texto and 'exit 0' in Texto,(Liña,Texto)
        return Texto
    def 화소들():
        cliente.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            Categoría_VALOR=EXACTO_VALOR(cliente,1)[0]
            if Categoría_VALOR==2:continue
            if Categoría_VALOR==3:
                elemento_CONTAR=struct.unpack('>I',EXACTO_VALOR(cliente,7)[3:])[0];EXACTO_VALOR(cliente,elemento_CONTAR);continue
            assert Categoría_VALOR==0,Categoría_VALOR
            introdución_CONTAR=struct.unpack('>H',EXACTO_VALOR(cliente,3)[1:])[0]
            for _ in range(introdución_CONTAR):
                X_coordenada,Y_coordenada,너비값,높이값,conxunto_de_caracteres=struct.unpack('>HHHHi',EXACTO_VALOR(cliente,12));assert conxunto_de_caracteres==0,conxunto_de_caracteres
                datos=EXACTO_VALOR(cliente,너비값*높이값*4)
                for FILA_cargo in range(높이값):
                    for COLUMNA_cargo in range(너비값):
                        원본자료=(FILA_cargo*너비값+COLUMNA_cargo)*4;obxectivo_VALOR=((Y_coordenada+FILA_cargo)*640+X_coordenada+COLUMNA_cargo)*3
                        빛삼원색[obxectivo_VALOR:obxectivo_VALOR+3]=bytes((datos[원본자료+2],datos[원본자료+1],datos[원본자료]))
            if introdución_CONTAR:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        número_do_porto=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        cliente=socket.create_connection(('127.0.0.1',número_do_porto),timeout=10)
        assert EXACTO_VALOR(cliente,12)==b'RFB 003.008\n';cliente.sendall(b'RFB 003.008\n')
        assert 1 in EXACTO_VALOR(cliente,EXACTO_VALOR(cliente,1)[0]);cliente.sendall(b'\x01');assert EXACTO_VALOR(cliente,4)==b'\0'*4
        cliente.sendall(b'\x01');초기값=EXACTO_VALOR(cliente,24);EXACTO_VALOR(cliente,struct.unpack('>I',초기값[20:])[0])
        cliente.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        cliente.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in shell('ftpd start')
        transferencia_de_ficheiros_conexión=ftplib.FTP();transferencia_de_ficheiros_conexión.encoding='utf-8';transferencia_de_ficheiros_conexión.connect('127.0.0.1',transferencia_de_ficheiros_número_do_porto,timeout=20);transferencia_de_ficheiros_conexión.login()
        carga_datos_60367a51=('GUI와 FTP 동시 사용 '+Idioma+' 😀\n').encode()
        transferencia_de_ficheiros_conexión.storbinary('STOR 함께.txt',io.BytesIO(carga_datos_60367a51))
        assert carga_datos_60367a51.decode().strip() in shell('cat /함께.txt')
        RECIBIDO_CONTAR=bytearray();transferencia_de_ficheiros_conexión.retrbinary('RETR 함께.txt',RECIBIDO_CONTAR.extend);assert RECIBIDO_CONTAR==carga_datos_60367a51;transferencia_de_ficheiros_conexión.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        enviar_Lista=shell('ls /example')
        assert all(Nome in enviar_Lista for Nome in ('java/','c/','python/','README.md')),enviar_Lista
        if Idioma=='java':
            꾸러미명세=json.loads((Project_raíz/'build/examples/manifest.json').read_text())
            for CAMIÑO,introdución_p in 꾸러미명세.items():
                shell('cp '+CAMIÑO+' /example-check.bin')
                Contido_VALOR=bytearray();transferencia_de_ficheiros_conexión.retrbinary('RETR example-check.bin',Contido_VALOR.extend)
                assert len(Contido_VALOR)==introdución_p['bytes'] and hashlib.sha256(Contido_VALOR).hexdigest()==introdución_p['sha256'],CAMIÑO
            transferencia_de_ficheiros_conexión.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binario=bytes(range(256))*64
            transferencia_de_ficheiros_conexión.storbinary('STOR boundary.bin',io.BytesIO(binario))
            Contido_VALOR=bytearray();transferencia_de_ficheiros_conexión.retrbinary('RETR boundary.bin',Contido_VALOR.extend)
            assert Contido_VALOR==binario and 'boundary.bin' in transferencia_de_ficheiros_conexión.nlst()
            shell('cp /boundary.bin /boundary-copy.bin')
            Contido_VALOR=bytearray();transferencia_de_ficheiros_conexión.retrbinary('RETR boundary-copy.bin',Contido_VALOR.extend)
            assert Contido_VALOR==binario
            transferencia_de_ficheiros_conexión.delete('boundary.bin');transferencia_de_ficheiros_conexión.delete('boundary-copy.bin')
        assert '출력예제' in shell('ls /example/'+Idioma)
        shell('cd /example/'+Idioma)
        nome_táboa={'java':'JAVA','c':'C','python':'PYTHON'}[Idioma]
        예상파일=nome_táboa+' Ficheiro: 한글 datos 😀\n'
        if Idioma=='java':
            executar_comando('javac 출력예제.java','Compiled:');executar_comando('java 출력예제','JAVA Saída: 안녕하세요 😀')
            executar_comando('javac 파일예제.java','Compiled:');executar_comando('java 파일예제',예상파일)
            executar_comando('java 네트워크예제 {} {}'.format(eco_servidor_introdución.TCP_porto,eco_servidor_introdución.UDP_porto),'JAVA 네트워크 verificar: TCP UDP 한글')
            gráficos_comando='java 그래픽예제'
        elif Idioma=='c':
            for Nome,전달값,예상결과 in [('Saída','', 'C Saída: 안녕하세요 😀'),('Ficheiro','',예상파일),
                    ('네트워크',' '+str(eco_servidor_introdución.UDP_porto),'C 네트워크 verificar: UDP 한글')]:
                executar_comando('cc '+Nome+'예제.c -o executar_comando','Compiled native ARM64 ELF:')
                executar_comando('./executar_comando'+전달값,예상결과)
            executar_comando('cc 그래픽예제.c -o executar_comando','Compiled native ARM64 ELF:');gráficos_comando='./executar_comando'
        else:
            for Nome,전달값,예상결과 in [('Saída','','PYTHON Saída: 안녕하세요 😀'),('Ficheiro','',예상파일),
                    ('네트워크',' '+str(eco_servidor_introdución.UDP_porto),'PYTHON 네트워크 verificar: UDP 한글')]:
                executar_comando('python '+Nome+'예제.py'+전달값,예상결과)
            gráficos_comando='python 그래픽예제.py'
        그림시작=START_DESPRAZAMENTO(gráficos_comando)
        Texto=수신하기('그림을 확인한 ATRÁS_VALOR Enter를 누르세요.\r\n'.encode(),그림시작)
        assert nome_táboa+' 그래픽: 빨강 초록 파랑' in Texto and 'exit 0' not in Texto,Texto
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        transferencia_de_ficheiros_conexión.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECIBIDO_CONTAR=bytearray();transferencia_de_ficheiros_conexión.retrbinary('RETR 도중.txt',RECIBIDO_CONTAR.extend);assert RECIBIDO_CONTAR==b'FTP DURING GRAPHICS';transferencia_de_ficheiros_conexión.delete('도중.txt')
        빛삼원색=화소들()
        for Y_coordenada,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            DESPRAZAMENTO_VALOR=(Y_coordenada*640+610)*3;assert tuple(빛삼원색[DESPRAZAMENTO_VALOR:DESPRAZAMENTO_VALOR+3])==색상,(Idioma,Y_coordenada,tuple(빛삼원색[DESPRAZAMENTO_VALOR:DESPRAZAMENTO_VALOR+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(medida_datos/(Idioma+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',그림시작)
        if Idioma=='java':
            START_ventá=START_DESPRAZAMENTO('java 창예제')
            수신하기('GUI 예제 준비: 창예제'.encode(),START_ventá)
            def clic_VALOR(가로,Vertical_cargo):
                for botón in (1,0):cliente.sendall(struct.pack('>BBHH',5,botón,가로,Vertical_cargo))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            clic_VALOR(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for carácter_VALOR in '한글':누름값(0x1000000|ord(carácter_VALOR));누름값(0x1000000|ord(carácter_VALOR),False)
            for 횟수 in (1,2):
                Executar_2=len(대화기록);clic_VALOR(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Executar_2)
            time.sleep(.3)
            창그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=창그림.crop((110,272,530,300)).tobytes()
            창그림.save(str(medida_datos/'java-swing.png'))
            Executar_2=len(대화기록);clic_VALOR(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Executar_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Ficheiro_introdución_nome={'java':'java.txt','c':'c.txt','python':'python.txt'}[Idioma]
        shell('cp '+Ficheiro_introdución_nome+' /validar.txt')
        RECIBIDO_CONTAR=bytearray();transferencia_de_ficheiros_conexión.retrbinary('RETR validar.txt',RECIBIDO_CONTAR.extend);assert RECIBIDO_CONTAR==예상파일.encode()
        shell('echo preserved > 출력예제.'+('py' if Idioma=='python' else Idioma))
        assert 'EXAMPLES READY' in shell('example '+Idioma)
        assert '\npreserved\n' in shell('cat 출력예제.'+('py' if Idioma=='python' else Idioma))
        assert '한/영 Chave_VALOR, Shift+Space 또는 F9' in shell('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in shell('echo GUI NETWORK TOGETHER')
        transferencia_de_ficheiros_conexión.quit();transferencia_de_ficheiros_conexión=None;assert 'FTP stopped' in shell('ftpd stop')
        print('PASS '+Idioma+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if transferencia_de_ficheiros_conexión:
            try:transferencia_de_ficheiros_conexión.close()
            except OSError:pass
        if cliente:cliente.close()
        Proceso.terminate()
        try:Proceso.wait(timeout=8)
        except subprocess.TimeoutExpired:Proceso.kill();Proceso.wait()
        준비선택기.close();Proceso.stdout.close();(medida_datos/(Idioma+'-serial.log')).write_bytes(대화기록)


def Executar_2():
    medida_datos=Project_raíz/'build/verification/examples';medida_datos.mkdir(parents=True,exist_ok=True)
    validación_informe={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_raíz/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with eco_Servidores() as eco_servidor_introdución:
            for Idioma in ('java','c','python'):
                test_언어(Idioma,eco_servidor_introdución,medida_datos);validación_informe['languages'].append(Idioma)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert eco_servidor_introdución.수신됨==[(Categoría_VALOR,datos.encode()) for Categoría_VALOR,datos in 예상결과],eco_servidor_introdución.수신됨
            validación_informe['host_network_payloads']=[{'protocol':Categoría_VALOR,'text':datos.decode()} for Categoría_VALOR,datos in eco_servidor_introdución.수신됨]
        validación_informe.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(medida_datos/'report.json').write_text(json.dumps(validación_informe,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Executar_2()
