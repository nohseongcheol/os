#!/usr/bin/env python3
"""real_datos QEMU/VNC에서 화면 Tamaño·경계·Xanela mover_VALOR·Swing·언어별 그리기를 검사한다."""
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


def 해상도시험(너비, 높이, medida_camiño):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); número_do_porto = 임시.getsockname()[1]
    크기글 = '{}x{}'.format(너비, 높이)
    Proceso_VALOR = subprocess.Popen(['python3', str(Project_raíz/'Ferramentas/executar_comando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(número_do_porto), '--resolution', 크기글], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector(); 선택기.register(Proceso_VALOR.stdout, selectors.EVENT_READ)
    LOG_fila = bytearray(); remoto_VALOR = None; Transferir_VALOR = None

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

    def shell(Texto): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', enviar_SMS(Texto+'; echo __RESOLUTION_DONE__\n'))

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
        remoto_VALOR.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        cheque_píxel((너비-1, 높이-1), (24, 32, 48))
        # 화면 DEREITA 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        cheque_píxel((너비-568, 높이-360), (32, 80, 144))
        Executar_2 = len(LOG_fila); clic_VALOR(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Executar_2)
        cheque_píxel((너비-568, 높이-360), (24, 32, 48))
        Executar_2 = len(LOG_fila); clic_VALOR(80, 16); 기다리기(b'TERMINAL FOCUS 1', Executar_2)
        shell('ftpd start')
        Transferir_VALOR = ftplib.FTP(); Transferir_VALOR.encoding = 'utf-8'; Transferir_VALOR.connect('127.0.0.1', número_do_porto, timeout=20); Transferir_VALOR.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERTER_VALOR·clip 밖·빈 사각형을 포함한다.
        FONTE = '''#include <화면규약.h>
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
    escribir_Ficheiro_datos(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        carga_Ficheiros('화면시험.c', FONTE.encode())
        assert 'exit 0' in shell('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', enviar_SMS('run /화면시험\n'))
        cheque_píxel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', enviar_SMS('q'))
        FONTE = '''from Galego import 화면크기, 네모그리기, 그림기다리기, Saída, sistema_erro
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sistema_erro as ERRO:
    assert ERRO.ÍNDICE == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
Saída("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        carga_Ficheiros('화면시험.py', FONTE.encode())
        기다리기(b'PYTHON RESOLUTION PASS', enviar_SMS('python /화면시험.py\n'))
        cheque_píxel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', enviar_SMS('q'))
        FONTE = '''import Galego.자체.*;
public class 해상도시험 {
    public static void main(String[] Argumentos) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Estado_excepción("Tamaño");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new Estado_excepción("clip"); }
        catch (non_válido_argumento_excepción ERRO) { }
        화면.borrar_introdución(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # excepción 처리는 hospedar javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = medida_camiño/'해상도경계시험.java'
        경계원문.write_text(FONTE.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_raíz/'dist/jkoros-native-korean.jar'), '-d', str(medida_camiño), str(경계원문)])
        carga_Ficheiros('해상도경계시험.class', (medida_camiño/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', enviar_SMS('java 해상도경계시험\n'))
        cheque_píxel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', enviar_SMS('q'))
        # 게스트 javac의 soporte_VALOR 문법으로 Tamaño consulta_VALOR·borrar_introdución·다섯 Argumentos 그리기를 컴파일한다.
        FONTE = '''public class 해상도시험 {
    public static void main(String[] Argumentos) {
        int 너비=Galego.자체.화면.너비();
        int 높이=Galego.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Galego.자체.화면.borrar_introdución(3153944);
        Galego.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        Galego.자체.Saída.escribir_liña("JAVA RESOLUTION PASS");
        Galego.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        carga_Ficheiros('해상도시험.java', FONTE.encode())
        RESULTANTE = shell('javac 해상도시험.java'); assert 'exit 0' in RESULTANTE, RESULTANTE
        기다리기(b'JAVA RESOLUTION PASS', enviar_SMS('java 해상도시험\n'))
        cheque_píxel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', enviar_SMS('q'))
        carga_Ficheiros('스윙시험.class', (medida_camiño/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', enviar_SMS('java 스윙시험\n'))
        가로, Vertical_cargo = (너비-400)//2, (높이-280)//2
        그림 = cheque_píxel((가로, Vertical_cargo), (32, 80, 144))
        그림.save(str(medida_camiño/(크기글+'.png')))
        Executar_2 = len(LOG_fila); clic_VALOR(가로+80, Vertical_cargo+155)
        기다리기('SWING CLICK Nome'.encode(), Executar_2)
        Executar_2 = len(LOG_fila); clic_VALOR(가로+385, Vertical_cargo+15); 기다리기(b'jkoros-native> ', Executar_2)
        assert 'AFTER_RESOLUTION' in shell('echo AFTER_RESOLUTION')
        print('PASS:', 크기글, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if Transferir_VALOR: Transferir_VALOR.close()
        if remoto_VALOR: remoto_VALOR.close()
        if Proceso_VALOR.poll() is None:
            Proceso_VALOR.terminate()
            try: Proceso_VALOR.wait(timeout=8)
            except subprocess.TimeoutExpired: Proceso_VALOR.kill(); Proceso_VALOR.wait()
        선택기.close(); Proceso_VALOR.stdout.close()
        (medida_camiño/(크기글+'.log')).write_bytes(LOG_fila)


def Executar_2():
    medida_camiño = Project_raíz/'build/verification/resolution'; medida_camiño.mkdir(parents=True, exist_ok=True)
    LOG_fila = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_raíz/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for non_válido_VALOR in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            RESULTANTE = subprocess.run(['python3', str(Project_raíz/'Ferramentas/executar_comando.py'), '--resolution', non_válido_VALOR], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert RESULTANTE.returncode == 2 and b'--resolution' in RESULTANTE.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(medida_camiño), str(Project_raíz/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, medida_camiño); LOG_fila['resolutions'].append([너비, 높이])
        LOG_fila.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (medida_camiño/'report.json').write_text(json.dumps(LOG_fila, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Executar_2()
