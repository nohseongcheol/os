"""독립된 vlastiti ABI ELF64와 로더 odbiti_VALUE 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from međuverzija_PYTHON import Create_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from međuverzija_C_kompilator import Create_C_kompilator


def Create_korisnik_Space(korijen_put, spremište_put, C_kompilator, 시플플번역기, 연결편집기, Arhiva_alat, konfiguracija_Pozadinski_pametni_servis_za_transfer, Izvrši_naredba):
    konfiguracija_Pozadinski_pametni_servis_za_transfer = [Postavke_VALUE for Postavke_VALUE in konfiguracija_Pozadinski_pametni_servis_za_transfer if Postavke_VALUE != '-mgeneral-regs-only']
    međuverzija_put = korijen_put / 'build'
    출력결과 = međuverzija_put / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = korijen_put / 'korisnik'
    포직스경로 = spremište_put / 'posix-kor/arm64-native'
    obuhvaćati_put = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for kompilator_alat, 추가영역, PUTANJA, Ime in [
            (C_kompilator, [], 원본자료 / 'Pokreni.S', 'start.o'),
            (C_kompilator, ['-std=c11'], 원본자료 / 'Izvrši_naredba.c', 'runtime.o'),
            (C_kompilator, ['-std=c11'], 포직스경로 / 'korisnik_most.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'PrimjerDatoteke.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_kompilator, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (C_kompilator, ['-std=c11'], 원본자료 / 'Editor.c', 'vi.o')]:
        Izvrši_naredba([kompilator_alat] + konfiguracija_Pozadinski_pametni_servis_za_transfer + 추가영역 + obuhvaćati_put + ['-Wall', '-Wextra', '-Werror', '-c', PUTANJA, '-o', 출력결과 / Ime])
    Izvrši_naredba([Arhiva_alat, 'rcs', međuverzija_put / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Ime in ('demo', 'fault', 'network', 'vi'):
        Izvrši_naredba([연결편집기, '-T', 원본자료 / 'veza_Raspored.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Ime + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Ime + '.o'), međuverzija_put / 'libposix-kor-user.a'])
    자바라이브러리만들기(korijen_put, Izvrši_naredba)
    # 기존 vlastiti Java kompilator/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(međuverzija_put)) as 작업경로:
        poduka_put = Path(작업경로)
        Izvrši_naredba(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', poduka_put, '-sourcepath', poduka_put, '-d', poduka_put] +
            [podaci_položaj for podaci_položaj in sorted((spremište_put / 'os/korisnik/자바').glob('*.java')) if podaci_položaj.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Izvrši_naredba(['sh', spremište_put / 'compiler/미리번역.sh', '--entry', 'alat_unos.Pokreni',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(poduka_put.glob('*.class')))
    압축해제경로 = korijen_put / 'vendor/uzlib'
    for PUTANJA, Ime in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'komplet.c', 'jar.o')] + [(압축해제경로 / (Ime + '.c'), Ime + '.o') for Ime in ('tinflate', 'crc32', 'adler32')]:
        Izvrši_naredba([C_kompilator] + konfiguracija_Pozadinski_pametni_servis_za_transfer + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + obuhvaćati_put + ['-c', PUTANJA, '-o', 출력결과 / Ime])
    Izvrši_naredba([연결편집기, '-T', 원본자료 / 'veza_Raspored.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Ime for Ime in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Create_PYTHON(korijen_put, C_kompilator, 연결편집기)
    Create_C_kompilator(korijen_put, spremište_put, C_kompilator, 연결편집기, konfiguracija_Pozadinski_pametni_servis_za_transfer, Izvrši_naredba)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    program_Zaglavlje_pomak = struct.unpack_from('<Q', 유효함, 32)[0]
    Zaglavlje_Popis = [program_Zaglavlje_pomak + artikl_COUNT * 56 for artikl_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [podaci_položaj for podaci_položaj in Zaglavlje_Popis if struct.unpack_from('<I', 유효함, podaci_položaj)[0] == 1]
    Tekst, podaci = 적재구획[:2]
    naredba_adresa = struct.unpack_from('<Q', 유효함, Tekst + 16)[0]
    podaci_adresa = struct.unpack_from('<Q', 유효함, podaci + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', naredba_adresa + 1), ('data-entry', 24, 'Q', podaci_adresa),
               ('outside-file', Tekst + 32, 'Q', len(유효함) + 1), ('short-memory', Tekst + 40, 'Q', 1),
               ('kernel-address', Tekst + 16, 'Q', 0x80000), ('memory-overflow', Tekst + 40, 'Q', 2**64 - 1),
               ('writable-code', Tekst + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Tekst, 'I', 2),
               ('unaligned-load', Tekst + 16, 'Q', naredba_adresa + 8),
               ('overlap', podaci + 16, 'Q', naredba_adresa)]
    for Ime, pomak_VALUE, oblik_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + oblik_932e03c8, 바뀐자료, pomak_VALUE, VALUE)
        시험사례.append((Ime, bytes(바뀐자료)))
    탑재덩이들 = [(Ime.replace('-', '_'), 출력결과 / (Ime + '.elf')) for Ime in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Ime, korisni_podaci_podaci) in enumerate(시험사례):
        PUTANJA = 출력결과 / ('invalid-{}.elf'.format(Ime)); PUTANJA.write_bytes(korisni_podaci_podaci)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), PUTANJA))
    sklop, Zaglavlje_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Ime, PUTANJA in 탑재덩이들:
        simbol_VALUE = 'user_blob_' + Ime
        크기목록[Ime] = PUTANJA.stat().st_size
        # 생성한 ravnopravan_član_VALUE 경로만 넣어 프로젝트 경로의 공백/Citat 영향을 피한다.
        sklop += ['.balign 16', '.global ' + simbol_VALUE, simbol_VALUE + ':', '.incbin "{}"'.format(PUTANJA.relative_to(korijen_put))]
        Zaglavlje_VALUE.append('extern const unsigned char {}[];'.format(simbol_VALUE))
    sklop.append('.section .note.GNU-stack,"",%progbits')
    Zaglavlje_VALUE += ['static const program 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Zaglavlje_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Zaglavlje_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Zaglavlje_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], postupak_MODE) for postupak_MODE in (0, 1)]
    Zaglavlje_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Zaglavlje_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Zaglavlje_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Zaglavlje_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Zaglavlje_VALUE += ['};', 'static const program 잘못된실행항목들[] = {']
    Zaglavlje_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(korisni_podaci_podaci)) for 순번, (_, korisni_podaci_podaci) in enumerate(시험사례)]
    Zaglavlje_VALUE += ['};']
    (međuverzija_put / 'programs.S').write_text('\n'.join(sklop) + '\n')
    (međuverzija_put / 'programs.h').write_text('\n'.join(Zaglavlje_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Ime for Ime, _ in 시험사례) + '\n')
    Izvrši_naredba([C_kompilator] + konfiguracija_Pozadinski_pametni_servis_za_transfer + ['-c', međuverzija_put / 'programs.S', '-o', međuverzija_put / 'programs.o'])
