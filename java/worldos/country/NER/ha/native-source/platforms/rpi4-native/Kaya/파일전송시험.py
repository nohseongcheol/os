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
from gudanar_Umarni import 기준, Umarni
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Tafiyar_da():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    amincewa_Rahoto = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.Rubuta_Layi("JAR gudanar_Umarni: " + 인수[0]); 한국어.자체.Fayil.Yi_Rubutu("jar.txt", "자체 Kwara_Daraja Fayil"); 한국어.자체.출력.Rubuta_Layi(한국어.자체.Fayil.Yi_Karatu("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    Rumbun_ajiya = io.BytesIO()
    with zipfile.ZipFile(Rumbun_ajiya, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); lambar_kafa = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); Saba_watsuwa_fot = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(lambar_kafa, ['tcp:{}:9300'.format(Saba_watsuwa_fot), 'udp:{}:9301'.format(서버전문접속번호)], ɗauka=True) as 연결다리:
        haryar_aikin_na_ura = subprocess.Popen(Umarni() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        mai_zabe = selectors.DefaultSelector(); mai_zabe.register(haryar_aikin_na_ura.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            Tarin_bayani = bytearray(); Ƙarshe_Sassautawa = time.monotonic() + 시간제한
            while 확인표시 not in Tarin_bayani:
                if time.monotonic() > Ƙarshe_Sassautawa or haryar_aikin_na_ura.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + Tarin_bayani.decode('utf-8', 'replace'))
                for 누름값, _ in mai_zabe.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: Tarin_bayani.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in Tarin_bayani or b'FAIL ' in Tarin_bayani: raise AssertionError(Tarin_bayani)
            return Tarin_bayani.decode('utf-8', 'replace').replace('\r\n', '\n')
        def Mai_fayyace_umani(Layi):
            haryar_aikin_na_ura.stdin.write(Layi.encode() + b'\n'); haryar_aikin_na_ura.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in Mai_fayyace_umani('ftpd start')
            Fayil_Gusar_da_haɗi = ftplib.FTP(); Fayil_Gusar_da_haɗi.encoding = 'utf-8'; Fayil_Gusar_da_haɗi.connect('127.0.0.1', lambar_kafa, timeout=20); Fayil_Gusar_da_haɗi.login()
            Kumshinbayanai_Tarin_bayani = bytes(range(256)) * 32
            Fayil_Gusar_da_haɗi.storbinary('STOR binary.dat', io.BytesIO(Kumshinbayanai_Tarin_bayani))
            결과 = bytearray(); Fayil_Gusar_da_haɗi.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == Kumshinbayanai_Tarin_bayani; assert Fayil_Gusar_da_haɗi.size('binary.dat') == len(Kumshinbayanai_Tarin_bayani)
            amincewa_Rahoto['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            Fayil_Gusar_da_haɗi.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in Mai_fayyace_umani('cat 한글.txt')
            assert '한글.txt' in Fayil_Gusar_da_haɗi.nlst()
            assert dict(Fayil_Gusar_da_haɗi.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            amincewa_Rahoto['checks'].append('UTF-8 filename and content visible in guest shell')
            try: Fayil_Gusar_da_haɗi.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); Fayil_Gusar_da_haɗi.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == Kumshinbayanai_Tarin_bayani
            amincewa_Rahoto['checks'].append('oversized replacement rejected; previous file preserved')
            with Fayil_Gusar_da_haɗi.transfercmd('STOR pending.txt') as lodawa_Fayiloli:
                # A control command must not change the active upload's destination.
                assert Fayil_Gusar_da_haɗi.size('binary.dat') == len(Kumshinbayanai_Tarin_bayani)
                lodawa_Fayiloli.sendall(b'UPLOAD TARGET PRESERVED')
            assert Fayil_Gusar_da_haɗi.voidresp().startswith('226')
            결과 = bytearray(); Fayil_Gusar_da_haɗi.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); Fayil_Gusar_da_haɗi.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == Kumshinbayanai_Tarin_bayani
            Fayil_Gusar_da_haɗi.delete('pending.txt')
            amincewa_Rahoto['checks'].append('interleaved SIZE cannot change the active STOR destination')
            Fayil_Gusar_da_haɗi.storbinary('STOR 인사.jar', io.BytesIO(Rumbun_ajiya.getvalue()))
            SMS = Mai_fayyace_umani('java -jar 인사.jar 누리')
            assert 'JAR gudanar_Umarni: 누리' in SMS and '자체 Kwara_Daraja Fayil' in SMS and 'exit 0' in SMS, SMS
            SMS = Mai_fayyace_umani('./인사.jar 세상')
            assert 'JAR gudanar_Umarni: 세상' in SMS and 'exit 0' in SMS, SMS
            amincewa_Rahoto['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct Tarin_bayani { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct Tarin_bayani Daraja = {합(10), 1.25}; if (Daraja.수 != 55 || Daraja.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = buɗe_Fayil("cc.txt", Rubutuwa_karantuwa | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; Rubuta_Fayil_Tarin_bayani(문서, 인사, sizeof(인사)-1); Rufe_Fayil(문서); Rubuta_Fayil_Tarin_bayani(1, 인사, sizeof(인사)-1); return 0; }\n'
            Fayil_Gusar_da_haɗi.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            SMS = Mai_fayyace_umani('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = Mai_fayyace_umani('run 한글.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            assert 'CC NATIVE PASS' in Mai_fayyace_umani('cat cc.txt')
            실행파일 = bytearray(); Fayil_Gusar_da_haɗi.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            Fayil_Gusar_da_haɗi.storbinary('STOR Kwafi_Daraja.elf', io.BytesIO(실행파일)); SMS = Mai_fayyace_umani('run Kwafi_Daraja.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            Fayil_Gusar_da_haɗi.storbinary('STOR gudanar_Umarni', io.BytesIO(실행파일)); SMS=Mai_fayyace_umani('./gudanar_Umarni');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            Fayil_Gusar_da_haɗi.storbinary('STOR Suna.txt', io.BytesIO(실행파일)); SMS=Mai_fayyace_umani('./Suna.txt');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            Mai_fayyace_umani('rm gudanar_Umarni Suna.txt')
            amincewa_Rahoto['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            Mai_fayyace_umani('rm binary.dat 한글.txt 한글.c 한글.elf Kwafi_Daraja.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            Fayil_Gusar_da_haɗi.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            SMS=Mai_fayyace_umani('./리눅스인사');assert 'exit -8' in SMS,SMS
            SMS=Mai_fayyace_umani('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in SMS,SMS
            assert 'LINUX ELF FILE IO' in Mai_fayyace_umani('cat linux.txt')
            Fayil_Gusar_da_haɗi.delete('리눅스인사');Fayil_Gusar_da_haɗi.delete('linux.txt')
            Fayil_Gusar_da_haɗi.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in Mai_fayyace_umani('./거짓.elf');Fayil_Gusar_da_haɗi.delete('거짓.elf')
            amincewa_Rahoto['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Haɗi = 한국어.자체.연결통신.Haɗi("10.0.2.2", Integer.parseInt(args[0]));
 Haɗi.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] tushe = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<tushe.length;i++) if (Haɗi.getInputStream().read() != (tushe[i]&255)) throw new RuntimeException("TCP mismatch");
 Haɗi.close();
 DatagramSocket 종단 = 한국어.자체.통신.Buɗe(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.Aika(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                Fayil_Gusar_da_haɗi.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                SMS = Mai_fayyace_umani('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_fot, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in SMS and '10.0.2.2' in SMS and 'exit 0' in SMS, SMS
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            amincewa_Rahoto['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            Fayil_Gusar_da_haɗi.delete('바깥통신.class')
            Saba_tushe=결과자료/'서버시험.java'
            Saba_tushe.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket Saba_Daraja = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket baƙo_Daraja = Saba_Daraja.accept();
  baƙo_Daraja.getOutputStream().write(baƙo_Daraja.getInputStream().read()+1); baƙo_Daraja.close(); Saba_Daraja.close();
  byte[] kunshiya_Daraja = new byte[8]; DatagramPacket 전문 = new DatagramPacket(kunshiya_Daraja, kunshiya_Daraja.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(Saba_tushe)])
            Fayil_Gusar_da_haɗi.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            haryar_aikin_na_ura.stdin.write('java 서버시험\n'.encode());haryar_aikin_na_ura.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',Saba_watsuwa_fot),timeout=5) as Fiya_Daraja:
                Fiya_Daraja.sendall(b'A');assert Fiya_Daraja.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as Fiya_Daraja:
                Fiya_Daraja.settimeout(5);Fiya_Daraja.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert Fiya_Daraja.recvfrom(512)[0]==b'UDP-IN'
            SMS=수신하기();assert 'INBOUND TCP UDP PASS' in SMS and 'exit 0' in SMS,SMS
            amincewa_Rahoto['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            Fayil_Gusar_da_haɗi.delete('서버시험.class')
            Sharadi_JERI = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.Fayil.Yi_Rubutu("aot.txt", "한글 AOT Fayil 😀"); 한국어.자체.출력.Rubuta_Layi(한국어.자체.Fayil.Yi_Karatu("aot.txt")); } }'
            Fayil_Gusar_da_haɗi.storbinary('STOR 빛.java', io.BytesIO(Sharadi_JERI.encode()))
            SMS = Mai_fayyace_umani('javac 빛.java'); assert 'exit 0' in SMS and 'Compiled:' in SMS, SMS
            SMS = Mai_fayyace_umani('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = Mai_fayyace_umani('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT Fayil 😀' in SMS and 'exit 0' in SMS, SMS
            자체실행파일 = bytearray(); Fayil_Gusar_da_haɗi.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            SMS = Mai_fayyace_umani('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in SMS and 'unsupported' in SMS, SMS
            보존자료 = bytearray(); Fayil_Gusar_da_haɗi.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); Fayil_Gusar_da_haɗi.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            Fayil_Gusar_da_haɗi.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            SMS = Mai_fayyace_umani('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = Mai_fayyace_umani('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT Fayil 😀' in SMS and 'exit 0' in SMS, SMS
            amincewa_Rahoto['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            amincewa_Rahoto['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            Tsaye_cik_tushe=결과자료/'정적시험.java'
            Tsaye_cik_tushe.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] Daraja = new int[] {기준, 합(10)};
  System.out.println(Daraja[0] + Daraja[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(Tsaye_cik_tushe)])
            Fayil_Gusar_da_haɗi.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            SMS=Mai_fayyace_umani('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in SMS,SMS
            SMS=Mai_fayyace_umani('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in SMS,SMS
            Fayil_Gusar_da_haɗi.delete('정적시험.class');Fayil_Gusar_da_haɗi.delete('정적시험.elf')
            amincewa_Rahoto['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Rumbun_ajiya.getvalue());손상자료[14]^=1
            Fayil_Gusar_da_haɗi.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            SMS=Mai_fayyace_umani('java -jar 인사.jar');assert 'Main-Class\nexit 1' in SMS,SMS
            amincewa_Rahoto['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            Fayil_Gusar_da_haɗi.quit(); assert 'FTP stopped' in Mai_fayyace_umani('ftpd stop')
            assert not 연결다리.Kuskure, 연결다리.Kuskure
            amincewa_Rahoto.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in mai_zabe.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.dakata_Faruwa.set()
            haryar_aikin_na_ura.terminate()
            try: haryar_aikin_na_ura.wait(timeout=5)
            except subprocess.TimeoutExpired: haryar_aikin_na_ura.kill(); haryar_aikin_na_ura.wait()
            mai_zabe.close(); haryar_aikin_na_ura.stdin.close(); haryar_aikin_na_ura.stdout.close()
            amincewa_Rahoto['bridge_error'] = 연결다리.Kuskure
            amincewa_Rahoto['frames_to_guest'] = 연결다리.커널수신틀수; amincewa_Rahoto['frames_from_guest'] = 연결다리.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(연결다리.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(amincewa_Rahoto, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Tafiyar_da()
