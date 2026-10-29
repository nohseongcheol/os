#!/usr/bin/env python3
"""Publish the measured country coverage without treating generation as testing."""
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/native'
configs=[json.loads(path.read_text()) for path in sorted((ROOT/'country').glob('*/native.json'))]
verification=json.loads((OUT/'verification.json').read_text())
assert verification['passed'],'Finish source verification before publishing results'
languages={config['language'] for config in configs}
pending=sum(bool(config['naming']['untranslated_identifiers']) for config in configs)
help_count=sum(config['help_sentence_translated'] for config in configs)
bridge_count=sum(bool(item.get('input_bridge',{}).get('passed')) for item in verification['source_compilation'])
lines=['# 자체 커널 국가별 현황','',
       '국가별 대표 언어는 golang/worldos 선택표와 같다. 소수 언어·공동 공용어 전체를 수록한 목록은 아니다.',
       '이름 수는 적용한 대응표 항목 수이며 완역률이 아니다. 한국어판은 원문이므로 치환 수가 0이다.',
       '미번역 열은 원문에서 남은 한국어 식별자의 종류 수다. 현지어 검토와 역사적 어원 검토는 모두 별도 과제다.',
       '입력 안내가 `기호`인 판은 `F9 / Shift+Space: [EN] ↔ [언어명]`으로 표시하며 문장 번역은 미완료다.',
       '입력·UTF-8 보존과 복잡한 문자 조판은 구분한다. 인도계 문자 결합과 완전한 양방향 배치는 미완료다.','',
       '| 국가 폴더 | 대표 언어 | 소스 폴더 | 이름 수 | 미번역 | 입력 | help 안내 |',
       '|---|---|---|---:|---:|---|---|']
for config in configs:
    code=config['country'];naming=config['naming']
    lines.append('| [{}](../country/{}/NATIVE.md) | {} ({}) | `{}` | {} | [{}](../country/{}/native-pending.tsv) | {} | {} |'.format(
        code,code,config['native_name'],config['language'],config['source'],naming['mapped_identifiers'],naming['untranslated_identifiers'],code,config['input']['kind'],'문장' if config['help_sentence_translated'] else '기호'))
(ROOT/'native/국가별현황.md').write_text('\n'.join(lines)+'\n')

runtime=[]
by_code={config['country']:config for config in configs}
for path in sorted((OUT/'verification').glob('*/report.json')):
    report=json.loads(path.read_text())
    if path.parent.name not in by_code:continue
    config=by_code[report['country']];source=ROOT/'country'/config['country']/config['source'];native=source/config['native']
    digest=hashlib.sha256()
    for name in sorted(config['owned_files']):digest.update(name.encode());digest.update((source/name).read_bytes())
    report['current_source_built']=digest.hexdigest()==(native/'build/worldos-source.sha256').read_text().strip()
    report['current_kernel_tested']=hashlib.sha256((native/'build/kernel8.img').read_bytes()).hexdigest()==report['kernel_sha256']
    assert report['passed'],path
    runtime.append(report)
system=[]
for path in sorted((OUT/'system').glob('*/report.json')):
    report=json.loads(path.read_text());config=by_code[report['country']]
    source=ROOT/'country'/config['country']/config['source'];native=source/config['native']
    digest=hashlib.sha256()
    for name in sorted(config['owned_files']):digest.update(name.encode());digest.update((source/name).read_bytes())
    report['current_source_built']=digest.hexdigest()==(native/'build/worldos-source.sha256').read_text().strip()
    report['current_kernel_tested']=hashlib.sha256((native/'build/kernel8.img').read_bytes()).hexdigest()==report['kernel_sha256']
    assert report['passed'] and report['current_source_built'] and report['current_kernel_tested'],path
    system.append(report)
