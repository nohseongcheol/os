"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def yila_umsebenzisi_isithuba(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, Uvimba_isixhobo_sokutayipha, 설정비트, ukwenza_umyalelo):
    설정비트 = [Iisetingi_ixabiso for Iisetingi_ixabiso in 설정비트 if Iisetingi_ixabiso != '-mgeneral-regs-only']
    yakha_indlela = 기준경로 / 'build'
    출력결과 = yakha_indlela / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'umsebenzisi'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, INDLELA, Igama in [
            (시언어번역기, [], 원본자료 / 'Phumeza.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ukwenza_umyalelo.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'umsebenzisi_ibhulorho.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Umhleli.c', 'vi.o')]:
        ukwenza_umyalelo([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', INDLELA, '-o', 출력결과 / Igama])
    ukwenza_umyalelo([Uvimba_isixhobo_sokutayipha, 'rcs', yakha_indlela / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Igama in ('demo', 'fault', 'network', 'vi'):
        ukwenza_umyalelo([연결편집기, '-T', 원본자료 / 'Ilinki_ubume.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Igama + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Igama + '.o'), yakha_indlela / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, ukwenza_umyalelo)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(yakha_indlela)) as 작업경로:
        iklasi_indlela = Path(작업경로)
        ukwenza_umyalelo(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', iklasi_indlela, '-sourcepath', iklasi_indlela, '-d', iklasi_indlela] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/umsebenzisi/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        ukwenza_umyalelo(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'isixhobo_sokutayipha_ufako_nkcukacha.Phumeza',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(iklasi_indlela.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for INDLELA, Igama in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'umqulu.c', 'jar.o')] + [(압축해제경로 / (Igama + '.c'), Igama + '.o') for Igama in ('tinflate', 'crc32', 'adler32')]:
        ukwenza_umyalelo([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', INDLELA, '-o', 출력결과 / Igama])
    ukwenza_umyalelo([연결편집기, '-T', 원본자료 / 'Ilinki_ubume.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Igama for Igama in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, ukwenza_umyalelo)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    inkqubo_Iheda_Ukulinganisa = struct.unpack_from('<Q', 유효함, 32)[0]
    Iheda_uludwe = [inkqubo_Iheda_Ukulinganisa + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in Iheda_uludwe if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    Umbhalo, iingcombolo = 적재구획[:2]
    umyalelo_idilesi = struct.unpack_from('<Q', 유효함, Umbhalo + 16)[0]
    iingcombolo_idilesi = struct.unpack_from('<Q', 유효함, iingcombolo + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', umyalelo_idilesi + 1), ('data-entry', 24, 'Q', iingcombolo_idilesi),
               ('outside-file', Umbhalo + 32, 'Q', len(유효함) + 1), ('short-memory', Umbhalo + 40, 'Q', 1),
               ('kernel-address', Umbhalo + 16, 'Q', 0x80000), ('memory-overflow', Umbhalo + 40, 'Q', 2**64 - 1),
               ('writable-code', Umbhalo + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Umbhalo, 'I', 2),
               ('unaligned-load', Umbhalo + 16, 'Q', umyalelo_idilesi + 8),
               ('overlap', iingcombolo + 16, 'Q', umyalelo_idilesi)]
    for Igama, Ukulinganisa_ixabiso, ifomathi, ixabiso in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + ifomathi, 바뀐자료, Ukulinganisa_ixabiso, ixabiso)
        시험사례.append((Igama, bytes(바뀐자료)))
    탑재덩이들 = [(Igama.replace('-', '_'), 출력결과 / (Igama + '.elf')) for Igama in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (Igama, umthwalo_wentlawulo_iingcombolo) in enumerate(시험사례):
        INDLELA = 출력결과 / ('invalid-{}.elf'.format(Igama)); INDLELA.write_bytes(umthwalo_wentlawulo_iingcombolo)
        탑재덩이들.append(('invalid_{}'.format(색인), INDLELA))
    어셈블리자료, Iheda_ixabiso = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Igama, INDLELA in 탑재덩이들:
        isimboli_ixabiso = 'user_blob_' + Igama
        크기목록[Igama] = INDLELA.stat().st_size
        # 생성한 untanga_ixabiso 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + isimboli_ixabiso, isimboli_ixabiso + ':', '.incbin "{}"'.format(INDLELA.relative_to(기준경로))]
        Iheda_ixabiso.append('extern const unsigned char {}[];'.format(isimboli_ixabiso))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Iheda_ixabiso += ['static const inkqubo 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Iheda_ixabiso += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Iheda_ixabiso += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Iheda_ixabiso += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], imethodi_imo) for imethodi_imo in (0, 1)]
    Iheda_ixabiso += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Iheda_ixabiso += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Iheda_ixabiso += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Iheda_ixabiso += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Iheda_ixabiso += ['};', 'static const inkqubo 잘못된실행항목들[] = {']
    Iheda_ixabiso += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(umthwalo_wentlawulo_iingcombolo)) for 순번, (_, umthwalo_wentlawulo_iingcombolo) in enumerate(시험사례)]
    Iheda_ixabiso += ['};']
    (yakha_indlela / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (yakha_indlela / 'programs.h').write_text('\n'.join(Iheda_ixabiso) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Igama for Igama, _ in 시험사례) + '\n')
    ukwenza_umyalelo([시언어번역기] + 설정비트 + ['-c', yakha_indlela / 'programs.S', '-o', yakha_indlela / 'programs.o'])
