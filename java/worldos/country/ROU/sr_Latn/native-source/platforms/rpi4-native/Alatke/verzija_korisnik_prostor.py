"""독립된 자체 ABI ELF64와 로더 odbaciti_VALUE_e3ecc00b 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from verzija_PYTHON import Create_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from verzija_C_kompajler import Create_C_kompajler


def Create_korisnik_prostor(koren_putanja, depo_putanja, C_kompajler, 시플플번역기, 연결편집기, Arhiva_alatka, konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini, Izvrši_komanda):
    konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini = [Postavke_VALUE for Postavke_VALUE in konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini if Postavke_VALUE != '-mgeneral-regs-only']
    verzija_putanja = koren_putanja / 'build'
    출력결과 = verzija_putanja / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = koren_putanja / 'korisnik'
    포직스경로 = depo_putanja / 'posix-kor/arm64-native'
    uključiti_putanja = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for kompajler_alatka, 추가영역, putanja, ime in [
            (C_kompajler, [], 원본자료 / 'koristiti.S', 'start.o'),
            (C_kompajler, ['-std=c11'], 원본자료 / 'Izvrši_komanda.c', 'runtime.o'),
            (C_kompajler, ['-std=c11'], 포직스경로 / 'korisnik_most.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_kompajler, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (C_kompajler, ['-std=c11'], 원본자료 / 'Uređivač.c', 'vi.o')]:
        Izvrši_komanda([kompajler_alatka] + konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini + 추가영역 + uključiti_putanja + ['-Wall', '-Wextra', '-Werror', '-c', putanja, '-o', 출력결과 / ime])
    Izvrši_komanda([Arhiva_alatka, 'rcs', verzija_putanja / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for ime in ('demo', 'fault', 'network', 'vi'):
        Izvrši_komanda([연결편집기, '-T', 원본자료 / 'Veza_Raspored.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (ime + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (ime + '.o'), verzija_putanja / 'libposix-kor-user.a'])
    자바라이브러리만들기(koren_putanja, Izvrši_komanda)
    # 기존 자체 Java kompajler/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(verzija_putanja)) as 작업경로:
        Razred_putanja = Path(작업경로)
        Izvrši_komanda(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Razred_putanja, '-sourcepath', Razred_putanja, '-d', Razred_putanja] +
            [podaci_pozicija for podaci_pozicija in sorted((depo_putanja / 'os/korisnik/자바').glob('*.java')) if podaci_pozicija.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Izvrši_komanda(['sh', depo_putanja / 'compiler/미리번역.sh', '--entry', 'alatka_stavka.koristiti',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(Razred_putanja.glob('*.class')))
    압축해제경로 = koren_putanja / 'vendor/uzlib'
    for putanja, ime in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'komplet.c', 'jar.o')] + [(압축해제경로 / (ime + '.c'), ime + '.o') for ime in ('tinflate', 'crc32', 'adler32')]:
        Izvrši_komanda([C_kompajler] + konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + uključiti_putanja + ['-c', putanja, '-o', 출력결과 / ime])
    Izvrši_komanda([연결편집기, '-T', 원본자료 / 'Veza_Raspored.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / ime for ime in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Create_PYTHON(koren_putanja, C_kompajler, 연결편집기)
    Create_C_kompajler(koren_putanja, depo_putanja, C_kompajler, 연결편집기, konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini, Izvrši_komanda)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    program_Zaglavlje_Pomak = struct.unpack_from('<Q', 유효함, 32)[0]
    Zaglavlje_Lista = [program_Zaglavlje_Pomak + stavka_COUNT * 56 for stavka_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [podaci_pozicija for podaci_pozicija in Zaglavlje_Lista if struct.unpack_from('<I', 유효함, podaci_pozicija)[0] == 1]
    SMS, podaci = 적재구획[:2]
    komanda_adresa = struct.unpack_from('<Q', 유효함, SMS + 16)[0]
    podaci_adresa = struct.unpack_from('<Q', 유효함, podaci + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', komanda_adresa + 1), ('data-entry', 24, 'Q', podaci_adresa),
               ('outside-file', SMS + 32, 'Q', len(유효함) + 1), ('short-memory', SMS + 40, 'Q', 1),
               ('kernel-address', SMS + 16, 'Q', 0x80000), ('memory-overflow', SMS + 40, 'Q', 2**64 - 1),
               ('writable-code', SMS + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', SMS, 'I', 2),
               ('unaligned-load', SMS + 16, 'Q', komanda_adresa + 8),
               ('overlap', podaci + 16, 'Q', komanda_adresa)]
    for ime, Pomak_VALUE, format_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + format_932e03c8, 바뀐자료, Pomak_VALUE, VALUE)
        시험사례.append((ime, bytes(바뀐자료)))
    탑재덩이들 = [(ime.replace('-', '_'), 출력결과 / (ime + '.elf')) for ime in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (ime, korisni_podaci_podaci) in enumerate(시험사례):
        putanja = 출력결과 / ('invalid-{}.elf'.format(ime)); putanja.write_bytes(korisni_podaci_podaci)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), putanja))
    sklop, Zaglavlje_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for ime, putanja in 탑재덩이들:
        simbol_VALUE = 'user_blob_' + ime
        크기목록[ime] = putanja.stat().st_size
        # 생성한 ravnopravni_uređaj_VALUE 경로만 넣어 프로젝트 경로의 공백/Citat 영향을 피한다.
        sklop += ['.balign 16', '.global ' + simbol_VALUE, simbol_VALUE + ':', '.incbin "{}"'.format(putanja.relative_to(koren_putanja))]
        Zaglavlje_VALUE.append('extern const unsigned char {}[];'.format(simbol_VALUE))
    sklop.append('.section .note.GNU-stack,"",%progbits')
    Zaglavlje_VALUE += ['static const program 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Zaglavlje_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Zaglavlje_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Zaglavlje_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metod_MODE) for metod_MODE in (0, 1)]
    Zaglavlje_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Zaglavlje_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Zaglavlje_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Zaglavlje_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Zaglavlje_VALUE += ['};', 'static const program 잘못된실행항목들[] = {']
    Zaglavlje_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(korisni_podaci_podaci)) for 순번, (_, korisni_podaci_podaci) in enumerate(시험사례)]
    Zaglavlje_VALUE += ['};']
    (verzija_putanja / 'programs.S').write_text('\n'.join(sklop) + '\n')
    (verzija_putanja / 'programs.h').write_text('\n'.join(Zaglavlje_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(ime for ime, _ in 시험사례) + '\n')
    Izvrši_komanda([C_kompajler] + konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini + ['-c', verzija_putanja / 'programs.S', '-o', verzija_putanja / 'programs.o'])
