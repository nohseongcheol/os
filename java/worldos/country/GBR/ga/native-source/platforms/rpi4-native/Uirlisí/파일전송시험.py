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
from Líonra_traschóiritheoir import Líonra_traschóiritheoir
from Rith_ordú import teilgean_fréamh, Ordú
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Rith_2():
    tomhas_sonraí = teilgean_fréamh / 'build/verification/ftp'; tomhas_sonraí.mkdir(parents=True, exist_ok=True)
    bailíochtú_tuairisc = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((teilgean_fréamh / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = tomhas_sonraí / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Argóintí) throws Exception { Gaeilge.자체.Aschur.scríobh_líne("JAR Rith_ordú: " + Argóintí[0]); Gaeilge.자체.Comhad.Scríobh("jar.txt", "자체 eithne_VALUE Comhad"); Gaeilge.자체.Aschur.scríobh_líne(Gaeilge.자체.Comhad.Léigh("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(teilgean_fréamh/'build/java-library/classes'), '-d', str(tomhas_sonraí), str(자바원문)])
    Cartlann = io.BytesIO()
    with zipfile.ZipFile(Cartlann, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(tomhas_sonraí/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); uimhir_phoirt = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); freastalaí_sruth_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Líonra_traschóiritheoir(uimhir_phoirt, ['tcp:{}:9300'.format(freastalaí_sruth_port), 'udp:{}:9301'.format(서버전문접속번호)], taifead=True) as traschóiritheoir:
        Próiseas = subprocess.Popen(Ordú() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + traschóiritheoir.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        roghnóir = selectors.DefaultSelector(); roghnóir.register(Próiseas.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            sonraí = bytearray(); cuir_deireadh_le_OFFSET = time.monotonic() + 시간제한
            while 확인표시 not in sonraí:
                if time.monotonic() > cuir_deireadh_le_OFFSET or Próiseas.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + sonraí.decode('utf-8', 'replace'))
                for 누름값, _ in roghnóir.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: sonraí.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in sonraí or b'FAIL ' in sonraí: raise AssertionError(sonraí)
            return sonraí.decode('utf-8', 'replace').replace('\r\n', '\n')
        def blaosc(Líne):
            Próiseas.stdin.write(Líne.encode() + b'\n'); Próiseas.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in blaosc('ftpd start')
            comhad_traschur_nasc = ftplib.FTP(); comhad_traschur_nasc.encoding = 'utf-8'; comhad_traschur_nasc.connect('127.0.0.1', uimhir_phoirt, timeout=20); comhad_traschur_nasc.login()
            pálasta_sonraí = bytes(range(256)) * 32
            comhad_traschur_nasc.storbinary('STOR binary.dat', io.BytesIO(pálasta_sonraí))
            tomhas = bytearray(); comhad_traschur_nasc.retrbinary('RETR binary.dat', tomhas.extend)
            assert tomhas == pálasta_sonraí; assert comhad_traschur_nasc.size('binary.dat') == len(pálasta_sonraí)
            bailíochtú_tuairisc['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            comhad_traschur_nasc.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in blaosc('cat 한글.txt')
            assert '한글.txt' in comhad_traschur_nasc.nlst()
            assert dict(comhad_traschur_nasc.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            bailíochtú_tuairisc['checks'].append('UTF-8 filename and content visible in guest shell')
            try: comhad_traschur_nasc.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            tomhas = bytearray(); comhad_traschur_nasc.retrbinary('RETR binary.dat', tomhas.extend); assert tomhas == pálasta_sonraí
            bailíochtú_tuairisc['checks'].append('oversized replacement rejected; previous file preserved')
            with comhad_traschur_nasc.transfercmd('STOR pending.txt') as uaslódáil_Comhaid:
                # A control command must not change the active upload's destination.
                assert comhad_traschur_nasc.size('binary.dat') == len(pálasta_sonraí)
                uaslódáil_Comhaid.sendall(b'UPLOAD TARGET PRESERVED')
            assert comhad_traschur_nasc.voidresp().startswith('226')
            tomhas = bytearray(); comhad_traschur_nasc.retrbinary('RETR pending.txt', tomhas.extend)
            assert tomhas == b'UPLOAD TARGET PRESERVED'
            tomhas = bytearray(); comhad_traschur_nasc.retrbinary('RETR binary.dat', tomhas.extend)
            assert tomhas == pálasta_sonraí
            comhad_traschur_nasc.delete('pending.txt')
            bailíochtú_tuairisc['checks'].append('interleaved SIZE cannot change the active STOR destination')
            comhad_traschur_nasc.storbinary('STOR 인사.jar', io.BytesIO(Cartlann.getvalue()))
            Téacs = blaosc('java -jar 인사.jar 누리')
            assert 'JAR Rith_ordú: 누리' in Téacs and '자체 eithne_VALUE Comhad' in Téacs and 'exit 0' in Téacs, Téacs
            Téacs = blaosc('./인사.jar 세상')
            assert 'JAR Rith_ordú: 세상' in Téacs and 'exit 0' in Téacs, Téacs
            bailíochtú_tuairisc['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct sonraí { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct sonraí VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = oscail_comhad("cc.txt", inléite_inscríofa | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; scríobh_comhad_sonraí(문서, 인사, sizeof(인사)-1); dún_comhad(문서); scríobh_comhad_sonraí(1, 인사, sizeof(인사)-1); return 0; }\n'
            comhad_traschur_nasc.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Téacs = blaosc('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Téacs and 'exit 0' in Téacs, Téacs
            Téacs = blaosc('run 한글.elf'); assert 'CC NATIVE PASS' in Téacs and 'exit 0' in Téacs, Téacs
            assert 'CC NATIVE PASS' in blaosc('cat cc.txt')
            실행파일 = bytearray(); comhad_traschur_nasc.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            comhad_traschur_nasc.storbinary('STOR ásc_VALUE.elf', io.BytesIO(실행파일)); Téacs = blaosc('run ásc_VALUE.elf'); assert 'CC NATIVE PASS' in Téacs and 'exit 0' in Téacs, Téacs
            comhad_traschur_nasc.storbinary('STOR Rith_ordú', io.BytesIO(실행파일)); Téacs=blaosc('./Rith_ordú');assert 'CC NATIVE PASS' in Téacs and 'exit 0' in Téacs,Téacs
            comhad_traschur_nasc.storbinary('STOR Ainm.txt', io.BytesIO(실행파일)); Téacs=blaosc('./Ainm.txt');assert 'CC NATIVE PASS' in Téacs and 'exit 0' in Téacs,Téacs
            blaosc('rm Rith_ordú Ainm.txt')
            bailíochtú_tuairisc['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            blaosc('rm binary.dat 한글.txt 한글.c 한글.elf ásc_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(tomhas_sonraí/'linux-reference')
            comhad_traschur_nasc.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Téacs=blaosc('./리눅스인사');assert 'exit -8' in Téacs,Téacs
            Téacs=blaosc('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Téacs,Téacs
            assert 'LINUX ELF FILE IO' in blaosc('cat linux.txt')
            comhad_traschur_nasc.delete('리눅스인사');comhad_traschur_nasc.delete('linux.txt')
            comhad_traschur_nasc.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in blaosc('./FALSE_VALUE.elf');comhad_traschur_nasc.delete('FALSE_VALUE.elf')
            bailíochtú_tuairisc['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = tomhas_sonraí/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Nasc = Gaeilge.자체.연결통신.Nasc("10.0.2.2", Integer.parseInt(args[0]));
 Nasc.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] FOINSE = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<FOINSE.length;i++) if (Nasc.getInputStream().read() != (FOINSE[i]&255)) throw new RuntimeException("TCP mismatch");
 Nasc.close();
 DatagramSocket 종단 = Gaeilge.자체.통신.Oscail(0); Gaeilge.자체.통신.TIMEOUT(종단, 500);
 Gaeilge.자체.통신.seol(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Gaeilge.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(teilgean_fréamh/'build/java-library/classes'),'-d',str(tomhas_sonraí),str(통신원문)])
                comhad_traschur_nasc.storbinary('STOR 바깥통신.class', io.BytesIO((tomhas_sonraí/'바깥통신.class').read_bytes()))
                Téacs = blaosc('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_port, 되돌림서버항목.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in Téacs and '10.0.2.2' in Téacs and 'exit 0' in Téacs, Téacs
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            bailíochtú_tuairisc['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            comhad_traschur_nasc.delete('바깥통신.class')
            freastalaí_foinse=tomhas_sonraí/'서버시험.java'
            freastalaí_foinse.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket freastalaí_VALUE = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket aoi_VALUE = freastalaí_VALUE.accept();
  aoi_VALUE.getOutputStream().write(aoi_VALUE.getInputStream().read()+1); aoi_VALUE.close(); freastalaí_VALUE.close();
  byte[] Inneachar_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Inneachar_VALUE, Inneachar_VALUE.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(tomhas_sonraí),str(freastalaí_foinse)])
            comhad_traschur_nasc.storbinary('STOR 서버시험.class',io.BytesIO((tomhas_sonraí/'서버시험.class').read_bytes()))
            Próiseas.stdin.write('java 서버시험\n'.encode());Próiseas.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',freastalaí_sruth_port),timeout=5) as piara_VALUE:
                piara_VALUE.sendall(b'A');assert piara_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as piara_VALUE:
                piara_VALUE.settimeout(5);piara_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert piara_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Téacs=수신하기();assert 'INBOUND TCP UDP PASS' in Téacs and 'exit 0' in Téacs,Téacs
            bailíochtú_tuairisc['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            comhad_traschur_nasc.delete('서버시험.class')
            treoir_SEQUENCE = 'public class 빛 { public static void main(String[] Argóintí) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } Gaeilge.자체.Aschur.수쓰기(SUM_VALUE); Gaeilge.자체.Comhad.Scríobh("aot.txt", "한글 AOT Comhad 😀"); Gaeilge.자체.Aschur.scríobh_líne(Gaeilge.자체.Comhad.Léigh("aot.txt")); } }'
            comhad_traschur_nasc.storbinary('STOR 빛.java', io.BytesIO(treoir_SEQUENCE.encode()))
            Téacs = blaosc('javac 빛.java'); assert 'exit 0' in Téacs and 'Compiled:' in Téacs, Téacs
            Téacs = blaosc('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Téacs and 'exit 0' in Téacs, Téacs
            Téacs = blaosc('run 빛.elf'); assert '\n55\n' in Téacs and '한글 AOT Comhad 😀' in Téacs and 'exit 0' in Téacs, Téacs
            자체실행파일 = bytearray(); comhad_traschur_nasc.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Téacs = blaosc('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Téacs and 'unsupported' in Téacs, Téacs
            보존자료 = bytearray(); comhad_traschur_nasc.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); comhad_traschur_nasc.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            comhad_traschur_nasc.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Téacs = blaosc('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Téacs and 'exit 0' in Téacs, Téacs
            Téacs = blaosc('run 빛.elf'); assert '\n55\n' in Téacs and '한글 AOT Comhad 😀' in Téacs and 'exit 0' in Téacs, Téacs
            bailíochtú_tuairisc['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            bailíochtú_tuairisc['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statach_foinse=tomhas_sonraí/'정적시험.java'
            statach_foinse.write_text('''public class 정적시험 {
 static int teilgean_fréamh = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] Argóintí) {
  int[] VALUE = new int[] {teilgean_fréamh, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(Argóintí[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(tomhas_sonraí),str(statach_foinse)])
            comhad_traschur_nasc.storbinary('STOR 정적시험.class',io.BytesIO((tomhas_sonraí/'정적시험.class').read_bytes()))
            Téacs=blaosc('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Téacs,Téacs
            Téacs=blaosc('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Téacs,Téacs
            comhad_traschur_nasc.delete('정적시험.class');comhad_traschur_nasc.delete('정적시험.elf')
            bailíochtú_tuairisc['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Cartlann.getvalue());손상자료[14]^=1
            comhad_traschur_nasc.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Téacs=blaosc('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Téacs,Téacs
            bailíochtú_tuairisc['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            comhad_traschur_nasc.quit(); assert 'FTP stopped' in blaosc('ftpd stop')
            assert not traschóiritheoir.ERREÁID, traschóiritheoir.ERREÁID
            bailíochtú_tuairisc.update(passed=True, frames_to_guest=traschóiritheoir.커널수신틀수, frames_from_guest=traschóiritheoir.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in roghnóir.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            traschóiritheoir.cuir_ar_shos_ócáid.set()
            Próiseas.terminate()
            try: Próiseas.wait(timeout=5)
            except subprocess.TimeoutExpired: Próiseas.kill(); Próiseas.wait()
            roghnóir.close(); Próiseas.stdin.close(); Próiseas.stdout.close()
            bailíochtú_tuairisc['bridge_error'] = traschóiritheoir.ERREÁID
            bailíochtú_tuairisc['frames_to_guest'] = traschóiritheoir.커널수신틀수; bailíochtú_tuairisc['frames_from_guest'] = traschóiritheoir.커널발신틀수
            (tomhas_sonraí/'packets.json').write_text(json.dumps(traschóiritheoir.rian_LOG,indent=2)+'\n')
            (tomhas_sonraí / 'serial.log').write_bytes(대화기록)
            (tomhas_sonraí / 'report.json').write_text(json.dumps(bailíochtú_tuairisc, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Rith_2()
