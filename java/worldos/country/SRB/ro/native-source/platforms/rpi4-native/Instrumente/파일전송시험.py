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
from punte_3de4fe3a import punte_3de4fe3a
from executa_comandă import Project_rădăcină, Comandă
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Pornește():
    KR_date = Project_rădăcină / 'build/verification/ftp'; KR_date.mkdir(parents=True, exist_ok=True)
    validare_raport = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Project_rădăcină / 'build/kernel8.img').read_bytes()).hexdigest()}
    transcriere = bytearray()
    자바원문 = KR_date / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Argumente) throws Exception { Română.propriu.Rezultat.scriere_linie("JAR executa_comandă: " + Argumente[0]); Română.propriu.Fișier.Scriere("jar.txt", "propriu nucleu_VALUE Fișier"); Română.propriu.Rezultat.scriere_linie(Română.propriu.Fișier.Citire("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_rădăcină/'build/java-library/classes'), '-d', str(KR_date), str(자바원문)])
    Arhivă = io.BytesIO()
    with zipfile.ZipFile(Arhivă, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(KR_date/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); număr_port = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_flux_muta = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_diagramă_informații_muta = 임시자원.getsockname()[1]
    with punte_3de4fe3a(număr_port, ['tcp:{}:9300'.format(server_flux_muta), 'udp:{}:9301'.format(server_diagramă_informații_muta)], captura=True) as punte:
        Proces = subprocess.Popen(Comandă() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + punte.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selector = selectors.DefaultSelector(); selector.register(Proces.stdout, selectors.EVENT_READ)
        def primi_mesaj(marcaj=b'jkoros-native> ', executare_TIMEOUT=60):
            date = bytearray(); termina_un_apel_OFFSET = time.monotonic() + executare_TIMEOUT
            while marcaj not in date:
                if time.monotonic() > termina_un_apel_OFFSET or Proces.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + date.decode('utf-8', 'replace'))
                for 누름값, _ in selector.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: date.extend(조각); transcriere.extend(조각)
                if b'PANIC:' in date or b'FAIL ' in date: raise AssertionError(date)
            return date.decode('utf-8', 'replace').replace('\r\n', '\n')
        def shell(Linie):
            Proces.stdin.write(Linie.encode() + b'\n'); Proces.stdin.flush(); return primi_mesaj()
        try:
            primi_mesaj(); assert 'FTP listening' in shell('ftpd start')
            transfer_de_fișiere_conexiune = ftplib.FTP(); transfer_de_fișiere_conexiune.encoding = 'utf-8'; transfer_de_fișiere_conexiune.connect('127.0.0.1', număr_port, timeout=20); transfer_de_fișiere_conexiune.login()
            sarcină_date = bytes(range(256)) * 32
            transfer_de_fișiere_conexiune.storbinary('STOR binary.dat', io.BytesIO(sarcină_date))
            KR = bytearray(); transfer_de_fișiere_conexiune.retrbinary('RETR binary.dat', KR.extend)
            assert KR == sarcină_date; assert transfer_de_fișiere_conexiune.size('binary.dat') == len(sarcină_date)
            validare_raport['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            transfer_de_fișiere_conexiune.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in shell('cat 한글.txt')
            assert '한글.txt' in transfer_de_fișiere_conexiune.nlst()
            assert dict(transfer_de_fișiere_conexiune.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            validare_raport['checks'].append('UTF-8 filename and content visible in guest shell')
            try: transfer_de_fișiere_conexiune.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            KR = bytearray(); transfer_de_fișiere_conexiune.retrbinary('RETR binary.dat', KR.extend); assert KR == sarcină_date
            validare_raport['checks'].append('oversized replacement rejected; previous file preserved')
            with transfer_de_fișiere_conexiune.transfercmd('STOR pending.txt') as Upload_Fișiere:
                # A control command must not change the active upload's destination.
                assert transfer_de_fișiere_conexiune.size('binary.dat') == len(sarcină_date)
                Upload_Fișiere.sendall(b'UPLOAD TARGET PRESERVED')
            assert transfer_de_fișiere_conexiune.voidresp().startswith('226')
            KR = bytearray(); transfer_de_fișiere_conexiune.retrbinary('RETR pending.txt', KR.extend)
            assert KR == b'UPLOAD TARGET PRESERVED'
            KR = bytearray(); transfer_de_fișiere_conexiune.retrbinary('RETR binary.dat', KR.extend)
            assert KR == sarcină_date
            transfer_de_fișiere_conexiune.delete('pending.txt')
            validare_raport['checks'].append('interleaved SIZE cannot change the active STOR destination')
            transfer_de_fișiere_conexiune.storbinary('STOR 인사.jar', io.BytesIO(Arhivă.getvalue()))
            SMS = shell('java -jar 인사.jar 누리')
            assert 'JAR executa_comandă: 누리' in SMS and 'propriu nucleu_VALUE Fișier' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('./인사.jar 세상')
            assert 'JAR executa_comandă: 세상' in SMS and 'exit 0' in SMS, SMS
            validare_raport['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct date { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct date VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = crea_Fișier("cc.txt", citire_scriere | 없으면만들기 | trunchia_TOC, 0600); if (문서 < 0) return 1; scriere_Fișier_date(문서, 인사, sizeof(인사)-1); închide_Fișier(문서); scriere_Fișier_date(1, 인사, sizeof(인사)-1); return 0; }\n'
            transfer_de_fișiere_conexiune.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            SMS = shell('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('run 한글.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            assert 'CC NATIVE PASS' in shell('cat cc.txt')
            실행파일 = bytearray(); transfer_de_fișiere_conexiune.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            transfer_de_fișiere_conexiune.storbinary('STOR copia_VALUE.elf', io.BytesIO(실행파일)); SMS = shell('run copia_VALUE.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            transfer_de_fișiere_conexiune.storbinary('STOR executa_comandă', io.BytesIO(실행파일)); SMS=shell('./executa_comandă');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            transfer_de_fișiere_conexiune.storbinary('STOR Nume.txt', io.BytesIO(실행파일)); SMS=shell('./Nume.txt');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            shell('rm executa_comandă Nume.txt')
            validare_raport['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            shell('rm binary.dat 한글.txt 한글.c 한글.elf copia_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_date/'linux-reference')
            transfer_de_fișiere_conexiune.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            SMS=shell('./리눅스인사');assert 'exit -8' in SMS,SMS
            SMS=shell('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in SMS,SMS
            assert 'LINUX ELF FILE IO' in shell('cat linux.txt')
            transfer_de_fișiere_conexiune.delete('리눅스인사');transfer_de_fișiere_conexiune.delete('linux.txt')
            transfer_de_fișiere_conexiune.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in shell('./FALSE_VALUE.elf');transfer_de_fișiere_conexiune.delete('FALSE_VALUE.elf')
            validare_raport['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as ecou_server_intrare:
                NET_sursă = KR_date/'바깥통신.java'
                NET_sursă.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Conectează = Română.propriu.연결통신.Conectează("10.0.2.2", Integer.parseInt(args[0]));
 Conectează.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] SURSĂ = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<SURSĂ.length;i++) if (Conectează.getInputStream().read() != (SURSĂ[i]&255)) throw new RuntimeException("TCP mismatch");
 Conectează.close();
 DatagramSocket participant = Română.propriu.통신.Deschide(0); Română.propriu.통신.TIMEOUT(participant, 500);
 Română.propriu.통신.trimite(participant, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Română.propriu.통신.primi(participant).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 participant.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_rădăcină/'build/java-library/classes'),'-d',str(KR_date),str(NET_sursă)])
                transfer_de_fișiere_conexiune.storbinary('STOR 바깥통신.class', io.BytesIO((KR_date/'바깥통신.class').read_bytes()))
                SMS = shell('java 바깥통신 {} {}'.format(ecou_server_intrare.TCP_muta, ecou_server_intrare.UDP_muta))
                assert 'EXTERNAL TCP UDP PASS' in SMS and '10.0.2.2' in SMS and 'exit 0' in SMS, SMS
                assert ecou_server_intrare.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, ecou_server_intrare.수신됨
                assert not ecou_server_intrare.오류들, ecou_server_intrare.오류들
            validare_raport['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            transfer_de_fișiere_conexiune.delete('바깥통신.class')
            server_sursă=KR_date/'서버시험.java'
            server_sursă.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); DatagramSocket participant = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket invitat_VALUE = server_VALUE.accept();
  invitat_VALUE.getOutputStream().write(invitat_VALUE.getInputStream().read()+1); invitat_VALUE.close(); server_VALUE.close();
  byte[] Conținut_VALUE = new byte[8]; DatagramPacket diagramă_informații = new DatagramPacket(Conținut_VALUE, Conținut_VALUE.length); participant.receive(diagramă_informații);
  participant.send(diagramă_informații); participant.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_date),str(server_sursă)])
            transfer_de_fișiere_conexiune.storbinary('STOR 서버시험.class',io.BytesIO((KR_date/'서버시험.class').read_bytes()))
            Proces.stdin.write('java 서버시험\n'.encode());Proces.stdin.flush();primi_mesaj(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_flux_muta),timeout=5) as pereche_VALUE:
                pereche_VALUE.sendall(b'A');assert pereche_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as pereche_VALUE:
                pereche_VALUE.settimeout(5);pereche_VALUE.sendto(b'UDP-IN',('127.0.0.1',server_diagramă_informații_muta));assert pereche_VALUE.recvfrom(512)[0]==b'UDP-IN'
            SMS=primi_mesaj();assert 'INBOUND TCP UDP PASS' in SMS and 'exit 0' in SMS,SMS
            validare_raport['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            transfer_de_fișiere_conexiune.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] Argumente) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } Română.propriu.Rezultat.수쓰기(SUM_VALUE); Română.propriu.Fișier.Scriere("aot.txt", "한글 AOT Fișier 😀"); Română.propriu.Rezultat.scriere_linie(Română.propriu.Fișier.Citire("aot.txt")); } }'
            transfer_de_fișiere_conexiune.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            SMS = shell('javac 빛.java'); assert 'exit 0' in SMS and 'Compiled:' in SMS, SMS
            SMS = shell('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT Fișier 😀' in SMS and 'exit 0' in SMS, SMS
            자체실행파일 = bytearray(); transfer_de_fișiere_conexiune.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            SMS = shell('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in SMS and 'unsupported' in SMS, SMS
            보존자료 = bytearray(); transfer_de_fișiere_conexiune.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); transfer_de_fișiere_conexiune.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            transfer_de_fișiere_conexiune.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            SMS = shell('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT Fișier 😀' in SMS and 'exit 0' in SMS, SMS
            validare_raport['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            validare_raport['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            정적원문=KR_date/'정적시험.java'
            정적원문.write_text('''public class 정적시험 {
 static int Project_rădăcină = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] Argumente) {
  int[] VALUE = new int[] {Project_rădăcină, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(Argumente[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_date),str(정적원문)])
            transfer_de_fișiere_conexiune.storbinary('STOR 정적시험.class',io.BytesIO((KR_date/'정적시험.class').read_bytes()))
            SMS=shell('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in SMS,SMS
            SMS=shell('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in SMS,SMS
            transfer_de_fișiere_conexiune.delete('정적시험.class');transfer_de_fișiere_conexiune.delete('정적시험.elf')
            validare_raport['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arhivă.getvalue());손상자료[14]^=1
            transfer_de_fișiere_conexiune.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            SMS=shell('java -jar 인사.jar');assert 'Main-Class\nexit 1' in SMS,SMS
            validare_raport['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            transfer_de_fișiere_conexiune.quit(); assert 'FTP stopped' in shell('ftpd stop')
            assert not punte.eroare, punte.eroare
            validare_raport.update(passed=True, frames_to_guest=punte.커널수신틀수, frames_from_guest=punte.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in selector.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: transcriere.extend(조각)
            punte.Pauză_eveniment.set()
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
            selector.close(); Proces.stdin.close(); Proces.stdout.close()
            validare_raport['bridge_error'] = punte.eroare
            validare_raport['frames_to_guest'] = punte.커널수신틀수; validare_raport['frames_from_guest'] = punte.커널발신틀수
            (KR_date/'packets.json').write_text(json.dumps(punte.jurnal_de_urmărire,indent=2)+'\n')
            (KR_date / 'serial.log').write_bytes(transcriere)
            (KR_date / 'report.json').write_text(json.dumps(validare_raport, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Pornește()
