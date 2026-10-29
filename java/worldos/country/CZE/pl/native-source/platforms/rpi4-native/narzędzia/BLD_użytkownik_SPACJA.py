"""독립된 własny ABI ELF64와 로더 odrzucić_WARTOŚĆ testy 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from BLD_PYTHON import Twórca_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from BLD_C_kompilator import Twórca_C_kompilator


def Twórca_użytkownik_SPACJA(korzeń_ścieżka, repozytorium_ścieżka, C_kompilator, 시플플번역기, konsolidator_narzędzie, Archiwum_narzędzie, konfiguracja_BITS, Wykonaj_polecenie):
    konfiguracja_BITS = [Ustawienia_WARTOŚĆ for Ustawienia_WARTOŚĆ in konfiguracja_BITS if Ustawienia_WARTOŚĆ != '-mgeneral-regs-only']
    BLD_ścieżka = korzeń_ścieżka / 'build'
    produkt_wyjściowy = BLD_ścieżka / 'user'
    produkt_wyjściowy.mkdir(exist_ok=True)
    원본자료 = korzeń_ścieżka / 'przestrzeń_użytkownika'
    포직스경로 = repozytorium_ścieżka / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / 'deklaracje', '-I', produkt_wyjściowy]
    for kompilator_narzędzie, 추가영역, ścieżka_2, Nazwa in [
            (C_kompilator, [], 원본자료 / 'Uruchom_2.S', 'start.o'),
            (C_kompilator, ['-std=c11'], 원본자료 / 'Wykonaj_polecenie.c', 'runtime.o'),
            (C_kompilator, ['-std=c11'], 포직스경로 / 'użytkownik_mostek.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'PrzykładPliku.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_kompilator, ['-std=c11'], 원본자료 / 'Ochrona_test.c', 'fault.o'),
            (C_kompilator, ['-std=c11'], 원본자료 / 'edytor.c', 'vi.o')]:
        Wykonaj_polecenie([kompilator_narzędzie] + konfiguracja_BITS + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', ścieżka_2, '-o', produkt_wyjściowy / Nazwa])
    Wykonaj_polecenie([Archiwum_narzędzie, 'rcs', BLD_ścieżka / 'libposix-kor-user.a', produkt_wyjściowy / 'posix.o'])
    for Nazwa in ('demo', 'fault', 'network', 'vi'):
        Wykonaj_polecenie([konsolidator_narzędzie, '-T', 원본자료 / 'układ_konsolidacji.ld', '-z', 'max-page-size=4096', '-o', produkt_wyjściowy / (Nazwa + '.elf'),
             produkt_wyjściowy / 'start.o', produkt_wyjściowy / 'runtime.o', produkt_wyjściowy / (Nazwa + '.o'), BLD_ścieżka / 'libposix-kor-user.a'])
    자바라이브러리만들기(korzeń_ścieżka, Wykonaj_polecenie)
    # 기존 własny Java kompilator/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(BLD_ścieżka)) as 작업경로:
        Klasa_ścieżka = Path(작업경로)
        Wykonaj_polecenie(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Klasa_ścieżka, '-sourcepath', Klasa_ścieżka, '-d', Klasa_ścieżka] +
            [dane_stanowisko for dane_stanowisko in sorted((repozytorium_ścieżka / 'os/przestrzeń_użytkownika/자바').glob('*.java')) if dane_stanowisko.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Wykonaj_polecenie(['sh', repozytorium_ścieżka / 'compiler/미리번역.sh', '--entry', 'narzędzie_wpis.Uruchom_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', produkt_wyjściowy / 'java-tools.c'] + sorted(Klasa_ścieżka.glob('*.class')))
    압축해제경로 = korzeń_ścieżka / 'vendor/uzlib'
    for ścieżka_2, Nazwa in [(produkt_wyjściowy / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'pakiet.c', 'jar.o')] + [(압축해제경로 / (Nazwa + '.c'), Nazwa + '.o') for Nazwa in ('tinflate', 'crc32', 'adler32')]:
        Wykonaj_polecenie([C_kompilator] + konfiguracja_BITS + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', ścieżka_2, '-o', produkt_wyjściowy / Nazwa])
    Wykonaj_polecenie([konsolidator_narzędzie, '-T', 원본자료 / 'układ_konsolidacji.ld', '-z', 'max-page-size=4096', '-o', produkt_wyjściowy / 'java-tools.elf'] +
        [produkt_wyjściowy / Nazwa for Nazwa in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Twórca_PYTHON(korzeń_ścieżka, C_kompilator, konsolidator_narzędzie)
    Twórca_C_kompilator(korzeń_ścieżka, repozytorium_ścieżka, C_kompilator, konsolidator_narzędzie, konfiguracja_BITS, Wykonaj_polecenie)
    prawidłowy = (produkt_wyjściowy / 'demo.elf').read_bytes()
    program_Nagłówek_przesunąć = struct.unpack_from('<Q', prawidłowy, 32)[0]
    Nagłówek_Lista = [program_Nagłówek_przesunąć + towar_ILE_LICZB * 56 for towar_ILE_LICZB in range(struct.unpack_from('<H', prawidłowy, 56)[0])]
    적재구획 = [dane_stanowisko for dane_stanowisko in Nagłówek_Lista if struct.unpack_from('<I', prawidłowy, dane_stanowisko)[0] == 1]
    tekst, dane = 적재구획[:2]
    polecenie_ADRES = struct.unpack_from('<Q', prawidłowy, tekst + 16)[0]
    dane_ADRES = struct.unpack_from('<Q', prawidłowy, dane + 16)[0]
    Połącz_ABI = prawidłowy.index(b'JKOROS\0')
    przypadek_testowy = [('empty', b''), ('short', prawidłowy[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', polecenie_ADRES + 1), ('data-entry', 24, 'Q', dane_ADRES),
               ('outside-file', tekst + 32, 'Q', len(prawidłowy) + 1), ('short-memory', tekst + 40, 'Q', 1),
               ('kernel-address', tekst + 16, 'Q', 0x80000), ('memory-overflow', tekst + 40, 'Q', 2**64 - 1),
               ('writable-code', tekst + 4, 'I', 7), ('missing-abi', Połącz_ABI, 'B', ord('X')),
               ('wrong-abi', Połącz_ABI + 8, 'I', 2), ('dynamic', tekst, 'I', 2),
               ('unaligned-load', tekst + 16, 'Q', polecenie_ADRES + 8),
               ('overlap', dane + 16, 'Q', polecenie_ADRES)]
    for Nazwa, przesunąć_WARTOŚĆ_450fc799, format_932e03c8, WARTOŚĆ in 수정사항:
        바뀐자료 = bytearray(prawidłowy); struct.pack_into('<' + format_932e03c8, 바뀐자료, przesunąć_WARTOŚĆ_450fc799, WARTOŚĆ)
        przypadek_testowy.append((Nazwa, bytes(바뀐자료)))
    탑재덩이들 = [(Nazwa.replace('-', '_'), produkt_wyjściowy / (Nazwa + '.elf')) for Nazwa in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for WYSZUKAJ_INDEKS, (Nazwa, ładunek_dane) in enumerate(przypadek_testowy):
        ścieżka_2 = produkt_wyjściowy / ('invalid-{}.elf'.format(Nazwa)); ścieżka_2.write_bytes(ładunek_dane)
        탑재덩이들.append(('invalid_{}'.format(WYSZUKAJ_INDEKS), ścieżka_2))
    zestaw, Nagłówek_WARTOŚĆ = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Nazwa, ścieżka_2 in 탑재덩이들:
        symbol_WARTOŚĆ = 'user_blob_' + Nazwa
        크기목록[Nazwa] = ścieżka_2.stat().st_size
        # 생성한 węzeł_równorzędny_WARTOŚĆ 경로만 넣어 프로젝트 경로의 공백/Cytat 영향을 피한다.
        zestaw += ['.balign 16', '.global ' + symbol_WARTOŚĆ, symbol_WARTOŚĆ + ':', '.incbin "{}"'.format(ścieżka_2.relative_to(korzeń_ścieżka))]
        Nagłówek_WARTOŚĆ.append('extern const unsigned char {}[];'.format(symbol_WARTOŚĆ))
    zestaw.append('.section .note.GNU-stack,"",%progbits')
    Nagłówek_WARTOŚĆ += ['static const program 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Nagłówek_WARTOŚĆ += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Nagłówek_WARTOŚĆ += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Nagłówek_WARTOŚĆ += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metoda_tryb) for metoda_tryb in (0, 1)]
    Nagłówek_WARTOŚĆ += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Nagłówek_WARTOŚĆ += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Nagłówek_WARTOŚĆ += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Nagłówek_WARTOŚĆ += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Nagłówek_WARTOŚĆ += ['};', 'static const program 잘못된실행항목들[] = {']
    Nagłówek_WARTOŚĆ += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(ładunek_dane)) for 순번, (_, ładunek_dane) in enumerate(przypadek_testowy)]
    Nagłówek_WARTOŚĆ += ['};']
    (BLD_ścieżka / 'programs.S').write_text('\n'.join(zestaw) + '\n')
    (BLD_ścieżka / 'programs.h').write_text('\n'.join(Nagłówek_WARTOŚĆ) + '\n')
    (produkt_wyjściowy / 'invalid-cases.txt').write_text('\n'.join(Nazwa for Nazwa, _ in przypadek_testowy) + '\n')
    Wykonaj_polecenie([C_kompilator] + konfiguracja_BITS + ['-c', BLD_ścieżka / 'programs.S', '-o', BLD_ścieżka / 'programs.o'])
