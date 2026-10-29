"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 構建Java庫 import 創建Java庫


def 創建範例集(根路徑, 代碼庫路徑, 執行命令):
    原始資料=代碼庫路徑/'example';結果資料=根路徑/'build/examples';結果資料.mkdir(parents=True,exist_ok=True)
    類別路徑=結果資料/'classes';類別路徑.mkdir(exist_ok=True)
    創建Java庫(根路徑,執行命令)
    ip_settings = read_config(根路徑)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 結果資料/'java-source'; java_sources.mkdir(exist_ok=True)
    執行Java=[]
    for path in sorted((原始資料/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 執行Java.append(target)
    執行命令(['javac','--release','8','-encoding','UTF-8','-cp',根路徑/'build/java-library/classes','-d',類別路徑]+執行Java)
    指令序列=['public final class 範例捆綁 { public static int 安裝值(int 語言) { int 已處理值;',
          '已處理值=命令解釋器.範例目錄("/example"); if(已處理值<0)return 已處理值;']
    捆綁構建清單={}
    自述文件=guest_bytes(原始資料/'README.md')
    if len(自述文件)>16384: raise ValueError('example README exceeds native VFS limit')
    指令序列.append('已處理值=命令解釋器.範例檔案("/example/README.md","%s"); if(已處理值<0)return 已處理值;'%自述文件.hex())
    捆綁構建清單['/example/README.md']={'bytes':len(自述文件),'sha256':hashlib.sha256(自述文件).hexdigest()}
    指令序列.append('if(語言==0){已處理值=命令解釋器.範例目錄("/lib"); if(已處理值<0)return 已處理值;')
    for 路徑 in [原始資料/'python/中文.py'] + sorted((根路徑/'Python橋接/庫').glob('*.py')):
        內容值=guest_bytes(路徑);目標值='/lib/'+路徑.name
        if len(內容值)>16384 or len(目標值.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+目標值)
        指令序列.append('已處理值=命令解釋器.範例檔案(%s,"%s"); if(已處理值<0)return 已處理值;'%(json.dumps(目標值,ensure_ascii=True),內容值.hex()))
        捆綁構建清單[目標值]={'bytes':len(內容值),'sha256':hashlib.sha256(內容值).hexdigest()}
    指令序列.append('}')
    for 查找索引,語言 in enumerate(('java','c','python')):
        檔案列表=[(資料位置.name,資料位置) for 資料位置 in sorted((原始資料/語言).iterdir()) if 資料位置.is_file()]
        if 語言=='java':檔案列表 += [(資料位置.stem+'.class',類別路徑/(資料位置.stem+'.class')) for 資料位置 in 執行Java]
        指令序列 += ['if(語言==%d){'%查找索引,'已處理值=命令解釋器.範例目錄("/example/%s"); if(已處理值<0)return 已處理值;'%語言]
        for 名稱,路徑 in 檔案列表:
            內容值=guest_bytes(路徑);目標值='/example/'+語言+'/'+名稱
            if len(內容值)>16384 or len(目標值.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+目標值)
            指令序列.append('已處理值=命令解釋器.範例檔案(%s,"%s"); if(已處理值<0)return 已處理值;'%(json.dumps(目標值,ensure_ascii=True),內容值.hex()))
            捆綁構建清單[目標值]={'bytes':len(內容值),'sha256':hashlib.sha256(內容值).hexdigest()}
        指令序列 += ['return 0;}']
    指令序列 += ['return -22;}}']
    (根路徑/'build/範例捆綁.java').write_text('\n'.join(指令序列)+'\n')
    (結果資料/'manifest.json').write_text(json.dumps(捆綁構建清單,ensure_ascii=False,indent=2)+'\n')
