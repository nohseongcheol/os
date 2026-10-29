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
from desktop_Exibir import EXATO_VALOR
from 예제되돌림서버 import eco_Servidores
from Executar_comando import ação_raiz


def teste_Idioma(Idioma,eco_servidor_entrada,RC_dados):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));transferência_de_arquivo_número_da_porta=임시자원.getsockname()[1]
    Processo=subprocess.Popen(['python3',str(ação_raiz/'ferramentas/Executar_comando.py'),'--desktop','--network','--port','0','--ftp-port',str(transferência_de_arquivo_número_da_porta)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    seletor=selectors.DefaultSelector();seletor.register(Processo.stdout,selectors.EVENT_READ)
    transcrição=bytearray();cliente=None;transferência_de_arquivo_conexão=None
    def receber_email(favorito,iniciar=0):
        encerrar_DESLOC=time.monotonic()+60
        while favorito not in transcrição[iniciar:]:
            if time.monotonic()>encerrar_DESLOC or Processo.poll() is not None:raise AssertionError(transcrição[iniciar:].decode('utf-8','replace'))
            for 누름값,_ in seletor.select(.1):
                dados=누름값.fileobj.read(65536)
                if dados:transcrição.extend(dados)
        return transcrição[iniciar:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(símbolo_VALOR,누르는중=True):cliente.sendall(struct.pack('>BBHI',4,int(누르는중),0,símbolo_VALOR))
    def START_DESLOC(linha_de_entrada):
        iniciar=len(transcrição)
        for ponto_de_código in linha_de_entrada+'\n':
            símbolo_VALOR=0xff0d if ponto_de_código=='\n' else ord(ponto_de_código) if ord(ponto_de_código)<256 else 0x1000000|ord(ponto_de_código)
            누름값(símbolo_VALOR);누름값(símbolo_VALOR,False)
        return iniciar
    def shell(linha_de_entrada):return receber_email(b'jkoros-native> ',START_DESLOC(linha_de_entrada))
    def Executar_comando(linha_de_entrada,예상결과):
        texto=shell(linha_de_entrada);assert 예상결과 in texto and 'exit 0' in texto,(linha_de_entrada,texto)
        return texto
    def 화소들():
        cliente.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            área_VALOR=EXATO_VALOR(cliente,1)[0]
            if área_VALOR==2:continue
            if área_VALOR==3:
                item_CONT_NÚM=struct.unpack('>I',EXATO_VALOR(cliente,7)[3:])[0];EXATO_VALOR(cliente,item_CONT_NÚM);continue
            assert área_VALOR==0,área_VALOR
            entrada_CONT_NÚM_8f7753a1=struct.unpack('>H',EXATO_VALOR(cliente,3)[1:])[0]
            for _ in range(entrada_CONT_NÚM_8f7753a1):
                coordenada_X,Y_coordenada,너비값,solicitado_altura_VALOR,conjunto_de_caracteres=struct.unpack('>HHHHi',EXATO_VALOR(cliente,12));assert conjunto_de_caracteres==0,conjunto_de_caracteres
                dados=EXATO_VALOR(cliente,너비값*solicitado_altura_VALOR*4)
                for LIN_cargo in range(solicitado_altura_VALOR):
                    for COL_cargo in range(너비값):
                        원본자료=(LIN_cargo*너비값+COL_cargo)*4;meta=((Y_coordenada+LIN_cargo)*640+coordenada_X+COL_cargo)*3
                        빛삼원색[meta:meta+3]=bytes((dados[원본자료+2],dados[원본자료+1],dados[원본자료]))
            if entrada_CONT_NÚM_8f7753a1:return 빛삼원색
    try:
        receber_email(b'TERMINAL READY');receber_email(b'jkoros-native> ',transcrição.rfind(b'TERMINAL READY'))
        número_da_porta=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transcrição).group(1))
        cliente=socket.create_connection(('127.0.0.1',número_da_porta),timeout=10)
        assert EXATO_VALOR(cliente,12)==b'RFB 003.008\n';cliente.sendall(b'RFB 003.008\n')
        assert 1 in EXATO_VALOR(cliente,EXATO_VALOR(cliente,1)[0]);cliente.sendall(b'\x01');assert EXATO_VALOR(cliente,4)==b'\0'*4
        cliente.sendall(b'\x01');초기값=EXATO_VALOR(cliente,24);EXATO_VALOR(cliente,struct.unpack('>I',초기값[20:])[0])
        cliente.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        cliente.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in shell('ftpd start')
        transferência_de_arquivo_conexão=ftplib.FTP();transferência_de_arquivo_conexão.encoding='utf-8';transferência_de_arquivo_conexão.connect('127.0.0.1',transferência_de_arquivo_número_da_porta,timeout=20);transferência_de_arquivo_conexão.login()
        carga_dados=('GUI와 FTP 동시 uso_VALOR '+Idioma+' 😀\n').encode()
        transferência_de_arquivo_conexão.storbinary('STOR 함께.txt',io.BytesIO(carga_dados))
        assert carga_dados.decode().strip() in shell('cat /함께.txt')
        RECEBER_CONT_NÚM=bytearray();transferência_de_arquivo_conexão.retrbinary('RETR 함께.txt',RECEBER_CONT_NÚM.extend);assert RECEBER_CONT_NÚM==carga_dados;transferência_de_arquivo_conexão.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        enviar_Lista=shell('ls /example')
        assert all(Nome in enviar_Lista for Nome in ('java/','c/','python/','README.md')),enviar_Lista
        if Idioma=='java':
            grupo_manifesto=json.loads((ação_raiz/'build/examples/manifest.json').read_text())
            for caminho,ponto_de_entrada in grupo_manifesto.items():
                shell('cp '+caminho+' /example-check.bin')
                Conteúdo_VALOR=bytearray();transferência_de_arquivo_conexão.retrbinary('RETR example-check.bin',Conteúdo_VALOR.extend)
                assert len(Conteúdo_VALOR)==ponto_de_entrada['bytes'] and hashlib.sha256(Conteúdo_VALOR).hexdigest()==ponto_de_entrada['sha256'],caminho
            transferência_de_arquivo_conexão.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            base_2=bytes(range(256))*64
            transferência_de_arquivo_conexão.storbinary('STOR boundary.bin',io.BytesIO(base_2))
            Conteúdo_VALOR=bytearray();transferência_de_arquivo_conexão.retrbinary('RETR boundary.bin',Conteúdo_VALOR.extend)
            assert Conteúdo_VALOR==base_2 and 'boundary.bin' in transferência_de_arquivo_conexão.nlst()
            shell('cp /boundary.bin /boundary-copy.bin')
            Conteúdo_VALOR=bytearray();transferência_de_arquivo_conexão.retrbinary('RETR boundary-copy.bin',Conteúdo_VALOR.extend)
            assert Conteúdo_VALOR==base_2
            transferência_de_arquivo_conexão.delete('boundary.bin');transferência_de_arquivo_conexão.delete('boundary-copy.bin')
        assert 'ExemploSaída' in shell('ls /example/'+Idioma)
        shell('cd /example/'+Idioma)
        nome_tabela={'java':'JAVA','c':'C','python':'PYTHON'}[Idioma]
        예상파일=nome_tabela+' ficheiro: 한글 dados 😀\n'
        if Idioma=='java':
            Executar_comando('javac ExemploSaída.java','Compiled:');Executar_comando('java ExemploSaída','JAVA saídaTexto: 안녕하세요 😀')
            Executar_comando('javac ExemploFicheiro.java','Compiled:');Executar_comando('java ExemploFicheiro',예상파일)
            Executar_comando('java ExemploRede {} {}'.format(eco_servidor_entrada.porta_TCP,eco_servidor_entrada.UDP_porta),'JAVA 네트워크 verificar: TCP UDP 한글')
            gráficos_comando='java ExemploDesenho'
        elif Idioma=='c':
            for Nome,전달값,예상결과 in [('saídaTexto','', 'C saídaTexto: 안녕하세요 😀'),('ficheiro','',예상파일),
                    ('네트워크',' '+str(eco_servidor_entrada.UDP_porta),'C 네트워크 verificar: UDP 한글')]:
                Executar_comando('cc '+Nome+'예제.c -o Executar_comando','Compiled native ARM64 ELF:')
                Executar_comando('./Executar_comando'+전달값,예상결과)
            Executar_comando('cc ExemploDesenho.c -o Executar_comando','Compiled native ARM64 ELF:');gráficos_comando='./Executar_comando'
        else:
            for Nome,전달값,예상결과 in [('saídaTexto','','PYTHON saídaTexto: 안녕하세요 😀'),('ficheiro','',예상파일),
                    ('네트워크',' '+str(eco_servidor_entrada.UDP_porta),'PYTHON 네트워크 verificar: UDP 한글')]:
                Executar_comando('python '+Nome+'예제.py'+전달값,예상결과)
            gráficos_comando='python ExemploDesenho.py'
        START_desenho=START_DESLOC(gráficos_comando)
        texto=receber_email('그림을 확인한 BACK_VALOR Enter를 누르세요.\r\n'.encode(),START_desenho)
        assert nome_tabela+' 그래픽: 빨강 초록 파랑' in texto and 'exit 0' not in texto,texto
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        transferência_de_arquivo_conexão.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEBER_CONT_NÚM=bytearray();transferência_de_arquivo_conexão.retrbinary('RETR 도중.txt',RECEBER_CONT_NÚM.extend);assert RECEBER_CONT_NÚM==b'FTP DURING GRAPHICS';transferência_de_arquivo_conexão.delete('도중.txt')
        빛삼원색=화소들()
        for Y_coordenada,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            DESLOC_VALOR=(Y_coordenada*640+610)*3;assert tuple(빛삼원색[DESLOC_VALOR:DESLOC_VALOR+3])==색상,(Idioma,Y_coordenada,tuple(빛삼원색[DESLOC_VALOR:DESLOC_VALOR+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(RC_dados/(Idioma+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in receber_email(b'jkoros-native> ',START_desenho)
        if Idioma=='java':
            START_janela=START_DESLOC('java ExemploJanela')
            receber_email('GUI 예제 Preparar: ExemploJanela'.encode(),START_janela)
            def clicar_VALOR(가로,Vertical_cargo):
                for botão in (1,0):cliente.sendall(struct.pack('>BBHH',5,botão,가로,Vertical_cargo))
            time.sleep(.3)
            Anterior_foto=Image.frombytes('RGB',(640,480),bytes(화소들()))
            clicar_VALOR(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for caractere_VALOR in '한글':누름값(0x1000000|ord(caractere_VALOR));누름값(0x1000000|ord(caractere_VALOR),False)
            for repetição_CONT_NÚM in (1,2):
                iniciar=len(transcrição);clicar_VALOR(180,242)
                receber_email(('GUI saudação_ae353e94: 안녕하세요, 한글님! ('+str(repetição_CONT_NÚM)+')').encode(),iniciar)
            time.sleep(.3)
            janela_desenho=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert Anterior_foto.crop((110,272,530,300)).tobytes()!=janela_desenho.crop((110,272,530,300)).tobytes()
            janela_desenho.save(str(RC_dados/'java-swing.png'))
            iniciar=len(transcrição);clicar_VALOR(535,105)
            assert 'exit 0' in receber_email(b'jkoros-native> ',iniciar)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Arquivo_entrada_nome={'java':'java.txt','c':'c.txt','python':'python.txt'}[Idioma]
        shell('cp '+Arquivo_entrada_nome+' /validar.txt')
        RECEBER_CONT_NÚM=bytearray();transferência_de_arquivo_conexão.retrbinary('RETR validar.txt',RECEBER_CONT_NÚM.extend);assert RECEBER_CONT_NÚM==예상파일.encode()
        shell('echo preserved > ExemploSaída.'+('py' if Idioma=='python' else Idioma))
        assert 'EXAMPLES READY' in shell('example '+Idioma)
        assert '\npreserved\n' in shell('cat ExemploSaída.'+('py' if Idioma=='python' else Idioma))
        assert '한/zero_operando Chave_VALOR, Shift+Space 또는 F9' in shell('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in shell('echo GUI NETWORK TOGETHER')
        transferência_de_arquivo_conexão.quit();transferência_de_arquivo_conexão=None;assert 'FTP stopped' in shell('ftpd stop')
        print('PASS '+Idioma+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if transferência_de_arquivo_conexão:
            try:transferência_de_arquivo_conexão.close()
            except OSError:pass
        if cliente:cliente.close()
        Processo.terminate()
        try:Processo.wait(timeout=8)
        except subprocess.TimeoutExpired:Processo.kill();Processo.wait()
        seletor.close();Processo.stdout.close();(RC_dados/(Idioma+'-serial.log')).write_bytes(transcrição)


def iniciar():
    RC_dados=ação_raiz/'build/verification/examples';RC_dados.mkdir(parents=True,exist_ok=True)
    validação_relatar={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ação_raiz/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with eco_Servidores() as eco_servidor_entrada:
            for Idioma in ('java','c','python'):
                teste_Idioma(Idioma,eco_servidor_entrada,RC_dados);validação_relatar['languages'].append(Idioma)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert eco_servidor_entrada.수신됨==[(área_VALOR,dados.encode()) for área_VALOR,dados in 예상결과],eco_servidor_entrada.수신됨
            validação_relatar['host_network_payloads']=[{'protocol':área_VALOR,'text':dados.decode()} for área_VALOR,dados in eco_servidor_entrada.수신됨]
        validação_relatar.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(RC_dados/'report.json').write_text(json.dumps(validação_relatar,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':iniciar()
