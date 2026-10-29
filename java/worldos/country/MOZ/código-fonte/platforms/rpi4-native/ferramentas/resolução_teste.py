#!/usr/bin/env python3
"""real_dados QEMU/VNC에서 tela Tamanho·limite_VALOR·Janela mover_VALOR·Swing·언어별 그리기를 검사한다."""
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


def resolução_teste(너비, altura_VALOR, RC_caminho):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); número_da_porta = 임시.getsockname()[1]
    dimensionar_SMS = '{}x{}'.format(너비, altura_VALOR)
    Processo_VALOR = subprocess.Popen(['python3', str(ação_raiz/'ferramentas/Executar_comando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(número_da_porta), '--resolution', dimensionar_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    seletor_a916db4e = selectors.DefaultSelector(); seletor_a916db4e.register(Processo_VALOR.stdout, selectors.EVENT_READ)
    LOG_linha = bytearray(); remoto_VALOR = None; Transferir_VALOR = None

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

    def shell(texto): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', enviar_SMS(texto+'; echo __RESOLUTION_DONE__\n'))

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
        remoto_VALOR.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        cheque_pixel((너비-1, altura_VALOR-1), (24, 32, 48))
        # tela DIREITA 아래까지 이동한다. Anterior_item 640×480 limite_VALOR 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, altura_VALOR-360+12, 1); 가리키기(너비-568+28, altura_VALOR-360+12, 0)
        cheque_pixel((너비-568, altura_VALOR-360), (32, 80, 144))
        iniciar = len(LOG_linha); clicar_VALOR(너비-20, altura_VALOR-345); 기다리기(b'TERMINAL FOCUS 1', iniciar)
        cheque_pixel((너비-568, altura_VALOR-360), (24, 32, 48))
        iniciar = len(LOG_linha); clicar_VALOR(80, 16); 기다리기(b'TERMINAL FOCUS 1', iniciar)
        shell('ftpd start')
        Transferir_VALOR = ftplib.FTP(); Transferir_VALOR.encoding = 'utf-8'; Transferir_VALOR.connect('127.0.0.1', número_da_porta, timeout=20); Transferir_VALOR.login()
        # C limite_VALOR 검사는 32비트 unsigned negativo_VALOR CONVERTER_VALOR·recortar 밖·빈 사각형을 포함한다.
        códigoFonte = '''#include <tela_ABI.h>
#include <Arquivo_ABI.h>
int main(void) {
    unsigned 너비=화면너비(), altura_VALOR=tela_altura();
    if(너비!=WIDTH || altura_VALOR!=HEIGHT) return 1;
    if(emitir_retângulo(너비,altura_VALOR,0,0,0)) return 2;
    if(emitir_retângulo(너비,altura_VALOR-1,1,1,0)!=-22) return 3;
    if(emitir_retângulo(너비-1,altura_VALOR,1,1,0)!=-22) return 4;
    if(emitir_retângulo(-1,0,1,1,0)!=-22) return 5;
    if(emitir_retângulo(0,0,-1,1,0)!=-22) return 6;
    if(emitir_retângulo(너비-1,altura_VALOR-1,1,1,0x332211)) return 7;
    gravar_Arquivo_dados(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(altura_VALOR))
        Upload_Arquivos('teste_tela.c', códigoFonte.encode())
        assert 'exit 0' in shell('cc /teste_tela.c -o /teste_tela')
        기다리기(b'C RESOLUTION PASS', enviar_SMS('run /teste_tela\n'))
        cheque_pixel((너비-1, altura_VALOR-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', enviar_SMS('q'))
        códigoFonte = '''from Português import tela_dimensionar, emitir_retângulo, 그림기다리기, saídaTexto, erro_do_sistema
너비, altura_VALOR = tela_dimensionar()
assert (너비, altura_VALOR) == (WIDTH, HEIGHT)
try:
    emitir_retângulo(너비, altura_VALOR-1, 1, 1, 0)
    raise AssertionError("boundary")
except erro_do_sistema as erro:
    assert erro.ÍNDICE == 22
emitir_retângulo(너비-1, altura_VALOR-1, 1, 1, 0x665544)
saídaTexto("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(altura_VALOR))
        Upload_Arquivos('teste_tela.py', códigoFonte.encode())
        기다리기(b'PYTHON RESOLUTION PASS', enviar_SMS('python /teste_tela.py\n'))
        cheque_pixel((너비-1, altura_VALOR-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', enviar_SMS('q'))
        códigoFonte = '''import Português.nativo.*;
public class resolução_teste {
    public static void main(String[] argumentos) {
        int 너비=tela.너비(), altura_VALOR=tela.altura_VALOR();
        if (너비!=WIDTH || altura_VALOR!=HEIGHT) throw new Estado_exceção("Tamanho");
        try { tela.retângulo(너비,altura_VALOR-1,1,1,0); throw new Estado_exceção("recortar"); }
        catch (inválido_argumento_exceção erro) { }
        tela.apagar_entrada(0x302018);
        tela.retângulo(너비-1,altura_VALOR-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        tela.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(altura_VALOR))
        # exceção 처리는 host javac 결과를 nativo JVM에 올려 검사한다.
        limite_fonte = RC_caminho/'해상도경계시험.java'
        limite_fonte.write_text(códigoFonte.replace('class resolução_teste', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ação_raiz/'dist/jkoros-native-korean.jar'), '-d', str(RC_caminho), str(limite_fonte)])
        Upload_Arquivos('해상도경계시험.class', (RC_caminho/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', enviar_SMS('java 해상도경계시험\n'))
        cheque_pixel((너비-1, altura_VALOR-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', enviar_SMS('q'))
        # 게스트 javac의 Suporte_VALOR 문법으로 Tamanho consulta_VALOR·apagar_entrada·다섯 argumentos 그리기를 컴파일한다.
        códigoFonte = '''public class resolução_teste {
    public static void main(String[] argumentos) {
        int 너비=Português.nativo.tela.너비();
        int altura_VALOR=Português.nativo.tela.altura_VALOR();
        if (너비!=WIDTH || altura_VALOR!=HEIGHT) return;
        Português.nativo.tela.apagar_entrada(3153944);
        Português.nativo.tela.retângulo(너비-1,altura_VALOR-1,1,1,10061943);
        Português.nativo.saídaTexto.gravar_linha("JAVA RESOLUTION PASS");
        Português.nativo.tela.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(altura_VALOR))
        Upload_Arquivos('resolução_teste.java', códigoFonte.encode())
        resultado = shell('javac resolução_teste.java'); assert 'exit 0' in resultado, resultado
        기다리기(b'JAVA RESOLUTION PASS', enviar_SMS('java resolução_teste\n'))
        cheque_pixel((너비-1, altura_VALOR-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', enviar_SMS('q'))
        Upload_Arquivos('Swing_teste.class', (RC_caminho/'Swing_teste.class').read_bytes())
        기다리기(b'SWING READY', enviar_SMS('java Swing_teste\n'))
        가로, Vertical_cargo = (너비-400)//2, (altura_VALOR-280)//2
        desenho_VALOR = cheque_pixel((가로, Vertical_cargo), (32, 80, 144))
        desenho_VALOR.save(str(RC_caminho/(dimensionar_SMS+'.png')))
        iniciar = len(LOG_linha); clicar_VALOR(가로+80, Vertical_cargo+155)
        기다리기('SWING CLICK Nome'.encode(), iniciar)
        iniciar = len(LOG_linha); clicar_VALOR(가로+385, Vertical_cargo+15); 기다리기(b'jkoros-native> ', iniciar)
        assert 'AFTER_RESOLUTION' in shell('echo AFTER_RESOLUTION')
        print('PASS:', dimensionar_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if Transferir_VALOR: Transferir_VALOR.close()
        if remoto_VALOR: remoto_VALOR.close()
        if Processo_VALOR.poll() is None:
            Processo_VALOR.terminate()
            try: Processo_VALOR.wait(timeout=8)
            except subprocess.TimeoutExpired: Processo_VALOR.kill(); Processo_VALOR.wait()
        seletor_a916db4e.close(); Processo_VALOR.stdout.close()
        (RC_caminho/(dimensionar_SMS+'.log')).write_bytes(LOG_linha)


def iniciar():
    RC_caminho = ação_raiz/'build/verification/resolution'; RC_caminho.mkdir(parents=True, exist_ok=True)
    LOG_linha = {'passed': False, 'kernel_sha256': hashlib.sha256((ação_raiz/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for inválido_VALOR in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            resultado = subprocess.run(['python3', str(ação_raiz/'ferramentas/Executar_comando.py'), '--resolution', inválido_VALOR], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert resultado.returncode == 2 and b'--resolution' in resultado.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(RC_caminho), str(ação_raiz/'testes/자바/Swing_teste.java')])
        for 너비, altura_VALOR in ((1920,1080), (1280,720), (640,480)):
            resolução_teste(너비, altura_VALOR, RC_caminho); LOG_linha['resolutions'].append([너비, altura_VALOR])
        LOG_linha.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (RC_caminho/'report.json').write_text(json.dumps(LOG_linha, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': iniciar()
