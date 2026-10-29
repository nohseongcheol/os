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
from lìonra_drochaid import lìonra_drochaid
from gnìomhaich_àithne import tilg_freumh, àithne
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def ruith():
    tomhas_dàta = tilg_freumh / 'build/verification/ftp'; tomhas_dàta.mkdir(parents=True, exist_ok=True)
    dearbhadh_aithisg = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((tilg_freumh / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = tomhas_dàta / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.sgrìobh_loidhne("JAR gnìomhaich_àithne: " + 인수[0]); 한국어.자체.faidhle.sgrìobh("jar.txt", "자체 eitean_VALUE faidhle"); 한국어.자체.출력.sgrìobh_loidhne(한국어.자체.faidhle.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(tilg_freumh/'build/java-library/classes'), '-d', str(tomhas_dàta), str(자바원문)])
    taisg = io.BytesIO()
    with zipfile.ZipFile(taisg, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(tomhas_dàta/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); frithealaiche_sruth_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with lìonra_drochaid(접속번호, ['tcp:{}:9300'.format(frithealaiche_sruth_port), 'udp:{}:9301'.format(서버전문접속번호)], glac=True) as drochaid:
        Pròiseas = subprocess.Popen(àithne() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + drochaid.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        roghnaichear = selectors.DefaultSelector(); roghnaichear.register(Pròiseas.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            dàta = bytearray(); crìochnaich_OFFSET = time.monotonic() + 시간제한
            while 확인표시 not in dàta:
                if time.monotonic() > crìochnaich_OFFSET or Pròiseas.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + dàta.decode('utf-8', 'replace'))
                for 누름값, _ in roghnaichear.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: dàta.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in dàta or b'FAIL ' in dàta: raise AssertionError(dàta)
            return dàta.decode('utf-8', 'replace').replace('\r\n', '\n')
        def slige(loidhne):
            Pròiseas.stdin.write(loidhne.encode() + b'\n'); Pròiseas.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in slige('ftpd start')
            faidhle_tar_chur_ceangal = ftplib.FTP(); faidhle_tar_chur_ceangal.encoding = 'utf-8'; faidhle_tar_chur_ceangal.connect('127.0.0.1', 접속번호, timeout=20); faidhle_tar_chur_ceangal.login()
            payload_dàta = bytes(range(256)) * 32
            faidhle_tar_chur_ceangal.storbinary('STOR binary.dat', io.BytesIO(payload_dàta))
            tomhas = bytearray(); faidhle_tar_chur_ceangal.retrbinary('RETR binary.dat', tomhas.extend)
            assert tomhas == payload_dàta; assert faidhle_tar_chur_ceangal.size('binary.dat') == len(payload_dàta)
            dearbhadh_aithisg['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            faidhle_tar_chur_ceangal.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in slige('cat 한글.txt')
            assert '한글.txt' in faidhle_tar_chur_ceangal.nlst()
            assert dict(faidhle_tar_chur_ceangal.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            dearbhadh_aithisg['checks'].append('UTF-8 filename and content visible in guest shell')
            try: faidhle_tar_chur_ceangal.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            tomhas = bytearray(); faidhle_tar_chur_ceangal.retrbinary('RETR binary.dat', tomhas.extend); assert tomhas == payload_dàta
            dearbhadh_aithisg['checks'].append('oversized replacement rejected; previous file preserved')
            with faidhle_tar_chur_ceangal.transfercmd('STOR pending.txt') as luchdaich_suas_faidhlichean:
                # A control command must not change the active upload's destination.
                assert faidhle_tar_chur_ceangal.size('binary.dat') == len(payload_dàta)
                luchdaich_suas_faidhlichean.sendall(b'UPLOAD TARGET PRESERVED')
            assert faidhle_tar_chur_ceangal.voidresp().startswith('226')
            tomhas = bytearray(); faidhle_tar_chur_ceangal.retrbinary('RETR pending.txt', tomhas.extend)
            assert tomhas == b'UPLOAD TARGET PRESERVED'
            tomhas = bytearray(); faidhle_tar_chur_ceangal.retrbinary('RETR binary.dat', tomhas.extend)
            assert tomhas == payload_dàta
            faidhle_tar_chur_ceangal.delete('pending.txt')
            dearbhadh_aithisg['checks'].append('interleaved SIZE cannot change the active STOR destination')
            faidhle_tar_chur_ceangal.storbinary('STOR 인사.jar', io.BytesIO(taisg.getvalue()))
            SMS = slige('java -jar 인사.jar 누리')
            assert 'JAR gnìomhaich_àithne: 누리' in SMS and '자체 eitean_VALUE faidhle' in SMS and 'exit 0' in SMS, SMS
            SMS = slige('./인사.jar 세상')
            assert 'JAR gnìomhaich_àithne: 세상' in SMS and 'exit 0' in SMS, SMS
            dearbhadh_aithisg['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct dàta { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct dàta VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = fosgail_faidhle("cc.txt", so_leughte_so_sgrìobhte | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; sgrìobh_faidhle_dàta(문서, 인사, sizeof(인사)-1); dùin_faidhle(문서); sgrìobh_faidhle_dàta(1, 인사, sizeof(인사)-1); return 0; }\n'
            faidhle_tar_chur_ceangal.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            SMS = slige('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = slige('run 한글.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            assert 'CC NATIVE PASS' in slige('cat cc.txt')
            실행파일 = bytearray(); faidhle_tar_chur_ceangal.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            faidhle_tar_chur_ceangal.storbinary('STOR ionstans_VALUE.elf', io.BytesIO(실행파일)); SMS = slige('run ionstans_VALUE.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            faidhle_tar_chur_ceangal.storbinary('STOR gnìomhaich_àithne', io.BytesIO(실행파일)); SMS=slige('./gnìomhaich_àithne');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            faidhle_tar_chur_ceangal.storbinary('STOR Ainm.txt', io.BytesIO(실행파일)); SMS=slige('./Ainm.txt');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            slige('rm gnìomhaich_àithne Ainm.txt')
            dearbhadh_aithisg['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            slige('rm binary.dat 한글.txt 한글.c 한글.elf ionstans_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(tomhas_dàta/'linux-reference')
            faidhle_tar_chur_ceangal.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            SMS=slige('./리눅스인사');assert 'exit -8' in SMS,SMS
            SMS=slige('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in SMS,SMS
            assert 'LINUX ELF FILE IO' in slige('cat linux.txt')
            faidhle_tar_chur_ceangal.delete('리눅스인사');faidhle_tar_chur_ceangal.delete('linux.txt')
            faidhle_tar_chur_ceangal.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in slige('./FALSE_VALUE.elf');faidhle_tar_chur_ceangal.delete('FALSE_VALUE.elf')
            dearbhadh_aithisg['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = tomhas_dàta/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket CONNECT = 한국어.자체.연결통신.CONNECT("10.0.2.2", Integer.parseInt(args[0]));
 CONNECT.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] tùs = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<tùs.length;i++) if (CONNECT.getInputStream().read() != (tùs[i]&255)) throw new RuntimeException("TCP mismatch");
 CONNECT.close();
 DatagramSocket 종단 = 한국어.자체.통신.fosgail(0); 한국어.자체.통신.TIMEOUT(종단, 500);
 한국어.자체.통신.cuir(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(tilg_freumh/'build/java-library/classes'),'-d',str(tomhas_dàta),str(통신원문)])
                faidhle_tar_chur_ceangal.storbinary('STOR 바깥통신.class', io.BytesIO((tomhas_dàta/'바깥통신.class').read_bytes()))
                SMS = slige('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_port, 되돌림서버항목.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in SMS and '10.0.2.2' in SMS and 'exit 0' in SMS, SMS
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            dearbhadh_aithisg['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            faidhle_tar_chur_ceangal.delete('바깥통신.class')
            frithealaiche_tùs=tomhas_dàta/'서버시험.java'
            frithealaiche_tùs.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket frithealaiche_VALUE = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket aoigh_VALUE = frithealaiche_VALUE.accept();
  aoigh_VALUE.getOutputStream().write(aoigh_VALUE.getInputStream().read()+1); aoigh_VALUE.close(); frithealaiche_VALUE.close();
  byte[] susbaint_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(susbaint_VALUE, susbaint_VALUE.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(tomhas_dàta),str(frithealaiche_tùs)])
            faidhle_tar_chur_ceangal.storbinary('STOR 서버시험.class',io.BytesIO((tomhas_dàta/'서버시험.class').read_bytes()))
            Pròiseas.stdin.write('java 서버시험\n'.encode());Pròiseas.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',frithealaiche_sruth_port),timeout=5) as seise_VALUE:
                seise_VALUE.sendall(b'A');assert seise_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as seise_VALUE:
                seise_VALUE.settimeout(5);seise_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert seise_VALUE.recvfrom(512)[0]==b'UDP-IN'
            SMS=수신하기();assert 'INBOUND TCP UDP PASS' in SMS and 'exit 0' in SMS,SMS
            dearbhadh_aithisg['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            faidhle_tar_chur_ceangal.delete('서버시험.class')
            treòrachadh_SEQUENCE = 'public class 빛 { public static void main(String[] 인수) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(SUM_VALUE); 한국어.자체.faidhle.sgrìobh("aot.txt", "한글 AOT faidhle 😀"); 한국어.자체.출력.sgrìobh_loidhne(한국어.자체.faidhle.읽기("aot.txt")); } }'
            faidhle_tar_chur_ceangal.storbinary('STOR 빛.java', io.BytesIO(treòrachadh_SEQUENCE.encode()))
            SMS = slige('javac 빛.java'); assert 'exit 0' in SMS and 'Compiled:' in SMS, SMS
            SMS = slige('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = slige('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT faidhle 😀' in SMS and 'exit 0' in SMS, SMS
            자체실행파일 = bytearray(); faidhle_tar_chur_ceangal.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            SMS = slige('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in SMS and 'unsupported' in SMS, SMS
            보존자료 = bytearray(); faidhle_tar_chur_ceangal.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); faidhle_tar_chur_ceangal.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            faidhle_tar_chur_ceangal.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            SMS = slige('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = slige('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT faidhle 😀' in SMS and 'exit 0' in SMS, SMS
            dearbhadh_aithisg['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            dearbhadh_aithisg['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            stadaigeach_tùs=tomhas_dàta/'정적시험.java'
            stadaigeach_tùs.write_text('''public class 정적시험 {
 static int tilg_freumh = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] 인수) {
  int[] VALUE = new int[] {tilg_freumh, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(tomhas_dàta),str(stadaigeach_tùs)])
            faidhle_tar_chur_ceangal.storbinary('STOR 정적시험.class',io.BytesIO((tomhas_dàta/'정적시험.class').read_bytes()))
            SMS=slige('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in SMS,SMS
            SMS=slige('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in SMS,SMS
            faidhle_tar_chur_ceangal.delete('정적시험.class');faidhle_tar_chur_ceangal.delete('정적시험.elf')
            dearbhadh_aithisg['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(taisg.getvalue());손상자료[14]^=1
            faidhle_tar_chur_ceangal.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            SMS=slige('java -jar 인사.jar');assert 'Main-Class\nexit 1' in SMS,SMS
            dearbhadh_aithisg['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            faidhle_tar_chur_ceangal.quit(); assert 'FTP stopped' in slige('ftpd stop')
            assert not drochaid.Mearachd, drochaid.Mearachd
            dearbhadh_aithisg.update(passed=True, frames_to_guest=drochaid.커널수신틀수, frames_from_guest=drochaid.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in roghnaichear.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            drochaid.cuir_na_stad_tachartas.set()
            Pròiseas.terminate()
            try: Pròiseas.wait(timeout=5)
            except subprocess.TimeoutExpired: Pròiseas.kill(); Pròiseas.wait()
            roghnaichear.close(); Pròiseas.stdin.close(); Pròiseas.stdout.close()
            dearbhadh_aithisg['bridge_error'] = drochaid.Mearachd
            dearbhadh_aithisg['frames_to_guest'] = drochaid.커널수신틀수; dearbhadh_aithisg['frames_from_guest'] = drochaid.커널발신틀수
            (tomhas_dàta/'packets.json').write_text(json.dumps(drochaid.treus_LOG,indent=2)+'\n')
            (tomhas_dàta / 'serial.log').write_bytes(대화기록)
            (tomhas_dàta / 'report.json').write_text(json.dumps(dearbhadh_aithisg, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ruith()
