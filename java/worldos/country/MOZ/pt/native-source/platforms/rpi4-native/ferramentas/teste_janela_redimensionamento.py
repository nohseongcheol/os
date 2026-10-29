#!/usr/bin/env python3
"""real_dados QEMU/VNC에서 terminal 모서리 arrastar_VALOR·ponteiro·동적 caractere_VALOR slot_entrada·Editar_VALOR Conteúdo_VALOR 보존를 검사한다."""
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
from PIL import Image
from desktop_Exibir import EXATO_VALOR
from Executar_comando import ação_raiz


def teste_janela_redimensionamento(너비, altura_VALOR, RC_caminho):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); número_da_porta = 임시.getsockname()[1]
    dimensionar_SMS = '{}x{}'.format(너비, altura_VALOR)
    Processo_VALOR = subprocess.Popen(['python3', str(ação_raiz/'ferramentas/Executar_comando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(número_da_porta), '--resolution', dimensionar_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    seletor_a916db4e = selectors.DefaultSelector(); seletor_a916db4e.register(Processo_VALOR.stdout, selectors.EVENT_READ)
    LOG_linha = bytearray(); remoto_VALOR = None; Transferir_VALOR = None; ponteiro_Oculta=[False]

    def 기다리기(mostrar_VALOR, iniciar=0):
        data_limite_VALOR = time.monotonic() + 60
        while mostrar_VALOR not in LOG_linha[iniciar:]:
            if time.monotonic() > data_limite_VALOR or Processo_VALOR.poll() is not None or b'HALTED' in LOG_linha or b'PANIC:' in LOG_linha:
                raise AssertionError(LOG_linha[iniciar:].decode('utf-8', 'replace'))
            for Evento, _ in seletor_a916db4e.select(.1):
                dados = Evento.fileobj.read(65536)
                if dados: LOG_linha.extend(dados)
        return LOG_linha[iniciar:].decode('utf-8', 'replace')

    def clicar_botão(símbolo, 눌림=True): remoto_VALOR.sendall(struct.pack('>BBHI', 4, int(눌림), 0, símbolo))

    def enviar_SMS(texto):
        iniciar = len(LOG_linha)
        for caractere_VALOR in texto:
            símbolo = 0xff0d if caractere_VALOR == '\n' else ord(caractere_VALOR) if ord(caractere_VALOR) < 256 else 0x1000000 | ord(caractere_VALOR)
            clicar_botão(símbolo); clicar_botão(símbolo, False)
        return iniciar

    def shell(texto): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', enviar_SMS(texto+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Vertical_cargo, 눌림): remoto_VALOR.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertical_cargo))

    def clicar_VALOR(가로, Vertical_cargo): 가리키기(가로, Vertical_cargo, 1); 가리키기(가로, Vertical_cargo, 0)

    def bitmap_foto():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 real_dados 너비를 쓴다.
        remoto_VALOR.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, altura_VALOR))
        desenho_VALOR = Image.new('RGB', (너비, altura_VALOR)); área_VALOR_9285603e = 0
        while True:
            Tipo_VALOR = EXATO_VALOR(remoto_VALOR, 1)[0]
            if Tipo_VALOR == 2: continue
            if Tipo_VALOR == 3:
                duração_VALOR = struct.unpack('>I', EXATO_VALOR(remoto_VALOR, 7)[3:])[0]; EXATO_VALOR(remoto_VALOR, duração_VALOR); continue
            assert Tipo_VALOR == 0, Tipo_VALOR
            item_CONT_NÚM = struct.unpack('>H', EXATO_VALOR(remoto_VALOR, 3)[1:])[0]
            for _ in range(item_CONT_NÚM):
                가로, Vertical_cargo, 폭, duração_VALOR, Codificação_VALOR = struct.unpack('>HHHHi', EXATO_VALOR(remoto_VALOR, 12))
                if Codificação_VALOR == -239:
                    assert 폭==0 and duração_VALOR==0, 'remote cursor must be hidden'
                    ponteiro_Oculta[0]=True
                    continue
                assert Codificação_VALOR == 0 and 가로+폭 <= 너비 and Vertical_cargo+duração_VALOR <= altura_VALOR
                desenho_VALOR.paste(Image.frombytes('RGB', (폭, duração_VALOR), EXATO_VALOR(remoto_VALOR, 폭*duração_VALOR*4), 'raw', 'BGRX'), (가로, Vertical_cargo))
                área_VALOR_9285603e += 폭*duração_VALOR
            if área_VALOR_9285603e:
                assert área_VALOR_9285603e == 너비*altura_VALOR, área_VALOR_9285603e
                return desenho_VALOR

    def cheque_pixel(coordenada_VALOR, 색):
        data_limite_VALOR = time.monotonic()+10
        while True:
            desenho_VALOR = bitmap_foto()
            if desenho_VALOR.getpixel(coordenada_VALOR) == 색: return desenho_VALOR
            if time.monotonic() > data_limite_VALOR: raise AssertionError((coordenada_VALOR, desenho_VALOR.getpixel(coordenada_VALOR), 색))

    def Upload_Arquivos(Nome, dados): Transferir_VALOR.storbinary('STOR '+Nome, io.BytesIO(dados))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+dimensionar_SMS+' RGB32').encode() in LOG_linha
        print('BOOT:', dimensionar_SMS, flush=True)
        remoto_número = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_linha).group(1))
        remoto_VALOR = socket.create_connection(('127.0.0.1', remoto_número), timeout=20)
        assert EXATO_VALOR(remoto_VALOR, 12) == b'RFB 003.008\n'; remoto_VALOR.sendall(b'RFB 003.008\n')
        assert 1 in EXATO_VALOR(remoto_VALOR, EXATO_VALOR(remoto_VALOR, 1)[0]); remoto_VALOR.sendall(b'\x01')
        assert EXATO_VALOR(remoto_VALOR, 4) == b'\0'*4; remoto_VALOR.sendall(b'\x01')
        estado_inicial = EXATO_VALOR(remoto_VALOR, 24); assert struct.unpack('>HH', estado_inicial[:4]) == (너비, altura_VALOR)
        EXATO_VALOR(remoto_VALOR, struct.unpack('>I', estado_inicial[20:])[0])
        remoto_VALOR.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        remoto_VALOR.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        cheque_pixel((너비-1, altura_VALOR-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Evento,_ in seletor_a916db4e.select(.02):
                    dados=Evento.fileobj.read(65536)
                    if dados:LOG_linha.extend(dados)
        Janela=[12,48,568,360]
        def verificar_dimensionar():
            COL_VALOR,LIN_VALOR=(Janela[2]-24)//8,(Janela[3]-56)//16
            texto=shell('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COL_VALOR,LIN_VALOR) in texto,texto
            # real_dados Janela 테두리: 단지 Tamanho consulta_VALOR 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            cheque_pixel((Janela[0],Janela[1]),(32,80,144))
            desenho_VALOR=cheque_pixel((Janela[0]+Janela[2]-1,Janela[1]+Janela[3]-1),(39,49,64))
            return desenho_VALOR
        def 모서리(direção):
            return (Janela[0]+(3 if direção in (1,3) else Janela[2]-4),Janela[1]+(3 if direção<=2 else Janela[3]-4))
        def redimensionar_arrastar(direção,차이,botão=1):
            가,세=모서리(direção);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if direção in (1,4) else 가+7,세-7)
            cheque_pixel(흰점,(255,255,255))
            가리키기(가,세,botão)
            끝가=max(0,min(너비-1,가+차이[0]));encerrar_Vertical=max(0,min(altura_VALOR-1,세+차이[1]))
            가리키기(끝가,encerrar_Vertical,botão);가리키기(끝가,encerrar_Vertical,0);숨고르기()
            if botão==1:
                ESQUERDA_VALOR,위,폭,duração_VALOR=Janela;DIREITA_VALOR,아래=ESQUERDA_VALOR+폭,위+duração_VALOR
                if direção in (1,3):ESQUERDA_VALOR=max(0,min(DIREITA_VALOR-360,ESQUERDA_VALOR+끝가-가))
                else:DIREITA_VALOR=max(ESQUERDA_VALOR+360,min(너비,DIREITA_VALOR+끝가-가))
                if direção<=2:위=max(34,min(아래-216,위+encerrar_Vertical-세))
                else:아래=max(위+216,min(altura_VALOR,아래+encerrar_Vertical-세))
                Janela[:]=[ESQUERDA_VALOR,위,DIREITA_VALOR-ESQUERDA_VALOR,아래-위]
        verificar_dimensionar();assert ponteiro_Oculta[0]
        redimensionar_arrastar(4,(-100,-60),4);verificar_dimensionar() # DIREITA 버튼은 크기를 바꾸지 않는다.
        for direção,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            redimensionar_arrastar(direção,차이);verificar_dimensionar()
        # entrada_VALOR 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        enviar_SMS("echo '"+긴글+"'");숨고르기()
        redimensionar_arrastar(4,(-1000,-1000));assert Janela[2:]==[360,216]
        redimensionar_arrastar(4,(너비,altura_VALOR))
        iniciar=enviar_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),iniciar);verificar_dimensionar()
        # vi가 Editar_VALOR 중에 tela 크기를 repetir_VALOR 읽고, 저장하지 않은 한글도 유지한다.
        shell('ftpd start')
        Transferir_VALOR=ftplib.FTP();Transferir_VALOR.encoding='utf-8';Transferir_VALOR.connect('127.0.0.1',número_da_porta,timeout=20);Transferir_VALOR.login()
        기다리기(b'NORMAL',enviar_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',enviar_SMS('i미저장 한글 dados\n'));숨고르기()
        redimensionar_arrastar(4,(-너비,-altura_VALOR))
        # ANSI LIN_VALOR 이동에 새 LIN_VALOR 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Janela[3]-56)//16)).encode() in LOG_linha[-4096:]
        enviar_SMS('작은 창에서도 이어 Escrita\n');숨고르기()
        redimensionar_arrastar(4,(너비,altura_VALOR))
        enviar_SMS('큰 창에서도 이어 Escrita\n');숨고르기()
        clicar_botão(0xff1b);clicar_botão(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',enviar_SMS(':wq\n'))
        Conteúdo_VALOR=bytearray();Transferir_VALOR.retrbinary('RETR 크기자료.txt',Conteúdo_VALOR.extend)
        assert Conteúdo_VALOR=='미저장 한글 dados\n작은 창에서도 이어 Escrita\n큰 창에서도 이어 Escrita\n'.encode(),Conteúdo_VALOR
        verificar_dimensionar().save(str(RC_caminho/(dimensionar_SMS+'-large.png')))
        # 두 번째 창은 valor_padrão Tamanho, repetir_VALOR 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        iniciar=len(LOG_linha);clicar_VALOR(70,16);기다리기(b'TERMINAL FOCUS 2',iniciar)
        assert 'TERMINAL SIZE 68x19' in shell('terminal size')
        iniciar=len(LOG_linha);clicar_VALOR(180,16);기다리기(b'TERMINAL FOCUS 1',iniciar);verificar_dimensionar()
        redimensionar_arrastar(4,(-너비,-altura_VALOR));verificar_dimensionar().save(str(RC_caminho/(dimensionar_SMS+'-small.png')))
        # Tamanho alterar_VALOR BACK_VALOR X 닫기도 새로운 DIREITA 가장자리를 사용한다.
        iniciar=len(LOG_linha);clicar_VALOR(Janela[0]+Janela[2]-20,Janela[1]+15);기다리기(b'TERMINAL FOCUS 2',iniciar)
        assert 'RESIZE CLOSED' in shell('echo RESIZE CLOSED')
        print('PASS:',dimensionar_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if Transferir_VALOR:Transferir_VALOR.close()
        if remoto_VALOR:remoto_VALOR.close()
        if Processo_VALOR.poll() is None:
            Processo_VALOR.terminate()
            try:Processo_VALOR.wait(timeout=8)
            except subprocess.TimeoutExpired:Processo_VALOR.kill();Processo_VALOR.wait()
        seletor_a916db4e.close();Processo_VALOR.stdout.close();(RC_caminho/(dimensionar_SMS+'.log')).write_bytes(LOG_linha)


def iniciar():
    RC_caminho=ação_raiz/'build/verification/resize';RC_caminho.mkdir(parents=True,exist_ok=True)
    LOG_linha={'passed':False,'kernel_sha256':hashlib.sha256((ação_raiz/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,altura_VALOR in ((640,480),(1920,1080)):
            teste_janela_redimensionamento(너비,altura_VALOR,RC_caminho);LOG_linha['resolutions'].append([너비,altura_VALOR])
        LOG_linha.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(RC_caminho/'report.json').write_text(json.dumps(LOG_linha,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':iniciar()
