#!/usr/bin/env python3
"""명명 klip·özel_durum·경로를 검사한다. --시언어는 libclang bildirim 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

işlem_kök = Path(__file__).resolve().parents[1]
depo_kök = işlem_kök.parents[1]

def çalıştır():
    ayrıştırıcı_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ayrıştırıcı_48ee4b1b.add_argument('--C_Dil', action='store_true')
    bağımsız_değişkenler = ayrıştırıcı_48ee4b1b.parse_args()
    실패들 = []
    sözleşme_değeri = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Dosya_BAĞ_DEĞ_SAY = 0
    parametre_tablo = {}
    değişen_sayıda_bağımsız_değişken_içeren_işlev = set()
    나무들 = {}
    공용번역기들 = [depo_kök/'compiler/derleyici.py', depo_kök/'compiler/기계어미리번역.py']
    for yol in list((işlem_kök/'araçlar').glob('*.py')) + list((işlem_kök/'예제').rglob('*.py')) + 공용번역기들:
        if yol.name.endswith(('이름반영.py', '이름분석.py')): continue
        Dosya_BAĞ_DEĞ_SAY += 1
        나무 = ast.parse(yol.read_text()); 나무들[yol] = 나무
        for girdi_değer in ast.walk(나무):
            if isinstance(girdi_değer, ast.FunctionDef):
                parametre_tablo.setdefault(girdi_değer.name, set()).update(parametre_bağımsız_değişken.arg for parametre_bağımsız_değişken in girdi_değer.args.args + girdi_değer.args.kwonlyargs)
                if girdi_değer.args.kwarg: değişen_sayıda_bağımsız_değişken_içeren_işlev.add(girdi_değer.name)
            if isinstance(girdi_değer, ast.ClassDef):
                for işlev_değer in girdi_değer.body:
                    if isinstance(işlev_değer, ast.FunctionDef) and işlev_değer.name == '__init__':
                        parametre_tablo.setdefault(girdi_değer.name, set()).update(parametre_bağımsız_değişken.arg for parametre_bağımsız_değişken in işlev_değer.args.args + işlev_değer.args.kwonlyargs)
            İsim = ''
            if isinstance(girdi_değer, (ast.FunctionDef, ast.ClassDef)): İsim = girdi_değer.name
            elif isinstance(girdi_değer, ast.Name) and isinstance(girdi_değer.ctx, ast.Store): İsim = girdi_değer.id
            elif isinstance(girdi_değer, ast.arg): İsim = girdi_değer.arg
            if İsim and İsim not in sözleşme_değeri and all(ord(karakter_değer)<128 for karakter_değer in İsim):
                실패들.append('{}:{}: {}'.format(yol.relative_to(depo_kök), girdi_değer.lineno, İsim))
    for yol, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            İsim = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if İsim not in parametre_tablo or İsim in değişen_sayıda_bağımsız_değişken_içeren_işlev or not any(ord(karakter_değer)>127 for karakter_değer in İsim): continue
            for parametre_bağımsız_değişken in 호출.keywords:
                if parametre_bağımsız_değişken.arg and parametre_bağımsız_değişken.arg not in parametre_tablo[İsim]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(yol.relative_to(depo_kök), 호출.lineno, İsim, parametre_bağımsız_değişken.arg))
    for girdi_satırı in (işlem_kök/'명명/dosya_adı_eşleme.tsv').read_text().splitlines()[1:]:
        Önceki_öğe, geçerli_öğe, işlem_değer_girdi = girdi_satırı.split('\t')
        if not (işlem_kök/geçerli_öğe).is_file(): 실패들.append('taşımak_değer_83b651b8 dosya 없음: '+geçerli_öğe)
        if işlem_değer_girdi == '호환진입점유지' and not (işlem_kök/Önceki_öğe).is_file(): 실패들.append('호환 giriş_noktası 없음: '+Önceki_öğe)
    예제 = (işlem_kök.parents[1]/'example/java/AğÖrneği.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for yol in sorted((işlem_kök.parents[1]/'example/java').glob('*.java')):
        kaynakKod = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', yol.read_text())
        for İsim in re.findall(r'\b[^\W\d]\w*\b', kaynakKod, re.UNICODE):
            if İsim not in 예약어 and all(ord(karakter_değer)<128 for karakter_değer in İsim):
                실패들.append('{}: 예제의 영어 tanımlayıcı_değer {}'.format(yol.name, İsim))
    for İsim in ('Pencere', 'düğme', 'Etiket', 'metin_alanı', '화면구성요소', 'olay_sıra', 'arkaPlanGörevi', '실행할일', '동작받이', 'Eylem_uyarı', '작업'):
        kaynakKod = (işlem_kök/'한국어자바/Türkçe/Öz'/(İsim+'.java')).read_text()
        kaynakKod = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', kaynakKod)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', kaynakKod):
            실패들.append(İsim+': Türkçe 직접 구현에 표준 nesne_değer 래퍼가 남았습니다.')
    시언어예제 = (işlem_kök.parents[1]/'example/c/AğÖrneği.c').read_text()
    for İsim in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if İsim in 시언어예제: 실패들.append('C iletişim 예제에 남은 표준 İsim: '+İsim)
    파이썬예제 = (işlem_kök.parents[1]/'example/python/AğÖrneği.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python iletişim 예제에 남은 표준 özel_durum 직접 kullanmak_değer')
    머리 = (işlem_kök.parents[1]/'posix-kor/arm64-native/bildirimler/ağ_ABI.h').read_text()
    for İsim in ('bulut_Aile', 'veri_birimi_yuvası', 'veri_birimi_protokol', 'yuva_ADRES', 'bulut_yuva_ADRES', 'açmak_uç_nokta', 'göndermek_veri_birimi_veri'):
        if re.search(r'^#define\s+'+İsim+r'\b', 머리, re.M): 실패들.append('C 직접 gerçekleme 대신 makro_değer kullanmak_değer: '+İsim)
    자바파일수 = 0
    for kök_değer in ('kaynakKod', 'kullanıcı_alanı/자바', '한국어자바'):
        for yol in (işlem_kök/kök_değer).rglob('*.java'):
            자바파일수 += 1
            kaynakKod = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', yol.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', kaynakKod):
                실패들.append('{}: 한국어화되지 않은 bildirim {}'.format(yol.relative_to(işlem_kök), 맞음[1]))
            if kök_değer == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', kaynakKod):
                실패들.append('{}: 공개 özel_durum bildirim'.format(yol.relative_to(işlem_kök)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for yol in sorted((depo_kök/'os/kaynakKod').glob('*.java')):
        x86자바파일수 += 1
        kaynakKod = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', yol.read_text())
        for İsim in re.findall(r'\b[^\W\d]\w*\b', kaynakKod, re.UNICODE):
            if İsim not in 예약어 | 표준자바이름 and all(ord(karakter_değer)<128 for karakter_değer in İsim):
                실패들.append('{}: Öz 영어 tanımlayıcı_değer {}'.format(yol.relative_to(depo_kök), İsim))
    LOG_KAYIT = {'passed': False, 'python_files': Dosya_BAĞ_DEĞ_SAY, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if bağımsız_değişkenler.C_Dil:
        subprocess.check_call(['python3', str(işlem_kök/'araçlar/시언어이름분석.py')])
        Analiz_değer = json.loads((işlem_kök/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(hata) for hata in Analiz_değer['hata'])
        dışarı_aktarmak_ABI = set(json.loads((işlem_kök/'명명/규격이름.json').read_text()))
        for girdi_değer in Analiz_değer['bildirim'].values():
            İsim = girdi_değer['İsim']; yol = Path(girdi_değer['dosya'])
            kaynakKod = yol.read_bytes()
            # Türkçe 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if kaynakKod[girdi_değer['Ofset_değer']:girdi_değer['Ofset_değer']+len(İsim)] == İsim.encode() and İsim not in dışarı_aktarmak_ABI:
                실패들.append('{}:{}: {}'.format(yol.relative_to(işlem_kök), girdi_değer['girdi_satırı'], İsim))
        LOG_KAYIT['c_semantic_checked'] = True
        LOG_KAYIT['c_source_sha256'] = {str(Path(dosya).relative_to(işlem_kök)):özet_Dosya for dosya,özet_Dosya in Analiz_değer['원문해시'].items()}
    LOG_KAYIT['passed'] = not 실패들; LOG_KAYIT['failures'] = 실패들
    hedef_değer = işlem_kök/'build/verification/naming'; hedef_değer.mkdir(parents=True, exist_ok=True)
    (hedef_değer/'report.json').write_text(json.dumps(LOG_KAYIT, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Türkçe bildirim·dosya yol·호환 giriş_noktası·iletişim 예제')

if __name__ == '__main__': çalıştır()
