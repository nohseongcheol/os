"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def kurema_ukoresha_akanya(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, gushyingura_igikoresho, 설정비트, gukora_ibwiriza):
    설정비트 = [Amagenamiterere_agaciro for Amagenamiterere_agaciro in 설정비트 if Amagenamiterere_agaciro != '-mgeneral-regs-only']
    gusohora_inzira = 기준경로 / 'build'
    출력결과 = gusohora_inzira / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'ukoresha'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, Inzira, Izina in [
            (시언어번역기, [], 원본자료 / 'ihuriro.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'gukora_ibwiriza.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / '사용자연결.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Muhindura.c', 'vi.o')]:
        gukora_ibwiriza([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', Inzira, '-o', 출력결과 / Izina])
    gukora_ibwiriza([gushyingura_igikoresho, 'rcs', gusohora_inzira / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Izina in ('demo', 'fault', 'network', 'vi'):
        gukora_ibwiriza([연결편집기, '-T', 원본자료 / 'Ihuza_Imimerere.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Izina + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Izina + '.o'), gusohora_inzira / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, gukora_ibwiriza)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(gusohora_inzira)) as 작업경로:
        icyiciro_inzira = Path(작업경로)
        gukora_ibwiriza(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', icyiciro_inzira, '-sourcepath', icyiciro_inzira, '-d', icyiciro_inzira] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/ukoresha/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        gukora_ibwiriza(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'igikoresho_icyinjizwa.ihuriro',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(icyiciro_inzira.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for Inzira, Izina in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'ipaki.c', 'jar.o')] + [(압축해제경로 / (Izina + '.c'), Izina + '.o') for Izina in ('tinflate', 'crc32', 'adler32')]:
        gukora_ibwiriza([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', Inzira, '-o', 출력결과 / Izina])
    gukora_ibwiriza([연결편집기, '-T', 원본자료 / 'Ihuza_Imimerere.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Izina for Izina in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, gukora_ibwiriza)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    porogaramu_Umutwengaruka_Ofuseti = struct.unpack_from('<Q', 유효함, 32)[0]
    Umutwengaruka_Urutonde = [porogaramu_Umutwengaruka_Ofuseti + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in Umutwengaruka_Urutonde if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    Umwandiko, amakurushingiro = 적재구획[:2]
    ibwiriza_aderesi = struct.unpack_from('<Q', 유효함, Umwandiko + 16)[0]
    amakurushingiro_aderesi = struct.unpack_from('<Q', 유효함, amakurushingiro + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', ibwiriza_aderesi + 1), ('data-entry', 24, 'Q', amakurushingiro_aderesi),
               ('outside-file', Umwandiko + 32, 'Q', len(유효함) + 1), ('short-memory', Umwandiko + 40, 'Q', 1),
               ('kernel-address', Umwandiko + 16, 'Q', 0x80000), ('memory-overflow', Umwandiko + 40, 'Q', 2**64 - 1),
               ('writable-code', Umwandiko + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Umwandiko, 'I', 2),
               ('unaligned-load', Umwandiko + 16, 'Q', ibwiriza_aderesi + 8),
               ('overlap', amakurushingiro + 16, 'Q', ibwiriza_aderesi)]
    for Izina, Ofuseti_agaciro, imiterere_932e03c8, agaciro in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + imiterere_932e03c8, 바뀐자료, Ofuseti_agaciro, agaciro)
        시험사례.append((Izina, bytes(바뀐자료)))
    탑재덩이들 = [(Izina.replace('-', '_'), 출력결과 / (Izina + '.elf')) for Izina in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (Izina, ibitwarwa_amakurushingiro) in enumerate(시험사례):
        Inzira = 출력결과 / ('invalid-{}.elf'.format(Izina)); Inzira.write_bytes(ibitwarwa_amakurushingiro)
        탑재덩이들.append(('invalid_{}'.format(색인), Inzira))
    어셈블리자료, Umutwengaruka_agaciro = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Izina, Inzira in 탑재덩이들:
        ikimenyetso_agaciro = 'user_blob_' + Izina
        크기목록[Izina] = Inzira.stat().st_size
        # 생성한 Mugenzi_agaciro 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + ikimenyetso_agaciro, ikimenyetso_agaciro + ':', '.incbin "{}"'.format(Inzira.relative_to(기준경로))]
        Umutwengaruka_agaciro.append('extern const unsigned char {}[];'.format(ikimenyetso_agaciro))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Umutwengaruka_agaciro += ['static const porogaramu 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Umutwengaruka_agaciro += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Umutwengaruka_agaciro += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Umutwengaruka_agaciro += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], uburyo_uburyo) for uburyo_uburyo in (0, 1)]
    Umutwengaruka_agaciro += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Umutwengaruka_agaciro += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Umutwengaruka_agaciro += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Umutwengaruka_agaciro += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Umutwengaruka_agaciro += ['};', 'static const porogaramu 잘못된실행항목들[] = {']
    Umutwengaruka_agaciro += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(ibitwarwa_amakurushingiro)) for 순번, (_, ibitwarwa_amakurushingiro) in enumerate(시험사례)]
    Umutwengaruka_agaciro += ['};']
    (gusohora_inzira / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (gusohora_inzira / 'programs.h').write_text('\n'.join(Umutwengaruka_agaciro) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Izina for Izina, _ in 시험사례) + '\n')
    gukora_ibwiriza([시언어번역기] + 설정비트 + ['-c', gusohora_inzira / 'programs.S', '-o', gusohora_inzira / 'programs.o'])
