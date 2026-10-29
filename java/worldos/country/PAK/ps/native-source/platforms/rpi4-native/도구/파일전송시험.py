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
from 실행 import 기준, بولۍ
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def ځغلول():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    باورکړن_راپور = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.ليکل_ليکه("JAR 실행: " + 인수[0]); 한국어.자체.دوتنه.لوستل_2("jar.txt", "자체 نوغی_ارزښت دوتنه"); 한국어.자체.출력.ليکل_ليکه(한국어.자체.دوتنه.لوستل("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    ارشیف = io.BytesIO()
    with zipfile.ZipFile(ارشیف, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버연결접속번호 = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(접속번호, ['tcp:{}:9300'.format(서버연결접속번호), 'udp:{}:9301'.format(서버전문접속번호)], 포착여부=True) as 연결다리:
        بهير = subprocess.Popen(بولۍ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        준비선택기 = selectors.DefaultSelector(); 준비선택기.register(بهير.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            اومتوک = bytearray(); 끝위치 = time.monotonic() + 시간제한
            while 확인표시 not in اومتوک:
                if time.monotonic() > 끝위치 or بهير.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + اومتوک.decode('utf-8', 'replace'))
                for 누름값, _ in 준비선택기.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: اومتوک.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in اومتوک or b'FAIL ' in اومتوک: raise AssertionError(اومتوک)
            return اومتوک.decode('utf-8', 'replace').replace('\r\n', '\n')
        def سیپۍ(ليکه):
            بهير.stdin.write(ليکه.encode() + b'\n'); بهير.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in سیپۍ('ftpd start')
            دوتنه_لېږدول_پيوستون = ftplib.FTP(); دوتنه_لېږدول_پيوستون.encoding = 'utf-8'; دوتنه_لېږدول_پيوستون.connect('127.0.0.1', 접속번호, timeout=20); دوتنه_لېږدول_پيوستون.login()
            내용자료 = bytes(range(256)) * 32
            دوتنه_لېږدول_پيوستون.storbinary('STOR binary.dat', io.BytesIO(내용자료))
            결과 = bytearray(); دوتنه_لېږدول_پيوستون.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == 내용자료; assert دوتنه_لېږدول_پيوستون.size('binary.dat') == len(내용자료)
            باورکړن_راپور['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            دوتنه_لېږدول_پيوستون.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in سیپۍ('cat 한글.txt')
            assert '한글.txt' in دوتنه_لېږدول_پيوستون.nlst()
            assert dict(دوتنه_لېږدول_پيوستون.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            باورکړن_راپور['checks'].append('UTF-8 filename and content visible in guest shell')
            try: دوتنه_لېږدول_پيوستون.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); دوتنه_لېږدول_پيوستون.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == 내용자료
            باورکړن_راپور['checks'].append('oversized replacement rejected; previous file preserved')
            with دوتنه_لېږدول_پيوستون.transfercmd('STOR pending.txt') as 올리기:
                # A control command must not change the active upload's destination.
                assert دوتنه_لېږدول_پيوستون.size('binary.dat') == len(내용자료)
                올리기.sendall(b'UPLOAD TARGET PRESERVED')
            assert دوتنه_لېږدول_پيوستون.voidresp().startswith('226')
            결과 = bytearray(); دوتنه_لېږدول_پيوستون.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); دوتنه_لېږدول_پيوستون.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == 내용자료
            دوتنه_لېږدول_پيوستون.delete('pending.txt')
            باورکړن_راپور['checks'].append('interleaved SIZE cannot change the active STOR destination')
            دوتنه_لېږدول_پيوستون.storbinary('STOR 인사.jar', io.BytesIO(ارشیف.getvalue()))
            ليکنه = سیپۍ('java -jar 인사.jar 누리')
            assert 'JAR 실행: 누리' in ليکنه and '자체 نوغی_ارزښت دوتنه' in ليکنه and 'exit 0' in ليکنه, ليکنه
            ليکنه = سیپۍ('./인사.jar 세상')
            assert 'JAR 실행: 세상' in ليکنه and 'exit 0' in ليکنه, ليکنه
            باورکړن_راپور['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct اومتوک { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct اومتوک ارزښت = {합(10), 1.25}; if (ارزښت.수 != 55 || ارزښت.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = 파일열기("cc.txt", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; ليکل_دوتنه_اومتوک(문서, 인사, sizeof(인사)-1); بندول_دوتنه(문서); ليکل_دوتنه_اومتوک(1, 인사, sizeof(인사)-1); return 0; }\n'
            دوتنه_لېږدول_پيوستون.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            ليکنه = سیپۍ('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in ليکنه and 'exit 0' in ليکنه, ليکنه
            ليکنه = سیپۍ('run 한글.elf'); assert 'CC NATIVE PASS' in ليکنه and 'exit 0' in ليکنه, ليکنه
            assert 'CC NATIVE PASS' in سیپۍ('cat cc.txt')
            실행파일 = bytearray(); دوتنه_لېږدول_پيوستون.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            دوتنه_لېږدول_پيوستون.storbinary('STOR بېلګه_ارزښت_37b3d3b1.elf', io.BytesIO(실행파일)); ليکنه = سیپۍ('run بېلګه_ارزښت_37b3d3b1.elf'); assert 'CC NATIVE PASS' in ليکنه and 'exit 0' in ليکنه, ليکنه
            دوتنه_لېږدول_پيوستون.storbinary('STOR 실행', io.BytesIO(실행파일)); ليکنه=سیپۍ('./실행');assert 'CC NATIVE PASS' in ليکنه and 'exit 0' in ليکنه,ليکنه
            دوتنه_لېږدول_پيوستون.storbinary('STOR نوم.txt', io.BytesIO(실행파일)); ليکنه=سیپۍ('./نوم.txt');assert 'CC NATIVE PASS' in ليکنه and 'exit 0' in ليکنه,ليکنه
            سیپۍ('rm 실행 نوم.txt')
            باورکړن_راپور['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            سیپۍ('rm binary.dat 한글.txt 한글.c 한글.elf بېلګه_ارزښت_37b3d3b1.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            دوتنه_لېږدول_پيوستون.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            ليکنه=سیپۍ('./리눅스인사');assert 'exit -8' in ليکنه,ليکنه
            ليکنه=سیپۍ('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in ليکنه,ليکنه
            assert 'LINUX ELF FILE IO' in سیپۍ('cat linux.txt')
            دوتنه_لېږدول_پيوستون.delete('리눅스인사');دوتنه_لېږدول_پيوستون.delete('linux.txt')
            دوتنه_لېږدول_پيوستون.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in سیپۍ('./거짓.elf');دوتنه_لېږدول_پيوستون.delete('거짓.elf')
            باورکړن_راپور['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket نښلېدل = 한국어.자체.연결통신.نښلېدل("10.0.2.2", Integer.parseInt(args[0]));
 نښلېدل.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] سرچينه = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<سرچينه.length;i++) if (نښلېدل.getInputStream().read() != (سرچينه[i]&255)) throw new RuntimeException("TCP mismatch");
 نښلېدل.close();
 DatagramSocket 종단 = 한국어.자체.통신.پرانيستل(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.استول(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                دوتنه_لېږدول_پيوستون.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                ليکنه = سیپۍ('java 바깥통신 {} {}'.format(되돌림서버항목.لېږد_مهارې_باندره_درشل, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in ليکنه and '10.0.2.2' in ليکنه and 'exit 0' in ليکنه, ليکنه
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            باورکړن_راپور['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            دوتنه_لېږدول_پيوستون.delete('바깥통신.class')
            서버원문=결과자료/'서버시험.java'
            서버원문.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket 서버 = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket 손님 = 서버.accept();
  손님.getOutputStream().write(손님.getInputStream().read()+1); 손님.close(); 서버.close();
  byte[] منځپانګه_ارزښت = new byte[8]; DatagramPacket 전문 = new DatagramPacket(منځپانګه_ارزښت, منځپانګه_ارزښت.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(서버원문)])
            دوتنه_لېږدول_پيوستون.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            بهير.stdin.write('java 서버시험\n'.encode());بهير.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',서버연결접속번호),timeout=5) as جوړه_ارزښت:
                جوړه_ارزښت.sendall(b'A');assert جوړه_ارزښت.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as جوړه_ارزښت:
                جوړه_ارزښت.settimeout(5);جوړه_ارزښت.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert جوړه_ارزښت.recvfrom(512)[0]==b'UDP-IN'
            ليکنه=수신하기();assert 'INBOUND TCP UDP PASS' in ليکنه and 'exit 0' in ليکنه,ليکنه
            باورکړن_راپور['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            دوتنه_لېږدول_پيوستون.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.دوتنه.لوستل_2("aot.txt", "한글 AOT دوتنه 😀"); 한국어.자체.출력.ليکل_ليکه(한국어.자체.دوتنه.لوستل("aot.txt")); } }'
            دوتنه_لېږدول_پيوستون.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            ليکنه = سیپۍ('javac 빛.java'); assert 'exit 0' in ليکنه and 'Compiled:' in ليکنه, ليکنه
            ليکنه = سیپۍ('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ليکنه and 'exit 0' in ليکنه, ليکنه
            ليکنه = سیپۍ('run 빛.elf'); assert '\n55\n' in ليکنه and '한글 AOT دوتنه 😀' in ليکنه and 'exit 0' in ليکنه, ليکنه
            자체실행파일 = bytearray(); دوتنه_لېږدول_پيوستون.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            ليکنه = سیپۍ('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in ليکنه and 'unsupported' in ليکنه, ليکنه
            보존자료 = bytearray(); دوتنه_لېږدول_پيوستون.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); دوتنه_لېږدول_پيوستون.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            دوتنه_لېږدول_پيوستون.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            ليکنه = سیپۍ('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ليکنه and 'exit 0' in ليکنه, ليکنه
            ليکنه = سیپۍ('run 빛.elf'); assert '\n55\n' in ليکنه and '한글 AOT دوتنه 😀' in ليکنه and 'exit 0' in ليکنه, ليکنه
            باورکړن_راپور['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            باورکړن_راپور['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ولاړ_سرچینه=결과자료/'정적시험.java'
            ولاړ_سرچینه.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] ارزښت = new int[] {기준, 합(10)};
  System.out.println(ارزښت[0] + ارزښت[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(ولاړ_سرچینه)])
            دوتنه_لېږدول_پيوستون.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            ليکنه=سیپۍ('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in ليکنه,ليکنه
            ليکنه=سیپۍ('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in ليکنه,ليکنه
            دوتنه_لېږدول_پيوستون.delete('정적시험.class');دوتنه_لېږدول_پيوستون.delete('정적시험.elf')
            باورکړن_راپور['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ارشیف.getvalue());손상자료[14]^=1
            دوتنه_لېږدول_پيوستون.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            ليکنه=سیپۍ('java -jar 인사.jar');assert 'Main-Class\nexit 1' in ليکنه,ليکنه
            باورکړن_راپور['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            دوتنه_لېږدول_پيوستون.quit(); assert 'FTP stopped' in سیپۍ('ftpd stop')
            assert not 연결다리.تېروتنه, 연결다리.تېروتنه
            باورکړن_راپور.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in 준비선택기.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.ځنډ_پېښه.set()
            بهير.terminate()
            try: بهير.wait(timeout=5)
            except subprocess.TimeoutExpired: بهير.kill(); بهير.wait()
            준비선택기.close(); بهير.stdin.close(); بهير.stdout.close()
            باورکړن_راپور['bridge_error'] = 연결다리.تېروتنه
            باورکړن_راپور['frames_to_guest'] = 연결다리.커널수신틀수; باورکړن_راپور['frames_from_guest'] = 연결다리.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(연결다리.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(باورکړن_راپور, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ځغلول()
