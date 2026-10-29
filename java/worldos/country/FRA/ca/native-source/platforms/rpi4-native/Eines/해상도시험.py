#!/usr/bin/env python3
"""real_dades QEMU/VNC에서 화면 Mida·경계·Finestra moure_VALOR·Swing·언어별 그리기를 검사한다."""
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


def 해상도시험(너비, 높이, mesura_camí):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); número_de_port = 임시.getsockname()[1]
    canviar_la_mida_SMS = '{}x{}'.format(너비, 높이)
    Procés_VALOR = subprocess.Popen(['python3', str(Project_rel/'Eines/Executa_ordre.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(número_de_port), '--resolution', canviar_la_mida_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector(); 선택기.register(Procés_VALOR.stdout, selectors.EVENT_READ)
    LOG_fila = bytearray(); remot_VALOR = None; transferir_VALOR = None

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

    def shell(SMS): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', enviar_un_SMS(SMS+'; echo __RESOLUTION_DONE__\n'))

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
        remot_VALOR.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        xec_píxel((너비-1, 높이-1), (24, 32, 48))
        # 화면 DRETA 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        xec_píxel((너비-568, 높이-360), (32, 80, 144))
        Executa_2 = len(LOG_fila); clic_VALOR(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Executa_2)
        xec_píxel((너비-568, 높이-360), (24, 32, 48))
        Executa_2 = len(LOG_fila); clic_VALOR(80, 16); 기다리기(b'TERMINAL FOCUS 1', Executa_2)
        shell('ftpd start')
        transferir_VALOR = ftplib.FTP(); transferir_VALOR.encoding = 'utf-8'; transferir_VALOR.connect('127.0.0.1', número_de_port, timeout=20); transferir_VALOR.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALOR·clip 밖·빈 사각형을 포함한다.
        FONT = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(네모그리기(너비,높이,0,0,0)) return 2;
    if(네모그리기(너비,높이-1,1,1,0)!=-22) return 3;
    if(네모그리기(너비-1,높이,1,1,0)!=-22) return 4;
    if(네모그리기(-1,0,1,1,0)!=-22) return 5;
    if(네모그리기(0,0,-1,1,0)!=-22) return 6;
    if(네모그리기(너비-1,높이-1,1,1,0x332211)) return 7;
    escriure_arxiu_dades(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        pujar_Fitxers('화면시험.c', FONT.encode())
        assert 'exit 0' in shell('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', enviar_un_SMS('run /화면시험\n'))
        xec_píxel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', enviar_un_SMS('q'))
        FONT = '''from Català import 화면크기, 네모그리기, 그림기다리기, Sortida, sistema_error
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sistema_error as s_ha_produït_un_error:
    assert s_ha_produït_un_error.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
Sortida("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        pujar_Fitxers('화면시험.py', FONT.encode())
        기다리기(b'PYTHON RESOLUTION PASS', enviar_un_SMS('python /화면시험.py\n'))
        xec_píxel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', enviar_un_SMS('q'))
        FONT = '''import Català.propi.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Estat_excepció("Mida");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new Estat_excepció("clip"); }
        catch (invàlid_arg_excepció s_ha_produït_un_error) { }
        화면.esborrar_introducció(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # excepció 처리는 allotjar javac 결과를 propi JVM에 올려 검사한다.
        경계원문 = mesura_camí/'해상도경계시험.java'
        경계원문.write_text(FONT.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_rel/'dist/jkoros-native-korean.jar'), '-d', str(mesura_camí), str(경계원문)])
        pujar_Fitxers('해상도경계시험.class', (mesura_camí/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', enviar_un_SMS('java 해상도경계시험\n'))
        xec_píxel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', enviar_un_SMS('q'))
        # 게스트 javac의 suport_VALOR 문법으로 Mida cerca_VALOR·esborrar_introducció·다섯 인수 그리기를 컴파일한다.
        FONT = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=Català.propi.화면.너비();
        int 높이=Català.propi.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Català.propi.화면.esborrar_introducció(3153944);
        Català.propi.화면.사각형(너비-1,높이-1,1,1,10061943);
        Català.propi.Sortida.escriure_línia("JAVA RESOLUTION PASS");
        Català.propi.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        pujar_Fitxers('해상도시험.java', FONT.encode())
        RESULTAT = shell('javac 해상도시험.java'); assert 'exit 0' in RESULTAT, RESULTAT
        기다리기(b'JAVA RESOLUTION PASS', enviar_un_SMS('java 해상도시험\n'))
        xec_píxel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', enviar_un_SMS('q'))
        pujar_Fitxers('스윙시험.class', (mesura_camí/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', enviar_un_SMS('java 스윙시험\n'))
        가로, Vertical_càrrec = (너비-400)//2, (높이-280)//2
        dibuix_VALOR = xec_píxel((가로, Vertical_càrrec), (32, 80, 144))
        dibuix_VALOR.save(str(mesura_camí/(canviar_la_mida_SMS+'.png')))
        Executa_2 = len(LOG_fila); clic_VALOR(가로+80, Vertical_càrrec+155)
        기다리기('SWING CLICK Nom'.encode(), Executa_2)
        Executa_2 = len(LOG_fila); clic_VALOR(가로+385, Vertical_càrrec+15); 기다리기(b'jkoros-native> ', Executa_2)
        assert 'AFTER_RESOLUTION' in shell('echo AFTER_RESOLUTION')
        print('PASS:', canviar_la_mida_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if transferir_VALOR: transferir_VALOR.close()
        if remot_VALOR: remot_VALOR.close()
        if Procés_VALOR.poll() is None:
            Procés_VALOR.terminate()
            try: Procés_VALOR.wait(timeout=8)
            except subprocess.TimeoutExpired: Procés_VALOR.kill(); Procés_VALOR.wait()
        선택기.close(); Procés_VALOR.stdout.close()
        (mesura_camí/(canviar_la_mida_SMS+'.log')).write_bytes(LOG_fila)


def Executa_2():
    mesura_camí = Project_rel/'build/verification/resolution'; mesura_camí.mkdir(parents=True, exist_ok=True)
    LOG_fila = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_rel/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for invàlid_VALOR in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            RESULTAT = subprocess.run(['python3', str(Project_rel/'Eines/Executa_ordre.py'), '--resolution', invàlid_VALOR], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert RESULTAT.returncode == 2 and b'--resolution' in RESULTAT.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(mesura_camí), str(Project_rel/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, mesura_camí); LOG_fila['resolutions'].append([너비, 높이])
        LOG_fila.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (mesura_camí/'report.json').write_text(json.dumps(LOG_fila, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Executa_2()
