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
from Neteweke_leborogo import Neteweke_leborogo
from diragatsa_Taelo import 기준, Taelo
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def dirisa():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    netefatso_pego = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.kwala_Mola("JAR diragatsa_Taelo: " + 인수[0]); 한국어.자체.faele.kwala("jar.txt", "자체 Khenele_Boleng faele"); 한국어.자체.출력.kwala_Mola(한국어.자체.faele.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    boloka = io.BytesIO()
    with zipfile.ZipFile(boloka, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); sefara_moela_gorogisetsa = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Neteweke_leborogo(접속번호, ['tcp:{}:9300'.format(sefara_moela_gorogisetsa), 'udp:{}:9301'.format(서버전문접속번호)], tshwara=True) as leborogo:
        Thulaganyo = subprocess.Popen(Taelo() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + leborogo.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        setlhophi = selectors.DefaultSelector(); setlhophi.register(Thulaganyo.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            tshedimosetso = bytearray(); kgaola_Baya_ka_Tekatekanyo = time.monotonic() + 시간제한
            while 확인표시 not in tshedimosetso:
                if time.monotonic() > kgaola_Baya_ka_Tekatekanyo or Thulaganyo.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + tshedimosetso.decode('utf-8', 'replace'))
                for 누름값, _ in setlhophi.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: tshedimosetso.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in tshedimosetso or b'FAIL ' in tshedimosetso: raise AssertionError(tshedimosetso)
            return tshedimosetso.decode('utf-8', 'replace').replace('\r\n', '\n')
        def setlhalosataelo(Mola):
            Thulaganyo.stdin.write(Mola.encode() + b'\n'); Thulaganyo.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in setlhalosataelo('ftpd start')
            faele_fudusa_Kgolagano = ftplib.FTP(); faele_fudusa_Kgolagano.encoding = 'utf-8'; faele_fudusa_Kgolagano.connect('127.0.0.1', 접속번호, timeout=20); faele_fudusa_Kgolagano.login()
            selekanyo_sa_tshedimosetso_tshedimosetso = bytes(range(256)) * 32
            faele_fudusa_Kgolagano.storbinary('STOR binary.dat', io.BytesIO(selekanyo_sa_tshedimosetso_tshedimosetso))
            결과 = bytearray(); faele_fudusa_Kgolagano.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == selekanyo_sa_tshedimosetso_tshedimosetso; assert faele_fudusa_Kgolagano.size('binary.dat') == len(selekanyo_sa_tshedimosetso_tshedimosetso)
            netefatso_pego['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            faele_fudusa_Kgolagano.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in setlhalosataelo('cat 한글.txt')
            assert '한글.txt' in faele_fudusa_Kgolagano.nlst()
            assert dict(faele_fudusa_Kgolagano.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            netefatso_pego['checks'].append('UTF-8 filename and content visible in guest shell')
            try: faele_fudusa_Kgolagano.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); faele_fudusa_Kgolagano.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == selekanyo_sa_tshedimosetso_tshedimosetso
            netefatso_pego['checks'].append('oversized replacement rejected; previous file preserved')
            with faele_fudusa_Kgolagano.transfercmd('STOR pending.txt') as laisa_Difaele:
                # A control command must not change the active upload's destination.
                assert faele_fudusa_Kgolagano.size('binary.dat') == len(selekanyo_sa_tshedimosetso_tshedimosetso)
                laisa_Difaele.sendall(b'UPLOAD TARGET PRESERVED')
            assert faele_fudusa_Kgolagano.voidresp().startswith('226')
            결과 = bytearray(); faele_fudusa_Kgolagano.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); faele_fudusa_Kgolagano.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == selekanyo_sa_tshedimosetso_tshedimosetso
            faele_fudusa_Kgolagano.delete('pending.txt')
            netefatso_pego['checks'].append('interleaved SIZE cannot change the active STOR destination')
            faele_fudusa_Kgolagano.storbinary('STOR 인사.jar', io.BytesIO(boloka.getvalue()))
            SMS = setlhalosataelo('java -jar 인사.jar 누리')
            assert 'JAR diragatsa_Taelo: 누리' in SMS and '자체 Khenele_Boleng faele' in SMS and 'exit 0' in SMS, SMS
            SMS = setlhalosataelo('./인사.jar 세상')
            assert 'JAR diragatsa_Taelo: 세상' in SMS and 'exit 0' in SMS, SMS
            netefatso_pego['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct tshedimosetso { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct tshedimosetso Boleng = {합(10), 1.25}; if (Boleng.수 != 55 || Boleng.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = bula_faele("cc.txt", buisa_kwala | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; kwala_faele_tshedimosetso(문서, 인사, sizeof(인사)-1); tswala_faele(문서); kwala_faele_tshedimosetso(1, 인사, sizeof(인사)-1); return 0; }\n'
            faele_fudusa_Kgolagano.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            SMS = setlhalosataelo('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = setlhalosataelo('run 한글.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            assert 'CC NATIVE PASS' in setlhalosataelo('cat cc.txt')
            실행파일 = bytearray(); faele_fudusa_Kgolagano.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            faele_fudusa_Kgolagano.storbinary('STOR leloko_Boleng.elf', io.BytesIO(실행파일)); SMS = setlhalosataelo('run leloko_Boleng.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            faele_fudusa_Kgolagano.storbinary('STOR diragatsa_Taelo', io.BytesIO(실행파일)); SMS=setlhalosataelo('./diragatsa_Taelo');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            faele_fudusa_Kgolagano.storbinary('STOR leina.txt', io.BytesIO(실행파일)); SMS=setlhalosataelo('./leina.txt');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            setlhalosataelo('rm diragatsa_Taelo leina.txt')
            netefatso_pego['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            setlhalosataelo('rm binary.dat 한글.txt 한글.c 한글.elf leloko_Boleng.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            faele_fudusa_Kgolagano.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            SMS=setlhalosataelo('./리눅스인사');assert 'exit -8' in SMS,SMS
            SMS=setlhalosataelo('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in SMS,SMS
            assert 'LINUX ELF FILE IO' in setlhalosataelo('cat linux.txt')
            faele_fudusa_Kgolagano.delete('리눅스인사');faele_fudusa_Kgolagano.delete('linux.txt')
            faele_fudusa_Kgolagano.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in setlhalosataelo('./거짓.elf');faele_fudusa_Kgolagano.delete('거짓.elf')
            netefatso_pego['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Golaganya = 한국어.자체.연결통신.Golaganya("10.0.2.2", Integer.parseInt(args[0]));
 Golaganya.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] Motswedi = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<Motswedi.length;i++) if (Golaganya.getInputStream().read() != (Motswedi[i]&255)) throw new RuntimeException("TCP mismatch");
 Golaganya.close();
 DatagramSocket 종단 = 한국어.자체.통신.bula(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.romela(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                faele_fudusa_Kgolagano.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                SMS = setlhalosataelo('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_gorogisetsa, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in SMS and '10.0.2.2' in SMS and 'exit 0' in SMS, SMS
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            netefatso_pego['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            faele_fudusa_Kgolagano.delete('바깥통신.class')
            sefara_Motswedi=결과자료/'서버시험.java'
            sefara_Motswedi.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket sefara_Boleng = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket moeng_Boleng = sefara_Boleng.accept();
  moeng_Boleng.getOutputStream().write(moeng_Boleng.getInputStream().read()+1); moeng_Boleng.close(); sefara_Boleng.close();
  byte[] Diteng_Boleng = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Diteng_Boleng, Diteng_Boleng.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(sefara_Motswedi)])
            faele_fudusa_Kgolagano.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            Thulaganyo.stdin.write('java 서버시험\n'.encode());Thulaganyo.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',sefara_moela_gorogisetsa),timeout=5) as semphato_Boleng:
                semphato_Boleng.sendall(b'A');assert semphato_Boleng.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as semphato_Boleng:
                semphato_Boleng.settimeout(5);semphato_Boleng.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert semphato_Boleng.recvfrom(512)[0]==b'UDP-IN'
            SMS=수신하기();assert 'INBOUND TCP UDP PASS' in SMS and 'exit 0' in SMS,SMS
            netefatso_pego['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            faele_fudusa_Kgolagano.delete('서버시험.class')
            taelo_TATELANO = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.faele.kwala("aot.txt", "한글 AOT faele 😀"); 한국어.자체.출력.kwala_Mola(한국어.자체.faele.읽기("aot.txt")); } }'
            faele_fudusa_Kgolagano.storbinary('STOR 빛.java', io.BytesIO(taelo_TATELANO.encode()))
            SMS = setlhalosataelo('javac 빛.java'); assert 'exit 0' in SMS and 'Compiled:' in SMS, SMS
            SMS = setlhalosataelo('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = setlhalosataelo('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT faele 😀' in SMS and 'exit 0' in SMS, SMS
            자체실행파일 = bytearray(); faele_fudusa_Kgolagano.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            SMS = setlhalosataelo('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in SMS and 'unsupported' in SMS, SMS
            보존자료 = bytearray(); faele_fudusa_Kgolagano.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); faele_fudusa_Kgolagano.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            faele_fudusa_Kgolagano.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            SMS = setlhalosataelo('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = setlhalosataelo('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT faele 😀' in SMS and 'exit 0' in SMS, SMS
            netefatso_pego['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            netefatso_pego['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            e_e_emeng_Motswedi=결과자료/'정적시험.java'
            e_e_emeng_Motswedi.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] Boleng = new int[] {기준, 합(10)};
  System.out.println(Boleng[0] + Boleng[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(e_e_emeng_Motswedi)])
            faele_fudusa_Kgolagano.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            SMS=setlhalosataelo('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in SMS,SMS
            SMS=setlhalosataelo('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in SMS,SMS
            faele_fudusa_Kgolagano.delete('정적시험.class');faele_fudusa_Kgolagano.delete('정적시험.elf')
            netefatso_pego['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(boloka.getvalue());손상자료[14]^=1
            faele_fudusa_Kgolagano.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            SMS=setlhalosataelo('java -jar 인사.jar');assert 'Main-Class\nexit 1' in SMS,SMS
            netefatso_pego['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            faele_fudusa_Kgolagano.quit(); assert 'FTP stopped' in setlhalosataelo('ftpd stop')
            assert not leborogo.phoso, leborogo.phoso
            netefatso_pego.update(passed=True, frames_to_guest=leborogo.커널수신틀수, frames_from_guest=leborogo.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in setlhophi.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            leborogo.Kgaotsa_tiragalo.set()
            Thulaganyo.terminate()
            try: Thulaganyo.wait(timeout=5)
            except subprocess.TimeoutExpired: Thulaganyo.kill(); Thulaganyo.wait()
            setlhophi.close(); Thulaganyo.stdin.close(); Thulaganyo.stdout.close()
            netefatso_pego['bridge_error'] = leborogo.phoso
            netefatso_pego['frames_to_guest'] = leborogo.커널수신틀수; netefatso_pego['frames_from_guest'] = leborogo.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(leborogo.palo_tlhakanyo_rekota,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(netefatso_pego, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': dirisa()
