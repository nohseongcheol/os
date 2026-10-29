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
from 실행 import 기준, ginol
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def huutoraade():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    teeŋtingol_ciimtol = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.winndude_diidol("JAR 실행: " + 인수[0]); 한국어.자체.fiilde.winndude("jar.txt", "자체 aaluude_njaru fiilde"); 한국어.자체.출력.winndude_diidol(한국어.자체.fiilde.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    ƴeewtirde = io.BytesIO()
    with zipfile.ZipFile(ƴeewtirde, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); sarworde_waraango_poor = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(접속번호, ['tcp:{}:9300'.format(sarworde_waraango_poor), 'udp:{}:9301'.format(서버전문접속번호)], 포착여부=True) as 연결다리:
        Yuɓɓo_golle = subprocess.Popen(ginol() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        준비선택기 = selectors.DefaultSelector(); 준비선택기.register(Yuɓɓo_golle.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            keɓe = bytearray(); 끝위치 = time.monotonic() + 시간제한
            while 확인표시 not in keɓe:
                if time.monotonic() > 끝위치 or Yuɓɓo_golle.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + keɓe.decode('utf-8', 'replace'))
                for 누름값, _ in 준비선택기.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: keɓe.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in keɓe or b'FAIL ' in keɓe: raise AssertionError(keɓe)
            return keɓe.decode('utf-8', 'replace').replace('\r\n', '\n')
        def laalagal(diidol):
            Yuɓɓo_golle.stdin.write(diidol.encode() + b'\n'); Yuɓɓo_golle.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in laalagal('ftpd start')
            fiilde_egginde_ceŋondiral = ftplib.FTP(); fiilde_egginde_ceŋondiral.encoding = 'utf-8'; fiilde_egginde_ceŋondiral.connect('127.0.0.1', 접속번호, timeout=20); fiilde_egginde_ceŋondiral.login()
            내용자료 = bytes(range(256)) * 32
            fiilde_egginde_ceŋondiral.storbinary('STOR binary.dat', io.BytesIO(내용자료))
            결과 = bytearray(); fiilde_egginde_ceŋondiral.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == 내용자료; assert fiilde_egginde_ceŋondiral.size('binary.dat') == len(내용자료)
            teeŋtingol_ciimtol['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            fiilde_egginde_ceŋondiral.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in laalagal('cat 한글.txt')
            assert '한글.txt' in fiilde_egginde_ceŋondiral.nlst()
            assert dict(fiilde_egginde_ceŋondiral.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            teeŋtingol_ciimtol['checks'].append('UTF-8 filename and content visible in guest shell')
            try: fiilde_egginde_ceŋondiral.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); fiilde_egginde_ceŋondiral.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == 내용자료
            teeŋtingol_ciimtol['checks'].append('oversized replacement rejected; previous file preserved')
            with fiilde_egginde_ceŋondiral.transfercmd('STOR pending.txt') as 올리기:
                # A control command must not change the active upload's destination.
                assert fiilde_egginde_ceŋondiral.size('binary.dat') == len(내용자료)
                올리기.sendall(b'UPLOAD TARGET PRESERVED')
            assert fiilde_egginde_ceŋondiral.voidresp().startswith('226')
            결과 = bytearray(); fiilde_egginde_ceŋondiral.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); fiilde_egginde_ceŋondiral.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == 내용자료
            fiilde_egginde_ceŋondiral.delete('pending.txt')
            teeŋtingol_ciimtol['checks'].append('interleaved SIZE cannot change the active STOR destination')
            fiilde_egginde_ceŋondiral.storbinary('STOR 인사.jar', io.BytesIO(ƴeewtirde.getvalue()))
            binndi = laalagal('java -jar 인사.jar 누리')
            assert 'JAR 실행: 누리' in binndi and '자체 aaluude_njaru fiilde' in binndi and 'exit 0' in binndi, binndi
            binndi = laalagal('./인사.jar 세상')
            assert 'JAR 실행: 세상' in binndi and 'exit 0' in binndi, binndi
            teeŋtingol_ciimtol['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct keɓe { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct keɓe njaru = {합(10), 1.25}; if (njaru.수 != 55 || njaru.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = udditde_fiilde("cc.txt", tar_winndu | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; winndude_fiilde_keɓe(문서, 인사, sizeof(인사)-1); uddude_fiilde(문서); winndude_fiilde_keɓe(1, 인사, sizeof(인사)-1); return 0; }\n'
            fiilde_egginde_ceŋondiral.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            binndi = laalagal('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in binndi and 'exit 0' in binndi, binndi
            binndi = laalagal('run 한글.elf'); assert 'CC NATIVE PASS' in binndi and 'exit 0' in binndi, binndi
            assert 'CC NATIVE PASS' in laalagal('cat cc.txt')
            실행파일 = bytearray(); fiilde_egginde_ceŋondiral.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            fiilde_egginde_ceŋondiral.storbinary('STOR waanjitaade_njaru.elf', io.BytesIO(실행파일)); binndi = laalagal('run waanjitaade_njaru.elf'); assert 'CC NATIVE PASS' in binndi and 'exit 0' in binndi, binndi
            fiilde_egginde_ceŋondiral.storbinary('STOR 실행', io.BytesIO(실행파일)); binndi=laalagal('./실행');assert 'CC NATIVE PASS' in binndi and 'exit 0' in binndi,binndi
            fiilde_egginde_ceŋondiral.storbinary('STOR innde.txt', io.BytesIO(실행파일)); binndi=laalagal('./innde.txt');assert 'CC NATIVE PASS' in binndi and 'exit 0' in binndi,binndi
            laalagal('rm 실행 innde.txt')
            teeŋtingol_ciimtol['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            laalagal('rm binary.dat 한글.txt 한글.c 한글.elf waanjitaade_njaru.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            fiilde_egginde_ceŋondiral.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            binndi=laalagal('./리눅스인사');assert 'exit -8' in binndi,binndi
            binndi=laalagal('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in binndi,binndi
            assert 'LINUX ELF FILE IO' in laalagal('cat linux.txt')
            fiilde_egginde_ceŋondiral.delete('리눅스인사');fiilde_egginde_ceŋondiral.delete('linux.txt')
            fiilde_egginde_ceŋondiral.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in laalagal('./거짓.elf');fiilde_egginde_ceŋondiral.delete('거짓.elf')
            teeŋtingol_ciimtol['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket seŋaade = 한국어.자체.연결통신.seŋaade("10.0.2.2", Integer.parseInt(args[0]));
 seŋaade.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] sewnde = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<sewnde.length;i++) if (seŋaade.getInputStream().read() != (sewnde[i]&255)) throw new RuntimeException("TCP mismatch");
 seŋaade.close();
 DatagramSocket 종단 = 한국어.자체.통신.udditde(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.neldude(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                fiilde_egginde_ceŋondiral.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                binndi = laalagal('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_poor, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in binndi and '10.0.2.2' in binndi and 'exit 0' in binndi, binndi
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            teeŋtingol_ciimtol['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            fiilde_egginde_ceŋondiral.delete('바깥통신.class')
            sarworde_sewnde=결과자료/'서버시험.java'
            sarworde_sewnde.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket sarworde_njaru = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket 손님 = sarworde_njaru.accept();
  손님.getOutputStream().write(손님.getInputStream().read()+1); 손님.close(); sarworde_njaru.close();
  byte[] loowdi_njaru = new byte[8]; DatagramPacket 전문 = new DatagramPacket(loowdi_njaru, loowdi_njaru.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(sarworde_sewnde)])
            fiilde_egginde_ceŋondiral.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            Yuɓɓo_golle.stdin.write('java 서버시험\n'.encode());Yuɓɓo_golle.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',sarworde_waraango_poor),timeout=5) as giƴiraaɗo_njaru:
                giƴiraaɗo_njaru.sendall(b'A');assert giƴiraaɗo_njaru.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as giƴiraaɗo_njaru:
                giƴiraaɗo_njaru.settimeout(5);giƴiraaɗo_njaru.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert giƴiraaɗo_njaru.recvfrom(512)[0]==b'UDP-IN'
            binndi=수신하기();assert 'INBOUND TCP UDP PASS' in binndi and 'exit 0' in binndi,binndi
            teeŋtingol_ciimtol['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            fiilde_egginde_ceŋondiral.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.fiilde.winndude("aot.txt", "한글 AOT fiilde 😀"); 한국어.자체.출력.winndude_diidol(한국어.자체.fiilde.읽기("aot.txt")); } }'
            fiilde_egginde_ceŋondiral.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            binndi = laalagal('javac 빛.java'); assert 'exit 0' in binndi and 'Compiled:' in binndi, binndi
            binndi = laalagal('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in binndi and 'exit 0' in binndi, binndi
            binndi = laalagal('run 빛.elf'); assert '\n55\n' in binndi and '한글 AOT fiilde 😀' in binndi and 'exit 0' in binndi, binndi
            자체실행파일 = bytearray(); fiilde_egginde_ceŋondiral.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            binndi = laalagal('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in binndi and 'unsupported' in binndi, binndi
            보존자료 = bytearray(); fiilde_egginde_ceŋondiral.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); fiilde_egginde_ceŋondiral.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            fiilde_egginde_ceŋondiral.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            binndi = laalagal('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in binndi and 'exit 0' in binndi, binndi
            binndi = laalagal('run 빛.elf'); assert '\n55\n' in binndi and '한글 AOT fiilde 😀' in binndi and 'exit 0' in binndi, binndi
            teeŋtingol_ciimtol['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            teeŋtingol_ciimtol['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ñiiɓ_sewnde=결과자료/'정적시험.java'
            ñiiɓ_sewnde.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] njaru = new int[] {기준, 합(10)};
  System.out.println(njaru[0] + njaru[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(ñiiɓ_sewnde)])
            fiilde_egginde_ceŋondiral.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            binndi=laalagal('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in binndi,binndi
            binndi=laalagal('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in binndi,binndi
            fiilde_egginde_ceŋondiral.delete('정적시험.class');fiilde_egginde_ceŋondiral.delete('정적시험.elf')
            teeŋtingol_ciimtol['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ƴeewtirde.getvalue());손상자료[14]^=1
            fiilde_egginde_ceŋondiral.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            binndi=laalagal('java -jar 인사.jar');assert 'Main-Class\nexit 1' in binndi,binndi
            teeŋtingol_ciimtol['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            fiilde_egginde_ceŋondiral.quit(); assert 'FTP stopped' in laalagal('ftpd stop')
            assert not 연결다리.juumre, 연결다리.juumre
            teeŋtingol_ciimtol.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in 준비선택기.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.fooftinde_saɗteende.set()
            Yuɓɓo_golle.terminate()
            try: Yuɓɓo_golle.wait(timeout=5)
            except subprocess.TimeoutExpired: Yuɓɓo_golle.kill(); Yuɓɓo_golle.wait()
            준비선택기.close(); Yuɓɓo_golle.stdin.close(); Yuɓɓo_golle.stdout.close()
            teeŋtingol_ciimtol['bridge_error'] = 연결다리.juumre
            teeŋtingol_ciimtol['frames_to_guest'] = 연결다리.커널수신틀수; teeŋtingol_ciimtol['frames_from_guest'] = 연결다리.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(연결다리.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(teeŋtingol_ciimtol, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': huutoraade()
