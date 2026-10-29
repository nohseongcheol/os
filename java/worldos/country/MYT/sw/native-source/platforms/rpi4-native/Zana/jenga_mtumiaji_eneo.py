"""독립된 자체 ABI ELF64와 로더 kataa_thamani 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def unda_mtumiaji_eneo(기준경로, uwekaji_njia, 시언어번역기, 시플플번역기, 연결편집기, Hifadhi_zana, usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma, tekeleza_amri):
    usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma = [Mipangilio_thamani for Mipangilio_thamani in usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma if Mipangilio_thamani != '-mgeneral-regs-only']
    jenga_njia = 기준경로 / 'build'
    출력결과 = jenga_njia / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'mtumiaji'
    포직스경로 = uwekaji_njia / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, njia, Jina in [
            (시언어번역기, [], 원본자료 / 'endesha.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'tekeleza_amri.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'mtumiaji_daraja.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Kihariri.c', 'vi.o')]:
        tekeleza_amri([번역기] + usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', njia, '-o', 출력결과 / Jina])
    tekeleza_amri([Hifadhi_zana, 'rcs', jenga_njia / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Jina in ('demo', 'fault', 'network', 'vi'):
        tekeleza_amri([연결편집기, '-T', 원본자료 / 'Kiungo_Muundo.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Jina + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Jina + '.o'), jenga_njia / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, tekeleza_amri)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(jenga_njia)) as 작업경로:
        tabaka_njia = Path(작업경로)
        tekeleza_amri(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', tabaka_njia, '-sourcepath', tabaka_njia, '-d', tabaka_njia] +
            [자료위치 for 자료위치 in sorted((uwekaji_njia / 'os/mtumiaji/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        tekeleza_amri(['sh', uwekaji_njia / 'compiler/미리번역.sh', '--entry', 'zana_ingizo.endesha',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(tabaka_njia.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for njia, Jina in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'fungasha.c', 'jar.o')] + [(압축해제경로 / (Jina + '.c'), Jina + '.o') for Jina in ('tinflate', 'crc32', 'adler32')]:
        tekeleza_amri([시언어번역기] + usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', njia, '-o', 출력결과 / Jina])
    tekeleza_amri([연결편집기, '-T', 원본자료 / 'Kiungo_Muundo.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Jina for Jina in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, uwekaji_njia, 시언어번역기, 연결편집기, usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma, tekeleza_amri)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    programu_kichwa_Chipua = struct.unpack_from('<Q', 유효함, 32)[0]
    kichwa_Orodha = [programu_kichwa_Chipua + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in kichwa_Orodha if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    SMS, data = 적재구획[:2]
    amri_anwani = struct.unpack_from('<Q', 유효함, SMS + 16)[0]
    data_anwani = struct.unpack_from('<Q', 유효함, data + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', amri_anwani + 1), ('data-entry', 24, 'Q', data_anwani),
               ('outside-file', SMS + 32, 'Q', len(유효함) + 1), ('short-memory', SMS + 40, 'Q', 1),
               ('kernel-address', SMS + 16, 'Q', 0x80000), ('memory-overflow', SMS + 40, 'Q', 2**64 - 1),
               ('writable-code', SMS + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', SMS, 'I', 2),
               ('unaligned-load', SMS + 16, 'Q', amri_anwani + 8),
               ('overlap', data + 16, 'Q', amri_anwani)]
    for Jina, Chipua_thamani, umbizo, thamani in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + umbizo, 바뀐자료, Chipua_thamani, thamani)
        시험사례.append((Jina, bytes(바뀐자료)))
    탑재덩이들 = [(Jina.replace('-', '_'), 출력결과 / (Jina + '.elf')) for Jina in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (Jina, data_muhimu_data) in enumerate(시험사례):
        njia = 출력결과 / ('invalid-{}.elf'.format(Jina)); njia.write_bytes(data_muhimu_data)
        탑재덩이들.append(('invalid_{}'.format(색인), njia))
    어셈블리자료, kichwa_thamani = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Jina, njia in 탑재덩이들:
        ishara_thamani = 'user_blob_' + Jina
        크기목록[Jina] = njia.stat().st_size
        # 생성한 kompyuta_rika_thamani 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + ishara_thamani, ishara_thamani + ':', '.incbin "{}"'.format(njia.relative_to(기준경로))]
        kichwa_thamani.append('extern const unsigned char {}[];'.format(ishara_thamani))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    kichwa_thamani += ['static const programu 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    kichwa_thamani += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    kichwa_thamani += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    kichwa_thamani += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], mbinu_hali_tumizi) for mbinu_hali_tumizi in (0, 1)]
    kichwa_thamani += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    kichwa_thamani += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    kichwa_thamani += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    kichwa_thamani += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    kichwa_thamani += ['};', 'static const programu 잘못된실행항목들[] = {']
    kichwa_thamani += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(data_muhimu_data)) for 순번, (_, data_muhimu_data) in enumerate(시험사례)]
    kichwa_thamani += ['};']
    (jenga_njia / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (jenga_njia / 'programs.h').write_text('\n'.join(kichwa_thamani) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Jina for Jina, _ in 시험사례) + '\n')
    tekeleza_amri([시언어번역기] + usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma + ['-c', jenga_njia / 'programs.S', '-o', jenga_njia / 'programs.o'])
