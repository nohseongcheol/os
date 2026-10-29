"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 构建Java库 import 创建Java库


def 创建用例集(根路径, 代码库路径, 执行命令):
    原始数据=代码库路径/'example';结果数据=根路径/'build/examples';结果数据.mkdir(parents=True,exist_ok=True)
    类路径=结果数据/'classes';类路径.mkdir(exist_ok=True)
    创建Java库(根路径,执行命令)
    ip_settings = read_config(根路径)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 结果数据/'java-source'; java_sources.mkdir(exist_ok=True)
    执行Java=[]
    for path in sorted((原始数据/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 执行Java.append(target)
    执行命令(['javac','--release','8','-encoding','UTF-8','-cp',根路径/'build/java-library/classes','-d',类路径]+执行Java)
    指令序列=['public final class 示例捆绑 { public static int 安装值(int 语言) { int 已处理值;',
          '已处理值=命令解释器.示例目录("/example"); if(已处理值<0)return 已处理值;']
    捆绑构建清单={}
    自述文件=guest_bytes(原始数据/'README.md')
    if len(自述文件)>16384: raise ValueError('example README exceeds native VFS limit')
    指令序列.append('已处理值=命令解释器.示例文件("/example/README.md","%s"); if(已处理值<0)return 已处理值;'%自述文件.hex())
    捆绑构建清单['/example/README.md']={'bytes':len(自述文件),'sha256':hashlib.sha256(自述文件).hexdigest()}
    指令序列.append('if(语言==0){已处理值=命令解释器.示例目录("/lib"); if(已处理值<0)return 已处理值;')
    for 路径 in [原始数据/'python/中文.py'] + sorted((根路径/'Python桥接/库').glob('*.py')):
        内容值=guest_bytes(路径);目标值='/lib/'+路径.name
        if len(内容值)>16384 or len(目标值.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+目标值)
        指令序列.append('已处理值=命令解释器.示例文件(%s,"%s"); if(已处理值<0)return 已处理值;'%(json.dumps(目标值,ensure_ascii=True),内容值.hex()))
        捆绑构建清单[目标值]={'bytes':len(内容值),'sha256':hashlib.sha256(内容值).hexdigest()}
    指令序列.append('}')
    for 查找索引,语言 in enumerate(('java','c','python')):
        文件列表=[(数据位置.name,数据位置) for 数据位置 in sorted((原始数据/语言).iterdir()) if 数据位置.is_file()]
        if 语言=='java':文件列表 += [(数据位置.stem+'.class',类路径/(数据位置.stem+'.class')) for 数据位置 in 执行Java]
        指令序列 += ['if(语言==%d){'%查找索引,'已处理值=命令解释器.示例目录("/example/%s"); if(已处理值<0)return 已处理值;'%语言]
        for 名称,路径 in 文件列表:
            内容值=guest_bytes(路径);目标值='/example/'+语言+'/'+名称
            if len(内容值)>16384 or len(目标值.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+目标值)
            指令序列.append('已处理值=命令解释器.示例文件(%s,"%s"); if(已处理值<0)return 已处理值;'%(json.dumps(目标值,ensure_ascii=True),内容值.hex()))
            捆绑构建清单[目标值]={'bytes':len(内容值),'sha256':hashlib.sha256(内容值).hexdigest()}
        指令序列 += ['return 0;}']
    指令序列 += ['return -22;}}']
    (根路径/'build/示例捆绑.java').write_text('\n'.join(指令序列)+'\n')
    (结果数据/'manifest.json').write_text(json.dumps(捆绑构建清单,ensure_ascii=False,indent=2)+'\n')
