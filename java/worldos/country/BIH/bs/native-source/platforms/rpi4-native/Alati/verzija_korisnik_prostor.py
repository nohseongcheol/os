"""독립된 자체 ABI ELF64와 로더 odbiti_VALUE 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from verzija_PYTHON import Create_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Create_korisnik_prostor(koijen_put, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, Arhiva_alatka, 설정비트, Izvrši_komanda):
    설정비트 = [Postavke_VALUE for Postavke_VALUE in 설정비트 if Postavke_VALUE != '-mgeneral-regs-only']
    verzija_put = koijen_put / 'build'
    출력결과 = verzija_put / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = koijen_put / 'korisnik'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, Putanja, Naziv in [
            (시언어번역기, [], 원본자료 / 'Pokreni.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Izvrši_komanda.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'korisnik_most.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'urednik.c', 'vi.o')]:
        Izvrši_komanda([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', Putanja, '-o', 출력결과 / Naziv])
    Izvrši_komanda([Arhiva_alatka, 'rcs', verzija_put / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Naziv in ('demo', 'fault', 'network', 'vi'):
        Izvrši_komanda([연결편집기, '-T', 원본자료 / 'Veza_izgled.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Naziv + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Naziv + '.o'), verzija_put / 'libposix-kor-user.a'])
    자바라이브러리만들기(koijen_put, Izvrši_komanda)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(verzija_put)) as 작업경로:
        klasa_put = Path(작업경로)
        Izvrši_komanda(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klasa_put, '-sourcepath', klasa_put, '-d', klasa_put] +
            [podaci_položaj for podaci_položaj in sorted((저장소경로 / 'os/korisnik/자바').glob('*.java')) if podaci_položaj.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Izvrši_komanda(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'alatka_unos.Pokreni',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(klasa_put.glob('*.class')))
    압축해제경로 = koijen_put / 'vendor/uzlib'
    for Putanja, Naziv in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'paket.c', 'jar.o')] + [(압축해제경로 / (Naziv + '.c'), Naziv + '.o') for Naziv in ('tinflate', 'crc32', 'adler32')]:
        Izvrši_komanda([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', Putanja, '-o', 출력결과 / Naziv])
    Izvrši_komanda([연결편집기, '-T', 원본자료 / 'Veza_izgled.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Naziv for Naziv in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Create_PYTHON(koijen_put, 시언어번역기, 연결편집기)
    시언어번역기만들기(koijen_put, 저장소경로, 시언어번역기, 연결편집기, 설정비트, Izvrši_komanda)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    program_Zaglavlje_Pomak = struct.unpack_from('<Q', 유효함, 32)[0]
    Zaglavlje_spisak = [program_Zaglavlje_Pomak + stavka_COUNT * 56 for stavka_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [podaci_položaj for podaci_položaj in Zaglavlje_spisak if struct.unpack_from('<I', 유효함, podaci_položaj)[0] == 1]
    Tekst, podaci = 적재구획[:2]
    komanda_adresa = struct.unpack_from('<Q', 유효함, Tekst + 16)[0]
    podaci_adresa = struct.unpack_from('<Q', 유효함, podaci + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', komanda_adresa + 1), ('data-entry', 24, 'Q', podaci_adresa),
               ('outside-file', Tekst + 32, 'Q', len(유효함) + 1), ('short-memory', Tekst + 40, 'Q', 1),
               ('kernel-address', Tekst + 16, 'Q', 0x80000), ('memory-overflow', Tekst + 40, 'Q', 2**64 - 1),
               ('writable-code', Tekst + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Tekst, 'I', 2),
               ('unaligned-load', Tekst + 16, 'Q', komanda_adresa + 8),
               ('overlap', podaci + 16, 'Q', komanda_adresa)]
    for Naziv, Pomak_VALUE, format_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + format_932e03c8, 바뀐자료, Pomak_VALUE, VALUE)
        시험사례.append((Naziv, bytes(바뀐자료)))
    탑재덩이들 = [(Naziv.replace('-', '_'), 출력결과 / (Naziv + '.elf')) for Naziv in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Naziv, korisni_sadržaj_podaci) in enumerate(시험사례):
        Putanja = 출력결과 / ('invalid-{}.elf'.format(Naziv)); Putanja.write_bytes(korisni_sadržaj_podaci)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), Putanja))
    어셈블리자료, Zaglavlje_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Naziv, Putanja in 탑재덩이들:
        simbol_VALUE = 'user_blob_' + Naziv
        크기목록[Naziv] = Putanja.stat().st_size
        # 생성한 peer_VALUE 경로만 넣어 프로젝트 경로의 공백/Citat 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + simbol_VALUE, simbol_VALUE + ':', '.incbin "{}"'.format(Putanja.relative_to(koijen_put))]
        Zaglavlje_VALUE.append('extern const unsigned char {}[];'.format(simbol_VALUE))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Zaglavlje_VALUE += ['static const program 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Zaglavlje_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Zaglavlje_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Zaglavlje_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metoda_mod) for metoda_mod in (0, 1)]
    Zaglavlje_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Zaglavlje_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Zaglavlje_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Zaglavlje_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Zaglavlje_VALUE += ['};', 'static const program 잘못된실행항목들[] = {']
    Zaglavlje_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(korisni_sadržaj_podaci)) for 순번, (_, korisni_sadržaj_podaci) in enumerate(시험사례)]
    Zaglavlje_VALUE += ['};']
    (verzija_put / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (verzija_put / 'programs.h').write_text('\n'.join(Zaglavlje_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Naziv for Naziv, _ in 시험사례) + '\n')
    Izvrši_komanda([시언어번역기] + 설정비트 + ['-c', verzija_put / 'programs.S', '-o', verzija_put / 'programs.o'])
