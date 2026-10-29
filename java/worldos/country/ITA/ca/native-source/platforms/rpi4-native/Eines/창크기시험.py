#!/usr/bin/env python3
"""real_dades QEMU/VNC에서 Terminal 모서리 arrossegar_VALOR·punter·동적 caràcter_VALOR 칸·Editar_VALOR contingut_VALOR 보존를 검사한다."""
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
from escriptori_visualitzar import IGUAL_VALOR
from Executa_ordre import Project_rel


def 창크기시험(너비, 높이, mesura_camí):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); número_de_port = 임시.getsockname()[1]
    canviar_la_mida_SMS = '{}x{}'.format(너비, 높이)
    Procés_VALOR = subprocess.Popen(['python3', str(Project_rel/'Eines/Executa_ordre.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(número_de_port), '--resolution', canviar_la_mida_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector(); 선택기.register(Procés_VALOR.stdout, selectors.EVENT_READ)
    LOG_fila = bytearray(); remot_VALOR = None; transferir_VALOR = None; punter_Amagat=[False]

    def 기다리기(mostrar_VALOR, Executa_2=0):
        마감 = time.monotonic() + 60
        while mostrar_VALOR not in LOG_fila[Executa_2:]:
            if time.monotonic() > 마감 or Procés_VALOR.poll() is not None or b'HALTED' in LOG_fila or b'PANIC:' in LOG_fila:
                raise AssertionError(LOG_fila[Executa_2:].decode('utf-8', 'replace'))
            for Esdeveniment, _ in 선택기.select(.1):
                dades = Esdeveniment.fileobj.read(65536)
                if dades: LOG_fila.extend(dades)
        return LOG_fila[Executa_2:].decode('utf-8', 'replace')

    def clic_botó(símbol, 눌림=True): remot_VALOR.sendall(struct.pack('>BBHI', 4, int(눌림), 0, símbol))

    def enviar_un_SMS(SMS):
        Executa_2 = len(LOG_fila)
        for caràcter_VALOR in SMS:
            símbol = 0xff0d if caràcter_VALOR == '\n' else ord(caràcter_VALOR) if ord(caràcter_VALOR) < 256 else 0x1000000 | ord(caràcter_VALOR)
            clic_botó(símbol); clic_botó(símbol, False)
        return Executa_2

    def shell(SMS): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', enviar_un_SMS(SMS+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Vertical_càrrec, 눌림): remot_VALOR.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertical_càrrec))

    def clic_VALOR(가로, Vertical_càrrec): 가리키기(가로, Vertical_càrrec, 1); 가리키기(가로, Vertical_càrrec, 0)

    def mapa_de_bits_IMATGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 real_dades 너비를 쓴다.
        remot_VALOR.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        dibuix_VALOR = Image.new('RGB', (너비, 높이)); àrea_VALOR = 0
        while True:
            종류 = IGUAL_VALOR(remot_VALOR, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                durada_VALOR = struct.unpack('>I', IGUAL_VALOR(remot_VALOR, 7)[3:])[0]; IGUAL_VALOR(remot_VALOR, durada_VALOR); continue
            assert 종류 == 0, 종류
            element_COMPT = struct.unpack('>H', IGUAL_VALOR(remot_VALOR, 3)[1:])[0]
            for _ in range(element_COMPT):
                가로, Vertical_càrrec, 폭, durada_VALOR, codificació_VALOR = struct.unpack('>HHHHi', IGUAL_VALOR(remot_VALOR, 12))
                if codificació_VALOR == -239:
                    assert 폭==0 and durada_VALOR==0, 'remote cursor must be hidden'
                    punter_Amagat[0]=True
                    continue
                assert codificació_VALOR == 0 and 가로+폭 <= 너비 and Vertical_càrrec+durada_VALOR <= 높이
                dibuix_VALOR.paste(Image.frombytes('RGB', (폭, durada_VALOR), IGUAL_VALOR(remot_VALOR, 폭*durada_VALOR*4), 'raw', 'BGRX'), (가로, Vertical_càrrec))
                àrea_VALOR += 폭*durada_VALOR
            if àrea_VALOR:
                assert àrea_VALOR == 너비*높이, àrea_VALOR
                return dibuix_VALOR

    def xec_píxel(coordenada_VALOR, 색):
        마감 = time.monotonic()+10
        while True:
            dibuix_VALOR = mapa_de_bits_IMATGE()
            if dibuix_VALOR.getpixel(coordenada_VALOR) == 색: return dibuix_VALOR
            if time.monotonic() > 마감: raise AssertionError((coordenada_VALOR, dibuix_VALOR.getpixel(coordenada_VALOR), 색))

    def pujar_Fitxers(Nom, dades): transferir_VALOR.storbinary('STOR '+Nom, io.BytesIO(dades))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+canviar_la_mida_SMS+' RGB32').encode() in LOG_fila
        print('BOOT:', canviar_la_mida_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_fila).group(1))
        remot_VALOR = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert IGUAL_VALOR(remot_VALOR, 12) == b'RFB 003.008\n'; remot_VALOR.sendall(b'RFB 003.008\n')
        assert 1 in IGUAL_VALOR(remot_VALOR, IGUAL_VALOR(remot_VALOR, 1)[0]); remot_VALOR.sendall(b'\x01')
        assert IGUAL_VALOR(remot_VALOR, 4) == b'\0'*4; remot_VALOR.sendall(b'\x01')
        초기 = IGUAL_VALOR(remot_VALOR, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        IGUAL_VALOR(remot_VALOR, struct.unpack('>I', 초기[20:])[0])
        remot_VALOR.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        remot_VALOR.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        xec_píxel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Esdeveniment,_ in 선택기.select(.02):
                    dades=Esdeveniment.fileobj.read(65536)
                    if dades:LOG_fila.extend(dades)
        Finestra=[12,48,568,360]
        def verificar_canviar_la_mida():
            COLUMNA_VALOR,FILA_VALOR=(Finestra[2]-24)//8,(Finestra[3]-56)//16
            SMS=shell('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMNA_VALOR,FILA_VALOR) in SMS,SMS
            # real_dades Finestra 테두리: 단지 Mida cerca_VALOR 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            xec_píxel((Finestra[0],Finestra[1]),(32,80,144))
            dibuix_VALOR=xec_píxel((Finestra[0]+Finestra[2]-1,Finestra[1]+Finestra[3]-1),(39,49,64))
            return dibuix_VALOR
        def 모서리(방향):
            return (Finestra[0]+(3 if 방향 in (1,3) else Finestra[2]-4),Finestra[1]+(3 if 방향<=2 else Finestra[3]-4))
        def redimensionar_arrossegar(방향,차이,Botó=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            xec_píxel(흰점,(255,255,255))
            가리키기(가,세,Botó)
            끝가=max(0,min(너비-1,가+차이[0]));finalitzar_Vertical=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,finalitzar_Vertical,Botó);가리키기(끝가,finalitzar_Vertical,0);숨고르기()
            if Botó==1:
                ESQUERRA_VALOR,위,폭,durada_VALOR=Finestra;DRETA_VALOR,아래=ESQUERRA_VALOR+폭,위+durada_VALOR
                if 방향 in (1,3):ESQUERRA_VALOR=max(0,min(DRETA_VALOR-360,ESQUERRA_VALOR+끝가-가))
                else:DRETA_VALOR=max(ESQUERRA_VALOR+360,min(너비,DRETA_VALOR+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+finalitzar_Vertical-세))
                else:아래=max(위+216,min(높이,아래+finalitzar_Vertical-세))
                Finestra[:]=[ESQUERRA_VALOR,위,DRETA_VALOR-ESQUERRA_VALOR,아래-위]
        verificar_canviar_la_mida();assert punter_Amagat[0]
        redimensionar_arrossegar(4,(-100,-60),4);verificar_canviar_la_mida() # DRETA 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            redimensionar_arrossegar(방향,차이);verificar_canviar_la_mida()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        enviar_un_SMS("echo '"+긴글+"'");숨고르기()
        redimensionar_arrossegar(4,(-1000,-1000));assert Finestra[2:]==[360,216]
        redimensionar_arrossegar(4,(너비,높이))
        Executa_2=enviar_un_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Executa_2);verificar_canviar_la_mida()
        # vi가 Editar_VALOR 중에 화면 크기를 tornar_ho_a_provar_VALOR 읽고, 저장하지 않은 한글도 유지한다.
        shell('ftpd start')
        transferir_VALOR=ftplib.FTP();transferir_VALOR.encoding='utf-8';transferir_VALOR.connect('127.0.0.1',número_de_port,timeout=20);transferir_VALOR.login()
        기다리기(b'NORMAL',enviar_un_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',enviar_un_SMS('i미저장 한글 dades\n'));숨고르기()
        redimensionar_arrossegar(4,(-너비,-높이))
        # ANSI FILA_VALOR 이동에 새 FILA_VALOR 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Finestra[3]-56)//16)).encode() in LOG_fila[-4096:]
        enviar_un_SMS('작은 창에서도 이어 Escriptura\n');숨고르기()
        redimensionar_arrossegar(4,(너비,높이))
        enviar_un_SMS('큰 창에서도 이어 Escriptura\n');숨고르기()
        clic_botó(0xff1b);clic_botó(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',enviar_un_SMS(':wq\n'))
        contingut_VALOR=bytearray();transferir_VALOR.retrbinary('RETR 크기자료.txt',contingut_VALOR.extend)
        assert contingut_VALOR=='미저장 한글 dades\n작은 창에서도 이어 Escriptura\n큰 창에서도 이어 Escriptura\n'.encode(),contingut_VALOR
        verificar_canviar_la_mida().save(str(mesura_camí/(canviar_la_mida_SMS+'-large.png')))
        # 두 번째 창은 valor_per_defecte Mida, tornar_ho_a_provar_VALOR 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Executa_2=len(LOG_fila);clic_VALOR(70,16);기다리기(b'TERMINAL FOCUS 2',Executa_2)
        assert 'TERMINAL SIZE 68x19' in shell('terminal size')
        Executa_2=len(LOG_fila);clic_VALOR(180,16);기다리기(b'TERMINAL FOCUS 1',Executa_2);verificar_canviar_la_mida()
        redimensionar_arrossegar(4,(-너비,-높이));verificar_canviar_la_mida().save(str(mesura_camí/(canviar_la_mida_SMS+'-small.png')))
        # Mida canviar_VALOR ENRERE_VALOR X 닫기도 새로운 DRETA 가장자리를 사용한다.
        Executa_2=len(LOG_fila);clic_VALOR(Finestra[0]+Finestra[2]-20,Finestra[1]+15);기다리기(b'TERMINAL FOCUS 2',Executa_2)
        assert 'RESIZE CLOSED' in shell('echo RESIZE CLOSED')
        print('PASS:',canviar_la_mida_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if transferir_VALOR:transferir_VALOR.close()
        if remot_VALOR:remot_VALOR.close()
        if Procés_VALOR.poll() is None:
            Procés_VALOR.terminate()
            try:Procés_VALOR.wait(timeout=8)
            except subprocess.TimeoutExpired:Procés_VALOR.kill();Procés_VALOR.wait()
        선택기.close();Procés_VALOR.stdout.close();(mesura_camí/(canviar_la_mida_SMS+'.log')).write_bytes(LOG_fila)


def Executa_2():
    mesura_camí=Project_rel/'build/verification/resize';mesura_camí.mkdir(parents=True,exist_ok=True)
    LOG_fila={'passed':False,'kernel_sha256':hashlib.sha256((Project_rel/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,mesura_camí);LOG_fila['resolutions'].append([너비,높이])
        LOG_fila.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(mesura_camí/'report.json').write_text(json.dumps(LOG_fila,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Executa_2()
