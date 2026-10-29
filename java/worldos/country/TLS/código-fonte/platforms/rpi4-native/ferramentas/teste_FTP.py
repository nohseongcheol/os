#!/usr/bin/env python3
"""Real host TCP client -> SLIP -> bare-metal lwIP -> FTP -> Java VFS."""
import ftplib
import hashlib
import io
import json
import selectors
import socket
import subprocess
import time
import zipfile
from ponte_3de4fe3a import ponte_3de4fe3a
from Executar_comando import ação_raiz, comando
from eco_acessório import eco_acessório
from 실행파일시험 import 리눅스예제


def iniciar():
    RC_dados = ação_raiz / 'build/verification/ftp'; RC_dados.mkdir(parents=True, exist_ok=True)
    validação_relatar = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((ação_raiz / 'build/kernel8.img').read_bytes()).hexdigest()}
    transcrição = bytearray()
    자바원문 = RC_dados / 'teste_grupo.java'
    자바원문.write_text('public class teste_grupo { public static void main(String[] argumentos) throws Exception { Português.nativo.saídaTexto.gravar_linha("JAR Executar_comando: " + argumentos[0]); Português.nativo.ficheiro.Escrita("jar.txt", "nativo kernel_VALOR ficheiro"); Português.nativo.saídaTexto.gravar_linha(Português.nativo.ficheiro.Leitura("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ação_raiz/'build/java-library/classes'), '-d', str(RC_dados), str(자바원문)])
    arquivo = io.BytesIO()
    with zipfile.ZipFile(arquivo, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: teste_grupo\r\n\r\n')
        자바꾸러미.write(str(RC_dados/'teste_grupo.class'), 'teste_grupo.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); número_da_porta = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); servidor_fluxo_porta = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); servidor_datagrama_porta = 임시자원.getsockname()[1]
    with ponte_3de4fe3a(número_da_porta, ['tcp:{}:9300'.format(servidor_fluxo_porta), 'udp:{}:9301'.format(servidor_datagrama_porta)], Captura=True) as ponte:
        Processo = subprocess.Popen(comando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ponte.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        seletor = selectors.DefaultSelector(); seletor.register(Processo.stdout, selectors.EVENT_READ)
        def receber_email(favorito=b'jkoros-native> ', execução_TEMPOLIMITE=60):
            dados = bytearray(); encerrar_DESLOC = time.monotonic() + execução_TEMPOLIMITE
            while favorito not in dados:
                if time.monotonic() > encerrar_DESLOC or Processo.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + dados.decode('utf-8', 'replace'))
                for 누름값, _ in seletor.select(.1):
                    fragmento_VALOR = 누름값.fileobj.read(4096)
                    if fragmento_VALOR: dados.extend(fragmento_VALOR); transcrição.extend(fragmento_VALOR)
                if b'PANIC:' in dados or b'FAIL ' in dados: raise AssertionError(dados)
            return dados.decode('utf-8', 'replace').replace('\r\n', '\n')
        def shell(linha_de_entrada):
            Processo.stdin.write(linha_de_entrada.encode() + b'\n'); Processo.stdin.flush(); return receber_email()
        try:
            receber_email(); assert 'FTP listening' in shell('ftpd start')
            transferência_de_arquivo_conexão = ftplib.FTP(); transferência_de_arquivo_conexão.encoding = 'utf-8'; transferência_de_arquivo_conexão.connect('127.0.0.1', número_da_porta, timeout=20); transferência_de_arquivo_conexão.login()
            carga_dados = bytes(range(256)) * 32
            transferência_de_arquivo_conexão.storbinary('STOR binary.dat', io.BytesIO(carga_dados))
            resultado = bytearray(); transferência_de_arquivo_conexão.retrbinary('RETR binary.dat', resultado.extend)
            assert resultado == carga_dados; assert transferência_de_arquivo_conexão.size('binary.dat') == len(carga_dados)
            validação_relatar['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            transferência_de_arquivo_conexão.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in shell('cat 한글.txt')
            assert '한글.txt' in transferência_de_arquivo_conexão.nlst()
            assert dict(transferência_de_arquivo_conexão.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            validação_relatar['checks'].append('UTF-8 filename and content visible in guest shell')
            try: transferência_de_arquivo_conexão.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            resultado = bytearray(); transferência_de_arquivo_conexão.retrbinary('RETR binary.dat', resultado.extend); assert resultado == carga_dados
            validação_relatar['checks'].append('oversized replacement rejected; previous file preserved')
            with transferência_de_arquivo_conexão.transfercmd('STOR pending.txt') as Upload_Arquivos:
                # A control command must not change the active upload's destination.
                assert transferência_de_arquivo_conexão.size('binary.dat') == len(carga_dados)
                Upload_Arquivos.sendall(b'UPLOAD TARGET PRESERVED')
            assert transferência_de_arquivo_conexão.voidresp().startswith('226')
            resultado = bytearray(); transferência_de_arquivo_conexão.retrbinary('RETR pending.txt', resultado.extend)
            assert resultado == b'UPLOAD TARGET PRESERVED'
            resultado = bytearray(); transferência_de_arquivo_conexão.retrbinary('RETR binary.dat', resultado.extend)
            assert resultado == carga_dados
            transferência_de_arquivo_conexão.delete('pending.txt')
            validação_relatar['checks'].append('interleaved SIZE cannot change the active STOR destination')
            transferência_de_arquivo_conexão.storbinary('STOR saudação_ae353e94.jar', io.BytesIO(arquivo.getvalue()))
            texto = shell('java -jar saudação_ae353e94.jar 누리')
            assert 'JAR Executar_comando: 누리' in texto and 'nativo kernel_VALOR ficheiro' in texto and 'exit 0' in texto, texto
            texto = shell('./saudação_ae353e94.jar 세상')
            assert 'JAR Executar_comando: 세상' in texto and 'exit 0' in texto, texto
            validação_relatar['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <Arquivo_ABI.h>\nstruct dados { int número; double 비율; };\nint SUM_VALOR(int n) { return n ? n + SUM_VALOR(n-1) : 0; }\nint main(void) { struct dados VALOR = {SUM_VALOR(10), 1.25}; if (VALOR.número != 55 || VALOR.비율 * 2 != 2.5) return 3; const char saudação_ae353e94[] = "CC NATIVE PASS\\n"; int 문서 = abrir_Arquivo("cc.txt", de_leitura_gravação | 없으면만들기 | cortar_Sumário, 0600); if (문서 < 0) return 1; gravar_Arquivo_dados(문서, saudação_ae353e94, sizeof(saudação_ae353e94)-1); Close_Arquivo(문서); gravar_Arquivo_dados(1, saudação_ae353e94, sizeof(saudação_ae353e94)-1); return 0; }\n'
            transferência_de_arquivo_conexão.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            texto = shell('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in texto and 'exit 0' in texto, texto
            texto = shell('run 한글.elf'); assert 'CC NATIVE PASS' in texto and 'exit 0' in texto, texto
            assert 'CC NATIVE PASS' in shell('cat cc.txt')
            executável = bytearray(); transferência_de_arquivo_conexão.retrbinary('RETR 한글.elf', executável.extend)
            assert executável[:4] == b'\x7fELF' and executável[18:20] == b'\xb7\x00'
            transferência_de_arquivo_conexão.storbinary('STOR copiar_VALOR.elf', io.BytesIO(executável)); texto = shell('run copiar_VALOR.elf'); assert 'CC NATIVE PASS' in texto and 'exit 0' in texto, texto
            transferência_de_arquivo_conexão.storbinary('STOR Executar_comando', io.BytesIO(executável)); texto=shell('./Executar_comando');assert 'CC NATIVE PASS' in texto and 'exit 0' in texto,texto
            transferência_de_arquivo_conexão.storbinary('STOR Nome.txt', io.BytesIO(executável)); texto=shell('./Nome.txt');assert 'CC NATIVE PASS' in texto and 'exit 0' in texto,texto
            shell('rm Executar_comando Nome.txt')
            validação_relatar['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            shell('rm binary.dat 한글.txt 한글.c 한글.elf copiar_VALOR.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(RC_dados/'linux-reference')
            transferência_de_arquivo_conexão.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            texto=shell('./리눅스인사');assert 'exit -8' in texto,texto
            texto=shell('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in texto,texto
            assert 'LINUX ELF FILE IO' in shell('cat linux.txt')
            transferência_de_arquivo_conexão.delete('리눅스인사');transferência_de_arquivo_conexão.delete('linux.txt')
            transferência_de_arquivo_conexão.storbinary('STOR FALSO_VALOR.elf',io.BytesIO(b'plain text'))
            assert '실행할 número 없습니다:' in shell('./FALSO_VALOR.elf');transferência_de_arquivo_conexão.delete('FALSO_VALOR.elf')
            validação_relatar['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with eco_acessório() as eco_servidor_entrada:
                NET_fonte = RC_dados/'externo_comunicação.java'
                NET_fonte.write_text('''import java.net.*; import java.io.*;
public class externo_comunicação { public static void main(String[] args) throws Exception {
 Socket Ligar = Português.nativo.conexão_transporte.Ligar("10.0.2.2", Integer.parseInt(args[0]));
 Ligar.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] códigoFonte = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<códigoFonte.length;i++) if (Ligar.getInputStream().read() != (códigoFonte[i]&255)) throw new RuntimeException("TCP mismatch");
 Ligar.close();
 DatagramSocket empresa = Português.nativo.comunicação.Abrir(0); Português.nativo.comunicação.TEMPOLIMITE(empresa, 500);
 Português.nativo.comunicação.enviar(empresa, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Português.nativo.comunicação.receber(empresa).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 empresa.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(ação_raiz/'build/java-library/classes'),'-d',str(RC_dados),str(NET_fonte)])
                transferência_de_arquivo_conexão.storbinary('STOR externo_comunicação.class', io.BytesIO((RC_dados/'externo_comunicação.class').read_bytes()))
                texto = shell('java externo_comunicação {} {}'.format(eco_servidor_entrada.porta_TCP, eco_servidor_entrada.UDP_porta))
                assert 'EXTERNAL TCP UDP PASS' in texto and '10.0.2.2' in texto and 'exit 0' in texto, texto
                assert eco_servidor_entrada.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, eco_servidor_entrada.수신됨
                assert not eco_servidor_entrada.오류들, eco_servidor_entrada.오류들
            validação_relatar['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            transferência_de_arquivo_conexão.delete('externo_comunicação.class')
            servidor_fonte=RC_dados/'servidor_teste.java'
            servidor_fonte.write_text('''import java.net.*; public class servidor_teste {
 public static void main(String[] args) throws Exception {
  ServerSocket servidor_VALOR = new ServerSocket(9300); DatagramSocket empresa = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket convidado_VALOR = servidor_VALOR.accept();
  convidado_VALOR.getOutputStream().write(convidado_VALOR.getInputStream().read()+1); convidado_VALOR.close(); servidor_VALOR.close();
  byte[] Conteúdo_VALOR = new byte[8]; DatagramPacket datagrama = new DatagramPacket(Conteúdo_VALOR, Conteúdo_VALOR.length); empresa.receive(datagrama);
  empresa.send(datagrama); empresa.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(RC_dados),str(servidor_fonte)])
            transferência_de_arquivo_conexão.storbinary('STOR servidor_teste.class',io.BytesIO((RC_dados/'servidor_teste.class').read_bytes()))
            Processo.stdin.write('java servidor_teste\n'.encode());Processo.stdin.flush();receber_email(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',servidor_fluxo_porta),timeout=5) as par_VALOR:
                par_VALOR.sendall(b'A');assert par_VALOR.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as par_VALOR:
                par_VALOR.settimeout(5);par_VALOR.sendto(b'UDP-IN',('127.0.0.1',servidor_datagrama_porta));assert par_VALOR.recvfrom(512)[0]==b'UDP-IN'
            texto=receber_email();assert 'INBOUND TCP UDP PASS' in texto and 'exit 0' in texto,texto
            validação_relatar['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            transferência_de_arquivo_conexão.delete('servidor_teste.class')
            instrução_SEQUÊNCIA = 'public class 빛 { public static void main(String[] argumentos) throws Exception { int SUM_VALOR = 0; int número = 1; while (número <= 10) { SUM_VALOR = SUM_VALOR + número; número = número + 1; } Português.nativo.saídaTexto.gravar_número(SUM_VALOR); Português.nativo.ficheiro.Escrita("aot.txt", "한글 AOT ficheiro 😀"); Português.nativo.saídaTexto.gravar_linha(Português.nativo.ficheiro.Leitura("aot.txt")); } }'
            transferência_de_arquivo_conexão.storbinary('STOR 빛.java', io.BytesIO(instrução_SEQUÊNCIA.encode()))
            texto = shell('javac 빛.java'); assert 'exit 0' in texto and 'Compiled:' in texto, texto
            texto = shell('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in texto and 'exit 0' in texto, texto
            texto = shell('run 빛.elf'); assert '\n55\n' in texto and '한글 AOT ficheiro 😀' in texto and 'exit 0' in texto, texto
            nativo_fd019377 = bytearray(); transferência_de_arquivo_conexão.retrbinary('RETR 빛.elf', nativo_fd019377.extend)
            texto = shell('jaot saudação_ae353e94.jar -o 빛.elf'); assert 'exit 1' in texto and 'unsupported' in texto, texto
            보존자료 = bytearray(); transferência_de_arquivo_conexão.retrbinary('RETR 빛.elf', 보존자료.extend); assert nativo_fd019377 == 보존자료
            바이트코드 = bytearray(); transferência_de_arquivo_conexão.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            transferência_de_arquivo_conexão.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            texto = shell('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in texto and 'exit 0' in texto, texto
            texto = shell('run 빛.elf'); assert '\n55\n' in texto and '한글 AOT ficheiro 😀' in texto and 'exit 0' in texto, texto
            validação_relatar['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            validação_relatar['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            estático_fonte=RC_dados/'estático_teste.java'
            estático_fonte.write_text('''public class estático_teste {
 static int ação_raiz = 3;
 static int SUM_VALOR(int n) { return n == 0 ? 0 : n + SUM_VALOR(n-1); }
 public static void main(String[] argumentos) {
  int[] VALOR = new int[] {ação_raiz, SUM_VALOR(10)};
  System.out.println(VALOR[0] + VALOR[1]); System.out.println(argumentos[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(RC_dados),str(estático_fonte)])
            transferência_de_arquivo_conexão.storbinary('STOR estático_teste.class',io.BytesIO((RC_dados/'estático_teste.class').read_bytes()))
            texto=shell('jaot estático_teste.class -o estático_teste.elf');assert 'exit 0' in texto,texto
            texto=shell('run estático_teste.elf 한글인수');assert '\n58\n한글인수\nexit 0' in texto,texto
            transferência_de_arquivo_conexão.delete('estático_teste.class');transferência_de_arquivo_conexão.delete('estático_teste.elf')
            validação_relatar['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(arquivo.getvalue());손상자료[14]^=1
            transferência_de_arquivo_conexão.storbinary('STOR saudação_ae353e94.jar',io.BytesIO(손상자료))
            texto=shell('java -jar saudação_ae353e94.jar');assert 'Main-Class\nexit 1' in texto,texto
            validação_relatar['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            transferência_de_arquivo_conexão.quit(); assert 'FTP stopped' in shell('ftpd stop')
            assert not ponte.erro, ponte.erro
            validação_relatar.update(passed=True, frames_to_guest=ponte.커널수신틀수, frames_from_guest=ponte.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in seletor.select(0):
                fragmento_VALOR=누름값.fileobj.read(65536)
                if fragmento_VALOR: transcrição.extend(fragmento_VALOR)
            ponte.Pausar_Evento.set()
            Processo.terminate()
            try: Processo.wait(timeout=5)
            except subprocess.TimeoutExpired: Processo.kill(); Processo.wait()
            seletor.close(); Processo.stdin.close(); Processo.stdout.close()
            validação_relatar['bridge_error'] = ponte.erro
            validação_relatar['frames_to_guest'] = ponte.커널수신틀수; validação_relatar['frames_from_guest'] = ponte.커널발신틀수
            (RC_dados/'packets.json').write_text(json.dumps(ponte.log_de_rastreamento,indent=2)+'\n')
            (RC_dados / 'serial.log').write_bytes(transcrição)
            (RC_dados / 'report.json').write_text(json.dumps(validação_relatar, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': iniciar()
