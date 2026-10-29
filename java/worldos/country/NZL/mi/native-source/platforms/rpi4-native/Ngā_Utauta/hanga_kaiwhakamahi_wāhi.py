"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from hanga_PYTHON import Waihanga_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Waihanga_kaiwhakamahi_wāhi(pūtake_ara, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, Pūranga_utauta, 설정비트, kawe_tono):
    설정비트 = [Ngā_Tautuhinga_uara for Ngā_Tautuhinga_uara in 설정비트 if Ngā_Tautuhinga_uara != '-mgeneral-regs-only']
    hanga_ara = pūtake_ara / 'build'
    출력결과 = hanga_ara / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = pūtake_ara / 'kaiwhakamahi'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, ara, Ingoa in [
            (시언어번역기, [], 원본자료 / 'whakahaere.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'kawe_tono.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'kaiwhakamahi_arawhata.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Pūwhakatika.c', 'vi.o')]:
        kawe_tono([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', ara, '-o', 출력결과 / Ingoa])
    kawe_tono([Pūranga_utauta, 'rcs', hanga_ara / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Ingoa in ('demo', 'fault', 'network', 'vi'):
        kawe_tono([연결편집기, '-T', 원본자료 / 'Hono_Tahora.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Ingoa + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Ingoa + '.o'), hanga_ara / 'libposix-kor-user.a'])
    자바라이브러리만들기(pūtake_ara, kawe_tono)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(hanga_ara)) as 작업경로:
        tauaha_ara = Path(작업경로)
        kawe_tono(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', tauaha_ara, '-sourcepath', tauaha_ara, '-d', tauaha_ara] +
            [raraunga_tūranga for raraunga_tūranga in sorted((저장소경로 / 'os/kaiwhakamahi/자바').glob('*.java')) if raraunga_tūranga.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        kawe_tono(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'utauta_tāurunga.whakahaere',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(tauaha_ara.glob('*.class')))
    압축해제경로 = pūtake_ara / 'vendor/uzlib'
    for ara, Ingoa in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'pūpū.c', 'jar.o')] + [(압축해제경로 / (Ingoa + '.c'), Ingoa + '.o') for Ingoa in ('tinflate', 'crc32', 'adler32')]:
        kawe_tono([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', ara, '-o', 출력결과 / Ingoa])
    kawe_tono([연결편집기, '-T', 원본자료 / 'Hono_Tahora.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Ingoa for Ingoa in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Waihanga_PYTHON(pūtake_ara, 시언어번역기, 연결편집기)
    시언어번역기만들기(pūtake_ara, 저장소경로, 시언어번역기, 연결편집기, 설정비트, kawe_tono)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    kaupapa_Pane_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    Pane_Rārangi = [kaupapa_Pane_OFFSET + tuemi_COUNT * 56 for tuemi_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [raraunga_tūranga for raraunga_tūranga in Pane_Rārangi if struct.unpack_from('<I', 유효함, raraunga_tūranga)[0] == 1]
    Ngā_kupu, raraunga = 적재구획[:2]
    tono_ADDRESS = struct.unpack_from('<Q', 유효함, Ngā_kupu + 16)[0]
    raraunga_ADDRESS = struct.unpack_from('<Q', 유효함, raraunga + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', tono_ADDRESS + 1), ('data-entry', 24, 'Q', raraunga_ADDRESS),
               ('outside-file', Ngā_kupu + 32, 'Q', len(유효함) + 1), ('short-memory', Ngā_kupu + 40, 'Q', 1),
               ('kernel-address', Ngā_kupu + 16, 'Q', 0x80000), ('memory-overflow', Ngā_kupu + 40, 'Q', 2**64 - 1),
               ('writable-code', Ngā_kupu + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Ngā_kupu, 'I', 2),
               ('unaligned-load', Ngā_kupu + 16, 'Q', tono_ADDRESS + 8),
               ('overlap', raraunga + 16, 'Q', tono_ADDRESS)]
    for Ingoa, OFFSET_uara, hōputu_932e03c8, uara in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + hōputu_932e03c8, 바뀐자료, OFFSET_uara, uara)
        시험사례.append((Ingoa, bytes(바뀐자료)))
    탑재덩이들 = [(Ingoa.replace('-', '_'), 출력결과 / (Ingoa + '.elf')) for Ingoa in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for Rapu_INDEX, (Ingoa, tino_raraunga_raraunga) in enumerate(시험사례):
        ara = 출력결과 / ('invalid-{}.elf'.format(Ingoa)); ara.write_bytes(tino_raraunga_raraunga)
        탑재덩이들.append(('invalid_{}'.format(Rapu_INDEX), ara))
    어셈블리자료, Pane_uara = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Ingoa, ara in 탑재덩이들:
        tohu_uara = 'user_blob_' + Ingoa
        크기목록[Ingoa] = ara.stat().st_size
        # 생성한 hoa_uara 경로만 넣어 프로젝트 경로의 공백/Kī_horipū 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + tohu_uara, tohu_uara + ':', '.incbin "{}"'.format(ara.relative_to(pūtake_ara))]
        Pane_uara.append('extern const unsigned char {}[];'.format(tohu_uara))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Pane_uara += ['static const kaupapa 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Pane_uara += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Pane_uara += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Pane_uara += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], aratuka_MODE) for aratuka_MODE in (0, 1)]
    Pane_uara += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Pane_uara += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Pane_uara += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Pane_uara += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Pane_uara += ['};', 'static const kaupapa 잘못된실행항목들[] = {']
    Pane_uara += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(tino_raraunga_raraunga)) for 순번, (_, tino_raraunga_raraunga) in enumerate(시험사례)]
    Pane_uara += ['};']
    (hanga_ara / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (hanga_ara / 'programs.h').write_text('\n'.join(Pane_uara) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Ingoa for Ingoa, _ in 시험사례) + '\n')
    kawe_tono([시언어번역기] + 설정비트 + ['-c', hanga_ara / 'programs.S', '-o', hanga_ara / 'programs.o'])
