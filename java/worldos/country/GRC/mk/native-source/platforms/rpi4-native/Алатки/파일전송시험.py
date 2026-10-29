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
from Мрежа_мост import Мрежа_мост
from Изврши_наредба import Project_корен, Команда
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Изврши_2():
    мерка_податоци = Project_корен / 'build/verification/ftp'; мерка_податоци.mkdir(parents=True, exist_ok=True)
    проверка_извештај = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Project_корен / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = мерка_податоци / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Аргументи) throws Exception { Македонски.자체.출력.запиши_ред("JAR Изврши_наредба: " + Аргументи[0]); Македонски.자체.Датотека.Запиши("jar.txt", "자체 јадро_VALUE Датотека"); Македонски.자체.출력.запиши_ред(Македонски.자체.Датотека.Читај("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_корен/'build/java-library/classes'), '-d', str(мерка_податоци), str(자바원문)])
    Архива = io.BytesIO()
    with zipfile.ZipFile(Архива, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(мерка_податоци/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); број_на_порта = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); сервер_Stream_порта = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Мрежа_мост(број_на_порта, ['tcp:{}:9300'.format(сервер_Stream_порта), 'udp:{}:9301'.format(서버전문접속번호)], зафати=True) as мост:
        Процес = subprocess.Popen(Команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + мост.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        избирач = selectors.DefaultSelector(); избирач.register(Процес.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            податоци = bytearray(); крај_OFFSET = time.monotonic() + 시간제한
            while 확인표시 not in податоци:
                if time.monotonic() > крај_OFFSET or Процес.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + податоци.decode('utf-8', 'replace'))
                for 누름값, _ in избирач.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: податоци.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in податоци or b'FAIL ' in податоци: raise AssertionError(податоци)
            return податоци.decode('utf-8', 'replace').replace('\r\n', '\n')
        def обвивка(ред):
            Процес.stdin.write(ред.encode() + b'\n'); Процес.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in обвивка('ftpd start')
            датотека_пренос_врска = ftplib.FTP(); датотека_пренос_врска.encoding = 'utf-8'; датотека_пренос_врска.connect('127.0.0.1', број_на_порта, timeout=20); датотека_пренос_врска.login()
            капацитет_податоци = bytes(range(256)) * 32
            датотека_пренос_врска.storbinary('STOR binary.dat', io.BytesIO(капацитет_податоци))
            мерка = bytearray(); датотека_пренос_врска.retrbinary('RETR binary.dat', мерка.extend)
            assert мерка == капацитет_податоци; assert датотека_пренос_врска.size('binary.dat') == len(капацитет_податоци)
            проверка_извештај['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            датотека_пренос_врска.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in обвивка('cat 한글.txt')
            assert '한글.txt' in датотека_пренос_врска.nlst()
            assert dict(датотека_пренос_врска.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            проверка_извештај['checks'].append('UTF-8 filename and content visible in guest shell')
            try: датотека_пренос_врска.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            мерка = bytearray(); датотека_пренос_врска.retrbinary('RETR binary.dat', мерка.extend); assert мерка == капацитет_податоци
            проверка_извештај['checks'].append('oversized replacement rejected; previous file preserved')
            with датотека_пренос_врска.transfercmd('STOR pending.txt') as постави_Датотеки:
                # A control command must not change the active upload's destination.
                assert датотека_пренос_врска.size('binary.dat') == len(капацитет_податоци)
                постави_Датотеки.sendall(b'UPLOAD TARGET PRESERVED')
            assert датотека_пренос_врска.voidresp().startswith('226')
            мерка = bytearray(); датотека_пренос_врска.retrbinary('RETR pending.txt', мерка.extend)
            assert мерка == b'UPLOAD TARGET PRESERVED'
            мерка = bytearray(); датотека_пренос_врска.retrbinary('RETR binary.dat', мерка.extend)
            assert мерка == капацитет_податоци
            датотека_пренос_врска.delete('pending.txt')
            проверка_извештај['checks'].append('interleaved SIZE cannot change the active STOR destination')
            датотека_пренос_врска.storbinary('STOR 인사.jar', io.BytesIO(Архива.getvalue()))
            Текст = обвивка('java -jar 인사.jar 누리')
            assert 'JAR Изврши_наредба: 누리' in Текст and '자체 јадро_VALUE Датотека' in Текст and 'exit 0' in Текст, Текст
            Текст = обвивка('./인사.jar 세상')
            assert 'JAR Изврши_наредба: 세상' in Текст and 'exit 0' in Текст, Текст
            проверка_извештај['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct податоци { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct податоци VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = отвори_датотека("cc.txt", чита_пишува | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; запиши_датотека_податоци(문서, 인사, sizeof(인사)-1); затвори_датотека(문서); запиши_датотека_податоци(1, 인사, sizeof(인사)-1); return 0; }\n'
            датотека_пренос_врска.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Текст = обвивка('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Текст and 'exit 0' in Текст, Текст
            Текст = обвивка('run 한글.elf'); assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст, Текст
            assert 'CC NATIVE PASS' in обвивка('cat cc.txt')
            실행파일 = bytearray(); датотека_пренос_врска.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            датотека_пренос_врска.storbinary('STOR копирај_VALUE.elf', io.BytesIO(실행파일)); Текст = обвивка('run копирај_VALUE.elf'); assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст, Текст
            датотека_пренос_врска.storbinary('STOR Изврши_наредба', io.BytesIO(실행파일)); Текст=обвивка('./Изврши_наредба');assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст,Текст
            датотека_пренос_врска.storbinary('STOR Име.txt', io.BytesIO(실행파일)); Текст=обвивка('./Име.txt');assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст,Текст
            обвивка('rm Изврши_наредба Име.txt')
            проверка_извештај['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            обвивка('rm binary.dat 한글.txt 한글.c 한글.elf копирај_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(мерка_податоци/'linux-reference')
            датотека_пренос_врска.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Текст=обвивка('./리눅스인사');assert 'exit -8' in Текст,Текст
            Текст=обвивка('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Текст,Текст
            assert 'LINUX ELF FILE IO' in обвивка('cat linux.txt')
            датотека_пренос_врска.delete('리눅스인사');датотека_пренос_врска.delete('linux.txt')
            датотека_пренос_врска.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in обвивка('./FALSE_VALUE.elf');датотека_пренос_врска.delete('FALSE_VALUE.elf')
            проверка_извештај['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = мерка_податоци/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Врзи_се = Македонски.자체.연결통신.Врзи_се("10.0.2.2", Integer.parseInt(args[0]));
 Врзи_се.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ИЗВОР = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ИЗВОР.length;i++) if (Врзи_се.getInputStream().read() != (ИЗВОР[i]&255)) throw new RuntimeException("TCP mismatch");
 Врзи_се.close();
 DatagramSocket 종단 = Македонски.자체.통신.Отвори(0); Македонски.자체.통신.TIMEOUT(종단, 500);
 Македонски.자체.통신.испрати(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Македонски.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_корен/'build/java-library/classes'),'-d',str(мерка_податоци),str(통신원문)])
                датотека_пренос_врска.storbinary('STOR 바깥통신.class', io.BytesIO((мерка_податоци/'바깥통신.class').read_bytes()))
                Текст = обвивка('java 바깥통신 {} {}'.format(되돌림서버항목.ТЦП_порта, 되돌림서버항목.УДП_порта))
                assert 'EXTERNAL TCP UDP PASS' in Текст and '10.0.2.2' in Текст and 'exit 0' in Текст, Текст
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            проверка_извештај['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            датотека_пренос_врска.delete('바깥통신.class')
            сервер_извор=мерка_податоци/'서버시험.java'
            сервер_извор.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket сервер_VALUE = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket гостин_VALUE = сервер_VALUE.accept();
  гостин_VALUE.getOutputStream().write(гостин_VALUE.getInputStream().read()+1); гостин_VALUE.close(); сервер_VALUE.close();
  byte[] Содржина_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Содржина_VALUE, Содржина_VALUE.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(мерка_податоци),str(сервер_извор)])
            датотека_пренос_врска.storbinary('STOR 서버시험.class',io.BytesIO((мерка_податоци/'서버시험.class').read_bytes()))
            Процес.stdin.write('java 서버시험\n'.encode());Процес.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',сервер_Stream_порта),timeout=5) as рамноправен_уред_VALUE:
                рамноправен_уред_VALUE.sendall(b'A');assert рамноправен_уред_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as рамноправен_уред_VALUE:
                рамноправен_уред_VALUE.settimeout(5);рамноправен_уред_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert рамноправен_уред_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Текст=수신하기();assert 'INBOUND TCP UDP PASS' in Текст and 'exit 0' in Текст,Текст
            проверка_извештај['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            датотека_пренос_врска.delete('서버시험.class')
            инструкција_SEQUENCE = 'public class 빛 { public static void main(String[] Аргументи) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } Македонски.자체.출력.수쓰기(SUM_VALUE); Македонски.자체.Датотека.Запиши("aot.txt", "한글 AOT Датотека 😀"); Македонски.자체.출력.запиши_ред(Македонски.자체.Датотека.Читај("aot.txt")); } }'
            датотека_пренос_врска.storbinary('STOR 빛.java', io.BytesIO(инструкција_SEQUENCE.encode()))
            Текст = обвивка('javac 빛.java'); assert 'exit 0' in Текст and 'Compiled:' in Текст, Текст
            Текст = обвивка('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Текст and 'exit 0' in Текст, Текст
            Текст = обвивка('run 빛.elf'); assert '\n55\n' in Текст and '한글 AOT Датотека 😀' in Текст and 'exit 0' in Текст, Текст
            자체실행파일 = bytearray(); датотека_пренос_врска.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Текст = обвивка('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Текст and 'unsupported' in Текст, Текст
            보존자료 = bytearray(); датотека_пренос_врска.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); датотека_пренос_врска.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            датотека_пренос_врска.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Текст = обвивка('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Текст and 'exit 0' in Текст, Текст
            Текст = обвивка('run 빛.elf'); assert '\n55\n' in Текст and '한글 AOT Датотека 😀' in Текст and 'exit 0' in Текст, Текст
            проверка_извештај['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            проверка_извештај['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            статичен_извор=мерка_податоци/'정적시험.java'
            статичен_извор.write_text('''public class 정적시험 {
 static int Project_корен = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] Аргументи) {
  int[] VALUE = new int[] {Project_корен, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(Аргументи[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(мерка_податоци),str(статичен_извор)])
            датотека_пренос_врска.storbinary('STOR 정적시험.class',io.BytesIO((мерка_податоци/'정적시험.class').read_bytes()))
            Текст=обвивка('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Текст,Текст
            Текст=обвивка('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Текст,Текст
            датотека_пренос_врска.delete('정적시험.class');датотека_пренос_врска.delete('정적시험.elf')
            проверка_извештај['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Архива.getvalue());손상자료[14]^=1
            датотека_пренос_врска.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Текст=обвивка('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Текст,Текст
            проверка_извештај['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            датотека_пренос_врска.quit(); assert 'FTP stopped' in обвивка('ftpd stop')
            assert not мост.ГРЕШКА, мост.ГРЕШКА
            проверка_извештај.update(passed=True, frames_to_guest=мост.커널수신틀수, frames_from_guest=мост.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in избирач.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            мост.пауза_настан.set()
            Процес.terminate()
            try: Процес.wait(timeout=5)
            except subprocess.TimeoutExpired: Процес.kill(); Процес.wait()
            избирач.close(); Процес.stdin.close(); Процес.stdout.close()
            проверка_извештај['bridge_error'] = мост.ГРЕШКА
            проверка_извештај['frames_to_guest'] = мост.커널수신틀수; проверка_извештај['frames_from_guest'] = мост.커널발신틀수
            (мерка_податоци/'packets.json').write_text(json.dumps(мост.трага_LOG,indent=2)+'\n')
            (мерка_податоци / 'serial.log').write_bytes(대화기록)
            (мерка_податоци / 'report.json').write_text(json.dumps(проверка_извештај, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Изврши_2()
