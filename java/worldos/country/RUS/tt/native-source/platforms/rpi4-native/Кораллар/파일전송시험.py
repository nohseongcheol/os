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
from Челтәр_күпер import Челтәр_күпер
from үтәргә_команда import экранга_җибәрү_тамыр, команда
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def эшләтү():
    үлчәм_мәгълүмат = экранга_җибәрү_тамыр / 'build/verification/ftp'; үлчәм_мәгълүмат.mkdir(parents=True, exist_ok=True)
    раслау_отчет = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((экранга_җибәрү_тамыр / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = үлчәм_мәгълүмат / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { Татарча.자체.출력.язу_юл("JAR үтәргә_команда: " + 인수[0]); Татарча.자체.Birem.язу("jar.txt", "자체 төш_VALUE Birem"); Татарча.자체.출력.язу_юл(Татарча.자체.Birem.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(экранга_җибәрү_тамыр/'build/java-library/classes'), '-d', str(үлчәм_мәгълүмат), str(자바원문)])
    Архив = io.BytesIO()
    with zipfile.ZipFile(Архив, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(үлчәм_мәгълүмат/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); сервер_агым_порт = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Челтәр_күпер(접속번호, ['tcp:{}:9300'.format(сервер_агым_порт), 'udp:{}:9301'.format(서버전문접속번호)], яздыру=True) as күпер:
        Процесс = subprocess.Popen(команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + күпер.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        сайлагыч = selectors.DefaultSelector(); сайлагыч.register(Процесс.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            мәгълүмат = bytearray(); тәмамлау_OFFSET = time.monotonic() + 시간제한
            while 확인표시 not in мәгълүмат:
                if time.monotonic() > тәмамлау_OFFSET or Процесс.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + мәгълүмат.decode('utf-8', 'replace'))
                for 누름값, _ in сайлагыч.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: мәгълүмат.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in мәгълүмат or b'FAIL ' in мәгълүмат: raise AssertionError(мәгълүмат)
            return мәгълүмат.decode('utf-8', 'replace').replace('\r\n', '\n')
        def тышча(юл):
            Процесс.stdin.write(юл.encode() + b'\n'); Процесс.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in тышча('ftpd start')
            файл_күчерү_тоташу = ftplib.FTP(); файл_күчерү_тоташу.encoding = 'utf-8'; файл_күчерү_тоташу.connect('127.0.0.1', 접속번호, timeout=20); файл_күчерү_тоташу.login()
            төп_өлеш_мәгълүмат = bytes(range(256)) * 32
            файл_күчерү_тоташу.storbinary('STOR binary.dat', io.BytesIO(төп_өлеш_мәгълүмат))
            үлчәм = bytearray(); файл_күчерү_тоташу.retrbinary('RETR binary.dat', үлчәм.extend)
            assert үлчәм == төп_өлеш_мәгълүмат; assert файл_күчерү_тоташу.size('binary.dat') == len(төп_өлеш_мәгълүмат)
            раслау_отчет['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            файл_күчерү_тоташу.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in тышча('cat 한글.txt')
            assert '한글.txt' in файл_күчерү_тоташу.nlst()
            assert dict(файл_күчерү_тоташу.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            раслау_отчет['checks'].append('UTF-8 filename and content visible in guest shell')
            try: файл_күчерү_тоташу.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            үлчәм = bytearray(); файл_күчерү_тоташу.retrbinary('RETR binary.dat', үлчәм.extend); assert үлчәм == төп_өлеш_мәгълүмат
            раслау_отчет['checks'].append('oversized replacement rejected; previous file preserved')
            with файл_күчерү_тоташу.transfercmd('STOR pending.txt') as йөкләп_җибәрү_Файллар:
                # A control command must not change the active upload's destination.
                assert файл_күчерү_тоташу.size('binary.dat') == len(төп_өлеш_мәгълүмат)
                йөкләп_җибәрү_Файллар.sendall(b'UPLOAD TARGET PRESERVED')
            assert файл_күчерү_тоташу.voidresp().startswith('226')
            үлчәм = bytearray(); файл_күчерү_тоташу.retrbinary('RETR pending.txt', үлчәм.extend)
            assert үлчәм == b'UPLOAD TARGET PRESERVED'
            үлчәм = bytearray(); файл_күчерү_тоташу.retrbinary('RETR binary.dat', үлчәм.extend)
            assert үлчәм == төп_өлеш_мәгълүмат
            файл_күчерү_тоташу.delete('pending.txt')
            раслау_отчет['checks'].append('interleaved SIZE cannot change the active STOR destination')
            файл_күчерү_тоташу.storbinary('STOR 인사.jar', io.BytesIO(Архив.getvalue()))
            Mäten = тышча('java -jar 인사.jar 누리')
            assert 'JAR үтәргә_команда: 누리' in Mäten and '자체 төш_VALUE Birem' in Mäten and 'exit 0' in Mäten, Mäten
            Mäten = тышча('./인사.jar 세상')
            assert 'JAR үтәргә_команда: 세상' in Mäten and 'exit 0' in Mäten, Mäten
            раслау_отчет['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct мәгълүмат { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct мәгълүмат VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ачу_файл("cc.txt", укымалы_язмалы | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; язу_файл_мәгълүмат(문서, 인사, sizeof(인사)-1); чик_файл(문서); язу_файл_мәгълүмат(1, 인사, sizeof(인사)-1); return 0; }\n'
            файл_күчерү_тоташу.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Mäten = тышча('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Mäten and 'exit 0' in Mäten, Mäten
            Mäten = тышча('run 한글.elf'); assert 'CC NATIVE PASS' in Mäten and 'exit 0' in Mäten, Mäten
            assert 'CC NATIVE PASS' in тышча('cat cc.txt')
            실행파일 = bytearray(); файл_күчерү_тоташу.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            файл_күчерү_тоташу.storbinary('STOR экземпляр_VALUE.elf', io.BytesIO(실행파일)); Mäten = тышча('run экземпляр_VALUE.elf'); assert 'CC NATIVE PASS' in Mäten and 'exit 0' in Mäten, Mäten
            файл_күчерү_тоташу.storbinary('STOR үтәргә_команда', io.BytesIO(실행파일)); Mäten=тышча('./үтәргә_команда');assert 'CC NATIVE PASS' in Mäten and 'exit 0' in Mäten,Mäten
            файл_күчерү_тоташу.storbinary('STOR исем.txt', io.BytesIO(실행파일)); Mäten=тышча('./исем.txt');assert 'CC NATIVE PASS' in Mäten and 'exit 0' in Mäten,Mäten
            тышча('rm үтәргә_команда исем.txt')
            раслау_отчет['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            тышча('rm binary.dat 한글.txt 한글.c 한글.elf экземпляр_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(үлчәм_мәгълүмат/'linux-reference')
            файл_күчерү_тоташу.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Mäten=тышча('./리눅스인사');assert 'exit -8' in Mäten,Mäten
            Mäten=тышча('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Mäten,Mäten
            assert 'LINUX ELF FILE IO' in тышча('cat linux.txt')
            файл_күчерү_тоташу.delete('리눅스인사');файл_күчерү_тоташу.delete('linux.txt')
            файл_күчерү_тоташу.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in тышча('./FALSE_VALUE.elf');файл_күчерү_тоташу.delete('FALSE_VALUE.elf')
            раслау_отчет['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = үлчәм_мәгълүмат/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket ялгау = Татарча.자체.연결통신.ялгау("10.0.2.2", Integer.parseInt(args[0]));
 ялгау.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] чыганак = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<чыганак.length;i++) if (ялгау.getInputStream().read() != (чыганак[i]&255)) throw new RuntimeException("TCP mismatch");
 ялгау.close();
 DatagramSocket 종단 = Татарча.자체.통신.ачу(0); Татарча.자체.통신.КӨТҮВАКЫТЫЧЫГУ(종단, 500);
 Татарча.자체.통신.җибәрү(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Татарча.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(экранга_җибәрү_тамыр/'build/java-library/classes'),'-d',str(үлчәм_мәгълүмат),str(통신원문)])
                файл_күчерү_тоташу.storbinary('STOR 바깥통신.class', io.BytesIO((үлчәм_мәгълүмат/'바깥통신.class').read_bytes()))
                Mäten = тышча('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_протоколы_порт, 되돌림서버항목.UDP_порт))
                assert 'EXTERNAL TCP UDP PASS' in Mäten and '10.0.2.2' in Mäten and 'exit 0' in Mäten, Mäten
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            раслау_отчет['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            файл_күчерү_тоташу.delete('바깥통신.class')
            сервер_чыганак=үлчәм_мәгълүмат/'서버시험.java'
            сервер_чыганак.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket сервер_VALUE = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket кунак_VALUE = сервер_VALUE.accept();
  кунак_VALUE.getOutputStream().write(кунак_VALUE.getInputStream().read()+1); кунак_VALUE.close(); сервер_VALUE.close();
  byte[] Эчтәлек_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Эчтәлек_VALUE, Эчтәлек_VALUE.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(үлчәм_мәгълүмат),str(сервер_чыганак)])
            файл_күчерү_тоташу.storbinary('STOR 서버시험.class',io.BytesIO((үлчәм_мәгълүмат/'서버시험.class').read_bytes()))
            Процесс.stdin.write('java 서버시험\n'.encode());Процесс.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',сервер_агым_порт),timeout=5) as тиңдәш_VALUE:
                тиңдәш_VALUE.sendall(b'A');assert тиңдәш_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as тиңдәш_VALUE:
                тиңдәш_VALUE.settimeout(5);тиңдәш_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert тиңдәш_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Mäten=수신하기();assert 'INBOUND TCP UDP PASS' in Mäten and 'exit 0' in Mäten,Mäten
            раслау_отчет['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            файл_күчерү_тоташу.delete('서버시험.class')
            инструкция_SEQUENCE = 'public class 빛 { public static void main(String[] 인수) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } Татарча.자체.출력.수쓰기(SUM_VALUE); Татарча.자체.Birem.язу("aot.txt", "한글 AOT Birem 😀"); Татарча.자체.출력.язу_юл(Татарча.자체.Birem.읽기("aot.txt")); } }'
            файл_күчерү_тоташу.storbinary('STOR 빛.java', io.BytesIO(инструкция_SEQUENCE.encode()))
            Mäten = тышча('javac 빛.java'); assert 'exit 0' in Mäten and 'Compiled:' in Mäten, Mäten
            Mäten = тышча('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Mäten and 'exit 0' in Mäten, Mäten
            Mäten = тышча('run 빛.elf'); assert '\n55\n' in Mäten and '한글 AOT Birem 😀' in Mäten and 'exit 0' in Mäten, Mäten
            자체실행파일 = bytearray(); файл_күчерү_тоташу.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Mäten = тышча('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Mäten and 'unsupported' in Mäten, Mäten
            보존자료 = bytearray(); файл_күчерү_тоташу.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); файл_күчерү_тоташу.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            файл_күчерү_тоташу.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Mäten = тышча('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Mäten and 'exit 0' in Mäten, Mäten
            Mäten = тышча('run 빛.elf'); assert '\n55\n' in Mäten and '한글 AOT Birem 😀' in Mäten and 'exit 0' in Mäten, Mäten
            раслау_отчет['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            раслау_отчет['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            статик_чыганак=үлчәм_мәгълүмат/'정적시험.java'
            статик_чыганак.write_text('''public class 정적시험 {
 static int экранга_җибәрү_тамыр = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] 인수) {
  int[] VALUE = new int[] {экранга_җибәрү_тамыр, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(үлчәм_мәгълүмат),str(статик_чыганак)])
            файл_күчерү_тоташу.storbinary('STOR 정적시험.class',io.BytesIO((үлчәм_мәгълүмат/'정적시험.class').read_bytes()))
            Mäten=тышча('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Mäten,Mäten
            Mäten=тышча('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Mäten,Mäten
            файл_күчерү_тоташу.delete('정적시험.class');файл_күчерү_тоташу.delete('정적시험.elf')
            раслау_отчет['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Архив.getvalue());손상자료[14]^=1
            файл_күчерү_тоташу.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Mäten=тышча('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Mäten,Mäten
            раслау_отчет['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            файл_күчерү_тоташу.quit(); assert 'FTP stopped' in тышча('ftpd stop')
            assert not күпер.Хата, күпер.Хата
            раслау_отчет.update(passed=True, frames_to_guest=күпер.커널수신틀수, frames_from_guest=күпер.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in сайлагыч.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            күпер.туктатып_тору_вакыйга.set()
            Процесс.terminate()
            try: Процесс.wait(timeout=5)
            except subprocess.TimeoutExpired: Процесс.kill(); Процесс.wait()
            сайлагыч.close(); Процесс.stdin.close(); Процесс.stdout.close()
            раслау_отчет['bridge_error'] = күпер.Хата
            раслау_отчет['frames_to_guest'] = күпер.커널수신틀수; раслау_отчет['frames_from_guest'] = күпер.커널발신틀수
            (үлчәм_мәгълүмат/'packets.json').write_text(json.dumps(күпер.추적기록,indent=2)+'\n')
            (үлчәм_мәгълүмат / 'serial.log').write_bytes(대화기록)
            (үлчәм_мәгълүмат / 'report.json').write_text(json.dumps(раслау_отчет, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': эшләтү()
