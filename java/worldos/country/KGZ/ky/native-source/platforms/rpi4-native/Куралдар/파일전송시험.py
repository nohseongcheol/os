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
from 통신다리 import 통신다리
from аткаруу_буйрук import 기준, Команда
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Жүргүзүү():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    ырастоо_отчет = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.Чыгыш.жазуу_сап("JAR аткаруу_буйрук: " + 인수[0]); 한국어.자체.Файл.Жазуу("jar.txt", "자체 өзөк_маани Файл"); 한국어.자체.Чыгыш.жазуу_сап(한국어.자체.Файл.Окуу("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    Архив = io.BytesIO()
    with zipfile.ZipFile(Архив, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); сервер_агым_порт = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(접속번호, ['tcp:{}:9300'.format(сервер_агым_порт), 'udp:{}:9301'.format(서버전문접속번호)], тартуу_жаздыруу=True) as 연결다리:
        Процесси = subprocess.Popen(Команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        селектор = selectors.DefaultSelector(); селектор.register(Процесси.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            берилмелер = bytearray(); аяктоо_Жылбышуу = time.monotonic() + 시간제한
            while 확인표시 not in берилмелер:
                if time.monotonic() > аяктоо_Жылбышуу or Процесси.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + берилмелер.decode('utf-8', 'replace'))
                for 누름값, _ in селектор.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: берилмелер.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in берилмелер or b'FAIL ' in берилмелер: raise AssertionError(берилмелер)
            return берилмелер.decode('utf-8', 'replace').replace('\r\n', '\n')
        def сырты(сап):
            Процесси.stdin.write(сап.encode() + b'\n'); Процесси.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in сырты('ftpd start')
            файл_ташүү_туташуу = ftplib.FTP(); файл_ташүү_туташуу.encoding = 'utf-8'; файл_ташүү_туташуу.connect('127.0.0.1', 접속번호, timeout=20); файл_ташүү_туташуу.login()
            керектүү_жүктөө_ченеми_берилмелер = bytes(range(256)) * 32
            файл_ташүү_туташуу.storbinary('STOR binary.dat', io.BytesIO(керектүү_жүктөө_ченеми_берилмелер))
            결과 = bytearray(); файл_ташүү_туташуу.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == керектүү_жүктөө_ченеми_берилмелер; assert файл_ташүү_туташуу.size('binary.dat') == len(керектүү_жүктөө_ченеми_берилмелер)
            ырастоо_отчет['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            файл_ташүү_туташуу.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in сырты('cat 한글.txt')
            assert '한글.txt' in файл_ташүү_туташуу.nlst()
            assert dict(файл_ташүү_туташуу.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            ырастоо_отчет['checks'].append('UTF-8 filename and content visible in guest shell')
            try: файл_ташүү_туташуу.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); файл_ташүү_туташуу.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == керектүү_жүктөө_ченеми_берилмелер
            ырастоо_отчет['checks'].append('oversized replacement rejected; previous file preserved')
            with файл_ташүү_туташуу.transfercmd('STOR pending.txt') as жүктөп_жөнөтүү_Файлдар:
                # A control command must not change the active upload's destination.
                assert файл_ташүү_туташуу.size('binary.dat') == len(керектүү_жүктөө_ченеми_берилмелер)
                жүктөп_жөнөтүү_Файлдар.sendall(b'UPLOAD TARGET PRESERVED')
            assert файл_ташүү_туташуу.voidresp().startswith('226')
            결과 = bytearray(); файл_ташүү_туташуу.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); файл_ташүү_туташуу.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == керектүү_жүктөө_ченеми_берилмелер
            файл_ташүү_туташуу.delete('pending.txt')
            ырастоо_отчет['checks'].append('interleaved SIZE cannot change the active STOR destination')
            файл_ташүү_туташуу.storbinary('STOR 인사.jar', io.BytesIO(Архив.getvalue()))
            Текст = сырты('java -jar 인사.jar 누리')
            assert 'JAR аткаруу_буйрук: 누리' in Текст and '자체 өзөк_маани Файл' in Текст and 'exit 0' in Текст, Текст
            Текст = сырты('./인사.jar 세상')
            assert 'JAR аткаруу_буйрук: 세상' in Текст and 'exit 0' in Текст, Текст
            ырастоо_отчет['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct берилмелер { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct берилмелер маани = {합(10), 1.25}; if (маани.수 != 55 || маани.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ачуу_файл("cc.txt", окуу_жазуу | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; жазуу_файл_берилмелер(문서, 인사, sizeof(인사)-1); жабуу_файл(문서); жазуу_файл_берилмелер(1, 인사, sizeof(인사)-1); return 0; }\n'
            файл_ташүү_туташуу.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Текст = сырты('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Текст and 'exit 0' in Текст, Текст
            Текст = сырты('run 한글.elf'); assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст, Текст
            assert 'CC NATIVE PASS' in сырты('cat cc.txt')
            실행파일 = bytearray(); файл_ташүү_туташуу.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            файл_ташүү_туташуу.storbinary('STOR даана_маани.elf', io.BytesIO(실행파일)); Текст = сырты('run даана_маани.elf'); assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст, Текст
            файл_ташүү_туташуу.storbinary('STOR аткаруу_буйрук', io.BytesIO(실행파일)); Текст=сырты('./аткаруу_буйрук');assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст,Текст
            файл_ташүү_туташуу.storbinary('STOR Аты.txt', io.BytesIO(실행파일)); Текст=сырты('./Аты.txt');assert 'CC NATIVE PASS' in Текст and 'exit 0' in Текст,Текст
            сырты('rm аткаруу_буйрук Аты.txt')
            ырастоо_отчет['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            сырты('rm binary.dat 한글.txt 한글.c 한글.elf даана_маани.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            файл_ташүү_туташуу.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Текст=сырты('./리눅스인사');assert 'exit -8' in Текст,Текст
            Текст=сырты('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Текст,Текст
            assert 'LINUX ELF FILE IO' in сырты('cat linux.txt')
            файл_ташүү_туташуу.delete('리눅스인사');файл_ташүү_туташуу.delete('linux.txt')
            файл_ташүү_туташуу.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in сырты('./거짓.elf');файл_ташүү_туташуу.delete('거짓.elf')
            ырастоо_отчет['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Туташуу = 한국어.자체.연결통신.Туташуу("10.0.2.2", Integer.parseInt(args[0]));
 Туташуу.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] Булак = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<Булак.length;i++) if (Туташуу.getInputStream().read() != (Булак[i]&255)) throw new RuntimeException("TCP mismatch");
 Туташуу.close();
 DatagramSocket 종단 = 한국어.자체.통신.Ачуу(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.жөнөтүү(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                файл_ташүү_туташуу.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                Текст = сырты('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_протоколу_порт, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in Текст and '10.0.2.2' in Текст and 'exit 0' in Текст, Текст
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            ырастоо_отчет['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            файл_ташүү_туташуу.delete('바깥통신.class')
            сервер_башат=결과자료/'서버시험.java'
            сервер_башат.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket сервер_маани = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket 손님 = сервер_маани.accept();
  손님.getOutputStream().write(손님.getInputStream().read()+1); 손님.close(); сервер_маани.close();
  byte[] Мазмун_маани = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Мазмун_маани, Мазмун_маани.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(сервер_башат)])
            файл_ташүү_туташуу.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            Процесси.stdin.write('java 서버시험\n'.encode());Процесси.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',сервер_агым_порт),timeout=5) as бирдей_маани:
                бирдей_маани.sendall(b'A');assert бирдей_маани.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as бирдей_маани:
                бирдей_маани.settimeout(5);бирдей_маани.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert бирдей_маани.recvfrom(512)[0]==b'UDP-IN'
            Текст=수신하기();assert 'INBOUND TCP UDP PASS' in Текст and 'exit 0' in Текст,Текст
            ырастоо_отчет['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            файл_ташүү_туташуу.delete('서버시험.class')
            аткаруу_буйругу_ЫРААТТУУЛУК = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.Чыгыш.수쓰기(합); 한국어.자체.Файл.Жазуу("aot.txt", "한글 AOT Файл 😀"); 한국어.자체.Чыгыш.жазуу_сап(한국어.자체.Файл.Окуу("aot.txt")); } }'
            файл_ташүү_туташуу.storbinary('STOR 빛.java', io.BytesIO(аткаруу_буйругу_ЫРААТТУУЛУК.encode()))
            Текст = сырты('javac 빛.java'); assert 'exit 0' in Текст and 'Compiled:' in Текст, Текст
            Текст = сырты('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Текст and 'exit 0' in Текст, Текст
            Текст = сырты('run 빛.elf'); assert '\n55\n' in Текст and '한글 AOT Файл 😀' in Текст and 'exit 0' in Текст, Текст
            자체실행파일 = bytearray(); файл_ташүү_туташуу.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Текст = сырты('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Текст and 'unsupported' in Текст, Текст
            보존자료 = bytearray(); файл_ташүү_туташуу.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); файл_ташүү_туташуу.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            файл_ташүү_туташуу.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Текст = сырты('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Текст and 'exit 0' in Текст, Текст
            Текст = сырты('run 빛.elf'); assert '\n55\n' in Текст and '한글 AOT Файл 😀' in Текст and 'exit 0' in Текст, Текст
            ырастоо_отчет['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            ырастоо_отчет['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            статикалык_башат=결과자료/'정적시험.java'
            статикалык_башат.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] маани = new int[] {기준, 합(10)};
  System.out.println(маани[0] + маани[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(статикалык_башат)])
            файл_ташүү_туташуу.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            Текст=сырты('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Текст,Текст
            Текст=сырты('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Текст,Текст
            файл_ташүү_туташуу.delete('정적시험.class');файл_ташүү_туташуу.delete('정적시험.elf')
            ырастоо_отчет['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Архив.getvalue());손상자료[14]^=1
            файл_ташүү_туташуу.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Текст=сырты('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Текст,Текст
            ырастоо_отчет['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            файл_ташүү_туташуу.quit(); assert 'FTP stopped' in сырты('ftpd stop')
            assert not 연결다리.Ката, 연결다리.Ката
            ырастоо_отчет.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in селектор.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.пауза_окуя.set()
            Процесси.terminate()
            try: Процесси.wait(timeout=5)
            except subprocess.TimeoutExpired: Процесси.kill(); Процесси.wait()
            селектор.close(); Процесси.stdin.close(); Процесси.stdout.close()
            ырастоо_отчет['bridge_error'] = 연결다리.Ката
            ырастоо_отчет['frames_to_guest'] = 연결다리.커널수신틀수; ырастоо_отчет['frames_from_guest'] = 연결다리.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(연결다리.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(ырастоо_отчет, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Жүргүзүү()
