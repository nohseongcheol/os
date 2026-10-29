"""독립된 saját ABI ELF64와 로더 elutasít_ÉRTÉK 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from épít_PYTHON import készít_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from épít_C_fordítóprogram import készít_C_fordítóprogram


def készít_felhasználó_tér(gyök_útvonal, adattár_útvonal, C_fordítóprogram, 시플플번역기, kapcsolószerkesztő_eszköz, archív_eszköz, konfiguráció_BITS, végrehajt_parancs):
    konfiguráció_BITS = [Gépház_ÉRTÉK for Gépház_ÉRTÉK in konfiguráció_BITS if Gépház_ÉRTÉK != '-mgeneral-regs-only']
    épít_útvonal = gyök_útvonal / 'build'
    kimenet = épít_útvonal / 'user'
    kimenet.mkdir(exist_ok=True)
    원본자료 = gyök_útvonal / 'felhasználó'
    포직스경로 = adattár_útvonal / 'posix-kor/arm64-native'
    tartalmaz_útvonal = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', kimenet]
    for fordítóprogram_eszköz, 추가영역, ÚTVONAL, Név in [
            (C_fordítóprogram, [], 원본자료 / 'Futtatás.S', 'start.o'),
            (C_fordítóprogram, ['-std=c11'], 원본자료 / 'végrehajt_parancs.c', 'runtime.o'),
            (C_fordítóprogram, ['-std=c11'], 포직스경로 / 'felhasználó_híd.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'FájlPélda.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_fordítóprogram, ['-std=c11'], 원본자료 / 'Védelem_teszt.c', 'fault.o'),
            (C_fordítóprogram, ['-std=c11'], 원본자료 / 'Írássegéd.c', 'vi.o')]:
        végrehajt_parancs([fordítóprogram_eszköz] + konfiguráció_BITS + 추가영역 + tartalmaz_útvonal + ['-Wall', '-Wextra', '-Werror', '-c', ÚTVONAL, '-o', kimenet / Név])
    végrehajt_parancs([archív_eszköz, 'rcs', épít_útvonal / 'libposix-kor-user.a', kimenet / 'posix.o'])
    for Név in ('demo', 'fault', 'network', 'vi'):
        végrehajt_parancs([kapcsolószerkesztő_eszköz, '-T', 원본자료 / 'csatol_Navigáció.ld', '-z', 'max-page-size=4096', '-o', kimenet / (Név + '.elf'),
             kimenet / 'start.o', kimenet / 'runtime.o', kimenet / (Név + '.o'), épít_útvonal / 'libposix-kor-user.a'])
    자바라이브러리만들기(gyök_útvonal, végrehajt_parancs)
    # 기존 saját Java fordítóprogram/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(épít_útvonal)) as 작업경로:
        tanóra_útvonal = Path(작업경로)
        végrehajt_parancs(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', tanóra_útvonal, '-sourcepath', tanóra_útvonal, '-d', tanóra_útvonal] +
            [adat_pozíció for adat_pozíció in sorted((adattár_útvonal / 'os/felhasználó/자바').glob('*.java')) if adat_pozíció.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        végrehajt_parancs(['sh', adattár_útvonal / 'compiler/미리번역.sh', '--entry', 'eszköz_bejegyzés.Futtatás',
             '--profile', 'user', '--heap-words', '1048576', '-o', kimenet / 'java-tools.c'] + sorted(tanóra_útvonal.glob('*.class')))
    압축해제경로 = gyök_útvonal / 'vendor/uzlib'
    for ÚTVONAL, Név in [(kimenet / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'köteg.c', 'jar.o')] + [(압축해제경로 / (Név + '.c'), Név + '.o') for Név in ('tinflate', 'crc32', 'adler32')]:
        végrehajt_parancs([C_fordítóprogram] + konfiguráció_BITS + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + tartalmaz_útvonal + ['-c', ÚTVONAL, '-o', kimenet / Név])
    végrehajt_parancs([kapcsolószerkesztő_eszköz, '-T', 원본자료 / 'csatol_Navigáció.ld', '-z', 'max-page-size=4096', '-o', kimenet / 'java-tools.elf'] +
        [kimenet / Név for Név in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    készít_PYTHON(gyök_útvonal, C_fordítóprogram, kapcsolószerkesztő_eszköz)
    készít_C_fordítóprogram(gyök_útvonal, adattár_útvonal, C_fordítóprogram, kapcsolószerkesztő_eszköz, konfiguráció_BITS, végrehajt_parancs)
    érvényes = (kimenet / 'demo.elf').read_bytes()
    app_fejléc_Ofszet = struct.unpack_from('<Q', érvényes, 32)[0]
    fejléc_Lista = [app_fejléc_Ofszet + cikk_DARAB * 56 for cikk_DARAB in range(struct.unpack_from('<H', érvényes, 56)[0])]
    적재구획 = [adat_pozíció for adat_pozíció in fejléc_Lista if struct.unpack_from('<I', érvényes, adat_pozíció)[0] == 1]
    Szöveg, adat = 적재구획[:2]
    parancs_CÍM = struct.unpack_from('<Q', érvényes, Szöveg + 16)[0]
    adat_CÍM = struct.unpack_from('<Q', érvényes, adat + 16)[0]
    호출규약 = érvényes.index(b'JKOROS\0')
    teszt_eset = [('empty', b''), ('short', érvényes[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', parancs_CÍM + 1), ('data-entry', 24, 'Q', adat_CÍM),
               ('outside-file', Szöveg + 32, 'Q', len(érvényes) + 1), ('short-memory', Szöveg + 40, 'Q', 1),
               ('kernel-address', Szöveg + 16, 'Q', 0x80000), ('memory-overflow', Szöveg + 40, 'Q', 2**64 - 1),
               ('writable-code', Szöveg + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Szöveg, 'I', 2),
               ('unaligned-load', Szöveg + 16, 'Q', parancs_CÍM + 8),
               ('overlap', adat + 16, 'Q', parancs_CÍM)]
    for Név, Ofszet_ÉRTÉK, formátum, ÉRTÉK in 수정사항:
        바뀐자료 = bytearray(érvényes); struct.pack_into('<' + formátum, 바뀐자료, Ofszet_ÉRTÉK, ÉRTÉK)
        teszt_eset.append((Név, bytes(바뀐자료)))
    탑재덩이들 = [(Név.replace('-', '_'), kimenet / (Név + '.elf')) for Név in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for KERES_INDEX, (Név, teher_adat) in enumerate(teszt_eset):
        ÚTVONAL = kimenet / ('invalid-{}.elf'.format(Név)); ÚTVONAL.write_bytes(teher_adat)
        탑재덩이들.append(('invalid_{}'.format(KERES_INDEX), ÚTVONAL))
    szerelvény, fejléc_ÉRTÉK = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Név, ÚTVONAL in 탑재덩이들:
        szimbólum_ÉRTÉK = 'user_blob_' + Név
        크기목록[Név] = ÚTVONAL.stat().st_size
        # 생성한 társ_ÉRTÉK 경로만 넣어 프로젝트 경로의 공백/Idézet 영향을 피한다.
        szerelvény += ['.balign 16', '.global ' + szimbólum_ÉRTÉK, szimbólum_ÉRTÉK + ':', '.incbin "{}"'.format(ÚTVONAL.relative_to(gyök_útvonal))]
        fejléc_ÉRTÉK.append('extern const unsigned char {}[];'.format(szimbólum_ÉRTÉK))
    szerelvény.append('.section .note.GNU-stack,"",%progbits')
    fejléc_ÉRTÉK += ['static const app 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    fejléc_ÉRTÉK += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    fejléc_ÉRTÉK += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    fejléc_ÉRTÉK += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metódus_mód) for metódus_mód in (0, 1)]
    fejléc_ÉRTÉK += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    fejléc_ÉRTÉK += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    fejléc_ÉRTÉK += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    fejléc_ÉRTÉK += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    fejléc_ÉRTÉK += ['};', 'static const app 잘못된실행항목들[] = {']
    fejléc_ÉRTÉK += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(teher_adat)) for 순번, (_, teher_adat) in enumerate(teszt_eset)]
    fejléc_ÉRTÉK += ['};']
    (épít_útvonal / 'programs.S').write_text('\n'.join(szerelvény) + '\n')
    (épít_útvonal / 'programs.h').write_text('\n'.join(fejléc_ÉRTÉK) + '\n')
    (kimenet / 'invalid-cases.txt').write_text('\n'.join(Név for Név, _ in teszt_eset) + '\n')
    végrehajt_parancs([C_fordítóprogram] + konfiguráció_BITS + ['-c', épít_útvonal / 'programs.S', '-o', épít_útvonal / 'programs.o'])
