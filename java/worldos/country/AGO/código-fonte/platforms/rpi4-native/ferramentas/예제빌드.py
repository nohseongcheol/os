"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(raiz_caminho, repositório_caminho, Executar_comando):
    원본자료=repositório_caminho/'example';RC_dados=raiz_caminho/'build/examples';RC_dados.mkdir(parents=True,exist_ok=True)
    aula_caminho=RC_dados/'classes';aula_caminho.mkdir(exist_ok=True)
    자바라이브러리만들기(raiz_caminho,Executar_comando)
    ip_settings = read_config(raiz_caminho)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = RC_dados/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    Executar_comando(['javac','--release','8','-encoding','UTF-8','-cp',raiz_caminho/'build/java-library/classes','-d',aula_caminho]+자바실행)
    instrução_SEQUÊNCIA=['public final class 예제꾸러미 { public static int instalar_VALOR(int Idioma) { int 처리값;',
          '처리값=InterpretadorComandos.예제폴더("/example"); if(처리값<0)return 처리값;']
    grupo_manifesto={}
    LEIAME=guest_bytes(원본자료/'README.md')
    if len(LEIAME)>16384: raise ValueError('example README exceeds native VFS limit')
    instrução_SEQUÊNCIA.append('처리값=InterpretadorComandos.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%LEIAME.hex())
    grupo_manifesto['/example/README.md']={'bytes':len(LEIAME),'sha256':hashlib.sha256(LEIAME).hexdigest()}
    instrução_SEQUÊNCIA.append('if(Idioma==0){처리값=InterpretadorComandos.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for caminho in [원본자료/'python/Português.py'] + sorted((raiz_caminho/'PYTHON_ponte/biblioteca').glob('*.py')):
        Conteúdo_VALOR=guest_bytes(caminho);meta='/lib/'+caminho.name
        if len(Conteúdo_VALOR)>16384: raise ValueError('Python library exceeds native VFS limit: '+meta)
        instrução_SEQUÊNCIA.append('처리값=InterpretadorComandos.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(meta,ensure_ascii=True),Conteúdo_VALOR.hex()))
        grupo_manifesto[meta]={'bytes':len(Conteúdo_VALOR),'sha256':hashlib.sha256(Conteúdo_VALOR).hexdigest()}
    instrução_SEQUÊNCIA.append('}')
    for PROC_ÍNDICE,Idioma in enumerate(('java','c','python')):
        lista_de_arquivos=[(dados_cargo.name,dados_cargo) for dados_cargo in sorted((원본자료/Idioma).iterdir()) if dados_cargo.is_file()]
        if Idioma=='java':lista_de_arquivos += [(dados_cargo.stem+'.class',aula_caminho/(dados_cargo.stem+'.class')) for dados_cargo in 자바실행]
        instrução_SEQUÊNCIA += ['if(Idioma==%d){'%PROC_ÍNDICE,'처리값=InterpretadorComandos.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Idioma]
        for Nome,caminho in lista_de_arquivos:
            Conteúdo_VALOR=guest_bytes(caminho);meta='/example/'+Idioma+'/'+Nome
            if len(Conteúdo_VALOR)>16384 or len(meta.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+meta)
            instrução_SEQUÊNCIA.append('처리값=InterpretadorComandos.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(meta,ensure_ascii=True),Conteúdo_VALOR.hex()))
            grupo_manifesto[meta]={'bytes':len(Conteúdo_VALOR),'sha256':hashlib.sha256(Conteúdo_VALOR).hexdigest()}
        instrução_SEQUÊNCIA += ['return 0;}']
    instrução_SEQUÊNCIA += ['return -22;}}']
    (raiz_caminho/'build/예제꾸러미.java').write_text('\n'.join(instrução_SEQUÊNCIA)+'\n')
    (RC_dados/'manifest.json').write_text(json.dumps(grupo_manifesto,ensure_ascii=False,indent=2)+'\n')
