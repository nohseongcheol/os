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
from Шабака_кӯпрук import Шабака_кӯпрук
from иҷро_кардан_фармон import 기준, фармон
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def порча():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    санҷиши_эътибор_гузориш = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.навиштан_хат("JAR иҷро_кардан_фармон: " + 인수[0]); 한국어.자체.Файл.Навиштан("jar.txt", "자체 ҳаста_қимат Файл"); 한국어.자체.출력.навиштан_хат(한국어.자체.Файл.Хондан("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    Бойгонӣ = io.BytesIO()
    with zipfile.ZipFile(Бойгонӣ, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); сервер_ҷараён_порт = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Шабака_кӯпрук(접속번호, ['tcp:{}:9300'.format(сервер_ҷараён_порт), 'udp:{}:9301'.format(서버전문접속번호)], акс_гирифтан=True) as кӯпрук:
        Раванд = subprocess.Popen(фармон() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + кӯпрук.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        интихобкунанда = selectors.DefaultSelector(); интихобкунанда.register(Раванд.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            иттилоот = bytearray(); анҷом_додан_Интиқолшавӣ = time.monotonic() + 시간제한
            while 확인표시 not in иттилоот:
                if time.monotonic() > анҷом_додан_Интиқолшавӣ or Раванд.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + иттилоот.decode('utf-8', 'replace'))
                for 누름값, _ in интихобкунанда.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: иттилоот.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in иттилоот or b'FAIL ' in иттилоот: raise AssertionError(иттилоот)
            return иттилоот.decode('utf-8', 'replace').replace('\r\n', '\n')
        def восит(хат):
            Раванд.stdin.write(хат.encode() + b'\n'); Раванд.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in восит('ftpd start')
            файл_интиқол_пайваст = ftplib.FTP(); файл_интиқол_пайваст.encoding = 'utf-8'; файл_интиқол_пайваст.connect('127.0.0.1', 접속번호, timeout=20); файл_интиқол_пайваст.login()
            қобилият_иттилоот = bytes(range(256)) * 32
            файл_интиқол_пайваст.storbinary('STOR binary.dat', io.BytesIO(қобилият_иттилоот))
            결과 = bytearray(); файл_интиқол_пайваст.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == қобилият_иттилоот; assert файл_интиқол_пайваст.size('binary.dat') == len(қобилият_иттилоот)
            санҷиши_эътибор_гузориш['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            файл_интиқол_пайваст.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in восит('cat 한글.txt')
            assert '한글.txt' in файл_интиқол_пайваст.nlst()
            assert dict(файл_интиқол_пайваст.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            санҷиши_эътибор_гузориш['checks'].append('UTF-8 filename and content visible in guest shell')
            try: файл_интиқол_пайваст.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); файл_интиқол_пайваст.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == қобилият_иттилоот
            санҷиши_эътибор_гузориш['checks'].append('oversized replacement rejected; previous file preserved')
            with файл_интиқол_пайваст.transfercmd('STOR pending.txt') as бор_кардан_Файлҳо:
                # A control command must not change the active upload's destination.
                assert файл_интиқол_пайваст.size('binary.dat') == len(қобилият_иттилоот)
                бор_кардан_Файлҳо.sendall(b'UPLOAD TARGET PRESERVED')
            assert файл_интиқол_пайваст.voidresp().startswith('226')
            결과 = bytearray(); файл_интиқол_пайваст.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); файл_интиқол_пайваст.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == қобилият_иттилоот
            файл_интиқол_пайваст.delete('pending.txt')
            санҷиши_эътибор_гузориш['checks'].append('interleaved SIZE cannot change the active STOR destination')
            файл_интиқол_пайваст.storbinary('STOR 인사.jar', io.BytesIO(Бойгонӣ.getvalue()))
            Матн = восит('java -jar 인사.jar 누리')
            assert 'JAR иҷро_кардан_фармон: 누리' in Матн and '자체 ҳаста_қимат Файл' in Матн and 'exit 0' in Матн, Матн
            Матн = восит('./인사.jar 세상')
            assert 'JAR иҷро_кардан_фармон: 세상' in Матн and 'exit 0' in Матн, Матн
            санҷиши_эътибор_гузориш['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct иттилоот { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct иттилоот қимат = {합(10), 1.25}; if (қимат.수 != 55 || қимат.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = кушодан_файл("cc.txt", хондан_навиштан | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; навиштан_файл_иттилоот(문서, 인사, sizeof(인사)-1); пӯшидан_файл(문서); навиштан_файл_иттилоот(1, 인사, sizeof(인사)-1); return 0; }\n'
            файл_интиқол_пайваст.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Матн = восит('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Матн and 'exit 0' in Матн, Матн
            Матн = восит('run 한글.elf'); assert 'CC NATIVE PASS' in Матн and 'exit 0' in Матн, Матн
            assert 'CC NATIVE PASS' in восит('cat cc.txt')
            실행파일 = bytearray(); файл_интиқол_пайваст.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            файл_интиқол_пайваст.storbinary('STOR ҳолат_қимат.elf', io.BytesIO(실행파일)); Матн = восит('run ҳолат_қимат.elf'); assert 'CC NATIVE PASS' in Матн and 'exit 0' in Матн, Матн
            файл_интиқол_пайваст.storbinary('STOR иҷро_кардан_фармон', io.BytesIO(실행파일)); Матн=восит('./иҷро_кардан_фармон');assert 'CC NATIVE PASS' in Матн and 'exit 0' in Матн,Матн
            файл_интиқол_пайваст.storbinary('STOR Ном.txt', io.BytesIO(실행파일)); Матн=восит('./Ном.txt');assert 'CC NATIVE PASS' in Матн and 'exit 0' in Матн,Матн
            восит('rm иҷро_кардан_фармон Ном.txt')
            санҷиши_эътибор_гузориш['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            восит('rm binary.dat 한글.txt 한글.c 한글.elf ҳолат_қимат.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            файл_интиқол_пайваст.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Матн=восит('./리눅스인사');assert 'exit -8' in Матн,Матн
            Матн=восит('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Матн,Матн
            assert 'LINUX ELF FILE IO' in восит('cat linux.txt')
            файл_интиқол_пайваст.delete('리눅스인사');файл_интиқол_пайваст.delete('linux.txt')
            файл_интиқол_пайваст.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in восит('./거짓.elf');файл_интиқол_пайваст.delete('거짓.elf')
            санҷиши_эътибор_гузориш['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket ПАЙВАСТ = 한국어.자체.연결통신.ПАЙВАСТ("10.0.2.2", Integer.parseInt(args[0]));
 ПАЙВАСТ.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] манбаъ = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<манбаъ.length;i++) if (ПАЙВАСТ.getInputStream().read() != (манбаъ[i]&255)) throw new RuntimeException("TCP mismatch");
 ПАЙВАСТ.close();
 DatagramSocket 종단 = 한국어.자체.통신.кушодан(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.фиристодан(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                файл_интиқол_пайваст.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                Матн = восит('java 바깥통신 {} {}'.format(되돌림서버항목.Протоколи_TCP_порт, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in Матн and '10.0.2.2' in Матн and 'exit 0' in Матн, Матн
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            санҷиши_эътибор_гузориш['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            файл_интиқол_пайваст.delete('바깥통신.class')
            сервер_манбаъ=결과자료/'서버시험.java'
            сервер_манбаъ.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket сервер_қимат = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket меҳмон_қимат = сервер_қимат.accept();
  меҳмон_қимат.getOutputStream().write(меҳмон_қимат.getInputStream().read()+1); меҳмон_қимат.close(); сервер_қимат.close();
  byte[] Мӯҳтаво_қимат = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Мӯҳтаво_қимат, Мӯҳтаво_қимат.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(сервер_манбаъ)])
            файл_интиқол_пайваст.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            Раванд.stdin.write('java 서버시험\n'.encode());Раванд.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',сервер_ҷараён_порт),timeout=5) as ҳамсон_қимат:
                ҳамсон_қимат.sendall(b'A');assert ҳамсон_қимат.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ҳамсон_қимат:
                ҳамсон_қимат.settimeout(5);ҳамсон_қимат.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert ҳамсон_қимат.recvfrom(512)[0]==b'UDP-IN'
            Матн=수신하기();assert 'INBOUND TCP UDP PASS' in Матн and 'exit 0' in Матн,Матн
            санҷиши_эътибор_гузориш['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            файл_интиқол_пайваст.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.Файл.Навиштан("aot.txt", "한글 AOT Файл 😀"); 한국어.자체.출력.навиштан_хат(한국어.자체.Файл.Хондан("aot.txt")); } }'
            файл_интиқол_пайваст.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            Матн = восит('javac 빛.java'); assert 'exit 0' in Матн and 'Compiled:' in Матн, Матн
            Матн = восит('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Матн and 'exit 0' in Матн, Матн
            Матн = восит('run 빛.elf'); assert '\n55\n' in Матн and '한글 AOT Файл 😀' in Матн and 'exit 0' in Матн, Матн
            자체실행파일 = bytearray(); файл_интиқол_пайваст.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Матн = восит('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Матн and 'unsupported' in Матн, Матн
            보존자료 = bytearray(); файл_интиқол_пайваст.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); файл_интиқол_пайваст.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            файл_интиқол_пайваст.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Матн = восит('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Матн and 'exit 0' in Матн, Матн
            Матн = восит('run 빛.elf'); assert '\n55\n' in Матн and '한글 AOT Файл 😀' in Матн and 'exit 0' in Матн, Матн
            санҷиши_эътибор_гузориш['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            санҷиши_эътибор_гузориш['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            собит_манбаъ=결과자료/'정적시험.java'
            собит_манбаъ.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] қимат = new int[] {기준, 합(10)};
  System.out.println(қимат[0] + қимат[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(собит_манбаъ)])
            файл_интиқол_пайваст.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            Матн=восит('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Матн,Матн
            Матн=восит('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Матн,Матн
            файл_интиқол_пайваст.delete('정적시험.class');файл_интиқол_пайваст.delete('정적시험.elf')
            санҷиши_эътибор_гузориш['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Бойгонӣ.getvalue());손상자료[14]^=1
            файл_интиқол_пайваст.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Матн=восит('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Матн,Матн
            санҷиши_эътибор_гузориш['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            файл_интиқол_пайваст.quit(); assert 'FTP stopped' in восит('ftpd stop')
            assert not кӯпрук.Хато, кӯпрук.Хато
            санҷиши_эътибор_гузориш.update(passed=True, frames_to_guest=кӯпрук.커널수신틀수, frames_from_guest=кӯпрук.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in интихобкунанда.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            кӯпрук.таваққуф_кардан_рӯйдод.set()
            Раванд.terminate()
            try: Раванд.wait(timeout=5)
            except subprocess.TimeoutExpired: Раванд.kill(); Раванд.wait()
            интихобкунанда.close(); Раванд.stdin.close(); Раванд.stdout.close()
            санҷиши_эътибор_гузориш['bridge_error'] = кӯпрук.Хато
            санҷиши_эътибор_гузориш['frames_to_guest'] = кӯпрук.커널수신틀수; санҷиши_эътибор_гузориш['frames_from_guest'] = кӯпрук.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(кӯпрук.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(санҷиши_эътибор_гузориш, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': порча()
