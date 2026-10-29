"""nativo JVM용 Italiano class/JAR와 EL0에 넣을 Lettura 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(radice_percorso, Esegui_comando):
    (radice_percorso / 'build/user').mkdir(parents=True, exist_ok=True)
    output = radice_percorso / 'build/java-library'
    Corso_percorso = output / 'classes'
    Corso_percorso.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((radice_percorso / '한국어자바').rglob('*.java'))
    Esegui_comando(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Corso_percorso] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        percorso_relativo = 원본주소.relative_to(radice_percorso / '한국어자바').with_suffix('.class')
        payload_dati = (Corso_percorso / percorso_relativo).read_bytes()
        Nome = str(percorso_relativo).replace('/', '.')
        if len(payload_dati) > 16384 or len(Nome.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Nome)
        항목들.append((percorso_relativo, Nome, payload_dati))
    Intestazione_VALORE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Nome; const unsigned char *dati; unsigned Dimensione; } 자바자원;']
    for 순번, (_, Nome, payload_dati) in enumerate(항목들):
        Intestazione_VALORE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECONDO_VALORE) for SECONDO_VALORE in payload_dati)))
    Intestazione_VALORE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Nome, payload_dati) in enumerate(항목들):
        Intestazione_VALORE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Nome, ensure_ascii=False), 순번, len(payload_dati)))
    Intestazione_VALORE.append('};')
    (radice_percorso / 'build/user/java-resources.h').write_text('\n'.join(Intestazione_VALORE) + '\n', encoding='utf-8')
    distribuzione_percorso = radice_percorso / 'dist'; distribuzione_percorso.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(distribuzione_percorso / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for percorso_relativo, _, payload_dati in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(percorso_relativo), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, payload_dati)
    with zipfile.ZipFile(str(distribuzione_percorso / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Archivio:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(radice_percorso / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Archivio.writestr(msinfo32_exe, 원본주소.read_bytes())
