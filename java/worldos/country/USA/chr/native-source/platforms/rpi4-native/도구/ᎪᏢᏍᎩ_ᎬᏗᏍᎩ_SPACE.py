"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def 사용자영역만들기(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ, 설정비트, ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ):
    설정비트 = [ᏕᎦᎧᎲᎢ_ᏧᎬᏩᎶᏗᏯ for ᏕᎦᎧᎲᎢ_ᏧᎬᏩᎶᏗᏯ in 설정비트 if ᏕᎦᎧᎲᎢ_ᏧᎬᏩᎶᏗᏯ != '-mgeneral-regs-only']
    ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ = 기준경로 / 'build'
    출력결과 = ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'ᎬᏗᏍᎩ'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, ᎠᏍᏓᏩᏛᏍᏗ, ᏚᏙᎥᎢ in [
            (시언어번역기, [], 원본자료 / 'ᎠᎢᏎᏍᏗ.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / '사용자연결.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ᎣᏍᏓ_ᏗᎦᎧᎲᏍᎩ.c', 'vi.o')]:
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', ᎠᏍᏓᏩᏛᏍᏗ, '-o', 출력결과 / ᏚᏙᎥᎢ])
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ, 'rcs', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for ᏚᏙᎥᎢ in ('demo', 'fault', 'network', 'vi'):
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([연결편집기, '-T', 원본자료 / 'ᎫᏓᎸᎢ_ᏱᎬᏂ.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (ᏚᏙᎥᎢ + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (ᏚᏙᎥᎢ + '.o'), ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ)) as 작업경로:
        ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ = Path(작업경로)
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ, '-sourcepath', ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ, '-d', ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/ᎬᏗᏍᎩ/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'ᎬᏔᏂᏓᏍᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.ᎠᎢᏎᏍᏗ',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for ᎠᏍᏓᏩᏛᏍᏗ, ᏚᏙᎥᎢ in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'ᎦᏇᏅᎯ.c', 'jar.o')] + [(압축해제경로 / (ᏚᏙᎥᎢ + '.c'), ᏚᏙᎥᎢ + '.o') for ᏚᏙᎥᎢ in ('tinflate', 'crc32', 'adler32')]:
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', ᎠᏍᏓᏩᏛᏍᏗ, '-o', 출력결과 / ᏚᏙᎥᎢ])
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([연결편집기, '-T', 원본자료 / 'ᎫᏓᎸᎢ_ᏱᎬᏂ.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / ᏚᏙᎥᎢ for ᏚᏙᎥᎢ in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    프로그램머리변위 = struct.unpack_from('<Q', 유효함, 32)[0]
    ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏕᎦᏅᏅᏛ = [프로그램머리변위 + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏕᎦᏅᏅᏛ if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    ᎠᎪᎵᏰᏗ, ᎦᏟᏌᏅᎯ = 적재구획[:2]
    ᎤᏁᏤᎸᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ = struct.unpack_from('<Q', 유효함, ᎠᎪᎵᏰᏗ + 16)[0]
    ᎦᏟᏌᏅᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ = struct.unpack_from('<Q', 유효함, ᎦᏟᏌᏅᎯ + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    ᎠᏓᎪᎵᏰᏍᎩ_ᎢᏳᎵᏍᏔᏅᎢ = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', ᎤᏁᏤᎸᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ + 1), ('data-entry', 24, 'Q', ᎦᏟᏌᏅᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ),
               ('outside-file', ᎠᎪᎵᏰᏗ + 32, 'Q', len(유효함) + 1), ('short-memory', ᎠᎪᎵᏰᏗ + 40, 'Q', 1),
               ('kernel-address', ᎠᎪᎵᏰᏗ + 16, 'Q', 0x80000), ('memory-overflow', ᎠᎪᎵᏰᏗ + 40, 'Q', 2**64 - 1),
               ('writable-code', ᎠᎪᎵᏰᏗ + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', ᎠᎪᎵᏰᏗ, 'I', 2),
               ('unaligned-load', ᎠᎪᎵᏰᏗ + 16, 'Q', ᎤᏁᏤᎸᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ + 8),
               ('overlap', ᎦᏟᏌᏅᎯ + 16, 'Q', ᎤᏁᏤᎸᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ)]
    for ᏚᏙᎥᎢ, 변위, ᏱᎬᏁᎸᎯ_932e03c8, ᏧᎬᏩᎶᏗᏯ in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + ᏱᎬᏁᎸᎯ_932e03c8, 바뀐자료, 변위, ᏧᎬᏩᎶᏗᏯ)
        ᎠᏓᎪᎵᏰᏍᎩ_ᎢᏳᎵᏍᏔᏅᎢ.append((ᏚᏙᎥᎢ, bytes(바뀐자료)))
    탑재덩이들 = [(ᏚᏙᎥᎢ.replace('-', '_'), 출력결과 / (ᏚᏙᎥᎢ + '.elf')) for ᏚᏙᎥᎢ in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (ᏚᏙᎥᎢ, ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ) in enumerate(ᎠᏓᎪᎵᏰᏍᎩ_ᎢᏳᎵᏍᏔᏅᎢ):
        ᎠᏍᏓᏩᏛᏍᏗ = 출력결과 / ('invalid-{}.elf'.format(ᏚᏙᎥᎢ)); ᎠᏍᏓᏩᏛᏍᏗ.write_bytes(ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ)
        탑재덩이들.append(('invalid_{}'.format(색인), ᎠᏍᏓᏩᏛᏍᏗ))
    어셈블리자료, ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for ᏚᏙᎥᎢ, ᎠᏍᏓᏩᏛᏍᏗ in 탑재덩이들:
        심볼 = 'user_blob_' + ᏚᏙᎥᎢ
        크기목록[ᏚᏙᎥᎢ] = ᎠᏍᏓᏩᏛᏍᏗ.stat().st_size
        # 생성한 ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + 심볼, 심볼 + ':', '.incbin "{}"'.format(ᎠᏍᏓᏩᏛᏍᏗ.relative_to(기준경로))]
        ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ.append('extern const unsigned char {}[];'.format(심볼))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ += ['static const ᎬᏙᏗ 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], method_ᎬᏙᏗ) for method_ᎬᏙᏗ in (0, 1)]
    ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ += ['};', 'static const ᎬᏙᏗ 잘못된실행항목들[] = {']
    ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ)) for 순번, (_, ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ) in enumerate(ᎠᏓᎪᎵᏰᏍᎩ_ᎢᏳᎵᏍᏔᏅᎢ)]
    ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ += ['};']
    (ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'programs.h').write_text('\n'.join(ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(ᏚᏙᎥᎢ for ᏚᏙᎥᎢ, _ in ᎠᏓᎪᎵᏰᏍᎩ_ᎢᏳᎵᏍᏔᏅᎢ) + '\n')
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([시언어번역기] + 설정비트 + ['-c', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'programs.S', '-o', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'programs.o'])
