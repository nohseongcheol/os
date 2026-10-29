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
from Şəbəkə_körpü import Şəbəkə_körpü
from icra_etmək_əmr import Project_kök, Əmr
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def İcra_Et():
    ölçü_verilənlər = Project_kök / 'build/verification/ftp'; ölçü_verilənlər.mkdir(parents=True, exist_ok=True)
    yoxlama_hesabat = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Project_kök / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = ölçü_verilənlər / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.yazmaq_xətt("JAR icra_etmək_əmr: " + 인수[0]); 한국어.자체.FAYL.Yazma("jar.txt", "자체 nüvə_VALUE FAYL"); 한국어.자체.출력.yazmaq_xətt(한국어.자체.FAYL.Oxuma("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_kök/'build/java-library/classes'), '-d', str(ölçü_verilənlər), str(자바원문)])
    Arxiv = io.BytesIO()
    with zipfile.ZipFile(Arxiv, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(ölçü_verilənlər/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_axın_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Şəbəkə_körpü(접속번호, ['tcp:{}:9300'.format(server_axın_port), 'udp:{}:9301'.format(서버전문접속번호)], çəkmək=True) as körpü:
        Proses = subprocess.Popen(Əmr() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + körpü.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        seçici = selectors.DefaultSelector(); seçici.register(Proses.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            verilənlər = bytearray(); bitirmək_OFFSET = time.monotonic() + 시간제한
            while 확인표시 not in verilənlər:
                if time.monotonic() > bitirmək_OFFSET or Proses.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + verilənlər.decode('utf-8', 'replace'))
                for 누름값, _ in seçici.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: verilənlər.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in verilənlər or b'FAIL ' in verilənlər: raise AssertionError(verilənlər)
            return verilənlər.decode('utf-8', 'replace').replace('\r\n', '\n')
        def örtük(Giriş):
            Proses.stdin.write(Giriş.encode() + b'\n'); Proses.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in örtük('ftpd start')
            fayl_ötürmə_qoşulma = ftplib.FTP(); fayl_ötürmə_qoşulma.encoding = 'utf-8'; fayl_ötürmə_qoşulma.connect('127.0.0.1', 접속번호, timeout=20); fayl_ötürmə_qoşulma.login()
            faydalı_yük_verilənlər = bytes(range(256)) * 32
            fayl_ötürmə_qoşulma.storbinary('STOR binary.dat', io.BytesIO(faydalı_yük_verilənlər))
            ölçü = bytearray(); fayl_ötürmə_qoşulma.retrbinary('RETR binary.dat', ölçü.extend)
            assert ölçü == faydalı_yük_verilənlər; assert fayl_ötürmə_qoşulma.size('binary.dat') == len(faydalı_yük_verilənlər)
            yoxlama_hesabat['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            fayl_ötürmə_qoşulma.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in örtük('cat 한글.txt')
            assert '한글.txt' in fayl_ötürmə_qoşulma.nlst()
            assert dict(fayl_ötürmə_qoşulma.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            yoxlama_hesabat['checks'].append('UTF-8 filename and content visible in guest shell')
            try: fayl_ötürmə_qoşulma.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            ölçü = bytearray(); fayl_ötürmə_qoşulma.retrbinary('RETR binary.dat', ölçü.extend); assert ölçü == faydalı_yük_verilənlər
            yoxlama_hesabat['checks'].append('oversized replacement rejected; previous file preserved')
            with fayl_ötürmə_qoşulma.transfercmd('STOR pending.txt') as Upload_Fayllar:
                # A control command must not change the active upload's destination.
                assert fayl_ötürmə_qoşulma.size('binary.dat') == len(faydalı_yük_verilənlər)
                Upload_Fayllar.sendall(b'UPLOAD TARGET PRESERVED')
            assert fayl_ötürmə_qoşulma.voidresp().startswith('226')
            ölçü = bytearray(); fayl_ötürmə_qoşulma.retrbinary('RETR pending.txt', ölçü.extend)
            assert ölçü == b'UPLOAD TARGET PRESERVED'
            ölçü = bytearray(); fayl_ötürmə_qoşulma.retrbinary('RETR binary.dat', ölçü.extend)
            assert ölçü == faydalı_yük_verilənlər
            fayl_ötürmə_qoşulma.delete('pending.txt')
            yoxlama_hesabat['checks'].append('interleaved SIZE cannot change the active STOR destination')
            fayl_ötürmə_qoşulma.storbinary('STOR 인사.jar', io.BytesIO(Arxiv.getvalue()))
            Mətn = örtük('java -jar 인사.jar 누리')
            assert 'JAR icra_etmək_əmr: 누리' in Mətn and '자체 nüvə_VALUE FAYL' in Mətn and 'exit 0' in Mətn, Mətn
            Mətn = örtük('./인사.jar 세상')
            assert 'JAR icra_etmək_əmr: 세상' in Mətn and 'exit 0' in Mətn, Mətn
            yoxlama_hesabat['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct verilənlər { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct verilənlər VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = açmaq_fayl("cc.txt", oxunan_yazılan | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; yazmaq_fayl_verilənlər(문서, 인사, sizeof(인사)-1); bağlamaq_fayl(문서); yazmaq_fayl_verilənlər(1, 인사, sizeof(인사)-1); return 0; }\n'
            fayl_ötürmə_qoşulma.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Mətn = örtük('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Mətn and 'exit 0' in Mətn, Mətn
            Mətn = örtük('run 한글.elf'); assert 'CC NATIVE PASS' in Mətn and 'exit 0' in Mətn, Mətn
            assert 'CC NATIVE PASS' in örtük('cat cc.txt')
            실행파일 = bytearray(); fayl_ötürmə_qoşulma.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            fayl_ötürmə_qoşulma.storbinary('STOR nümunə_VALUE.elf', io.BytesIO(실행파일)); Mətn = örtük('run nümunə_VALUE.elf'); assert 'CC NATIVE PASS' in Mətn and 'exit 0' in Mətn, Mətn
            fayl_ötürmə_qoşulma.storbinary('STOR icra_etmək_əmr', io.BytesIO(실행파일)); Mətn=örtük('./icra_etmək_əmr');assert 'CC NATIVE PASS' in Mətn and 'exit 0' in Mətn,Mətn
            fayl_ötürmə_qoşulma.storbinary('STOR Ad.txt', io.BytesIO(실행파일)); Mətn=örtük('./Ad.txt');assert 'CC NATIVE PASS' in Mətn and 'exit 0' in Mətn,Mətn
            örtük('rm icra_etmək_əmr Ad.txt')
            yoxlama_hesabat['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            örtük('rm binary.dat 한글.txt 한글.c 한글.elf nümunə_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(ölçü_verilənlər/'linux-reference')
            fayl_ötürmə_qoşulma.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Mətn=örtük('./리눅스인사');assert 'exit -8' in Mətn,Mətn
            Mətn=örtük('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Mətn,Mətn
            assert 'LINUX ELF FILE IO' in örtük('cat linux.txt')
            fayl_ötürmə_qoşulma.delete('리눅스인사');fayl_ötürmə_qoşulma.delete('linux.txt')
            fayl_ötürmə_qoşulma.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in örtük('./FALSE_VALUE.elf');fayl_ötürmə_qoşulma.delete('FALSE_VALUE.elf')
            yoxlama_hesabat['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = ölçü_verilənlər/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Bağlan = 한국어.자체.연결통신.Bağlan("10.0.2.2", Integer.parseInt(args[0]));
 Bağlan.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] QAYNAQ = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<QAYNAQ.length;i++) if (Bağlan.getInputStream().read() != (QAYNAQ[i]&255)) throw new RuntimeException("TCP mismatch");
 Bağlan.close();
 DatagramSocket 종단 = 한국어.자체.통신.Aç(0); 한국어.자체.통신.FASİLƏ(종단, 500);
 한국어.자체.통신.göndərmək(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_kök/'build/java-library/classes'),'-d',str(ölçü_verilənlər),str(통신원문)])
                fayl_ötürmə_qoşulma.storbinary('STOR 바깥통신.class', io.BytesIO((ölçü_verilənlər/'바깥통신.class').read_bytes()))
                Mətn = örtük('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_port, 되돌림서버항목.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in Mətn and '10.0.2.2' in Mətn and 'exit 0' in Mətn, Mətn
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            yoxlama_hesabat['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            fayl_ötürmə_qoşulma.delete('바깥통신.class')
            server_mənbə=ölçü_verilənlər/'서버시험.java'
            server_mənbə.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket qonaq_VALUE = server_VALUE.accept();
  qonaq_VALUE.getOutputStream().write(qonaq_VALUE.getInputStream().read()+1); qonaq_VALUE.close(); server_VALUE.close();
  byte[] Məzmun_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Məzmun_VALUE, Məzmun_VALUE.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ölçü_verilənlər),str(server_mənbə)])
            fayl_ötürmə_qoşulma.storbinary('STOR 서버시험.class',io.BytesIO((ölçü_verilənlər/'서버시험.class').read_bytes()))
            Proses.stdin.write('java 서버시험\n'.encode());Proses.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_axın_port),timeout=5) as eynisəviyyəli_VALUE:
                eynisəviyyəli_VALUE.sendall(b'A');assert eynisəviyyəli_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as eynisəviyyəli_VALUE:
                eynisəviyyəli_VALUE.settimeout(5);eynisəviyyəli_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert eynisəviyyəli_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Mətn=수신하기();assert 'INBOUND TCP UDP PASS' in Mətn and 'exit 0' in Mətn,Mətn
            yoxlama_hesabat['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            fayl_ötürmə_qoşulma.delete('서버시험.class')
            təlimat_SEQUENCE = 'public class 빛 { public static void main(String[] 인수) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(SUM_VALUE); 한국어.자체.FAYL.Yazma("aot.txt", "한글 AOT FAYL 😀"); 한국어.자체.출력.yazmaq_xətt(한국어.자체.FAYL.Oxuma("aot.txt")); } }'
            fayl_ötürmə_qoşulma.storbinary('STOR 빛.java', io.BytesIO(təlimat_SEQUENCE.encode()))
            Mətn = örtük('javac 빛.java'); assert 'exit 0' in Mətn and 'Compiled:' in Mətn, Mətn
            Mətn = örtük('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Mətn and 'exit 0' in Mətn, Mətn
            Mətn = örtük('run 빛.elf'); assert '\n55\n' in Mətn and '한글 AOT FAYL 😀' in Mətn and 'exit 0' in Mətn, Mətn
            자체실행파일 = bytearray(); fayl_ötürmə_qoşulma.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Mətn = örtük('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Mətn and 'unsupported' in Mətn, Mətn
            보존자료 = bytearray(); fayl_ötürmə_qoşulma.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); fayl_ötürmə_qoşulma.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            fayl_ötürmə_qoşulma.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Mətn = örtük('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Mətn and 'exit 0' in Mətn, Mətn
            Mətn = örtük('run 빛.elf'); assert '\n55\n' in Mətn and '한글 AOT FAYL 😀' in Mətn and 'exit 0' in Mətn, Mətn
            yoxlama_hesabat['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            yoxlama_hesabat['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statik_mənbə=ölçü_verilənlər/'정적시험.java'
            statik_mənbə.write_text('''public class 정적시험 {
 static int Project_kök = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] 인수) {
  int[] VALUE = new int[] {Project_kök, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ölçü_verilənlər),str(statik_mənbə)])
            fayl_ötürmə_qoşulma.storbinary('STOR 정적시험.class',io.BytesIO((ölçü_verilənlər/'정적시험.class').read_bytes()))
            Mətn=örtük('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Mətn,Mətn
            Mətn=örtük('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Mətn,Mətn
            fayl_ötürmə_qoşulma.delete('정적시험.class');fayl_ötürmə_qoşulma.delete('정적시험.elf')
            yoxlama_hesabat['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arxiv.getvalue());손상자료[14]^=1
            fayl_ötürmə_qoşulma.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Mətn=örtük('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Mətn,Mətn
            yoxlama_hesabat['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            fayl_ötürmə_qoşulma.quit(); assert 'FTP stopped' in örtük('ftpd stop')
            assert not körpü.XƏTA, körpü.XƏTA
            yoxlama_hesabat.update(passed=True, frames_to_guest=körpü.커널수신틀수, frames_from_guest=körpü.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in seçici.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            körpü.pauza_hadisə.set()
            Proses.terminate()
            try: Proses.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
            seçici.close(); Proses.stdin.close(); Proses.stdout.close()
            yoxlama_hesabat['bridge_error'] = körpü.XƏTA
            yoxlama_hesabat['frames_to_guest'] = körpü.커널수신틀수; yoxlama_hesabat['frames_from_guest'] = körpü.커널발신틀수
            (ölçü_verilənlər/'packets.json').write_text(json.dumps(körpü.iz_LOG,indent=2)+'\n')
            (ölçü_verilənlər / 'serial.log').write_bytes(대화기록)
            (ölçü_verilənlər / 'report.json').write_text(json.dumps(yoxlama_hesabat, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': İcra_Et()
