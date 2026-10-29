#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 tekeleza_amri, kushindwa_thamani/rasilimali_thamani 경계 시험."""
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
from 사용자통신시험 import pepe_mashine, 위치


def hariri_thamani(mashine, Jina, maudhui_thamani, Store_thamani=True):
    endesha = len(mashine.batli_REKODI)
    mashine.직렬.sendall(('edit ' + Jina + '\n').encode())
    mashine.subiri_hali('...> ', endesha)
    for laini in maudhui_thamani.splitlines():
        assert len(laini) <= 128
        endesha = len(mashine.batli_REKODI)
        mashine.직렬.sendall((laini + '\n').encode())
        mashine.subiri_hali('...> ', endesha)
    endesha = len(mashine.batli_REKODI)
    mashine.직렬.sendall(b'.save\n' if Store_thamani else b'.cancel\n')
    결과 = mashine.subiri_hali('jkoros> ', endesha)
    assert ('Saved:' if Store_thamani else 'Cancelled; original preserved') in 결과, 결과


def faili_anwani():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for laini in 결과.splitlines():
        if laini.endswith(' ram_files'):
            return int(laini.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def mgeni_faili(mashine, Sloti_thamani, panga_ukubwa, njia):
    # 시험 VM의 메모리에서 halisi_data 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    anwani = faili_anwani() + Sloti_thamani * 16384
    mashine.monita_thamani.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(anwani, panga_ukubwa, njia)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if njia.exists() and njia.stat().st_size == panga_ukubwa:
            return njia.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    mashine = pepe_mashine(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Mtandao_thamani=False)
    결과 = {}
    try:
        mashine.amri('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        mashine.amri('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        mashine.amri('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        mashine.amri('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        mashine.amri('java Missing', ['cannot read class: -2', 'Exit: 1'])
        mashine.amri('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        mashine.amri('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        maudhui_thamani = '''public class Calc {
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
        hariri_thamani(mashine, 'Calc.java', maudhui_thamani)
        mashine.amri('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = mashine.amri('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        ingizo_Orodha = mashine.amri('ls', ['Calc.class'])
        panga_ukubwa = int(re.search(r'Calc\.class\s+(\d+) bytes', ingizo_Orodha).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Saraka_thamani:
            njia = Path(Saraka_thamani) / 'Calc.class'
            data = mgeni_faili(mashine, 3, panga_ukubwa, njia)
            halisi_data = subprocess.check_output(['java', '-Xverify:all', '-cp', Saraka_thamani, 'Calc', '6', 'guest'], universal_newlines=True)
            assert halisi_data.splitlines() == 기대, halisi_data
            결과['class_sha256'] = hashlib.sha256(data).hexdigest()
            결과['openjdk_output'] = halisi_data
        # 실패한 hariri_thamani/컴파일은 기존 class를 보존한다.
        hariri_thamani(mashine, 'Calc.java', 'not Java at all', Store_thamani=False)
        mashine.amri('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            hariri_thamani(mashine, 'Calc.java', 잘못)
            mashine.amri('javac Calc.java', ['javac error:', 'Exit: 1'])
            mashine.amri('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_thamani 실행은 mtumiaji 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            mashine.amri('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        mashine.amri('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        mashine.amri('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        hariri_thamani(mashine, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        mashine.amri('javac Calc.java', ['Compiled:', 'Exit: 0'])
        mashine.amri('java Calc', ['instruction limit', 'Exit: 1'])
        mashine.amri('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        hariri_thamani(mashine, 'Bad.class', 'garbage')
        mashine.amri('java Bad', ['JVM error:', 'Exit: 1'])
        mashine.amri('rm Bad.class', ['Removed'])
        mashine.amri('java Bad', ['cannot read class: -2'])
        # hariri_thamani 입력의 넘친 부분을 잘라서 저장하지 않는다.
        endesha = len(mashine.batli_REKODI)
        mashine.직렬.sendall(b'edit Hello.java\n')
        mashine.subiri_hali('...> ', endesha)
        endesha = len(mashine.batli_REKODI)
        mashine.직렬.sendall(b'x' * 129 + b'\n')
        mashine.subiri_hali('...> ', endesha)
        mashine.amri('.save', ['Too much input; original preserved'])
        mashine.amri('javac Hello.java', ['Compiled:', 'Exit: 0'])
        hariri_thamani(mashine, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            hariri_thamani(mashine, 'f' + str(수), 'occupied')
        mashine.amri('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        mashine.amri('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in mashine.batli_REKODI.decode('utf-8', 'replace')
        결과['serial'] = mashine.batli_REKODI.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        mashine.funga()


def 주코드(data):
    """손상 시험용 main Code의 halisi_data faili 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        thamani = struct.unpack_from('>H', data, 위치값)[0]
        위치값 += 2
        return thamani
    def 정():
        nonlocal 위치값
        thamani = struct.unpack_from('>I', data, 위치값)[0]
        위치값 += 4
        return thamani
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = data[위치값]
        위치값 += 1
        if 종류 == 1:
            urefu_thamani = 짧()
            문자들[수] = data[위치값:위치값 + urefu_thamani]
            위치값 += urefu_thamani
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Jina = 짧()
        짧()
        for 수 in range(짧()):
            sifa_thamani = 짧()
            panga_ukubwa = 정()
            if 문자들[Jina] == b'main' and 문자들[sifa_thamani] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', data, 위치값 + 4)[0]
            위치값 += panga_ukubwa
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Saraka_thamani = Path(임시)
        (Saraka_thamani / 'build').mkdir()
        chanzo = Saraka_thamani / 'Imported.java'
        chanzo.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(chanzo)], check=True)
        원본 = (Saraka_thamani / 'Imported.class').read_bytes()
        msimbo_thamani, urefu_thamani = 주코드(원본)
        변형 = {}
        data = bytearray(원본); data[0] = 0; 변형['BadMagic'] = data
        data = bytearray(원본); data[7] = 61; 변형['BadVer'] = data
        data = bytearray(원본); data[8:10] = b'\xff\xff'; 변형['BadPool'] = data
        data = bytearray(원본); data[msimbo_thamani:msimbo_thamani + urefu_thamani] = bytes(urefu_thamani)
        data[msimbo_thamani:msimbo_thamani + 3] = b'\xa7\x00\x01'; data[msimbo_thamani + urefu_thamani - 1] = 177; 변형['BadJump'] = data
        data = bytearray(원본); data[msimbo_thamani:msimbo_thamani + urefu_thamani] = bytes(urefu_thamani)
        data[msimbo_thamani] = 87; data[msimbo_thamani + urefu_thamani - 1] = 177; 변형['BadStack'] = data
        # Jina 검사를 통과시켜 halisi_data tekeleza_amri 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ingizo_thamani = ['Imported.class=' + str(Saraka_thamani / 'Imported.class'), 'Imported.java=' + str(chanzo)]
        for Jina, data in 변형.items():
            njia = Saraka_thamani / (Jina + '.class'); njia.write_bytes(data)
            ingizo_thamani.append(Jina + '.class=' + str(njia))
        Kikundi_thamani = Saraka_thamani / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'Zana/자바파일묶기.py'), '-o', str(Kikundi_thamani)] + ingizo_thamani, check=True)
        subprocess.run(['as', '--32', '-o', str(Saraka_thamani / 'user.o'), str(위치 / '부팅/mtumiaji.s')], cwd=str(Saraka_thamani), check=True)
        kiini_thamani_0611a8a8 = Saraka_thamani / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Kiungo_Muundo.ld'), '-o', str(kiini_thamani_0611a8a8),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(Saraka_thamani / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        mashine = pepe_mashine(kiini_thamani_0611a8a8, Mtandao_thamani=False)
        try:
            mashine.amri('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            mashine.amri('cat Imported.java', ['int[] values = new int[3]'])
            for Jina, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                mashine.amri('java ' + Jina, [문구, 'Exit: 1'])
                mashine.amri('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return mashine.batli_REKODI.decode('utf-8', 'replace')
        finally:
            mashine.funga()


if __name__ == '__main__':
    changanua_thamani = argparse.ArgumentParser()
    changanua_thamani.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = changanua_thamani.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
