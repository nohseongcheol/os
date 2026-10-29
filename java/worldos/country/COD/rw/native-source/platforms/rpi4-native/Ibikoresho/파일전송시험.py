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
from gukora_ibwiriza import 기준, Icyo_wifuza
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def ihuriro():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    iyemeza_raporo = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { Ikinyarwanda.자체.출력.kwandika_umurongo("JAR gukora_ibwiriza: " + 인수[0]); Ikinyarwanda.자체.Idosiye.kwandika("jar.txt", "자체 intima_agaciro Idosiye"); Ikinyarwanda.자체.출력.kwandika_umurongo(Ikinyarwanda.자체.Idosiye.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    gushyingura = io.BytesIO()
    with zipfile.ZipFile(gushyingura, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); seriveri_Stream_poti = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(접속번호, ['tcp:{}:9300'.format(seriveri_Stream_poti), 'udp:{}:9301'.format(서버전문접속번호)], ishusho_ba7b8054=True) as 연결다리:
        Inzira_a7054519 = subprocess.Popen(Icyo_wifuza() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        muhitamo = selectors.DefaultSelector(); muhitamo.register(Inzira_a7054519.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            amakurushingiro = bytearray(); kurangiza_Ofuseti = time.monotonic() + 시간제한
            while 확인표시 not in amakurushingiro:
                if time.monotonic() > kurangiza_Ofuseti or Inzira_a7054519.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + amakurushingiro.decode('utf-8', 'replace'))
                for 누름값, _ in muhitamo.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: amakurushingiro.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in amakurushingiro or b'FAIL ' in amakurushingiro: raise AssertionError(amakurushingiro)
            return amakurushingiro.decode('utf-8', 'replace').replace('\r\n', '\n')
        def insomamabwiriza(umurongo):
            Inzira_a7054519.stdin.write(umurongo.encode() + b'\n'); Inzira_a7054519.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in insomamabwiriza('ftpd start')
            dosiye_iyimura_kwihuza = ftplib.FTP(); dosiye_iyimura_kwihuza.encoding = 'utf-8'; dosiye_iyimura_kwihuza.connect('127.0.0.1', 접속번호, timeout=20); dosiye_iyimura_kwihuza.login()
            ibitwarwa_amakurushingiro = bytes(range(256)) * 32
            dosiye_iyimura_kwihuza.storbinary('STOR binary.dat', io.BytesIO(ibitwarwa_amakurushingiro))
            결과 = bytearray(); dosiye_iyimura_kwihuza.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ibitwarwa_amakurushingiro; assert dosiye_iyimura_kwihuza.size('binary.dat') == len(ibitwarwa_amakurushingiro)
            iyemeza_raporo['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            dosiye_iyimura_kwihuza.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in insomamabwiriza('cat 한글.txt')
            assert '한글.txt' in dosiye_iyimura_kwihuza.nlst()
            assert dict(dosiye_iyimura_kwihuza.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            iyemeza_raporo['checks'].append('UTF-8 filename and content visible in guest shell')
            try: dosiye_iyimura_kwihuza.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); dosiye_iyimura_kwihuza.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == ibitwarwa_amakurushingiro
            iyemeza_raporo['checks'].append('oversized replacement rejected; previous file preserved')
            with dosiye_iyimura_kwihuza.transfercmd('STOR pending.txt') as gukurura_Dosiye:
                # A control command must not change the active upload's destination.
                assert dosiye_iyimura_kwihuza.size('binary.dat') == len(ibitwarwa_amakurushingiro)
                gukurura_Dosiye.sendall(b'UPLOAD TARGET PRESERVED')
            assert dosiye_iyimura_kwihuza.voidresp().startswith('226')
            결과 = bytearray(); dosiye_iyimura_kwihuza.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); dosiye_iyimura_kwihuza.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ibitwarwa_amakurushingiro
            dosiye_iyimura_kwihuza.delete('pending.txt')
            iyemeza_raporo['checks'].append('interleaved SIZE cannot change the active STOR destination')
            dosiye_iyimura_kwihuza.storbinary('STOR 인사.jar', io.BytesIO(gushyingura.getvalue()))
            Umwandiko = insomamabwiriza('java -jar 인사.jar 누리')
            assert 'JAR gukora_ibwiriza: 누리' in Umwandiko and '자체 intima_agaciro Idosiye' in Umwandiko and 'exit 0' in Umwandiko, Umwandiko
            Umwandiko = insomamabwiriza('./인사.jar 세상')
            assert 'JAR gukora_ibwiriza: 세상' in Umwandiko and 'exit 0' in Umwandiko, Umwandiko
            iyemeza_raporo['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct amakurushingiro { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct amakurushingiro agaciro = {합(10), 1.25}; if (agaciro.수 != 55 || agaciro.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = kurema_dosiye("cc.txt", gusoma_kwandika | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; kwandika_dosiye_amakurushingiro(문서, 인사, sizeof(인사)-1); gufunga_dosiye(문서); kwandika_dosiye_amakurushingiro(1, 인사, sizeof(인사)-1); return 0; }\n'
            dosiye_iyimura_kwihuza.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Umwandiko = insomamabwiriza('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Umwandiko and 'exit 0' in Umwandiko, Umwandiko
            Umwandiko = insomamabwiriza('run 한글.elf'); assert 'CC NATIVE PASS' in Umwandiko and 'exit 0' in Umwandiko, Umwandiko
            assert 'CC NATIVE PASS' in insomamabwiriza('cat cc.txt')
            실행파일 = bytearray(); dosiye_iyimura_kwihuza.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            dosiye_iyimura_kwihuza.storbinary('STOR kopi_agaciro.elf', io.BytesIO(실행파일)); Umwandiko = insomamabwiriza('run kopi_agaciro.elf'); assert 'CC NATIVE PASS' in Umwandiko and 'exit 0' in Umwandiko, Umwandiko
            dosiye_iyimura_kwihuza.storbinary('STOR gukora_ibwiriza', io.BytesIO(실행파일)); Umwandiko=insomamabwiriza('./gukora_ibwiriza');assert 'CC NATIVE PASS' in Umwandiko and 'exit 0' in Umwandiko,Umwandiko
            dosiye_iyimura_kwihuza.storbinary('STOR Izina.txt', io.BytesIO(실행파일)); Umwandiko=insomamabwiriza('./Izina.txt');assert 'CC NATIVE PASS' in Umwandiko and 'exit 0' in Umwandiko,Umwandiko
            insomamabwiriza('rm gukora_ibwiriza Izina.txt')
            iyemeza_raporo['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            insomamabwiriza('rm binary.dat 한글.txt 한글.c 한글.elf kopi_agaciro.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            dosiye_iyimura_kwihuza.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Umwandiko=insomamabwiriza('./리눅스인사');assert 'exit -8' in Umwandiko,Umwandiko
            Umwandiko=insomamabwiriza('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Umwandiko,Umwandiko
            assert 'LINUX ELF FILE IO' in insomamabwiriza('cat linux.txt')
            dosiye_iyimura_kwihuza.delete('리눅스인사');dosiye_iyimura_kwihuza.delete('linux.txt')
            dosiye_iyimura_kwihuza.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in insomamabwiriza('./거짓.elf');dosiye_iyimura_kwihuza.delete('거짓.elf')
            iyemeza_raporo['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Guhuza = Ikinyarwanda.자체.연결통신.Guhuza("10.0.2.2", Integer.parseInt(args[0]));
 Guhuza.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] Inkomoko = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<Inkomoko.length;i++) if (Guhuza.getInputStream().read() != (Inkomoko[i]&255)) throw new RuntimeException("TCP mismatch");
 Guhuza.close();
 DatagramSocket 종단 = Ikinyarwanda.자체.통신.Gufungura(0); Ikinyarwanda.자체.통신.대기시간(종단, 500);
 Ikinyarwanda.자체.통신.kohereza(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Ikinyarwanda.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                dosiye_iyimura_kwihuza.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                Umwandiko = insomamabwiriza('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_poti, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in Umwandiko and '10.0.2.2' in Umwandiko and 'exit 0' in Umwandiko, Umwandiko
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            iyemeza_raporo['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            dosiye_iyimura_kwihuza.delete('바깥통신.class')
            seriveri_inkomoko=결과자료/'서버시험.java'
            seriveri_inkomoko.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket seriveri_agaciro = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket 손님 = seriveri_agaciro.accept();
  손님.getOutputStream().write(손님.getInputStream().read()+1); 손님.close(); seriveri_agaciro.close();
  byte[] Ibirimo_agaciro = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Ibirimo_agaciro, Ibirimo_agaciro.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(seriveri_inkomoko)])
            dosiye_iyimura_kwihuza.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            Inzira_a7054519.stdin.write('java 서버시험\n'.encode());Inzira_a7054519.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',seriveri_Stream_poti),timeout=5) as Mugenzi_agaciro:
                Mugenzi_agaciro.sendall(b'A');assert Mugenzi_agaciro.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as Mugenzi_agaciro:
                Mugenzi_agaciro.settimeout(5);Mugenzi_agaciro.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert Mugenzi_agaciro.recvfrom(512)[0]==b'UDP-IN'
            Umwandiko=수신하기();assert 'INBOUND TCP UDP PASS' in Umwandiko and 'exit 0' in Umwandiko,Umwandiko
            iyemeza_raporo['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            dosiye_iyimura_kwihuza.delete('서버시험.class')
            ibwiriza_URUKURIKIRANE = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } Ikinyarwanda.자체.출력.수쓰기(합); Ikinyarwanda.자체.Idosiye.kwandika("aot.txt", "한글 AOT Idosiye 😀"); Ikinyarwanda.자체.출력.kwandika_umurongo(Ikinyarwanda.자체.Idosiye.읽기("aot.txt")); } }'
            dosiye_iyimura_kwihuza.storbinary('STOR 빛.java', io.BytesIO(ibwiriza_URUKURIKIRANE.encode()))
            Umwandiko = insomamabwiriza('javac 빛.java'); assert 'exit 0' in Umwandiko and 'Compiled:' in Umwandiko, Umwandiko
            Umwandiko = insomamabwiriza('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Umwandiko and 'exit 0' in Umwandiko, Umwandiko
            Umwandiko = insomamabwiriza('run 빛.elf'); assert '\n55\n' in Umwandiko and '한글 AOT Idosiye 😀' in Umwandiko and 'exit 0' in Umwandiko, Umwandiko
            자체실행파일 = bytearray(); dosiye_iyimura_kwihuza.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Umwandiko = insomamabwiriza('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Umwandiko and 'unsupported' in Umwandiko, Umwandiko
            보존자료 = bytearray(); dosiye_iyimura_kwihuza.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); dosiye_iyimura_kwihuza.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            dosiye_iyimura_kwihuza.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Umwandiko = insomamabwiriza('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Umwandiko and 'exit 0' in Umwandiko, Umwandiko
            Umwandiko = insomamabwiriza('run 빛.elf'); assert '\n55\n' in Umwandiko and '한글 AOT Idosiye 😀' in Umwandiko and 'exit 0' in Umwandiko, Umwandiko
            iyemeza_raporo['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            iyemeza_raporo['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            kitayega_inkomoko=결과자료/'정적시험.java'
            kitayega_inkomoko.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] agaciro = new int[] {기준, 합(10)};
  System.out.println(agaciro[0] + agaciro[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(kitayega_inkomoko)])
            dosiye_iyimura_kwihuza.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            Umwandiko=insomamabwiriza('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Umwandiko,Umwandiko
            Umwandiko=insomamabwiriza('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Umwandiko,Umwandiko
            dosiye_iyimura_kwihuza.delete('정적시험.class');dosiye_iyimura_kwihuza.delete('정적시험.elf')
            iyemeza_raporo['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(gushyingura.getvalue());손상자료[14]^=1
            dosiye_iyimura_kwihuza.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Umwandiko=insomamabwiriza('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Umwandiko,Umwandiko
            iyemeza_raporo['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            dosiye_iyimura_kwihuza.quit(); assert 'FTP stopped' in insomamabwiriza('ftpd stop')
            assert not 연결다리.IKOSA, 연결다리.IKOSA
            iyemeza_raporo.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in muhitamo.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.gusubika_icyabaye.set()
            Inzira_a7054519.terminate()
            try: Inzira_a7054519.wait(timeout=5)
            except subprocess.TimeoutExpired: Inzira_a7054519.kill(); Inzira_a7054519.wait()
            muhitamo.close(); Inzira_a7054519.stdin.close(); Inzira_a7054519.stdout.close()
            iyemeza_raporo['bridge_error'] = 연결다리.IKOSA
            iyemeza_raporo['frames_to_guest'] = 연결다리.커널수신틀수; iyemeza_raporo['frames_from_guest'] = 연결다리.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(연결다리.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(iyemeza_raporo, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ihuriro()
