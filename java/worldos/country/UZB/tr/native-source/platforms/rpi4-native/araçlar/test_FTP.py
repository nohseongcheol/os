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
from köprü_3de4fe3a import köprü_3de4fe3a
from yürütmek_komut import işlem_kök, komut
from yankı_düzen import yankı_düzen
from 실행파일시험 import 리눅스예제


def çalıştır():
    KR_veri = işlem_kök / 'build/verification/ftp'; KR_veri.mkdir(parents=True, exist_ok=True)
    doğrulama_Rapor = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((işlem_kök / 'build/kernel8.img').read_bytes()).hexdigest()}
    döküm = bytearray()
    자바원문 = KR_veri / 'test_paket_iş.java'
    자바원문.write_text('public class test_paket_iş { public static void main(String[] bağımsız_değişkenler) throws Exception { Türkçe.Öz.metinÇıktısı.yazma_hat("JAR yürütmek_komut: " + bağımsız_değişkenler[0]); Türkçe.Öz.dosya.Yazma("jar.txt", "Öz çekirdek_değer dosya"); Türkçe.Öz.metinÇıktısı.yazma_hat(Türkçe.Öz.dosya.Okuma("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(işlem_kök/'build/java-library/classes'), '-d', str(KR_veri), str(자바원문)])
    Arşiv = io.BytesIO()
    with zipfile.ZipFile(Arşiv, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: test_paket_iş\r\n\r\n')
        자바꾸러미.write(str(KR_veri/'test_paket_iş.class'), 'test_paket_iş.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); bağlantı_noktası_numarası = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); sunucu_akış_taşımak = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); sunucu_veri_birimi_taşımak = 임시자원.getsockname()[1]
    with köprü_3de4fe3a(bağlantı_noktası_numarası, ['tcp:{}:9300'.format(sunucu_akış_taşımak), 'udp:{}:9301'.format(sunucu_veri_birimi_taşımak)], çekmek=True) as köprü:
        Süreç = subprocess.Popen(komut() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + köprü.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        seçici = selectors.DefaultSelector(); seçici.register(Süreç.stdout, selectors.EVENT_READ)
        def almak_belge(işaret=b'jkoros-native> ', yürütme_ZAMANAŞIMI=60):
            veri = bytearray(); Bitiş_Ofset = time.monotonic() + yürütme_ZAMANAŞIMI
            while işaret not in veri:
                if time.monotonic() > Bitiş_Ofset or Süreç.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + veri.decode('utf-8', 'replace'))
                for 누름값, _ in seçici.select(.1):
                    parça_değer = 누름값.fileobj.read(4096)
                    if parça_değer: veri.extend(parça_değer); döküm.extend(parça_değer)
                if b'PANIC:' in veri or b'FAIL ' in veri: raise AssertionError(veri)
            return veri.decode('utf-8', 'replace').replace('\r\n', '\n')
        def kabuk(girdi_satırı):
            Süreç.stdin.write(girdi_satırı.encode() + b'\n'); Süreç.stdin.flush(); return almak_belge()
        try:
            almak_belge(); assert 'FTP listening' in kabuk('ftpd start')
            dosya_aktarımı_cxn = ftplib.FTP(); dosya_aktarımı_cxn.encoding = 'utf-8'; dosya_aktarımı_cxn.connect('127.0.0.1', bağlantı_noktası_numarası, timeout=20); dosya_aktarımı_cxn.login()
            yük_veri = bytes(range(256)) * 32
            dosya_aktarımı_cxn.storbinary('STOR binary.dat', io.BytesIO(yük_veri))
            sonuç = bytearray(); dosya_aktarımı_cxn.retrbinary('RETR binary.dat', sonuç.extend)
            assert sonuç == yük_veri; assert dosya_aktarımı_cxn.size('binary.dat') == len(yük_veri)
            doğrulama_Rapor['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            dosya_aktarımı_cxn.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in kabuk('cat 한글.txt')
            assert '한글.txt' in dosya_aktarımı_cxn.nlst()
            assert dict(dosya_aktarımı_cxn.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            doğrulama_Rapor['checks'].append('UTF-8 filename and content visible in guest shell')
            try: dosya_aktarımı_cxn.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            sonuç = bytearray(); dosya_aktarımı_cxn.retrbinary('RETR binary.dat', sonuç.extend); assert sonuç == yük_veri
            doğrulama_Rapor['checks'].append('oversized replacement rejected; previous file preserved')
            with dosya_aktarımı_cxn.transfercmd('STOR pending.txt') as yükle_Dosyalar:
                # A control command must not change the active upload's destination.
                assert dosya_aktarımı_cxn.size('binary.dat') == len(yük_veri)
                yükle_Dosyalar.sendall(b'UPLOAD TARGET PRESERVED')
            assert dosya_aktarımı_cxn.voidresp().startswith('226')
            sonuç = bytearray(); dosya_aktarımı_cxn.retrbinary('RETR pending.txt', sonuç.extend)
            assert sonuç == b'UPLOAD TARGET PRESERVED'
            sonuç = bytearray(); dosya_aktarımı_cxn.retrbinary('RETR binary.dat', sonuç.extend)
            assert sonuç == yük_veri
            dosya_aktarımı_cxn.delete('pending.txt')
            doğrulama_Rapor['checks'].append('interleaved SIZE cannot change the active STOR destination')
            dosya_aktarımı_cxn.storbinary('STOR 인사.jar', io.BytesIO(Arşiv.getvalue()))
            metin = kabuk('java -jar 인사.jar 누리')
            assert 'JAR yürütmek_komut: 누리' in metin and 'Öz çekirdek_değer dosya' in metin and 'exit 0' in metin, metin
            metin = kabuk('./인사.jar 세상')
            assert 'JAR yürütmek_komut: 세상' in metin and 'exit 0' in metin, metin
            doğrulama_Rapor['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <Dosya_ABI.h>\nstruct veri { int 수; double 비율; };\nint SUM_değer(int n) { return n ? n + SUM_değer(n-1) : 0; }\nint main(void) { struct veri değer = {SUM_değer(10), 1.25}; if (değer.수 != 55 || değer.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = açık_Dosya("cc.txt", R_W | 없으면만들기 | kesmek_içindekiler, 0600); if (문서 < 0) return 1; yazma_Dosya_veri(문서, 인사, sizeof(인사)-1); Kapat_Dosya(문서); yazma_Dosya_veri(1, 인사, sizeof(인사)-1); return 0; }\n'
            dosya_aktarımı_cxn.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            metin = kabuk('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in metin and 'exit 0' in metin, metin
            metin = kabuk('run 한글.elf'); assert 'CC NATIVE PASS' in metin and 'exit 0' in metin, metin
            assert 'CC NATIVE PASS' in kabuk('cat cc.txt')
            çalıştırılabilir = bytearray(); dosya_aktarımı_cxn.retrbinary('RETR 한글.elf', çalıştırılabilir.extend)
            assert çalıştırılabilir[:4] == b'\x7fELF' and çalıştırılabilir[18:20] == b'\xb7\x00'
            dosya_aktarımı_cxn.storbinary('STOR örnek_değer.elf', io.BytesIO(çalıştırılabilir)); metin = kabuk('run örnek_değer.elf'); assert 'CC NATIVE PASS' in metin and 'exit 0' in metin, metin
            dosya_aktarımı_cxn.storbinary('STOR yürütmek_komut', io.BytesIO(çalıştırılabilir)); metin=kabuk('./yürütmek_komut');assert 'CC NATIVE PASS' in metin and 'exit 0' in metin,metin
            dosya_aktarımı_cxn.storbinary('STOR İsim.txt', io.BytesIO(çalıştırılabilir)); metin=kabuk('./İsim.txt');assert 'CC NATIVE PASS' in metin and 'exit 0' in metin,metin
            kabuk('rm yürütmek_komut İsim.txt')
            doğrulama_Rapor['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            kabuk('rm binary.dat 한글.txt 한글.c 한글.elf örnek_değer.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_veri/'linux-reference')
            dosya_aktarımı_cxn.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            metin=kabuk('./리눅스인사');assert 'exit -8' in metin,metin
            metin=kabuk('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in metin,metin
            assert 'LINUX ELF FILE IO' in kabuk('cat linux.txt')
            dosya_aktarımı_cxn.delete('리눅스인사');dosya_aktarımı_cxn.delete('linux.txt')
            dosya_aktarımı_cxn.storbinary('STOR YANLIŞ_değer.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in kabuk('./YANLIŞ_değer.elf');dosya_aktarımı_cxn.delete('YANLIŞ_değer.elf')
            doğrulama_Rapor['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with yankı_düzen() as yankı_sunucu_girdi:
                NET_kaynak = KR_veri/'dış_iletişim.java'
                NET_kaynak.write_text('''import java.net.*; import java.io.*;
public class dış_iletişim { public static void main(String[] args) throws Exception {
 Socket Bağlan = Türkçe.Öz.cxn_taşıma.Bağlan("10.0.2.2", Integer.parseInt(args[0]));
 Bağlan.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] kaynakKod = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<kaynakKod.length;i++) if (Bağlan.getInputStream().read() != (kaynakKod[i]&255)) throw new RuntimeException("TCP mismatch");
 Bağlan.close();
 DatagramSocket uç_nokta = Türkçe.Öz.iletişim.Aç(0); Türkçe.Öz.iletişim.ZAMANAŞIMI(uç_nokta, 500);
 Türkçe.Öz.iletişim.göndermek(uç_nokta, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Türkçe.Öz.iletişim.almak(uç_nokta).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 uç_nokta.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(işlem_kök/'build/java-library/classes'),'-d',str(KR_veri),str(NET_kaynak)])
                dosya_aktarımı_cxn.storbinary('STOR dış_iletişim.class', io.BytesIO((KR_veri/'dış_iletişim.class').read_bytes()))
                metin = kabuk('java dış_iletişim {} {}'.format(yankı_sunucu_girdi.TCP_bağlantı_noktası, yankı_sunucu_girdi.UDP_taşımak))
                assert 'EXTERNAL TCP UDP PASS' in metin and '10.0.2.2' in metin and 'exit 0' in metin, metin
                assert yankı_sunucu_girdi.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, yankı_sunucu_girdi.수신됨
                assert not yankı_sunucu_girdi.오류들, yankı_sunucu_girdi.오류들
            doğrulama_Rapor['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            dosya_aktarımı_cxn.delete('dış_iletişim.class')
            sunucu_kaynak=KR_veri/'sunucu_test.java'
            sunucu_kaynak.write_text('''import java.net.*; public class sunucu_test {
 public static void main(String[] args) throws Exception {
  ServerSocket sunucu_değer = new ServerSocket(9300); DatagramSocket uç_nokta = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket konuk_değer = sunucu_değer.accept();
  konuk_değer.getOutputStream().write(konuk_değer.getInputStream().read()+1); konuk_değer.close(); sunucu_değer.close();
  byte[] içerik_değer = new byte[8]; DatagramPacket veri_birimi = new DatagramPacket(içerik_değer, içerik_değer.length); uç_nokta.receive(veri_birimi);
  uç_nokta.send(veri_birimi); uç_nokta.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_veri),str(sunucu_kaynak)])
            dosya_aktarımı_cxn.storbinary('STOR sunucu_test.class',io.BytesIO((KR_veri/'sunucu_test.class').read_bytes()))
            Süreç.stdin.write('java sunucu_test\n'.encode());Süreç.stdin.flush();almak_belge(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',sunucu_akış_taşımak),timeout=5) as eş_değer:
                eş_değer.sendall(b'A');assert eş_değer.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as eş_değer:
                eş_değer.settimeout(5);eş_değer.sendto(b'UDP-IN',('127.0.0.1',sunucu_veri_birimi_taşımak));assert eş_değer.recvfrom(512)[0]==b'UDP-IN'
            metin=almak_belge();assert 'INBOUND TCP UDP PASS' in metin and 'exit 0' in metin,metin
            doğrulama_Rapor['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            dosya_aktarımı_cxn.delete('sunucu_test.class')
            명령열 = 'public class 빛 { public static void main(String[] bağımsız_değişkenler) throws Exception { int SUM_değer = 0; int 수 = 1; while (수 <= 10) { SUM_değer = SUM_değer + 수; 수 = 수 + 1; } Türkçe.Öz.metinÇıktısı.수쓰기(SUM_değer); Türkçe.Öz.dosya.Yazma("aot.txt", "한글 AOT dosya 😀"); Türkçe.Öz.metinÇıktısı.yazma_hat(Türkçe.Öz.dosya.Okuma("aot.txt")); } }'
            dosya_aktarımı_cxn.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            metin = kabuk('javac 빛.java'); assert 'exit 0' in metin and 'Compiled:' in metin, metin
            metin = kabuk('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in metin and 'exit 0' in metin, metin
            metin = kabuk('run 빛.elf'); assert '\n55\n' in metin and '한글 AOT dosya 😀' in metin and 'exit 0' in metin, metin
            yerel_fd019377 = bytearray(); dosya_aktarımı_cxn.retrbinary('RETR 빛.elf', yerel_fd019377.extend)
            metin = kabuk('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in metin and 'unsupported' in metin, metin
            보존자료 = bytearray(); dosya_aktarımı_cxn.retrbinary('RETR 빛.elf', 보존자료.extend); assert yerel_fd019377 == 보존자료
            바이트코드 = bytearray(); dosya_aktarımı_cxn.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            dosya_aktarımı_cxn.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            metin = kabuk('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in metin and 'exit 0' in metin, metin
            metin = kabuk('run 빛.elf'); assert '\n55\n' in metin and '한글 AOT dosya 😀' in metin and 'exit 0' in metin, metin
            doğrulama_Rapor['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            doğrulama_Rapor['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statik_kaynak=KR_veri/'statik_test.java'
            statik_kaynak.write_text('''public class statik_test {
 static int işlem_kök = 3;
 static int SUM_değer(int n) { return n == 0 ? 0 : n + SUM_değer(n-1); }
 public static void main(String[] bağımsız_değişkenler) {
  int[] değer = new int[] {işlem_kök, SUM_değer(10)};
  System.out.println(değer[0] + değer[1]); System.out.println(bağımsız_değişkenler[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_veri),str(statik_kaynak)])
            dosya_aktarımı_cxn.storbinary('STOR statik_test.class',io.BytesIO((KR_veri/'statik_test.class').read_bytes()))
            metin=kabuk('jaot statik_test.class -o statik_test.elf');assert 'exit 0' in metin,metin
            metin=kabuk('run statik_test.elf 한글인수');assert '\n58\n한글인수\nexit 0' in metin,metin
            dosya_aktarımı_cxn.delete('statik_test.class');dosya_aktarımı_cxn.delete('statik_test.elf')
            doğrulama_Rapor['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arşiv.getvalue());손상자료[14]^=1
            dosya_aktarımı_cxn.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            metin=kabuk('java -jar 인사.jar');assert 'Main-Class\nexit 1' in metin,metin
            doğrulama_Rapor['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            dosya_aktarımı_cxn.quit(); assert 'FTP stopped' in kabuk('ftpd stop')
            assert not köprü.hata, köprü.hata
            doğrulama_Rapor.update(passed=True, frames_to_guest=köprü.커널수신틀수, frames_from_guest=köprü.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in seçici.select(0):
                parça_değer=누름값.fileobj.read(65536)
                if parça_değer: döküm.extend(parça_değer)
            köprü.Duraklat_olay.set()
            Süreç.terminate()
            try: Süreç.wait(timeout=5)
            except subprocess.TimeoutExpired: Süreç.kill(); Süreç.wait()
            seçici.close(); Süreç.stdin.close(); Süreç.stdout.close()
            doğrulama_Rapor['bridge_error'] = köprü.hata
            doğrulama_Rapor['frames_to_guest'] = köprü.커널수신틀수; doğrulama_Rapor['frames_from_guest'] = köprü.커널발신틀수
            (KR_veri/'packets.json').write_text(json.dumps(köprü.izleme_günlüğü,indent=2)+'\n')
            (KR_veri / 'serial.log').write_bytes(döküm)
            (KR_veri / 'report.json').write_text(json.dumps(doğrulama_Rapor, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': çalıştır()
