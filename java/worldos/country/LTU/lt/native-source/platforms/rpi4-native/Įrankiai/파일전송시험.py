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
from tiltas_3de4fe3a import tiltas_3de4fe3a
from Vykdyti_komanda import Project_šaknis, Komanda
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Paleisti():
    KR_duomenys = Project_šaknis / 'build/verification/ftp'; KR_duomenys.mkdir(parents=True, exist_ok=True)
    tikrinimas_pranešti = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Project_šaknis / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkribavimas = bytearray()
    자바원문 = KR_duomenys / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Argumentai) throws Exception { Lietuvių.savas.Išvestis.rašymas_eilutė("JAR Vykdyti_komanda: " + Argumentai[0]); Lietuvių.savas.Failas.Rašymas("jar.txt", "savas branduolys_VALUE Failas"); Lietuvių.savas.Išvestis.rašymas_eilutė(Lietuvių.savas.Failas.Skaitymas("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_šaknis/'build/java-library/classes'), '-d', str(KR_duomenys), str(자바원문)])
    Archyvas = io.BytesIO()
    with zipfile.ZipFile(Archyvas, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(KR_duomenys/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); prievado_numeris = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); serveris_Stream_jungtis = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); serveris_paketų_kelio_schema_jungtis = 임시자원.getsockname()[1]
    with tiltas_3de4fe3a(prievado_numeris, ['tcp:{}:9300'.format(serveris_Stream_jungtis), 'udp:{}:9301'.format(serveris_paketų_kelio_schema_jungtis)], įrašyti=True) as tiltas:
        Procesas = subprocess.Popen(Komanda() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + tiltas.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        išrinkiklis = selectors.DefaultSelector(); išrinkiklis.register(Procesas.stdout, selectors.EVENT_READ)
        def gauti_žinutė(žymeklis=b'jkoros-native> ', 시간제한=60):
            duomenys = bytearray(); baigti_pokalbį_OFFSET = time.monotonic() + 시간제한
            while žymeklis not in duomenys:
                if time.monotonic() > baigti_pokalbį_OFFSET or Procesas.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + duomenys.decode('utf-8', 'replace'))
                for 누름값, _ in išrinkiklis.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: duomenys.extend(조각); transkribavimas.extend(조각)
                if b'PANIC:' in duomenys or b'FAIL ' in duomenys: raise AssertionError(duomenys)
            return duomenys.decode('utf-8', 'replace').replace('\r\n', '\n')
        def apvalkalas(Eilutė):
            Procesas.stdin.write(Eilutė.encode() + b'\n'); Procesas.stdin.flush(); return gauti_žinutė()
        try:
            gauti_žinutė(); assert 'FTP listening' in apvalkalas('ftpd start')
            failo_perdavimas_ryšys = ftplib.FTP(); failo_perdavimas_ryšys.encoding = 'utf-8'; failo_perdavimas_ryšys.connect('127.0.0.1', prievado_numeris, timeout=20); failo_perdavimas_ryšys.login()
            mokamoji_krova_duomenys = bytes(range(256)) * 32
            failo_perdavimas_ryšys.storbinary('STOR binary.dat', io.BytesIO(mokamoji_krova_duomenys))
            REZULTATAS = bytearray(); failo_perdavimas_ryšys.retrbinary('RETR binary.dat', REZULTATAS.extend)
            assert REZULTATAS == mokamoji_krova_duomenys; assert failo_perdavimas_ryšys.size('binary.dat') == len(mokamoji_krova_duomenys)
            tikrinimas_pranešti['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            failo_perdavimas_ryšys.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in apvalkalas('cat 한글.txt')
            assert '한글.txt' in failo_perdavimas_ryšys.nlst()
            assert dict(failo_perdavimas_ryšys.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            tikrinimas_pranešti['checks'].append('UTF-8 filename and content visible in guest shell')
            try: failo_perdavimas_ryšys.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            REZULTATAS = bytearray(); failo_perdavimas_ryšys.retrbinary('RETR binary.dat', REZULTATAS.extend); assert REZULTATAS == mokamoji_krova_duomenys
            tikrinimas_pranešti['checks'].append('oversized replacement rejected; previous file preserved')
            with failo_perdavimas_ryšys.transfercmd('STOR pending.txt') as Upload_Failai:
                # A control command must not change the active upload's destination.
                assert failo_perdavimas_ryšys.size('binary.dat') == len(mokamoji_krova_duomenys)
                Upload_Failai.sendall(b'UPLOAD TARGET PRESERVED')
            assert failo_perdavimas_ryšys.voidresp().startswith('226')
            REZULTATAS = bytearray(); failo_perdavimas_ryšys.retrbinary('RETR pending.txt', REZULTATAS.extend)
            assert REZULTATAS == b'UPLOAD TARGET PRESERVED'
            REZULTATAS = bytearray(); failo_perdavimas_ryšys.retrbinary('RETR binary.dat', REZULTATAS.extend)
            assert REZULTATAS == mokamoji_krova_duomenys
            failo_perdavimas_ryšys.delete('pending.txt')
            tikrinimas_pranešti['checks'].append('interleaved SIZE cannot change the active STOR destination')
            failo_perdavimas_ryšys.storbinary('STOR 인사.jar', io.BytesIO(Archyvas.getvalue()))
            Tekstas = apvalkalas('java -jar 인사.jar 누리')
            assert 'JAR Vykdyti_komanda: 누리' in Tekstas and 'savas branduolys_VALUE Failas' in Tekstas and 'exit 0' in Tekstas, Tekstas
            Tekstas = apvalkalas('./인사.jar 세상')
            assert 'JAR Vykdyti_komanda: 세상' in Tekstas and 'exit 0' in Tekstas, Tekstas
            tikrinimas_pranešti['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct duomenys { int numeris; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct duomenys VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.numeris != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = kurti_Failas("cc.txt", 읽고쓰기 | 없으면만들기 | trumpinti_Turinys, 0600); if (문서 < 0) return 1; rašymas_Failas_duomenys(문서, 인사, sizeof(인사)-1); Uždaryti_Failas(문서); rašymas_Failas_duomenys(1, 인사, sizeof(인사)-1); return 0; }\n'
            failo_perdavimas_ryšys.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Tekstas = apvalkalas('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Tekstas and 'exit 0' in Tekstas, Tekstas
            Tekstas = apvalkalas('run 한글.elf'); assert 'CC NATIVE PASS' in Tekstas and 'exit 0' in Tekstas, Tekstas
            assert 'CC NATIVE PASS' in apvalkalas('cat cc.txt')
            실행파일 = bytearray(); failo_perdavimas_ryšys.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            failo_perdavimas_ryšys.storbinary('STOR kopijuoti_VALUE.elf', io.BytesIO(실행파일)); Tekstas = apvalkalas('run kopijuoti_VALUE.elf'); assert 'CC NATIVE PASS' in Tekstas and 'exit 0' in Tekstas, Tekstas
            failo_perdavimas_ryšys.storbinary('STOR Vykdyti_komanda', io.BytesIO(실행파일)); Tekstas=apvalkalas('./Vykdyti_komanda');assert 'CC NATIVE PASS' in Tekstas and 'exit 0' in Tekstas,Tekstas
            failo_perdavimas_ryšys.storbinary('STOR Pavadinimas_2.txt', io.BytesIO(실행파일)); Tekstas=apvalkalas('./Pavadinimas_2.txt');assert 'CC NATIVE PASS' in Tekstas and 'exit 0' in Tekstas,Tekstas
            apvalkalas('rm Vykdyti_komanda Pavadinimas_2.txt')
            tikrinimas_pranešti['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            apvalkalas('rm binary.dat 한글.txt 한글.c 한글.elf kopijuoti_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_duomenys/'linux-reference')
            failo_perdavimas_ryšys.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Tekstas=apvalkalas('./리눅스인사');assert 'exit -8' in Tekstas,Tekstas
            Tekstas=apvalkalas('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Tekstas,Tekstas
            assert 'LINUX ELF FILE IO' in apvalkalas('cat linux.txt')
            failo_perdavimas_ryšys.delete('리눅스인사');failo_perdavimas_ryšys.delete('linux.txt')
            failo_perdavimas_ryšys.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 numeris 없습니다:' in apvalkalas('./FALSE_VALUE.elf');failo_perdavimas_ryšys.delete('FALSE_VALUE.elf')
            tikrinimas_pranešti['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as aidas_serveris_įrašas:
                NET_šaltinis = KR_duomenys/'바깥통신.java'
                NET_šaltinis.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Prisijungti = Lietuvių.savas.ryšys_transportavimas.Prisijungti("10.0.2.2", Integer.parseInt(args[0]));
 Prisijungti.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ŠALTINIS = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ŠALTINIS.length;i++) if (Prisijungti.getInputStream().read() != (ŠALTINIS[i]&255)) throw new RuntimeException("TCP mismatch");
 Prisijungti.close();
 DatagramSocket dalyvis = Lietuvių.savas.통신.Atverti(0); Lietuvių.savas.통신.SKIRTASIS_LAIKAS(dalyvis, 500);
 Lietuvių.savas.통신.siųsti(dalyvis, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Lietuvių.savas.통신.gauti(dalyvis).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 dalyvis.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_šaknis/'build/java-library/classes'),'-d',str(KR_duomenys),str(NET_šaltinis)])
                failo_perdavimas_ryšys.storbinary('STOR 바깥통신.class', io.BytesIO((KR_duomenys/'바깥통신.class').read_bytes()))
                Tekstas = apvalkalas('java 바깥통신 {} {}'.format(aidas_serveris_įrašas.TCP_jungtis, aidas_serveris_įrašas.UDP_jungtis))
                assert 'EXTERNAL TCP UDP PASS' in Tekstas and '10.0.2.2' in Tekstas and 'exit 0' in Tekstas, Tekstas
                assert aidas_serveris_įrašas.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, aidas_serveris_įrašas.수신됨
                assert not aidas_serveris_įrašas.오류들, aidas_serveris_įrašas.오류들
            tikrinimas_pranešti['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            failo_perdavimas_ryšys.delete('바깥통신.class')
            serveris_šaltinis=KR_duomenys/'서버시험.java'
            serveris_šaltinis.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket serveris_VALUE = new ServerSocket(9300); DatagramSocket dalyvis = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket svečias_VALUE = serveris_VALUE.accept();
  svečias_VALUE.getOutputStream().write(svečias_VALUE.getInputStream().read()+1); svečias_VALUE.close(); serveris_VALUE.close();
  byte[] Turinys_VALUE = new byte[8]; DatagramPacket paketų_kelio_schema = new DatagramPacket(Turinys_VALUE, Turinys_VALUE.length); dalyvis.receive(paketų_kelio_schema);
  dalyvis.send(paketų_kelio_schema); dalyvis.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_duomenys),str(serveris_šaltinis)])
            failo_perdavimas_ryšys.storbinary('STOR 서버시험.class',io.BytesIO((KR_duomenys/'서버시험.class').read_bytes()))
            Procesas.stdin.write('java 서버시험\n'.encode());Procesas.stdin.flush();gauti_žinutė(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',serveris_Stream_jungtis),timeout=5) as lygiavertis_mazgas_VALUE:
                lygiavertis_mazgas_VALUE.sendall(b'A');assert lygiavertis_mazgas_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as lygiavertis_mazgas_VALUE:
                lygiavertis_mazgas_VALUE.settimeout(5);lygiavertis_mazgas_VALUE.sendto(b'UDP-IN',('127.0.0.1',serveris_paketų_kelio_schema_jungtis));assert lygiavertis_mazgas_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Tekstas=gauti_žinutė();assert 'INBOUND TCP UDP PASS' in Tekstas and 'exit 0' in Tekstas,Tekstas
            tikrinimas_pranešti['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            failo_perdavimas_ryšys.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] Argumentai) throws Exception { int SUM_VALUE = 0; int numeris = 1; while (numeris <= 10) { SUM_VALUE = SUM_VALUE + numeris; numeris = numeris + 1; } Lietuvių.savas.Išvestis.rašymas_numeris(SUM_VALUE); Lietuvių.savas.Failas.Rašymas("aot.txt", "한글 AOT Failas 😀"); Lietuvių.savas.Išvestis.rašymas_eilutė(Lietuvių.savas.Failas.Skaitymas("aot.txt")); } }'
            failo_perdavimas_ryšys.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            Tekstas = apvalkalas('javac 빛.java'); assert 'exit 0' in Tekstas and 'Compiled:' in Tekstas, Tekstas
            Tekstas = apvalkalas('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekstas and 'exit 0' in Tekstas, Tekstas
            Tekstas = apvalkalas('run 빛.elf'); assert '\n55\n' in Tekstas and '한글 AOT Failas 😀' in Tekstas and 'exit 0' in Tekstas, Tekstas
            자체실행파일 = bytearray(); failo_perdavimas_ryšys.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Tekstas = apvalkalas('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Tekstas and 'unsupported' in Tekstas, Tekstas
            보존자료 = bytearray(); failo_perdavimas_ryšys.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); failo_perdavimas_ryšys.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            failo_perdavimas_ryšys.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Tekstas = apvalkalas('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekstas and 'exit 0' in Tekstas, Tekstas
            Tekstas = apvalkalas('run 빛.elf'); assert '\n55\n' in Tekstas and '한글 AOT Failas 😀' in Tekstas and 'exit 0' in Tekstas, Tekstas
            tikrinimas_pranešti['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            tikrinimas_pranešti['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            정적원문=KR_duomenys/'정적시험.java'
            정적원문.write_text('''public class 정적시험 {
 static int Project_šaknis = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] Argumentai) {
  int[] VALUE = new int[] {Project_šaknis, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(Argumentai[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_duomenys),str(정적원문)])
            failo_perdavimas_ryšys.storbinary('STOR 정적시험.class',io.BytesIO((KR_duomenys/'정적시험.class').read_bytes()))
            Tekstas=apvalkalas('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Tekstas,Tekstas
            Tekstas=apvalkalas('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Tekstas,Tekstas
            failo_perdavimas_ryšys.delete('정적시험.class');failo_perdavimas_ryšys.delete('정적시험.elf')
            tikrinimas_pranešti['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Archyvas.getvalue());손상자료[14]^=1
            failo_perdavimas_ryšys.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Tekstas=apvalkalas('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Tekstas,Tekstas
            tikrinimas_pranešti['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            failo_perdavimas_ryšys.quit(); assert 'FTP stopped' in apvalkalas('ftpd stop')
            assert not tiltas.KLAIDA, tiltas.KLAIDA
            tikrinimas_pranešti.update(passed=True, frames_to_guest=tiltas.커널수신틀수, frames_from_guest=tiltas.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in išrinkiklis.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: transkribavimas.extend(조각)
            tiltas.Pauzė_įvykis.set()
            Procesas.terminate()
            try: Procesas.wait(timeout=5)
            except subprocess.TimeoutExpired: Procesas.kill(); Procesas.wait()
            išrinkiklis.close(); Procesas.stdin.close(); Procesas.stdout.close()
            tikrinimas_pranešti['bridge_error'] = tiltas.KLAIDA
            tikrinimas_pranešti['frames_to_guest'] = tiltas.커널수신틀수; tikrinimas_pranešti['frames_from_guest'] = tiltas.커널발신틀수
            (KR_duomenys/'packets.json').write_text(json.dumps(tiltas.sekimo_žurnalas,indent=2)+'\n')
            (KR_duomenys / 'serial.log').write_bytes(transkribavimas)
            (KR_duomenys / 'report.json').write_text(json.dumps(tikrinimas_pranešti, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Paleisti()