command_pending={config['country']:config['commands']['pending'] for config in configs if config['commands']['pending']}
relocation=json.loads((OUT/'relocation/JPN.json').read_text())
relocated_run=json.loads((OUT/'verification/JPN-relocated/report.json').read_text())
assert relocation['passed'] and relocated_run['passed'] and relocation['kernel_sha256']==relocated_run['kernel_sha256']
summary={'countries':len(configs),'languages':len(languages),'source_verification':verification['passed'],
         'input_bridges_verified':bridge_count,
         'files_verified':verification['files_verified'],'runtime':runtime,'relocation':relocation,
         'relocated_runtime':relocated_run,'countries_with_untranslated_identifiers':pending,
         'system_commands_runtime':system,'countries_with_pending_command_names':command_pending,
         'localized_help_sentences':help_count,'symbolic_help':len(configs)-help_count,
         'input_kinds':dict(Counter(config['input']['kind'] for config in configs)),
         'all_identifiers_translated':False,'historical_etymology_review_complete':False,
         'complex_script_shaping_complete':False,'physical_pi_tested':False}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
lines=['# 자체 ARM64 Java 커널 국가판 검증','',
       '{}개 국가·지역 폴더, {}개 대표 언어. 자체 jkoros 커널로 빌드하며 기존 Linux 판은 별도다.'.format(len(configs),len(languages)),
       '생성된 폴더 수, 호스트 소스 컴파일, 실제 부팅 시험은 서로 다른 범위다.','',
       '## 네트워크·체계 명령 검증','',
       '공통 명령은 249개 판에 포함한다. 현지어 별칭 미번역 항목이 남은 판: {}개. 각 판의 native-commands.json에 항목을 명시한다.'.format(len(command_pending)),
       '아래 시험은 현재 소스·커널 해시를 확인한다. IP 변경·ICMP 성공/실패·변경 주소의 FTP·ps/free/df/top·현지어 명령·Tab·게스트 poweroff를 실제 QEMU에서 실행했다.',
       '', '| 판 | 현재 커널의 체계 명령 시험 |', '|---|---|',
       *['| {} | [통과](../build/native/system/{}/report.json) |'.format(report['country'],report['country']) for report in system],
       '', '[명령 사용법·기능 범위](네트워크와체계명령.md). 실물 Pi 4 종료·네트워크 장치는 미검증이다.','',
       '| 검사 | 결과와 범위 |','|---|---|',
       '| 파일 독립성 | {}개 파일 해시, 외부 묶음 해시, 판 내부 경로·예제 링크 검사 통과 |'.format(verification['files_verified']),
       '| 언어별 소스 | {}개 대표 언어의 Java 라이브러리·예제·커널·사용자 코드 호스트 컴파일, C 예제 문법 검사 통과 |'.format(len(languages)),
       '| 게스트 파일 제한 | UTF-8 경로 63바이트, 파일 16 KiB 범위 확인 |',
       '| 글꼴 | help·입력 표본·예제 이름·관리 명령 별칭/설명의 글리프 누락 없음. 전체 문자 조판 시험은 아님 |',
       '| 입력 | {}개 언어의 F9 반복 입력, Shift+Space, 표본 입력, 유니코드 직접 입력 검사; 해당 자판의 AltGr·조합키·후보 전환 포함 |'.format(bridge_count),
       '| 경로 이동 | 이전 일본어 커널판에서 공백 경로 독립 빌드·QEMU/VNC 실행 통과. 이번 관리 명령 변경의 새 경로 재시험은 아님 |',
       '| SD 이미지 | 이전 KOR 이미지 생성 성공. 새 명령 포함 이미지는 make image로 재생성. 실물 Raspberry Pi 4 미시험 |','',
       '## 실제 QEMU/VNC 검증','',
       '아래 저장된 실행 보고서는 현지 자판 전환, vi UTF-8 편집·저장, 현지 이름의 Java 원문 게스트 컴파일·실행, C 게스트 컴파일·실행, Python 실행, Java GUI 단추 콜백을 확인했다. 현재 커널 열이 이전이면 새 커널 전체 GUI 재검증 결과로 세지 않는다.',
       '게스트 `javac` 시험은 출력 예제이며 전체 Java 문법·JDK 호환성 시험이 아니다. GUI 예제는 호스트에서 사전 컴파일한 클래스를 실행했다.','',
       '| 판 | 부팅·입력·컴파일·GUI | Java·C·Python 파일 I/O | TCP/UDP·FTP JAR | 화면 | 현재 커널 |','|---|---|---|---|---|---|']
