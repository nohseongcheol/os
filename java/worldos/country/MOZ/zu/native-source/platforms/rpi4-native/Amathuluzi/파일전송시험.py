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
from iNethiwekhi_ibhuloho import iNethiwekhi_ibhuloho
from yenza_umyalo import 기준, Umlayelo
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Sebenzisa():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    ukufakazisa_umbiko = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { Isi_Zulu.자체.출력.bhala_umugqa("JAR yenza_umyalo: " + 인수[0]); Isi_Zulu.자체.Ihele.Bhala("jar.txt", "자체 ikhenela_inani Ihele"); Isi_Zulu.자체.출력.bhala_umugqa(Isi_Zulu.자체.Ihele.Funda("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    londoloza = io.BytesIO()
    with zipfile.ZipFile(londoloza, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); Iseva_Stream_intuba = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with iNethiwekhi_ibhuloho(접속번호, ['tcp:{}:9300'.format(Iseva_Stream_intuba), 'udp:{}:9301'.format(서버전문접속번호)], thwebula=True) as ibhuloho:
        Inqubo = subprocess.Popen(Umlayelo() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ibhuloho.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        isiqoki = selectors.DefaultSelector(); isiqoki.register(Inqubo.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            imininingwane = bytearray(); yekisa_I_ofisethi = time.monotonic() + 시간제한
            while 확인표시 not in imininingwane:
                if time.monotonic() > yekisa_I_ofisethi or Inqubo.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + imininingwane.decode('utf-8', 'replace'))
                for 누름값, _ in isiqoki.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: imininingwane.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in imininingwane or b'FAIL ' in imininingwane: raise AssertionError(imininingwane)
            return imininingwane.decode('utf-8', 'replace').replace('\r\n', '\n')
        def isihumushi_miyalelo(umugqa):
            Inqubo.stdin.write(umugqa.encode() + b'\n'); Inqubo.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in isihumushi_miyalelo('ftpd start')
            ifayela_dlulisa_uxhumano = ftplib.FTP(); ifayela_dlulisa_uxhumano.encoding = 'utf-8'; ifayela_dlulisa_uxhumano.connect('127.0.0.1', 접속번호, timeout=20); ifayela_dlulisa_uxhumano.login()
            ukulayisha_okukhokhelwayo_imininingwane = bytes(range(256)) * 32
            ifayela_dlulisa_uxhumano.storbinary('STOR binary.dat', io.BytesIO(ukulayisha_okukhokhelwayo_imininingwane))
            결과 = bytearray(); ifayela_dlulisa_uxhumano.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ukulayisha_okukhokhelwayo_imininingwane; assert ifayela_dlulisa_uxhumano.size('binary.dat') == len(ukulayisha_okukhokhelwayo_imininingwane)
            ukufakazisa_umbiko['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ifayela_dlulisa_uxhumano.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in isihumushi_miyalelo('cat 한글.txt')
            assert '한글.txt' in ifayela_dlulisa_uxhumano.nlst()
            assert dict(ifayela_dlulisa_uxhumano.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            ukufakazisa_umbiko['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ifayela_dlulisa_uxhumano.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); ifayela_dlulisa_uxhumano.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == ukulayisha_okukhokhelwayo_imininingwane
            ukufakazisa_umbiko['checks'].append('oversized replacement rejected; previous file preserved')
            with ifayela_dlulisa_uxhumano.transfercmd('STOR pending.txt') as layisha_Amafayela:
                # A control command must not change the active upload's destination.
                assert ifayela_dlulisa_uxhumano.size('binary.dat') == len(ukulayisha_okukhokhelwayo_imininingwane)
                layisha_Amafayela.sendall(b'UPLOAD TARGET PRESERVED')
            assert ifayela_dlulisa_uxhumano.voidresp().startswith('226')
            결과 = bytearray(); ifayela_dlulisa_uxhumano.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); ifayela_dlulisa_uxhumano.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ukulayisha_okukhokhelwayo_imininingwane
            ifayela_dlulisa_uxhumano.delete('pending.txt')
            ukufakazisa_umbiko['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ifayela_dlulisa_uxhumano.storbinary('STOR 인사.jar', io.BytesIO(londoloza.getvalue()))
            Itekisi = isihumushi_miyalelo('java -jar 인사.jar 누리')
            assert 'JAR yenza_umyalo: 누리' in Itekisi and '자체 ikhenela_inani Ihele' in Itekisi and 'exit 0' in Itekisi, Itekisi
            Itekisi = isihumushi_miyalelo('./인사.jar 세상')
            assert 'JAR yenza_umyalo: 세상' in Itekisi and 'exit 0' in Itekisi, Itekisi
            ukufakazisa_umbiko['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct imininingwane { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct imininingwane inani = {합(10), 1.25}; if (inani.수 != 55 || inani.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = vula_ifayela("cc.txt", fundeka_bhaleka | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; bhala_ifayela_imininingwane(문서, 인사, sizeof(인사)-1); vala_ifayela(문서); bhala_ifayela_imininingwane(1, 인사, sizeof(인사)-1); return 0; }\n'
            ifayela_dlulisa_uxhumano.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Itekisi = isihumushi_miyalelo('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Itekisi and 'exit 0' in Itekisi, Itekisi
            Itekisi = isihumushi_miyalelo('run 한글.elf'); assert 'CC NATIVE PASS' in Itekisi and 'exit 0' in Itekisi, Itekisi
            assert 'CC NATIVE PASS' in isihumushi_miyalelo('cat cc.txt')
            실행파일 = bytearray(); ifayela_dlulisa_uxhumano.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ifayela_dlulisa_uxhumano.storbinary('STOR kopisha_inani.elf', io.BytesIO(실행파일)); Itekisi = isihumushi_miyalelo('run kopisha_inani.elf'); assert 'CC NATIVE PASS' in Itekisi and 'exit 0' in Itekisi, Itekisi
            ifayela_dlulisa_uxhumano.storbinary('STOR yenza_umyalo', io.BytesIO(실행파일)); Itekisi=isihumushi_miyalelo('./yenza_umyalo');assert 'CC NATIVE PASS' in Itekisi and 'exit 0' in Itekisi,Itekisi
            ifayela_dlulisa_uxhumano.storbinary('STOR Igama.txt', io.BytesIO(실행파일)); Itekisi=isihumushi_miyalelo('./Igama.txt');assert 'CC NATIVE PASS' in Itekisi and 'exit 0' in Itekisi,Itekisi
            isihumushi_miyalelo('rm yenza_umyalo Igama.txt')
            ukufakazisa_umbiko['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            isihumushi_miyalelo('rm binary.dat 한글.txt 한글.c 한글.elf kopisha_inani.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            ifayela_dlulisa_uxhumano.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Itekisi=isihumushi_miyalelo('./리눅스인사');assert 'exit -8' in Itekisi,Itekisi
            Itekisi=isihumushi_miyalelo('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Itekisi,Itekisi
            assert 'LINUX ELF FILE IO' in isihumushi_miyalelo('cat linux.txt')
            ifayela_dlulisa_uxhumano.delete('리눅스인사');ifayela_dlulisa_uxhumano.delete('linux.txt')
            ifayela_dlulisa_uxhumano.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in isihumushi_miyalelo('./거짓.elf');ifayela_dlulisa_uxhumano.delete('거짓.elf')
            ukufakazisa_umbiko['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Xhumanisa = Isi_Zulu.자체.연결통신.Xhumanisa("10.0.2.2", Integer.parseInt(args[0]));
 Xhumanisa.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] umthombo = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<umthombo.length;i++) if (Xhumanisa.getInputStream().read() != (umthombo[i]&255)) throw new RuntimeException("TCP mismatch");
 Xhumanisa.close();
 DatagramSocket 종단 = Isi_Zulu.자체.통신.Vula(0); Isi_Zulu.자체.통신.대기시간(종단, 500);
 Isi_Zulu.자체.통신.Thumela(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Isi_Zulu.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                ifayela_dlulisa_uxhumano.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                Itekisi = isihumushi_miyalelo('java 바깥통신 {} {}'.format(되돌림서버항목.i_TCP_intuba, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in Itekisi and '10.0.2.2' in Itekisi and 'exit 0' in Itekisi, Itekisi
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            ukufakazisa_umbiko['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ifayela_dlulisa_uxhumano.delete('바깥통신.class')
            Iseva_umthombo=결과자료/'서버시험.java'
            Iseva_umthombo.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket Iseva_inani = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket isivakashi_inani = Iseva_inani.accept();
  isivakashi_inani.getOutputStream().write(isivakashi_inani.getInputStream().read()+1); isivakashi_inani.close(); Iseva_inani.close();
  byte[] Okuqukethwe_inani = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Okuqukethwe_inani, Okuqukethwe_inani.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(Iseva_umthombo)])
            ifayela_dlulisa_uxhumano.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            Inqubo.stdin.write('java 서버시험\n'.encode());Inqubo.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',Iseva_Stream_intuba),timeout=5) as untanga_inani:
                untanga_inani.sendall(b'A');assert untanga_inani.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as untanga_inani:
                untanga_inani.settimeout(5);untanga_inani.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert untanga_inani.recvfrom(512)[0]==b'UDP-IN'
            Itekisi=수신하기();assert 'INBOUND TCP UDP PASS' in Itekisi and 'exit 0' in Itekisi,Itekisi
            ukufakazisa_umbiko['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ifayela_dlulisa_uxhumano.delete('서버시험.class')
            umyalelo_UKULANDELANA = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } Isi_Zulu.자체.출력.수쓰기(합); Isi_Zulu.자체.Ihele.Bhala("aot.txt", "한글 AOT Ihele 😀"); Isi_Zulu.자체.출력.bhala_umugqa(Isi_Zulu.자체.Ihele.Funda("aot.txt")); } }'
            ifayela_dlulisa_uxhumano.storbinary('STOR 빛.java', io.BytesIO(umyalelo_UKULANDELANA.encode()))
            Itekisi = isihumushi_miyalelo('javac 빛.java'); assert 'exit 0' in Itekisi and 'Compiled:' in Itekisi, Itekisi
            Itekisi = isihumushi_miyalelo('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Itekisi and 'exit 0' in Itekisi, Itekisi
            Itekisi = isihumushi_miyalelo('run 빛.elf'); assert '\n55\n' in Itekisi and '한글 AOT Ihele 😀' in Itekisi and 'exit 0' in Itekisi, Itekisi
            자체실행파일 = bytearray(); ifayela_dlulisa_uxhumano.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Itekisi = isihumushi_miyalelo('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Itekisi and 'unsupported' in Itekisi, Itekisi
            보존자료 = bytearray(); ifayela_dlulisa_uxhumano.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ifayela_dlulisa_uxhumano.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ifayela_dlulisa_uxhumano.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Itekisi = isihumushi_miyalelo('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Itekisi and 'exit 0' in Itekisi, Itekisi
            Itekisi = isihumushi_miyalelo('run 빛.elf'); assert '\n55\n' in Itekisi and '한글 AOT Ihele 😀' in Itekisi and 'exit 0' in Itekisi, Itekisi
            ukufakazisa_umbiko['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            ukufakazisa_umbiko['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ngaguquki_umthombo=결과자료/'정적시험.java'
            ngaguquki_umthombo.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] inani = new int[] {기준, 합(10)};
  System.out.println(inani[0] + inani[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(ngaguquki_umthombo)])
            ifayela_dlulisa_uxhumano.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            Itekisi=isihumushi_miyalelo('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Itekisi,Itekisi
            Itekisi=isihumushi_miyalelo('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Itekisi,Itekisi
            ifayela_dlulisa_uxhumano.delete('정적시험.class');ifayela_dlulisa_uxhumano.delete('정적시험.elf')
            ukufakazisa_umbiko['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(londoloza.getvalue());손상자료[14]^=1
            ifayela_dlulisa_uxhumano.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Itekisi=isihumushi_miyalelo('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Itekisi,Itekisi
            ukufakazisa_umbiko['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ifayela_dlulisa_uxhumano.quit(); assert 'FTP stopped' in isihumushi_miyalelo('ftpd stop')
            assert not ibhuloho.Iphutha, ibhuloho.Iphutha
            ukufakazisa_umbiko.update(passed=True, frames_to_guest=ibhuloho.커널수신틀수, frames_from_guest=ibhuloho.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in isiqoki.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            ibhuloho.phumuza_isikhashana_isigameko.set()
            Inqubo.terminate()
            try: Inqubo.wait(timeout=5)
            except subprocess.TimeoutExpired: Inqubo.kill(); Inqubo.wait()
            isiqoki.close(); Inqubo.stdin.close(); Inqubo.stdout.close()
            ukufakazisa_umbiko['bridge_error'] = ibhuloho.Iphutha
            ukufakazisa_umbiko['frames_to_guest'] = ibhuloho.커널수신틀수; ukufakazisa_umbiko['frames_from_guest'] = ibhuloho.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(ibhuloho.ithreyisi_loga,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(ukufakazisa_umbiko, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Sebenzisa()
