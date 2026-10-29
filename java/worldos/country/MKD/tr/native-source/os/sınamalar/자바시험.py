#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 yürütmek_komut, hata_değer/kaynak_değer sınır_değer sınamalar."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import time
from test_kullanıcı_ağ import VM, konum


def Düzenle_değer(makine, İsim, içerik_değer, depo_değer=True):
    çalıştır = len(makine.LOG_KAYIT)
    makine.직렬.sendall(('edit ' + İsim + '\n').encode())
    makine.bekleme_durumu('...> ', çalıştır)
    for girdi_satırı in içerik_değer.splitlines():
        assert len(girdi_satırı) <= 128
        çalıştır = len(makine.LOG_KAYIT)
        makine.직렬.sendall((girdi_satırı + '\n').encode())
        makine.bekleme_durumu('...> ', çalıştır)
    çalıştır = len(makine.LOG_KAYIT)
    makine.직렬.sendall(b'.save\n' if depo_değer else b'.cancel\n')
    sonuç = makine.bekleme_durumu('jkoros> ', çalıştır)
    assert ('Saved:' if depo_değer else 'Cancelled; original preserved') in sonuç, sonuç


def Dosya_ADRES():
    sonuç = subprocess.check_output(['nm', '-n', str(konum / 'build/kernel.elf')], universal_newlines=True)
    for girdi_satırı in sonuç.splitlines():
        if girdi_satırı.endswith(' ram_files'):
            return int(girdi_satırı.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def konuk_Dosya(makine, yuva_değer_ff41a4f1, Boyut, yol):
    # sınamalar VM의 메모리에서 fiili_veri 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ADRES = Dosya_ADRES() + yuva_değer_ff41a4f1 * 16384
    makine.izlemek_değer.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ADRES, Boyut, yol)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if yol.exists() and yol.stat().st_size == Boyut:
            return yol.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def test_çalıştırması(Tip_değer):
    makine = VM(konum / ('build/kernel.elf' if Tip_değer == 'elf' else 'build/kernel.iso'), Tip_değer, ağ_değer=False)
    sonuç = {}
    try:
        makine.komut('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        makine.komut('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        makine.komut('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        makine.komut('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        makine.komut('java Missing', ['cannot read class: -2', 'Exit: 1'])
        makine.komut('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        makine.komut('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        içerik_değer = '''public class Calc {
 public static int fact(int n) {
  if (n <= 1) { return 1; } else { return n * fact(n - 1); }
 }
 public static boolean check(int n) { return n == 7; }
 public static void main(String[] args) {
  int n = Integer.parseInt(args[0]);
  System.out.println(fact(n));
  int sum = 0;
  for (int i = 1; i <= n; i++) { sum = sum + i; }
  while (n > 0) { n--; }
  System.out.println(sum);
  System.out.println(n);
  System.out.println(check(7) && false || true);
  System.out.println(false && 1 / 0 == 0);
  System.out.println(true || 1 / 0 == 0);
  System.out.println(-2147483648 / -1);
  System.out.println(args[1]);
  System.out.println(args[1].length());
  System.out.println(args.length);
  String label = "sum=";
  label += sum;
  System.out.println(label);
  System.out.println(12 + "x" + false);
  System.out.println("logic=" + (true && check(7)));
  char letter = 'a';
  letter++;
  System.out.println(letter);
  System.out.println("letter=" + letter);
  int extra = 7;
  extra *= 3;
  extra -= 1;
  System.out.println(extra);
 }
}'''
        Düzenle_değer(makine, 'Calc.java', içerik_değer)
        makine.komut('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        metinÇıktısı = makine.komut('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        sonuç['guest_output'] = metinÇıktısı
        girdi_Liste = makine.komut('ls', ['Calc.class'])
        Boyut = int(re.search(r'Calc\.class\s+(\d+) bytes', girdi_Liste).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as dizin_değer:
            yol = Path(dizin_değer) / 'Calc.class'
            veri = konuk_Dosya(makine, 3, Boyut, yol)
            fiili_veri = subprocess.check_output(['java', '-Xverify:all', '-cp', dizin_değer, 'Calc', '6', 'guest'], universal_newlines=True)
            assert fiili_veri.splitlines() == 기대, fiili_veri
            sonuç['class_sha256'] = hashlib.sha256(veri).hexdigest()
            sonuç['openjdk_output'] = fiili_veri
        # 실패한 Düzenle_değer/컴파일은 기존 class를 보존한다.
        Düzenle_değer(makine, 'Calc.java', 'not Java at all', depo_değer=False)
        makine.komut('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for geçersiz_KR in [
            'public class Calc { public static void main(String[] args) { int x = ; } }',
            'public class Calc { public static void main(String[] args) { int x = true; } }',
            'public class Calc { public static void main(String[] args) { int x = 2147483648; } }',
            'public class Calc { public static int f() { int x = 1; } }',
            'public class Calc { public static void main(String[] args) { Object x = new Object(); } }',
            'public class Other { public static void main(String[] args) {} }',
            'public class Calc { public static void main(String[] args) { int while = 3; } }',
            'public class Calc { public static void main(String[] args) { if (true) int x = 3; } }',
            'public class Calc { public static void main(String[] args) { int x = 010; } }',
        ]:
            Düzenle_değer(makine, 'Calc.java', geçersiz_KR)
            makine.komut('javac Calc.java', ['javac error:', 'Exit: 1'])
            makine.komut('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # öğe_değer_58902391 실행은 kullanıcı_alanı yığın_değer/프레임을 매번 초기화한다.
        for 수 in range(12):
            makine.komut('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        makine.komut('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        makine.komut('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Düzenle_değer(makine, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        makine.komut('javac Calc.java', ['Compiled:', 'Exit: 0'])
        makine.komut('java Calc', ['instruction limit', 'Exit: 1'])
        makine.komut('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Düzenle_değer(makine, 'Bad.class', 'garbage')
        makine.komut('java Bad', ['JVM error:', 'Exit: 1'])
        makine.komut('rm Bad.class', ['Removed'])
        makine.komut('java Bad', ['cannot read class: -2'])
        # Düzenle_değer 입력의 넘친 부분을 잘라서 저장하지 않는다.
        çalıştır = len(makine.LOG_KAYIT)
        makine.직렬.sendall(b'edit Hello.java\n')
        makine.bekleme_durumu('...> ', çalıştır)
        çalıştır = len(makine.LOG_KAYIT)
        makine.직렬.sendall(b'x' * 129 + b'\n')
        makine.bekleme_durumu('...> ', çalıştır)
        makine.komut('.save', ['Too much input; original preserved'])
        makine.komut('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Düzenle_değer(makine, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            Düzenle_değer(makine, 'f' + str(수), 'occupied')
        makine.komut('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        makine.komut('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in makine.LOG_KAYIT.decode('utf-8', 'replace')
        sonuç['serial'] = makine.LOG_KAYIT.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(Tip_değer))
        return sonuç
    finally:
        makine.Kapat()


def 주코드(veri):
    """손상 시험용 main Code의 fiili_veri dosya 오프셋/길이만 읽는다."""
    konum_değer = 8
    def 짧():
        nonlocal konum_değer
        değer = struct.unpack_from('>H', veri, konum_değer)[0]
        konum_değer += 2
        return değer
    def 정():
        nonlocal konum_değer
        değer = struct.unpack_from('>I', veri, konum_değer)[0]
        konum_değer += 4
        return değer
    문자들 = {}
    for 수 in range(1, 짧()):
        Tip_değer = veri[konum_değer]
        konum_değer += 1
        if Tip_değer == 1:
            süre_değer = 짧()
            문자들[수] = veri[konum_değer:konum_değer + süre_değer]
            konum_değer += süre_değer
        elif Tip_değer in (7, 8): konum_değer += 2
        elif Tip_değer in (3, 9, 10, 12): konum_değer += 4
        else: raise AssertionError(Tip_değer)
    konum_değer += 6
    öğe_BAĞ_DEĞ_SAY = 짧()
    konum_değer += öğe_BAĞ_DEĞ_SAY * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        İsim = 짧()
        짧()
        for 수 in range(짧()):
            öznitelik_değer = 짧()
            Boyut = 정()
            if 문자들[İsim] == b'main' and 문자들[öznitelik_değer] == b'Code':
                return konum_değer + 8, struct.unpack_from('>I', veri, konum_değer + 4)[0]
            konum_değer += Boyut
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        dizin_değer = Path(임시)
        (dizin_değer / 'build').mkdir()
        kaynakKod = dizin_değer / 'Imported.java'
        kaynakKod.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(kaynakKod)], check=True)
        원본 = (dizin_değer / 'Imported.class').read_bytes()
        KOD_değer, süre_değer = 주코드(원본)
        çeşit_değer = {}
        veri = bytearray(원본); veri[0] = 0; çeşit_değer['BadMagic'] = veri
        veri = bytearray(원본); veri[7] = 61; çeşit_değer['BadVer'] = veri
        veri = bytearray(원본); veri[8:10] = b'\xff\xff'; çeşit_değer['BadPool'] = veri
        veri = bytearray(원본); veri[KOD_değer:KOD_değer + süre_değer] = bytes(süre_değer)
        veri[KOD_değer:KOD_değer + 3] = b'\xa7\x00\x01'; veri[KOD_değer + süre_değer - 1] = 177; çeşit_değer['BadJump'] = veri
        veri = bytearray(원본); veri[KOD_değer:KOD_değer + süre_değer] = bytes(süre_değer)
        veri[KOD_değer] = 87; veri[KOD_değer + süre_değer - 1] = 177; çeşit_değer['BadStack'] = veri
        # İsim 검사를 통과시켜 fiili_veri yürütmek_komut 중의 işlenen_Yığın 오류까지 검사한다.
        çeşit_değer['BadStack'] = çeşit_değer['BadStack'].replace(b'Imported', b'BadStack')
        girdi_değer = ['Imported.class=' + str(dizin_değer / 'Imported.class'), 'Imported.java=' + str(kaynakKod)]
        for İsim, veri in çeşit_değer.items():
            yol = dizin_değer / (İsim + '.class'); yol.write_bytes(veri)
            girdi_değer.append(İsim + '.class=' + str(yol))
        Grup_değer = dizin_değer / 'build/java-files.bin'
        subprocess.run([sys.executable, str(konum / 'araçlar/자바파일묶기.py'), '-o', str(Grup_değer)] + girdi_değer, check=True)
        subprocess.run(['as', '--32', '-o', str(dizin_değer / 'user.o'), str(konum / 'makine_başlatma/kullanıcı_alanı.s')], cwd=str(dizin_değer), check=True)
        çekirdek_değer = dizin_değer / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(konum / 'makine_başlatma/bağlama_düzeni.ld'), '-o', str(çekirdek_değer),
                        str(konum / 'build/boot.o'), str(konum / 'build/java.o'), str(dizin_değer / 'user.o'), str(konum / 'build/apps.o')], check=True)
        makine = VM(çekirdek_değer, ağ_değer=False)
        try:
            makine.komut('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            makine.komut('cat Imported.java', ['int[] values = new int[3]'])
            for İsim, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                makine.komut('java ' + İsim, [문구, 'Exit: 1'])
                makine.komut('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return makine.LOG_KAYIT.decode('utf-8', 'replace')
        finally:
            makine.Kapat()


if __name__ == '__main__':
    ayrıştırmak_değer = argparse.ArgumentParser()
    ayrıştırmak_değer.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    bağımsız_değişkenler = ayrıştırmak_değer.parse_args()
    sonuç = {Tip_değer: test_çalıştırması(Tip_değer) for Tip_değer in (('elf', 'iso') if bağımsız_değişkenler.boot == 'both' else (bağımsız_değişkenler.boot,))}
    sonuç['import'] = 적재시험()
    (konum / 'build/자바시험.json').write_text(json.dumps(sonuç, ensure_ascii=False, indent=2) + '\n')
