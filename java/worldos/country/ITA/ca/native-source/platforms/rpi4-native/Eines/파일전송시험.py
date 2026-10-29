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
from xarxa_pont import xarxa_pont
from Executa_ordre import Project_rel, Ordre
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Executa_2():
    mesura_dades = Project_rel / 'build/verification/ftp'; mesura_dades.mkdir(parents=True, exist_ok=True)
    validació_informe = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Project_rel / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = mesura_dades / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { Català.propi.Sortida.escriure_línia("JAR Executa_ordre: " + 인수[0]); Català.propi.Fitxer.Escriptura("jar.txt", "propi nucli_VALOR Fitxer"); Català.propi.Sortida.escriure_línia(Català.propi.Fitxer.Lectura("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_rel/'build/java-library/classes'), '-d', str(mesura_dades), str(자바원문)])
    Arxiu = io.BytesIO()
    with zipfile.ZipFile(Arxiu, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(mesura_dades/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); número_de_port = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); servidor_flux_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with xarxa_pont(número_de_port, ['tcp:{}:9300'.format(servidor_flux_port), 'udp:{}:9301'.format(서버전문접속번호)], capturar=True) as pont:
        Procés = subprocess.Popen(Ordre() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + pont.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        준비선택기 = selectors.DefaultSelector(); 준비선택기.register(Procés.stdout, selectors.EVENT_READ)
        def rebre_correu(확인표시=b'jkoros-native> ', 시간제한=60):
            dades = bytearray(); finalitzar_DESPLAÇAMENT = time.monotonic() + 시간제한
            while 확인표시 not in dades:
                if time.monotonic() > finalitzar_DESPLAÇAMENT or Procés.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + dades.decode('utf-8', 'replace'))
                for 누름값, _ in 준비선택기.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: dades.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in dades or b'FAIL ' in dades: raise AssertionError(dades)
            return dades.decode('utf-8', 'replace').replace('\r\n', '\n')
        def shell(línia):
            Procés.stdin.write(línia.encode() + b'\n'); Procés.stdin.flush(); return rebre_correu()
        try:
            rebre_correu(); assert 'FTP listening' in shell('ftpd start')
            transferència_de_fitxers_connexió = ftplib.FTP(); transferència_de_fitxers_connexió.encoding = 'utf-8'; transferència_de_fitxers_connexió.connect('127.0.0.1', número_de_port, timeout=20); transferència_de_fitxers_connexió.login()
            càrrega_dades = bytes(range(256)) * 32
            transferència_de_fitxers_connexió.storbinary('STOR binary.dat', io.BytesIO(càrrega_dades))
            RESULTAT = bytearray(); transferència_de_fitxers_connexió.retrbinary('RETR binary.dat', RESULTAT.extend)
            assert RESULTAT == càrrega_dades; assert transferència_de_fitxers_connexió.size('binary.dat') == len(càrrega_dades)
            validació_informe['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            transferència_de_fitxers_connexió.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in shell('cat 한글.txt')
            assert '한글.txt' in transferència_de_fitxers_connexió.nlst()
            assert dict(transferència_de_fitxers_connexió.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            validació_informe['checks'].append('UTF-8 filename and content visible in guest shell')
            try: transferència_de_fitxers_connexió.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            RESULTAT = bytearray(); transferència_de_fitxers_connexió.retrbinary('RETR binary.dat', RESULTAT.extend); assert RESULTAT == càrrega_dades
            validació_informe['checks'].append('oversized replacement rejected; previous file preserved')
            with transferència_de_fitxers_connexió.transfercmd('STOR pending.txt') as pujar_Fitxers:
                # A control command must not change the active upload's destination.
                assert transferència_de_fitxers_connexió.size('binary.dat') == len(càrrega_dades)
                pujar_Fitxers.sendall(b'UPLOAD TARGET PRESERVED')
            assert transferència_de_fitxers_connexió.voidresp().startswith('226')
            RESULTAT = bytearray(); transferència_de_fitxers_connexió.retrbinary('RETR pending.txt', RESULTAT.extend)
            assert RESULTAT == b'UPLOAD TARGET PRESERVED'
            RESULTAT = bytearray(); transferència_de_fitxers_connexió.retrbinary('RETR binary.dat', RESULTAT.extend)
            assert RESULTAT == càrrega_dades
            transferència_de_fitxers_connexió.delete('pending.txt')
            validació_informe['checks'].append('interleaved SIZE cannot change the active STOR destination')
            transferència_de_fitxers_connexió.storbinary('STOR 인사.jar', io.BytesIO(Arxiu.getvalue()))
            SMS = shell('java -jar 인사.jar 누리')
            assert 'JAR Executa_ordre: 누리' in SMS and 'propi nucli_VALOR Fitxer' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('./인사.jar 세상')
            assert 'JAR Executa_ordre: 세상' in SMS and 'exit 0' in SMS, SMS
            validació_informe['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct dades { int 수; double 비율; };\nint SUMA_VALOR(int n) { return n ? n + SUMA_VALOR(n-1) : 0; }\nint main(void) { struct dades VALOR = {SUMA_VALOR(10), 1.25}; if (VALOR.수 != 55 || VALOR.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = crear_arxiu("cc.txt", lectura_escriptura | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; escriure_arxiu_dades(문서, 인사, sizeof(인사)-1); Tanca_arxiu(문서); escriure_arxiu_dades(1, 인사, sizeof(인사)-1); return 0; }\n'
            transferència_de_fitxers_connexió.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            SMS = shell('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('run 한글.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            assert 'CC NATIVE PASS' in shell('cat cc.txt')
            실행파일 = bytearray(); transferència_de_fitxers_connexió.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            transferència_de_fitxers_connexió.storbinary('STOR copiar_VALOR.elf', io.BytesIO(실행파일)); SMS = shell('run copiar_VALOR.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            transferència_de_fitxers_connexió.storbinary('STOR Executa_ordre', io.BytesIO(실행파일)); SMS=shell('./Executa_ordre');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            transferència_de_fitxers_connexió.storbinary('STOR Nom.txt', io.BytesIO(실행파일)); SMS=shell('./Nom.txt');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            shell('rm Executa_ordre Nom.txt')
            validació_informe['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            shell('rm binary.dat 한글.txt 한글.c 한글.elf copiar_VALOR.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(mesura_dades/'linux-reference')
            transferència_de_fitxers_connexió.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            SMS=shell('./리눅스인사');assert 'exit -8' in SMS,SMS
            SMS=shell('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in SMS,SMS
            assert 'LINUX ELF FILE IO' in shell('cat linux.txt')
            transferència_de_fitxers_connexió.delete('리눅스인사');transferència_de_fitxers_connexió.delete('linux.txt')
            transferència_de_fitxers_connexió.storbinary('STOR FALS_VALOR.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in shell('./FALS_VALOR.elf');transferència_de_fitxers_connexió.delete('FALS_VALOR.elf')
            validació_informe['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as eco_servidor_introducció:
                통신원문 = mesura_dades/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Connecta = Català.propi.연결통신.Connecta("10.0.2.2", Integer.parseInt(args[0]));
 Connecta.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] FONT = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<FONT.length;i++) if (Connecta.getInputStream().read() != (FONT[i]&255)) throw new RuntimeException("TCP mismatch");
 Connecta.close();
 DatagramSocket extrem = Català.propi.통신.Obre(0); Català.propi.통신.TIMEOUT(extrem, 500);
 Català.propi.통신.enviar(extrem, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Català.propi.통신.rebre(extrem).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 extrem.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_rel/'build/java-library/classes'),'-d',str(mesura_dades),str(통신원문)])
                transferència_de_fitxers_connexió.storbinary('STOR 바깥통신.class', io.BytesIO((mesura_dades/'바깥통신.class').read_bytes()))
                SMS = shell('java 바깥통신 {} {}'.format(eco_servidor_introducció.TCP_port, eco_servidor_introducció.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in SMS and '10.0.2.2' in SMS and 'exit 0' in SMS, SMS
                assert eco_servidor_introducció.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, eco_servidor_introducció.수신됨
                assert not eco_servidor_introducció.오류들, eco_servidor_introducció.오류들
            validació_informe['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            transferència_de_fitxers_connexió.delete('바깥통신.class')
            servidor_font=mesura_dades/'서버시험.java'
            servidor_font.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket servidor_VALOR = new ServerSocket(9300); DatagramSocket extrem = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket convidat_VALOR = servidor_VALOR.accept();
  convidat_VALOR.getOutputStream().write(convidat_VALOR.getInputStream().read()+1); convidat_VALOR.close(); servidor_VALOR.close();
  byte[] contingut_VALOR = new byte[8]; DatagramPacket 전문 = new DatagramPacket(contingut_VALOR, contingut_VALOR.length); extrem.receive(전문);
  extrem.send(전문); extrem.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mesura_dades),str(servidor_font)])
            transferència_de_fitxers_connexió.storbinary('STOR 서버시험.class',io.BytesIO((mesura_dades/'서버시험.class').read_bytes()))
            Procés.stdin.write('java 서버시험\n'.encode());Procés.stdin.flush();rebre_correu(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',servidor_flux_port),timeout=5) as homòleg_VALOR:
                homòleg_VALOR.sendall(b'A');assert homòleg_VALOR.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as homòleg_VALOR:
                homòleg_VALOR.settimeout(5);homòleg_VALOR.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert homòleg_VALOR.recvfrom(512)[0]==b'UDP-IN'
            SMS=rebre_correu();assert 'INBOUND TCP UDP PASS' in SMS and 'exit 0' in SMS,SMS
            validació_informe['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            transferència_de_fitxers_connexió.delete('서버시험.class')
            instrucció_SEQÜÈNCIA = 'public class 빛 { public static void main(String[] 인수) throws Exception { int SUMA_VALOR = 0; int 수 = 1; while (수 <= 10) { SUMA_VALOR = SUMA_VALOR + 수; 수 = 수 + 1; } Català.propi.Sortida.수쓰기(SUMA_VALOR); Català.propi.Fitxer.Escriptura("aot.txt", "한글 AOT Fitxer 😀"); Català.propi.Sortida.escriure_línia(Català.propi.Fitxer.Lectura("aot.txt")); } }'
            transferència_de_fitxers_connexió.storbinary('STOR 빛.java', io.BytesIO(instrucció_SEQÜÈNCIA.encode()))
            SMS = shell('javac 빛.java'); assert 'exit 0' in SMS and 'Compiled:' in SMS, SMS
            SMS = shell('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT Fitxer 😀' in SMS and 'exit 0' in SMS, SMS
            자체실행파일 = bytearray(); transferència_de_fitxers_connexió.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            SMS = shell('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in SMS and 'unsupported' in SMS, SMS
            보존자료 = bytearray(); transferència_de_fitxers_connexió.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); transferència_de_fitxers_connexió.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            transferència_de_fitxers_connexió.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            SMS = shell('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT Fitxer 😀' in SMS and 'exit 0' in SMS, SMS
            validació_informe['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            validació_informe['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            estàtic_font=mesura_dades/'정적시험.java'
            estàtic_font.write_text('''public class 정적시험 {
 static int Project_rel = 3;
 static int SUMA_VALOR(int n) { return n == 0 ? 0 : n + SUMA_VALOR(n-1); }
 public static void main(String[] 인수) {
  int[] VALOR = new int[] {Project_rel, SUMA_VALOR(10)};
  System.out.println(VALOR[0] + VALOR[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mesura_dades),str(estàtic_font)])
            transferència_de_fitxers_connexió.storbinary('STOR 정적시험.class',io.BytesIO((mesura_dades/'정적시험.class').read_bytes()))
            SMS=shell('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in SMS,SMS
            SMS=shell('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in SMS,SMS
            transferència_de_fitxers_connexió.delete('정적시험.class');transferència_de_fitxers_connexió.delete('정적시험.elf')
            validació_informe['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arxiu.getvalue());손상자료[14]^=1
            transferència_de_fitxers_connexió.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            SMS=shell('java -jar 인사.jar');assert 'Main-Class\nexit 1' in SMS,SMS
            validació_informe['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            transferència_de_fitxers_connexió.quit(); assert 'FTP stopped' in shell('ftpd stop')
            assert not pont.s_ha_produït_un_error, pont.s_ha_produït_un_error
            validació_informe.update(passed=True, frames_to_guest=pont.커널수신틀수, frames_from_guest=pont.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in 준비선택기.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            pont.Pausa_incidència.set()
            Procés.terminate()
            try: Procés.wait(timeout=5)
            except subprocess.TimeoutExpired: Procés.kill(); Procés.wait()
            준비선택기.close(); Procés.stdin.close(); Procés.stdout.close()
            validació_informe['bridge_error'] = pont.s_ha_produït_un_error
            validació_informe['frames_to_guest'] = pont.커널수신틀수; validació_informe['frames_from_guest'] = pont.커널발신틀수
            (mesura_dades/'packets.json').write_text(json.dumps(pont.traça_LOG,indent=2)+'\n')
            (mesura_dades / 'serial.log').write_bytes(대화기록)
            (mesura_dades / 'report.json').write_text(json.dumps(validació_informe, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Executa_2()
