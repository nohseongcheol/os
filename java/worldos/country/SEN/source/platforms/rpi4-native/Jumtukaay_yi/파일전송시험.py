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
from mbaal_poŋ import mbaal_poŋ
from def_ndigel import 기준, ndigel
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def daw():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    wéral_tënk = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.biir_buum("JAR def_ndigel: " + 인수[0]); 한국어.자체.bara_denc.biir("jar.txt", "자체 xoox_xëyma bara_denc"); 한국어.자체.출력.biir_buum(한국어.자체.bara_denc.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    denc = io.BytesIO()
    with zipfile.ZipFile(denc, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); dëggu_dawal_jël = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with mbaal_poŋ(접속번호, ['tcp:{}:9300'.format(dëggu_dawal_jël), 'udp:{}:9301'.format(서버전문접속번호)], jël=True) as poŋ:
        yokkute = subprocess.Popen(ndigel() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + poŋ.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        tànnkat = selectors.DefaultSelector(); tànnkat.register(yokkute.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            mbir = bytearray(); jeexal_Randal = time.monotonic() + 시간제한
            while 확인표시 not in mbir:
                if time.monotonic() > jeexal_Randal or yokkute.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + mbir.decode('utf-8', 'replace'))
                for 누름값, _ in tànnkat.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: mbir.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in mbir or b'FAIL ' in mbir: raise AssertionError(mbir)
            return mbir.decode('utf-8', 'replace').replace('\r\n', '\n')
        def Wëreef(buum):
            yokkute.stdin.write(buum.encode() + b'\n'); yokkute.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in Wëreef('ftpd start')
            bara_denc_toxal_jokkalóo = ftplib.FTP(); bara_denc_toxal_jokkalóo.encoding = 'utf-8'; bara_denc_toxal_jokkalóo.connect('127.0.0.1', 접속번호, timeout=20); bara_denc_toxal_jokkalóo.login()
            njoxe_yu_solowu_mbir = bytes(range(256)) * 32
            bara_denc_toxal_jokkalóo.storbinary('STOR binary.dat', io.BytesIO(njoxe_yu_solowu_mbir))
            결과 = bytearray(); bara_denc_toxal_jokkalóo.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == njoxe_yu_solowu_mbir; assert bara_denc_toxal_jokkalóo.size('binary.dat') == len(njoxe_yu_solowu_mbir)
            wéral_tënk['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            bara_denc_toxal_jokkalóo.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in Wëreef('cat 한글.txt')
            assert '한글.txt' in bara_denc_toxal_jokkalóo.nlst()
            assert dict(bara_denc_toxal_jokkalóo.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            wéral_tënk['checks'].append('UTF-8 filename and content visible in guest shell')
            try: bara_denc_toxal_jokkalóo.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); bara_denc_toxal_jokkalóo.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == njoxe_yu_solowu_mbir
            wéral_tënk['checks'].append('oversized replacement rejected; previous file preserved')
            with bara_denc_toxal_jokkalóo.transfercmd('STOR pending.txt') as toxalsi_Fisiye_yi:
                # A control command must not change the active upload's destination.
                assert bara_denc_toxal_jokkalóo.size('binary.dat') == len(njoxe_yu_solowu_mbir)
                toxalsi_Fisiye_yi.sendall(b'UPLOAD TARGET PRESERVED')
            assert bara_denc_toxal_jokkalóo.voidresp().startswith('226')
            결과 = bytearray(); bara_denc_toxal_jokkalóo.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); bara_denc_toxal_jokkalóo.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == njoxe_yu_solowu_mbir
            bara_denc_toxal_jokkalóo.delete('pending.txt')
            wéral_tënk['checks'].append('interleaved SIZE cannot change the active STOR destination')
            bara_denc_toxal_jokkalóo.storbinary('STOR 인사.jar', io.BytesIO(denc.getvalue()))
            Tekst = Wëreef('java -jar 인사.jar 누리')
            assert 'JAR def_ndigel: 누리' in Tekst and '자체 xoox_xëyma bara_denc' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = Wëreef('./인사.jar 세상')
            assert 'JAR def_ndigel: 세상' in Tekst and 'exit 0' in Tekst, Tekst
            wéral_tënk['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct mbir { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct mbir xëyma = {합(10), 1.25}; if (xëyma.수 != 55 || xëyma.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = sos_bara_denc("cc.txt", jàng_bind | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; biir_bara_denc_mbir(문서, 인사, sizeof(인사)-1); Tej_bara_denc(문서); biir_bara_denc_mbir(1, 인사, sizeof(인사)-1); return 0; }\n'
            bara_denc_toxal_jokkalóo.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Tekst = Wëreef('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = Wëreef('run 한글.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            assert 'CC NATIVE PASS' in Wëreef('cat cc.txt')
            실행파일 = bytearray(); bara_denc_toxal_jokkalóo.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            bara_denc_toxal_jokkalóo.storbinary('STOR mbokk_xëyma.elf', io.BytesIO(실행파일)); Tekst = Wëreef('run mbokk_xëyma.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            bara_denc_toxal_jokkalóo.storbinary('STOR def_ndigel', io.BytesIO(실행파일)); Tekst=Wëreef('./def_ndigel');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            bara_denc_toxal_jokkalóo.storbinary('STOR tur_253d1510.txt', io.BytesIO(실행파일)); Tekst=Wëreef('./tur_253d1510.txt');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            Wëreef('rm def_ndigel tur_253d1510.txt')
            wéral_tënk['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            Wëreef('rm binary.dat 한글.txt 한글.c 한글.elf mbokk_xëyma.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            bara_denc_toxal_jokkalóo.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Tekst=Wëreef('./리눅스인사');assert 'exit -8' in Tekst,Tekst
            Tekst=Wëreef('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Tekst,Tekst
            assert 'LINUX ELF FILE IO' in Wëreef('cat linux.txt')
            bara_denc_toxal_jokkalóo.delete('리눅스인사');bara_denc_toxal_jokkalóo.delete('linux.txt')
            bara_denc_toxal_jokkalóo.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in Wëreef('./거짓.elf');bara_denc_toxal_jokkalóo.delete('거짓.elf')
            wéral_tënk['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket JOKKOO = 한국어.자체.연결통신.JOKKOO("10.0.2.2", Integer.parseInt(args[0]));
 JOKKOO.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] Cosaan = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<Cosaan.length;i++) if (JOKKOO.getInputStream().read() != (Cosaan[i]&255)) throw new RuntimeException("TCP mismatch");
 JOKKOO.close();
 DatagramSocket 종단 = 한국어.자체.통신.sos(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.Yónnee(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                bara_denc_toxal_jokkalóo.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                Tekst = Wëreef('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_jël, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in Tekst and '10.0.2.2' in Tekst and 'exit 0' in Tekst, Tekst
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            wéral_tënk['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            bara_denc_toxal_jokkalóo.delete('바깥통신.class')
            dëggu_Cosaan=결과자료/'서버시험.java'
            dëggu_Cosaan.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket dëggu_xëyma = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gan_xëyma = dëggu_xëyma.accept();
  gan_xëyma.getOutputStream().write(gan_xëyma.getInputStream().read()+1); gan_xëyma.close(); dëggu_xëyma.close();
  byte[] Këmb_xëyma = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Këmb_xëyma, Këmb_xëyma.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(dëggu_Cosaan)])
            bara_denc_toxal_jokkalóo.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            yokkute.stdin.write('java 서버시험\n'.encode());yokkute.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',dëggu_dawal_jël),timeout=5) as Nàttangoo_xëyma:
                Nàttangoo_xëyma.sendall(b'A');assert Nàttangoo_xëyma.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as Nàttangoo_xëyma:
                Nàttangoo_xëyma.settimeout(5);Nàttangoo_xëyma.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert Nàttangoo_xëyma.recvfrom(512)[0]==b'UDP-IN'
            Tekst=수신하기();assert 'INBOUND TCP UDP PASS' in Tekst and 'exit 0' in Tekst,Tekst
            wéral_tënk['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            bara_denc_toxal_jokkalóo.delete('서버시험.class')
            ndigal_SEQUENCE = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.bara_denc.biir("aot.txt", "한글 AOT bara_denc 😀"); 한국어.자체.출력.biir_buum(한국어.자체.bara_denc.읽기("aot.txt")); } }'
            bara_denc_toxal_jokkalóo.storbinary('STOR 빛.java', io.BytesIO(ndigal_SEQUENCE.encode()))
            Tekst = Wëreef('javac 빛.java'); assert 'exit 0' in Tekst and 'Compiled:' in Tekst, Tekst
            Tekst = Wëreef('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = Wëreef('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT bara_denc 😀' in Tekst and 'exit 0' in Tekst, Tekst
            자체실행파일 = bytearray(); bara_denc_toxal_jokkalóo.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Tekst = Wëreef('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Tekst and 'unsupported' in Tekst, Tekst
            보존자료 = bytearray(); bara_denc_toxal_jokkalóo.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); bara_denc_toxal_jokkalóo.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            bara_denc_toxal_jokkalóo.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Tekst = Wëreef('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = Wëreef('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT bara_denc 😀' in Tekst and 'exit 0' in Tekst, Tekst
            wéral_tënk['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            wéral_tënk['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            Soppeekoodi_Cosaan=결과자료/'정적시험.java'
            Soppeekoodi_Cosaan.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] xëyma = new int[] {기준, 합(10)};
  System.out.println(xëyma[0] + xëyma[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(Soppeekoodi_Cosaan)])
            bara_denc_toxal_jokkalóo.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            Tekst=Wëreef('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Tekst,Tekst
            Tekst=Wëreef('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Tekst,Tekst
            bara_denc_toxal_jokkalóo.delete('정적시험.class');bara_denc_toxal_jokkalóo.delete('정적시험.elf')
            wéral_tënk['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(denc.getvalue());손상자료[14]^=1
            bara_denc_toxal_jokkalóo.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Tekst=Wëreef('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Tekst,Tekst
            wéral_tënk['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            bara_denc_toxal_jokkalóo.quit(); assert 'FTP stopped' in Wëreef('ftpd stop')
            assert not poŋ.njumte, poŋ.njumte
            wéral_tënk.update(passed=True, frames_to_guest=poŋ.커널수신틀수, frames_from_guest=poŋ.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in tànnkat.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            poŋ.Ajandi_xewxew.set()
            yokkute.terminate()
            try: yokkute.wait(timeout=5)
            except subprocess.TimeoutExpired: yokkute.kill(); yokkute.wait()
            tànnkat.close(); yokkute.stdin.close(); yokkute.stdout.close()
            wéral_tënk['bridge_error'] = poŋ.njumte
            wéral_tënk['frames_to_guest'] = poŋ.커널수신틀수; wéral_tënk['frames_from_guest'] = poŋ.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(poŋ.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(wéral_tënk, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': daw()
