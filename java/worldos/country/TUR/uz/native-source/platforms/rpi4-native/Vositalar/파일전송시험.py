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
from bajarmoq_buyruq import Project_ildiz, Buyruq
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Bajarish():
    o_lchov_ma_lumotlar = Project_ildiz / 'build/verification/ftp'; o_lchov_ma_lumotlar.mkdir(parents=True, exist_ok=True)
    tasdiq_hisobot = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Project_ildiz / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = o_lchov_ma_lumotlar / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.yozmoq_satr("JAR bajarmoq_buyruq: " + 인수[0]); 한국어.자체.Fayl.Yozish("jar.txt", "자체 o_zak_VALUE Fayl"); 한국어.자체.출력.yozmoq_satr(한국어.자체.Fayl.Oʻqish("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_ildiz/'build/java-library/classes'), '-d', str(o_lchov_ma_lumotlar), str(자바원문)])
    Arxiv = io.BytesIO()
    with zipfile.ZipFile(Arxiv, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(o_lchov_ma_lumotlar/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_oqim_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(접속번호, ['tcp:{}:9300'.format(server_oqim_port), 'udp:{}:9301'.format(서버전문접속번호)], olish=True) as 연결다리:
        Jarayon = subprocess.Popen(Buyruq() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        tanlagich = selectors.DefaultSelector(); tanlagich.register(Jarayon.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            ma_lumotlar = bytearray(); to_xtatmoq_OFFSET = time.monotonic() + 시간제한
            while 확인표시 not in ma_lumotlar:
                if time.monotonic() > to_xtatmoq_OFFSET or Jarayon.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + ma_lumotlar.decode('utf-8', 'replace'))
                for 누름값, _ in tanlagich.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: ma_lumotlar.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ma_lumotlar or b'FAIL ' in ma_lumotlar: raise AssertionError(ma_lumotlar)
            return ma_lumotlar.decode('utf-8', 'replace').replace('\r\n', '\n')
        def qobiq(satr):
            Jarayon.stdin.write(satr.encode() + b'\n'); Jarayon.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in qobiq('ftpd start')
            fayl_uzatish_aloqa = ftplib.FTP(); fayl_uzatish_aloqa.encoding = 'utf-8'; fayl_uzatish_aloqa.connect('127.0.0.1', 접속번호, timeout=20); fayl_uzatish_aloqa.login()
            foydali_yuklanma_ma_lumotlar = bytes(range(256)) * 32
            fayl_uzatish_aloqa.storbinary('STOR binary.dat', io.BytesIO(foydali_yuklanma_ma_lumotlar))
            o_lchov = bytearray(); fayl_uzatish_aloqa.retrbinary('RETR binary.dat', o_lchov.extend)
            assert o_lchov == foydali_yuklanma_ma_lumotlar; assert fayl_uzatish_aloqa.size('binary.dat') == len(foydali_yuklanma_ma_lumotlar)
            tasdiq_hisobot['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            fayl_uzatish_aloqa.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in qobiq('cat 한글.txt')
            assert '한글.txt' in fayl_uzatish_aloqa.nlst()
            assert dict(fayl_uzatish_aloqa.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            tasdiq_hisobot['checks'].append('UTF-8 filename and content visible in guest shell')
            try: fayl_uzatish_aloqa.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            o_lchov = bytearray(); fayl_uzatish_aloqa.retrbinary('RETR binary.dat', o_lchov.extend); assert o_lchov == foydali_yuklanma_ma_lumotlar
            tasdiq_hisobot['checks'].append('oversized replacement rejected; previous file preserved')
            with fayl_uzatish_aloqa.transfercmd('STOR pending.txt') as uzatmoq_Fayllar:
                # A control command must not change the active upload's destination.
                assert fayl_uzatish_aloqa.size('binary.dat') == len(foydali_yuklanma_ma_lumotlar)
                uzatmoq_Fayllar.sendall(b'UPLOAD TARGET PRESERVED')
            assert fayl_uzatish_aloqa.voidresp().startswith('226')
            o_lchov = bytearray(); fayl_uzatish_aloqa.retrbinary('RETR pending.txt', o_lchov.extend)
            assert o_lchov == b'UPLOAD TARGET PRESERVED'
            o_lchov = bytearray(); fayl_uzatish_aloqa.retrbinary('RETR binary.dat', o_lchov.extend)
            assert o_lchov == foydali_yuklanma_ma_lumotlar
            fayl_uzatish_aloqa.delete('pending.txt')
            tasdiq_hisobot['checks'].append('interleaved SIZE cannot change the active STOR destination')
            fayl_uzatish_aloqa.storbinary('STOR 인사.jar', io.BytesIO(Arxiv.getvalue()))
            Matn = qobiq('java -jar 인사.jar 누리')
            assert 'JAR bajarmoq_buyruq: 누리' in Matn and '자체 o_zak_VALUE Fayl' in Matn and 'exit 0' in Matn, Matn
            Matn = qobiq('./인사.jar 세상')
            assert 'JAR bajarmoq_buyruq: 세상' in Matn and 'exit 0' in Matn, Matn
            tasdiq_hisobot['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct ma_lumotlar { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct ma_lumotlar VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ochmoq_fayl("cc.txt", o_qish_yozish_mumkin | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; yozmoq_fayl_ma_lumotlar(문서, 인사, sizeof(인사)-1); yopmoq_fayl(문서); yozmoq_fayl_ma_lumotlar(1, 인사, sizeof(인사)-1); return 0; }\n'
            fayl_uzatish_aloqa.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Matn = qobiq('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Matn and 'exit 0' in Matn, Matn
            Matn = qobiq('run 한글.elf'); assert 'CC NATIVE PASS' in Matn and 'exit 0' in Matn, Matn
            assert 'CC NATIVE PASS' in qobiq('cat cc.txt')
            실행파일 = bytearray(); fayl_uzatish_aloqa.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            fayl_uzatish_aloqa.storbinary('STOR namuna_VALUE.elf', io.BytesIO(실행파일)); Matn = qobiq('run namuna_VALUE.elf'); assert 'CC NATIVE PASS' in Matn and 'exit 0' in Matn, Matn
            fayl_uzatish_aloqa.storbinary('STOR bajarmoq_buyruq', io.BytesIO(실행파일)); Matn=qobiq('./bajarmoq_buyruq');assert 'CC NATIVE PASS' in Matn and 'exit 0' in Matn,Matn
            fayl_uzatish_aloqa.storbinary('STOR Nomi.txt', io.BytesIO(실행파일)); Matn=qobiq('./Nomi.txt');assert 'CC NATIVE PASS' in Matn and 'exit 0' in Matn,Matn
            qobiq('rm bajarmoq_buyruq Nomi.txt')
            tasdiq_hisobot['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            qobiq('rm binary.dat 한글.txt 한글.c 한글.elf namuna_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(o_lchov_ma_lumotlar/'linux-reference')
            fayl_uzatish_aloqa.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Matn=qobiq('./리눅스인사');assert 'exit -8' in Matn,Matn
            Matn=qobiq('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Matn,Matn
            assert 'LINUX ELF FILE IO' in qobiq('cat linux.txt')
            fayl_uzatish_aloqa.delete('리눅스인사');fayl_uzatish_aloqa.delete('linux.txt')
            fayl_uzatish_aloqa.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in qobiq('./FALSE_VALUE.elf');fayl_uzatish_aloqa.delete('FALSE_VALUE.elf')
            tasdiq_hisobot['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = o_lchov_ma_lumotlar/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Ulanish = 한국어.자체.연결통신.Ulanish("10.0.2.2", Integer.parseInt(args[0]));
 Ulanish.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] manba = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<manba.length;i++) if (Ulanish.getInputStream().read() != (manba[i]&255)) throw new RuntimeException("TCP mismatch");
 Ulanish.close();
 DatagramSocket 종단 = 한국어.자체.통신.Ochish(0); 한국어.자체.통신.TANAFFUS(종단, 500);
 한국어.자체.통신.yuborish(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_ildiz/'build/java-library/classes'),'-d',str(o_lchov_ma_lumotlar),str(통신원문)])
                fayl_uzatish_aloqa.storbinary('STOR 바깥통신.class', io.BytesIO((o_lchov_ma_lumotlar/'바깥통신.class').read_bytes()))
                Matn = qobiq('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_bayonnomasi_port, 되돌림서버항목.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in Matn and '10.0.2.2' in Matn and 'exit 0' in Matn, Matn
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            tasdiq_hisobot['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            fayl_uzatish_aloqa.delete('바깥통신.class')
            server_manba=o_lchov_ma_lumotlar/'서버시험.java'
            server_manba.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket mehmon_VALUE = server_VALUE.accept();
  mehmon_VALUE.getOutputStream().write(mehmon_VALUE.getInputStream().read()+1); mehmon_VALUE.close(); server_VALUE.close();
  byte[] tarkib_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(tarkib_VALUE, tarkib_VALUE.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(o_lchov_ma_lumotlar),str(server_manba)])
            fayl_uzatish_aloqa.storbinary('STOR 서버시험.class',io.BytesIO((o_lchov_ma_lumotlar/'서버시험.class').read_bytes()))
            Jarayon.stdin.write('java 서버시험\n'.encode());Jarayon.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_oqim_port),timeout=5) as bir_rangli_VALUE:
                bir_rangli_VALUE.sendall(b'A');assert bir_rangli_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as bir_rangli_VALUE:
                bir_rangli_VALUE.settimeout(5);bir_rangli_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert bir_rangli_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Matn=수신하기();assert 'INBOUND TCP UDP PASS' in Matn and 'exit 0' in Matn,Matn
            tasdiq_hisobot['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            fayl_uzatish_aloqa.delete('서버시험.class')
            qo_llanma_SEQUENCE = 'public class 빛 { public static void main(String[] 인수) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(SUM_VALUE); 한국어.자체.Fayl.Yozish("aot.txt", "한글 AOT Fayl 😀"); 한국어.자체.출력.yozmoq_satr(한국어.자체.Fayl.Oʻqish("aot.txt")); } }'
            fayl_uzatish_aloqa.storbinary('STOR 빛.java', io.BytesIO(qo_llanma_SEQUENCE.encode()))
            Matn = qobiq('javac 빛.java'); assert 'exit 0' in Matn and 'Compiled:' in Matn, Matn
            Matn = qobiq('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Matn and 'exit 0' in Matn, Matn
            Matn = qobiq('run 빛.elf'); assert '\n55\n' in Matn and '한글 AOT Fayl 😀' in Matn and 'exit 0' in Matn, Matn
            자체실행파일 = bytearray(); fayl_uzatish_aloqa.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Matn = qobiq('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Matn and 'unsupported' in Matn, Matn
            보존자료 = bytearray(); fayl_uzatish_aloqa.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); fayl_uzatish_aloqa.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            fayl_uzatish_aloqa.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Matn = qobiq('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Matn and 'exit 0' in Matn, Matn
            Matn = qobiq('run 빛.elf'); assert '\n55\n' in Matn and '한글 AOT Fayl 😀' in Matn and 'exit 0' in Matn, Matn
            tasdiq_hisobot['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            tasdiq_hisobot['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statik_manba=o_lchov_ma_lumotlar/'정적시험.java'
            statik_manba.write_text('''public class 정적시험 {
 static int Project_ildiz = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] 인수) {
  int[] VALUE = new int[] {Project_ildiz, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(o_lchov_ma_lumotlar),str(statik_manba)])
            fayl_uzatish_aloqa.storbinary('STOR 정적시험.class',io.BytesIO((o_lchov_ma_lumotlar/'정적시험.class').read_bytes()))
            Matn=qobiq('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Matn,Matn
            Matn=qobiq('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Matn,Matn
            fayl_uzatish_aloqa.delete('정적시험.class');fayl_uzatish_aloqa.delete('정적시험.elf')
            tasdiq_hisobot['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arxiv.getvalue());손상자료[14]^=1
            fayl_uzatish_aloqa.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Matn=qobiq('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Matn,Matn
            tasdiq_hisobot['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            fayl_uzatish_aloqa.quit(); assert 'FTP stopped' in qobiq('ftpd stop')
            assert not 연결다리.Xato, 연결다리.Xato
            tasdiq_hisobot.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in tanlagich.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.to_xtamoq_hodisa.set()
            Jarayon.terminate()
            try: Jarayon.wait(timeout=5)
            except subprocess.TimeoutExpired: Jarayon.kill(); Jarayon.wait()
            tanlagich.close(); Jarayon.stdin.close(); Jarayon.stdout.close()
            tasdiq_hisobot['bridge_error'] = 연결다리.Xato
            tasdiq_hisobot['frames_to_guest'] = 연결다리.커널수신틀수; tasdiq_hisobot['frames_from_guest'] = 연결다리.커널발신틀수
            (o_lchov_ma_lumotlar/'packets.json').write_text(json.dumps(연결다리.iz_LOG,indent=2)+'\n')
            (o_lchov_ma_lumotlar / 'serial.log').write_bytes(대화기록)
            (o_lchov_ma_lumotlar / 'report.json').write_text(json.dumps(tasdiq_hisobot, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Bajarish()
