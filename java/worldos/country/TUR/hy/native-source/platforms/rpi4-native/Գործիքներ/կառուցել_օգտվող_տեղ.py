"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Կերտի_ր_օգտվող_տեղ(արմատ_ուղի, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, Պահոց_գործիք, 설정비트, կատարել_հրաման):
    설정비트 = [Կարգավորումներ_արժեք for Կարգավորումներ_արժեք in 설정비트 if Կարգավորումներ_արժեք != '-mgeneral-regs-only']
    կառուցել_ուղի = արմատ_ուղի / 'build'
    출력결과 = կառուցել_ուղի / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = արմատ_ուղի / 'օգտվող'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, Ճանապարհ, Անուն in [
            (시언어번역기, [], 원본자료 / 'Գործարկել.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'կատարել_հրաման.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'օգտվող_կամուրջ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Խմբագիր.c', 'vi.o')]:
        կատարել_հրաման([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', Ճանապարհ, '-o', 출력결과 / Անուն])
    կատարել_հրաման([Պահոց_գործիք, 'rcs', կառուցել_ուղի / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Անուն in ('demo', 'fault', 'network', 'vi'):
        կատարել_հրաման([연결편집기, '-T', 원본자료 / 'կապ_Դասավորություն.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Անուն + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Անուն + '.o'), կառուցել_ուղի / 'libposix-kor-user.a'])
    자바라이브러리만들기(արմատ_ուղի, կատարել_հրաման)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(կառուցել_ուղի)) as 작업경로:
        դաս_ուղի = Path(작업경로)
        կատարել_հրաման(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', դաս_ուղի, '-sourcepath', դաս_ուղի, '-d', դաս_ուղի] +
            [տվյալ_դիրք for տվյալ_դիրք in sorted((저장소경로 / 'os/օգտվող/자바').glob('*.java')) if տվյալ_դիրք.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        կատարել_հրաման(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'գործիք_մուտքագրում.Գործարկել',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(դաս_ուղի.glob('*.class')))
    압축해제경로 = արմատ_ուղի / 'vendor/uzlib'
    for Ճանապարհ, Անուն in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'փաթեթ.c', 'jar.o')] + [(압축해제경로 / (Անուն + '.c'), Անուն + '.o') for Անուն in ('tinflate', 'crc32', 'adler32')]:
        կատարել_հրաման([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', Ճանապարհ, '-o', 출력결과 / Անուն])
    կատարել_հրաման([연결편집기, '-T', 원본자료 / 'կապ_Դասավորություն.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Անուն for Անուն in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(արմատ_ուղի, 시언어번역기, 연결편집기)
    시언어번역기만들기(արմատ_ուղի, 저장소경로, 시언어번역기, 연결편집기, 설정비트, կատարել_հրաման)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    ծրագիր_Վերնագիր_Տեղաշարժում = struct.unpack_from('<Q', 유효함, 32)[0]
    Վերնագիր_Ցուցակ = [ծրագիր_Վերնագիր_Տեղաշարժում + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [տվյալ_դիրք for տվյալ_դիրք in Վերնագիր_Ցուցակ if struct.unpack_from('<I', 유효함, տվյալ_դիրք)[0] == 1]
    Տեքստ, տվյալ = 적재구획[:2]
    հրաման_հասցե = struct.unpack_from('<Q', 유효함, Տեքստ + 16)[0]
    տվյալ_հասցե = struct.unpack_from('<Q', 유효함, տվյալ + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', հրաման_հասցե + 1), ('data-entry', 24, 'Q', տվյալ_հասցե),
               ('outside-file', Տեքստ + 32, 'Q', len(유효함) + 1), ('short-memory', Տեքստ + 40, 'Q', 1),
               ('kernel-address', Տեքստ + 16, 'Q', 0x80000), ('memory-overflow', Տեքստ + 40, 'Q', 2**64 - 1),
               ('writable-code', Տեքստ + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Տեքստ, 'I', 2),
               ('unaligned-load', Տեքստ + 16, 'Q', հրաման_հասցե + 8),
               ('overlap', տվյալ + 16, 'Q', հրաման_հասցե)]
    for Անուն, Տեղաշարժում_արժեք, ձեւաչափ_932e03c8, արժեք in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + ձեւաչափ_932e03c8, 바뀐자료, Տեղաշարժում_արժեք, արժեք)
        시험사례.append((Անուն, bytes(바뀐자료)))
    탑재덩이들 = [(Անուն.replace('-', '_'), 출력결과 / (Անուն + '.elf')) for Անուն in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for Փնտրում_դասիչ, (Անուն, օգտակար_բեռնվածք_տվյալ) in enumerate(시험사례):
        Ճանապարհ = 출력결과 / ('invalid-{}.elf'.format(Անուն)); Ճանապարհ.write_bytes(օգտակար_բեռնվածք_տվյալ)
        탑재덩이들.append(('invalid_{}'.format(Փնտրում_դասիչ), Ճանապարհ))
    어셈블리자료, Վերնագիր_արժեք = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Անուն, Ճանապարհ in 탑재덩이들:
        նշան_արժեք = 'user_blob_' + Անուն
        크기목록[Անուն] = Ճանապարհ.stat().st_size
        # 생성한 հավասարազոր_սարք_արժեք 경로만 넣어 프로젝트 경로의 공백/Մեջբերում 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + նշան_արժեք, նշան_արժեք + ':', '.incbin "{}"'.format(Ճանապարհ.relative_to(արմատ_ուղի))]
        Վերնագիր_արժեք.append('extern const unsigned char {}[];'.format(նշան_արժեք))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Վերնագիր_արժեք += ['static const ծրագիր 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Վերնագիր_արժեք += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Վերնագիր_արժեք += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Վերնագիր_արժեք += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], եղանակ_կերպ) for եղանակ_կերպ in (0, 1)]
    Վերնագիր_արժեք += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Վերնագիր_արժեք += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Վերնագիր_արժեք += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Վերնագիր_արժեք += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Վերնագիր_արժեք += ['};', 'static const ծրագիր 잘못된실행항목들[] = {']
    Վերնագիր_արժեք += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(օգտակար_բեռնվածք_տվյալ)) for 순번, (_, օգտակար_բեռնվածք_տվյալ) in enumerate(시험사례)]
    Վերնագիր_արժեք += ['};']
    (կառուցել_ուղի / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (կառուցել_ուղի / 'programs.h').write_text('\n'.join(Վերնագիր_արժեք) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Անուն for Անուն, _ in 시험사례) + '\n')
    կատարել_հրաման([시언어번역기] + 설정비트 + ['-c', կառուցել_ուղի / 'programs.S', '-o', կառուցել_ուղի / 'programs.o'])
