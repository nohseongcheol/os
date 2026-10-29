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
from Гүйцэтгэх_команд import 기준, Тушаал
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Ажиллуулах():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    баталгаажуулалт_тайлан = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.бичих_мөр("JAR Гүйцэтгэх_команд: " + 인수[0]); 한국어.자체.Файл.Бичих("jar.txt", "자체 кернел_утга Файл"); 한국어.자체.출력.бичих_мөр(한국어.자체.Файл.Унших("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    Архив = io.BytesIO()
    with zipfile.ZipFile(Архив, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); сервер_урсгал_порт = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(접속번호, ['tcp:{}:9300'.format(сервер_урсгал_порт), 'udp:{}:9301'.format(서버전문접속번호)], авах=True) as 연결다리:
        үйл_явц = subprocess.Popen(Тушаал() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        сонгогч = selectors.DefaultSelector(); сонгогч.register(үйл_явц.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            өгөгдөл = bytearray(); дуусгах_Оффсет = time.monotonic() + 시간제한
            while 확인표시 not in өгөгдөл:
                if time.monotonic() > дуусгах_Оффсет or үйл_явц.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + өгөгдөл.decode('utf-8', 'replace'))
                for 누름값, _ in сонгогч.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: өгөгдөл.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in өгөгдөл or b'FAIL ' in өгөгдөл: raise AssertionError(өгөгдөл)
            return өгөгдөл.decode('utf-8', 'replace').replace('\r\n', '\n')
        def бүрхүүл(Шугам):
            үйл_явц.stdin.write(Шугам.encode() + b'\n'); үйл_явц.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in бүрхүүл('ftpd start')
            файл_дамжуулах_холболт = ftplib.FTP(); файл_дамжуулах_холболт.encoding = 'utf-8'; файл_дамжуулах_холболт.connect('127.0.0.1', 접속번호, timeout=20); файл_дамжуулах_холболт.login()
            ашигтай_ачаалал_өгөгдөл = bytes(range(256)) * 32
            файл_дамжуулах_холболт.storbinary('STOR binary.dat', io.BytesIO(ашигтай_ачаалал_өгөгдөл))
            결과 = bytearray(); файл_дамжуулах_холболт.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ашигтай_ачаалал_өгөгдөл; assert файл_дамжуулах_холболт.size('binary.dat') == len(ашигтай_ачаалал_өгөгдөл)
            баталгаажуулалт_тайлан['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            файл_дамжуулах_холболт.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in бүрхүүл('cat 한글.txt')
            assert '한글.txt' in файл_дамжуулах_холболт.nlst()
            assert dict(файл_дамжуулах_холболт.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            баталгаажуулалт_тайлан['checks'].append('UTF-8 filename and content visible in guest shell')
            try: файл_дамжуулах_холболт.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); файл_дамжуулах_холболт.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == ашигтай_ачаалал_өгөгдөл
            баталгаажуулалт_тайлан['checks'].append('oversized replacement rejected; previous file preserved')
            with файл_дамжуулах_холболт.transfercmd('STOR pending.txt') as байршуулах_Файлууд:
                # A control command must not change the active upload's destination.
                assert файл_дамжуулах_холболт.size('binary.dat') == len(ашигтай_ачаалал_өгөгдөл)
                байршуулах_Файлууд.sendall(b'UPLOAD TARGET PRESERVED')
            assert файл_дамжуулах_холболт.voidresp().startswith('226')
            결과 = bytearray(); файл_дамжуулах_холболт.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); файл_дамжуулах_холболт.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ашигтай_ачаалал_өгөгдөл
            файл_дамжуулах_холболт.delete('pending.txt')
            баталгаажуулалт_тайлан['checks'].append('interleaved SIZE cannot change the active STOR destination')
            файл_дамжуулах_холболт.storbinary('STOR 인사.jar', io.BytesIO(Архив.getvalue()))
            Бичвэр = бүрхүүл('java -jar 인사.jar 누리')
            assert 'JAR Гүйцэтгэх_команд: 누리' in Бичвэр and '자체 кернел_утга Файл' in Бичвэр and 'exit 0' in Бичвэр, Бичвэр
            Бичвэр = бүрхүүл('./인사.jar 세상')
            assert 'JAR Гүйцэтгэх_команд: 세상' in Бичвэр and 'exit 0' in Бичвэр, Бичвэр
            баталгаажуулалт_тайлан['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct өгөгдөл { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct өгөгдөл утга = {합(10), 1.25}; if (утга.수 != 55 || утга.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = нээх_файл("cc.txt", унших_бичих | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; бичих_файл_өгөгдөл(문서, 인사, sizeof(인사)-1); хаах_файл(문서); бичих_файл_өгөгдөл(1, 인사, sizeof(인사)-1); return 0; }\n'
            файл_дамжуулах_холболт.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Бичвэр = бүрхүүл('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Бичвэр and 'exit 0' in Бичвэр, Бичвэр
            Бичвэр = бүрхүүл('run 한글.elf'); assert 'CC NATIVE PASS' in Бичвэр and 'exit 0' in Бичвэр, Бичвэр
            assert 'CC NATIVE PASS' in бүрхүүл('cat cc.txt')
            실행파일 = bytearray(); файл_дамжуулах_холболт.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            файл_дамжуулах_холболт.storbinary('STOR хуулах_утга.elf', io.BytesIO(실행파일)); Бичвэр = бүрхүүл('run хуулах_утга.elf'); assert 'CC NATIVE PASS' in Бичвэр and 'exit 0' in Бичвэр, Бичвэр
            файл_дамжуулах_холболт.storbinary('STOR Гүйцэтгэх_команд', io.BytesIO(실행파일)); Бичвэр=бүрхүүл('./Гүйцэтгэх_команд');assert 'CC NATIVE PASS' in Бичвэр and 'exit 0' in Бичвэр,Бичвэр
            файл_дамжуулах_холболт.storbinary('STOR Нэр.txt', io.BytesIO(실행파일)); Бичвэр=бүрхүүл('./Нэр.txt');assert 'CC NATIVE PASS' in Бичвэр and 'exit 0' in Бичвэр,Бичвэр
            бүрхүүл('rm Гүйцэтгэх_команд Нэр.txt')
            баталгаажуулалт_тайлан['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            бүрхүүл('rm binary.dat 한글.txt 한글.c 한글.elf хуулах_утга.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            файл_дамжуулах_холболт.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Бичвэр=бүрхүүл('./리눅스인사');assert 'exit -8' in Бичвэр,Бичвэр
            Бичвэр=бүрхүүл('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Бичвэр,Бичвэр
            assert 'LINUX ELF FILE IO' in бүрхүүл('cat linux.txt')
            файл_дамжуулах_холболт.delete('리눅스인사');файл_дамжуулах_холболт.delete('linux.txt')
            файл_дамжуулах_холболт.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in бүрхүүл('./거짓.elf');файл_дамжуулах_холболт.delete('거짓.elf')
            баталгаажуулалт_тайлан['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Холбох = 한국어.자체.연결통신.Холбох("10.0.2.2", Integer.parseInt(args[0]));
 Холбох.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ЭХ = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ЭХ.length;i++) if (Холбох.getInputStream().read() != (ЭХ[i]&255)) throw new RuntimeException("TCP mismatch");
 Холбох.close();
 DatagramSocket 종단 = 한국어.자체.통신.Нээх(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.илгээх(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                файл_дамжуулах_холболт.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                Бичвэр = бүрхүүл('java 바깥통신 {} {}'.format(되돌림서버항목.Дамжууллын_хяналтын_протокол_порт, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in Бичвэр and '10.0.2.2' in Бичвэр and 'exit 0' in Бичвэр, Бичвэр
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            баталгаажуулалт_тайлан['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            файл_дамжуулах_холболт.delete('바깥통신.class')
            сервер_эх=결과자료/'서버시험.java'
            сервер_эх.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket сервер_утга = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket 손님 = сервер_утга.accept();
  손님.getOutputStream().write(손님.getInputStream().read()+1); 손님.close(); сервер_утга.close();
  byte[] Агуулга_утга = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Агуулга_утга, Агуулга_утга.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(сервер_эх)])
            файл_дамжуулах_холболт.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            үйл_явц.stdin.write('java 서버시험\n'.encode());үйл_явц.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',сервер_урсгал_порт),timeout=5) as ижил_түвшин_утга:
                ижил_түвшин_утга.sendall(b'A');assert ижил_түвшин_утга.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ижил_түвшин_утга:
                ижил_түвшин_утга.settimeout(5);ижил_түвшин_утга.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert ижил_түвшин_утга.recvfrom(512)[0]==b'UDP-IN'
            Бичвэр=수신하기();assert 'INBOUND TCP UDP PASS' in Бичвэр and 'exit 0' in Бичвэр,Бичвэр
            баталгаажуулалт_тайлан['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            файл_дамжуулах_холболт.delete('서버시험.class')
            заавар_ДАРААЛАЛ = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.Файл.Бичих("aot.txt", "한글 AOT Файл 😀"); 한국어.자체.출력.бичих_мөр(한국어.자체.Файл.Унших("aot.txt")); } }'
            файл_дамжуулах_холболт.storbinary('STOR 빛.java', io.BytesIO(заавар_ДАРААЛАЛ.encode()))
            Бичвэр = бүрхүүл('javac 빛.java'); assert 'exit 0' in Бичвэр and 'Compiled:' in Бичвэр, Бичвэр
            Бичвэр = бүрхүүл('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Бичвэр and 'exit 0' in Бичвэр, Бичвэр
            Бичвэр = бүрхүүл('run 빛.elf'); assert '\n55\n' in Бичвэр and '한글 AOT Файл 😀' in Бичвэр and 'exit 0' in Бичвэр, Бичвэр
            자체실행파일 = bytearray(); файл_дамжуулах_холболт.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Бичвэр = бүрхүүл('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Бичвэр and 'unsupported' in Бичвэр, Бичвэр
            보존자료 = bytearray(); файл_дамжуулах_холболт.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); файл_дамжуулах_холболт.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            файл_дамжуулах_холболт.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Бичвэр = бүрхүүл('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Бичвэр and 'exit 0' in Бичвэр, Бичвэр
            Бичвэр = бүрхүүл('run 빛.elf'); assert '\n55\n' in Бичвэр and '한글 AOT Файл 😀' in Бичвэр and 'exit 0' in Бичвэр, Бичвэр
            баталгаажуулалт_тайлан['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            баталгаажуулалт_тайлан['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            статик_эх=결과자료/'정적시험.java'
            статик_эх.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] утга = new int[] {기준, 합(10)};
  System.out.println(утга[0] + утга[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(статик_эх)])
            файл_дамжуулах_холболт.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            Бичвэр=бүрхүүл('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Бичвэр,Бичвэр
            Бичвэр=бүрхүүл('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Бичвэр,Бичвэр
            файл_дамжуулах_холболт.delete('정적시험.class');файл_дамжуулах_холболт.delete('정적시험.elf')
            баталгаажуулалт_тайлан['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Архив.getvalue());손상자료[14]^=1
            файл_дамжуулах_холболт.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Бичвэр=бүрхүүл('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Бичвэр,Бичвэр
            баталгаажуулалт_тайлан['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            файл_дамжуулах_холболт.quit(); assert 'FTP stopped' in бүрхүүл('ftpd stop')
            assert not 연결다리.Алдаа, 연결다리.Алдаа
            баталгаажуулалт_тайлан.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in сонгогч.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.түр_зогсоох_үйлдэл.set()
            үйл_явц.terminate()
            try: үйл_явц.wait(timeout=5)
            except subprocess.TimeoutExpired: үйл_явц.kill(); үйл_явц.wait()
            сонгогч.close(); үйл_явц.stdin.close(); үйл_явц.stdout.close()
            баталгаажуулалт_тайлан['bridge_error'] = 연결다리.Алдаа
            баталгаажуулалт_тайлан['frames_to_guest'] = 연결다리.커널수신틀수; баталгаажуулалт_тайлан['frames_from_guest'] = 연결다리.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(연결다리.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(баталгаажуулалт_тайлан, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Ажиллуулах()
