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
from Alásopọ̀_afará import Alásopọ̀_afará
from ṣiṣẹ́_àṣẹ import 기준, Àṣẹ
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Rọ́ọ̀nù():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    Àfọwọ́sí_ìjábọ̀ = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.kọ_ìlà("JAR ṣiṣẹ́_àṣẹ: " + 인수[0]); 한국어.자체.Fáìlì.Kọ("jar.txt", "자체 kánẹ́ẹ̀lì_iye Fáìlì"); 한국어.자체.출력.kọ_ìlà(한국어.자체.Fáìlì.Kàá("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    Ìpamọ_ọlọ́jọ́pípẹ́ = io.BytesIO()
    with zipfile.ZipFile(Ìpamọ_ọlọ́jọ́pípẹ́, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); apèsè_Stream_ojú = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Alásopọ̀_afará(접속번호, ['tcp:{}:9300'.format(apèsè_Stream_ojú), 'udp:{}:9301'.format(서버전문접속번호)], gbàwòránsílẹ̀=True) as afará:
        Ìlànà = subprocess.Popen(Àṣẹ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + afará.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        olùyàn = selectors.DefaultSelector(); olùyàn.register(Ìlànà.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            détà = bytearray(); parí_Ìtayọ = time.monotonic() + 시간제한
            while 확인표시 not in détà:
                if time.monotonic() > parí_Ìtayọ or Ìlànà.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + détà.decode('utf-8', 'replace'))
                for 누름값, _ in olùyàn.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: détà.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in détà or b'FAIL ' in détà: raise AssertionError(détà)
            return détà.decode('utf-8', 'replace').replace('\r\n', '\n')
        def ṣẹ́ẹ̀lì(ìlà):
            Ìlànà.stdin.write(ìlà.encode() + b'\n'); Ìlànà.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in ṣẹ́ẹ̀lì('ftpd start')
            fáìlì_ṣàgbélọ_Ìsomọ́ = ftplib.FTP(); fáìlì_ṣàgbélọ_Ìsomọ́.encoding = 'utf-8'; fáìlì_ṣàgbélọ_Ìsomọ́.connect('127.0.0.1', 접속번호, timeout=20); fáìlì_ṣàgbélọ_Ìsomọ́.login()
            ojúlówó_détà_détà = bytes(range(256)) * 32
            fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR binary.dat', io.BytesIO(ojúlówó_détà_détà))
            결과 = bytearray(); fáìlì_ṣàgbélọ_Ìsomọ́.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ojúlówó_détà_détà; assert fáìlì_ṣàgbélọ_Ìsomọ́.size('binary.dat') == len(ojúlówó_détà_détà)
            Àfọwọ́sí_ìjábọ̀['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in ṣẹ́ẹ̀lì('cat 한글.txt')
            assert '한글.txt' in fáìlì_ṣàgbélọ_Ìsomọ́.nlst()
            assert dict(fáìlì_ṣàgbélọ_Ìsomọ́.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            Àfọwọ́sí_ìjábọ̀['checks'].append('UTF-8 filename and content visible in guest shell')
            try: fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); fáìlì_ṣàgbélọ_Ìsomọ́.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == ojúlówó_détà_détà
            Àfọwọ́sí_ìjábọ̀['checks'].append('oversized replacement rejected; previous file preserved')
            with fáìlì_ṣàgbélọ_Ìsomọ́.transfercmd('STOR pending.txt') as fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì:
                # A control command must not change the active upload's destination.
                assert fáìlì_ṣàgbélọ_Ìsomọ́.size('binary.dat') == len(ojúlówó_détà_détà)
                fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì.sendall(b'UPLOAD TARGET PRESERVED')
            assert fáìlì_ṣàgbélọ_Ìsomọ́.voidresp().startswith('226')
            결과 = bytearray(); fáìlì_ṣàgbélọ_Ìsomọ́.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); fáìlì_ṣàgbélọ_Ìsomọ́.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ojúlówó_détà_détà
            fáìlì_ṣàgbélọ_Ìsomọ́.delete('pending.txt')
            Àfọwọ́sí_ìjábọ̀['checks'].append('interleaved SIZE cannot change the active STOR destination')
            fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR 인사.jar', io.BytesIO(Ìpamọ_ọlọ́jọ́pípẹ́.getvalue()))
            SMS = ṣẹ́ẹ̀lì('java -jar 인사.jar 누리')
            assert 'JAR ṣiṣẹ́_àṣẹ: 누리' in SMS and '자체 kánẹ́ẹ̀lì_iye Fáìlì' in SMS and 'exit 0' in SMS, SMS
            SMS = ṣẹ́ẹ̀lì('./인사.jar 세상')
            assert 'JAR ṣiṣẹ́_àṣẹ: 세상' in SMS and 'exit 0' in SMS, SMS
            Àfọwọ́sí_ìjábọ̀['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct détà { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct détà iye = {합(10), 1.25}; if (iye.수 != 55 || iye.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ṣí_fáìlì("cc.txt", tí_a_lè_kà_tí_a_lè_kọ | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; kọ_fáìlì_détà(문서, 인사, sizeof(인사)-1); pa_dé_fáìlì(문서); kọ_fáìlì_détà(1, 인사, sizeof(인사)-1); return 0; }\n'
            fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            SMS = ṣẹ́ẹ̀lì('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = ṣẹ́ẹ̀lì('run 한글.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            assert 'CC NATIVE PASS' in ṣẹ́ẹ̀lì('cat cc.txt')
            실행파일 = bytearray(); fáìlì_ṣàgbélọ_Ìsomọ́.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR ṣẹ̀dà_iye.elf', io.BytesIO(실행파일)); SMS = ṣẹ́ẹ̀lì('run ṣẹ̀dà_iye.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR ṣiṣẹ́_àṣẹ', io.BytesIO(실행파일)); SMS=ṣẹ́ẹ̀lì('./ṣiṣẹ́_àṣẹ');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR Orúkọ.txt', io.BytesIO(실행파일)); SMS=ṣẹ́ẹ̀lì('./Orúkọ.txt');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            ṣẹ́ẹ̀lì('rm ṣiṣẹ́_àṣẹ Orúkọ.txt')
            Àfọwọ́sí_ìjábọ̀['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            ṣẹ́ẹ̀lì('rm binary.dat 한글.txt 한글.c 한글.elf ṣẹ̀dà_iye.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            SMS=ṣẹ́ẹ̀lì('./리눅스인사');assert 'exit -8' in SMS,SMS
            SMS=ṣẹ́ẹ̀lì('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in SMS,SMS
            assert 'LINUX ELF FILE IO' in ṣẹ́ẹ̀lì('cat linux.txt')
            fáìlì_ṣàgbélọ_Ìsomọ́.delete('리눅스인사');fáìlì_ṣàgbélọ_Ìsomọ́.delete('linux.txt')
            fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in ṣẹ́ẹ̀lì('./거짓.elf');fáìlì_ṣàgbélọ_Ìsomọ́.delete('거짓.elf')
            Àfọwọ́sí_ìjábọ̀['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Darapọ̀ = 한국어.자체.연결통신.Darapọ̀("10.0.2.2", Integer.parseInt(args[0]));
 Darapọ̀.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] orísun = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<orísun.length;i++) if (Darapọ̀.getInputStream().read() != (orísun[i]&255)) throw new RuntimeException("TCP mismatch");
 Darapọ̀.close();
 DatagramSocket 종단 = 한국어.자체.통신.Ṣi(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.í_meèlì(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                SMS = ṣẹ́ẹ̀lì('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_ojú, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in SMS and '10.0.2.2' in SMS and 'exit 0' in SMS, SMS
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            Àfọwọ́sí_ìjábọ̀['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            fáìlì_ṣàgbélọ_Ìsomọ́.delete('바깥통신.class')
            apèsè_orísun=결과자료/'서버시험.java'
            apèsè_orísun.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket apèsè_iye = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket àlejò_iye = apèsè_iye.accept();
  àlejò_iye.getOutputStream().write(àlejò_iye.getInputStream().read()+1); àlejò_iye.close(); apèsè_iye.close();
  byte[] Àkóónú_iye = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Àkóónú_iye, Àkóónú_iye.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(apèsè_orísun)])
            fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            Ìlànà.stdin.write('java 서버시험\n'.encode());Ìlànà.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',apèsè_Stream_ojú),timeout=5) as ọ̀gbà_iye:
                ọ̀gbà_iye.sendall(b'A');assert ọ̀gbà_iye.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ọ̀gbà_iye:
                ọ̀gbà_iye.settimeout(5);ọ̀gbà_iye.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert ọ̀gbà_iye.recvfrom(512)[0]==b'UDP-IN'
            SMS=수신하기();assert 'INBOUND TCP UDP PASS' in SMS and 'exit 0' in SMS,SMS
            Àfọwọ́sí_ìjábọ̀['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            fáìlì_ṣàgbélọ_Ìsomọ́.delete('서버시험.class')
            ìtọ́sọ́nà_ÀTẸ̀LÉRA = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.Fáìlì.Kọ("aot.txt", "한글 AOT Fáìlì 😀"); 한국어.자체.출력.kọ_ìlà(한국어.자체.Fáìlì.Kàá("aot.txt")); } }'
            fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR 빛.java', io.BytesIO(ìtọ́sọ́nà_ÀTẸ̀LÉRA.encode()))
            SMS = ṣẹ́ẹ̀lì('javac 빛.java'); assert 'exit 0' in SMS and 'Compiled:' in SMS, SMS
            SMS = ṣẹ́ẹ̀lì('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = ṣẹ́ẹ̀lì('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT Fáìlì 😀' in SMS and 'exit 0' in SMS, SMS
            자체실행파일 = bytearray(); fáìlì_ṣàgbélọ_Ìsomọ́.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            SMS = ṣẹ́ẹ̀lì('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in SMS and 'unsupported' in SMS, SMS
            보존자료 = bytearray(); fáìlì_ṣàgbélọ_Ìsomọ́.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); fáìlì_ṣàgbélọ_Ìsomọ́.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            SMS = ṣẹ́ẹ̀lì('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = ṣẹ́ẹ̀lì('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT Fáìlì 😀' in SMS and 'exit 0' in SMS, SMS
            Àfọwọ́sí_ìjábọ̀['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            Àfọwọ́sí_ìjábọ̀['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ìdágún_orísun=결과자료/'정적시험.java'
            ìdágún_orísun.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] iye = new int[] {기준, 합(10)};
  System.out.println(iye[0] + iye[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(ìdágún_orísun)])
            fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            SMS=ṣẹ́ẹ̀lì('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in SMS,SMS
            SMS=ṣẹ́ẹ̀lì('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in SMS,SMS
            fáìlì_ṣàgbélọ_Ìsomọ́.delete('정적시험.class');fáìlì_ṣàgbélọ_Ìsomọ́.delete('정적시험.elf')
            Àfọwọ́sí_ìjábọ̀['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Ìpamọ_ọlọ́jọ́pípẹ́.getvalue());손상자료[14]^=1
            fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            SMS=ṣẹ́ẹ̀lì('java -jar 인사.jar');assert 'Main-Class\nexit 1' in SMS,SMS
            Àfọwọ́sí_ìjábọ̀['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            fáìlì_ṣàgbélọ_Ìsomọ́.quit(); assert 'FTP stopped' in ṣẹ́ẹ̀lì('ftpd stop')
            assert not afará.àṣìṣe, afará.àṣìṣe
            Àfọwọ́sí_ìjábọ̀.update(passed=True, frames_to_guest=afará.커널수신틀수, frames_from_guest=afará.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in olùyàn.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            afará.dúró_díẹ̀_ìgbéṣẹ̀.set()
            Ìlànà.terminate()
            try: Ìlànà.wait(timeout=5)
            except subprocess.TimeoutExpired: Ìlànà.kill(); Ìlànà.wait()
            olùyàn.close(); Ìlànà.stdin.close(); Ìlànà.stdout.close()
            Àfọwọ́sí_ìjábọ̀['bridge_error'] = afará.àṣìṣe
            Àfọwọ́sí_ìjábọ̀['frames_to_guest'] = afará.커널수신틀수; Àfọwọ́sí_ìjábọ̀['frames_from_guest'] = afará.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(afará.àròpọ̀_mátirísì_adọ́gbaníhà_àkọsílẹ̀_ìṣe,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(Àfọwọ́sí_ìjábọ̀, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Rọ́ọ̀nù()
