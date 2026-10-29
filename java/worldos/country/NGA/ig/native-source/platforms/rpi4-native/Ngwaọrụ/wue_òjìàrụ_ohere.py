"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def mepụta_òjìàrụ_ohere(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, ọkpụ_ngwaọrụ, 설정비트, mee_nnyemiwu):
    설정비트 = [Mwube_valuu for Mwube_valuu in 설정비트 if Mwube_valuu != '-mgeneral-regs-only']
    wue_ụzọ_ozi = 기준경로 / 'build'
    출력결과 = wue_ụzọ_ozi / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'òjìàrụ'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, ụzọ_ozi, Aha in [
            (시언어번역기, [], 원본자료 / 'Bido.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'mee_nnyemiwu.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / '사용자연결.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'òdezi.c', 'vi.o')]:
        mee_nnyemiwu([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', ụzọ_ozi, '-o', 출력결과 / Aha])
    mee_nnyemiwu([ọkpụ_ngwaọrụ, 'rcs', wue_ụzọ_ozi / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Aha in ('demo', 'fault', 'network', 'vi'):
        mee_nnyemiwu([연결편집기, '-T', 원본자료 / 'Njikọ_Nhàzi.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Aha + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Aha + '.o'), wue_ụzọ_ozi / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, mee_nnyemiwu)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(wue_ụzọ_ozi)) as 작업경로:
        klaàsị_ụzọ_ozi = Path(작업경로)
        mee_nnyemiwu(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klaàsị_ụzọ_ozi, '-sourcepath', klaàsị_ụzọ_ozi, '-d', klaàsị_ụzọ_ozi] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/òjìàrụ/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        mee_nnyemiwu(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'ngwaọrụ_ndebà.Bido',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(klaàsị_ụzọ_ozi.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for ụzọ_ozi, Aha in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'ngwungwu.c', 'jar.o')] + [(압축해제경로 / (Aha + '.c'), Aha + '.o') for Aha in ('tinflate', 'crc32', 'adler32')]:
        mee_nnyemiwu([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', ụzọ_ozi, '-o', 출력결과 / Aha])
    mee_nnyemiwu([연결편집기, '-T', 원본자료 / 'Njikọ_Nhàzi.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Aha for Aha in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, mee_nnyemiwu)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    app_isi_Nnokwata = struct.unpack_from('<Q', 유효함, 32)[0]
    isi_ndepụta = [app_isi_Nnokwata + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in isi_ndepụta if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    SMS, datà = 적재구획[:2]
    nnyemiwu_àdreèsì = struct.unpack_from('<Q', 유효함, SMS + 16)[0]
    datà_àdreèsì = struct.unpack_from('<Q', 유효함, datà + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', nnyemiwu_àdreèsì + 1), ('data-entry', 24, 'Q', datà_àdreèsì),
               ('outside-file', SMS + 32, 'Q', len(유효함) + 1), ('short-memory', SMS + 40, 'Q', 1),
               ('kernel-address', SMS + 16, 'Q', 0x80000), ('memory-overflow', SMS + 40, 'Q', 2**64 - 1),
               ('writable-code', SMS + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', SMS, 'I', 2),
               ('unaligned-load', SMS + 16, 'Q', nnyemiwu_àdreèsì + 8),
               ('overlap', datà + 16, 'Q', nnyemiwu_àdreèsì)]
    for Aha, Nnokwata_valuu, nsìrìhazi, valuu in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + nsìrìhazi, 바뀐자료, Nnokwata_valuu, valuu)
        시험사례.append((Aha, bytes(바뀐자료)))
    탑재덩이들 = [(Aha.replace('-', '_'), 출력결과 / (Aha + '.elf')) for Aha in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (Aha, ebe_mbulingwa_datà) in enumerate(시험사례):
        ụzọ_ozi = 출력결과 / ('invalid-{}.elf'.format(Aha)); ụzọ_ozi.write_bytes(ebe_mbulingwa_datà)
        탑재덩이들.append(('invalid_{}'.format(색인), ụzọ_ozi))
    어셈블리자료, isi_valuu = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Aha, ụzọ_ozi in 탑재덩이들:
        adimara_valuu = 'user_blob_' + Aha
        크기목록[Aha] = ụzọ_ozi.stat().st_size
        # 생성한 ibè_valuu 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + adimara_valuu, adimara_valuu + ':', '.incbin "{}"'.format(ụzọ_ozi.relative_to(기준경로))]
        isi_valuu.append('extern const unsigned char {}[];'.format(adimara_valuu))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    isi_valuu += ['static const app 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    isi_valuu += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    isi_valuu += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    isi_valuu += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], usoro_moòdù) for usoro_moòdù in (0, 1)]
    isi_valuu += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    isi_valuu += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    isi_valuu += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    isi_valuu += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    isi_valuu += ['};', 'static const app 잘못된실행항목들[] = {']
    isi_valuu += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(ebe_mbulingwa_datà)) for 순번, (_, ebe_mbulingwa_datà) in enumerate(시험사례)]
    isi_valuu += ['};']
    (wue_ụzọ_ozi / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (wue_ụzọ_ozi / 'programs.h').write_text('\n'.join(isi_valuu) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Aha for Aha, _ in 시험사례) + '\n')
    mee_nnyemiwu([시언어번역기] + 설정비트 + ['-c', wue_ụzọ_ozi / 'programs.S', '-o', wue_ụzọ_ozi / 'programs.o'])
