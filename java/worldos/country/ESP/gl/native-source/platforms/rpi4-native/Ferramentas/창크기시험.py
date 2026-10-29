#!/usr/bin/env python3
"""real_datos QEMU/VNC에서 Terminal 모서리 arrastrar_VALOR·punteiro·동적 carácter_VALOR 칸·editar_VALOR Contido_VALOR 보존를 검사한다."""
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
from escritorio_ver import EXACTO_VALOR
from executar_comando import Project_raíz


def 창크기시험(너비, 높이, medida_camiño):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); número_do_porto = 임시.getsockname()[1]
    크기글 = '{}x{}'.format(너비, 높이)
    Proceso_VALOR = subprocess.Popen(['python3', str(Project_raíz/'Ferramentas/executar_comando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(número_do_porto), '--resolution', 크기글], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector(); 선택기.register(Proceso_VALOR.stdout, selectors.EVENT_READ)
    LOG_fila = bytearray(); remoto_VALOR = None; Transferir_VALOR = None; punteiro_Oculto=[False]

    def 기다리기(mostrar_VALOR, Executar_2=0):
        마감 = time.monotonic() + 60
        while mostrar_VALOR not in LOG_fila[Executar_2:]:
            if time.monotonic() > 마감 or Proceso_VALOR.poll() is not None or b'HALTED' in LOG_fila or b'PANIC:' in LOG_fila:
                raise AssertionError(LOG_fila[Executar_2:].decode('utf-8', 'replace'))
            for Evento, _ in 선택기.select(.1):
                datos = Evento.fileobj.read(65536)
                if datos: LOG_fila.extend(datos)
        return LOG_fila[Executar_2:].decode('utf-8', 'replace')

    def clic_botón(símbolo, 눌림=True): remoto_VALOR.sendall(struct.pack('>BBHI', 4, int(눌림), 0, símbolo))

    def enviar_SMS(Texto):
        Executar_2 = len(LOG_fila)
        for carácter_VALOR in Texto:
            símbolo = 0xff0d if carácter_VALOR == '\n' else ord(carácter_VALOR) if ord(carácter_VALOR) < 256 else 0x1000000 | ord(carácter_VALOR)
            clic_botón(símbolo); clic_botón(símbolo, False)
        return Executar_2

    def shell(Texto): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', enviar_SMS(Texto+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Vertical_cargo, 눌림): remoto_VALOR.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertical_cargo))

    def clic_VALOR(가로, Vertical_cargo): 가리키기(가로, Vertical_cargo, 1); 가리키기(가로, Vertical_cargo, 0)

    def mapa_de_bits_IMAXE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 real_datos 너비를 쓴다.
        remoto_VALOR.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        그림 = Image.new('RGB', (너비, 높이)); área_VALOR = 0
        while True:
            종류 = EXACTO_VALOR(remoto_VALOR, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                duración_VALOR = struct.unpack('>I', EXACTO_VALOR(remoto_VALOR, 7)[3:])[0]; EXACTO_VALOR(remoto_VALOR, duración_VALOR); continue
            assert 종류 == 0, 종류
            elemento_CONTAR = struct.unpack('>H', EXACTO_VALOR(remoto_VALOR, 3)[1:])[0]
            for _ in range(elemento_CONTAR):
                가로, Vertical_cargo, 폭, duración_VALOR, codificación_VALOR = struct.unpack('>HHHHi', EXACTO_VALOR(remoto_VALOR, 12))
                if codificación_VALOR == -239:
                    assert 폭==0 and duración_VALOR==0, 'remote cursor must be hidden'
                    punteiro_Oculto[0]=True
                    continue
                assert codificación_VALOR == 0 and 가로+폭 <= 너비 and Vertical_cargo+duración_VALOR <= 높이
                그림.paste(Image.frombytes('RGB', (폭, duración_VALOR), EXACTO_VALOR(remoto_VALOR, 폭*duración_VALOR*4), 'raw', 'BGRX'), (가로, Vertical_cargo))
                área_VALOR += 폭*duración_VALOR
            if área_VALOR:
                assert área_VALOR == 너비*높이, área_VALOR
                return 그림

    def cheque_píxel(coordenada_VALOR, 색):
        마감 = time.monotonic()+10
        while True:
            그림 = mapa_de_bits_IMAXE()
            if 그림.getpixel(coordenada_VALOR) == 색: return 그림
            if time.monotonic() > 마감: raise AssertionError((coordenada_VALOR, 그림.getpixel(coordenada_VALOR), 색))

    def carga_Ficheiros(Nome, datos): Transferir_VALOR.storbinary('STOR '+Nome, io.BytesIO(datos))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+크기글+' RGB32').encode() in LOG_fila
        print('BOOT:', 크기글, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_fila).group(1))
        remoto_VALOR = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACTO_VALOR(remoto_VALOR, 12) == b'RFB 003.008\n'; remoto_VALOR.sendall(b'RFB 003.008\n')
        assert 1 in EXACTO_VALOR(remoto_VALOR, EXACTO_VALOR(remoto_VALOR, 1)[0]); remoto_VALOR.sendall(b'\x01')
        assert EXACTO_VALOR(remoto_VALOR, 4) == b'\0'*4; remoto_VALOR.sendall(b'\x01')
        초기 = EXACTO_VALOR(remoto_VALOR, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACTO_VALOR(remoto_VALOR, struct.unpack('>I', 초기[20:])[0])
        remoto_VALOR.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        remoto_VALOR.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        cheque_píxel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Evento,_ in 선택기.select(.02):
                    datos=Evento.fileobj.read(65536)
                    if datos:LOG_fila.extend(datos)
        Xanela=[12,48,568,360]
        def 크기확인():
            COLUMNA_VALOR,FILA_VALOR=(Xanela[2]-24)//8,(Xanela[3]-56)//16
            Texto=shell('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMNA_VALOR,FILA_VALOR) in Texto,Texto
            # real_datos Xanela 테두리: 단지 Tamaño consulta_VALOR 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            cheque_píxel((Xanela[0],Xanela[1]),(32,80,144))
            그림=cheque_píxel((Xanela[0]+Xanela[2]-1,Xanela[1]+Xanela[3]-1),(39,49,64))
            return 그림
        def 모서리(방향):
            return (Xanela[0]+(3 if 방향 in (1,3) else Xanela[2]-4),Xanela[1]+(3 if 방향<=2 else Xanela[3]-4))
        def redimensionar_arrastrar(방향,차이,botón=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            cheque_píxel(흰점,(255,255,255))
            가리키기(가,세,botón)
            끝가=max(0,min(너비-1,가+차이[0]));finalizar_Vertical=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,finalizar_Vertical,botón);가리키기(끝가,finalizar_Vertical,0);숨고르기()
            if botón==1:
                ESQUERDA_VALOR,위,폭,duración_VALOR=Xanela;DEREITA_VALOR,아래=ESQUERDA_VALOR+폭,위+duración_VALOR
                if 방향 in (1,3):ESQUERDA_VALOR=max(0,min(DEREITA_VALOR-360,ESQUERDA_VALOR+끝가-가))
                else:DEREITA_VALOR=max(ESQUERDA_VALOR+360,min(너비,DEREITA_VALOR+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+finalizar_Vertical-세))
                else:아래=max(위+216,min(높이,아래+finalizar_Vertical-세))
                Xanela[:]=[ESQUERDA_VALOR,위,DEREITA_VALOR-ESQUERDA_VALOR,아래-위]
        크기확인();assert punteiro_Oculto[0]
        redimensionar_arrastrar(4,(-100,-60),4);크기확인() # DEREITA 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            redimensionar_arrastrar(방향,차이);크기확인()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        enviar_SMS("echo '"+긴글+"'");숨고르기()
        redimensionar_arrastrar(4,(-1000,-1000));assert Xanela[2:]==[360,216]
        redimensionar_arrastrar(4,(너비,높이))
        Executar_2=enviar_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Executar_2);크기확인()
        # vi가 editar_VALOR 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        shell('ftpd start')
        Transferir_VALOR=ftplib.FTP();Transferir_VALOR.encoding='utf-8';Transferir_VALOR.connect('127.0.0.1',número_do_porto,timeout=20);Transferir_VALOR.login()
        기다리기(b'NORMAL',enviar_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',enviar_SMS('i미저장 한글 datos\n'));숨고르기()
        redimensionar_arrastrar(4,(-너비,-높이))
        # ANSI FILA_VALOR 이동에 새 FILA_VALOR 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Xanela[3]-56)//16)).encode() in LOG_fila[-4096:]
        enviar_SMS('작은 창에서도 이어 Escritura\n');숨고르기()
        redimensionar_arrastrar(4,(너비,높이))
        enviar_SMS('큰 창에서도 이어 Escritura\n');숨고르기()
        clic_botón(0xff1b);clic_botón(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',enviar_SMS(':wq\n'))
        Contido_VALOR=bytearray();Transferir_VALOR.retrbinary('RETR 크기자료.txt',Contido_VALOR.extend)
        assert Contido_VALOR=='미저장 한글 datos\n작은 창에서도 이어 Escritura\n큰 창에서도 이어 Escritura\n'.encode(),Contido_VALOR
        크기확인().save(str(medida_camiño/(크기글+'-large.png')))
        # 두 번째 창은 valor_predefinido Tamaño, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Executar_2=len(LOG_fila);clic_VALOR(70,16);기다리기(b'TERMINAL FOCUS 2',Executar_2)
        assert 'TERMINAL SIZE 68x19' in shell('terminal size')
        Executar_2=len(LOG_fila);clic_VALOR(180,16);기다리기(b'TERMINAL FOCUS 1',Executar_2);크기확인()
        redimensionar_arrastrar(4,(-너비,-높이));크기확인().save(str(medida_camiño/(크기글+'-small.png')))
        # Tamaño modificar_VALOR ATRÁS_VALOR X 닫기도 새로운 DEREITA 가장자리를 사용한다.
        Executar_2=len(LOG_fila);clic_VALOR(Xanela[0]+Xanela[2]-20,Xanela[1]+15);기다리기(b'TERMINAL FOCUS 2',Executar_2)
        assert 'RESIZE CLOSED' in shell('echo RESIZE CLOSED')
        print('PASS:',크기글,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if Transferir_VALOR:Transferir_VALOR.close()
        if remoto_VALOR:remoto_VALOR.close()
        if Proceso_VALOR.poll() is None:
            Proceso_VALOR.terminate()
            try:Proceso_VALOR.wait(timeout=8)
            except subprocess.TimeoutExpired:Proceso_VALOR.kill();Proceso_VALOR.wait()
        선택기.close();Proceso_VALOR.stdout.close();(medida_camiño/(크기글+'.log')).write_bytes(LOG_fila)


def Executar_2():
    medida_camiño=Project_raíz/'build/verification/resize';medida_camiño.mkdir(parents=True,exist_ok=True)
    LOG_fila={'passed':False,'kernel_sha256':hashlib.sha256((Project_raíz/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,medida_camiño);LOG_fila['resolutions'].append([너비,높이])
        LOG_fila.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(medida_camiño/'report.json').write_text(json.dumps(LOG_fila,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Executar_2()
