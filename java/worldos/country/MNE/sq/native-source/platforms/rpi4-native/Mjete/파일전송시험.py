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
from rrjet_urë import rrjet_urë
from zbatoj_komandë import Project_rrënjë, Komanda
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Ekzekuto():
    llogaritje_të_dhëna = Project_rrënjë / 'build/verification/ftp'; llogaritje_të_dhëna.mkdir(parents=True, exist_ok=True)
    miratim_raport = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Project_rrënjë / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = llogaritje_të_dhëna / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Argumente) throws Exception { 한국어.자체.출력.shkruaj_linjë("JAR zbatoj_komandë: " + Argumente[0]); 한국어.자체.Kartelë.Shkrimi("jar.txt", "자체 bërthamë_VALUE Kartelë"); 한국어.자체.출력.shkruaj_linjë(한국어.자체.Kartelë.Leximi("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_rrënjë/'build/java-library/classes'), '-d', str(llogaritje_të_dhëna), str(자바원문)])
    arkiv = io.BytesIO()
    with zipfile.ZipFile(arkiv, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(llogaritje_të_dhëna/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); numri_i_portës = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_Stream_portë = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with rrjet_urë(numri_i_portës, ['tcp:{}:9300'.format(server_Stream_portë), 'udp:{}:9301'.format(서버전문접속번호)], kap=True) as urë:
        Proçes = subprocess.Popen(Komanda() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + urë.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        përzgjedhësi = selectors.DefaultSelector(); përzgjedhësi.register(Proçes.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            të_dhëna = bytearray(); mbaroj_OFFSET = time.monotonic() + 시간제한
            while 확인표시 not in të_dhëna:
                if time.monotonic() > mbaroj_OFFSET or Proçes.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + të_dhëna.decode('utf-8', 'replace'))
                for 누름값, _ in përzgjedhësi.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: të_dhëna.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in të_dhëna or b'FAIL ' in të_dhëna: raise AssertionError(të_dhëna)
            return të_dhëna.decode('utf-8', 'replace').replace('\r\n', '\n')
        def pasues(linjë):
            Proçes.stdin.write(linjë.encode() + b'\n'); Proçes.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in pasues('ftpd start')
            skedar_transferim_lidhje = ftplib.FTP(); skedar_transferim_lidhje.encoding = 'utf-8'; skedar_transferim_lidhje.connect('127.0.0.1', numri_i_portës, timeout=20); skedar_transferim_lidhje.login()
            ngarkesë_e_dobishme_të_dhëna = bytes(range(256)) * 32
            skedar_transferim_lidhje.storbinary('STOR binary.dat', io.BytesIO(ngarkesë_e_dobishme_të_dhëna))
            llogaritje = bytearray(); skedar_transferim_lidhje.retrbinary('RETR binary.dat', llogaritje.extend)
            assert llogaritje == ngarkesë_e_dobishme_të_dhëna; assert skedar_transferim_lidhje.size('binary.dat') == len(ngarkesë_e_dobishme_të_dhëna)
            miratim_raport['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            skedar_transferim_lidhje.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in pasues('cat 한글.txt')
            assert '한글.txt' in skedar_transferim_lidhje.nlst()
            assert dict(skedar_transferim_lidhje.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            miratim_raport['checks'].append('UTF-8 filename and content visible in guest shell')
            try: skedar_transferim_lidhje.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            llogaritje = bytearray(); skedar_transferim_lidhje.retrbinary('RETR binary.dat', llogaritje.extend); assert llogaritje == ngarkesë_e_dobishme_të_dhëna
            miratim_raport['checks'].append('oversized replacement rejected; previous file preserved')
            with skedar_transferim_lidhje.transfercmd('STOR pending.txt') as Ngarkim_Skedarët:
                # A control command must not change the active upload's destination.
                assert skedar_transferim_lidhje.size('binary.dat') == len(ngarkesë_e_dobishme_të_dhëna)
                Ngarkim_Skedarët.sendall(b'UPLOAD TARGET PRESERVED')
            assert skedar_transferim_lidhje.voidresp().startswith('226')
            llogaritje = bytearray(); skedar_transferim_lidhje.retrbinary('RETR pending.txt', llogaritje.extend)
            assert llogaritje == b'UPLOAD TARGET PRESERVED'
            llogaritje = bytearray(); skedar_transferim_lidhje.retrbinary('RETR binary.dat', llogaritje.extend)
            assert llogaritje == ngarkesë_e_dobishme_të_dhëna
            skedar_transferim_lidhje.delete('pending.txt')
            miratim_raport['checks'].append('interleaved SIZE cannot change the active STOR destination')
            skedar_transferim_lidhje.storbinary('STOR 인사.jar', io.BytesIO(arkiv.getvalue()))
            Teksti = pasues('java -jar 인사.jar 누리')
            assert 'JAR zbatoj_komandë: 누리' in Teksti and '자체 bërthamë_VALUE Kartelë' in Teksti and 'exit 0' in Teksti, Teksti
            Teksti = pasues('./인사.jar 세상')
            assert 'JAR zbatoj_komandë: 세상' in Teksti and 'exit 0' in Teksti, Teksti
            miratim_raport['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct të_dhëna { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct të_dhëna VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = hap_skedar("cc.txt", lexoj_shkruaj | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; shkruaj_skedar_të_dhëna(문서, 인사, sizeof(인사)-1); mbyll_skedar(문서); shkruaj_skedar_të_dhëna(1, 인사, sizeof(인사)-1); return 0; }\n'
            skedar_transferim_lidhje.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Teksti = pasues('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Teksti and 'exit 0' in Teksti, Teksti
            Teksti = pasues('run 한글.elf'); assert 'CC NATIVE PASS' in Teksti and 'exit 0' in Teksti, Teksti
            assert 'CC NATIVE PASS' in pasues('cat cc.txt')
            실행파일 = bytearray(); skedar_transferim_lidhje.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            skedar_transferim_lidhje.storbinary('STOR kopjoj_VALUE.elf', io.BytesIO(실행파일)); Teksti = pasues('run kopjoj_VALUE.elf'); assert 'CC NATIVE PASS' in Teksti and 'exit 0' in Teksti, Teksti
            skedar_transferim_lidhje.storbinary('STOR zbatoj_komandë', io.BytesIO(실행파일)); Teksti=pasues('./zbatoj_komandë');assert 'CC NATIVE PASS' in Teksti and 'exit 0' in Teksti,Teksti
            skedar_transferim_lidhje.storbinary('STOR Emër.txt', io.BytesIO(실행파일)); Teksti=pasues('./Emër.txt');assert 'CC NATIVE PASS' in Teksti and 'exit 0' in Teksti,Teksti
            pasues('rm zbatoj_komandë Emër.txt')
            miratim_raport['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            pasues('rm binary.dat 한글.txt 한글.c 한글.elf kopjoj_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(llogaritje_të_dhëna/'linux-reference')
            skedar_transferim_lidhje.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Teksti=pasues('./리눅스인사');assert 'exit -8' in Teksti,Teksti
            Teksti=pasues('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Teksti,Teksti
            assert 'LINUX ELF FILE IO' in pasues('cat linux.txt')
            skedar_transferim_lidhje.delete('리눅스인사');skedar_transferim_lidhje.delete('linux.txt')
            skedar_transferim_lidhje.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in pasues('./FALSE_VALUE.elf');skedar_transferim_lidhje.delete('FALSE_VALUE.elf')
            miratim_raport['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = llogaritje_të_dhëna/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Lidhu = 한국어.자체.연결통신.Lidhu("10.0.2.2", Integer.parseInt(args[0]));
 Lidhu.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] BURIMI = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<BURIMI.length;i++) if (Lidhu.getInputStream().read() != (BURIMI[i]&255)) throw new RuntimeException("TCP mismatch");
 Lidhu.close();
 DatagramSocket 종단 = 한국어.자체.통신.Hap(0); 한국어.자체.통신.TIMEOUT(종단, 500);
 한국어.자체.통신.dërgoj(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_rrënjë/'build/java-library/classes'),'-d',str(llogaritje_të_dhëna),str(통신원문)])
                skedar_transferim_lidhje.storbinary('STOR 바깥통신.class', io.BytesIO((llogaritje_të_dhëna/'바깥통신.class').read_bytes()))
                Teksti = pasues('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_portë, 되돌림서버항목.UDP_portë))
                assert 'EXTERNAL TCP UDP PASS' in Teksti and '10.0.2.2' in Teksti and 'exit 0' in Teksti, Teksti
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            miratim_raport['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            skedar_transferim_lidhje.delete('바깥통신.class')
            server_burim=llogaritje_të_dhëna/'서버시험.java'
            server_burim.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket i_ftuar_VALUE = server_VALUE.accept();
  i_ftuar_VALUE.getOutputStream().write(i_ftuar_VALUE.getInputStream().read()+1); i_ftuar_VALUE.close(); server_VALUE.close();
  byte[] Përmbajtje_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Përmbajtje_VALUE, Përmbajtje_VALUE.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(llogaritje_të_dhëna),str(server_burim)])
            skedar_transferim_lidhje.storbinary('STOR 서버시험.class',io.BytesIO((llogaritje_të_dhëna/'서버시험.class').read_bytes()))
            Proçes.stdin.write('java 서버시험\n'.encode());Proçes.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_Stream_portë),timeout=5) as homolog_VALUE:
                homolog_VALUE.sendall(b'A');assert homolog_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as homolog_VALUE:
                homolog_VALUE.settimeout(5);homolog_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert homolog_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Teksti=수신하기();assert 'INBOUND TCP UDP PASS' in Teksti and 'exit 0' in Teksti,Teksti
            miratim_raport['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            skedar_transferim_lidhje.delete('서버시험.class')
            instruksion_SEQUENCE = 'public class 빛 { public static void main(String[] Argumente) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(SUM_VALUE); 한국어.자체.Kartelë.Shkrimi("aot.txt", "한글 AOT Kartelë 😀"); 한국어.자체.출력.shkruaj_linjë(한국어.자체.Kartelë.Leximi("aot.txt")); } }'
            skedar_transferim_lidhje.storbinary('STOR 빛.java', io.BytesIO(instruksion_SEQUENCE.encode()))
            Teksti = pasues('javac 빛.java'); assert 'exit 0' in Teksti and 'Compiled:' in Teksti, Teksti
            Teksti = pasues('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Teksti and 'exit 0' in Teksti, Teksti
            Teksti = pasues('run 빛.elf'); assert '\n55\n' in Teksti and '한글 AOT Kartelë 😀' in Teksti and 'exit 0' in Teksti, Teksti
            자체실행파일 = bytearray(); skedar_transferim_lidhje.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Teksti = pasues('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Teksti and 'unsupported' in Teksti, Teksti
            보존자료 = bytearray(); skedar_transferim_lidhje.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); skedar_transferim_lidhje.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            skedar_transferim_lidhje.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Teksti = pasues('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Teksti and 'exit 0' in Teksti, Teksti
            Teksti = pasues('run 빛.elf'); assert '\n55\n' in Teksti and '한글 AOT Kartelë 😀' in Teksti and 'exit 0' in Teksti, Teksti
            miratim_raport['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            miratim_raport['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statik_burim=llogaritje_të_dhëna/'정적시험.java'
            statik_burim.write_text('''public class 정적시험 {
 static int Project_rrënjë = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] Argumente) {
  int[] VALUE = new int[] {Project_rrënjë, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(Argumente[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(llogaritje_të_dhëna),str(statik_burim)])
            skedar_transferim_lidhje.storbinary('STOR 정적시험.class',io.BytesIO((llogaritje_të_dhëna/'정적시험.class').read_bytes()))
            Teksti=pasues('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Teksti,Teksti
            Teksti=pasues('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Teksti,Teksti
            skedar_transferim_lidhje.delete('정적시험.class');skedar_transferim_lidhje.delete('정적시험.elf')
            miratim_raport['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(arkiv.getvalue());손상자료[14]^=1
            skedar_transferim_lidhje.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Teksti=pasues('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Teksti,Teksti
            miratim_raport['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            skedar_transferim_lidhje.quit(); assert 'FTP stopped' in pasues('ftpd stop')
            assert not urë.GABIM, urë.GABIM
            miratim_raport.update(passed=True, frames_to_guest=urë.커널수신틀수, frames_from_guest=urë.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in përzgjedhësi.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            urë.pezulloj_ngjarje.set()
            Proçes.terminate()
            try: Proçes.wait(timeout=5)
            except subprocess.TimeoutExpired: Proçes.kill(); Proçes.wait()
            përzgjedhësi.close(); Proçes.stdin.close(); Proçes.stdout.close()
            miratim_raport['bridge_error'] = urë.GABIM
            miratim_raport['frames_to_guest'] = urë.커널수신틀수; miratim_raport['frames_from_guest'] = urë.커널발신틀수
            (llogaritje_të_dhëna/'packets.json').write_text(json.dumps(urë.gjurmë_LOG,indent=2)+'\n')
            (llogaritje_të_dhëna / 'serial.log').write_bytes(대화기록)
            (llogaritje_të_dhëna / 'report.json').write_text(json.dumps(miratim_raport, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Ekzekuto()
