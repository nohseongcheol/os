"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from buildJavaLibrary import createJavaLibrary


def createExamples(rootPath, repositoryPath, executeCommand):
    originalData=repositoryPath/'example';resultData=rootPath/'build/examples';resultData.mkdir(parents=True,exist_ok=True)
    classPath=resultData/'classes';classPath.mkdir(exist_ok=True)
    createJavaLibrary(rootPath,executeCommand)
    ip_settings = read_config(rootPath)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = resultData/'java-source'; java_sources.mkdir(exist_ok=True)
    executeJava=[]
    for path in sorted((originalData/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); executeJava.append(target)
    executeCommand(['javac','--release','8','-encoding','UTF-8','-cp',rootPath/'build/java-library/classes','-d',classPath]+executeJava)
    instructionSequence=['public final class ExampleBundle { public static int installValue(int language) { int processedValue;',
          'processedValue=CommandInterpreter.exampleDirectory("/example"); if(processedValue<0)return processedValue;']
    bundleManifest={}
    readme=guest_bytes(originalData/'README.md')
    if len(readme)>16384: raise ValueError('example README exceeds native VFS limit')
    instructionSequence.append('processedValue=CommandInterpreter.exampleFile("/example/README.md","%s"); if(processedValue<0)return processedValue;'%readme.hex())
    bundleManifest['/example/README.md']={'bytes':len(readme),'sha256':hashlib.sha256(readme).hexdigest()}
    instructionSequence.append('if(language==0){processedValue=CommandInterpreter.exampleDirectory("/lib"); if(processedValue<0)return processedValue;')
    for path in [originalData/'python/English.py'] + sorted((rootPath/'pythonBridge/library').glob('*.py')):
        contentValue=guest_bytes(path);targetValue='/lib/'+path.name
        if len(contentValue)>16384 or len(targetValue.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+targetValue)
        instructionSequence.append('processedValue=CommandInterpreter.exampleFile(%s,"%s"); if(processedValue<0)return processedValue;'%(json.dumps(targetValue,ensure_ascii=True),contentValue.hex()))
        bundleManifest[targetValue]={'bytes':len(contentValue),'sha256':hashlib.sha256(contentValue).hexdigest()}
    instructionSequence.append('}')
    for lookupIndex,language in enumerate(('java','c','python')):
        fileList=[(dataPosition.name,dataPosition) for dataPosition in sorted((originalData/language).iterdir()) if dataPosition.is_file()]
        if language=='java':fileList += [(dataPosition.stem+'.class',classPath/(dataPosition.stem+'.class')) for dataPosition in executeJava]
        instructionSequence += ['if(language==%d){'%lookupIndex,'processedValue=CommandInterpreter.exampleDirectory("/example/%s"); if(processedValue<0)return processedValue;'%language]
        for name,path in fileList:
            contentValue=guest_bytes(path);targetValue='/example/'+language+'/'+name
            if len(contentValue)>16384 or len(targetValue.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+targetValue)
            instructionSequence.append('processedValue=CommandInterpreter.exampleFile(%s,"%s"); if(processedValue<0)return processedValue;'%(json.dumps(targetValue,ensure_ascii=True),contentValue.hex()))
            bundleManifest[targetValue]={'bytes':len(contentValue),'sha256':hashlib.sha256(contentValue).hexdigest()}
        instructionSequence += ['return 0;}']
    instructionSequence += ['return -22;}}']
    (rootPath/'build/ExampleBundle.java').write_text('\n'.join(instructionSequence)+'\n')
    (resultData/'manifest.json').write_text(json.dumps(bundleManifest,ensure_ascii=False,indent=2)+'\n')
