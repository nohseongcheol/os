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
from Inethiwekhi_ibhulorho import Inethiwekhi_ibhulorho
from ukwenza_umyalelo import 기준, Umyalelo
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Phumeza():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    uqinisekiso_ingxelo = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { isiXhosa.자체.출력.bhala_umgca("JAR ukwenza_umyalelo: " + 인수[0]); isiXhosa.자체.iFayili.Bhala("jar.txt", "자체 ikheneli_ixabiso iFayili"); isiXhosa.자체.출력.bhala_umgca(isiXhosa.자체.iFayili.Funda("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    Uvimba = io.BytesIO()
    with zipfile.ZipFile(Uvimba, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); iseva_Stream_iphothi = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Inethiwekhi_ibhulorho(접속번호, ['tcp:{}:9300'.format(iseva_Stream_iphothi), 'udp:{}:9301'.format(서버전문접속번호)], bamba=True) as ibhulorho:
        Inkqubo = subprocess.Popen(Umyalelo() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ibhulorho.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        umkhethi = selectors.DefaultSelector(); umkhethi.register(Inkqubo.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            iingcombolo = bytearray(); phela_Ukulinganisa = time.monotonic() + 시간제한
            while 확인표시 not in iingcombolo:
                if time.monotonic() > phela_Ukulinganisa or Inkqubo.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + iingcombolo.decode('utf-8', 'replace'))
                for 누름값, _ in umkhethi.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: iingcombolo.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in iingcombolo or b'FAIL ' in iingcombolo: raise AssertionError(iingcombolo)
            return iingcombolo.decode('utf-8', 'replace').replace('\r\n', '\n')
        def isiniki_myalelo(umgca):
            Inkqubo.stdin.write(umgca.encode() + b'\n'); Inkqubo.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in isiniki_myalelo('ftpd start')
            ifayile_gqithisela_uqhagamshelo = ftplib.FTP(); ifayile_gqithisela_uqhagamshelo.encoding = 'utf-8'; ifayile_gqithisela_uqhagamshelo.connect('127.0.0.1', 접속번호, timeout=20); ifayile_gqithisela_uqhagamshelo.login()
            umthwalo_wentlawulo_iingcombolo = bytes(range(256)) * 32
            ifayile_gqithisela_uqhagamshelo.storbinary('STOR binary.dat', io.BytesIO(umthwalo_wentlawulo_iingcombolo))
            결과 = bytearray(); ifayile_gqithisela_uqhagamshelo.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == umthwalo_wentlawulo_iingcombolo; assert ifayile_gqithisela_uqhagamshelo.size('binary.dat') == len(umthwalo_wentlawulo_iingcombolo)
            uqinisekiso_ingxelo['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ifayile_gqithisela_uqhagamshelo.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in isiniki_myalelo('cat 한글.txt')
            assert '한글.txt' in ifayile_gqithisela_uqhagamshelo.nlst()
            assert dict(ifayile_gqithisela_uqhagamshelo.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            uqinisekiso_ingxelo['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ifayile_gqithisela_uqhagamshelo.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); ifayile_gqithisela_uqhagamshelo.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == umthwalo_wentlawulo_iingcombolo
            uqinisekiso_ingxelo['checks'].append('oversized replacement rejected; previous file preserved')
            with ifayile_gqithisela_uqhagamshelo.transfercmd('STOR pending.txt') as layisha_Iifayile:
                # A control command must not change the active upload's destination.
                assert ifayile_gqithisela_uqhagamshelo.size('binary.dat') == len(umthwalo_wentlawulo_iingcombolo)
                layisha_Iifayile.sendall(b'UPLOAD TARGET PRESERVED')
            assert ifayile_gqithisela_uqhagamshelo.voidresp().startswith('226')
            결과 = bytearray(); ifayile_gqithisela_uqhagamshelo.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); ifayile_gqithisela_uqhagamshelo.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == umthwalo_wentlawulo_iingcombolo
            ifayile_gqithisela_uqhagamshelo.delete('pending.txt')
            uqinisekiso_ingxelo['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ifayile_gqithisela_uqhagamshelo.storbinary('STOR 인사.jar', io.BytesIO(Uvimba.getvalue()))
            Umbhalo = isiniki_myalelo('java -jar 인사.jar 누리')
            assert 'JAR ukwenza_umyalelo: 누리' in Umbhalo and '자체 ikheneli_ixabiso iFayili' in Umbhalo and 'exit 0' in Umbhalo, Umbhalo
            Umbhalo = isiniki_myalelo('./인사.jar 세상')
            assert 'JAR ukwenza_umyalelo: 세상' in Umbhalo and 'exit 0' in Umbhalo, Umbhalo
            uqinisekiso_ingxelo['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct iingcombolo { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct iingcombolo ixabiso = {합(10), 1.25}; if (ixabiso.수 != 55 || ixabiso.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = vula_ifayile("cc.txt", funda_bhala | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; bhala_ifayile_iingcombolo(문서, 인사, sizeof(인사)-1); vala_ifayile(문서); bhala_ifayile_iingcombolo(1, 인사, sizeof(인사)-1); return 0; }\n'
            ifayile_gqithisela_uqhagamshelo.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Umbhalo = isiniki_myalelo('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Umbhalo and 'exit 0' in Umbhalo, Umbhalo
            Umbhalo = isiniki_myalelo('run 한글.elf'); assert 'CC NATIVE PASS' in Umbhalo and 'exit 0' in Umbhalo, Umbhalo
            assert 'CC NATIVE PASS' in isiniki_myalelo('cat cc.txt')
            실행파일 = bytearray(); ifayile_gqithisela_uqhagamshelo.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ifayile_gqithisela_uqhagamshelo.storbinary('STOR kopa_ixabiso.elf', io.BytesIO(실행파일)); Umbhalo = isiniki_myalelo('run kopa_ixabiso.elf'); assert 'CC NATIVE PASS' in Umbhalo and 'exit 0' in Umbhalo, Umbhalo
            ifayile_gqithisela_uqhagamshelo.storbinary('STOR ukwenza_umyalelo', io.BytesIO(실행파일)); Umbhalo=isiniki_myalelo('./ukwenza_umyalelo');assert 'CC NATIVE PASS' in Umbhalo and 'exit 0' in Umbhalo,Umbhalo
            ifayile_gqithisela_uqhagamshelo.storbinary('STOR Igama.txt', io.BytesIO(실행파일)); Umbhalo=isiniki_myalelo('./Igama.txt');assert 'CC NATIVE PASS' in Umbhalo and 'exit 0' in Umbhalo,Umbhalo
            isiniki_myalelo('rm ukwenza_umyalelo Igama.txt')
            uqinisekiso_ingxelo['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            isiniki_myalelo('rm binary.dat 한글.txt 한글.c 한글.elf kopa_ixabiso.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            ifayile_gqithisela_uqhagamshelo.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Umbhalo=isiniki_myalelo('./리눅스인사');assert 'exit -8' in Umbhalo,Umbhalo
            Umbhalo=isiniki_myalelo('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Umbhalo,Umbhalo
            assert 'LINUX ELF FILE IO' in isiniki_myalelo('cat linux.txt')
            ifayile_gqithisela_uqhagamshelo.delete('리눅스인사');ifayile_gqithisela_uqhagamshelo.delete('linux.txt')
            ifayile_gqithisela_uqhagamshelo.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in isiniki_myalelo('./거짓.elf');ifayile_gqithisela_uqhagamshelo.delete('거짓.elf')
            uqinisekiso_ingxelo['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Nxulumanisa = isiXhosa.자체.연결통신.Nxulumanisa("10.0.2.2", Integer.parseInt(args[0]));
 Nxulumanisa.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] UMTHOMBO = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<UMTHOMBO.length;i++) if (Nxulumanisa.getInputStream().read() != (UMTHOMBO[i]&255)) throw new RuntimeException("TCP mismatch");
 Nxulumanisa.close();
 DatagramSocket 종단 = isiXhosa.자체.통신.Vula(0); isiXhosa.자체.통신.대기시간(종단, 500);
 isiXhosa.자체.통신.thumela(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!isiXhosa.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                ifayile_gqithisela_uqhagamshelo.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                Umbhalo = isiniki_myalelo('java 바깥통신 {} {}'.format(되돌림서버항목.i_TCP_iphothi, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in Umbhalo and '10.0.2.2' in Umbhalo and 'exit 0' in Umbhalo, Umbhalo
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            uqinisekiso_ingxelo['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ifayile_gqithisela_uqhagamshelo.delete('바깥통신.class')
            iseva_umthombo=결과자료/'서버시험.java'
            iseva_umthombo.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket iseva_ixabiso = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket undwendwe_ixabiso = iseva_ixabiso.accept();
  undwendwe_ixabiso.getOutputStream().write(undwendwe_ixabiso.getInputStream().read()+1); undwendwe_ixabiso.close(); iseva_ixabiso.close();
  byte[] Isiqulatho_ixabiso = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Isiqulatho_ixabiso, Isiqulatho_ixabiso.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(iseva_umthombo)])
            ifayile_gqithisela_uqhagamshelo.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            Inkqubo.stdin.write('java 서버시험\n'.encode());Inkqubo.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',iseva_Stream_iphothi),timeout=5) as untanga_ixabiso:
                untanga_ixabiso.sendall(b'A');assert untanga_ixabiso.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as untanga_ixabiso:
                untanga_ixabiso.settimeout(5);untanga_ixabiso.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert untanga_ixabiso.recvfrom(512)[0]==b'UDP-IN'
            Umbhalo=수신하기();assert 'INBOUND TCP UDP PASS' in Umbhalo and 'exit 0' in Umbhalo,Umbhalo
            uqinisekiso_ingxelo['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ifayile_gqithisela_uqhagamshelo.delete('서버시험.class')
            umyalelo_ULANDELELWANO = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } isiXhosa.자체.출력.수쓰기(합); isiXhosa.자체.iFayili.Bhala("aot.txt", "한글 AOT iFayili 😀"); isiXhosa.자체.출력.bhala_umgca(isiXhosa.자체.iFayili.Funda("aot.txt")); } }'
            ifayile_gqithisela_uqhagamshelo.storbinary('STOR 빛.java', io.BytesIO(umyalelo_ULANDELELWANO.encode()))
            Umbhalo = isiniki_myalelo('javac 빛.java'); assert 'exit 0' in Umbhalo and 'Compiled:' in Umbhalo, Umbhalo
            Umbhalo = isiniki_myalelo('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Umbhalo and 'exit 0' in Umbhalo, Umbhalo
            Umbhalo = isiniki_myalelo('run 빛.elf'); assert '\n55\n' in Umbhalo and '한글 AOT iFayili 😀' in Umbhalo and 'exit 0' in Umbhalo, Umbhalo
            자체실행파일 = bytearray(); ifayile_gqithisela_uqhagamshelo.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Umbhalo = isiniki_myalelo('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Umbhalo and 'unsupported' in Umbhalo, Umbhalo
            보존자료 = bytearray(); ifayile_gqithisela_uqhagamshelo.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ifayile_gqithisela_uqhagamshelo.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ifayile_gqithisela_uqhagamshelo.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Umbhalo = isiniki_myalelo('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Umbhalo and 'exit 0' in Umbhalo, Umbhalo
            Umbhalo = isiniki_myalelo('run 빛.elf'); assert '\n55\n' in Umbhalo and '한글 AOT iFayili 😀' in Umbhalo and 'exit 0' in Umbhalo, Umbhalo
            uqinisekiso_ingxelo['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            uqinisekiso_ingxelo['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            imi_ndawonye_umthombo=결과자료/'정적시험.java'
            imi_ndawonye_umthombo.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] ixabiso = new int[] {기준, 합(10)};
  System.out.println(ixabiso[0] + ixabiso[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(imi_ndawonye_umthombo)])
            ifayile_gqithisela_uqhagamshelo.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            Umbhalo=isiniki_myalelo('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Umbhalo,Umbhalo
            Umbhalo=isiniki_myalelo('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Umbhalo,Umbhalo
            ifayile_gqithisela_uqhagamshelo.delete('정적시험.class');ifayile_gqithisela_uqhagamshelo.delete('정적시험.elf')
            uqinisekiso_ingxelo['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Uvimba.getvalue());손상자료[14]^=1
            ifayile_gqithisela_uqhagamshelo.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Umbhalo=isiniki_myalelo('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Umbhalo,Umbhalo
            uqinisekiso_ingxelo['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ifayile_gqithisela_uqhagamshelo.quit(); assert 'FTP stopped' in isiniki_myalelo('ftpd stop')
            assert not ibhulorho.Impazamo, ibhulorho.Impazamo
            uqinisekiso_ingxelo.update(passed=True, frames_to_guest=ibhulorho.커널수신틀수, frames_from_guest=ibhulorho.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in umkhethi.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            ibhulorho.nqumama_umcimbi.set()
            Inkqubo.terminate()
            try: Inkqubo.wait(timeout=5)
            except subprocess.TimeoutExpired: Inkqubo.kill(); Inkqubo.wait()
            umkhethi.close(); Inkqubo.stdin.close(); Inkqubo.stdout.close()
            uqinisekiso_ingxelo['bridge_error'] = ibhulorho.Impazamo
            uqinisekiso_ingxelo['frames_to_guest'] = ibhulorho.커널수신틀수; uqinisekiso_ingxelo['frames_from_guest'] = ibhulorho.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(ibhulorho.ithreyisi_ilog,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(uqinisekiso_ingxelo, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Phumeza()
