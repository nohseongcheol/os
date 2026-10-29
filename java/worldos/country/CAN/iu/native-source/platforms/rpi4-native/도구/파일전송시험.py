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
from 실행 import 기준, piqujijjut
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def 시작():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    naammannirainiq_unikkaaq = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.titiraq_titikutaak("JAR 실행: " + 인수[0]); 한국어.자체.ini.titiraq("jar.txt", "자체 kernel_atuutilik ini"); 한국어.자체.출력.titiraq_titikutaak(한국어.자체.ini.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    tuqqurli = io.BytesIO()
    with zipfile.ZipFile(tuqqurli, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); ikiaqqitittivik_ingirrania_aulataup_kapputigaq = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(접속번호, ['tcp:{}:9300'.format(ikiaqqitittivik_ingirrania_aulataup_kapputigaq), 'udp:{}:9301'.format(서버전문접속번호)], 포착여부=True) as 연결다리:
        Pivallianiq = subprocess.Popen(piqujijjut() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        준비선택기 = selectors.DefaultSelector(); 준비선택기.register(Pivallianiq.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            titiqqat = bytearray(); 끝위치 = time.monotonic() + 시간제한
            while 확인표시 not in titiqqat:
                if time.monotonic() > 끝위치 or Pivallianiq.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + titiqqat.decode('utf-8', 'replace'))
                for 누름값, _ in 준비선택기.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: titiqqat.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in titiqqat or b'FAIL ' in titiqqat: raise AssertionError(titiqqat)
            return titiqqat.decode('utf-8', 'replace').replace('\r\n', '\n')
        def piqujijjutiliriji(titikutaak):
            Pivallianiq.stdin.write(titikutaak.encode() + b'\n'); Pivallianiq.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in piqujijjutiliriji('ftpd start')
            ini_aullaaqtilli_kasuqsimaniq = ftplib.FTP(); ini_aullaaqtilli_kasuqsimaniq.encoding = 'utf-8'; ini_aullaaqtilli_kasuqsimaniq.connect('127.0.0.1', 접속번호, timeout=20); ini_aullaaqtilli_kasuqsimaniq.login()
            내용자료 = bytes(range(256)) * 32
            ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR binary.dat', io.BytesIO(내용자료))
            결과 = bytearray(); ini_aullaaqtilli_kasuqsimaniq.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == 내용자료; assert ini_aullaaqtilli_kasuqsimaniq.size('binary.dat') == len(내용자료)
            naammannirainiq_unikkaaq['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in piqujijjutiliriji('cat 한글.txt')
            assert '한글.txt' in ini_aullaaqtilli_kasuqsimaniq.nlst()
            assert dict(ini_aullaaqtilli_kasuqsimaniq.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            naammannirainiq_unikkaaq['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); ini_aullaaqtilli_kasuqsimaniq.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == 내용자료
            naammannirainiq_unikkaaq['checks'].append('oversized replacement rejected; previous file preserved')
            with ini_aullaaqtilli_kasuqsimaniq.transfercmd('STOR pending.txt') as 올리기:
                # A control command must not change the active upload's destination.
                assert ini_aullaaqtilli_kasuqsimaniq.size('binary.dat') == len(내용자료)
                올리기.sendall(b'UPLOAD TARGET PRESERVED')
            assert ini_aullaaqtilli_kasuqsimaniq.voidresp().startswith('226')
            결과 = bytearray(); ini_aullaaqtilli_kasuqsimaniq.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); ini_aullaaqtilli_kasuqsimaniq.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == 내용자료
            ini_aullaaqtilli_kasuqsimaniq.delete('pending.txt')
            naammannirainiq_unikkaaq['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR 인사.jar', io.BytesIO(tuqqurli.getvalue()))
            titiqqaq = piqujijjutiliriji('java -jar 인사.jar 누리')
            assert 'JAR 실행: 누리' in titiqqaq and '자체 kernel_atuutilik ini' in titiqqaq and 'exit 0' in titiqqaq, titiqqaq
            titiqqaq = piqujijjutiliriji('./인사.jar 세상')
            assert 'JAR 실행: 세상' in titiqqaq and 'exit 0' in titiqqaq, titiqqaq
            naammannirainiq_unikkaaq['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct titiqqat { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct titiqqat atuutilik = {합(10), 1.25}; if (atuutilik.수 != 55 || atuutilik.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = matuirli_ini("cc.txt", uqalimaarli_titirarli | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; titiraq_ini_titiqqat(문서, 인사, sizeof(인사)-1); matuli_ini(문서); titiraq_ini_titiqqat(1, 인사, sizeof(인사)-1); return 0; }\n'
            ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            titiqqaq = piqujijjutiliriji('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in titiqqaq and 'exit 0' in titiqqaq, titiqqaq
            titiqqaq = piqujijjutiliriji('run 한글.elf'); assert 'CC NATIVE PASS' in titiqqaq and 'exit 0' in titiqqaq, titiqqaq
            assert 'CC NATIVE PASS' in piqujijjutiliriji('cat cc.txt')
            실행파일 = bytearray(); ini_aullaaqtilli_kasuqsimaniq.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR ijjuarli_atuutilik.elf', io.BytesIO(실행파일)); titiqqaq = piqujijjutiliriji('run ijjuarli_atuutilik.elf'); assert 'CC NATIVE PASS' in titiqqaq and 'exit 0' in titiqqaq, titiqqaq
            ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR 실행', io.BytesIO(실행파일)); titiqqaq=piqujijjutiliriji('./실행');assert 'CC NATIVE PASS' in titiqqaq and 'exit 0' in titiqqaq,titiqqaq
            ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR atiq.txt', io.BytesIO(실행파일)); titiqqaq=piqujijjutiliriji('./atiq.txt');assert 'CC NATIVE PASS' in titiqqaq and 'exit 0' in titiqqaq,titiqqaq
            piqujijjutiliriji('rm 실행 atiq.txt')
            naammannirainiq_unikkaaq['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            piqujijjutiliriji('rm binary.dat 한글.txt 한글.c 한글.elf ijjuarli_atuutilik.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            titiqqaq=piqujijjutiliriji('./리눅스인사');assert 'exit -8' in titiqqaq,titiqqaq
            titiqqaq=piqujijjutiliriji('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in titiqqaq,titiqqaq
            assert 'LINUX ELF FILE IO' in piqujijjutiliriji('cat linux.txt')
            ini_aullaaqtilli_kasuqsimaniq.delete('리눅스인사');ini_aullaaqtilli_kasuqsimaniq.delete('linux.txt')
            ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in piqujijjutiliriji('./거짓.elf');ini_aullaaqtilli_kasuqsimaniq.delete('거짓.elf')
            naammannirainiq_unikkaaq['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket kasurli = 한국어.자체.연결통신.kasurli("10.0.2.2", Integer.parseInt(args[0]));
 kasurli.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] pivviujuq = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<pivviujuq.length;i++) if (kasurli.getInputStream().read() != (pivviujuq[i]&255)) throw new RuntimeException("TCP mismatch");
 kasurli.close();
 DatagramSocket 종단 = 한국어.자체.통신.matuirli(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.nassiutili(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                titiqqaq = piqujijjutiliriji('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_kapputigaq, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in titiqqaq and '10.0.2.2' in titiqqaq and 'exit 0' in titiqqaq, titiqqaq
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            naammannirainiq_unikkaaq['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ini_aullaaqtilli_kasuqsimaniq.delete('바깥통신.class')
            ikiaqqitittivik_pivviujuq=결과자료/'서버시험.java'
            ikiaqqitittivik_pivviujuq.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket ikiaqqitittivik_atuutilik = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket 손님 = ikiaqqitittivik_atuutilik.accept();
  손님.getOutputStream().write(손님.getInputStream().read()+1); 손님.close(); ikiaqqitittivik_atuutilik.close();
  byte[] Ilulingit_atuutilik = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Ilulingit_atuutilik, Ilulingit_atuutilik.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(ikiaqqitittivik_pivviujuq)])
            ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            Pivallianiq.stdin.write('java 서버시험\n'.encode());Pivallianiq.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',ikiaqqitittivik_ingirrania_aulataup_kapputigaq),timeout=5) as ilagijaujuq_atuutilik:
                ilagijaujuq_atuutilik.sendall(b'A');assert ilagijaujuq_atuutilik.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ilagijaujuq_atuutilik:
                ilagijaujuq_atuutilik.settimeout(5);ilagijaujuq_atuutilik.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert ilagijaujuq_atuutilik.recvfrom(512)[0]==b'UDP-IN'
            titiqqaq=수신하기();assert 'INBOUND TCP UDP PASS' in titiqqaq and 'exit 0' in titiqqaq,titiqqaq
            naammannirainiq_unikkaaq['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ini_aullaaqtilli_kasuqsimaniq.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.ini.titiraq("aot.txt", "한글 AOT ini 😀"); 한국어.자체.출력.titiraq_titikutaak(한국어.자체.ini.읽기("aot.txt")); } }'
            ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            titiqqaq = piqujijjutiliriji('javac 빛.java'); assert 'exit 0' in titiqqaq and 'Compiled:' in titiqqaq, titiqqaq
            titiqqaq = piqujijjutiliriji('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in titiqqaq and 'exit 0' in titiqqaq, titiqqaq
            titiqqaq = piqujijjutiliriji('run 빛.elf'); assert '\n55\n' in titiqqaq and '한글 AOT ini 😀' in titiqqaq and 'exit 0' in titiqqaq, titiqqaq
            자체실행파일 = bytearray(); ini_aullaaqtilli_kasuqsimaniq.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            titiqqaq = piqujijjutiliriji('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in titiqqaq and 'unsupported' in titiqqaq, titiqqaq
            보존자료 = bytearray(); ini_aullaaqtilli_kasuqsimaniq.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ini_aullaaqtilli_kasuqsimaniq.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            titiqqaq = piqujijjutiliriji('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in titiqqaq and 'exit 0' in titiqqaq, titiqqaq
            titiqqaq = piqujijjutiliriji('run 빛.elf'); assert '\n55\n' in titiqqaq and '한글 AOT ini 😀' in titiqqaq and 'exit 0' in titiqqaq, titiqqaq
            naammannirainiq_unikkaaq['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            naammannirainiq_unikkaaq['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            surravviqanngittuq_pivviujuq=결과자료/'정적시험.java'
            surravviqanngittuq_pivviujuq.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] atuutilik = new int[] {기준, 합(10)};
  System.out.println(atuutilik[0] + atuutilik[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(surravviqanngittuq_pivviujuq)])
            ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            titiqqaq=piqujijjutiliriji('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in titiqqaq,titiqqaq
            titiqqaq=piqujijjutiliriji('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in titiqqaq,titiqqaq
            ini_aullaaqtilli_kasuqsimaniq.delete('정적시험.class');ini_aullaaqtilli_kasuqsimaniq.delete('정적시험.elf')
            naammannirainiq_unikkaaq['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(tuqqurli.getvalue());손상자료[14]^=1
            ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            titiqqaq=piqujijjutiliriji('java -jar 인사.jar');assert 'Main-Class\nexit 1' in titiqqaq,titiqqaq
            naammannirainiq_unikkaaq['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ini_aullaaqtilli_kasuqsimaniq.quit(); assert 'FTP stopped' in piqujijjutiliriji('ftpd stop')
            assert not 연결다리.tammarniq, 연결다리.tammarniq
            naammannirainiq_unikkaaq.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in 준비선택기.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.nuqqakiainnarli_piniku.set()
            Pivallianiq.terminate()
            try: Pivallianiq.wait(timeout=5)
            except subprocess.TimeoutExpired: Pivallianiq.kill(); Pivallianiq.wait()
            준비선택기.close(); Pivallianiq.stdin.close(); Pivallianiq.stdout.close()
            naammannirainiq_unikkaaq['bridge_error'] = 연결다리.tammarniq
            naammannirainiq_unikkaaq['frames_to_guest'] = 연결다리.커널수신틀수; naammannirainiq_unikkaaq['frames_from_guest'] = 연결다리.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(연결다리.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(naammannirainiq_unikkaaq, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': 시작()
