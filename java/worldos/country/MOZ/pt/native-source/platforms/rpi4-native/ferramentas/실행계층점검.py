#!/usr/bin/env python3
"""QEMU의 real_dados CPU Permissão_VALOR, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
import ftplib
import hashlib
import io
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time

from Executar_comando import ação_raiz, comando
from ponte_3de4fe3a import ponte_3de4fe3a
from eco_acessório import eco_acessório


def iniciar():
    saídaTexto = ação_raiz / 'build/verification/execution-network-review'
    saídaTexto.mkdir(parents=True, exist_ok=True)
    relatar_VALOR = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((ação_raiz / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    fonte_Arquivos = {
        'permissão_cheque': '''public class permissão_cheque {
 public static void main(String[] argumentos) {
  System.out.println("EL0_PROBE_READY");
  int número = 0; while (true) { número++; }
 }
}''',
        'rede_cheque': '''import java.net.*;
public class rede_cheque {
 public static void main(String[] argumentos) throws Exception {
  Socket Ligar = new Socket("10.0.2.2", Integer.parseInt(argumentos[0]));
  Ligar.setSoTimeout(3000);
  byte[] texto = "TCP 한글\\n".getBytes("UTF-8");
  Ligar.getOutputStream().write(texto);
  for (int cargo_ÍNDICE = 0; cargo_ÍNDICE < texto.length; cargo_ÍNDICE++)
   if (Ligar.getInputStream().read() != (texto[cargo_ÍNDICE] & 255)) throw new RuntimeException("TCP mismatch");
  Ligar.close();
  DatagramSocket empresa = new DatagramSocket(); empresa.setSoTimeout(3000);
  texto = "UDP 한글".getBytes("UTF-8");
  empresa.send(new DatagramPacket(texto, texto.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(argumentos[1])));
  byte[] resposta = new byte[64]; DatagramPacket datagrama = new DatagramPacket(resposta, resposta.length);
  empresa.receive(datagrama);
  if (datagrama.getLength() != texto.length) throw new RuntimeException("UDP length");
  for (int cargo_ÍNDICE = 0; cargo_ÍNDICE < texto.length; cargo_ÍNDICE++)
   if (resposta[cargo_ÍNDICE] != texto[cargo_ÍNDICE]) throw new RuntimeException("UDP mismatch");
  empresa.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'receber_cheque': '''import java.net.*;
public class receber_cheque {
 public static void main(String[] argumentos) throws Exception {
  ServerSocket servidor_VALOR = new ServerSocket(9300); servidor_VALOR.setSoTimeout(5000);
  DatagramSocket empresa = new DatagramSocket(9301); empresa.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Ligar = servidor_VALOR.accept(); Ligar.setSoTimeout(5000);
  Ligar.getOutputStream().write(Ligar.getInputStream().read() + 1);
  Ligar.close(); servidor_VALOR.close();
  byte[] dados = new byte[64]; DatagramPacket datagrama = new DatagramPacket(dados, dados.length);
  empresa.receive(datagrama); empresa.send(datagrama); empresa.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Nome, códigoFonte in fonte_Arquivos.items():
        (saídaTexto / (Nome + '.java')).write_text(códigoFonte, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(saídaTexto)] +
                          [str(saídaTexto / (Nome + '.java')) for Nome in fonte_Arquivos])
    LOG_linha = bytearray()
    def vazio_número_da_porta(TIPO_área=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TIPO_área) as busca_VALOR:
            busca_VALOR.bind(('127.0.0.4', 0))
            return busca_VALOR.getsockname()[1]
    porta_de_arquivo_número, porta_TCP, UDP_porta = vazio_número_da_porta(), vazio_número_da_porta(), vazio_número_da_porta(socket.SOCK_DGRAM)
    Processo_VALOR = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, ponte_3de4fe3a(
                porta_de_arquivo_número, ['tcp:{}:9300'.format(porta_TCP), 'udp:{}:9301'.format(UDP_porta)],
                Captura=True, ID_do_host='127.0.0.4') as ponte_VALOR:
            visual_caminho = Path(임시) / 'qmp.sock'
            Processo_VALOR = subprocess.Popen(comando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(visual_caminho)] + ponte_VALOR.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ESCOLHER_item = selectors.DefaultSelector()
            ESCOLHER_item.register(Processo_VALOR.stdout, selectors.EVENT_READ)
            def receber(mostrar_VALOR=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while mostrar_VALOR not in LOG_linha[처음:]:
                    if time.monotonic() > 끝 or Processo_VALOR.poll() is not None:
                        raise AssertionError('Missing ' + repr(mostrar_VALOR) + '\n' + LOG_linha[처음:].decode('utf-8', 'replace'))
                    for Chave_VALOR, _ in ESCOLHER_item.select(.05):
                        fragmento_VALOR = Chave_VALOR.fileobj.read(65536)
                        if fragmento_VALOR:
                            LOG_linha.extend(fragmento_VALOR)
                return LOG_linha[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def enviar(dados):
                Processo_VALOR.stdin.write(dados)
                Processo_VALOR.stdin.flush()
            def shell(texto):
                print(texto, flush=True)
                처음 = len(LOG_linha)
                enviar((texto + '\n').encode())
                return receber(처음=처음)
            receber()
            with socket.socket(socket.AF_UNIX) as visual_VALOR:
                visual_VALOR.settimeout(10)
                visual_VALOR.connect(str(visual_caminho))
                fluxo_VALOR = visual_VALOR.makefile('rwb')
                json.loads(fluxo_VALOR.readline())
                def solicitação(instrução_VALOR_4c26ea1b, argumentos=None):
                    dados = {'execute': instrução_VALOR_4c26ea1b}
                    if argumentos is not None:
                        dados['arguments'] = argumentos
                    fluxo_VALOR.write((json.dumps(dados) + '\n').encode())
                    fluxo_VALOR.flush()
                    while True:
                        resposta = json.loads(fluxo_VALOR.readline())
                        if 'error' in resposta:
                            raise AssertionError(resposta)
                        if 'return' in resposta:
                            return resposta['return']
                solicitação('qmp_capabilities')
                def permissão_de_leitura():
                    solicitação('stop')
                    try:
                        return solicitação('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        solicitação('cont')
                relatar_VALOR['shell_cpu'] = permissão_de_leitura()
                assert 'EL1h' in relatar_VALOR['shell_cpu'], relatar_VALOR['shell_cpu']
                relatar_VALOR['initial_ps'] = shell('ps')
                assert 'kernel/shell' in relatar_VALOR['initial_ps']
                relatar_VALOR['ipconfig'] = shell('ipconfig')
                assert 'inet 10.0.2.15' in relatar_VALOR['ipconfig']
                relatar_VALOR['gateway_ping'] = shell('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in relatar_VALOR['gateway_ping']
                assert 'FTP listening' in shell('ftpd start')
                with ftplib.FTP() as Transferir_VALOR:
                    Transferir_VALOR.encoding = 'utf-8'
                    Transferir_VALOR.connect('127.0.0.4', porta_de_arquivo_número, timeout=20)
                    Transferir_VALOR.login()
                    for Nome in fonte_Arquivos:
                        Transferir_VALOR.storbinary('STOR ' + Nome + '.class', io.BytesIO((saídaTexto / (Nome + '.class')).read_bytes()))
                처음 = len(LOG_linha)
                enviar('java permissão_cheque\n'.encode())
                receber(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    relatar_VALOR['java_cpu'] = permissão_de_leitura()
                    if 'EL0t' in relatar_VALOR['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in relatar_VALOR['java_cpu'], relatar_VALOR['java_cpu']
                receber(처음=처음)
                relatar_VALOR['after_exit_ps'] = shell('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', relatar_VALOR['after_exit_ps'])
                relatar_VALOR['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with eco_acessório() as par_VALOR:
                    texto = shell('java rede_cheque {} {}'.format(par_VALOR.porta_TCP, par_VALOR.UDP_porta))
                    assert 'OUTBOUND_TCP_UDP_PASS' in texto and 'exit 0' in texto, texto
                    assert par_VALOR.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, par_VALOR.수신됨
                    assert not par_VALOR.오류들, par_VALOR.오류들
                    relatar_VALOR['outbound_peers'] = {Tipo_VALOR: dados.decode() for Tipo_VALOR, dados in par_VALOR.수신됨.items()}
                처음 = len(LOG_linha)
                enviar('java receber_cheque\n'.encode())
                receber(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', porta_TCP), timeout=5) as par_VALOR:
                    par_VALOR.sendall(b'A')
                    assert par_VALOR.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as par_VALOR:
                    par_VALOR.settimeout(5)
                    par_VALOR.sendto(b'UDP-IN', ('127.0.0.4', UDP_porta))
                    assert par_VALOR.recvfrom(64)[0] == b'UDP-IN'
                texto = receber(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in texto and 'exit 0' in texto, texto
                relatar_VALOR['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in shell('terminal')
                shell('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_linha)
                enviar('java ExemploJanela\n'.encode())
                receber('GUI 예제 Preparar: ExemploJanela\r\n'.encode(), 처음)
                처음 = len(LOG_linha)
                enviar(bytes([30, 2, 1, 0, 0, 0, 0]))
                receber(처음=처음)
                relatar_VALOR['suspended_java_ps'] = shell('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java ExemploJanela', relatar_VALOR['suspended_java_ps']), relatar_VALOR['suspended_java_ps']
                relatar_VALOR['top'] = shell('top -n 1')
                assert 'java ExemploJanela' in relatar_VALOR['top'] and 'kernel/shell' in relatar_VALOR['top']
                relatar_VALOR['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                relatar_VALOR['network_trace'] = ponte_VALOR.log_de_rastreamento
                assert not ponte_VALOR.erro, ponte_VALOR.erro
                enviar(b'poweroff\n')
                assert Processo_VALOR.wait(timeout=15) == 0
                relatar_VALOR['passed'] = True
            ESCOLHER_item.close()
    except Exception as erro:
        relatar_VALOR['error'] = str(erro)
        raise
    finally:
        if Processo_VALOR is not None and Processo_VALOR.poll() is None:
            Processo_VALOR.terminate()
            try:
                Processo_VALOR.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Processo_VALOR.kill()
                Processo_VALOR.wait()
        (saídaTexto / 'serial.log').write_bytes(LOG_linha)
        (saídaTexto / 'report.json').write_text(json.dumps(relatar_VALOR, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Chave_VALOR: relatar_VALOR[Chave_VALOR] for Chave_VALOR in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    iniciar()
