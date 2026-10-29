"""독립된 内蔵 ABI ELF64와 로더 値却下 試験 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from Python構築 import Python作成
from Javaライブラリ構築 import Javaライブラリ作成
from Cコンパイラ構築 import Cコンパイラ作成


def 利用者空間作成(根経路, 保管庫経路, Cコンパイラ, Cppコンパイラ, 連結器道具要素, 書庫道具要素, 構成設定ビット列, 命令実行):
    構成設定ビット列 = [設定値値 for 設定値値 in 構成設定ビット列 if 設定値値 != '-mgeneral-regs-only']
    経路構築 = 根経路 / 'build'
    出力結果 = 経路構築 / 'user'
    出力結果.mkdir(exist_ok=True)
    原本データ = 根経路 / '利用者'
    POSIX = 保管庫経路 / 'posix-kor/arm64-native'
    包含経路 = ['-I', 原本データ, '-I', POSIX / 'ヘッダー', '-I', 出力結果]
    for コンパイラ道具要素, 追加分領域, 経路, 名前 in [
            (Cコンパイラ, [], 原本データ / '起動処理.S', 'start.o'),
            (Cコンパイラ, ['-std=c11'], 原本データ / '命令実行.c', 'runtime.o'),
            (Cコンパイラ, ['-std=c11'], POSIX / '利用者橋渡し.c', 'posix.o'),
            (Cppコンパイラ, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 原本データ / 'ファイル例.cpp', 'demo.o'),
            (Cppコンパイラ, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 原本データ / '通信用例.cpp', 'network.o'),
            (Cコンパイラ, ['-std=c11'], 原本データ / '保護試験.c', 'fault.o'),
            (Cコンパイラ, ['-std=c11'], 原本データ / '編集器.c', 'vi.o')]:
        命令実行([コンパイラ道具要素] + 構成設定ビット列 + 追加分領域 + 包含経路 + ['-Wall', '-Wextra', '-Werror', '-c', 経路, '-o', 出力結果 / 名前])
    命令実行([書庫道具要素, 'rcs', 経路構築 / 'libposix-kor-user.a', 出力結果 / 'posix.o'])
    for 名前 in ('demo', 'fault', 'network', 'vi'):
        命令実行([連結器道具要素, '-T', 原本データ / '連結配置.ld', '-z', 'max-page-size=4096', '-o', 出力結果 / (名前 + '.elf'),
             出力結果 / 'start.o', 出力結果 / 'runtime.o', 出力結果 / (名前 + '.o'), 経路構築 / 'libposix-kor-user.a'])
    Javaライブラリ作成(根経路, 命令実行)
    # 기존 内蔵 Java コンパイラ/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(経路構築)) as 作業中経路:
        クラス経路 = Path(作業中経路)
        命令実行(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', クラス経路, '-sourcepath', クラス経路, '-d', クラス経路] +
            [データ位置 for データ位置 in sorted((保管庫経路 / 'os/利用者/Java').glob('*.java')) if データ位置.name != 'Java仮想機械.java'] + sorted((原本データ / 'Java').glob('*.java')))
        命令実行(['sh', 保管庫経路 / 'compiler/事前用時間.sh', '--entry', '道具要素入口.起動処理',
             '--profile', 'user', '--heap-words', '1048576', '-o', 出力結果 / 'java-tools.c'] + sorted(クラス経路.glob('*.class')))
    解凍ライブラリ = 根経路 / 'vendor/uzlib'
    for 経路, 名前 in [(出力結果 / 'java-tools.c', 'java-tools.o'), (原本データ / 'Java橋渡し.c', 'java-link.o'),
                       (原本データ / 'パッケージ.c', 'jar.o')] + [(解凍ライブラリ / (名前 + '.c'), 名前 + '.o') for 名前 in ('tinflate', 'crc32', 'adler32')]:
        命令実行([Cコンパイラ] + 構成設定ビット列 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 解凍ライブラリ] + 包含経路 + ['-c', 経路, '-o', 出力結果 / 名前])
    命令実行([連結器道具要素, '-T', 原本データ / '連結配置.ld', '-z', 'max-page-size=4096', '-o', 出力結果 / 'java-tools.elf'] +
        [出力結果 / 名前 for 名前 in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Python作成(根経路, Cコンパイラ, 連結器道具要素)
    Cコンパイラ作成(根経路, 保管庫経路, Cコンパイラ, 連結器道具要素, 構成設定ビット列, 命令実行)
    妥当 = (出力結果 / 'demo.elf').read_bytes()
    プログラムヘッダー変位量 = struct.unpack_from('<Q', 妥当, 32)[0]
    ヘッダー一覧 = [プログラムヘッダー変位量 + 項目個数 * 56 for 項目個数 in range(struct.unpack_from('<H', 妥当, 56)[0])]
    読込項目 = [データ位置 for データ位置 in ヘッダー一覧 if struct.unpack_from('<I', 妥当, データ位置)[0] == 1]
    文, データ = 読込項目[:2]
    命令番地 = struct.unpack_from('<Q', 妥当, 文 + 16)[0]
    データ番地 = struct.unpack_from('<Q', 妥当, データ + 16)[0]
    呼出しABI = 妥当.index(b'JKOROS\0')
    場合試験 = [('empty', b''), ('short', 妥当[:63])]
    変更一覧 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', 命令番地 + 1), ('data-entry', 24, 'Q', データ番地),
               ('outside-file', 文 + 32, 'Q', len(妥当) + 1), ('short-memory', 文 + 40, 'Q', 1),
               ('kernel-address', 文 + 16, 'Q', 0x80000), ('memory-overflow', 文 + 40, 'Q', 2**64 - 1),
               ('writable-code', 文 + 4, 'I', 7), ('missing-abi', 呼出しABI, 'B', ord('X')),
               ('wrong-abi', 呼出しABI + 8, 'I', 2), ('dynamic', 文, 'I', 2),
               ('unaligned-load', 文 + 16, 'Q', 命令番地 + 8),
               ('overlap', データ + 16, 'Q', 命令番地)]
    for 名前, 変位量値, データ書式, 値 in 変更一覧:
        変更済み = bytearray(妥当); struct.pack_into('<' + データ書式, 変更済み, 変位量値, 値)
        場合試験.append((名前, bytes(変更済み)))
    二進資料群 = [(名前.replace('-', '_'), 出力結果 / (名前 + '.elf')) for 名前 in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 検索添字, (名前, 本文データデータ) in enumerate(場合試験):
        経路 = 出力結果 / ('invalid-{}.elf'.format(名前)); 経路.write_bytes(本文データデータ)
        二進資料群.append(('invalid_{}'.format(検索添字), 経路))
    アセンブリ, ヘッダー値 = ['.section .rodata.user,"a"'], []
    容量一覧 = {}
    for 名前, 経路 in 二進資料群:
        記号値 = 'user_blob_' + 名前
        容量一覧[名前] = 経路.stat().st_size
        # 생성한 通信相手値 경로만 넣어 프로젝트 경로의 공백/引用 영향을 피한다.
        アセンブリ += ['.balign 16', '.global ' + 記号値, 記号値 + ':', '.incbin "{}"'.format(経路.relative_to(根経路))]
        ヘッダー値.append('extern const unsigned char {}[];'.format(記号値))
    アセンブリ.append('.section .note.GNU-stack,"",%progbits')
    ヘッダー値 += ['static const 実行項目 実行形式登録項目一覧[] = {', '{user_blob_demo, %d, 0},' % 容量一覧['demo']]
    ヘッダー値 += ['{user_blob_fault, %d, %d},' % (容量一覧['fault'], 転送済み値) for 転送済み値 in range(8)]
    ヘッダー値 += ['{user_blob_network, %d, 0},' % 容量一覧['network']]
    ヘッダー値 += ['{user_blob_java_tools, %d, %d},' % (容量一覧['java_tools'], メソッド方式) for メソッド方式 in (0, 1)]
    ヘッダー値 += ['{user_blob_python, %d, 0},' % 容量一覧['python'], '{user_blob_vi, %d, 0},' % 容量一覧['vi']]
    ヘッダー値 += ['{user_blob_java_tools, %d, 2},' % 容量一覧['java_tools']]
    ヘッダー値 += ['{user_blob_cc, %d, 0},' % 容量一覧['cc']]
    ヘッダー値 += ['{user_blob_cc, %d, 1},' % 容量一覧['cc']]
    ヘッダー値 += ['};', 'static const 実行項目 無効実行形式一覧[] = {']
    ヘッダー値 += ['{user_blob_invalid_%d, %d, 0},' % (序数添字, len(本文データデータ)) for 序数添字, (_, 本文データデータ) in enumerate(場合試験)]
    ヘッダー値 += ['};']
    (経路構築 / 'programs.S').write_text('\n'.join(アセンブリ) + '\n')
    (経路構築 / 'programs.h').write_text('\n'.join(ヘッダー値) + '\n')
    (出力結果 / 'invalid-cases.txt').write_text('\n'.join(名前 for 名前, _ in 場合試験) + '\n')
    命令実行([Cコンパイラ] + 構成設定ビット列 + ['-c', 経路構築 / 'programs.S', '-o', 経路構築 / 'programs.o'])
