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
from Net_brú import Net_brú
from keyra_skipun import verk_rót, Skipun
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Keyra_2():
    mæld_stærð_gögn = verk_rót / 'build/verification/ftp'; mæld_stærð_gögn.mkdir(parents=True, exist_ok=True)
    prófun_skrá = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((verk_rót / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = mæld_stærð_gögn / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Viðföng) throws Exception { Íslenska.eigin.úttak.skrifa_lína("JAR keyra_skipun: " + Viðföng[0]); Íslenska.eigin.Skrá.Skrift("jar.txt", "eigin kjarni_VALUE Skrá"); Íslenska.eigin.úttak.skrifa_lína(Íslenska.eigin.Skrá.Lestur("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(verk_rót/'build/java-library/classes'), '-d', str(mæld_stærð_gögn), str(자바원문)])
    Safn = io.BytesIO()
    with zipfile.ZipFile(Safn, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(mæld_stærð_gögn/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); tengisnúmer = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); þjónn_Stream_gátt = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Net_brú(tengisnúmer, ['tcp:{}:9300'.format(þjónn_Stream_gátt), 'udp:{}:9301'.format(서버전문접속번호)], fanga=True) as brú:
        Ferli = subprocess.Popen(Skipun() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + brú.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        val = selectors.DefaultSelector(); val.register(Ferli.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            gögn = bytearray(); ljúka_OFFSET = time.monotonic() + 시간제한
            while 확인표시 not in gögn:
                if time.monotonic() > ljúka_OFFSET or Ferli.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + gögn.decode('utf-8', 'replace'))
                for 누름값, _ in val.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: gögn.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in gögn or b'FAIL ' in gögn: raise AssertionError(gögn)
            return gögn.decode('utf-8', 'replace').replace('\r\n', '\n')
        def skel(Lína):
            Ferli.stdin.write(Lína.encode() + b'\n'); Ferli.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in skel('ftpd start')
            skrá_flytja_tenging = ftplib.FTP(); skrá_flytja_tenging.encoding = 'utf-8'; skrá_flytja_tenging.connect('127.0.0.1', tengisnúmer, timeout=20); skrá_flytja_tenging.login()
            farmur_gögn = bytes(range(256)) * 32
            skrá_flytja_tenging.storbinary('STOR binary.dat', io.BytesIO(farmur_gögn))
            NIÐURSTAÐA = bytearray(); skrá_flytja_tenging.retrbinary('RETR binary.dat', NIÐURSTAÐA.extend)
            assert NIÐURSTAÐA == farmur_gögn; assert skrá_flytja_tenging.size('binary.dat') == len(farmur_gögn)
            prófun_skrá['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            skrá_flytja_tenging.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in skel('cat 한글.txt')
            assert '한글.txt' in skrá_flytja_tenging.nlst()
            assert dict(skrá_flytja_tenging.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            prófun_skrá['checks'].append('UTF-8 filename and content visible in guest shell')
            try: skrá_flytja_tenging.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            NIÐURSTAÐA = bytearray(); skrá_flytja_tenging.retrbinary('RETR binary.dat', NIÐURSTAÐA.extend); assert NIÐURSTAÐA == farmur_gögn
            prófun_skrá['checks'].append('oversized replacement rejected; previous file preserved')
            with skrá_flytja_tenging.transfercmd('STOR pending.txt') as hlaða_upp_Skrár:
                # A control command must not change the active upload's destination.
                assert skrá_flytja_tenging.size('binary.dat') == len(farmur_gögn)
                hlaða_upp_Skrár.sendall(b'UPLOAD TARGET PRESERVED')
            assert skrá_flytja_tenging.voidresp().startswith('226')
            NIÐURSTAÐA = bytearray(); skrá_flytja_tenging.retrbinary('RETR pending.txt', NIÐURSTAÐA.extend)
            assert NIÐURSTAÐA == b'UPLOAD TARGET PRESERVED'
            NIÐURSTAÐA = bytearray(); skrá_flytja_tenging.retrbinary('RETR binary.dat', NIÐURSTAÐA.extend)
            assert NIÐURSTAÐA == farmur_gögn
            skrá_flytja_tenging.delete('pending.txt')
            prófun_skrá['checks'].append('interleaved SIZE cannot change the active STOR destination')
            skrá_flytja_tenging.storbinary('STOR 인사.jar', io.BytesIO(Safn.getvalue()))
            Texti = skel('java -jar 인사.jar 누리')
            assert 'JAR keyra_skipun: 누리' in Texti and 'eigin kjarni_VALUE Skrá' in Texti and 'exit 0' in Texti, Texti
            Texti = skel('./인사.jar 세상')
            assert 'JAR keyra_skipun: 세상' in Texti and 'exit 0' in Texti, Texti
            prófun_skrá['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct gögn { int númer; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct gögn VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.númer != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = opið_skrá("cc.txt", les_skrifheimild | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; skrifa_skrá_gögn(문서, 인사, sizeof(인사)-1); loka_skrá(문서); skrifa_skrá_gögn(1, 인사, sizeof(인사)-1); return 0; }\n'
            skrá_flytja_tenging.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Texti = skel('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Texti and 'exit 0' in Texti, Texti
            Texti = skel('run 한글.elf'); assert 'CC NATIVE PASS' in Texti and 'exit 0' in Texti, Texti
            assert 'CC NATIVE PASS' in skel('cat cc.txt')
            실행파일 = bytearray(); skrá_flytja_tenging.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            skrá_flytja_tenging.storbinary('STOR afrita_VALUE.elf', io.BytesIO(실행파일)); Texti = skel('run afrita_VALUE.elf'); assert 'CC NATIVE PASS' in Texti and 'exit 0' in Texti, Texti
            skrá_flytja_tenging.storbinary('STOR keyra_skipun', io.BytesIO(실행파일)); Texti=skel('./keyra_skipun');assert 'CC NATIVE PASS' in Texti and 'exit 0' in Texti,Texti
            skrá_flytja_tenging.storbinary('STOR Heiti.txt', io.BytesIO(실행파일)); Texti=skel('./Heiti.txt');assert 'CC NATIVE PASS' in Texti and 'exit 0' in Texti,Texti
            skel('rm keyra_skipun Heiti.txt')
            prófun_skrá['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            skel('rm binary.dat 한글.txt 한글.c 한글.elf afrita_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(mæld_stærð_gögn/'linux-reference')
            skrá_flytja_tenging.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Texti=skel('./리눅스인사');assert 'exit -8' in Texti,Texti
            Texti=skel('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Texti,Texti
            assert 'LINUX ELF FILE IO' in skel('cat linux.txt')
            skrá_flytja_tenging.delete('리눅스인사');skrá_flytja_tenging.delete('linux.txt')
            skrá_flytja_tenging.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 númer 없습니다:' in skel('./FALSE_VALUE.elf');skrá_flytja_tenging.delete('FALSE_VALUE.elf')
            prófun_skrá['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                nettó_uppruni = mæld_stærð_gögn/'바깥통신.java'
                nettó_uppruni.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Tengjast = Íslenska.eigin.tenging_flutningur.Tengjast("10.0.2.2", Integer.parseInt(args[0]));
 Tengjast.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] Uppruni = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<Uppruni.length;i++) if (Tengjast.getInputStream().read() != (Uppruni[i]&255)) throw new RuntimeException("TCP mismatch");
 Tengjast.close();
 DatagramSocket endastöð = Íslenska.eigin.통신.Opna(0); Íslenska.eigin.통신.TIMEOUT(endastöð, 500);
 Íslenska.eigin.통신.senda(endastöð, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Íslenska.eigin.통신.받기(endastöð).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 endastöð.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(verk_rót/'build/java-library/classes'),'-d',str(mæld_stærð_gögn),str(nettó_uppruni)])
                skrá_flytja_tenging.storbinary('STOR 바깥통신.class', io.BytesIO((mæld_stærð_gögn/'바깥통신.class').read_bytes()))
                Texti = skel('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_gátt, 되돌림서버항목.UDP_gátt))
                assert 'EXTERNAL TCP UDP PASS' in Texti and '10.0.2.2' in Texti and 'exit 0' in Texti, Texti
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            prófun_skrá['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            skrá_flytja_tenging.delete('바깥통신.class')
            þjónn_uppruni=mæld_stærð_gögn/'서버시험.java'
            þjónn_uppruni.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket þjónn_VALUE = new ServerSocket(9300); DatagramSocket endastöð = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gestur_VALUE = þjónn_VALUE.accept();
  gestur_VALUE.getOutputStream().write(gestur_VALUE.getInputStream().read()+1); gestur_VALUE.close(); þjónn_VALUE.close();
  byte[] Efni_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Efni_VALUE, Efni_VALUE.length); endastöð.receive(전문);
  endastöð.send(전문); endastöð.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mæld_stærð_gögn),str(þjónn_uppruni)])
            skrá_flytja_tenging.storbinary('STOR 서버시험.class',io.BytesIO((mæld_stærð_gögn/'서버시험.class').read_bytes()))
            Ferli.stdin.write('java 서버시험\n'.encode());Ferli.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',þjónn_Stream_gátt),timeout=5) as jafningi_VALUE:
                jafningi_VALUE.sendall(b'A');assert jafningi_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as jafningi_VALUE:
                jafningi_VALUE.settimeout(5);jafningi_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert jafningi_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Texti=수신하기();assert 'INBOUND TCP UDP PASS' in Texti and 'exit 0' in Texti,Texti
            prófun_skrá['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            skrá_flytja_tenging.delete('서버시험.class')
            skipun_SEQUENCE = 'public class 빛 { public static void main(String[] Viðföng) throws Exception { int SUM_VALUE = 0; int númer = 1; while (númer <= 10) { SUM_VALUE = SUM_VALUE + númer; númer = númer + 1; } Íslenska.eigin.úttak.skrifa_númer(SUM_VALUE); Íslenska.eigin.Skrá.Skrift("aot.txt", "한글 AOT Skrá 😀"); Íslenska.eigin.úttak.skrifa_lína(Íslenska.eigin.Skrá.Lestur("aot.txt")); } }'
            skrá_flytja_tenging.storbinary('STOR 빛.java', io.BytesIO(skipun_SEQUENCE.encode()))
            Texti = skel('javac 빛.java'); assert 'exit 0' in Texti and 'Compiled:' in Texti, Texti
            Texti = skel('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Texti and 'exit 0' in Texti, Texti
            Texti = skel('run 빛.elf'); assert '\n55\n' in Texti and '한글 AOT Skrá 😀' in Texti and 'exit 0' in Texti, Texti
            자체실행파일 = bytearray(); skrá_flytja_tenging.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Texti = skel('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Texti and 'unsupported' in Texti, Texti
            보존자료 = bytearray(); skrá_flytja_tenging.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); skrá_flytja_tenging.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            skrá_flytja_tenging.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Texti = skel('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Texti and 'exit 0' in Texti, Texti
            Texti = skel('run 빛.elf'); assert '\n55\n' in Texti and '한글 AOT Skrá 😀' in Texti and 'exit 0' in Texti, Texti
            prófun_skrá['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            prófun_skrá['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            fast_uppruni=mæld_stærð_gögn/'정적시험.java'
            fast_uppruni.write_text('''public class 정적시험 {
 static int verk_rót = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] Viðföng) {
  int[] VALUE = new int[] {verk_rót, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(Viðföng[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mæld_stærð_gögn),str(fast_uppruni)])
            skrá_flytja_tenging.storbinary('STOR 정적시험.class',io.BytesIO((mæld_stærð_gögn/'정적시험.class').read_bytes()))
            Texti=skel('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Texti,Texti
            Texti=skel('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Texti,Texti
            skrá_flytja_tenging.delete('정적시험.class');skrá_flytja_tenging.delete('정적시험.elf')
            prófun_skrá['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Safn.getvalue());손상자료[14]^=1
            skrá_flytja_tenging.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Texti=skel('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Texti,Texti
            prófun_skrá['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            skrá_flytja_tenging.quit(); assert 'FTP stopped' in skel('ftpd stop')
            assert not brú.Villa, brú.Villa
            prófun_skrá.update(passed=True, frames_to_guest=brú.커널수신틀수, frames_from_guest=brú.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in val.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            brú.gera_hlé_atvik.set()
            Ferli.terminate()
            try: Ferli.wait(timeout=5)
            except subprocess.TimeoutExpired: Ferli.kill(); Ferli.wait()
            val.close(); Ferli.stdin.close(); Ferli.stdout.close()
            prófun_skrá['bridge_error'] = brú.Villa
            prófun_skrá['frames_to_guest'] = brú.커널수신틀수; prófun_skrá['frames_from_guest'] = brú.커널발신틀수
            (mæld_stærð_gögn/'packets.json').write_text(json.dumps(brú.spor_LOG,indent=2)+'\n')
            (mæld_stærð_gögn / 'serial.log').write_bytes(대화기록)
            (mæld_stærð_gögn / 'report.json').write_text(json.dumps(prófun_skrá, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Keyra_2()
