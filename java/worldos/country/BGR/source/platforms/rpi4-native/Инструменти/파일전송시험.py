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
from мост_3de4fe3a import мост_3de4fe3a
from изпълнявам_команда import проект_корен, Команда
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Стартиране():
    мярка_данни = проект_корен / 'build/verification/ftp'; мярка_данни.mkdir(parents=True, exist_ok=True)
    проверка_отчет = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((проект_корен / 'build/kernel8.img').read_bytes()).hexdigest()}
    препис = bytearray()
    자바원문 = мярка_данни / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Параметри) throws Exception { Български.자체.Изход.записване_ред("JAR изпълнявам_команда: " + Параметри[0]); Български.자체.Файл.Писане("jar.txt", "자체 ядро_стойност Файл"); Български.자체.Изход.записване_ред(Български.자체.Файл.Четене("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(проект_корен/'build/java-library/classes'), '-d', str(мярка_данни), str(자바원문)])
    Архив = io.BytesIO()
    with zipfile.ZipFile(Архив, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(мярка_данни/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); номер_на_порт = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); сървър_поток_порт = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); сървър_дейтаграма_порт = 임시자원.getsockname()[1]
    with мост_3de4fe3a(номер_на_порт, ['tcp:{}:9300'.format(сървър_поток_порт), 'udp:{}:9301'.format(сървър_дейтаграма_порт)], заснемам=True) as мост:
        Процес = subprocess.Popen(Команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + мост.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        свързан_елемент_за_избор = selectors.DefaultSelector(); свързан_елемент_за_избор.register(Процес.stdout, selectors.EVENT_READ)
        def получавам_имейл(маркер=b'jkoros-native> ', 시간제한=60):
            данни = bytearray(); прекратяване_на_повикването_Изместване = time.monotonic() + 시간제한
            while маркер not in данни:
                if time.monotonic() > прекратяване_на_повикването_Изместване or Процес.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + данни.decode('utf-8', 'replace'))
                for 누름값, _ in свързан_елемент_за_избор.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: данни.extend(조각); препис.extend(조각)
                if b'PANIC:' in данни or b'FAIL ' in данни: raise AssertionError(данни)
            return данни.decode('utf-8', 'replace').replace('\r\n', '\n')
        def обвивка(ред):
            Процес.stdin.write(ред.encode() + b'\n'); Процес.stdin.flush(); return получавам_имейл()
        try:
            получавам_имейл(); assert 'FTP listening' in обвивка('ftpd start')
            прехвърляне_на_файл_връзка = ftplib.FTP(); прехвърляне_на_файл_връзка.encoding = 'utf-8'; прехвърляне_на_файл_връзка.connect('127.0.0.1', номер_на_порт, timeout=20); прехвърляне_на_файл_връзка.login()
            полезен_обем_данни = bytes(range(256)) * 32
            прехвърляне_на_файл_връзка.storbinary('STOR binary.dat', io.BytesIO(полезен_обем_данни))
            РЕЗУЛТАТ = bytearray(); прехвърляне_на_файл_връзка.retrbinary('RETR binary.dat', РЕЗУЛТАТ.extend)
            assert РЕЗУЛТАТ == полезен_обем_данни; assert прехвърляне_на_файл_връзка.size('binary.dat') == len(полезен_обем_данни)
            проверка_отчет['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            прехвърляне_на_файл_връзка.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in обвивка('cat 한글.txt')
            assert '한글.txt' in прехвърляне_на_файл_връзка.nlst()
            assert dict(прехвърляне_на_файл_връзка.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            проверка_отчет['checks'].append('UTF-8 filename and content visible in guest shell')
            try: прехвърляне_на_файл_връзка.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            РЕЗУЛТАТ = bytearray(); прехвърляне_на_файл_връзка.retrbinary('RETR binary.dat', РЕЗУЛТАТ.extend); assert РЕЗУЛТАТ == полезен_обем_данни
            проверка_отчет['checks'].append('oversized replacement rejected; previous file preserved')
            with прехвърляне_на_файл_връзка.transfercmd('STOR pending.txt') as качвам_Файлове:
                # A control command must not change the active upload's destination.
                assert прехвърляне_на_файл_връзка.size('binary.dat') == len(полезен_обем_данни)
                качвам_Файлове.sendall(b'UPLOAD TARGET PRESERVED')
            assert прехвърляне_на_файл_връзка.voidresp().startswith('226')
            РЕЗУЛТАТ = bytearray(); прехвърляне_на_файл_връзка.retrbinary('RETR pending.txt', РЕЗУЛТАТ.extend)
            assert РЕЗУЛТАТ == b'UPLOAD TARGET PRESERVED'
            РЕЗУЛТАТ = bytearray(); прехвърляне_на_файл_връзка.retrbinary('RETR binary.dat', РЕЗУЛТАТ.extend)
            assert РЕЗУЛТАТ == полезен_обем_данни
            прехвърляне_на_файл_връзка.delete('pending.txt')
            проверка_отчет['checks'].append('interleaved SIZE cannot change the active STOR destination')
            прехвърляне_на_файл_връзка.storbinary('STOR 인사.jar', io.BytesIO(Архив.getvalue()))
            Текст = обвивка('java -jar 인사.jar 누리')
            assert 'JAR изпълнявам_команда: 누리' in Текст and '자체 ядро_стойност Файл' in Текст and 'exit 0' in Текст, Текст
            Текст = обвивка('./인사.jar 세상')
            assert 'JAR изпълнявам_команда: 세상' in Текст and 'exit 0' in Текст, Текст
            проверка_отчет['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct данни { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct данни стойност = {합(10), 1.25}; if (стойност.수 != 55 || стойност.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = отварям_Файл("cc.txt", 읽고쓰기 | 없으면만들기 | съкращавам_Съдържание, 0600); if (문서 < 0) return 1; записване_Файл_данни(문서, 인사, sizeof(인사)-1); затварям_Файл(문서); записване_Файл_данни(1, 인사, sizeof(인사)-1); return 0; }\n'
            прехвърляне_на_файл_връзка.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Текст = обвивка('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Текст and 'exit 0' in Текст, Текст
            Текст = обвивка('run 한글.elf'); assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст, Текст
            assert 'CC NATIVE PASS' in обвивка('cat cc.txt')
            실행파일 = bytearray(); прехвърляне_на_файл_връзка.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            прехвърляне_на_файл_връзка.storbinary('STOR копирам_стойност.elf', io.BytesIO(실행파일)); Текст = обвивка('run копирам_стойност.elf'); assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст, Текст
            прехвърляне_на_файл_връзка.storbinary('STOR изпълнявам_команда', io.BytesIO(실행파일)); Текст=обвивка('./изпълнявам_команда');assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст,Текст
            прехвърляне_на_файл_връзка.storbinary('STOR Име.txt', io.BytesIO(실행파일)); Текст=обвивка('./Име.txt');assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст,Текст
            обвивка('rm изпълнявам_команда Име.txt')
            проверка_отчет['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            обвивка('rm binary.dat 한글.txt 한글.c 한글.elf копирам_стойност.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(мярка_данни/'linux-reference')
            прехвърляне_на_файл_връзка.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Текст=обвивка('./리눅스인사');assert 'exit -8' in Текст,Текст
            Текст=обвивка('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Текст,Текст
            assert 'LINUX ELF FILE IO' in обвивка('cat linux.txt')
            прехвърляне_на_файл_връзка.delete('리눅스인사');прехвърляне_на_файл_връзка.delete('linux.txt')
            прехвърляне_на_файл_връзка.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in обвивка('./거짓.elf');прехвърляне_на_файл_връзка.delete('거짓.elf')
            проверка_отчет['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as Ехо_сървър_запис:
                통신원문 = мярка_данни/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Свързване = Български.자체.연결통신.Свързване("10.0.2.2", Integer.parseInt(args[0]));
 Свързване.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ИЗТОЧНИК = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ИЗТОЧНИК.length;i++) if (Свързване.getInputStream().read() != (ИЗТОЧНИК[i]&255)) throw new RuntimeException("TCP mismatch");
 Свързване.close();
 DatagramSocket участник = Български.자체.통신.Отваряне(0); Български.자체.통신.време_на_изчакване(участник, 500);
 Български.자체.통신.изпращам(участник, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Български.자체.통신.получавам(участник).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 участник.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(проект_корен/'build/java-library/classes'),'-d',str(мярка_данни),str(통신원문)])
                прехвърляне_на_файл_връзка.storbinary('STOR 바깥통신.class', io.BytesIO((мярка_данни/'바깥통신.class').read_bytes()))
                Текст = обвивка('java 바깥통신 {} {}'.format(Ехо_сървър_запис.연결접속번호, Ехо_сървър_запис.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in Текст and '10.0.2.2' in Текст and 'exit 0' in Текст, Текст
                assert Ехо_сървър_запис.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, Ехо_сървър_запис.수신됨
                assert not Ехо_сървър_запис.오류들, Ехо_сървър_запис.오류들
            проверка_отчет['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            прехвърляне_на_файл_връзка.delete('바깥통신.class')
            сървър_източник=мярка_данни/'서버시험.java'
            сървър_източник.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket сървър_стойност = new ServerSocket(9300); DatagramSocket участник = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket гост_стойност = сървър_стойност.accept();
  гост_стойност.getOutputStream().write(гост_стойност.getInputStream().read()+1); гост_стойност.close(); сървър_стойност.close();
  byte[] Съдържание_стойност = new byte[8]; DatagramPacket дейтаграма = new DatagramPacket(Съдържание_стойност, Съдържание_стойност.length); участник.receive(дейтаграма);
  участник.send(дейтаграма); участник.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(мярка_данни),str(сървър_източник)])
            прехвърляне_на_файл_връзка.storbinary('STOR 서버시험.class',io.BytesIO((мярка_данни/'서버시험.class').read_bytes()))
            Процес.stdin.write('java 서버시험\n'.encode());Процес.stdin.flush();получавам_имейл(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',сървър_поток_порт),timeout=5) as крайно_устройство_стойност:
                крайно_устройство_стойност.sendall(b'A');assert крайно_устройство_стойност.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as крайно_устройство_стойност:
                крайно_устройство_стойност.settimeout(5);крайно_устройство_стойност.sendto(b'UDP-IN',('127.0.0.1',сървър_дейтаграма_порт));assert крайно_устройство_стойност.recvfrom(512)[0]==b'UDP-IN'
            Текст=получавам_имейл();assert 'INBOUND TCP UDP PASS' in Текст and 'exit 0' in Текст,Текст
            проверка_отчет['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            прехвърляне_на_файл_връзка.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] Параметри) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } Български.자체.Изход.수쓰기(합); Български.자체.Файл.Писане("aot.txt", "한글 AOT Файл 😀"); Български.자체.Изход.записване_ред(Български.자체.Файл.Четене("aot.txt")); } }'
            прехвърляне_на_файл_връзка.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            Текст = обвивка('javac 빛.java'); assert 'exit 0' in Текст and 'Compiled:' in Текст, Текст
            Текст = обвивка('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Текст and 'exit 0' in Текст, Текст
            Текст = обвивка('run 빛.elf'); assert '\n55\n' in Текст and '한글 AOT Файл 😀' in Текст and 'exit 0' in Текст, Текст
            자체실행파일 = bytearray(); прехвърляне_на_файл_връзка.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Текст = обвивка('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Текст and 'unsupported' in Текст, Текст
            보존자료 = bytearray(); прехвърляне_на_файл_връзка.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); прехвърляне_на_файл_връзка.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            прехвърляне_на_файл_връзка.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Текст = обвивка('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Текст and 'exit 0' in Текст, Текст
            Текст = обвивка('run 빛.elf'); assert '\n55\n' in Текст and '한글 AOT Файл 😀' in Текст and 'exit 0' in Текст, Текст
            проверка_отчет['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            проверка_отчет['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            정적원문=мярка_данни/'정적시험.java'
            정적원문.write_text('''public class 정적시험 {
 static int проект_корен = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] Параметри) {
  int[] стойност = new int[] {проект_корен, 합(10)};
  System.out.println(стойност[0] + стойност[1]); System.out.println(Параметри[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(мярка_данни),str(정적원문)])
            прехвърляне_на_файл_връзка.storbinary('STOR 정적시험.class',io.BytesIO((мярка_данни/'정적시험.class').read_bytes()))
            Текст=обвивка('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Текст,Текст
            Текст=обвивка('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Текст,Текст
            прехвърляне_на_файл_връзка.delete('정적시험.class');прехвърляне_на_файл_връзка.delete('정적시험.elf')
            проверка_отчет['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Архив.getvalue());손상자료[14]^=1
            прехвърляне_на_файл_връзка.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Текст=обвивка('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Текст,Текст
            проверка_отчет['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            прехвърляне_на_файл_връзка.quit(); assert 'FTP stopped' in обвивка('ftpd stop')
            assert not мост.ГРЕШКА, мост.ГРЕШКА
            проверка_отчет.update(passed=True, frames_to_guest=мост.커널수신틀수, frames_from_guest=мост.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in свързан_елемент_за_избор.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: препис.extend(조각)
            мост.Пауза_събитие.set()
            Процес.terminate()
            try: Процес.wait(timeout=5)
            except subprocess.TimeoutExpired: Процес.kill(); Процес.wait()
            свързан_елемент_за_избор.close(); Процес.stdin.close(); Процес.stdout.close()
            проверка_отчет['bridge_error'] = мост.ГРЕШКА
            проверка_отчет['frames_to_guest'] = мост.커널수신틀수; проверка_отчет['frames_from_guest'] = мост.커널발신틀수
            (мярка_данни/'packets.json').write_text(json.dumps(мост.регистрационен_файл_за_проследяванията,indent=2)+'\n')
            (мярка_данни / 'serial.log').write_bytes(препис)
            (мярка_данни / 'report.json').write_text(json.dumps(проверка_отчет, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Стартиране()
