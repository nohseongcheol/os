"""독립된 eigin ABI ELF64와 로더 hafna_VALUE 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from smíð_PYTHON import stofna_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def stofna_notandi_svæði(rót_slóð_3f268910, gagnageymsla_slóð, 시언어번역기, 시플플번역기, 연결편집기, Safn_verkfæri, afbrigði_Background_Intelligent_Transfer_Service, keyra_skipun):
    afbrigði_Background_Intelligent_Transfer_Service = [Stillingar_VALUE for Stillingar_VALUE in afbrigði_Background_Intelligent_Transfer_Service if Stillingar_VALUE != '-mgeneral-regs-only']
    smíð_slóð = rót_slóð_3f268910 / 'build'
    úttak_54cd5e1d = smíð_slóð / 'user'
    úttak_54cd5e1d.mkdir(exist_ok=True)
    원본자료 = rót_slóð_3f268910 / 'notandi'
    포직스경로 = gagnageymsla_slóð / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', úttak_54cd5e1d]
    for 번역기, 추가영역, SLÓÐ, Heiti in [
            (시언어번역기, [], 원본자료 / 'Keyra_2.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'keyra_skipun.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'notandi_brú.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'Skráardæmi.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ritill.c', 'vi.o')]:
        keyra_skipun([번역기] + afbrigði_Background_Intelligent_Transfer_Service + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', SLÓÐ, '-o', úttak_54cd5e1d / Heiti])
    keyra_skipun([Safn_verkfæri, 'rcs', smíð_slóð / 'libposix-kor-user.a', úttak_54cd5e1d / 'posix.o'])
    for Heiti in ('demo', 'fault', 'network', 'vi'):
        keyra_skipun([연결편집기, '-T', 원본자료 / 'tengja_útlit.ld', '-z', 'max-page-size=4096', '-o', úttak_54cd5e1d / (Heiti + '.elf'),
             úttak_54cd5e1d / 'start.o', úttak_54cd5e1d / 'runtime.o', úttak_54cd5e1d / (Heiti + '.o'), smíð_slóð / 'libposix-kor-user.a'])
    자바라이브러리만들기(rót_slóð_3f268910, keyra_skipun)
    # 기존 eigin Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(smíð_slóð)) as 작업경로:
        klasi_slóð = Path(작업경로)
        keyra_skipun(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klasi_slóð, '-sourcepath', klasi_slóð, '-d', klasi_slóð] +
            [gögn_staða for gögn_staða in sorted((gagnageymsla_slóð / 'os/notandi/자바').glob('*.java')) if gögn_staða.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        keyra_skipun(['sh', gagnageymsla_slóð / 'compiler/미리번역.sh', '--entry', 'verkfæri_færsla.Keyra_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', úttak_54cd5e1d / 'java-tools.c'] + sorted(klasi_slóð.glob('*.class')))
    압축해제경로 = rót_slóð_3f268910 / 'vendor/uzlib'
    for SLÓÐ, Heiti in [(úttak_54cd5e1d / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'búnt.c', 'jar.o')] + [(압축해제경로 / (Heiti + '.c'), Heiti + '.o') for Heiti in ('tinflate', 'crc32', 'adler32')]:
        keyra_skipun([시언어번역기] + afbrigði_Background_Intelligent_Transfer_Service + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', SLÓÐ, '-o', úttak_54cd5e1d / Heiti])
    keyra_skipun([연결편집기, '-T', 원본자료 / 'tengja_útlit.ld', '-z', 'max-page-size=4096', '-o', úttak_54cd5e1d / 'java-tools.elf'] +
        [úttak_54cd5e1d / Heiti for Heiti in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    stofna_PYTHON(rót_slóð_3f268910, 시언어번역기, 연결편집기)
    시언어번역기만들기(rót_slóð_3f268910, gagnageymsla_slóð, 시언어번역기, 연결편집기, afbrigði_Background_Intelligent_Transfer_Service, keyra_skipun)
    유효함 = (úttak_54cd5e1d / 'demo.elf').read_bytes()
    forrit_Haus_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    Haus_Listi = [forrit_Haus_OFFSET + vara_COUNT * 56 for vara_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [gögn_staða for gögn_staða in Haus_Listi if struct.unpack_from('<I', 유효함, gögn_staða)[0] == 1]
    Texti, gögn = 적재구획[:2]
    skipun_slóð = struct.unpack_from('<Q', 유효함, Texti + 16)[0]
    gögn_slóð = struct.unpack_from('<Q', 유효함, gögn + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', skipun_slóð + 1), ('data-entry', 24, 'Q', gögn_slóð),
               ('outside-file', Texti + 32, 'Q', len(유효함) + 1), ('short-memory', Texti + 40, 'Q', 1),
               ('kernel-address', Texti + 16, 'Q', 0x80000), ('memory-overflow', Texti + 40, 'Q', 2**64 - 1),
               ('writable-code', Texti + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Texti, 'I', 2),
               ('unaligned-load', Texti + 16, 'Q', skipun_slóð + 8),
               ('overlap', gögn + 16, 'Q', skipun_slóð)]
    for Heiti, OFFSET_VALUE, snið_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + snið_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((Heiti, bytes(바뀐자료)))
    탑재덩이들 = [(Heiti.replace('-', '_'), úttak_54cd5e1d / (Heiti + '.elf')) for Heiti in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Heiti, farmur_gögn) in enumerate(시험사례):
        SLÓÐ = úttak_54cd5e1d / ('invalid-{}.elf'.format(Heiti)); SLÓÐ.write_bytes(farmur_gögn)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), SLÓÐ))
    samsetning, Haus_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Heiti, SLÓÐ in 탑재덩이들:
        tákn_VALUE = 'user_blob_' + Heiti
        크기목록[Heiti] = SLÓÐ.stat().st_size
        # 생성한 jafningi_VALUE 경로만 넣어 프로젝트 경로의 공백/Tilvitnun 영향을 피한다.
        samsetning += ['.balign 16', '.global ' + tákn_VALUE, tákn_VALUE + ':', '.incbin "{}"'.format(SLÓÐ.relative_to(rót_slóð_3f268910))]
        Haus_VALUE.append('extern const unsigned char {}[];'.format(tákn_VALUE))
    samsetning.append('.section .note.GNU-stack,"",%progbits')
    Haus_VALUE += ['static const forrit 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Haus_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Haus_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Haus_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], aðferð_MODE) for aðferð_MODE in (0, 1)]
    Haus_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Haus_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Haus_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Haus_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Haus_VALUE += ['};', 'static const forrit 잘못된실행항목들[] = {']
    Haus_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(farmur_gögn)) for 순번, (_, farmur_gögn) in enumerate(시험사례)]
    Haus_VALUE += ['};']
    (smíð_slóð / 'programs.S').write_text('\n'.join(samsetning) + '\n')
    (smíð_slóð / 'programs.h').write_text('\n'.join(Haus_VALUE) + '\n')
    (úttak_54cd5e1d / 'invalid-cases.txt').write_text('\n'.join(Heiti for Heiti, _ in 시험사례) + '\n')
    keyra_skipun([시언어번역기] + afbrigði_Background_Intelligent_Transfer_Service + ['-c', smíð_slóð / 'programs.S', '-o', smíð_slóð / 'programs.o'])
