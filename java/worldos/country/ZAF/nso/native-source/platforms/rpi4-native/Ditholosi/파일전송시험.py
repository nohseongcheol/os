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
from Netweke_kgokaganyo import Netweke_kgokaganyo
from phethagatša_taelo import 기준, Taelo
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Diriša():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    tiišetšo_pego = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.ngwala_mothaladi("JAR phethagatša_taelo: " + 인수[0]); 한국어.자체.Faele.Ngwala("jar.txt", "자체 khenele_boleng Faele"); 한국어.자체.출력.ngwala_mothaladi(한국어.자체.Faele.Bala("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    Akhaebe = io.BytesIO()
    with zipfile.ZipFile(Akhaebe, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); seba_Stream_phote = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Netweke_kgokaganyo(접속번호, ['tcp:{}:9300'.format(seba_Stream_phote), 'udp:{}:9301'.format(서버전문접속번호)], tšea=True) as kgokaganyo:
        tiragalo_a7054519 = subprocess.Popen(Taelo() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + kgokaganyo.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        sekgethi = selectors.DefaultSelector(); sekgethi.register(tiragalo_a7054519.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            data = bytearray(); fetša_E_Šetšego = time.monotonic() + 시간제한
            while 확인표시 not in data:
                if time.monotonic() > fetša_E_Šetšego or tiragalo_a7054519.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + data.decode('utf-8', 'replace'))
                for 누름값, _ in sekgethi.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8', 'replace').replace('\r\n', '\n')
        def šele(mothaladi):
            tiragalo_a7054519.stdin.write(mothaladi.encode() + b'\n'); tiragalo_a7054519.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in šele('ftpd start')
            faele_fetišetša_kgokaganya = ftplib.FTP(); faele_fetišetša_kgokaganya.encoding = 'utf-8'; faele_fetišetša_kgokaganya.connect('127.0.0.1', 접속번호, timeout=20); faele_fetišetša_kgokaganya.login()
            morwalotefelwa_data = bytes(range(256)) * 32
            faele_fetišetša_kgokaganya.storbinary('STOR binary.dat', io.BytesIO(morwalotefelwa_data))
            결과 = bytearray(); faele_fetišetša_kgokaganya.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == morwalotefelwa_data; assert faele_fetišetša_kgokaganya.size('binary.dat') == len(morwalotefelwa_data)
            tiišetšo_pego['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            faele_fetišetša_kgokaganya.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in šele('cat 한글.txt')
            assert '한글.txt' in faele_fetišetša_kgokaganya.nlst()
            assert dict(faele_fetišetša_kgokaganya.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            tiišetšo_pego['checks'].append('UTF-8 filename and content visible in guest shell')
            try: faele_fetišetša_kgokaganya.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); faele_fetišetša_kgokaganya.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == morwalotefelwa_data
            tiišetšo_pego['checks'].append('oversized replacement rejected; previous file preserved')
            with faele_fetišetša_kgokaganya.transfercmd('STOR pending.txt') as apolouto_Difaele:
                # A control command must not change the active upload's destination.
                assert faele_fetišetša_kgokaganya.size('binary.dat') == len(morwalotefelwa_data)
                apolouto_Difaele.sendall(b'UPLOAD TARGET PRESERVED')
            assert faele_fetišetša_kgokaganya.voidresp().startswith('226')
            결과 = bytearray(); faele_fetišetša_kgokaganya.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); faele_fetišetša_kgokaganya.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == morwalotefelwa_data
            faele_fetišetša_kgokaganya.delete('pending.txt')
            tiišetšo_pego['checks'].append('interleaved SIZE cannot change the active STOR destination')
            faele_fetišetša_kgokaganya.storbinary('STOR 인사.jar', io.BytesIO(Akhaebe.getvalue()))
            Sengwalwa = šele('java -jar 인사.jar 누리')
            assert 'JAR phethagatša_taelo: 누리' in Sengwalwa and '자체 khenele_boleng Faele' in Sengwalwa and 'exit 0' in Sengwalwa, Sengwalwa
            Sengwalwa = šele('./인사.jar 세상')
            assert 'JAR phethagatša_taelo: 세상' in Sengwalwa and 'exit 0' in Sengwalwa, Sengwalwa
            tiišetšo_pego['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct data { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct data boleng = {합(10), 1.25}; if (boleng.수 != 55 || boleng.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = bula_faele("cc.txt", bala_ngwala | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; ngwala_faele_data(문서, 인사, sizeof(인사)-1); tswalela_faele(문서); ngwala_faele_data(1, 인사, sizeof(인사)-1); return 0; }\n'
            faele_fetišetša_kgokaganya.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Sengwalwa = šele('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Sengwalwa and 'exit 0' in Sengwalwa, Sengwalwa
            Sengwalwa = šele('run 한글.elf'); assert 'CC NATIVE PASS' in Sengwalwa and 'exit 0' in Sengwalwa, Sengwalwa
            assert 'CC NATIVE PASS' in šele('cat cc.txt')
            실행파일 = bytearray(); faele_fetišetša_kgokaganya.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            faele_fetišetša_kgokaganya.storbinary('STOR kopiša_boleng.elf', io.BytesIO(실행파일)); Sengwalwa = šele('run kopiša_boleng.elf'); assert 'CC NATIVE PASS' in Sengwalwa and 'exit 0' in Sengwalwa, Sengwalwa
            faele_fetišetša_kgokaganya.storbinary('STOR phethagatša_taelo', io.BytesIO(실행파일)); Sengwalwa=šele('./phethagatša_taelo');assert 'CC NATIVE PASS' in Sengwalwa and 'exit 0' in Sengwalwa,Sengwalwa
            faele_fetišetša_kgokaganya.storbinary('STOR Leina.txt', io.BytesIO(실행파일)); Sengwalwa=šele('./Leina.txt');assert 'CC NATIVE PASS' in Sengwalwa and 'exit 0' in Sengwalwa,Sengwalwa
            šele('rm phethagatša_taelo Leina.txt')
            tiišetšo_pego['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            šele('rm binary.dat 한글.txt 한글.c 한글.elf kopiša_boleng.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            faele_fetišetša_kgokaganya.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Sengwalwa=šele('./리눅스인사');assert 'exit -8' in Sengwalwa,Sengwalwa
            Sengwalwa=šele('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Sengwalwa,Sengwalwa
            assert 'LINUX ELF FILE IO' in šele('cat linux.txt')
            faele_fetišetša_kgokaganya.delete('리눅스인사');faele_fetišetša_kgokaganya.delete('linux.txt')
            faele_fetišetša_kgokaganya.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in šele('./거짓.elf');faele_fetišetša_kgokaganya.delete('거짓.elf')
            tiišetšo_pego['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Ikgokaganye = 한국어.자체.연결통신.Ikgokaganye("10.0.2.2", Integer.parseInt(args[0]));
 Ikgokaganye.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] mohlodi = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<mohlodi.length;i++) if (Ikgokaganye.getInputStream().read() != (mohlodi[i]&255)) throw new RuntimeException("TCP mismatch");
 Ikgokaganye.close();
 DatagramSocket 종단 = 한국어.자체.통신.Bula(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.Romela(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                faele_fetišetša_kgokaganya.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                Sengwalwa = šele('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_phote, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in Sengwalwa and '10.0.2.2' in Sengwalwa and 'exit 0' in Sengwalwa, Sengwalwa
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            tiišetšo_pego['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            faele_fetišetša_kgokaganya.delete('바깥통신.class')
            seba_mohlodi=결과자료/'서버시험.java'
            seba_mohlodi.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket seba_boleng = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket moeng_boleng = seba_boleng.accept();
  moeng_boleng.getOutputStream().write(moeng_boleng.getInputStream().read()+1); moeng_boleng.close(); seba_boleng.close();
  byte[] Diteng_boleng = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Diteng_boleng, Diteng_boleng.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(seba_mohlodi)])
            faele_fetišetša_kgokaganya.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            tiragalo_a7054519.stdin.write('java 서버시험\n'.encode());tiragalo_a7054519.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',seba_Stream_phote),timeout=5) as sedirišwa_sa_legoro_le_tee_boleng:
                sedirišwa_sa_legoro_le_tee_boleng.sendall(b'A');assert sedirišwa_sa_legoro_le_tee_boleng.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sedirišwa_sa_legoro_le_tee_boleng:
                sedirišwa_sa_legoro_le_tee_boleng.settimeout(5);sedirišwa_sa_legoro_le_tee_boleng.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert sedirišwa_sa_legoro_le_tee_boleng.recvfrom(512)[0]==b'UDP-IN'
            Sengwalwa=수신하기();assert 'INBOUND TCP UDP PASS' in Sengwalwa and 'exit 0' in Sengwalwa,Sengwalwa
            tiišetšo_pego['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            faele_fetišetša_kgokaganya.delete('서버시험.class')
            taelo_TATELANO = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.Faele.Ngwala("aot.txt", "한글 AOT Faele 😀"); 한국어.자체.출력.ngwala_mothaladi(한국어.자체.Faele.Bala("aot.txt")); } }'
            faele_fetišetša_kgokaganya.storbinary('STOR 빛.java', io.BytesIO(taelo_TATELANO.encode()))
            Sengwalwa = šele('javac 빛.java'); assert 'exit 0' in Sengwalwa and 'Compiled:' in Sengwalwa, Sengwalwa
            Sengwalwa = šele('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Sengwalwa and 'exit 0' in Sengwalwa, Sengwalwa
            Sengwalwa = šele('run 빛.elf'); assert '\n55\n' in Sengwalwa and '한글 AOT Faele 😀' in Sengwalwa and 'exit 0' in Sengwalwa, Sengwalwa
            자체실행파일 = bytearray(); faele_fetišetša_kgokaganya.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Sengwalwa = šele('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Sengwalwa and 'unsupported' in Sengwalwa, Sengwalwa
            보존자료 = bytearray(); faele_fetišetša_kgokaganya.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); faele_fetišetša_kgokaganya.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            faele_fetišetša_kgokaganya.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Sengwalwa = šele('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Sengwalwa and 'exit 0' in Sengwalwa, Sengwalwa
            Sengwalwa = šele('run 빛.elf'); assert '\n55\n' in Sengwalwa and '한글 AOT Faele 😀' in Sengwalwa and 'exit 0' in Sengwalwa, Sengwalwa
            tiišetšo_pego['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            tiišetšo_pego['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ya_go_se_fetoge_mohlodi=결과자료/'정적시험.java'
            ya_go_se_fetoge_mohlodi.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] boleng = new int[] {기준, 합(10)};
  System.out.println(boleng[0] + boleng[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(ya_go_se_fetoge_mohlodi)])
            faele_fetišetša_kgokaganya.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            Sengwalwa=šele('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Sengwalwa,Sengwalwa
            Sengwalwa=šele('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Sengwalwa,Sengwalwa
            faele_fetišetša_kgokaganya.delete('정적시험.class');faele_fetišetša_kgokaganya.delete('정적시험.elf')
            tiišetšo_pego['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Akhaebe.getvalue());손상자료[14]^=1
            faele_fetišetša_kgokaganya.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Sengwalwa=šele('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Sengwalwa,Sengwalwa
            tiišetšo_pego['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            faele_fetišetša_kgokaganya.quit(); assert 'FTP stopped' in šele('ftpd stop')
            assert not kgokaganyo.Phošo, kgokaganyo.Phošo
            tiišetšo_pego.update(passed=True, frames_to_guest=kgokaganyo.커널수신틀수, frames_from_guest=kgokaganyo.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in sekgethi.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            kgokaganyo.emiša_nakwana_tiragalo.set()
            tiragalo_a7054519.terminate()
            try: tiragalo_a7054519.wait(timeout=5)
            except subprocess.TimeoutExpired: tiragalo_a7054519.kill(); tiragalo_a7054519.wait()
            sekgethi.close(); tiragalo_a7054519.stdin.close(); tiragalo_a7054519.stdout.close()
            tiišetšo_pego['bridge_error'] = kgokaganyo.Phošo
            tiišetšo_pego['frames_to_guest'] = kgokaganyo.커널수신틀수; tiišetšo_pego['frames_from_guest'] = kgokaganyo.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(kgokaganyo.latišiša_pego,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(tiišetšo_pego, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Diriša()
