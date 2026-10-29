#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ukwenza_umyalelo, ukungaphumeleli_ixabiso/isixhobo_sekhompyutha_ixabiso 경계 시험."""
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
from 사용자통신시험 import enembonakalo_yenyani_umatshini, 위치


def hlela_ixabiso(umatshini, Igama, Isiqulatho_ixabiso, Store_ixabiso=True):
    Phumeza = len(umatshini.ilog_umqolo)
    umatshini.직렬.sendall(('edit ' + Igama + '\n').encode())
    umatshini.기다림('...> ', Phumeza)
    for umgca in Isiqulatho_ixabiso.splitlines():
        assert len(umgca) <= 128
        Phumeza = len(umatshini.ilog_umqolo)
        umatshini.직렬.sendall((umgca + '\n').encode())
        umatshini.기다림('...> ', Phumeza)
    Phumeza = len(umatshini.ilog_umqolo)
    umatshini.직렬.sendall(b'.save\n' if Store_ixabiso else b'.cancel\n')
    결과 = umatshini.기다림('jkoros> ', Phumeza)
    assert ('Saved:' if Store_ixabiso else 'Cancelled; original preserved') in 결과, 결과


def ifayile_idilesi():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for umgca in 결과.splitlines():
        if umgca.endswith(' ram_files'):
            return int(umgca.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def undwendwe_ifayile(umatshini, isithuba_ixabiso, Ubukhulu, INDLELA):
    # 시험 VM의 메모리에서 eyona_yenzekileyo_iingcombolo 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    idilesi = ifayile_idilesi() + isithuba_ixabiso * 16384
    umatshini.imonitha_ixabiso.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(idilesi, Ubukhulu, INDLELA)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if INDLELA.exists() and INDLELA.stat().st_size == Ubukhulu:
            return INDLELA.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    umatshini = enembonakalo_yenyani_umatshini(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Inethiwekhi_ixabiso=False)
    결과 = {}
    try:
        umatshini.Umyalelo('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        umatshini.Umyalelo('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        umatshini.Umyalelo('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        umatshini.Umyalelo('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        umatshini.Umyalelo('java Missing', ['cannot read class: -2', 'Exit: 1'])
        umatshini.Umyalelo('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        umatshini.Umyalelo('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Isiqulatho_ixabiso = '''public class Calc {
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
        hlela_ixabiso(umatshini, 'Calc.java', Isiqulatho_ixabiso)
        umatshini.Umyalelo('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = umatshini.Umyalelo('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        ufako_nkcukacha_uludwe = umatshini.Umyalelo('ls', ['Calc.class'])
        Ubukhulu = int(re.search(r'Calc\.class\s+(\d+) bytes', ufako_nkcukacha_uludwe).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as isalathisi_ixabiso_e5561a2b:
            INDLELA = Path(isalathisi_ixabiso_e5561a2b) / 'Calc.class'
            iingcombolo = undwendwe_ifayile(umatshini, 3, Ubukhulu, INDLELA)
            eyona_yenzekileyo_iingcombolo = subprocess.check_output(['java', '-Xverify:all', '-cp', isalathisi_ixabiso_e5561a2b, 'Calc', '6', 'guest'], universal_newlines=True)
            assert eyona_yenzekileyo_iingcombolo.splitlines() == 기대, eyona_yenzekileyo_iingcombolo
            결과['class_sha256'] = hashlib.sha256(iingcombolo).hexdigest()
            결과['openjdk_output'] = eyona_yenzekileyo_iingcombolo
        # 실패한 hlela_ixabiso/컴파일은 기존 class를 보존한다.
        hlela_ixabiso(umatshini, 'Calc.java', 'not Java at all', Store_ixabiso=False)
        umatshini.Umyalelo('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for 잘못 in [
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
            hlela_ixabiso(umatshini, 'Calc.java', 잘못)
            umatshini.Umyalelo('javac Calc.java', ['javac error:', 'Exit: 1'])
            umatshini.Umyalelo('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # uniko_lomyalelo_omnye_ixabiso 실행은 umsebenzisi 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            umatshini.Umyalelo('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        umatshini.Umyalelo('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        umatshini.Umyalelo('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        hlela_ixabiso(umatshini, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        umatshini.Umyalelo('javac Calc.java', ['Compiled:', 'Exit: 0'])
        umatshini.Umyalelo('java Calc', ['instruction limit', 'Exit: 1'])
        umatshini.Umyalelo('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        hlela_ixabiso(umatshini, 'Bad.class', 'garbage')
        umatshini.Umyalelo('java Bad', ['JVM error:', 'Exit: 1'])
        umatshini.Umyalelo('rm Bad.class', ['Removed'])
        umatshini.Umyalelo('java Bad', ['cannot read class: -2'])
        # hlela_ixabiso 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Phumeza = len(umatshini.ilog_umqolo)
        umatshini.직렬.sendall(b'edit Hello.java\n')
        umatshini.기다림('...> ', Phumeza)
        Phumeza = len(umatshini.ilog_umqolo)
        umatshini.직렬.sendall(b'x' * 129 + b'\n')
        umatshini.기다림('...> ', Phumeza)
        umatshini.Umyalelo('.save', ['Too much input; original preserved'])
        umatshini.Umyalelo('javac Hello.java', ['Compiled:', 'Exit: 0'])
        hlela_ixabiso(umatshini, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            hlela_ixabiso(umatshini, 'f' + str(수), 'occupied')
        umatshini.Umyalelo('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        umatshini.Umyalelo('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in umatshini.ilog_umqolo.decode('utf-8', 'replace')
        결과['serial'] = umatshini.ilog_umqolo.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        umatshini.Vala()


def 주코드(iingcombolo):
    """손상 시험용 main Code의 eyona_yenzekileyo_iingcombolo iFayili 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        ixabiso = struct.unpack_from('>H', iingcombolo, 위치값)[0]
        위치값 += 2
        return ixabiso
    def 정():
        nonlocal 위치값
        ixabiso = struct.unpack_from('>I', iingcombolo, 위치값)[0]
        위치값 += 4
        return ixabiso
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = iingcombolo[위치값]
        위치값 += 1
        if 종류 == 1:
            ubude_ixabiso = 짧()
            문자들[수] = iingcombolo[위치값:위치값 + ubude_ixabiso]
            위치값 += ubude_ixabiso
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Igama = 짧()
        짧()
        for 수 in range(짧()):
            uphawu_ixabiso = 짧()
            Ubukhulu = 정()
            if 문자들[Igama] == b'main' and 문자들[uphawu_ixabiso] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', iingcombolo, 위치값 + 4)[0]
            위치값 += Ubukhulu
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        isalathisi_ixabiso_e5561a2b = Path(임시)
        (isalathisi_ixabiso_e5561a2b / 'build').mkdir()
        UMTHOMBO = isalathisi_ixabiso_e5561a2b / 'Imported.java'
        UMTHOMBO.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(UMTHOMBO)], check=True)
        원본 = (isalathisi_ixabiso_e5561a2b / 'Imported.class').read_bytes()
        코드, ubude_ixabiso = 주코드(원본)
        변형 = {}
        iingcombolo = bytearray(원본); iingcombolo[0] = 0; 변형['BadMagic'] = iingcombolo
        iingcombolo = bytearray(원본); iingcombolo[7] = 61; 변형['BadVer'] = iingcombolo
        iingcombolo = bytearray(원본); iingcombolo[8:10] = b'\xff\xff'; 변형['BadPool'] = iingcombolo
        iingcombolo = bytearray(원본); iingcombolo[코드:코드 + ubude_ixabiso] = bytes(ubude_ixabiso)
        iingcombolo[코드:코드 + 3] = b'\xa7\x00\x01'; iingcombolo[코드 + ubude_ixabiso - 1] = 177; 변형['BadJump'] = iingcombolo
        iingcombolo = bytearray(원본); iingcombolo[코드:코드 + ubude_ixabiso] = bytes(ubude_ixabiso)
        iingcombolo[코드] = 87; iingcombolo[코드 + ubude_ixabiso - 1] = 177; 변형['BadStack'] = iingcombolo
        # Igama 검사를 통과시켜 eyona_yenzekileyo_iingcombolo ukwenza_umyalelo 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ufako_nkcukacha_ixabiso = ['Imported.class=' + str(isalathisi_ixabiso_e5561a2b / 'Imported.class'), 'Imported.java=' + str(UMTHOMBO)]
        for Igama, iingcombolo in 변형.items():
            INDLELA = isalathisi_ixabiso_e5561a2b / (Igama + '.class'); INDLELA.write_bytes(iingcombolo)
            ufako_nkcukacha_ixabiso.append(Igama + '.class=' + str(INDLELA))
        iqela_ixabiso = isalathisi_ixabiso_e5561a2b / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'Izixhobo/자바파일묶기.py'), '-o', str(iqela_ixabiso)] + ufako_nkcukacha_ixabiso, check=True)
        subprocess.run(['as', '--32', '-o', str(isalathisi_ixabiso_e5561a2b / 'user.o'), str(위치 / '부팅/umsebenzisi.s')], cwd=str(isalathisi_ixabiso_e5561a2b), check=True)
        ikheneli_ixabiso = isalathisi_ixabiso_e5561a2b / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Ilinki_ubume.ld'), '-o', str(ikheneli_ixabiso),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(isalathisi_ixabiso_e5561a2b / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        umatshini = enembonakalo_yenyani_umatshini(ikheneli_ixabiso, Inethiwekhi_ixabiso=False)
        try:
            umatshini.Umyalelo('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            umatshini.Umyalelo('cat Imported.java', ['int[] values = new int[3]'])
            for Igama, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                umatshini.Umyalelo('java ' + Igama, [문구, 'Exit: 1'])
                umatshini.Umyalelo('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return umatshini.ilog_umqolo.decode('utf-8', 'replace')
        finally:
            umatshini.Vala()


if __name__ == '__main__':
    ingcaciso_yegama_ixabiso = argparse.ArgumentParser()
    ingcaciso_yegama_ixabiso.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = ingcaciso_yegama_ixabiso.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
