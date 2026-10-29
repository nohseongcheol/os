"""内蔵 JVM용 日本語 class/JAR와 EL0에 넣을 読取 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def Javaライブラリ作成(根経路, 命令実行):
    (根経路 / 'build/user').mkdir(parents=True, exist_ok=True)
    出力結果 = 根経路 / 'build/java-library'
    クラス経路 = 出力結果 / 'classes'
    クラス経路.mkdir(parents=True, exist_ok=True)
    ソース一覧 = sorted((根経路 / '日本語Java').rglob('*.java'))
    命令実行(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', クラス経路] + ソース一覧)
    登録項目一覧一覧 = []
    for 原本番地 in ソース一覧:
        相対経路 = 原本番地.relative_to(根経路 / '日本語Java').with_suffix('.class')
        本文データデータ = (クラス経路 / 相対経路).read_bytes()
        名前 = str(相対経路).replace('/', '.')
        if len(本文データデータ) > 16384 or len(名前.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + 名前)
        登録項目一覧一覧.append((相対経路, 名前, 本文データデータ))
    ヘッダー値 = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *名前; const unsigned char *データ; unsigned 容量; } Javaクラス資源;']
    for 序数添字, (_, 名前, 本文データデータ) in enumerate(登録項目一覧一覧):
        ヘッダー値.append('static const unsigned char Javaクラスデータ%d[] = {%s};' % (序数添字, ','.join(str(第二値) for 第二値 in 本文データデータ)))
    ヘッダー値.append('static const Javaクラス資源 Javaクラス一覧[] = {')
    for 序数添字, (_, 名前, 本文データデータ) in enumerate(登録項目一覧一覧):
        ヘッダー値.append('{%s, Javaクラスデータ%d, %d},' % (json.dumps(名前, ensure_ascii=False), 序数添字, len(本文データデータ)))
    ヘッダー値.append('};')
    (根経路 / 'build/user/java-resources.h').write_text('\n'.join(ヘッダー値) + '\n', encoding='utf-8')
    配布経路 = 根経路 / 'dist'; 配布経路.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(配布経路 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as Java束:
        for 相対経路, _, 本文データデータ in 登録項目一覧一覧:
            システム情報 = zipfile.ZipInfo(str(相対経路), date_time=(1980, 1, 1, 0, 0, 0)); システム情報.compress_type = zipfile.ZIP_DEFLATED
            Java束.writestr(システム情報, 本文データデータ)
    with zipfile.ZipFile(str(配布経路 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as 書庫:
        for 原本番地 in ソース一覧:
            システム情報 = zipfile.ZipInfo(str(原本番地.relative_to(根経路 / '日本語Java')), date_time=(1980, 1, 1, 0, 0, 0)); システム情報.compress_type = zipfile.ZIP_DEFLATED
            書庫.writestr(システム情報, 原本番地.read_bytes())
