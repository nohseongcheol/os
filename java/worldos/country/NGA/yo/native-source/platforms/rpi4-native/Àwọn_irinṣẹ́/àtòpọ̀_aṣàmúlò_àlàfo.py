"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Ṣẹ̀dá_aṣàmúlò_àlàfo(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́, 설정비트, ṣiṣẹ́_àṣẹ):
    설정비트 = [Àwọn_ààtò_iye for Àwọn_ààtò_iye in 설정비트 if Àwọn_ààtò_iye != '-mgeneral-regs-only']
    àtòpọ̀_ọ̀nà = 기준경로 / 'build'
    출력결과 = àtòpọ̀_ọ̀nà / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'aṣàmúlò'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, ọ̀nà, Orúkọ in [
            (시언어번역기, [], 원본자료 / 'Rọ́ọ̀nù.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ṣiṣẹ́_àṣẹ.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'aṣàmúlò_afará.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'aṣàtúnṣe.c', 'vi.o')]:
        ṣiṣẹ́_àṣẹ([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', ọ̀nà, '-o', 출력결과 / Orúkọ])
    ṣiṣẹ́_àṣẹ([Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́, 'rcs', àtòpọ̀_ọ̀nà / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Orúkọ in ('demo', 'fault', 'network', 'vi'):
        ṣiṣẹ́_àṣẹ([연결편집기, '-T', 원본자료 / 'ṣàsopọ̀_ètò_ìrísí.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Orúkọ + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Orúkọ + '.o'), àtòpọ̀_ọ̀nà / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, ṣiṣẹ́_àṣẹ)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(àtòpọ̀_ọ̀nà)) as 작업경로:
        ọ̀wọ́_ọ̀nà = Path(작업경로)
        ṣiṣẹ́_àṣẹ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', ọ̀wọ́_ọ̀nà, '-sourcepath', ọ̀wọ́_ọ̀nà, '-d', ọ̀wọ́_ọ̀nà] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/aṣàmúlò/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        ṣiṣẹ́_àṣẹ(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'irinṣẹ́_ìgbéwọlé.Rọ́ọ̀nù',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(ọ̀wọ́_ọ̀nà.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for ọ̀nà, Orúkọ in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'àkópọ̀.c', 'jar.o')] + [(압축해제경로 / (Orúkọ + '.c'), Orúkọ + '.o') for Orúkọ in ('tinflate', 'crc32', 'adler32')]:
        ṣiṣẹ́_àṣẹ([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', ọ̀nà, '-o', 출력결과 / Orúkọ])
    ṣiṣẹ́_àṣẹ([연결편집기, '-T', 원본자료 / 'ṣàsopọ̀_ètò_ìrísí.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Orúkọ for Orúkọ in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, ṣiṣẹ́_àṣẹ)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    àtòjọ_ètò_àkọlé_Ìtayọ = struct.unpack_from('<Q', 유효함, 32)[0]
    àkọlé_Àtòkọ = [àtòjọ_ètò_àkọlé_Ìtayọ + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in àkọlé_Àtòkọ if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    SMS, détà = 적재구획[:2]
    àṣẹ_àdírẹ́ẹ̀sì = struct.unpack_from('<Q', 유효함, SMS + 16)[0]
    détà_àdírẹ́ẹ̀sì = struct.unpack_from('<Q', 유효함, détà + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', àṣẹ_àdírẹ́ẹ̀sì + 1), ('data-entry', 24, 'Q', détà_àdírẹ́ẹ̀sì),
               ('outside-file', SMS + 32, 'Q', len(유효함) + 1), ('short-memory', SMS + 40, 'Q', 1),
               ('kernel-address', SMS + 16, 'Q', 0x80000), ('memory-overflow', SMS + 40, 'Q', 2**64 - 1),
               ('writable-code', SMS + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', SMS, 'I', 2),
               ('unaligned-load', SMS + 16, 'Q', àṣẹ_àdírẹ́ẹ̀sì + 8),
               ('overlap', détà + 16, 'Q', àṣẹ_àdírẹ́ẹ̀sì)]
    for Orúkọ, Ìtayọ_iye, ìgúnrégé_932e03c8, iye in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + ìgúnrégé_932e03c8, 바뀐자료, Ìtayọ_iye, iye)
        시험사례.append((Orúkọ, bytes(바뀐자료)))
    탑재덩이들 = [(Orúkọ.replace('-', '_'), 출력결과 / (Orúkọ + '.elf')) for Orúkọ in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (Orúkọ, ojúlówó_détà_détà) in enumerate(시험사례):
        ọ̀nà = 출력결과 / ('invalid-{}.elf'.format(Orúkọ)); ọ̀nà.write_bytes(ojúlówó_détà_détà)
        탑재덩이들.append(('invalid_{}'.format(색인), ọ̀nà))
    어셈블리자료, àkọlé_iye = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Orúkọ, ọ̀nà in 탑재덩이들:
        àmì_iye = 'user_blob_' + Orúkọ
        크기목록[Orúkọ] = ọ̀nà.stat().st_size
        # 생성한 ọ̀gbà_iye 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + àmì_iye, àmì_iye + ':', '.incbin "{}"'.format(ọ̀nà.relative_to(기준경로))]
        àkọlé_iye.append('extern const unsigned char {}[];'.format(àmì_iye))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    àkọlé_iye += ['static const àtòjọ_ètò 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    àkọlé_iye += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    àkọlé_iye += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    àkọlé_iye += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], ìlànà_móòdù) for ìlànà_móòdù in (0, 1)]
    àkọlé_iye += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    àkọlé_iye += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    àkọlé_iye += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    àkọlé_iye += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    àkọlé_iye += ['};', 'static const àtòjọ_ètò 잘못된실행항목들[] = {']
    àkọlé_iye += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(ojúlówó_détà_détà)) for 순번, (_, ojúlówó_détà_détà) in enumerate(시험사례)]
    àkọlé_iye += ['};']
    (àtòpọ̀_ọ̀nà / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (àtòpọ̀_ọ̀nà / 'programs.h').write_text('\n'.join(àkọlé_iye) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Orúkọ for Orúkọ, _ in 시험사례) + '\n')
    ṣiṣẹ́_àṣẹ([시언어번역기] + 설정비트 + ['-c', àtòpọ̀_ọ̀nà / 'programs.S', '-o', àtòpọ̀_ọ̀nà / 'programs.o'])
