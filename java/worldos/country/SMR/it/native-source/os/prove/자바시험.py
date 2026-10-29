#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Esegui_comando, errore_VALORE/risorsa_VALORE limite_VALORE prove."""
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
from test_Usenet import VM, posizione


def Modifica_VALORE(computer, Nome, Contenuto_VALORE, Store_VALORE=True):
    avvia = len(computer.LOG_riga)
    computer.seriale_VALORE.sendall(('edit ' + Nome + '\n').encode())
    computer.stato_di_attesa('...> ', avvia)
    for riga_di_ingresso in Contenuto_VALORE.splitlines():
        assert len(riga_di_ingresso) <= 128
        avvia = len(computer.LOG_riga)
        computer.seriale_VALORE.sendall((riga_di_ingresso + '\n').encode())
        computer.stato_di_attesa('...> ', avvia)
    avvia = len(computer.LOG_riga)
    computer.seriale_VALORE.sendall(b'.save\n' if Store_VALORE else b'.cancel\n')
    risultato = computer.stato_di_attesa('jkoros> ', avvia)
    assert ('Saved:' if Store_VALORE else 'Cancelled; original preserved') in risultato, risultato


def File_e_mail():
    risultato = subprocess.check_output(['nm', '-n', str(posizione / 'build/kernel.elf')], universal_newlines=True)
    for riga_di_ingresso in risultato.splitlines():
        if riga_di_ingresso.endswith(' ram_files'):
            return int(riga_di_ingresso.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def guest_File(computer, slot_VALORE, Dimensione, percorso):
    # prove VM의 메모리에서 effettivo_dati 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    e_mail = File_e_mail() + slot_VALORE * 16384
    computer.monitor_VALORE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(e_mail, Dimensione, percorso)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if percorso.exists() and percorso.stat().st_size == Dimensione:
            return percorso.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def esecuzione_dei_test(Kind_VALORE):
    computer = VM(posizione / ('build/kernel.elf' if Kind_VALORE == 'elf' else 'build/kernel.iso'), Kind_VALORE, rete_VALORE=False)
    risultato = {}
    try:
        computer.comando('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        computer.comando('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        computer.comando('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        computer.comando('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        computer.comando('java Missing', ['cannot read class: -2', 'Exit: 1'])
        computer.comando('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        computer.comando('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Contenuto_VALORE = '''public class Calc {
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
        Modifica_VALORE(computer, 'Calc.java', Contenuto_VALORE)
        computer.comando('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        uscitaTesto = computer.comando('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        risultato['guest_output'] = uscitaTesto
        voce_elenco = computer.comando('ls', ['Calc.class'])
        Dimensione = int(re.search(r'Calc\.class\s+(\d+) bytes', voce_elenco).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as elenco_VALORE:
            percorso = Path(elenco_VALORE) / 'Calc.class'
            dati = guest_File(computer, 3, Dimensione, percorso)
            effettivo_dati = subprocess.check_output(['java', '-Xverify:all', '-cp', elenco_VALORE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert effettivo_dati.splitlines() == 기대, effettivo_dati
            risultato['class_sha256'] = hashlib.sha256(dati).hexdigest()
            risultato['openjdk_output'] = effettivo_dati
        # 실패한 Modifica_VALORE/컴파일은 기존 class를 보존한다.
        Modifica_VALORE(computer, 'Calc.java', 'not Java at all', Store_VALORE=False)
        computer.comando('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for non_valida_KR in [
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
            Modifica_VALORE(computer, 'Calc.java', non_valida_KR)
            computer.comando('javac Calc.java', ['javac error:', 'Exit: 1'])
            computer.comando('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_VALORE 실행은 spazio_utente heap_VALORE/프레임을 매번 초기화한다.
        for numero in range(12):
            computer.comando('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        computer.comando('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        computer.comando('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Modifica_VALORE(computer, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        computer.comando('javac Calc.java', ['Compiled:', 'Exit: 0'])
        computer.comando('java Calc', ['instruction limit', 'Exit: 1'])
        computer.comando('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Modifica_VALORE(computer, 'Bad.class', 'garbage')
        computer.comando('java Bad', ['JVM error:', 'Exit: 1'])
        computer.comando('rm Bad.class', ['Removed'])
        computer.comando('java Bad', ['cannot read class: -2'])
        # Modifica_VALORE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        avvia = len(computer.LOG_riga)
        computer.seriale_VALORE.sendall(b'edit Hello.java\n')
        computer.stato_di_attesa('...> ', avvia)
        avvia = len(computer.LOG_riga)
        computer.seriale_VALORE.sendall(b'x' * 129 + b'\n')
        computer.stato_di_attesa('...> ', avvia)
        computer.comando('.save', ['Too much input; original preserved'])
        computer.comando('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Modifica_VALORE(computer, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for numero in range(3):
            Modifica_VALORE(computer, 'f' + str(numero), 'occupied')
        computer.comando('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        computer.comando('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in computer.LOG_riga.decode('utf-8', 'replace')
        risultato['serial'] = computer.LOG_riga.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(Kind_VALORE))
        return risultato
    finally:
        computer.Chiudi()


def 주코드(dati):
    """손상 시험용 main Code의 effettivo_dati file 오프셋/길이만 읽는다."""
    funzione_VALORE = 8
    def 짧():
        nonlocal funzione_VALORE
        VALORE = struct.unpack_from('>H', dati, funzione_VALORE)[0]
        funzione_VALORE += 2
        return VALORE
    def 정():
        nonlocal funzione_VALORE
        VALORE = struct.unpack_from('>I', dati, funzione_VALORE)[0]
        funzione_VALORE += 4
        return VALORE
    문자들 = {}
    for numero in range(1, 짧()):
        Kind_VALORE = dati[funzione_VALORE]
        funzione_VALORE += 1
        if Kind_VALORE == 1:
            durata_VALORE = 짧()
            문자들[numero] = dati[funzione_VALORE:funzione_VALORE + durata_VALORE]
            funzione_VALORE += durata_VALORE
        elif Kind_VALORE in (7, 8): funzione_VALORE += 2
        elif Kind_VALORE in (3, 9, 10, 12): funzione_VALORE += 4
        else: raise AssertionError(Kind_VALORE)
    funzione_VALORE += 6
    articolo_CONTA_NUMERI = 짧()
    funzione_VALORE += articolo_CONTA_NUMERI * 2
    assert 짧() == 0
    for numero in range(짧()):
        짧()
        Nome = 짧()
        짧()
        for numero in range(짧()):
            valore_dell_attributo = 짧()
            Dimensione = 정()
            if 문자들[Nome] == b'main' and 문자들[valore_dell_attributo] == b'Code':
                return funzione_VALORE + 8, struct.unpack_from('>I', dati, funzione_VALORE + 4)[0]
            funzione_VALORE += Dimensione
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        elenco_VALORE = Path(임시)
        (elenco_VALORE / 'build').mkdir()
        codiceSorgente = elenco_VALORE / 'Imported.java'
        codiceSorgente.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(codiceSorgente)], check=True)
        원본 = (elenco_VALORE / 'Imported.class').read_bytes()
        CODICE_VALORE, durata_VALORE = 주코드(원본)
        variante_VALORE = {}
        dati = bytearray(원본); dati[0] = 0; variante_VALORE['BadMagic'] = dati
        dati = bytearray(원본); dati[7] = 61; variante_VALORE['BadVer'] = dati
        dati = bytearray(원본); dati[8:10] = b'\xff\xff'; variante_VALORE['BadPool'] = dati
        dati = bytearray(원본); dati[CODICE_VALORE:CODICE_VALORE + durata_VALORE] = bytes(durata_VALORE)
        dati[CODICE_VALORE:CODICE_VALORE + 3] = b'\xa7\x00\x01'; dati[CODICE_VALORE + durata_VALORE - 1] = 177; variante_VALORE['BadJump'] = dati
        dati = bytearray(원본); dati[CODICE_VALORE:CODICE_VALORE + durata_VALORE] = bytes(durata_VALORE)
        dati[CODICE_VALORE] = 87; dati[CODICE_VALORE + durata_VALORE - 1] = 177; variante_VALORE['BadStack'] = dati
        # Nome 검사를 통과시켜 effettivo_dati Esegui_comando 중의 operando_Pila 오류까지 검사한다.
        variante_VALORE['BadStack'] = variante_VALORE['BadStack'].replace(b'Imported', b'BadStack')
        voce_VALORE = ['Imported.class=' + str(elenco_VALORE / 'Imported.class'), 'Imported.java=' + str(codiceSorgente)]
        for Nome, dati in variante_VALORE.items():
            percorso = elenco_VALORE / (Nome + '.class'); percorso.write_bytes(dati)
            voce_VALORE.append(Nome + '.class=' + str(percorso))
        gruppo_VALORE = elenco_VALORE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(posizione / 'strumenti/자바파일묶기.py'), '-o', str(gruppo_VALORE)] + voce_VALORE, check=True)
        subprocess.run(['as', '--32', '-o', str(elenco_VALORE / 'user.o'), str(posizione / 'avvio_macchina/spazio_utente.s')], cwd=str(elenco_VALORE), check=True)
        kernel_VALORE = elenco_VALORE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(posizione / 'avvio_macchina/disposizione_di_collegamento.ld'), '-o', str(kernel_VALORE),
                        str(posizione / 'build/boot.o'), str(posizione / 'build/java.o'), str(elenco_VALORE / 'user.o'), str(posizione / 'build/apps.o')], check=True)
        computer = VM(kernel_VALORE, rete_VALORE=False)
        try:
            computer.comando('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            computer.comando('cat Imported.java', ['int[] values = new int[3]'])
            for Nome, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                computer.comando('java ' + Nome, [문구, 'Exit: 1'])
                computer.comando('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return computer.LOG_riga.decode('utf-8', 'replace')
        finally:
            computer.Chiudi()


if __name__ == '__main__':
    analizzare_VALORE = argparse.ArgumentParser()
    analizzare_VALORE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    argomenti = analizzare_VALORE.parse_args()
    risultato = {Kind_VALORE: esecuzione_dei_test(Kind_VALORE) for Kind_VALORE in (('elf', 'iso') if argomenti.boot == 'both' else (argomenti.boot,))}
    risultato['import'] = 적재시험()
    (posizione / 'build/자바시험.json').write_text(json.dumps(risultato, ensure_ascii=False, indent=2) + '\n')
