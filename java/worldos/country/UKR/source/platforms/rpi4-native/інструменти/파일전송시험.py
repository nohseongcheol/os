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
from міст_3de4fe3a import міст_3de4fe3a
from Виконати_команда import Дії_корінь, команда
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def запустити():
    КР_дані = Дії_корінь / 'build/verification/ftp'; КР_дані.mkdir(parents=True, exist_ok=True)
    перевірка_звіт = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Дії_корінь / 'build/kernel8.img').read_bytes()).hexdigest()}
    транскрипт = bytearray()
    자바원문 = КР_дані / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] аргументи) throws Exception { українська.своє.Вивід.записування_рядок("JAR Виконати_команда: " + аргументи[0]); українська.своє.файл.Запис("jar.txt", "своє ядро_значення файл"); українська.своє.Вивід.записування_рядок(українська.своє.файл.Читання("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Дії_корінь/'build/java-library/classes'), '-d', str(КР_дані), str(자바원문)])
    Архів = io.BytesIO()
    with zipfile.ZipFile(Архів, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(КР_дані/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); номер_порту = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); сервер_потік_порт = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); сервер_дейтаграма_порт = 임시자원.getsockname()[1]
    with міст_3de4fe3a(номер_порту, ['tcp:{}:9300'.format(сервер_потік_порт), 'udp:{}:9301'.format(сервер_дейтаграма_порт)], записувати=True) as міст:
        Процеси = subprocess.Popen(команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + міст.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        селектор = selectors.DefaultSelector(); селектор.register(Процеси.stdout, selectors.EVENT_READ)
        def отримувати_повідомлення(маркер=b'jkoros-native> ', 시간제한=60):
            дані = bytearray(); завершити_виклик_Зміщена_копія = time.monotonic() + 시간제한
            while маркер not in дані:
                if time.monotonic() > завершити_виклик_Зміщена_копія or Процеси.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + дані.decode('utf-8', 'replace'))
                for 누름값, _ in селектор.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: дані.extend(조각); транскрипт.extend(조각)
                if b'PANIC:' in дані or b'FAIL ' in дані: raise AssertionError(дані)
            return дані.decode('utf-8', 'replace').replace('\r\n', '\n')
        def оболонка(рядок_введення):
            Процеси.stdin.write(рядок_введення.encode() + b'\n'); Процеси.stdin.flush(); return отримувати_повідомлення()
        try:
            отримувати_повідомлення(); assert 'FTP listening' in оболонка('ftpd start')
            передавання_файлу_зв_язок = ftplib.FTP(); передавання_файлу_зв_язок.encoding = 'utf-8'; передавання_файлу_зв_язок.connect('127.0.0.1', номер_порту, timeout=20); передавання_файлу_зв_язок.login()
            вміст_пакета_дані = bytes(range(256)) * 32
            передавання_файлу_зв_язок.storbinary('STOR binary.dat', io.BytesIO(вміст_пакета_дані))
            результат = bytearray(); передавання_файлу_зв_язок.retrbinary('RETR binary.dat', результат.extend)
            assert результат == вміст_пакета_дані; assert передавання_файлу_зв_язок.size('binary.dat') == len(вміст_пакета_дані)
            перевірка_звіт['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            передавання_файлу_зв_язок.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in оболонка('cat 한글.txt')
            assert '한글.txt' in передавання_файлу_зв_язок.nlst()
            assert dict(передавання_файлу_зв_язок.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            перевірка_звіт['checks'].append('UTF-8 filename and content visible in guest shell')
            try: передавання_файлу_зв_язок.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            результат = bytearray(); передавання_файлу_зв_язок.retrbinary('RETR binary.dat', результат.extend); assert результат == вміст_пакета_дані
            перевірка_звіт['checks'].append('oversized replacement rejected; previous file preserved')
            with передавання_файлу_зв_язок.transfercmd('STOR pending.txt') as передавати_Файли:
                # A control command must not change the active upload's destination.
                assert передавання_файлу_зв_язок.size('binary.dat') == len(вміст_пакета_дані)
                передавати_Файли.sendall(b'UPLOAD TARGET PRESERVED')
            assert передавання_файлу_зв_язок.voidresp().startswith('226')
            результат = bytearray(); передавання_файлу_зв_язок.retrbinary('RETR pending.txt', результат.extend)
            assert результат == b'UPLOAD TARGET PRESERVED'
            результат = bytearray(); передавання_файлу_зв_язок.retrbinary('RETR binary.dat', результат.extend)
            assert результат == вміст_пакета_дані
            передавання_файлу_зв_язок.delete('pending.txt')
            перевірка_звіт['checks'].append('interleaved SIZE cannot change the active STOR destination')
            передавання_файлу_зв_язок.storbinary('STOR 인사.jar', io.BytesIO(Архів.getvalue()))
            текст = оболонка('java -jar 인사.jar 누리')
            assert 'JAR Виконати_команда: 누리' in текст and 'своє ядро_значення файл' in текст and 'exit 0' in текст, текст
            текст = оболонка('./인사.jar 세상')
            assert 'JAR Виконати_команда: 세상' in текст and 'exit 0' in текст, текст
            перевірка_звіт['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct дані { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct дані значення = {합(10), 1.25}; if (значення.수 != 55 || значення.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = відкрито_Файл("cc.txt", 읽고쓰기 | 없으면만들기 | скорочувати_Зміст, 0600); if (문서 < 0) return 1; записування_Файл_дані(문서, 인사, sizeof(인사)-1); Закрити_Файл(문서); записування_Файл_дані(1, 인사, sizeof(인사)-1); return 0; }\n'
            передавання_файлу_зв_язок.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            текст = оболонка('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in текст and 'exit 0' in текст, текст
            текст = оболонка('run 한글.elf'); assert 'CC NATIVE PASS' in текст and 'exit 0' in текст, текст
            assert 'CC NATIVE PASS' in оболонка('cat cc.txt')
            실행파일 = bytearray(); передавання_файлу_зв_язок.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            передавання_файлу_зв_язок.storbinary('STOR екземпляр_значення.elf', io.BytesIO(실행파일)); текст = оболонка('run екземпляр_значення.elf'); assert 'CC NATIVE PASS' in текст and 'exit 0' in текст, текст
            передавання_файлу_зв_язок.storbinary('STOR Виконати_команда', io.BytesIO(실행파일)); текст=оболонка('./Виконати_команда');assert 'CC NATIVE PASS' in текст and 'exit 0' in текст,текст
            передавання_файлу_зв_язок.storbinary('STOR Назва.txt', io.BytesIO(실행파일)); текст=оболонка('./Назва.txt');assert 'CC NATIVE PASS' in текст and 'exit 0' in текст,текст
            оболонка('rm Виконати_команда Назва.txt')
            перевірка_звіт['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            оболонка('rm binary.dat 한글.txt 한글.c 한글.elf екземпляр_значення.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(КР_дані/'linux-reference')
            передавання_файлу_зв_язок.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            текст=оболонка('./리눅스인사');assert 'exit -8' in текст,текст
            текст=оболонка('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in текст,текст
            assert 'LINUX ELF FILE IO' in оболонка('cat linux.txt')
            передавання_файлу_зв_язок.delete('리눅스인사');передавання_файлу_зв_язок.delete('linux.txt')
            передавання_файлу_зв_язок.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in оболонка('./거짓.elf');передавання_файлу_зв_язок.delete('거짓.elf')
            перевірка_звіт['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as відлуння_сервер_запис:
                통신원문 = КР_дані/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket З_єднання = українська.своє.연결통신.З_єднання("10.0.2.2", Integer.parseInt(args[0]));
 З_єднання.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] вихіднийКод = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<вихіднийКод.length;i++) if (З_єднання.getInputStream().read() != (вихіднийКод[i]&255)) throw new RuntimeException("TCP mismatch");
 З_єднання.close();
 DatagramSocket учасник = українська.своє.통신.Відкрити(0); українська.своє.통신.대기시간(учасник, 500);
 українська.своє.통신.надсилати(учасник, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!українська.своє.통신.отримувати(учасник).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 учасник.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Дії_корінь/'build/java-library/classes'),'-d',str(КР_дані),str(통신원문)])
                передавання_файлу_зв_язок.storbinary('STOR 바깥통신.class', io.BytesIO((КР_дані/'바깥통신.class').read_bytes()))
                текст = оболонка('java 바깥통신 {} {}'.format(відлуння_сервер_запис.протокол_керування_передаванням_порт, відлуння_сервер_запис.протокол_користувацьких_дейтаграм_порт))
                assert 'EXTERNAL TCP UDP PASS' in текст and '10.0.2.2' in текст and 'exit 0' in текст, текст
                assert відлуння_сервер_запис.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, відлуння_сервер_запис.수신됨
                assert not відлуння_сервер_запис.오류들, відлуння_сервер_запис.오류들
            перевірка_звіт['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            передавання_файлу_зв_язок.delete('바깥통신.class')
            сервер_джерело=КР_дані/'서버시험.java'
            сервер_джерело.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket сервер_значення = new ServerSocket(9300); DatagramSocket учасник = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket гість_значення = сервер_значення.accept();
  гість_значення.getOutputStream().write(гість_значення.getInputStream().read()+1); гість_значення.close(); сервер_значення.close();
  byte[] Вміст_значення = new byte[8]; DatagramPacket дейтаграма = new DatagramPacket(Вміст_значення, Вміст_значення.length); учасник.receive(дейтаграма);
  учасник.send(дейтаграма); учасник.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(КР_дані),str(сервер_джерело)])
            передавання_файлу_зв_язок.storbinary('STOR 서버시험.class',io.BytesIO((КР_дані/'서버시험.class').read_bytes()))
            Процеси.stdin.write('java 서버시험\n'.encode());Процеси.stdin.flush();отримувати_повідомлення(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',сервер_потік_порт),timeout=5) as точка_значення:
                точка_значення.sendall(b'A');assert точка_значення.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as точка_значення:
                точка_значення.settimeout(5);точка_значення.sendto(b'UDP-IN',('127.0.0.1',сервер_дейтаграма_порт));assert точка_значення.recvfrom(512)[0]==b'UDP-IN'
            текст=отримувати_повідомлення();assert 'INBOUND TCP UDP PASS' in текст and 'exit 0' in текст,текст
            перевірка_звіт['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            передавання_файлу_зв_язок.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] аргументи) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } українська.своє.Вивід.수쓰기(합); українська.своє.файл.Запис("aot.txt", "한글 AOT файл 😀"); українська.своє.Вивід.записування_рядок(українська.своє.файл.Читання("aot.txt")); } }'
            передавання_файлу_зв_язок.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            текст = оболонка('javac 빛.java'); assert 'exit 0' in текст and 'Compiled:' in текст, текст
            текст = оболонка('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in текст and 'exit 0' in текст, текст
            текст = оболонка('run 빛.elf'); assert '\n55\n' in текст and '한글 AOT файл 😀' in текст and 'exit 0' in текст, текст
            자체실행파일 = bytearray(); передавання_файлу_зв_язок.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            текст = оболонка('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in текст and 'unsupported' in текст, текст
            보존자료 = bytearray(); передавання_файлу_зв_язок.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); передавання_файлу_зв_язок.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            передавання_файлу_зв_язок.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            текст = оболонка('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in текст and 'exit 0' in текст, текст
            текст = оболонка('run 빛.elf'); assert '\n55\n' in текст and '한글 AOT файл 😀' in текст and 'exit 0' in текст, текст
            перевірка_звіт['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            перевірка_звіт['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            정적원문=КР_дані/'정적시험.java'
            정적원문.write_text('''public class 정적시험 {
 static int Дії_корінь = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] аргументи) {
  int[] значення = new int[] {Дії_корінь, 합(10)};
  System.out.println(значення[0] + значення[1]); System.out.println(аргументи[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(КР_дані),str(정적원문)])
            передавання_файлу_зв_язок.storbinary('STOR 정적시험.class',io.BytesIO((КР_дані/'정적시험.class').read_bytes()))
            текст=оболонка('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in текст,текст
            текст=оболонка('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in текст,текст
            передавання_файлу_зв_язок.delete('정적시험.class');передавання_файлу_зв_язок.delete('정적시험.elf')
            перевірка_звіт['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Архів.getvalue());손상자료[14]^=1
            передавання_файлу_зв_язок.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            текст=оболонка('java -jar 인사.jar');assert 'Main-Class\nexit 1' in текст,текст
            перевірка_звіт['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            передавання_файлу_зв_язок.quit(); assert 'FTP stopped' in оболонка('ftpd stop')
            assert not міст.ПОМИЛКА, міст.ПОМИЛКА
            перевірка_звіт.update(passed=True, frames_to_guest=міст.커널수신틀수, frames_from_guest=міст.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in селектор.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: транскрипт.extend(조각)
            міст.Пауза_подія.set()
            Процеси.terminate()
            try: Процеси.wait(timeout=5)
            except subprocess.TimeoutExpired: Процеси.kill(); Процеси.wait()
            селектор.close(); Процеси.stdin.close(); Процеси.stdout.close()
            перевірка_звіт['bridge_error'] = міст.ПОМИЛКА
            перевірка_звіт['frames_to_guest'] = міст.커널수신틀수; перевірка_звіт['frames_from_guest'] = міст.커널발신틀수
            (КР_дані/'packets.json').write_text(json.dumps(міст.журнал_трасування,indent=2)+'\n')
            (КР_дані / 'serial.log').write_bytes(транскрипт)
            (КР_дані / 'report.json').write_text(json.dumps(перевірка_звіт, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': запустити()
