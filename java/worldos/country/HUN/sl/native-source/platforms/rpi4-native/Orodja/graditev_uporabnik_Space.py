"""독립된 lastno ABI ELF64와 로더 zavrniti_VALUE 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from graditev_PYTHON import Ustvari_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from graditev_C_prevajalnik import Ustvari_C_prevajalnik


def Ustvari_uporabnik_Space(koren_pot, shramba_pot, C_prevajalnik, 시플플번역기, 연결편집기, Arhiv_orodje, konfiguracija_storitev_Background_Intelligent_Transfer_Service, Izvedi_ukaz):
    konfiguracija_storitev_Background_Intelligent_Transfer_Service = [Nastavitve_VALUE for Nastavitve_VALUE in konfiguracija_storitev_Background_Intelligent_Transfer_Service if Nastavitve_VALUE != '-mgeneral-regs-only']
    graditev_pot = koren_pot / 'build'
    출력결과 = graditev_pot / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = koren_pot / 'uporabnik'
    포직스경로 = shramba_pot / 'posix-kor/arm64-native'
    vključevati_pot = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for prevajalnik_orodje, 추가영역, POT, Ime in [
            (C_prevajalnik, [], 원본자료 / 'Zaženi.S', 'start.o'),
            (C_prevajalnik, ['-std=c11'], 원본자료 / 'Izvedi_ukaz.c', 'runtime.o'),
            (C_prevajalnik, ['-std=c11'], 포직스경로 / 'uporabnik_most.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'PrimerDatoteke.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_prevajalnik, ['-std=c11'], 원본자료 / 'Zaščita_preskusiti.c', 'fault.o'),
            (C_prevajalnik, ['-std=c11'], 원본자료 / 'Urejevalnik.c', 'vi.o')]:
        Izvedi_ukaz([prevajalnik_orodje] + konfiguracija_storitev_Background_Intelligent_Transfer_Service + 추가영역 + vključevati_pot + ['-Wall', '-Wextra', '-Werror', '-c', POT, '-o', 출력결과 / Ime])
    Izvedi_ukaz([Arhiv_orodje, 'rcs', graditev_pot / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Ime in ('demo', 'fault', 'network', 'vi'):
        Izvedi_ukaz([연결편집기, '-T', 원본자료 / 'Povezava_Krmarjenje.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Ime + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Ime + '.o'), graditev_pot / 'libposix-kor-user.a'])
    자바라이브러리만들기(koren_pot, Izvedi_ukaz)
    # 기존 lastno Java prevajalnik/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(graditev_pot)) as 작업경로:
        Razred_pot = Path(작업경로)
        Izvedi_ukaz(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Razred_pot, '-sourcepath', Razred_pot, '-d', Razred_pot] +
            [podatki_položaj for podatki_položaj in sorted((shramba_pot / 'os/uporabnik/자바').glob('*.java')) if podatki_položaj.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Izvedi_ukaz(['sh', shramba_pot / 'compiler/미리번역.sh', '--entry', 'orodje_vnos.Zaženi',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(Razred_pot.glob('*.class')))
    압축해제경로 = koren_pot / 'vendor/uzlib'
    for POT, Ime in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'sveženj.c', 'jar.o')] + [(압축해제경로 / (Ime + '.c'), Ime + '.o') for Ime in ('tinflate', 'crc32', 'adler32')]:
        Izvedi_ukaz([C_prevajalnik] + konfiguracija_storitev_Background_Intelligent_Transfer_Service + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + vključevati_pot + ['-c', POT, '-o', 출력결과 / Ime])
    Izvedi_ukaz([연결편집기, '-T', 원본자료 / 'Povezava_Krmarjenje.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Ime for Ime in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Ustvari_PYTHON(koren_pot, C_prevajalnik, 연결편집기)
    Ustvari_C_prevajalnik(koren_pot, shramba_pot, C_prevajalnik, 연결편집기, konfiguracija_storitev_Background_Intelligent_Transfer_Service, Izvedi_ukaz)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    aplikacija_Glava_odmik = struct.unpack_from('<Q', 유효함, 32)[0]
    Glava_Seznam = [aplikacija_Glava_odmik + element_COUNT * 56 for element_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [podatki_položaj for podatki_položaj in Glava_Seznam if struct.unpack_from('<I', 유효함, podatki_položaj)[0] == 1]
    Besedilo, podatki = 적재구획[:2]
    ukaz_naslov = struct.unpack_from('<Q', 유효함, Besedilo + 16)[0]
    podatki_naslov = struct.unpack_from('<Q', 유효함, podatki + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    preskusiti_spor = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', ukaz_naslov + 1), ('data-entry', 24, 'Q', podatki_naslov),
               ('outside-file', Besedilo + 32, 'Q', len(유효함) + 1), ('short-memory', Besedilo + 40, 'Q', 1),
               ('kernel-address', Besedilo + 16, 'Q', 0x80000), ('memory-overflow', Besedilo + 40, 'Q', 2**64 - 1),
               ('writable-code', Besedilo + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Besedilo, 'I', 2),
               ('unaligned-load', Besedilo + 16, 'Q', ukaz_naslov + 8),
               ('overlap', podatki + 16, 'Q', ukaz_naslov)]
    for Ime, odmik_VALUE, oblika_zapisa, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + oblika_zapisa, 바뀐자료, odmik_VALUE, VALUE)
        preskusiti_spor.append((Ime, bytes(바뀐자료)))
    탑재덩이들 = [(Ime.replace('-', '_'), 출력결과 / (Ime + '.elf')) for Ime in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Ime, koristna_vsebina_podatki) in enumerate(preskusiti_spor):
        POT = 출력결과 / ('invalid-{}.elf'.format(Ime)); POT.write_bytes(koristna_vsebina_podatki)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), POT))
    zbir, Glava_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Ime, POT in 탑재덩이들:
        simbol_VALUE = 'user_blob_' + Ime
        크기목록[Ime] = POT.stat().st_size
        # 생성한 enakovreden_VALUE 경로만 넣어 프로젝트 경로의 공백/Navedek 영향을 피한다.
        zbir += ['.balign 16', '.global ' + simbol_VALUE, simbol_VALUE + ':', '.incbin "{}"'.format(POT.relative_to(koren_pot))]
        Glava_VALUE.append('extern const unsigned char {}[];'.format(simbol_VALUE))
    zbir.append('.section .note.GNU-stack,"",%progbits')
    Glava_VALUE += ['static const aplikacija 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Glava_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Glava_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Glava_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metoda_MODE) for metoda_MODE in (0, 1)]
    Glava_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Glava_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Glava_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Glava_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Glava_VALUE += ['};', 'static const aplikacija 잘못된실행항목들[] = {']
    Glava_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(koristna_vsebina_podatki)) for 순번, (_, koristna_vsebina_podatki) in enumerate(preskusiti_spor)]
    Glava_VALUE += ['};']
    (graditev_pot / 'programs.S').write_text('\n'.join(zbir) + '\n')
    (graditev_pot / 'programs.h').write_text('\n'.join(Glava_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Ime for Ime, _ in preskusiti_spor) + '\n')
    Izvedi_ukaz([C_prevajalnik] + konfiguracija_storitev_Background_Intelligent_Transfer_Service + ['-c', graditev_pot / 'programs.S', '-o', graditev_pot / 'programs.o'])
