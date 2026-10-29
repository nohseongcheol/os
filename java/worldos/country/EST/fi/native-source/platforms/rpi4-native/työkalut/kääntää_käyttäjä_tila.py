"""독립된 oma ABI ELF64와 로더 hylkää_ARVO_e3ecc00b testit 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from kääntää_PYTHON import Luo_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from kääntää_C_kääntäjä import Luo_C_kääntäjä


def Luo_käyttäjä_tila(juuri_polku, säilö_polku, C_kääntäjä, 시플플번역기, linkitin_työkalu, Arkisto_työkalu, määritys_Background_Intelligent_Transfer_Service, Suorita_komento):
    määritys_Background_Intelligent_Transfer_Service = [Asetukset_ARVO for Asetukset_ARVO in määritys_Background_Intelligent_Transfer_Service if Asetukset_ARVO != '-mgeneral-regs-only']
    kääntää_polku = juuri_polku / 'build'
    tulos = kääntää_polku / 'user'
    tulos.mkdir(exist_ok=True)
    원본자료 = juuri_polku / 'käyttäjätila'
    포직스경로 = säilö_polku / 'posix-kor/arm64-native'
    sisältää_polku = ['-I', 원본자료, '-I', 포직스경로 / 'esittelyt', '-I', tulos]
    for kääntäjä_työkalu, 추가영역, polku_2, Nimi in [
            (C_kääntäjä, [], 원본자료 / 'Suorita_2.S', 'start.o'),
            (C_kääntäjä, ['-std=c11'], 원본자료 / 'Suorita_komento.c', 'runtime.o'),
            (C_kääntäjä, ['-std=c11'], 포직스경로 / 'käyttäjä_silta.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'Tiedostoesimerkki.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_kääntäjä, ['-std=c11'], 원본자료 / 'Suojaus_testi.c', 'fault.o'),
            (C_kääntäjä, ['-std=c11'], 원본자료 / 'editori.c', 'vi.o')]:
        Suorita_komento([kääntäjä_työkalu] + määritys_Background_Intelligent_Transfer_Service + 추가영역 + sisältää_polku + ['-Wall', '-Wextra', '-Werror', '-c', polku_2, '-o', tulos / Nimi])
    Suorita_komento([Arkisto_työkalu, 'rcs', kääntää_polku / 'libposix-kor-user.a', tulos / 'posix.o'])
    for Nimi in ('demo', 'fault', 'network', 'vi'):
        Suorita_komento([linkitin_työkalu, '-T', 원본자료 / 'linkitysasettelu.ld', '-z', 'max-page-size=4096', '-o', tulos / (Nimi + '.elf'),
             tulos / 'start.o', tulos / 'runtime.o', tulos / (Nimi + '.o'), kääntää_polku / 'libposix-kor-user.a'])
    자바라이브러리만들기(juuri_polku, Suorita_komento)
    # 기존 oma Java kääntäjä/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(kääntää_polku)) as 작업경로:
        Luokka_polku = Path(작업경로)
        Suorita_komento(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Luokka_polku, '-sourcepath', Luokka_polku, '-d', Luokka_polku] +
            [data_toimi for data_toimi in sorted((säilö_polku / 'os/käyttäjätila/자바').glob('*.java')) if data_toimi.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Suorita_komento(['sh', säilö_polku / 'compiler/미리번역.sh', '--entry', 'työkalu_merkintä.Suorita_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', tulos / 'java-tools.c'] + sorted(Luokka_polku.glob('*.class')))
    압축해제경로 = juuri_polku / 'vendor/uzlib'
    for polku_2, Nimi in [(tulos / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'nippu.c', 'jar.o')] + [(압축해제경로 / (Nimi + '.c'), Nimi + '.o') for Nimi in ('tinflate', 'crc32', 'adler32')]:
        Suorita_komento([C_kääntäjä] + määritys_Background_Intelligent_Transfer_Service + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + sisältää_polku + ['-c', polku_2, '-o', tulos / Nimi])
    Suorita_komento([linkitin_työkalu, '-T', 원본자료 / 'linkitysasettelu.ld', '-z', 'max-page-size=4096', '-o', tulos / 'java-tools.elf'] +
        [tulos / Nimi for Nimi in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Luo_PYTHON(juuri_polku, C_kääntäjä, linkitin_työkalu)
    Luo_C_kääntäjä(juuri_polku, säilö_polku, C_kääntäjä, linkitin_työkalu, määritys_Background_Intelligent_Transfer_Service, Suorita_komento)
    kelvollinen = (tulos / 'demo.elf').read_bytes()
    ohjelma_otsikko_SIIRTYMÄ = struct.unpack_from('<Q', kelvollinen, 32)[0]
    otsikko_luettelo = [ohjelma_otsikko_SIIRTYMÄ + kohde_LASKE * 56 for kohde_LASKE in range(struct.unpack_from('<H', kelvollinen, 56)[0])]
    적재구획 = [data_toimi for data_toimi in otsikko_luettelo if struct.unpack_from('<I', kelvollinen, data_toimi)[0] == 1]
    teksti, data = 적재구획[:2]
    komento_OSOITE = struct.unpack_from('<Q', kelvollinen, teksti + 16)[0]
    data_OSOITE = struct.unpack_from('<Q', kelvollinen, data + 16)[0]
    호출규약 = kelvollinen.index(b'JKOROS\0')
    testi_työ = [('empty', b''), ('short', kelvollinen[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', komento_OSOITE + 1), ('data-entry', 24, 'Q', data_OSOITE),
               ('outside-file', teksti + 32, 'Q', len(kelvollinen) + 1), ('short-memory', teksti + 40, 'Q', 1),
               ('kernel-address', teksti + 16, 'Q', 0x80000), ('memory-overflow', teksti + 40, 'Q', 2**64 - 1),
               ('writable-code', teksti + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', teksti, 'I', 2),
               ('unaligned-load', teksti + 16, 'Q', komento_OSOITE + 8),
               ('overlap', data + 16, 'Q', komento_OSOITE)]
    for Nimi, SIIRTYMÄ_ARVO, muoto_932e03c8, ARVO in 수정사항:
        바뀐자료 = bytearray(kelvollinen); struct.pack_into('<' + muoto_932e03c8, 바뀐자료, SIIRTYMÄ_ARVO, ARVO)
        testi_työ.append((Nimi, bytes(바뀐자료)))
    탑재덩이들 = [(Nimi.replace('-', '_'), tulos / (Nimi + '.elf')) for Nimi in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for HAKU_INDEKSI, (Nimi, tiedot_data) in enumerate(testi_työ):
        polku_2 = tulos / ('invalid-{}.elf'.format(Nimi)); polku_2.write_bytes(tiedot_data)
        탑재덩이들.append(('invalid_{}'.format(HAKU_INDEKSI), polku_2))
    kokoonpano, otsikko_ARVO = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Nimi, polku_2 in 탑재덩이들:
        symboli_ARVO = 'user_blob_' + Nimi
        크기목록[Nimi] = polku_2.stat().st_size
        # 생성한 vertaissolmu_ARVO 경로만 넣어 프로젝트 경로의 공백/Lainaus 영향을 피한다.
        kokoonpano += ['.balign 16', '.global ' + symboli_ARVO, symboli_ARVO + ':', '.incbin "{}"'.format(polku_2.relative_to(juuri_polku))]
        otsikko_ARVO.append('extern const unsigned char {}[];'.format(symboli_ARVO))
    kokoonpano.append('.section .note.GNU-stack,"",%progbits')
    otsikko_ARVO += ['static const ohjelma 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    otsikko_ARVO += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    otsikko_ARVO += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    otsikko_ARVO += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], menetelmä_tila) for menetelmä_tila in (0, 1)]
    otsikko_ARVO += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    otsikko_ARVO += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    otsikko_ARVO += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    otsikko_ARVO += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    otsikko_ARVO += ['};', 'static const ohjelma 잘못된실행항목들[] = {']
    otsikko_ARVO += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(tiedot_data)) for 순번, (_, tiedot_data) in enumerate(testi_työ)]
    otsikko_ARVO += ['};']
    (kääntää_polku / 'programs.S').write_text('\n'.join(kokoonpano) + '\n')
    (kääntää_polku / 'programs.h').write_text('\n'.join(otsikko_ARVO) + '\n')
    (tulos / 'invalid-cases.txt').write_text('\n'.join(Nimi for Nimi, _ in testi_työ) + '\n')
    Suorita_komento([C_kääntäjä] + määritys_Background_Intelligent_Transfer_Service + ['-c', kääntää_polku / 'programs.S', '-o', kääntää_polku / 'programs.o'])
