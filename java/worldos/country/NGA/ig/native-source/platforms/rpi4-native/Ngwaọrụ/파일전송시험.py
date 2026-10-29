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
from mee_nnyemiwu import 기준, Ntiiwu
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Bido():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    nkwèputaonòdù_akụkọ = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.dee_ahịrī("JAR mee_nnyemiwu: " + 인수[0]); 한국어.자체.Faịlụ.Chekwaa_ozi("jar.txt", "자체 mkpụrụobī_kọmpùta_valuu Faịlụ"); 한국어.자체.출력.dee_ahịrī(한국어.자체.Faịlụ.Wepụta_ọzi("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    ọkpụ = io.BytesIO()
    with zipfile.ZipFile(ọkpụ, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); savà_agịrị_pọọt = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(접속번호, ['tcp:{}:9300'.format(savà_agịrị_pọọt), 'udp:{}:9301'.format(서버전문접속번호)], See=True) as 연결다리:
        ùsòrò = subprocess.Popen(Ntiiwu() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        ihe_nhọpụta = selectors.DefaultSelector(); ihe_nhọpụta.register(ùsòrò.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            datà = bytearray(); mèdebe_Nnokwata = time.monotonic() + 시간제한
            while 확인표시 not in datà:
                if time.monotonic() > mèdebe_Nnokwata or ùsòrò.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + datà.decode('utf-8', 'replace'))
                for 누름값, _ in ihe_nhọpụta.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: datà.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in datà or b'FAIL ' in datà: raise AssertionError(datà)
            return datà.decode('utf-8', 'replace').replace('\r\n', '\n')
        def nkọwannyemiwu(ahịrī):
            ùsòrò.stdin.write(ahịrī.encode() + b'\n'); ùsòrò.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in nkọwannyemiwu('ftpd start')
            ọbọakwụkwọ_dògharịa_njikọ = ftplib.FTP(); ọbọakwụkwọ_dògharịa_njikọ.encoding = 'utf-8'; ọbọakwụkwọ_dògharịa_njikọ.connect('127.0.0.1', 접속번호, timeout=20); ọbọakwụkwọ_dògharịa_njikọ.login()
            ebe_mbulingwa_datà = bytes(range(256)) * 32
            ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR binary.dat', io.BytesIO(ebe_mbulingwa_datà))
            결과 = bytearray(); ọbọakwụkwọ_dògharịa_njikọ.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ebe_mbulingwa_datà; assert ọbọakwụkwọ_dògharịa_njikọ.size('binary.dat') == len(ebe_mbulingwa_datà)
            nkwèputaonòdù_akụkọ['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in nkọwannyemiwu('cat 한글.txt')
            assert '한글.txt' in ọbọakwụkwọ_dògharịa_njikọ.nlst()
            assert dict(ọbọakwụkwọ_dògharịa_njikọ.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            nkwèputaonòdù_akụkọ['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); ọbọakwụkwọ_dògharịa_njikọ.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == ebe_mbulingwa_datà
            nkwèputaonòdù_akụkọ['checks'].append('oversized replacement rejected; previous file preserved')
            with ọbọakwụkwọ_dògharịa_njikọ.transfercmd('STOR pending.txt') as bùlie_Ndi_ọbọakwụkwọ:
                # A control command must not change the active upload's destination.
                assert ọbọakwụkwọ_dògharịa_njikọ.size('binary.dat') == len(ebe_mbulingwa_datà)
                bùlie_Ndi_ọbọakwụkwọ.sendall(b'UPLOAD TARGET PRESERVED')
            assert ọbọakwụkwọ_dògharịa_njikọ.voidresp().startswith('226')
            결과 = bytearray(); ọbọakwụkwọ_dògharịa_njikọ.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); ọbọakwụkwọ_dògharịa_njikọ.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ebe_mbulingwa_datà
            ọbọakwụkwọ_dògharịa_njikọ.delete('pending.txt')
            nkwèputaonòdù_akụkọ['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR 인사.jar', io.BytesIO(ọkpụ.getvalue()))
            SMS = nkọwannyemiwu('java -jar 인사.jar 누리')
            assert 'JAR mee_nnyemiwu: 누리' in SMS and '자체 mkpụrụobī_kọmpùta_valuu Faịlụ' in SMS and 'exit 0' in SMS, SMS
            SMS = nkọwannyemiwu('./인사.jar 세상')
            assert 'JAR mee_nnyemiwu: 세상' in SMS and 'exit 0' in SMS, SMS
            nkwèputaonòdù_akụkọ['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct datà { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct datà valuu = {합(10), 1.25}; if (valuu.수 != 55 || valuu.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = mepee_ọbọakwụkwọ("cc.txt", gụọ_dèe | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; dee_ọbọakwụkwọ_datà(문서, 인사, sizeof(인사)-1); mmechi_ọbọakwụkwọ(문서); dee_ọbọakwụkwọ_datà(1, 인사, sizeof(인사)-1); return 0; }\n'
            ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            SMS = nkọwannyemiwu('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = nkọwannyemiwu('run 한글.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            assert 'CC NATIVE PASS' in nkọwannyemiwu('cat cc.txt')
            실행파일 = bytearray(); ọbọakwụkwọ_dògharịa_njikọ.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR ṅomie_valuu.elf', io.BytesIO(실행파일)); SMS = nkọwannyemiwu('run ṅomie_valuu.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR mee_nnyemiwu', io.BytesIO(실행파일)); SMS=nkọwannyemiwu('./mee_nnyemiwu');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR Aha.txt', io.BytesIO(실행파일)); SMS=nkọwannyemiwu('./Aha.txt');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            nkọwannyemiwu('rm mee_nnyemiwu Aha.txt')
            nkwèputaonòdù_akụkọ['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            nkọwannyemiwu('rm binary.dat 한글.txt 한글.c 한글.elf ṅomie_valuu.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            SMS=nkọwannyemiwu('./리눅스인사');assert 'exit -8' in SMS,SMS
            SMS=nkọwannyemiwu('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in SMS,SMS
            assert 'LINUX ELF FILE IO' in nkọwannyemiwu('cat linux.txt')
            ọbọakwụkwọ_dògharịa_njikọ.delete('리눅스인사');ọbọakwụkwọ_dògharịa_njikọ.delete('linux.txt')
            ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in nkọwannyemiwu('./거짓.elf');ọbọakwụkwọ_dògharịa_njikọ.delete('거짓.elf')
            nkwèputaonòdù_akụkọ['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Banye = 한국어.자체.연결통신.Banye("10.0.2.2", Integer.parseInt(args[0]));
 Banye.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ebensìbịa = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ebensìbịa.length;i++) if (Banye.getInputStream().read() != (ebensìbịa[i]&255)) throw new RuntimeException("TCP mismatch");
 Banye.close();
 DatagramSocket 종단 = 한국어.자체.통신.Mepee(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.zìga(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                SMS = nkọwannyemiwu('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_pọọt, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in SMS and '10.0.2.2' in SMS and 'exit 0' in SMS, SMS
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            nkwèputaonòdù_akụkọ['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ọbọakwụkwọ_dògharịa_njikọ.delete('바깥통신.class')
            savà_ebensìbịa=결과자료/'서버시험.java'
            savà_ebensìbịa.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket savà_valuu = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket 손님 = savà_valuu.accept();
  손님.getOutputStream().write(손님.getInputStream().read()+1); 손님.close(); savà_valuu.close();
  byte[] ndịnà_valuu = new byte[8]; DatagramPacket 전문 = new DatagramPacket(ndịnà_valuu, ndịnà_valuu.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(savà_ebensìbịa)])
            ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            ùsòrò.stdin.write('java 서버시험\n'.encode());ùsòrò.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',savà_agịrị_pọọt),timeout=5) as ibè_valuu:
                ibè_valuu.sendall(b'A');assert ibè_valuu.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ibè_valuu:
                ibè_valuu.settimeout(5);ibè_valuu.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert ibè_valuu.recvfrom(512)[0]==b'UDP-IN'
            SMS=수신하기();assert 'INBOUND TCP UDP PASS' in SMS and 'exit 0' in SMS,SMS
            nkwèputaonòdù_akụkọ['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ọbọakwụkwọ_dògharịa_njikọ.delete('서버시험.class')
            okwunkụzi_NSOTANSO = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.Faịlụ.Chekwaa_ozi("aot.txt", "한글 AOT Faịlụ 😀"); 한국어.자체.출력.dee_ahịrī(한국어.자체.Faịlụ.Wepụta_ọzi("aot.txt")); } }'
            ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR 빛.java', io.BytesIO(okwunkụzi_NSOTANSO.encode()))
            SMS = nkọwannyemiwu('javac 빛.java'); assert 'exit 0' in SMS and 'Compiled:' in SMS, SMS
            SMS = nkọwannyemiwu('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = nkọwannyemiwu('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT Faịlụ 😀' in SMS and 'exit 0' in SMS, SMS
            자체실행파일 = bytearray(); ọbọakwụkwọ_dògharịa_njikọ.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            SMS = nkọwannyemiwu('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in SMS and 'unsupported' in SMS, SMS
            보존자료 = bytearray(); ọbọakwụkwọ_dògharịa_njikọ.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ọbọakwụkwọ_dògharịa_njikọ.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            SMS = nkọwannyemiwu('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = nkọwannyemiwu('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT Faịlụ 😀' in SMS and 'exit 0' in SMS, SMS
            nkwèputaonòdù_akụkọ['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            nkwèputaonòdù_akụkọ['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            adịmgbanwò_ebensìbịa=결과자료/'정적시험.java'
            adịmgbanwò_ebensìbịa.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] valuu = new int[] {기준, 합(10)};
  System.out.println(valuu[0] + valuu[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(adịmgbanwò_ebensìbịa)])
            ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            SMS=nkọwannyemiwu('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in SMS,SMS
            SMS=nkọwannyemiwu('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in SMS,SMS
            ọbọakwụkwọ_dògharịa_njikọ.delete('정적시험.class');ọbọakwụkwọ_dògharịa_njikọ.delete('정적시험.elf')
            nkwèputaonòdù_akụkọ['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ọkpụ.getvalue());손상자료[14]^=1
            ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            SMS=nkọwannyemiwu('java -jar 인사.jar');assert 'Main-Class\nexit 1' in SMS,SMS
            nkwèputaonòdù_akụkọ['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ọbọakwụkwọ_dògharịa_njikọ.quit(); assert 'FTP stopped' in nkọwannyemiwu('ftpd stop')
            assert not 연결다리.mmejọ, 연결다리.mmejọ
            nkwèputaonòdù_akụkọ.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in ihe_nhọpụta.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.chèretụ_mmèrème.set()
            ùsòrò.terminate()
            try: ùsòrò.wait(timeout=5)
            except subprocess.TimeoutExpired: ùsòrò.kill(); ùsòrò.wait()
            ihe_nhọpụta.close(); ùsòrò.stdin.close(); ùsòrò.stdout.close()
            nkwèputaonòdù_akụkọ['bridge_error'] = 연결다리.mmejọ
            nkwèputaonòdù_akụkọ['frames_to_guest'] = 연결다리.커널수신틀수; nkwèputaonòdù_akụkọ['frames_from_guest'] = 연결다리.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(연결다리.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(nkwèputaonòdù_akụkọ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Bido()
