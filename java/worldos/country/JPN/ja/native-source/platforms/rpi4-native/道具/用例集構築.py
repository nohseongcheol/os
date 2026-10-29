"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from Javaライブラリ構築 import Javaライブラリ作成


def 用例集作成(根経路, 保管庫経路, 命令実行):
    原本データ=保管庫経路/'example';結果データ=根経路/'build/examples';結果データ.mkdir(parents=True,exist_ok=True)
    クラス経路=結果データ/'classes';クラス経路.mkdir(exist_ok=True)
    Javaライブラリ作成(根経路,命令実行)
    ip_settings = read_config(根経路)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 結果データ/'java-source'; java_sources.mkdir(exist_ok=True)
    Java実行=[]
    for path in sorted((原本データ/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); Java実行.append(target)
    命令実行(['javac','--release','8','-encoding','UTF-8','-cp',根経路/'build/java-library/classes','-d',クラス経路]+Java実行)
    命令語列順=['public final class 例束 { public static int 値導入(int 言語) { int 処理済み値;',
          '処理済み値=命令解釈器.例ディレクトリ("/example"); if(処理済み値<0)return 処理済み値;']
    束管理目録={}
    案内書=guest_bytes(原本データ/'README.md')
    if len(案内書)>16384: raise ValueError('example README exceeds native VFS limit')
    命令語列順.append('処理済み値=命令解釈器.例ファイル("/example/README.md","%s"); if(処理済み値<0)return 処理済み値;'%案内書.hex())
    束管理目録['/example/README.md']={'bytes':len(案内書),'sha256':hashlib.sha256(案内書).hexdigest()}
    命令語列順.append('if(言語==0){処理済み値=命令解釈器.例ディレクトリ("/lib"); if(処理済み値<0)return 処理済み値;')
    for 経路 in [原本データ/'python/日本語.py'] + sorted((根経路/'Python橋渡し/ライブラリ').glob('*.py')):
        内容物値=guest_bytes(経路);対象値='/lib/'+経路.name
        if len(内容物値)>16384 or len(対象値.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+対象値)
        命令語列順.append('処理済み値=命令解釈器.例ファイル(%s,"%s"); if(処理済み値<0)return 処理済み値;'%(json.dumps(対象値,ensure_ascii=True),内容物値.hex()))
        束管理目録[対象値]={'bytes':len(内容物値),'sha256':hashlib.sha256(内容物値).hexdigest()}
    命令語列順.append('}')
    for 検索添字,言語 in enumerate(('java','c','python')):
        ファイル一覧=[(データ位置.name,データ位置) for データ位置 in sorted((原本データ/言語).iterdir()) if データ位置.is_file()]
        if 言語=='java':ファイル一覧 += [(データ位置.stem+'.class',クラス経路/(データ位置.stem+'.class')) for データ位置 in Java実行]
        命令語列順 += ['if(言語==%d){'%検索添字,'処理済み値=命令解釈器.例ディレクトリ("/example/%s"); if(処理済み値<0)return 処理済み値;'%言語]
        for 名前,経路 in ファイル一覧:
            内容物値=guest_bytes(経路);対象値='/example/'+言語+'/'+名前
            if len(内容物値)>16384 or len(対象値.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+対象値)
            命令語列順.append('処理済み値=命令解釈器.例ファイル(%s,"%s"); if(処理済み値<0)return 処理済み値;'%(json.dumps(対象値,ensure_ascii=True),内容物値.hex()))
            束管理目録[対象値]={'bytes':len(内容物値),'sha256':hashlib.sha256(内容物値).hexdigest()}
        命令語列順 += ['return 0;}']
    命令語列順 += ['return -22;}}']
    (根経路/'build/例束.java').write_text('\n'.join(命令語列順)+'\n')
    (結果データ/'manifest.json').write_text(json.dumps(束管理目録,ensure_ascii=False,indent=2)+'\n')
