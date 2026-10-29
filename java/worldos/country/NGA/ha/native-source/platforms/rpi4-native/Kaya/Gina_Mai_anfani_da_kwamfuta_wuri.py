"""독립된 자체 ABI ELF64와 로더 kore_Daraja 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def ƙirƙíra_Mai_anfani_da_kwamfuta_wuri(기준경로, matattara_Hanyar_shiga, 시언어번역기, 시플플번역기, 연결편집기, Rumbun_ajiya_kayan_aiki, saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango, gudanar_Umarni):
    saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango = [Saituna_Daraja for Saituna_Daraja in saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango if Saituna_Daraja != '-mgeneral-regs-only']
    Gina_Hanyar_shiga = 기준경로 / 'build'
    출력결과 = Gina_Hanyar_shiga / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'Mai_anfani_da_kwamfuta'
    포직스경로 = matattara_Hanyar_shiga / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, Hanyar_shiga, Suna in [
            (시언어번역기, [], 원본자료 / 'Tafiyar_da.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'gudanar_Umarni.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / '사용자연결.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Edita.c', 'vi.o')]:
        gudanar_Umarni([번역기] + saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', Hanyar_shiga, '-o', 출력결과 / Suna])
    gudanar_Umarni([Rumbun_ajiya_kayan_aiki, 'rcs', Gina_Hanyar_shiga / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Suna in ('demo', 'fault', 'network', 'vi'):
        gudanar_Umarni([연결편집기, '-T', 원본자료 / 'Kafa_Zagaye.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Suna + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Suna + '.o'), Gina_Hanyar_shiga / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, gudanar_Umarni)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(Gina_Hanyar_shiga)) as 작업경로:
        Aji_Hanyar_shiga = Path(작업경로)
        gudanar_Umarni(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Aji_Hanyar_shiga, '-sourcepath', Aji_Hanyar_shiga, '-d', Aji_Hanyar_shiga] +
            [자료위치 for 자료위치 in sorted((matattara_Hanyar_shiga / 'os/Mai_anfani_da_kwamfuta/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        gudanar_Umarni(['sh', matattara_Hanyar_shiga / 'compiler/미리번역.sh', '--entry', 'kayan_aiki_Mashigar_bayanai.Tafiyar_da',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(Aji_Hanyar_shiga.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for Hanyar_shiga, Suna in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'dami.c', 'jar.o')] + [(압축해제경로 / (Suna + '.c'), Suna + '.o') for Suna in ('tinflate', 'crc32', 'adler32')]:
        gudanar_Umarni([시언어번역기] + saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', Hanyar_shiga, '-o', 출력결과 / Suna])
    gudanar_Umarni([연결편집기, '-T', 원본자료 / 'Kafa_Zagaye.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Suna for Suna in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, matattara_Hanyar_shiga, 시언어번역기, 연결편집기, saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango, gudanar_Umarni)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    Shiri_Kai_Sassautawa = struct.unpack_from('<Q', 유효함, 32)[0]
    Kai_Jeri = [Shiri_Kai_Sassautawa + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in Kai_Jeri if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    SMS, Tarin_bayani = 적재구획[:2]
    Umarni_imel = struct.unpack_from('<Q', 유효함, SMS + 16)[0]
    Tarin_bayani_imel = struct.unpack_from('<Q', 유효함, Tarin_bayani + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', Umarni_imel + 1), ('data-entry', 24, 'Q', Tarin_bayani_imel),
               ('outside-file', SMS + 32, 'Q', len(유효함) + 1), ('short-memory', SMS + 40, 'Q', 1),
               ('kernel-address', SMS + 16, 'Q', 0x80000), ('memory-overflow', SMS + 40, 'Q', 2**64 - 1),
               ('writable-code', SMS + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', SMS, 'I', 2),
               ('unaligned-load', SMS + 16, 'Q', Umarni_imel + 8),
               ('overlap', Tarin_bayani + 16, 'Q', Umarni_imel)]
    for Suna, Sassautawa_Daraja, tsari, Daraja in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + tsari, 바뀐자료, Sassautawa_Daraja, Daraja)
        시험사례.append((Suna, bytes(바뀐자료)))
    탑재덩이들 = [(Suna.replace('-', '_'), 출력결과 / (Suna + '.elf')) for Suna in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (Suna, Kumshinbayanai_Tarin_bayani) in enumerate(시험사례):
        Hanyar_shiga = 출력결과 / ('invalid-{}.elf'.format(Suna)); Hanyar_shiga.write_bytes(Kumshinbayanai_Tarin_bayani)
        탑재덩이들.append(('invalid_{}'.format(색인), Hanyar_shiga))
    어셈블리자료, Kai_Daraja = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Suna, Hanyar_shiga in 탑재덩이들:
        alama_Daraja = 'user_blob_' + Suna
        크기목록[Suna] = Hanyar_shiga.stat().st_size
        # 생성한 Fiya_Daraja 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + alama_Daraja, alama_Daraja + ':', '.incbin "{}"'.format(Hanyar_shiga.relative_to(기준경로))]
        Kai_Daraja.append('extern const unsigned char {}[];'.format(alama_Daraja))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Kai_Daraja += ['static const Shiri 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Kai_Daraja += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Kai_Daraja += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Kai_Daraja += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], tsari_yanayin_aiki) for tsari_yanayin_aiki in (0, 1)]
    Kai_Daraja += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Kai_Daraja += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Kai_Daraja += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Kai_Daraja += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Kai_Daraja += ['};', 'static const Shiri 잘못된실행항목들[] = {']
    Kai_Daraja += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(Kumshinbayanai_Tarin_bayani)) for 순번, (_, Kumshinbayanai_Tarin_bayani) in enumerate(시험사례)]
    Kai_Daraja += ['};']
    (Gina_Hanyar_shiga / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (Gina_Hanyar_shiga / 'programs.h').write_text('\n'.join(Kai_Daraja) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Suna for Suna, _ in 시험사례) + '\n')
    gudanar_Umarni([시언어번역기] + saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango + ['-c', Gina_Hanyar_shiga / 'programs.S', '-o', Gina_Hanyar_shiga / 'programs.o'])
