"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def ਬਣਾਓ_ਉਪਭੋਗਤਾ_ਥਾਂ(ਰੂਟ_ਰਸਤਾ, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, ਸੰਗ੍ਰਹਿ_ਸਾਧਨ, 설정비트, ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼):
    설정비트 = [ਸੈਟਿੰਗਾਂ_ਕੀਮਤ for ਸੈਟਿੰਗਾਂ_ਕੀਮਤ in 설정비트 if ਸੈਟਿੰਗਾਂ_ਕੀਮਤ != '-mgeneral-regs-only']
    ਬਿਲਡ_ਰਸਤਾ = ਰੂਟ_ਰਸਤਾ / 'build'
    출력결과 = ਬਿਲਡ_ਰਸਤਾ / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = ਰੂਟ_ਰਸਤਾ / 'ਉਪਭੋਗਤਾ'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, ਮਾਰਗ, ਨਾਂ in [
            (시언어번역기, [], 원본자료 / 'ਚਲਾਓ_2.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'ਉਪਭੋਗਤਾ_ਬਰਿਜ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ਸੰਪਾਦਕ.c', 'vi.o')]:
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', ਮਾਰਗ, '-o', 출력결과 / ਨਾਂ])
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([ਸੰਗ੍ਰਹਿ_ਸਾਧਨ, 'rcs', ਬਿਲਡ_ਰਸਤਾ / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for ਨਾਂ in ('demo', 'fault', 'network', 'vi'):
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([연결편집기, '-T', 원본자료 / 'ਲਿੰਕ_ਖਾਕਾ.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (ਨਾਂ + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (ਨਾਂ + '.o'), ਬਿਲਡ_ਰਸਤਾ / 'libposix-kor-user.a'])
    자바라이브러리만들기(ਰੂਟ_ਰਸਤਾ, ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(ਬਿਲਡ_ਰਸਤਾ)) as 작업경로:
        ਸ੍ਰੇਣੀ_ਰਸਤਾ = Path(작업경로)
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', ਸ੍ਰੇਣੀ_ਰਸਤਾ, '-sourcepath', ਸ੍ਰੇਣੀ_ਰਸਤਾ, '-d', ਸ੍ਰੇਣੀ_ਰਸਤਾ] +
            [ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ for ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ in sorted((저장소경로 / 'os/ਉਪਭੋਗਤਾ/자바').glob('*.java')) if ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'ਸਾਧਨ_ਦਾਖਲਾ.ਚਲਾਓ_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(ਸ੍ਰੇਣੀ_ਰਸਤਾ.glob('*.class')))
    압축해제경로 = ਰੂਟ_ਰਸਤਾ / 'vendor/uzlib'
    for ਮਾਰਗ, ਨਾਂ in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'ਬੰਡਲ.c', 'jar.o')] + [(압축해제경로 / (ਨਾਂ + '.c'), ਨਾਂ + '.o') for ਨਾਂ in ('tinflate', 'crc32', 'adler32')]:
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', ਮਾਰਗ, '-o', 출력결과 / ਨਾਂ])
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([연결편집기, '-T', 원본자료 / 'ਲਿੰਕ_ਖਾਕਾ.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / ਨਾਂ for ਨਾਂ in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(ਰੂਟ_ਰਸਤਾ, 시언어번역기, 연결편집기)
    시언어번역기만들기(ਰੂਟ_ਰਸਤਾ, 저장소경로, 시언어번역기, 연결편집기, 설정비트, ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    ਐਪਲੀਕੇਸ਼_ਸਿਰਲੇਖ_ਔਫਸੈਟ = struct.unpack_from('<Q', 유효함, 32)[0]
    ਸਿਰਲੇਖ_ਸੂਚੀ = [ਐਪਲੀਕੇਸ਼_ਸਿਰਲੇਖ_ਔਫਸੈਟ + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ for ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ in ਸਿਰਲੇਖ_ਸੂਚੀ if struct.unpack_from('<I', 유효함, ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ)[0] == 1]
    ਟੈਕਸਟ, ਸਮੱਗਰੀ = 적재구획[:2]
    ਆਦੇਸ਼_ਪਤਾ = struct.unpack_from('<Q', 유효함, ਟੈਕਸਟ + 16)[0]
    ਸਮੱਗਰੀ_ਪਤਾ = struct.unpack_from('<Q', 유효함, ਸਮੱਗਰੀ + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', ਆਦੇਸ਼_ਪਤਾ + 1), ('data-entry', 24, 'Q', ਸਮੱਗਰੀ_ਪਤਾ),
               ('outside-file', ਟੈਕਸਟ + 32, 'Q', len(유효함) + 1), ('short-memory', ਟੈਕਸਟ + 40, 'Q', 1),
               ('kernel-address', ਟੈਕਸਟ + 16, 'Q', 0x80000), ('memory-overflow', ਟੈਕਸਟ + 40, 'Q', 2**64 - 1),
               ('writable-code', ਟੈਕਸਟ + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', ਟੈਕਸਟ, 'I', 2),
               ('unaligned-load', ਟੈਕਸਟ + 16, 'Q', ਆਦੇਸ਼_ਪਤਾ + 8),
               ('overlap', ਸਮੱਗਰੀ + 16, 'Q', ਆਦੇਸ਼_ਪਤਾ)]
    for ਨਾਂ, ਔਫਸੈਟ_ਕੀਮਤ, ਸਰੂਪ_932e03c8, ਕੀਮਤ in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + ਸਰੂਪ_932e03c8, 바뀐자료, ਔਫਸੈਟ_ਕੀਮਤ, ਕੀਮਤ)
        시험사례.append((ਨਾਂ, bytes(바뀐자료)))
    탑재덩이들 = [(ਨਾਂ.replace('-', '_'), 출력결과 / (ਨਾਂ + '.elf')) for ਨਾਂ in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for ਲੱਭਣਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ, (ਨਾਂ, ਪੇਲੋਡ_ਸਮੱਗਰੀ) in enumerate(시험사례):
        ਮਾਰਗ = 출력결과 / ('invalid-{}.elf'.format(ਨਾਂ)); ਮਾਰਗ.write_bytes(ਪੇਲੋਡ_ਸਮੱਗਰੀ)
        탑재덩이들.append(('invalid_{}'.format(ਲੱਭਣਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ), ਮਾਰਗ))
    어셈블리자료, ਸਿਰਲੇਖ_ਕੀਮਤ = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for ਨਾਂ, ਮਾਰਗ in 탑재덩이들:
        ਪ੍ਰਤੀਕ_ਕੀਮਤ = 'user_blob_' + ਨਾਂ
        크기목록[ਨਾਂ] = ਮਾਰਗ.stat().st_size
        # 생성한 ਪਿਅਰ_ਕੀਮਤ 경로만 넣어 프로젝트 경로의 공백/ਹਵਾਲਾ 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + ਪ੍ਰਤੀਕ_ਕੀਮਤ, ਪ੍ਰਤੀਕ_ਕੀਮਤ + ':', '.incbin "{}"'.format(ਮਾਰਗ.relative_to(ਰੂਟ_ਰਸਤਾ))]
        ਸਿਰਲੇਖ_ਕੀਮਤ.append('extern const unsigned char {}[];'.format(ਪ੍ਰਤੀਕ_ਕੀਮਤ))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    ਸਿਰਲੇਖ_ਕੀਮਤ += ['static const ਐਪਲੀਕੇਸ਼ 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    ਸਿਰਲੇਖ_ਕੀਮਤ += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    ਸਿਰਲੇਖ_ਕੀਮਤ += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    ਸਿਰਲੇਖ_ਕੀਮਤ += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], ਮੈਥਡ_ਮੋਡ) for ਮੈਥਡ_ਮੋਡ in (0, 1)]
    ਸਿਰਲੇਖ_ਕੀਮਤ += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    ਸਿਰਲੇਖ_ਕੀਮਤ += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    ਸਿਰਲੇਖ_ਕੀਮਤ += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    ਸਿਰਲੇਖ_ਕੀਮਤ += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    ਸਿਰਲੇਖ_ਕੀਮਤ += ['};', 'static const ਐਪਲੀਕੇਸ਼ 잘못된실행항목들[] = {']
    ਸਿਰਲੇਖ_ਕੀਮਤ += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(ਪੇਲੋਡ_ਸਮੱਗਰੀ)) for 순번, (_, ਪੇਲੋਡ_ਸਮੱਗਰੀ) in enumerate(시험사례)]
    ਸਿਰਲੇਖ_ਕੀਮਤ += ['};']
    (ਬਿਲਡ_ਰਸਤਾ / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (ਬਿਲਡ_ਰਸਤਾ / 'programs.h').write_text('\n'.join(ਸਿਰਲੇਖ_ਕੀਮਤ) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(ਨਾਂ for ਨਾਂ, _ in 시험사례) + '\n')
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([시언어번역기] + 설정비트 + ['-c', ਬਿਲਡ_ਰਸਤਾ / 'programs.S', '-o', ਬਿਲਡ_ਰਸਤਾ / 'programs.o'])
