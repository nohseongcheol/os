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
from híd_3de4fe3a import híd_3de4fe3a
from végrehajt_parancs import teendő_gyök, Parancs
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Futtatás():
    KR_adat = teendő_gyök / 'build/verification/ftp'; KR_adat.mkdir(parents=True, exist_ok=True)
    ellenőrzés_jelent = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((teendő_gyök / 'build/kernel8.img').read_bytes()).hexdigest()}
    átirat = bytearray()
    자바원문 = KR_adat / 'teszt_köteg.java'
    자바원문.write_text('public class teszt_köteg { public static void main(String[] Argumentumok) throws Exception { magyar.saját.Kimenet.ír_sor("JAR végrehajt_parancs: " + Argumentumok[0]); magyar.saját.Fájl.Írás("jar.txt", "saját kernel_ÉRTÉK Fájl"); magyar.saját.Kimenet.ír_sor(magyar.saját.Fájl.Olvasás("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(teendő_gyök/'build/java-library/classes'), '-d', str(KR_adat), str(자바원문)])
    archív = io.BytesIO()
    with zipfile.ZipFile(archív, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: teszt_köteg\r\n\r\n')
        자바꾸러미.write(str(KR_adat/'teszt_köteg.class'), 'teszt_köteg.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); portszám = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); kiszolgáló_Stream_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); kiszolgáló_datagram_port = 임시자원.getsockname()[1]
    with híd_3de4fe3a(portszám, ['tcp:{}:9300'.format(kiszolgáló_Stream_port), 'udp:{}:9301'.format(kiszolgáló_datagram_port)], kioszt=True) as híd:
        Folyamat = subprocess.Popen(Parancs() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + híd.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        szelektor = selectors.DefaultSelector(); szelektor.register(Folyamat.stdout, selectors.EVENT_READ)
        def fogad_e_mail(jelölő=b'jkoros-native> ', végrehajtás_IDŐTÚLLÉPÉS=60):
            adat = bytearray(); megszüntet_Ofszet = time.monotonic() + végrehajtás_IDŐTÚLLÉPÉS
            while jelölő not in adat:
                if time.monotonic() > megszüntet_Ofszet or Folyamat.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + adat.decode('utf-8', 'replace'))
                for 누름값, _ in szelektor.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: adat.extend(조각); átirat.extend(조각)
                if b'PANIC:' in adat or b'FAIL ' in adat: raise AssertionError(adat)
            return adat.decode('utf-8', 'replace').replace('\r\n', '\n')
        def felület(Vonal):
            Folyamat.stdin.write(Vonal.encode() + b'\n'); Folyamat.stdin.flush(); return fogad_e_mail()
        try:
            fogad_e_mail(); assert 'FTP listening' in felület('ftpd start')
            fájlátvitel_ismerős = ftplib.FTP(); fájlátvitel_ismerős.encoding = 'utf-8'; fájlátvitel_ismerős.connect('127.0.0.1', portszám, timeout=20); fájlátvitel_ismerős.login()
            teher_adat = bytes(range(256)) * 32
            fájlátvitel_ismerős.storbinary('STOR binary.dat', io.BytesIO(teher_adat))
            KR = bytearray(); fájlátvitel_ismerős.retrbinary('RETR binary.dat', KR.extend)
            assert KR == teher_adat; assert fájlátvitel_ismerős.size('binary.dat') == len(teher_adat)
            ellenőrzés_jelent['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            fájlátvitel_ismerős.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in felület('cat 한글.txt')
            assert '한글.txt' in fájlátvitel_ismerős.nlst()
            assert dict(fájlátvitel_ismerős.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            ellenőrzés_jelent['checks'].append('UTF-8 filename and content visible in guest shell')
            try: fájlátvitel_ismerős.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            KR = bytearray(); fájlátvitel_ismerős.retrbinary('RETR binary.dat', KR.extend); assert KR == teher_adat
            ellenőrzés_jelent['checks'].append('oversized replacement rejected; previous file preserved')
            with fájlátvitel_ismerős.transfercmd('STOR pending.txt') as feltölt_Files:
                # A control command must not change the active upload's destination.
                assert fájlátvitel_ismerős.size('binary.dat') == len(teher_adat)
                feltölt_Files.sendall(b'UPLOAD TARGET PRESERVED')
            assert fájlátvitel_ismerős.voidresp().startswith('226')
            KR = bytearray(); fájlátvitel_ismerős.retrbinary('RETR pending.txt', KR.extend)
            assert KR == b'UPLOAD TARGET PRESERVED'
            KR = bytearray(); fájlátvitel_ismerős.retrbinary('RETR binary.dat', KR.extend)
            assert KR == teher_adat
            fájlátvitel_ismerős.delete('pending.txt')
            ellenőrzés_jelent['checks'].append('interleaved SIZE cannot change the active STOR destination')
            fájlátvitel_ismerős.storbinary('STOR 인사.jar', io.BytesIO(archív.getvalue()))
            Szöveg = felület('java -jar 인사.jar 누리')
            assert 'JAR végrehajt_parancs: 누리' in Szöveg and 'saját kernel_ÉRTÉK Fájl' in Szöveg and 'exit 0' in Szöveg, Szöveg
            Szöveg = felület('./인사.jar 세상')
            assert 'JAR végrehajt_parancs: 세상' in Szöveg and 'exit 0' in Szöveg, Szöveg
            ellenőrzés_jelent['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct adat { int szám; double 비율; };\nint SUM_ÉRTÉK(int n) { return n ? n + SUM_ÉRTÉK(n-1) : 0; }\nint main(void) { struct adat ÉRTÉK = {SUM_ÉRTÉK(10), 1.25}; if (ÉRTÉK.szám != 55 || ÉRTÉK.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = készít_Fájl("cc.txt", 읽고쓰기 | 없으면만들기 | vág_Tartalom, 0600); if (문서 < 0) return 1; ír_Fájl_adat(문서, 인사, sizeof(인사)-1); bezár_Fájl(문서); ír_Fájl_adat(1, 인사, sizeof(인사)-1); return 0; }\n'
            fájlátvitel_ismerős.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Szöveg = felület('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Szöveg and 'exit 0' in Szöveg, Szöveg
            Szöveg = felület('run 한글.elf'); assert 'CC NATIVE PASS' in Szöveg and 'exit 0' in Szöveg, Szöveg
            assert 'CC NATIVE PASS' in felület('cat cc.txt')
            végrehajtható_Fájl = bytearray(); fájlátvitel_ismerős.retrbinary('RETR 한글.elf', végrehajtható_Fájl.extend)
            assert végrehajtható_Fájl[:4] == b'\x7fELF' and végrehajtható_Fájl[18:20] == b'\xb7\x00'
            fájlátvitel_ismerős.storbinary('STOR másol_ÉRTÉK.elf', io.BytesIO(végrehajtható_Fájl)); Szöveg = felület('run másol_ÉRTÉK.elf'); assert 'CC NATIVE PASS' in Szöveg and 'exit 0' in Szöveg, Szöveg
            fájlátvitel_ismerős.storbinary('STOR végrehajt_parancs', io.BytesIO(végrehajtható_Fájl)); Szöveg=felület('./végrehajt_parancs');assert 'CC NATIVE PASS' in Szöveg and 'exit 0' in Szöveg,Szöveg
            fájlátvitel_ismerős.storbinary('STOR Név.txt', io.BytesIO(végrehajtható_Fájl)); Szöveg=felület('./Név.txt');assert 'CC NATIVE PASS' in Szöveg and 'exit 0' in Szöveg,Szöveg
            felület('rm végrehajt_parancs Név.txt')
            ellenőrzés_jelent['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            felület('rm binary.dat 한글.txt 한글.c 한글.elf másol_ÉRTÉK.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_adat/'linux-reference')
            fájlátvitel_ismerős.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Szöveg=felület('./리눅스인사');assert 'exit -8' in Szöveg,Szöveg
            Szöveg=felület('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Szöveg,Szöveg
            assert 'LINUX ELF FILE IO' in felület('cat linux.txt')
            fájlátvitel_ismerős.delete('리눅스인사');fájlátvitel_ismerős.delete('linux.txt')
            fájlátvitel_ismerős.storbinary('STOR HAMIS_ÉRTÉK.elf',io.BytesIO(b'plain text'))
            assert '실행할 szám 없습니다:' in felület('./HAMIS_ÉRTÉK.elf');fájlátvitel_ismerős.delete('HAMIS_ÉRTÉK.elf')
            ellenőrzés_jelent['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as visszhang_kiszolgáló_bejegyzés:
                NET_forrás = KR_adat/'külső_kommunikáció.java'
                NET_forrás.write_text('''import java.net.*; import java.io.*;
public class külső_kommunikáció { public static void main(String[] args) throws Exception {
 Socket Kapcsolódás = magyar.saját.ismerős_szállítás.Kapcsolódás("10.0.2.2", Integer.parseInt(args[0]));
 Kapcsolódás.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] FORRÁS = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<FORRÁS.length;i++) if (Kapcsolódás.getInputStream().read() != (FORRÁS[i]&255)) throw new RuntimeException("TCP mismatch");
 Kapcsolódás.close();
 DatagramSocket végpont = magyar.saját.kommunikáció.Megnyitás(0); magyar.saját.kommunikáció.IDŐTÚLLÉPÉS(végpont, 500);
 magyar.saját.kommunikáció.küld(végpont, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!magyar.saját.kommunikáció.fogad(végpont).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 végpont.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(teendő_gyök/'build/java-library/classes'),'-d',str(KR_adat),str(NET_forrás)])
                fájlátvitel_ismerős.storbinary('STOR külső_kommunikáció.class', io.BytesIO((KR_adat/'külső_kommunikáció.class').read_bytes()))
                Szöveg = felület('java külső_kommunikáció {} {}'.format(visszhang_kiszolgáló_bejegyzés.TCP_port, visszhang_kiszolgáló_bejegyzés.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in Szöveg and '10.0.2.2' in Szöveg and 'exit 0' in Szöveg, Szöveg
                assert visszhang_kiszolgáló_bejegyzés.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, visszhang_kiszolgáló_bejegyzés.수신됨
                assert not visszhang_kiszolgáló_bejegyzés.오류들, visszhang_kiszolgáló_bejegyzés.오류들
            ellenőrzés_jelent['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            fájlátvitel_ismerős.delete('külső_kommunikáció.class')
            kiszolgáló_forrás=KR_adat/'kiszolgáló_teszt.java'
            kiszolgáló_forrás.write_text('''import java.net.*; public class kiszolgáló_teszt {
 public static void main(String[] args) throws Exception {
  ServerSocket kiszolgáló_ÉRTÉK = new ServerSocket(9300); DatagramSocket végpont = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket vendég_ÉRTÉK = kiszolgáló_ÉRTÉK.accept();
  vendég_ÉRTÉK.getOutputStream().write(vendég_ÉRTÉK.getInputStream().read()+1); vendég_ÉRTÉK.close(); kiszolgáló_ÉRTÉK.close();
  byte[] Tartalom_ÉRTÉK = new byte[8]; DatagramPacket datagram = new DatagramPacket(Tartalom_ÉRTÉK, Tartalom_ÉRTÉK.length); végpont.receive(datagram);
  végpont.send(datagram); végpont.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_adat),str(kiszolgáló_forrás)])
            fájlátvitel_ismerős.storbinary('STOR kiszolgáló_teszt.class',io.BytesIO((KR_adat/'kiszolgáló_teszt.class').read_bytes()))
            Folyamat.stdin.write('java kiszolgáló_teszt\n'.encode());Folyamat.stdin.flush();fogad_e_mail(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',kiszolgáló_Stream_port),timeout=5) as társ_ÉRTÉK:
                társ_ÉRTÉK.sendall(b'A');assert társ_ÉRTÉK.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as társ_ÉRTÉK:
                társ_ÉRTÉK.settimeout(5);társ_ÉRTÉK.sendto(b'UDP-IN',('127.0.0.1',kiszolgáló_datagram_port));assert társ_ÉRTÉK.recvfrom(512)[0]==b'UDP-IN'
            Szöveg=fogad_e_mail();assert 'INBOUND TCP UDP PASS' in Szöveg and 'exit 0' in Szöveg,Szöveg
            ellenőrzés_jelent['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            fájlátvitel_ismerős.delete('kiszolgáló_teszt.class')
            명령열 = 'public class 빛 { public static void main(String[] Argumentumok) throws Exception { int SUM_ÉRTÉK = 0; int szám = 1; while (szám <= 10) { SUM_ÉRTÉK = SUM_ÉRTÉK + szám; szám = szám + 1; } magyar.saját.Kimenet.ír_szám(SUM_ÉRTÉK); magyar.saját.Fájl.Írás("aot.txt", "한글 AOT Fájl 😀"); magyar.saját.Kimenet.ír_sor(magyar.saját.Fájl.Olvasás("aot.txt")); } }'
            fájlátvitel_ismerős.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            Szöveg = felület('javac 빛.java'); assert 'exit 0' in Szöveg and 'Compiled:' in Szöveg, Szöveg
            Szöveg = felület('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Szöveg and 'exit 0' in Szöveg, Szöveg
            Szöveg = felület('run 빛.elf'); assert '\n55\n' in Szöveg and '한글 AOT Fájl 😀' in Szöveg and 'exit 0' in Szöveg, Szöveg
            natív = bytearray(); fájlátvitel_ismerős.retrbinary('RETR 빛.elf', natív.extend)
            Szöveg = felület('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Szöveg and 'unsupported' in Szöveg, Szöveg
            보존자료 = bytearray(); fájlátvitel_ismerős.retrbinary('RETR 빛.elf', 보존자료.extend); assert natív == 보존자료
            바이트코드 = bytearray(); fájlátvitel_ismerős.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            fájlátvitel_ismerős.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Szöveg = felület('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Szöveg and 'exit 0' in Szöveg, Szöveg
            Szöveg = felület('run 빛.elf'); assert '\n55\n' in Szöveg and '한글 AOT Fájl 😀' in Szöveg and 'exit 0' in Szöveg, Szöveg
            ellenőrzés_jelent['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            ellenőrzés_jelent['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statikus_forrás=KR_adat/'statikus_teszt.java'
            statikus_forrás.write_text('''public class statikus_teszt {
 static int teendő_gyök = 3;
 static int SUM_ÉRTÉK(int n) { return n == 0 ? 0 : n + SUM_ÉRTÉK(n-1); }
 public static void main(String[] Argumentumok) {
  int[] ÉRTÉK = new int[] {teendő_gyök, SUM_ÉRTÉK(10)};
  System.out.println(ÉRTÉK[0] + ÉRTÉK[1]); System.out.println(Argumentumok[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_adat),str(statikus_forrás)])
            fájlátvitel_ismerős.storbinary('STOR statikus_teszt.class',io.BytesIO((KR_adat/'statikus_teszt.class').read_bytes()))
            Szöveg=felület('jaot statikus_teszt.class -o statikus_teszt.elf');assert 'exit 0' in Szöveg,Szöveg
            Szöveg=felület('run statikus_teszt.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Szöveg,Szöveg
            fájlátvitel_ismerős.delete('statikus_teszt.class');fájlátvitel_ismerős.delete('statikus_teszt.elf')
            ellenőrzés_jelent['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(archív.getvalue());손상자료[14]^=1
            fájlátvitel_ismerős.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Szöveg=felület('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Szöveg,Szöveg
            ellenőrzés_jelent['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            fájlátvitel_ismerős.quit(); assert 'FTP stopped' in felület('ftpd stop')
            assert not híd.HIBA, híd.HIBA
            ellenőrzés_jelent.update(passed=True, frames_to_guest=híd.커널수신틀수, frames_from_guest=híd.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in szelektor.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: átirat.extend(조각)
            híd.Szünet_esemény.set()
            Folyamat.terminate()
            try: Folyamat.wait(timeout=5)
            except subprocess.TimeoutExpired: Folyamat.kill(); Folyamat.wait()
            szelektor.close(); Folyamat.stdin.close(); Folyamat.stdout.close()
            ellenőrzés_jelent['bridge_error'] = híd.HIBA
            ellenőrzés_jelent['frames_to_guest'] = híd.커널수신틀수; ellenőrzés_jelent['frames_from_guest'] = híd.커널발신틀수
            (KR_adat/'packets.json').write_text(json.dumps(híd.nyomkövetési_napló,indent=2)+'\n')
            (KR_adat / 'serial.log').write_bytes(átirat)
            (KR_adat / 'report.json').write_text(json.dumps(ellenőrzés_jelent, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Futtatás()
