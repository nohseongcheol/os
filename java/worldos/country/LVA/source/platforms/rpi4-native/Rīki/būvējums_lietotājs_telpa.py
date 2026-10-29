"""독립된 savs ABI ELF64와 로더 noraidīt_VALUE 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from būvējums_PYTHON import atvērt_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from būvējums_C_kompilators import atvērt_C_kompilators


def atvērt_lietotājs_telpa(sakne_ceļš, repozitorijs_ceļš, C_kompilators, 시플플번역기, 연결편집기, Arhīvs_rīks, konfigurācija_Background_Intelligent_Transfer_Service, Izpildīt_komanda):
    konfigurācija_Background_Intelligent_Transfer_Service = [Iestatījumi_VALUE for Iestatījumi_VALUE in konfigurācija_Background_Intelligent_Transfer_Service if Iestatījumi_VALUE != '-mgeneral-regs-only']
    būvējums_ceļš = sakne_ceļš / 'build'
    ražojums = būvējums_ceļš / 'user'
    ražojums.mkdir(exist_ok=True)
    원본자료 = sakne_ceļš / 'lietotājs'
    포직스경로 = repozitorijs_ceļš / 'posix-kor/arm64-native'
    iekļaut_ceļš = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', ražojums]
    for kompilators_rīks, 추가영역, CEĻŠ, Nosaukums in [
            (C_kompilators, [], 원본자료 / 'Palaist.S', 'start.o'),
            (C_kompilators, ['-std=c11'], 원본자료 / 'Izpildīt_komanda.c', 'runtime.o'),
            (C_kompilators, ['-std=c11'], 포직스경로 / 'lietotājs_tilts.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'DatnesPiemērs.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_kompilators, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (C_kompilators, ['-std=c11'], 원본자료 / 'Redaktors.c', 'vi.o')]:
        Izpildīt_komanda([kompilators_rīks] + konfigurācija_Background_Intelligent_Transfer_Service + 추가영역 + iekļaut_ceļš + ['-Wall', '-Wextra', '-Werror', '-c', CEĻŠ, '-o', ražojums / Nosaukums])
    Izpildīt_komanda([Arhīvs_rīks, 'rcs', būvējums_ceļš / 'libposix-kor-user.a', ražojums / 'posix.o'])
    for Nosaukums in ('demo', 'fault', 'network', 'vi'):
        Izpildīt_komanda([연결편집기, '-T', 원본자료 / 'Saite_shēma.ld', '-z', 'max-page-size=4096', '-o', ražojums / (Nosaukums + '.elf'),
             ražojums / 'start.o', ražojums / 'runtime.o', ražojums / (Nosaukums + '.o'), būvējums_ceļš / 'libposix-kor-user.a'])
    자바라이브러리만들기(sakne_ceļš, Izpildīt_komanda)
    # 기존 savs Java kompilators/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(būvējums_ceļš)) as 작업경로:
        klase_ceļš = Path(작업경로)
        Izpildīt_komanda(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klase_ceļš, '-sourcepath', klase_ceļš, '-d', klase_ceļš] +
            [dati_amats for dati_amats in sorted((repozitorijs_ceļš / 'os/lietotājs/자바').glob('*.java')) if dati_amats.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Izpildīt_komanda(['sh', repozitorijs_ceļš / 'compiler/미리번역.sh', '--entry', 'rīks_ievade.Palaist',
             '--profile', 'user', '--heap-words', '1048576', '-o', ražojums / 'java-tools.c'] + sorted(klase_ceļš.glob('*.class')))
    압축해제경로 = sakne_ceļš / 'vendor/uzlib'
    for CEĻŠ, Nosaukums in [(ražojums / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'saistīt.c', 'jar.o')] + [(압축해제경로 / (Nosaukums + '.c'), Nosaukums + '.o') for Nosaukums in ('tinflate', 'crc32', 'adler32')]:
        Izpildīt_komanda([C_kompilators] + konfigurācija_Background_Intelligent_Transfer_Service + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + iekļaut_ceļš + ['-c', CEĻŠ, '-o', ražojums / Nosaukums])
    Izpildīt_komanda([연결편집기, '-T', 원본자료 / 'Saite_shēma.ld', '-z', 'max-page-size=4096', '-o', ražojums / 'java-tools.elf'] +
        [ražojums / Nosaukums for Nosaukums in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    atvērt_PYTHON(sakne_ceļš, C_kompilators, 연결편집기)
    atvērt_C_kompilators(sakne_ceļš, repozitorijs_ceļš, C_kompilators, 연결편집기, konfigurācija_Background_Intelligent_Transfer_Service, Izpildīt_komanda)
    유효함 = (ražojums / 'demo.elf').read_bytes()
    programma_galvene_Nobīde = struct.unpack_from('<Q', 유효함, 32)[0]
    galvene_Saraksts = [programma_galvene_Nobīde + krājums_COUNT * 56 for krājums_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [dati_amats for dati_amats in galvene_Saraksts if struct.unpack_from('<I', 유효함, dati_amats)[0] == 1]
    Teksts, dati = 적재구획[:2]
    komanda_adrese = struct.unpack_from('<Q', 유효함, Teksts + 16)[0]
    dati_adrese = struct.unpack_from('<Q', 유효함, dati + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', komanda_adrese + 1), ('data-entry', 24, 'Q', dati_adrese),
               ('outside-file', Teksts + 32, 'Q', len(유효함) + 1), ('short-memory', Teksts + 40, 'Q', 1),
               ('kernel-address', Teksts + 16, 'Q', 0x80000), ('memory-overflow', Teksts + 40, 'Q', 2**64 - 1),
               ('writable-code', Teksts + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Teksts, 'I', 2),
               ('unaligned-load', Teksts + 16, 'Q', komanda_adrese + 8),
               ('overlap', dati + 16, 'Q', komanda_adrese)]
    for Nosaukums, Nobīde_VALUE, formāts_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + formāts_932e03c8, 바뀐자료, Nobīde_VALUE, VALUE)
        시험사례.append((Nosaukums, bytes(바뀐자료)))
    탑재덩이들 = [(Nosaukums.replace('-', '_'), ražojums / (Nosaukums + '.elf')) for Nosaukums in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Nosaukums, vērtums_dati) in enumerate(시험사례):
        CEĻŠ = ražojums / ('invalid-{}.elf'.format(Nosaukums)); CEĻŠ.write_bytes(vērtums_dati)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), CEĻŠ))
    montāža, galvene_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Nosaukums, CEĻŠ in 탑재덩이들:
        simbols_VALUE = 'user_blob_' + Nosaukums
        크기목록[Nosaukums] = CEĻŠ.stat().st_size
        # 생성한 vienranga_VALUE 경로만 넣어 프로젝트 경로의 공백/Citāts 영향을 피한다.
        montāža += ['.balign 16', '.global ' + simbols_VALUE, simbols_VALUE + ':', '.incbin "{}"'.format(CEĻŠ.relative_to(sakne_ceļš))]
        galvene_VALUE.append('extern const unsigned char {}[];'.format(simbols_VALUE))
    montāža.append('.section .note.GNU-stack,"",%progbits')
    galvene_VALUE += ['static const programma 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    galvene_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    galvene_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    galvene_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metode_MODE) for metode_MODE in (0, 1)]
    galvene_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    galvene_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    galvene_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    galvene_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    galvene_VALUE += ['};', 'static const programma 잘못된실행항목들[] = {']
    galvene_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(vērtums_dati)) for 순번, (_, vērtums_dati) in enumerate(시험사례)]
    galvene_VALUE += ['};']
    (būvējums_ceļš / 'programs.S').write_text('\n'.join(montāža) + '\n')
    (būvējums_ceļš / 'programs.h').write_text('\n'.join(galvene_VALUE) + '\n')
    (ražojums / 'invalid-cases.txt').write_text('\n'.join(Nosaukums for Nosaukums, _ in 시험사례) + '\n')
    Izpildīt_komanda([C_kompilators] + konfigurācija_Background_Intelligent_Transfer_Service + ['-c', būvējums_ceļš / 'programs.S', '-o', būvējums_ceļš / 'programs.o'])
