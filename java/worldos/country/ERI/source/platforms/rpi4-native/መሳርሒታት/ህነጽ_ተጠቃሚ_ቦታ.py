"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def ፍጠር_ተጠቃሚ_ቦታ(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, ሰንድ_መሳርሒ, 설정비트, ተግብር_ትእዛዝ):
    설정비트 = [ኣቀማምጣታት_ዋጋ for ኣቀማምጣታት_ዋጋ in 설정비트 if ኣቀማምጣታት_ዋጋ != '-mgeneral-regs-only']
    ህነጽ_መገዲ = 기준경로 / 'build'
    출력결과 = ህነጽ_መገዲ / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'ተጠቃሚ'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, መገዲ, ሽም in [
            (시언어번역기, [], 원본자료 / 'ኣኺድ.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ተግብር_ትእዛዝ.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / '사용자연결.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ኣርታዒ.c', 'vi.o')]:
        ተግብር_ትእዛዝ([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', መገዲ, '-o', 출력결과 / ሽም])
    ተግብር_ትእዛዝ([ሰንድ_መሳርሒ, 'rcs', ህነጽ_መገዲ / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for ሽም in ('demo', 'fault', 'network', 'vi'):
        ተግብር_ትእዛዝ([연결편집기, '-T', 원본자료 / 'መጋጠሚ_ኣቀማምጣ.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (ሽም + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (ሽም + '.o'), ህነጽ_መገዲ / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, ተግብር_ትእዛዝ)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(ህነጽ_መገዲ)) as 작업경로:
        ክፍሊ_መገዲ = Path(작업경로)
        ተግብር_ትእዛዝ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', ክፍሊ_መገዲ, '-sourcepath', ክፍሊ_መገዲ, '-d', ክፍሊ_መገዲ] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/ተጠቃሚ/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        ተግብር_ትእዛዝ(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'መሳርሒ_ምእታው.ኣኺድ',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(ክፍሊ_መገዲ.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for መገዲ, ሽም in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'ጥማር.c', 'jar.o')] + [(압축해제경로 / (ሽም + '.c'), ሽም + '.o') for ሽም in ('tinflate', 'crc32', 'adler32')]:
        ተግብር_ትእዛዝ([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', መገዲ, '-o', 출력결과 / ሽም])
    ተግብር_ትእዛዝ([연결편집기, '-T', 원본자료 / 'መጋጠሚ_ኣቀማምጣ.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / ሽም for ሽም in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, ተግብር_ትእዛዝ)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    መተግበሪ_ርእሲ_ሽፋን = struct.unpack_from('<Q', 유효함, 32)[0]
    ርእሲ_ዝርዝር = [መተግበሪ_ርእሲ_ሽፋን + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in ርእሲ_ዝርዝር if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    ጽሑፍ, ሓበሬታ = 적재구획[:2]
    ትእዛዝ_ኣድራሻ = struct.unpack_from('<Q', 유효함, ጽሑፍ + 16)[0]
    ሓበሬታ_ኣድራሻ = struct.unpack_from('<Q', 유효함, ሓበሬታ + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', ትእዛዝ_ኣድራሻ + 1), ('data-entry', 24, 'Q', ሓበሬታ_ኣድራሻ),
               ('outside-file', ጽሑፍ + 32, 'Q', len(유효함) + 1), ('short-memory', ጽሑፍ + 40, 'Q', 1),
               ('kernel-address', ጽሑፍ + 16, 'Q', 0x80000), ('memory-overflow', ጽሑፍ + 40, 'Q', 2**64 - 1),
               ('writable-code', ጽሑፍ + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', ጽሑፍ, 'I', 2),
               ('unaligned-load', ጽሑፍ + 16, 'Q', ትእዛዝ_ኣድራሻ + 8),
               ('overlap', ሓበሬታ + 16, 'Q', ትእዛዝ_ኣድራሻ)]
    for ሽም, ሽፋን_ዋጋ, ቅርጺ, ዋጋ in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + ቅርጺ, 바뀐자료, ሽፋን_ዋጋ, ዋጋ)
        시험사례.append((ሽም, bytes(바뀐자료)))
    탑재덩이들 = [(ሽም.replace('-', '_'), 출력결과 / (ሽም + '.elf')) for ሽም in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (ሽም, ጽዕነት_ክፍሊት_ሓበሬታ) in enumerate(시험사례):
        መገዲ = 출력결과 / ('invalid-{}.elf'.format(ሽም)); መገዲ.write_bytes(ጽዕነት_ክፍሊት_ሓበሬታ)
        탑재덩이들.append(('invalid_{}'.format(색인), መገዲ))
    어셈블리자료, ርእሲ_ዋጋ = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for ሽም, መገዲ in 탑재덩이들:
        ምልክት_ዋጋ = 'user_blob_' + ሽም
        크기목록[ሽም] = መገዲ.stat().st_size
        # 생성한 መዘና_ዋጋ 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + ምልክት_ዋጋ, ምልክት_ዋጋ + ':', '.incbin "{}"'.format(መገዲ.relative_to(기준경로))]
        ርእሲ_ዋጋ.append('extern const unsigned char {}[];'.format(ምልክት_ዋጋ))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    ርእሲ_ዋጋ += ['static const መተግበሪ 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    ርእሲ_ዋጋ += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    ርእሲ_ዋጋ += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    ርእሲ_ዋጋ += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], ሜላ_ኹነት) for ሜላ_ኹነት in (0, 1)]
    ርእሲ_ዋጋ += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    ርእሲ_ዋጋ += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    ርእሲ_ዋጋ += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    ርእሲ_ዋጋ += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    ርእሲ_ዋጋ += ['};', 'static const መተግበሪ 잘못된실행항목들[] = {']
    ርእሲ_ዋጋ += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(ጽዕነት_ክፍሊት_ሓበሬታ)) for 순번, (_, ጽዕነት_ክፍሊት_ሓበሬታ) in enumerate(시험사례)]
    ርእሲ_ዋጋ += ['};']
    (ህነጽ_መገዲ / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (ህነጽ_መገዲ / 'programs.h').write_text('\n'.join(ርእሲ_ዋጋ) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(ሽም for ሽም, _ in 시험사례) + '\n')
    ተግብር_ትእዛዝ([시언어번역기] + 설정비트 + ['-c', ህነጽ_መገዲ / 'programs.S', '-o', ህነጽ_መገዲ / 'programs.o'])
