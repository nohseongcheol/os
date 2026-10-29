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
from ýerine_ýetir_buýruk import 기준, buýruk
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Bitir():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    barlag_hasabat = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.ýaz_setir("JAR ýerine_ýetir_buýruk: " + 인수[0]); 한국어.자체.Faýl.Ýaz("jar.txt", "자체 ýadro_baha Faýl"); 한국어.자체.출력.ýaz_setir(한국어.자체.Faýl.Oka("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    Arhiw = io.BytesIO()
    with zipfile.ZipFile(Arhiw, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); serwer_Stream_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(접속번호, ['tcp:{}:9300'.format(serwer_Stream_port), 'udp:{}:9301'.format(서버전문접속번호)], düşüriş=True) as 연결다리:
        Proses = subprocess.Popen(buýruk() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        saýlaýjy = selectors.DefaultSelector(); saýlaýjy.register(Proses.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            maglumat = bytearray(); tamamla_Süýşüriş = time.monotonic() + 시간제한
            while 확인표시 not in maglumat:
                if time.monotonic() > tamamla_Süýşüriş or Proses.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + maglumat.decode('utf-8', 'replace'))
                for 누름값, _ in saýlaýjy.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: maglumat.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in maglumat or b'FAIL ' in maglumat: raise AssertionError(maglumat)
            return maglumat.decode('utf-8', 'replace').replace('\r\n', '\n')
        def gabyjak(setir):
            Proses.stdin.write(setir.encode() + b'\n'); Proses.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in gabyjak('ftpd start')
            faýl_geçir_birikme = ftplib.FTP(); faýl_geçir_birikme.encoding = 'utf-8'; faýl_geçir_birikme.connect('127.0.0.1', 접속번호, timeout=20); faýl_geçir_birikme.login()
            ýük_gutujygy_maglumat = bytes(range(256)) * 32
            faýl_geçir_birikme.storbinary('STOR binary.dat', io.BytesIO(ýük_gutujygy_maglumat))
            결과 = bytearray(); faýl_geçir_birikme.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ýük_gutujygy_maglumat; assert faýl_geçir_birikme.size('binary.dat') == len(ýük_gutujygy_maglumat)
            barlag_hasabat['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            faýl_geçir_birikme.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in gabyjak('cat 한글.txt')
            assert '한글.txt' in faýl_geçir_birikme.nlst()
            assert dict(faýl_geçir_birikme.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            barlag_hasabat['checks'].append('UTF-8 filename and content visible in guest shell')
            try: faýl_geçir_birikme.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); faýl_geçir_birikme.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == ýük_gutujygy_maglumat
            barlag_hasabat['checks'].append('oversized replacement rejected; previous file preserved')
            with faýl_geçir_birikme.transfercmd('STOR pending.txt') as ýükle_Faýllar:
                # A control command must not change the active upload's destination.
                assert faýl_geçir_birikme.size('binary.dat') == len(ýük_gutujygy_maglumat)
                ýükle_Faýllar.sendall(b'UPLOAD TARGET PRESERVED')
            assert faýl_geçir_birikme.voidresp().startswith('226')
            결과 = bytearray(); faýl_geçir_birikme.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); faýl_geçir_birikme.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ýük_gutujygy_maglumat
            faýl_geçir_birikme.delete('pending.txt')
            barlag_hasabat['checks'].append('interleaved SIZE cannot change the active STOR destination')
            faýl_geçir_birikme.storbinary('STOR 인사.jar', io.BytesIO(Arhiw.getvalue()))
            Metin = gabyjak('java -jar 인사.jar 누리')
            assert 'JAR ýerine_ýetir_buýruk: 누리' in Metin and '자체 ýadro_baha Faýl' in Metin and 'exit 0' in Metin, Metin
            Metin = gabyjak('./인사.jar 세상')
            assert 'JAR ýerine_ýetir_buýruk: 세상' in Metin and 'exit 0' in Metin, Metin
            barlag_hasabat['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct maglumat { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct maglumat baha = {합(10), 1.25}; if (baha.수 != 55 || baha.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = aç_faýl("cc.txt", okalýan_ýazylýan | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; ýaz_faýl_maglumat(문서, 인사, sizeof(인사)-1); ýap_faýl(문서); ýaz_faýl_maglumat(1, 인사, sizeof(인사)-1); return 0; }\n'
            faýl_geçir_birikme.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Metin = gabyjak('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Metin and 'exit 0' in Metin, Metin
            Metin = gabyjak('run 한글.elf'); assert 'CC NATIVE PASS' in Metin and 'exit 0' in Metin, Metin
            assert 'CC NATIVE PASS' in gabyjak('cat cc.txt')
            실행파일 = bytearray(); faýl_geçir_birikme.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            faýl_geçir_birikme.storbinary('STOR synp_baha.elf', io.BytesIO(실행파일)); Metin = gabyjak('run synp_baha.elf'); assert 'CC NATIVE PASS' in Metin and 'exit 0' in Metin, Metin
            faýl_geçir_birikme.storbinary('STOR ýerine_ýetir_buýruk', io.BytesIO(실행파일)); Metin=gabyjak('./ýerine_ýetir_buýruk');assert 'CC NATIVE PASS' in Metin and 'exit 0' in Metin,Metin
            faýl_geçir_birikme.storbinary('STOR Ad.txt', io.BytesIO(실행파일)); Metin=gabyjak('./Ad.txt');assert 'CC NATIVE PASS' in Metin and 'exit 0' in Metin,Metin
            gabyjak('rm ýerine_ýetir_buýruk Ad.txt')
            barlag_hasabat['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            gabyjak('rm binary.dat 한글.txt 한글.c 한글.elf synp_baha.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            faýl_geçir_birikme.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Metin=gabyjak('./리눅스인사');assert 'exit -8' in Metin,Metin
            Metin=gabyjak('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Metin,Metin
            assert 'LINUX ELF FILE IO' in gabyjak('cat linux.txt')
            faýl_geçir_birikme.delete('리눅스인사');faýl_geçir_birikme.delete('linux.txt')
            faýl_geçir_birikme.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in gabyjak('./거짓.elf');faýl_geçir_birikme.delete('거짓.elf')
            barlag_hasabat['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Birikme = 한국어.자체.연결통신.Birikme("10.0.2.2", Integer.parseInt(args[0]));
 Birikme.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] Çeşme = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<Çeşme.length;i++) if (Birikme.getInputStream().read() != (Çeşme[i]&255)) throw new RuntimeException("TCP mismatch");
 Birikme.close();
 DatagramSocket 종단 = 한국어.자체.통신.Aç(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.iber(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                faýl_geçir_birikme.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                Metin = gabyjak('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_port, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in Metin and '10.0.2.2' in Metin and 'exit 0' in Metin, Metin
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            barlag_hasabat['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            faýl_geçir_birikme.delete('바깥통신.class')
            serwer_gor=결과자료/'서버시험.java'
            serwer_gor.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket serwer_baha = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket 손님 = serwer_baha.accept();
  손님.getOutputStream().write(손님.getInputStream().read()+1); 손님.close(); serwer_baha.close();
  byte[] Mazmun_baha = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Mazmun_baha, Mazmun_baha.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(serwer_gor)])
            faýl_geçir_birikme.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            Proses.stdin.write('java 서버시험\n'.encode());Proses.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',serwer_Stream_port),timeout=5) as deň_derejeli_düwün_baha:
                deň_derejeli_düwün_baha.sendall(b'A');assert deň_derejeli_düwün_baha.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as deň_derejeli_düwün_baha:
                deň_derejeli_düwün_baha.settimeout(5);deň_derejeli_düwün_baha.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert deň_derejeli_düwün_baha.recvfrom(512)[0]==b'UDP-IN'
            Metin=수신하기();assert 'INBOUND TCP UDP PASS' in Metin and 'exit 0' in Metin,Metin
            barlag_hasabat['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            faýl_geçir_birikme.delete('서버시험.class')
            instruksiýa_SEQUENCE = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.Faýl.Ýaz("aot.txt", "한글 AOT Faýl 😀"); 한국어.자체.출력.ýaz_setir(한국어.자체.Faýl.Oka("aot.txt")); } }'
            faýl_geçir_birikme.storbinary('STOR 빛.java', io.BytesIO(instruksiýa_SEQUENCE.encode()))
            Metin = gabyjak('javac 빛.java'); assert 'exit 0' in Metin and 'Compiled:' in Metin, Metin
            Metin = gabyjak('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Metin and 'exit 0' in Metin, Metin
            Metin = gabyjak('run 빛.elf'); assert '\n55\n' in Metin and '한글 AOT Faýl 😀' in Metin and 'exit 0' in Metin, Metin
            자체실행파일 = bytearray(); faýl_geçir_birikme.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Metin = gabyjak('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Metin and 'unsupported' in Metin, Metin
            보존자료 = bytearray(); faýl_geçir_birikme.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); faýl_geçir_birikme.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            faýl_geçir_birikme.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Metin = gabyjak('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Metin and 'exit 0' in Metin, Metin
            Metin = gabyjak('run 빛.elf'); assert '\n55\n' in Metin and '한글 AOT Faýl 😀' in Metin and 'exit 0' in Metin, Metin
            barlag_hasabat['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            barlag_hasabat['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statiki_gor=결과자료/'정적시험.java'
            statiki_gor.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] baha = new int[] {기준, 합(10)};
  System.out.println(baha[0] + baha[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(statiki_gor)])
            faýl_geçir_birikme.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            Metin=gabyjak('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Metin,Metin
            Metin=gabyjak('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Metin,Metin
            faýl_geçir_birikme.delete('정적시험.class');faýl_geçir_birikme.delete('정적시험.elf')
            barlag_hasabat['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arhiw.getvalue());손상자료[14]^=1
            faýl_geçir_birikme.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Metin=gabyjak('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Metin,Metin
            barlag_hasabat['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            faýl_geçir_birikme.quit(); assert 'FTP stopped' in gabyjak('ftpd stop')
            assert not 연결다리.Hata, 연결다리.Hata
            barlag_hasabat.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in saýlaýjy.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.sägin_waka.set()
            Proses.terminate()
            try: Proses.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
            saýlaýjy.close(); Proses.stdin.close(); Proses.stdout.close()
            barlag_hasabat['bridge_error'] = 연결다리.Hata
            barlag_hasabat['frames_to_guest'] = 연결다리.커널수신틀수; barlag_hasabat['frames_from_guest'] = 연결다리.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(연결다리.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(barlag_hasabat, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Bitir()
