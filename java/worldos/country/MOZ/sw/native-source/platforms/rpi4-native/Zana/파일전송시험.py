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
from Mtandao_daraja import Mtandao_daraja
from tekeleza_amri import 기준, amri
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def endesha():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    uhakikishi_ripoti = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.andika_laini("JAR tekeleza_amri: " + 인수[0]); 한국어.자체.faili.andika("jar.txt", "자체 kiini_thamani_0611a8a8 faili"); 한국어.자체.출력.andika_laini(한국어.자체.faili.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    Hifadhi_eb6be19d = io.BytesIO()
    with zipfile.ZipFile(Hifadhi_eb6be19d, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); namba_ya_kituo = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); seva_Stream_kituo = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Mtandao_daraja(namba_ya_kituo, ['tcp:{}:9300'.format(seva_Stream_kituo), 'udp:{}:9301'.format(서버전문접속번호)], unasaji=True) as daraja:
        Mchakato = subprocess.Popen(amri() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + daraja.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        kiteuzi = selectors.DefaultSelector(); kiteuzi.register(Mchakato.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            data = bytearray(); tamatia_Chipua = time.monotonic() + 시간제한
            while 확인표시 not in data:
                if time.monotonic() > tamatia_Chipua or Mchakato.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + data.decode('utf-8', 'replace'))
                for 누름값, _ in kiteuzi.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8', 'replace').replace('\r\n', '\n')
        def sheli(laini):
            Mchakato.stdin.write(laini.encode() + b'\n'); Mchakato.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in sheli('ftpd start')
            faili_hamisha_muunganisho = ftplib.FTP(); faili_hamisha_muunganisho.encoding = 'utf-8'; faili_hamisha_muunganisho.connect('127.0.0.1', namba_ya_kituo, timeout=20); faili_hamisha_muunganisho.login()
            data_muhimu_data = bytes(range(256)) * 32
            faili_hamisha_muunganisho.storbinary('STOR binary.dat', io.BytesIO(data_muhimu_data))
            결과 = bytearray(); faili_hamisha_muunganisho.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == data_muhimu_data; assert faili_hamisha_muunganisho.size('binary.dat') == len(data_muhimu_data)
            uhakikishi_ripoti['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            faili_hamisha_muunganisho.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in sheli('cat 한글.txt')
            assert '한글.txt' in faili_hamisha_muunganisho.nlst()
            assert dict(faili_hamisha_muunganisho.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            uhakikishi_ripoti['checks'].append('UTF-8 filename and content visible in guest shell')
            try: faili_hamisha_muunganisho.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); faili_hamisha_muunganisho.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == data_muhimu_data
            uhakikishi_ripoti['checks'].append('oversized replacement rejected; previous file preserved')
            with faili_hamisha_muunganisho.transfercmd('STOR pending.txt') as pakia_Faili:
                # A control command must not change the active upload's destination.
                assert faili_hamisha_muunganisho.size('binary.dat') == len(data_muhimu_data)
                pakia_Faili.sendall(b'UPLOAD TARGET PRESERVED')
            assert faili_hamisha_muunganisho.voidresp().startswith('226')
            결과 = bytearray(); faili_hamisha_muunganisho.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); faili_hamisha_muunganisho.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == data_muhimu_data
            faili_hamisha_muunganisho.delete('pending.txt')
            uhakikishi_ripoti['checks'].append('interleaved SIZE cannot change the active STOR destination')
            faili_hamisha_muunganisho.storbinary('STOR 인사.jar', io.BytesIO(Hifadhi_eb6be19d.getvalue()))
            SMS = sheli('java -jar 인사.jar 누리')
            assert 'JAR tekeleza_amri: 누리' in SMS and '자체 kiini_thamani_0611a8a8 faili' in SMS and 'exit 0' in SMS, SMS
            SMS = sheli('./인사.jar 세상')
            assert 'JAR tekeleza_amri: 세상' in SMS and 'exit 0' in SMS, SMS
            uhakikishi_ripoti['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct data { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct data thamani = {합(10), 1.25}; if (thamani.수 != 55 || thamani.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = unda_faili("cc.txt", soma_andika | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; andika_faili_data(문서, 인사, sizeof(인사)-1); funga_faili(문서); andika_faili_data(1, 인사, sizeof(인사)-1); return 0; }\n'
            faili_hamisha_muunganisho.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            SMS = sheli('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = sheli('run 한글.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            assert 'CC NATIVE PASS' in sheli('cat cc.txt')
            실행파일 = bytearray(); faili_hamisha_muunganisho.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            faili_hamisha_muunganisho.storbinary('STOR mfano_thamani.elf', io.BytesIO(실행파일)); SMS = sheli('run mfano_thamani.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            faili_hamisha_muunganisho.storbinary('STOR tekeleza_amri', io.BytesIO(실행파일)); SMS=sheli('./tekeleza_amri');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            faili_hamisha_muunganisho.storbinary('STOR Jina.txt', io.BytesIO(실행파일)); SMS=sheli('./Jina.txt');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            sheli('rm tekeleza_amri Jina.txt')
            uhakikishi_ripoti['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            sheli('rm binary.dat 한글.txt 한글.c 한글.elf mfano_thamani.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            faili_hamisha_muunganisho.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            SMS=sheli('./리눅스인사');assert 'exit -8' in SMS,SMS
            SMS=sheli('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in SMS,SMS
            assert 'LINUX ELF FILE IO' in sheli('cat linux.txt')
            faili_hamisha_muunganisho.delete('리눅스인사');faili_hamisha_muunganisho.delete('linux.txt')
            faili_hamisha_muunganisho.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in sheli('./거짓.elf');faili_hamisha_muunganisho.delete('거짓.elf')
            uhakikishi_ripoti['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket UNGANISHA = 한국어.자체.연결통신.UNGANISHA("10.0.2.2", Integer.parseInt(args[0]));
 UNGANISHA.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] chanzo = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<chanzo.length;i++) if (UNGANISHA.getInputStream().read() != (chanzo[i]&255)) throw new RuntimeException("TCP mismatch");
 UNGANISHA.close();
 DatagramSocket 종단 = 한국어.자체.통신.unda(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.tuma(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                faili_hamisha_muunganisho.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                SMS = sheli('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_kituo, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in SMS and '10.0.2.2' in SMS and 'exit 0' in SMS, SMS
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            uhakikishi_ripoti['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            faili_hamisha_muunganisho.delete('바깥통신.class')
            seva_chanzo=결과자료/'서버시험.java'
            seva_chanzo.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket seva_thamani = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket mgeni_thamani = seva_thamani.accept();
  mgeni_thamani.getOutputStream().write(mgeni_thamani.getInputStream().read()+1); mgeni_thamani.close(); seva_thamani.close();
  byte[] maudhui_thamani = new byte[8]; DatagramPacket 전문 = new DatagramPacket(maudhui_thamani, maudhui_thamani.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(seva_chanzo)])
            faili_hamisha_muunganisho.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            Mchakato.stdin.write('java 서버시험\n'.encode());Mchakato.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',seva_Stream_kituo),timeout=5) as kompyuta_rika_thamani:
                kompyuta_rika_thamani.sendall(b'A');assert kompyuta_rika_thamani.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as kompyuta_rika_thamani:
                kompyuta_rika_thamani.settimeout(5);kompyuta_rika_thamani.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert kompyuta_rika_thamani.recvfrom(512)[0]==b'UDP-IN'
            SMS=수신하기();assert 'INBOUND TCP UDP PASS' in SMS and 'exit 0' in SMS,SMS
            uhakikishi_ripoti['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            faili_hamisha_muunganisho.delete('서버시험.class')
            agizo_MFUATANO = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.faili.andika("aot.txt", "한글 AOT faili 😀"); 한국어.자체.출력.andika_laini(한국어.자체.faili.읽기("aot.txt")); } }'
            faili_hamisha_muunganisho.storbinary('STOR 빛.java', io.BytesIO(agizo_MFUATANO.encode()))
            SMS = sheli('javac 빛.java'); assert 'exit 0' in SMS and 'Compiled:' in SMS, SMS
            SMS = sheli('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = sheli('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT faili 😀' in SMS and 'exit 0' in SMS, SMS
            자체실행파일 = bytearray(); faili_hamisha_muunganisho.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            SMS = sheli('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in SMS and 'unsupported' in SMS, SMS
            보존자료 = bytearray(); faili_hamisha_muunganisho.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); faili_hamisha_muunganisho.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            faili_hamisha_muunganisho.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            SMS = sheli('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = sheli('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT faili 😀' in SMS and 'exit 0' in SMS, SMS
            uhakikishi_ripoti['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            uhakikishi_ripoti['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            tuli_chanzo=결과자료/'정적시험.java'
            tuli_chanzo.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] thamani = new int[] {기준, 합(10)};
  System.out.println(thamani[0] + thamani[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(tuli_chanzo)])
            faili_hamisha_muunganisho.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            SMS=sheli('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in SMS,SMS
            SMS=sheli('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in SMS,SMS
            faili_hamisha_muunganisho.delete('정적시험.class');faili_hamisha_muunganisho.delete('정적시험.elf')
            uhakikishi_ripoti['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Hifadhi_eb6be19d.getvalue());손상자료[14]^=1
            faili_hamisha_muunganisho.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            SMS=sheli('java -jar 인사.jar');assert 'Main-Class\nexit 1' in SMS,SMS
            uhakikishi_ripoti['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            faili_hamisha_muunganisho.quit(); assert 'FTP stopped' in sheli('ftpd stop')
            assert not daraja.kosa, daraja.kosa
            uhakikishi_ripoti.update(passed=True, frames_to_guest=daraja.커널수신틀수, frames_from_guest=daraja.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in kiteuzi.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            daraja.sitisha_tukio.set()
            Mchakato.terminate()
            try: Mchakato.wait(timeout=5)
            except subprocess.TimeoutExpired: Mchakato.kill(); Mchakato.wait()
            kiteuzi.close(); Mchakato.stdin.close(); Mchakato.stdout.close()
            uhakikishi_ripoti['bridge_error'] = daraja.kosa
            uhakikishi_ripoti['frames_to_guest'] = daraja.커널수신틀수; uhakikishi_ripoti['frames_from_guest'] = daraja.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(daraja.idadi_ya_maingizo_mlalo_batli,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(uhakikishi_ripoti, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': endesha()