for report in runtime:
    code=report['country'];base='../build/native/verification/'+code
    lines.append('| {} | [통과]({}/report.json) | {} | {} | [vi]({}/vi-source.png), [GUI]({}/window-example.png) | {} |'.format(
        code,base,'통과' if report.get('java_c_python_file_io') else '이 시험에서 별도 확인하지 않음',
        '통과' if report.get('ftp_localized_jar_upload_execute') else '이 시험에서 확인하지 않음',base,base,'일치' if report['current_source_built'] and report['current_kernel_tested'] else '이전 커널'))
lines+=['','TCP는 Java 예제, UDP는 Java·C·Python 예제를 호스트 되돌림 서버와 연결해 실제 수신 자료를 확인했다.',
        'FTP는 현지어 이름의 JAR을 올리고 다시 내려받아 바이트를 비교한 뒤 `java -jar`와 `./이름.jar` 양쪽 실행을 확인했다.',
        '이번 일본어 GUI 네트워크 회귀 시험은 다른 커널 빌드·시험을 함께 돌리던 중 700 ms 제한의 Java 예제에서 한 차례 시간초과가 있었다. 다른 시험 VM을 종료한 재시험에서는 Java/C/Python 통신과 FTP가 통과했다. 시간초과의 단일 원인은 확정하지 않았다.',
        '다른 경로의 [일본어판 실행 보고서](../build/native/verification/JPN-relocated/report.json)에서도 파일 I/O를 확인했다.','',
        '## 남은 범위','',
        '- {}개 판에 미번역 내부 식별자가 있다. 일부 언어는 대응표가 없어 원문 이름을 유지한다. 예제의 설명문·GUI 문구에도 원문이 남아 있다.'.format(pending),
        '- help 입력 문장 번역은 {}개 판에 적용했고, {}개 판은 키와 언어명을 기호로 안내한다.'.format(help_count,len(configs)-help_count),
        '- 자연스러운 용례와 언어별 역사적 어원 검토는 완료하지 않았다. 기능 중심 명명안을 검증된 전통 용어로 주장하지 않는다.',
        '- 아랍어의 연결형·양방향 배치, 인도계 문자의 복잡한 결합 조판은 미완료다. 화면에는 글리프가 나오지만 올바른 문장 조판을 보장하지 않는다.',
        '- 일본어 입력은 가나까지이며 한자 사전 변환은 없다. 중국어는 한 음절 후보를 공백으로 고르는 방식이다.',
        '- 게스트 Java 식별자는 생성된 Unicode 9.0 분류표의 BMP 범위를 지원하며 보충 평면 식별자는 미지원이다. 문자열의 이모지 입력·표시는 별도다.',
        '- 현재 JVM·MicroPython·TinyCC와 네트워크·GUI 부분집합을 계승했다. 전체 OpenJDK, 영구 SD 파일체계, 실물 USB/GENET 드라이버는 추가하지 않았다.','',
        '## 재검증','', '```sh','make native-verify','make native-test COUNTRY=KOR ARGS=--network','make native-relocate COUNTRY=JPN','make native-report','```','',
        '[국가별 이름·입력 현황](국가별현황.md), [기계 판독 요약](../build/native/summary.json), [전체 소스 검사](../build/native/verification.json)에서 세부 범위를 확인한다.']
(ROOT/'native/검증결과.md').write_text('\n'.join(lines)+'\n')
print('Published country coverage and verification results')
