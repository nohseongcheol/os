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
from Rede_ponte import Rede_ponte
from executar_comando import Project_raíz, Orde
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Executar_2():
    medida_datos = Project_raíz / 'build/verification/ftp'; medida_datos.mkdir(parents=True, exist_ok=True)
    validación_informe = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Project_raíz / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = medida_datos / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Argumentos) throws Exception { Galego.자체.Saída.escribir_liña("JAR executar_comando: " + Argumentos[0]); Galego.자체.Ficheiro.Escritura("jar.txt", "자체 kernel_VALOR Ficheiro"); Galego.자체.Saída.escribir_liña(Galego.자체.Ficheiro.Lectura("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_raíz/'build/java-library/classes'), '-d', str(medida_datos), str(자바원문)])
    Arquivo = io.BytesIO()
    with zipfile.ZipFile(Arquivo, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(medida_datos/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); número_do_porto = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); servidor_fluxo_porto = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Rede_ponte(número_do_porto, ['tcp:{}:9300'.format(servidor_fluxo_porto), 'udp:{}:9301'.format(서버전문접속번호)], capturar=True) as ponte:
        Proceso = subprocess.Popen(Orde() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ponte.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        준비선택기 = selectors.DefaultSelector(); 준비선택기.register(Proceso.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            datos = bytearray(); finalizar_DESPRAZAMENTO = time.monotonic() + 시간제한
            while 확인표시 not in datos:
                if time.monotonic() > finalizar_DESPRAZAMENTO or Proceso.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + datos.decode('utf-8', 'replace'))
                for 누름값, _ in 준비선택기.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: datos.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in datos or b'FAIL ' in datos: raise AssertionError(datos)
            return datos.decode('utf-8', 'replace').replace('\r\n', '\n')
        def shell(Liña):
            Proceso.stdin.write(Liña.encode() + b'\n'); Proceso.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in shell('ftpd start')
            transferencia_de_ficheiros_conexión = ftplib.FTP(); transferencia_de_ficheiros_conexión.encoding = 'utf-8'; transferencia_de_ficheiros_conexión.connect('127.0.0.1', número_do_porto, timeout=20); transferencia_de_ficheiros_conexión.login()
            carga_datos_60367a51 = bytes(range(256)) * 32
            transferencia_de_ficheiros_conexión.storbinary('STOR binary.dat', io.BytesIO(carga_datos_60367a51))
            RESULTANTE = bytearray(); transferencia_de_ficheiros_conexión.retrbinary('RETR binary.dat', RESULTANTE.extend)
            assert RESULTANTE == carga_datos_60367a51; assert transferencia_de_ficheiros_conexión.size('binary.dat') == len(carga_datos_60367a51)
            validación_informe['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            transferencia_de_ficheiros_conexión.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in shell('cat 한글.txt')
            assert '한글.txt' in transferencia_de_ficheiros_conexión.nlst()
            assert dict(transferencia_de_ficheiros_conexión.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            validación_informe['checks'].append('UTF-8 filename and content visible in guest shell')
            try: transferencia_de_ficheiros_conexión.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            RESULTANTE = bytearray(); transferencia_de_ficheiros_conexión.retrbinary('RETR binary.dat', RESULTANTE.extend); assert RESULTANTE == carga_datos_60367a51
            validación_informe['checks'].append('oversized replacement rejected; previous file preserved')
            with transferencia_de_ficheiros_conexión.transfercmd('STOR pending.txt') as carga_Ficheiros:
                # A control command must not change the active upload's destination.
                assert transferencia_de_ficheiros_conexión.size('binary.dat') == len(carga_datos_60367a51)
                carga_Ficheiros.sendall(b'UPLOAD TARGET PRESERVED')
            assert transferencia_de_ficheiros_conexión.voidresp().startswith('226')
            RESULTANTE = bytearray(); transferencia_de_ficheiros_conexión.retrbinary('RETR pending.txt', RESULTANTE.extend)
            assert RESULTANTE == b'UPLOAD TARGET PRESERVED'
            RESULTANTE = bytearray(); transferencia_de_ficheiros_conexión.retrbinary('RETR binary.dat', RESULTANTE.extend)
            assert RESULTANTE == carga_datos_60367a51
            transferencia_de_ficheiros_conexión.delete('pending.txt')
            validación_informe['checks'].append('interleaved SIZE cannot change the active STOR destination')
            transferencia_de_ficheiros_conexión.storbinary('STOR 인사.jar', io.BytesIO(Arquivo.getvalue()))
            Texto = shell('java -jar 인사.jar 누리')
            assert 'JAR executar_comando: 누리' in Texto and '자체 kernel_VALOR Ficheiro' in Texto and 'exit 0' in Texto, Texto
            Texto = shell('./인사.jar 세상')
            assert 'JAR executar_comando: 세상' in Texto and 'exit 0' in Texto, Texto
            validación_informe['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct datos { int 수; double 비율; };\nint SUMA_VALOR(int n) { return n ? n + SUMA_VALOR(n-1) : 0; }\nint main(void) { struct datos VALOR = {SUMA_VALOR(10), 1.25}; if (VALOR.수 != 55 || VALOR.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = abrir_Ficheiro("cc.txt", de_lectura_e_escrita | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; escribir_Ficheiro_datos(문서, 인사, sizeof(인사)-1); peche_Ficheiro(문서); escribir_Ficheiro_datos(1, 인사, sizeof(인사)-1); return 0; }\n'
            transferencia_de_ficheiros_conexión.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Texto = shell('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Texto and 'exit 0' in Texto, Texto
            Texto = shell('run 한글.elf'); assert 'CC NATIVE PASS' in Texto and 'exit 0' in Texto, Texto
            assert 'CC NATIVE PASS' in shell('cat cc.txt')
            실행파일 = bytearray(); transferencia_de_ficheiros_conexión.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            transferencia_de_ficheiros_conexión.storbinary('STOR copiar_VALOR.elf', io.BytesIO(실행파일)); Texto = shell('run copiar_VALOR.elf'); assert 'CC NATIVE PASS' in Texto and 'exit 0' in Texto, Texto
            transferencia_de_ficheiros_conexión.storbinary('STOR executar_comando', io.BytesIO(실행파일)); Texto=shell('./executar_comando');assert 'CC NATIVE PASS' in Texto and 'exit 0' in Texto,Texto
            transferencia_de_ficheiros_conexión.storbinary('STOR Nome.txt', io.BytesIO(실행파일)); Texto=shell('./Nome.txt');assert 'CC NATIVE PASS' in Texto and 'exit 0' in Texto,Texto
            shell('rm executar_comando Nome.txt')
            validación_informe['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            shell('rm binary.dat 한글.txt 한글.c 한글.elf copiar_VALOR.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(medida_datos/'linux-reference')
            transferencia_de_ficheiros_conexión.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Texto=shell('./리눅스인사');assert 'exit -8' in Texto,Texto
            Texto=shell('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Texto,Texto
            assert 'LINUX ELF FILE IO' in shell('cat linux.txt')
            transferencia_de_ficheiros_conexión.delete('리눅스인사');transferencia_de_ficheiros_conexión.delete('linux.txt')
            transferencia_de_ficheiros_conexión.storbinary('STOR FALSO_VALOR.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in shell('./FALSO_VALOR.elf');transferencia_de_ficheiros_conexión.delete('FALSO_VALOR.elf')
            validación_informe['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as eco_servidor_introdución:
                통신원문 = medida_datos/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Conectar = Galego.자체.연결통신.Conectar("10.0.2.2", Integer.parseInt(args[0]));
 Conectar.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] FONTE = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<FONTE.length;i++) if (Conectar.getInputStream().read() != (FONTE[i]&255)) throw new RuntimeException("TCP mismatch");
 Conectar.close();
 DatagramSocket extremo = Galego.자체.통신.Abrir(0); Galego.자체.통신.TIMEOUT(extremo, 500);
 Galego.자체.통신.enviar(extremo, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Galego.자체.통신.받기(extremo).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 extremo.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_raíz/'build/java-library/classes'),'-d',str(medida_datos),str(통신원문)])
                transferencia_de_ficheiros_conexión.storbinary('STOR 바깥통신.class', io.BytesIO((medida_datos/'바깥통신.class').read_bytes()))
                Texto = shell('java 바깥통신 {} {}'.format(eco_servidor_introdución.TCP_porto, eco_servidor_introdución.UDP_porto))
                assert 'EXTERNAL TCP UDP PASS' in Texto and '10.0.2.2' in Texto and 'exit 0' in Texto, Texto
                assert eco_servidor_introdución.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, eco_servidor_introdución.수신됨
                assert not eco_servidor_introdución.오류들, eco_servidor_introdución.오류들
            validación_informe['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            transferencia_de_ficheiros_conexión.delete('바깥통신.class')
            servidor_fonte=medida_datos/'서버시험.java'
            servidor_fonte.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket servidor_VALOR = new ServerSocket(9300); DatagramSocket extremo = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket convidado_VALOR = servidor_VALOR.accept();
  convidado_VALOR.getOutputStream().write(convidado_VALOR.getInputStream().read()+1); convidado_VALOR.close(); servidor_VALOR.close();
  byte[] Contido_VALOR = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Contido_VALOR, Contido_VALOR.length); extremo.receive(전문);
  extremo.send(전문); extremo.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(medida_datos),str(servidor_fonte)])
            transferencia_de_ficheiros_conexión.storbinary('STOR 서버시험.class',io.BytesIO((medida_datos/'서버시험.class').read_bytes()))
            Proceso.stdin.write('java 서버시험\n'.encode());Proceso.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',servidor_fluxo_porto),timeout=5) as punto_VALOR:
                punto_VALOR.sendall(b'A');assert punto_VALOR.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as punto_VALOR:
                punto_VALOR.settimeout(5);punto_VALOR.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert punto_VALOR.recvfrom(512)[0]==b'UDP-IN'
            Texto=수신하기();assert 'INBOUND TCP UDP PASS' in Texto and 'exit 0' in Texto,Texto
            validación_informe['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            transferencia_de_ficheiros_conexión.delete('서버시험.class')
            instrución_SECUENCIA = 'public class 빛 { public static void main(String[] Argumentos) throws Exception { int SUMA_VALOR = 0; int 수 = 1; while (수 <= 10) { SUMA_VALOR = SUMA_VALOR + 수; 수 = 수 + 1; } Galego.자체.Saída.수쓰기(SUMA_VALOR); Galego.자체.Ficheiro.Escritura("aot.txt", "한글 AOT Ficheiro 😀"); Galego.자체.Saída.escribir_liña(Galego.자체.Ficheiro.Lectura("aot.txt")); } }'
            transferencia_de_ficheiros_conexión.storbinary('STOR 빛.java', io.BytesIO(instrución_SECUENCIA.encode()))
            Texto = shell('javac 빛.java'); assert 'exit 0' in Texto and 'Compiled:' in Texto, Texto
            Texto = shell('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Texto and 'exit 0' in Texto, Texto
            Texto = shell('run 빛.elf'); assert '\n55\n' in Texto and '한글 AOT Ficheiro 😀' in Texto and 'exit 0' in Texto, Texto
            자체실행파일 = bytearray(); transferencia_de_ficheiros_conexión.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Texto = shell('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Texto and 'unsupported' in Texto, Texto
            보존자료 = bytearray(); transferencia_de_ficheiros_conexión.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); transferencia_de_ficheiros_conexión.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            transferencia_de_ficheiros_conexión.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Texto = shell('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Texto and 'exit 0' in Texto, Texto
            Texto = shell('run 빛.elf'); assert '\n55\n' in Texto and '한글 AOT Ficheiro 😀' in Texto and 'exit 0' in Texto, Texto
            validación_informe['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            validación_informe['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            estático_fonte=medida_datos/'정적시험.java'
            estático_fonte.write_text('''public class 정적시험 {
 static int Project_raíz = 3;
 static int SUMA_VALOR(int n) { return n == 0 ? 0 : n + SUMA_VALOR(n-1); }
 public static void main(String[] Argumentos) {
  int[] VALOR = new int[] {Project_raíz, SUMA_VALOR(10)};
  System.out.println(VALOR[0] + VALOR[1]); System.out.println(Argumentos[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(medida_datos),str(estático_fonte)])
            transferencia_de_ficheiros_conexión.storbinary('STOR 정적시험.class',io.BytesIO((medida_datos/'정적시험.class').read_bytes()))
            Texto=shell('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Texto,Texto
            Texto=shell('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Texto,Texto
            transferencia_de_ficheiros_conexión.delete('정적시험.class');transferencia_de_ficheiros_conexión.delete('정적시험.elf')
            validación_informe['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arquivo.getvalue());손상자료[14]^=1
            transferencia_de_ficheiros_conexión.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Texto=shell('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Texto,Texto
            validación_informe['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            transferencia_de_ficheiros_conexión.quit(); assert 'FTP stopped' in shell('ftpd stop')
            assert not ponte.ERRO, ponte.ERRO
            validación_informe.update(passed=True, frames_to_guest=ponte.커널수신틀수, frames_from_guest=ponte.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in 준비선택기.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            ponte.Pausa_evento.set()
            Proceso.terminate()
            try: Proceso.wait(timeout=5)
            except subprocess.TimeoutExpired: Proceso.kill(); Proceso.wait()
            준비선택기.close(); Proceso.stdin.close(); Proceso.stdout.close()
            validación_informe['bridge_error'] = ponte.ERRO
            validación_informe['frames_to_guest'] = ponte.커널수신틀수; validación_informe['frames_from_guest'] = ponte.커널발신틀수
            (medida_datos/'packets.json').write_text(json.dumps(ponte.traza_LOG,indent=2)+'\n')
            (medida_datos / 'serial.log').write_bytes(대화기록)
            (medida_datos / 'report.json').write_text(json.dumps(validación_informe, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Executar_2()
