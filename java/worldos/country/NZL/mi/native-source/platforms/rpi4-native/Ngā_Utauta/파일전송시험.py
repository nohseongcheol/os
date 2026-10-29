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
from whatunga_arawhata import whatunga_arawhata
from kawe_tono import whakaatu_pūtake, tono
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def whakahaere():
    mēhua_raraunga = whakaatu_pūtake / 'build/verification/ftp'; mēhua_raraunga.mkdir(parents=True, exist_ok=True)
    whakamana_pūrongo = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((whakaatu_pūtake / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = mēhua_raraunga / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { Reo_Māori.자체.출력.tuhi_hononga("JAR kawe_tono: " + 인수[0]); Reo_Māori.자체.Kōnae.Tuhia("jar.txt", "자체 kākano_uara_0611a8a8 Kōnae"); Reo_Māori.자체.출력.tuhi_hononga(Reo_Māori.자체.Kōnae.Pānuitia("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(whakaatu_pūtake/'build/java-library/classes'), '-d', str(mēhua_raraunga), str(자바원문)])
    Pūranga = io.BytesIO()
    with zipfile.ZipFile(Pūranga, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(mēhua_raraunga/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); tūmau_roma_kawe = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with whatunga_arawhata(접속번호, ['tcp:{}:9300'.format(tūmau_roma_kawe), 'udp:{}:9301'.format(서버전문접속번호)], hopu=True) as arawhata:
        Hātepe = subprocess.Popen(tono() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + arawhata.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        pūtīpako = selectors.DefaultSelector(); pūtīpako.register(Hātepe.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            raraunga = bytearray(); mutu_OFFSET = time.monotonic() + 시간제한
            while 확인표시 not in raraunga:
                if time.monotonic() > mutu_OFFSET or Hātepe.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + raraunga.decode('utf-8', 'replace'))
                for 누름값, _ in pūtīpako.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: raraunga.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in raraunga or b'FAIL ' in raraunga: raise AssertionError(raraunga)
            return raraunga.decode('utf-8', 'replace').replace('\r\n', '\n')
        def anga(hononga):
            Hātepe.stdin.write(hononga.encode() + b'\n'); Hātepe.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in anga('ftpd start')
            kōnae_whakawhiti_hononga = ftplib.FTP(); kōnae_whakawhiti_hononga.encoding = 'utf-8'; kōnae_whakawhiti_hononga.connect('127.0.0.1', 접속번호, timeout=20); kōnae_whakawhiti_hononga.login()
            tino_raraunga_raraunga = bytes(range(256)) * 32
            kōnae_whakawhiti_hononga.storbinary('STOR binary.dat', io.BytesIO(tino_raraunga_raraunga))
            mēhua = bytearray(); kōnae_whakawhiti_hononga.retrbinary('RETR binary.dat', mēhua.extend)
            assert mēhua == tino_raraunga_raraunga; assert kōnae_whakawhiti_hononga.size('binary.dat') == len(tino_raraunga_raraunga)
            whakamana_pūrongo['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            kōnae_whakawhiti_hononga.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in anga('cat 한글.txt')
            assert '한글.txt' in kōnae_whakawhiti_hononga.nlst()
            assert dict(kōnae_whakawhiti_hononga.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            whakamana_pūrongo['checks'].append('UTF-8 filename and content visible in guest shell')
            try: kōnae_whakawhiti_hononga.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            mēhua = bytearray(); kōnae_whakawhiti_hononga.retrbinary('RETR binary.dat', mēhua.extend); assert mēhua == tino_raraunga_raraunga
            whakamana_pūrongo['checks'].append('oversized replacement rejected; previous file preserved')
            with kōnae_whakawhiti_hononga.transfercmd('STOR pending.txt') as tukuatu_Ngā_Kōnae:
                # A control command must not change the active upload's destination.
                assert kōnae_whakawhiti_hononga.size('binary.dat') == len(tino_raraunga_raraunga)
                tukuatu_Ngā_Kōnae.sendall(b'UPLOAD TARGET PRESERVED')
            assert kōnae_whakawhiti_hononga.voidresp().startswith('226')
            mēhua = bytearray(); kōnae_whakawhiti_hononga.retrbinary('RETR pending.txt', mēhua.extend)
            assert mēhua == b'UPLOAD TARGET PRESERVED'
            mēhua = bytearray(); kōnae_whakawhiti_hononga.retrbinary('RETR binary.dat', mēhua.extend)
            assert mēhua == tino_raraunga_raraunga
            kōnae_whakawhiti_hononga.delete('pending.txt')
            whakamana_pūrongo['checks'].append('interleaved SIZE cannot change the active STOR destination')
            kōnae_whakawhiti_hononga.storbinary('STOR 인사.jar', io.BytesIO(Pūranga.getvalue()))
            Ngā_kupu = anga('java -jar 인사.jar 누리')
            assert 'JAR kawe_tono: 누리' in Ngā_kupu and '자체 kākano_uara_0611a8a8 Kōnae' in Ngā_kupu and 'exit 0' in Ngā_kupu, Ngā_kupu
            Ngā_kupu = anga('./인사.jar 세상')
            assert 'JAR kawe_tono: 세상' in Ngā_kupu and 'exit 0' in Ngā_kupu, Ngā_kupu
            whakamana_pūrongo['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct raraunga { int 수; double 비율; };\nint SUM_uara(int n) { return n ? n + SUM_uara(n-1) : 0; }\nint main(void) { struct raraunga uara = {SUM_uara(10), 1.25}; if (uara.수 != 55 || uara.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = tiwhikete_kōnae("cc.txt", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; tuhi_kōnae_raraunga(문서, 인사, sizeof(인사)-1); kati_kōnae(문서); tuhi_kōnae_raraunga(1, 인사, sizeof(인사)-1); return 0; }\n'
            kōnae_whakawhiti_hononga.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Ngā_kupu = anga('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Ngā_kupu and 'exit 0' in Ngā_kupu, Ngā_kupu
            Ngā_kupu = anga('run 한글.elf'); assert 'CC NATIVE PASS' in Ngā_kupu and 'exit 0' in Ngā_kupu, Ngā_kupu
            assert 'CC NATIVE PASS' in anga('cat cc.txt')
            실행파일 = bytearray(); kōnae_whakawhiti_hononga.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            kōnae_whakawhiti_hononga.storbinary('STOR tārua_uara.elf', io.BytesIO(실행파일)); Ngā_kupu = anga('run tārua_uara.elf'); assert 'CC NATIVE PASS' in Ngā_kupu and 'exit 0' in Ngā_kupu, Ngā_kupu
            kōnae_whakawhiti_hononga.storbinary('STOR kawe_tono', io.BytesIO(실행파일)); Ngā_kupu=anga('./kawe_tono');assert 'CC NATIVE PASS' in Ngā_kupu and 'exit 0' in Ngā_kupu,Ngā_kupu
            kōnae_whakawhiti_hononga.storbinary('STOR Ingoa.txt', io.BytesIO(실행파일)); Ngā_kupu=anga('./Ingoa.txt');assert 'CC NATIVE PASS' in Ngā_kupu and 'exit 0' in Ngā_kupu,Ngā_kupu
            anga('rm kawe_tono Ingoa.txt')
            whakamana_pūrongo['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            anga('rm binary.dat 한글.txt 한글.c 한글.elf tārua_uara.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(mēhua_raraunga/'linux-reference')
            kōnae_whakawhiti_hononga.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Ngā_kupu=anga('./리눅스인사');assert 'exit -8' in Ngā_kupu,Ngā_kupu
            Ngā_kupu=anga('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Ngā_kupu,Ngā_kupu
            assert 'LINUX ELF FILE IO' in anga('cat linux.txt')
            kōnae_whakawhiti_hononga.delete('리눅스인사');kōnae_whakawhiti_hononga.delete('linux.txt')
            kōnae_whakawhiti_hononga.storbinary('STOR FALSE_uara.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in anga('./FALSE_uara.elf');kōnae_whakawhiti_hononga.delete('FALSE_uara.elf')
            whakamana_pūrongo['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = mēhua_raraunga/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket TŪHONO = Reo_Māori.자체.연결통신.TŪHONO("10.0.2.2", Integer.parseInt(args[0]));
 TŪHONO.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] pūtake = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<pūtake.length;i++) if (TŪHONO.getInputStream().read() != (pūtake[i]&255)) throw new RuntimeException("TCP mismatch");
 TŪHONO.close();
 DatagramSocket 종단 = Reo_Māori.자체.통신.Huaki(0); Reo_Māori.자체.통신.KUA_PAU_TE_WĀ(종단, 500);
 Reo_Māori.자체.통신.tuku(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Reo_Māori.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(whakaatu_pūtake/'build/java-library/classes'),'-d',str(mēhua_raraunga),str(통신원문)])
                kōnae_whakawhiti_hononga.storbinary('STOR 바깥통신.class', io.BytesIO((mēhua_raraunga/'바깥통신.class').read_bytes()))
                Ngā_kupu = anga('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_kawe, 되돌림서버항목.UDP_kawe))
                assert 'EXTERNAL TCP UDP PASS' in Ngā_kupu and '10.0.2.2' in Ngā_kupu and 'exit 0' in Ngā_kupu, Ngā_kupu
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            whakamana_pūrongo['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            kōnae_whakawhiti_hononga.delete('바깥통신.class')
            tūmau_pūtake=mēhua_raraunga/'서버시험.java'
            tūmau_pūtake.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket tūmau_uara = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket manuhiri_uara = tūmau_uara.accept();
  manuhiri_uara.getOutputStream().write(manuhiri_uara.getInputStream().read()+1); manuhiri_uara.close(); tūmau_uara.close();
  byte[] Ihirangi_uara = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Ihirangi_uara, Ihirangi_uara.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mēhua_raraunga),str(tūmau_pūtake)])
            kōnae_whakawhiti_hononga.storbinary('STOR 서버시험.class',io.BytesIO((mēhua_raraunga/'서버시험.class').read_bytes()))
            Hātepe.stdin.write('java 서버시험\n'.encode());Hātepe.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',tūmau_roma_kawe),timeout=5) as hoa_uara:
                hoa_uara.sendall(b'A');assert hoa_uara.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as hoa_uara:
                hoa_uara.settimeout(5);hoa_uara.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert hoa_uara.recvfrom(512)[0]==b'UDP-IN'
            Ngā_kupu=수신하기();assert 'INBOUND TCP UDP PASS' in Ngā_kupu and 'exit 0' in Ngā_kupu,Ngā_kupu
            whakamana_pūrongo['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            kōnae_whakawhiti_hononga.delete('서버시험.class')
            tohutohu_SEQUENCE = 'public class 빛 { public static void main(String[] 인수) throws Exception { int SUM_uara = 0; int 수 = 1; while (수 <= 10) { SUM_uara = SUM_uara + 수; 수 = 수 + 1; } Reo_Māori.자체.출력.수쓰기(SUM_uara); Reo_Māori.자체.Kōnae.Tuhia("aot.txt", "한글 AOT Kōnae 😀"); Reo_Māori.자체.출력.tuhi_hononga(Reo_Māori.자체.Kōnae.Pānuitia("aot.txt")); } }'
            kōnae_whakawhiti_hononga.storbinary('STOR 빛.java', io.BytesIO(tohutohu_SEQUENCE.encode()))
            Ngā_kupu = anga('javac 빛.java'); assert 'exit 0' in Ngā_kupu and 'Compiled:' in Ngā_kupu, Ngā_kupu
            Ngā_kupu = anga('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Ngā_kupu and 'exit 0' in Ngā_kupu, Ngā_kupu
            Ngā_kupu = anga('run 빛.elf'); assert '\n55\n' in Ngā_kupu and '한글 AOT Kōnae 😀' in Ngā_kupu and 'exit 0' in Ngā_kupu, Ngā_kupu
            자체실행파일 = bytearray(); kōnae_whakawhiti_hononga.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Ngā_kupu = anga('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Ngā_kupu and 'unsupported' in Ngā_kupu, Ngā_kupu
            보존자료 = bytearray(); kōnae_whakawhiti_hononga.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); kōnae_whakawhiti_hononga.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            kōnae_whakawhiti_hononga.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Ngā_kupu = anga('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Ngā_kupu and 'exit 0' in Ngā_kupu, Ngā_kupu
            Ngā_kupu = anga('run 빛.elf'); assert '\n55\n' in Ngā_kupu and '한글 AOT Kōnae 😀' in Ngā_kupu and 'exit 0' in Ngā_kupu, Ngā_kupu
            whakamana_pūrongo['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            whakamana_pūrongo['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            pateko_pūtake=mēhua_raraunga/'정적시험.java'
            pateko_pūtake.write_text('''public class 정적시험 {
 static int whakaatu_pūtake = 3;
 static int SUM_uara(int n) { return n == 0 ? 0 : n + SUM_uara(n-1); }
 public static void main(String[] 인수) {
  int[] uara = new int[] {whakaatu_pūtake, SUM_uara(10)};
  System.out.println(uara[0] + uara[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mēhua_raraunga),str(pateko_pūtake)])
            kōnae_whakawhiti_hononga.storbinary('STOR 정적시험.class',io.BytesIO((mēhua_raraunga/'정적시험.class').read_bytes()))
            Ngā_kupu=anga('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Ngā_kupu,Ngā_kupu
            Ngā_kupu=anga('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Ngā_kupu,Ngā_kupu
            kōnae_whakawhiti_hononga.delete('정적시험.class');kōnae_whakawhiti_hononga.delete('정적시험.elf')
            whakamana_pūrongo['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Pūranga.getvalue());손상자료[14]^=1
            kōnae_whakawhiti_hononga.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Ngā_kupu=anga('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Ngā_kupu,Ngā_kupu
            whakamana_pūrongo['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            kōnae_whakawhiti_hononga.quit(); assert 'FTP stopped' in anga('ftpd stop')
            assert not arawhata.Pōhēhē, arawhata.Pōhēhē
            whakamana_pūrongo.update(passed=True, frames_to_guest=arawhata.커널수신틀수, frames_from_guest=arawhata.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in pūtīpako.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            arawhata.tatari_hui.set()
            Hātepe.terminate()
            try: Hātepe.wait(timeout=5)
            except subprocess.TimeoutExpired: Hātepe.kill(); Hātepe.wait()
            pūtīpako.close(); Hātepe.stdin.close(); Hātepe.stdout.close()
            whakamana_pūrongo['bridge_error'] = arawhata.Pōhēhē
            whakamana_pūrongo['frames_to_guest'] = arawhata.커널수신틀수; whakamana_pūrongo['frames_from_guest'] = arawhata.커널발신틀수
            (mēhua_raraunga/'packets.json').write_text(json.dumps(arawhata.tapeke_hauroki_LOG,indent=2)+'\n')
            (mēhua_raraunga / 'serial.log').write_bytes(대화기록)
            (mēhua_raraunga / 'report.json').write_text(json.dumps(whakamana_pūrongo, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': whakahaere()
