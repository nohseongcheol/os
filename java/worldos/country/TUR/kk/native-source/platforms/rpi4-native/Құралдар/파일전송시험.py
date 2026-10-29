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
from желі_көпір import желі_көпір
from орындау_пәрмен import жоба_түбір, Команда
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Орындау_2():
    өлшем_деректер = жоба_түбір / 'build/verification/ftp'; өлшем_деректер.mkdir(parents=True, exist_ok=True)
    тексерім_есеп = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((жоба_түбір / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = өлшем_деректер / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Аргументтер) throws Exception { 한국어.자체.Шығысы.жазу_жол("JAR орындау_пәрмен: " + Аргументтер[0]); 한국어.자체.Файл.Жазу("jar.txt", "자체 ядро_мән Файл"); 한국어.자체.Шығысы.жазу_жол(한국어.자체.Файл.Оқу("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(жоба_түбір/'build/java-library/classes'), '-d', str(өлшем_деректер), str(자바원문)])
    Мұрағат = io.BytesIO()
    with zipfile.ZipFile(Мұрағат, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(өлшем_деректер/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); порт_нөмірі = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); сервер_ағым_порт = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with желі_көпір(порт_нөмірі, ['tcp:{}:9300'.format(сервер_ағым_порт), 'udp:{}:9301'.format(서버전문접속번호)], түсіру=True) as көпір:
        Үрдіс = subprocess.Popen(Команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + көпір.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        селектор = selectors.DefaultSelector(); селектор.register(Үрдіс.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            деректер = bytearray(); тоқтату_жылжыту = time.monotonic() + 시간제한
            while 확인표시 not in деректер:
                if time.monotonic() > тоқтату_жылжыту or Үрдіс.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + деректер.decode('utf-8', 'replace'))
                for 누름값, _ in селектор.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: деректер.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in деректер or b'FAIL ' in деректер: raise AssertionError(деректер)
            return деректер.decode('utf-8', 'replace').replace('\r\n', '\n')
        def қоршам(Жол):
            Үрдіс.stdin.write(Жол.encode() + b'\n'); Үрдіс.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in қоршам('ftpd start')
            файл_тасымалдау_қосылым = ftplib.FTP(); файл_тасымалдау_қосылым.encoding = 'utf-8'; файл_тасымалдау_қосылым.connect('127.0.0.1', порт_нөмірі, timeout=20); файл_тасымалдау_қосылым.login()
            жүктеме_деректер = bytes(range(256)) * 32
            файл_тасымалдау_қосылым.storbinary('STOR binary.dat', io.BytesIO(жүктеме_деректер))
            НӘТИЖЕ = bytearray(); файл_тасымалдау_қосылым.retrbinary('RETR binary.dat', НӘТИЖЕ.extend)
            assert НӘТИЖЕ == жүктеме_деректер; assert файл_тасымалдау_қосылым.size('binary.dat') == len(жүктеме_деректер)
            тексерім_есеп['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            файл_тасымалдау_қосылым.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in қоршам('cat 한글.txt')
            assert '한글.txt' in файл_тасымалдау_қосылым.nlst()
            assert dict(файл_тасымалдау_қосылым.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            тексерім_есеп['checks'].append('UTF-8 filename and content visible in guest shell')
            try: файл_тасымалдау_қосылым.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            НӘТИЖЕ = bytearray(); файл_тасымалдау_қосылым.retrbinary('RETR binary.dat', НӘТИЖЕ.extend); assert НӘТИЖЕ == жүктеме_деректер
            тексерім_есеп['checks'].append('oversized replacement rejected; previous file preserved')
            with файл_тасымалдау_қосылым.transfercmd('STOR pending.txt') as Жүктеп_салу_Файлдар:
                # A control command must not change the active upload's destination.
                assert файл_тасымалдау_қосылым.size('binary.dat') == len(жүктеме_деректер)
                Жүктеп_салу_Файлдар.sendall(b'UPLOAD TARGET PRESERVED')
            assert файл_тасымалдау_қосылым.voidresp().startswith('226')
            НӘТИЖЕ = bytearray(); файл_тасымалдау_қосылым.retrbinary('RETR pending.txt', НӘТИЖЕ.extend)
            assert НӘТИЖЕ == b'UPLOAD TARGET PRESERVED'
            НӘТИЖЕ = bytearray(); файл_тасымалдау_қосылым.retrbinary('RETR binary.dat', НӘТИЖЕ.extend)
            assert НӘТИЖЕ == жүктеме_деректер
            файл_тасымалдау_қосылым.delete('pending.txt')
            тексерім_есеп['checks'].append('interleaved SIZE cannot change the active STOR destination')
            файл_тасымалдау_қосылым.storbinary('STOR 인사.jar', io.BytesIO(Мұрағат.getvalue()))
            Мәтін = қоршам('java -jar 인사.jar 누리')
            assert 'JAR орындау_пәрмен: 누리' in Мәтін and '자체 ядро_мән Файл' in Мәтін and 'exit 0' in Мәтін, Мәтін
            Мәтін = қоршам('./인사.jar 세상')
            assert 'JAR орындау_пәрмен: 세상' in Мәтін and 'exit 0' in Мәтін, Мәтін
            тексерім_есеп['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct деректер { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct деректер мән = {합(10), 1.25}; if (мән.수 != 55 || мән.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ашу_файл("cc.txt", оқу_жазу | 없으면만들기 | қысқарту_Мазмұны, 0600); if (문서 < 0) return 1; жазу_файл_деректер(문서, 인사, sizeof(인사)-1); Жабу_файл(문서); жазу_файл_деректер(1, 인사, sizeof(인사)-1); return 0; }\n'
            файл_тасымалдау_қосылым.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Мәтін = қоршам('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Мәтін and 'exit 0' in Мәтін, Мәтін
            Мәтін = қоршам('run 한글.elf'); assert 'CC NATIVE PASS' in Мәтін and 'exit 0' in Мәтін, Мәтін
            assert 'CC NATIVE PASS' in қоршам('cat cc.txt')
            실행파일 = bytearray(); файл_тасымалдау_қосылым.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            файл_тасымалдау_қосылым.storbinary('STOR дана_мән.elf', io.BytesIO(실행파일)); Мәтін = қоршам('run дана_мән.elf'); assert 'CC NATIVE PASS' in Мәтін and 'exit 0' in Мәтін, Мәтін
            файл_тасымалдау_қосылым.storbinary('STOR орындау_пәрмен', io.BytesIO(실행파일)); Мәтін=қоршам('./орындау_пәрмен');assert 'CC NATIVE PASS' in Мәтін and 'exit 0' in Мәтін,Мәтін
            файл_тасымалдау_қосылым.storbinary('STOR Аты.txt', io.BytesIO(실행파일)); Мәтін=қоршам('./Аты.txt');assert 'CC NATIVE PASS' in Мәтін and 'exit 0' in Мәтін,Мәтін
            қоршам('rm орындау_пәрмен Аты.txt')
            тексерім_есеп['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            қоршам('rm binary.dat 한글.txt 한글.c 한글.elf дана_мән.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(өлшем_деректер/'linux-reference')
            файл_тасымалдау_қосылым.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Мәтін=қоршам('./리눅스인사');assert 'exit -8' in Мәтін,Мәтін
            Мәтін=қоршам('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Мәтін,Мәтін
            assert 'LINUX ELF FILE IO' in қоршам('cat linux.txt')
            файл_тасымалдау_қосылым.delete('리눅스인사');файл_тасымалдау_қосылым.delete('linux.txt')
            файл_тасымалдау_қосылым.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in қоршам('./거짓.elf');файл_тасымалдау_қосылым.delete('거짓.elf')
            тексерім_есеп['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as экранға_шығару_сервер_енгізу:
                통신원문 = өлшем_деректер/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Байланысу = 한국어.자체.연결통신.Байланысу("10.0.2.2", Integer.parseInt(args[0]));
 Байланысу.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] Неден = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<Неден.length;i++) if (Байланысу.getInputStream().read() != (Неден[i]&255)) throw new RuntimeException("TCP mismatch");
 Байланысу.close();
 DatagramSocket қатысушы = 한국어.자체.통신.Ашу(0); 한국어.자체.통신.ТАЙМ_АУТ(қатысушы, 500);
 한국어.자체.통신.жіберу(қатысушы, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(қатысушы).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 қатысушы.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(жоба_түбір/'build/java-library/classes'),'-d',str(өлшем_деректер),str(통신원문)])
                файл_тасымалдау_қосылым.storbinary('STOR 바깥통신.class', io.BytesIO((өлшем_деректер/'바깥통신.class').read_bytes()))
                Мәтін = қоршам('java 바깥통신 {} {}'.format(экранға_шығару_сервер_енгізу.TCP_протоколы_порт, экранға_шығару_сервер_енгізу.пайдаланушы_датаграммасының_протоколы_порт))
                assert 'EXTERNAL TCP UDP PASS' in Мәтін and '10.0.2.2' in Мәтін and 'exit 0' in Мәтін, Мәтін
                assert экранға_шығару_сервер_енгізу.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, экранға_шығару_сервер_енгізу.수신됨
                assert not экранға_шығару_сервер_енгізу.오류들, экранға_шығару_сервер_енгізу.오류들
            тексерім_есеп['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            файл_тасымалдау_қосылым.delete('바깥통신.class')
            сервер_көз=өлшем_деректер/'서버시험.java'
            сервер_көз.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket сервер_мән = new ServerSocket(9300); DatagramSocket қатысушы = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket қонақ_мән = сервер_мән.accept();
  қонақ_мән.getOutputStream().write(қонақ_мән.getInputStream().read()+1); қонақ_мән.close(); сервер_мән.close();
  byte[] мазмұн_мән = new byte[8]; DatagramPacket 전문 = new DatagramPacket(мазмұн_мән, мазмұн_мән.length); қатысушы.receive(전문);
  қатысушы.send(전문); қатысушы.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(өлшем_деректер),str(сервер_көз)])
            файл_тасымалдау_қосылым.storbinary('STOR 서버시험.class',io.BytesIO((өлшем_деректер/'서버시험.class').read_bytes()))
            Үрдіс.stdin.write('java 서버시험\n'.encode());Үрдіс.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',сервер_ағым_порт),timeout=5) as бір_рангілі_мән:
                бір_рангілі_мән.sendall(b'A');assert бір_рангілі_мән.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as бір_рангілі_мән:
                бір_рангілі_мән.settimeout(5);бір_рангілі_мән.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert бір_рангілі_мән.recvfrom(512)[0]==b'UDP-IN'
            Мәтін=수신하기();assert 'INBOUND TCP UDP PASS' in Мәтін and 'exit 0' in Мәтін,Мәтін
            тексерім_есеп['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            файл_тасымалдау_қосылым.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] Аргументтер) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.Шығысы.수쓰기(합); 한국어.자체.Файл.Жазу("aot.txt", "한글 AOT Файл 😀"); 한국어.자체.Шығысы.жазу_жол(한국어.자체.Файл.Оқу("aot.txt")); } }'
            файл_тасымалдау_қосылым.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            Мәтін = қоршам('javac 빛.java'); assert 'exit 0' in Мәтін and 'Compiled:' in Мәтін, Мәтін
            Мәтін = қоршам('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Мәтін and 'exit 0' in Мәтін, Мәтін
            Мәтін = қоршам('run 빛.elf'); assert '\n55\n' in Мәтін and '한글 AOT Файл 😀' in Мәтін and 'exit 0' in Мәтін, Мәтін
            자체실행파일 = bytearray(); файл_тасымалдау_қосылым.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Мәтін = қоршам('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Мәтін and 'unsupported' in Мәтін, Мәтін
            보존자료 = bytearray(); файл_тасымалдау_қосылым.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); файл_тасымалдау_қосылым.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            файл_тасымалдау_қосылым.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Мәтін = қоршам('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Мәтін and 'exit 0' in Мәтін, Мәтін
            Мәтін = қоршам('run 빛.elf'); assert '\n55\n' in Мәтін and '한글 AOT Файл 😀' in Мәтін and 'exit 0' in Мәтін, Мәтін
            тексерім_есеп['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            тексерім_есеп['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            тұрақты_көз=өлшем_деректер/'정적시험.java'
            тұрақты_көз.write_text('''public class 정적시험 {
 static int жоба_түбір = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] Аргументтер) {
  int[] мән = new int[] {жоба_түбір, 합(10)};
  System.out.println(мән[0] + мән[1]); System.out.println(Аргументтер[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(өлшем_деректер),str(тұрақты_көз)])
            файл_тасымалдау_қосылым.storbinary('STOR 정적시험.class',io.BytesIO((өлшем_деректер/'정적시험.class').read_bytes()))
            Мәтін=қоршам('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Мәтін,Мәтін
            Мәтін=қоршам('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Мәтін,Мәтін
            файл_тасымалдау_қосылым.delete('정적시험.class');файл_тасымалдау_қосылым.delete('정적시험.elf')
            тексерім_есеп['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Мұрағат.getvalue());손상자료[14]^=1
            файл_тасымалдау_қосылым.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Мәтін=қоршам('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Мәтін,Мәтін
            тексерім_есеп['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            файл_тасымалдау_қосылым.quit(); assert 'FTP stopped' in қоршам('ftpd stop')
            assert not көпір.Қате, көпір.Қате
            тексерім_есеп.update(passed=True, frames_to_guest=көпір.커널수신틀수, frames_from_guest=көпір.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in селектор.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            көпір.Тоқтата_тұру_оқиға.set()
            Үрдіс.terminate()
            try: Үрдіс.wait(timeout=5)
            except subprocess.TimeoutExpired: Үрдіс.kill(); Үрдіс.wait()
            селектор.close(); Үрдіс.stdin.close(); Үрдіс.stdout.close()
            тексерім_есеп['bridge_error'] = көпір.Қате
            тексерім_есеп['frames_to_guest'] = көпір.커널수신틀수; тексерім_есеп['frames_from_guest'] = көпір.커널발신틀수
            (өлшем_деректер/'packets.json').write_text(json.dumps(көпір.трассалау_журналы,indent=2)+'\n')
            (өлшем_деректер / 'serial.log').write_bytes(대화기록)
            (өлшем_деректер / 'report.json').write_text(json.dumps(тексерім_есеп, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Орындау_2()
