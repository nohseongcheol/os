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
from Изврши_команда import пројектовати_корен, Наредба
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Покрени():
    мера_подаци = пројектовати_корен / 'build/verification/ftp'; мера_подаци.mkdir(parents=True, exist_ok=True)
    провјера_извештај = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((пројектовати_корен / 'build/kernel8.img').read_bytes()).hexdigest()}
    транскрипт = bytearray()
    자바원문 = мера_подаци / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Аргументи) throws Exception { 한국어.자체.Излаз.писати_редак("JAR Изврши_команда: " + Аргументи[0]); 한국어.자체.Датотека.Пише("jar.txt", "자체 језгро_вриједност Датотека"); 한국어.자체.Излаз.писати_редак(한국어.자체.Датотека.Чита("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(пројектовати_корен/'build/java-library/classes'), '-d', str(мера_подаци), str(자바원문)])
    Архива = io.BytesIO()
    with zipfile.ZipFile(Архива, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(мера_подаци/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); број_порта = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); сервер_ток_порт = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Мрежа_мост(број_порта, ['tcp:{}:9300'.format(сервер_ток_порт), 'udp:{}:9301'.format(서버전문접속번호)], снимити=True) as мост:
        Процес = subprocess.Popen(Наредба() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + мост.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        бирач = selectors.DefaultSelector(); бирач.register(Процес.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            подаци = bytearray(); завршити_Помак = time.monotonic() + 시간제한
            while 확인표시 not in подаци:
                if time.monotonic() > завршити_Помак or Процес.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + подаци.decode('utf-8', 'replace'))
                for 누름값, _ in бирач.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: подаци.extend(조각); транскрипт.extend(조각)
                if b'PANIC:' in подаци or b'FAIL ' in подаци: raise AssertionError(подаци)
            return подаци.decode('utf-8', 'replace').replace('\r\n', '\n')
        def љуска(Ред):
            Процес.stdin.write(Ред.encode() + b'\n'); Процес.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in љуска('ftpd start')
            фајл_пренос_веза = ftplib.FTP(); фајл_пренос_веза.encoding = 'utf-8'; фајл_пренос_веза.connect('127.0.0.1', број_порта, timeout=20); фајл_пренос_веза.login()
            корисни_подаци_подаци = bytes(range(256)) * 32
            фајл_пренос_веза.storbinary('STOR binary.dat', io.BytesIO(корисни_подаци_подаци))
            ИСХОД = bytearray(); фајл_пренос_веза.retrbinary('RETR binary.dat', ИСХОД.extend)
            assert ИСХОД == корисни_подаци_подаци; assert фајл_пренос_веза.size('binary.dat') == len(корисни_подаци_подаци)
            провјера_извештај['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            фајл_пренос_веза.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in љуска('cat 한글.txt')
            assert '한글.txt' in фајл_пренос_веза.nlst()
            assert dict(фајл_пренос_веза.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            провјера_извештај['checks'].append('UTF-8 filename and content visible in guest shell')
            try: фајл_пренос_веза.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            ИСХОД = bytearray(); фајл_пренос_веза.retrbinary('RETR binary.dat', ИСХОД.extend); assert ИСХОД == корисни_подаци_подаци
            провјера_извештај['checks'].append('oversized replacement rejected; previous file preserved')
            with фајл_пренос_веза.transfercmd('STOR pending.txt') as Отпрема_Фајлови:
                # A control command must not change the active upload's destination.
                assert фајл_пренос_веза.size('binary.dat') == len(корисни_подаци_подаци)
                Отпрема_Фајлови.sendall(b'UPLOAD TARGET PRESERVED')
            assert фајл_пренос_веза.voidresp().startswith('226')
            ИСХОД = bytearray(); фајл_пренос_веза.retrbinary('RETR pending.txt', ИСХОД.extend)
            assert ИСХОД == b'UPLOAD TARGET PRESERVED'
            ИСХОД = bytearray(); фајл_пренос_веза.retrbinary('RETR binary.dat', ИСХОД.extend)
            assert ИСХОД == корисни_подаци_подаци
            фајл_пренос_веза.delete('pending.txt')
            провјера_извештај['checks'].append('interleaved SIZE cannot change the active STOR destination')
            фајл_пренос_веза.storbinary('STOR 인사.jar', io.BytesIO(Архива.getvalue()))
            Текст = љуска('java -jar 인사.jar 누리')
            assert 'JAR Изврши_команда: 누리' in Текст and '자체 језгро_вриједност Датотека' in Текст and 'exit 0' in Текст, Текст
            Текст = љуска('./인사.jar 세상')
            assert 'JAR Изврши_команда: 세상' in Текст and 'exit 0' in Текст, Текст
            провјера_извештај['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct подаци { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct подаци вриједност = {합(10), 1.25}; if (вриједност.수 != 55 || вриједност.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = креирати_фајл("cc.txt", за_читање_писање | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; писати_фајл_подаци(문서, 인사, sizeof(인사)-1); затварање_фајл(문서); писати_фајл_подаци(1, 인사, sizeof(인사)-1); return 0; }\n'
            фајл_пренос_веза.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Текст = љуска('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Текст and 'exit 0' in Текст, Текст
            Текст = љуска('run 한글.elf'); assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст, Текст
            assert 'CC NATIVE PASS' in љуска('cat cc.txt')
            실행파일 = bytearray(); фајл_пренос_веза.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            фајл_пренос_веза.storbinary('STOR инстанца_вриједност.elf', io.BytesIO(실행파일)); Текст = љуска('run инстанца_вриједност.elf'); assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст, Текст
            фајл_пренос_веза.storbinary('STOR Изврши_команда', io.BytesIO(실행파일)); Текст=љуска('./Изврши_команда');assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст,Текст
            фајл_пренос_веза.storbinary('STOR Назив.txt', io.BytesIO(실행파일)); Текст=љуска('./Назив.txt');assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст,Текст
            љуска('rm Изврши_команда Назив.txt')
            провјера_извештај['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            љуска('rm binary.dat 한글.txt 한글.c 한글.elf инстанца_вриједност.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(мера_подаци/'linux-reference')
            фајл_пренос_веза.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Текст=љуска('./리눅스인사');assert 'exit -8' in Текст,Текст
            Текст=љуска('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Текст,Текст
            assert 'LINUX ELF FILE IO' in љуска('cat linux.txt')
            фајл_пренос_веза.delete('리눅스인사');фајл_пренос_веза.delete('linux.txt')
            фајл_пренос_веза.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in љуска('./거짓.elf');фајл_пренос_веза.delete('거짓.elf')
            провјера_извештај['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = мера_подаци/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Повежи_се = 한국어.자체.연결통신.Повежи_се("10.0.2.2", Integer.parseInt(args[0]));
 Повежи_се.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ИЗВОР = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ИЗВОР.length;i++) if (Повежи_се.getInputStream().read() != (ИЗВОР[i]&255)) throw new RuntimeException("TCP mismatch");
 Повежи_се.close();
 DatagramSocket крајња_тачка = 한국어.자체.통신.Отвори(0); 한국어.자체.통신.대기시간(крајња_тачка, 500);
 한국어.자체.통신.послати(крајња_тачка, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(крајња_тачка).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 крајња_тачка.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(пројектовати_корен/'build/java-library/classes'),'-d',str(мера_подаци),str(통신원문)])
                фајл_пренос_веза.storbinary('STOR 바깥통신.class', io.BytesIO((мера_подаци/'바깥통신.class').read_bytes()))
                Текст = љуска('java 바깥통신 {} {}'.format(되돌림서버항목.연결접속번호, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in Текст and '10.0.2.2' in Текст and 'exit 0' in Текст, Текст
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            провјера_извештај['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            фајл_пренос_веза.delete('바깥통신.class')
            сервер_извор=мера_подаци/'서버시험.java'
            сервер_извор.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket сервер_вриједност = new ServerSocket(9300); DatagramSocket крајња_тачка = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket гост_вриједност = сервер_вриједност.accept();
  гост_вриједност.getOutputStream().write(гост_вриједност.getInputStream().read()+1); гост_вриједност.close(); сервер_вриједност.close();
  byte[] Садржај_вриједност = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Садржај_вриједност, Садржај_вриједност.length); крајња_тачка.receive(전문);
  крајња_тачка.send(전문); крајња_тачка.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(мера_подаци),str(сервер_извор)])
            фајл_пренос_веза.storbinary('STOR 서버시험.class',io.BytesIO((мера_подаци/'서버시험.class').read_bytes()))
            Процес.stdin.write('java 서버시험\n'.encode());Процес.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',сервер_ток_порт),timeout=5) as 상대:
                상대.sendall(b'A');assert 상대.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as 상대:
                상대.settimeout(5);상대.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert 상대.recvfrom(512)[0]==b'UDP-IN'
            Текст=수신하기();assert 'INBOUND TCP UDP PASS' in Текст and 'exit 0' in Текст,Текст
            провјера_извештај['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            фајл_пренос_веза.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] Аргументи) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.Излаз.수쓰기(합); 한국어.자체.Датотека.Пише("aot.txt", "한글 AOT Датотека 😀"); 한국어.자체.Излаз.писати_редак(한국어.자체.Датотека.Чита("aot.txt")); } }'
            фајл_пренос_веза.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            Текст = љуска('javac 빛.java'); assert 'exit 0' in Текст and 'Compiled:' in Текст, Текст
            Текст = љуска('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Текст and 'exit 0' in Текст, Текст
            Текст = љуска('run 빛.elf'); assert '\n55\n' in Текст and '한글 AOT Датотека 😀' in Текст and 'exit 0' in Текст, Текст
            자체실행파일 = bytearray(); фајл_пренос_веза.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Текст = љуска('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Текст and 'unsupported' in Текст, Текст
            보존자료 = bytearray(); фајл_пренос_веза.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); фајл_пренос_веза.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            фајл_пренос_веза.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Текст = љуска('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Текст and 'exit 0' in Текст, Текст
            Текст = љуска('run 빛.elf'); assert '\n55\n' in Текст and '한글 AOT Датотека 😀' in Текст and 'exit 0' in Текст, Текст
            провјера_извештај['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            провјера_извештај['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            статични_извор=мера_подаци/'정적시험.java'
            статични_извор.write_text('''public class 정적시험 {
 static int пројектовати_корен = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] Аргументи) {
  int[] вриједност = new int[] {пројектовати_корен, 합(10)};
  System.out.println(вриједност[0] + вриједност[1]); System.out.println(Аргументи[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(мера_подаци),str(статични_извор)])
            фајл_пренос_веза.storbinary('STOR 정적시험.class',io.BytesIO((мера_подаци/'정적시험.class').read_bytes()))
            Текст=љуска('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Текст,Текст
            Текст=љуска('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Текст,Текст
            фајл_пренос_веза.delete('정적시험.class');фајл_пренос_веза.delete('정적시험.elf')
            провјера_извештај['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Архива.getvalue());손상자료[14]^=1
            фајл_пренос_веза.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Текст=љуска('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Текст,Текст
            провјера_извештај['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            фајл_пренос_веза.quit(); assert 'FTP stopped' in љуска('ftpd stop')
            assert not мост.ГРЕШКА, мост.ГРЕШКА
            провјера_извештај.update(passed=True, frames_to_guest=мост.커널수신틀수, frames_from_guest=мост.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in бирач.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: транскрипт.extend(조각)
            мост.пауза_догађај.set()
            Процес.terminate()
            try: Процес.wait(timeout=5)
            except subprocess.TimeoutExpired: Процес.kill(); Процес.wait()
            бирач.close(); Процес.stdin.close(); Процес.stdout.close()
            провјера_извештај['bridge_error'] = мост.ГРЕШКА
            провјера_извештај['frames_to_guest'] = мост.커널수신틀수; провјера_извештај['frames_from_guest'] = мост.커널발신틀수
            (мера_подаци/'packets.json').write_text(json.dumps(мост.траг_евиденција,indent=2)+'\n')
            (мера_подаци / 'serial.log').write_bytes(транскрипт)
            (мера_подаци / 'report.json').write_text(json.dumps(провјера_извештај, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Покрени()
