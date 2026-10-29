"""Native JVM용 English class/JAR와 EL0에 넣을 read 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def createJavaLibrary(rootPath, executeCommand):
    (rootPath / 'build/user').mkdir(parents=True, exist_ok=True)
    output = rootPath / 'build/java-library'
    classPath = output / 'classes'
    classPath.mkdir(parents=True, exist_ok=True)
    sources = sorted((rootPath / 'NativeJava').rglob('*.java'))
    executeCommand(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', classPath] + sources)
    entriesList = []
    for originalAddress in sources:
        relativePath = originalAddress.relative_to(rootPath / 'NativeJava').with_suffix('.class')
        payloadData = (classPath / relativePath).read_bytes()
        name = str(relativePath).replace('/', '.')
        if len(payloadData) > 16384 or len(name.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + name)
        entriesList.append((relativePath, name, payloadData))
    headerValue = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *name; const unsigned char *data; unsigned size; } JavaClassResource;']
    for ordinalIndex, (_, name, payloadData) in enumerate(entriesList):
        headerValue.append('static const unsigned char javaClassData_%d[] = {%s};' % (ordinalIndex, ','.join(str(secondValue) for secondValue in payloadData)))
    headerValue.append('static const JavaClassResource javaClassList[] = {')
    for ordinalIndex, (_, name, payloadData) in enumerate(entriesList):
        headerValue.append('{%s, javaClassData_%d, %d},' % (json.dumps(name, ensure_ascii=False), ordinalIndex, len(payloadData)))
    headerValue.append('};')
    (rootPath / 'build/user/java-resources.h').write_text('\n'.join(headerValue) + '\n', encoding='utf-8')
    distributionPath = rootPath / 'dist'; distributionPath.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(distributionPath / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as javaBundle:
        for relativePath, _, payloadData in entriesList:
            systemInformation = zipfile.ZipInfo(str(relativePath), date_time=(1980, 1, 1, 0, 0, 0)); systemInformation.compress_type = zipfile.ZIP_DEFLATED
            javaBundle.writestr(systemInformation, payloadData)
    with zipfile.ZipFile(str(distributionPath / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for originalAddress in sources:
            systemInformation = zipfile.ZipInfo(str(originalAddress.relative_to(rootPath / 'NativeJava')), date_time=(1980, 1, 1, 0, 0, 0)); systemInformation.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(systemInformation, originalAddress.read_bytes())
