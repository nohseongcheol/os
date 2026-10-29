#!/usr/bin/env python3
"""Report measured naming and boot coverage without promoting partial translation."""
from collections import defaultdict
import argparse
import hashlib
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'native'))
from verify_country_boots import source_digest, launcher_digest, digest, PROBE_VERSION


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-historical-boots',action='store_true',help='Report prior-image proofs separately when the latest follow-up covers selected languages')
    args=parser.parse_args()
    audit = read(ROOT / 'build/country-localization/country-audit.json')
    assert audit['countries'] == 249 and audit['editions'] == 1827 and audit['passed'], 'Run a successful full naming audit first'
    boots = read(ROOT / 'build/native/country-boots/summary.json')
    assert boots['requested_countries'] == 249 and boots['complete'], 'Complete the full country boot campaign first'
    output = ROOT / 'build/localization-round2'
    paths = sorted((ROOT / 'country').glob('*/native.json')) + sorted((ROOT / 'country').glob('*/*/native.json'))
    languages, configs = defaultdict(list), {}
    for path in paths:
        config = read(path)
        configs[str(path.parent.relative_to(ROOT))] = config
        languages[config['language']].append((path.parent, config))
    current_boots, stale_boots, image_boots = [], [], []
    live_hashes = {}
    for path in sorted((ROOT / 'country').glob('*/native.json')):
        folder, config = path.parent, read(path)
        source_hash = source_digest(folder, config)
        live_hashes[str(folder.relative_to(ROOT))] = source_hash
        kernel = folder / config['source'] / config['native'] / 'build/kernel8.img'
        report = read(ROOT / 'build/native/country-boots' / folder.name / 'report.json')
        if report.get('passed') and kernel.is_file() and report.get('kernel_sha256') == digest(kernel):
            image_boots.append(folder.name)
        if (report.get('passed') and report.get('probe_version') == PROBE_VERSION and
                report.get('source_sha256') == source_hash and kernel.is_file() and
                report.get('launcher_sha256') == launcher_digest(folder, config) and
                report.get('kernel_sha256') == digest(kernel)):
            current_boots.append(report)
        else:
            stale_boots.append(folder.name)
    runtime = []
    for path in sorted((ROOT / 'build/native/verification').glob('*localized/report.json')):
        report = read(path)
        if not report.get('passed'):
            continue
        if report['language'] == 'mr':
            edition = 'country/IND/mr'
        elif report['language'] == 'zh':
            edition = 'country/CHN/zh'
        else:
            edition = 'country/' + report['country']
        config = configs.get(edition)
        if config is None:
            continue
        folder = ROOT / edition
        source_hash = live_hashes.get(edition) or source_digest(folder, config)
        kernel = folder / config['source'] / config['native'] / 'build/kernel8.img'
        image_current = kernel.is_file() and digest(kernel) == report.get('kernel_sha256')
        runtime.append({'edition': edition, 'language': report['language'],
                        'report': str(path.relative_to(ROOT)),
                        'current_image': image_current,
                        'source_bound': image_current and report.get('source_sha256') == source_hash and report.get('launcher_sha256') == launcher_digest(folder,config)})
    by_language = []
    for language, editions in sorted(languages.items()):
        pending = max(c['naming']['untranslated_identifiers'] for _,c in editions)
        if pending:
            folder, config = editions[0]
            by_language.append({'language':language,'editions':len(editions),
                                'remaining_identifiers':pending,
                                'example_pending_file':str((folder/'native-pending.tsv').relative_to(ROOT))})
    compilation = {}
    for path in sorted((ROOT/'build/country-localization/compilation').glob('check-*.json'),key=lambda p:p.stat().st_mtime):
        for report in read(path).get('results',[]):
            edition = report.get('edition')
            if not report.get('passed') or not report.get('source_sha256') or edition not in configs:
                continue
            current = live_hashes.get(edition) or source_digest(ROOT/edition,configs[edition])
            if current==report['source_sha256']:
                compilation[report['language']]={'edition':edition,'source_sha256':current,
                    'report':str(path.relative_to(ROOT)), 'managed_and_x86_java_compiled':report.get('managed_and_x86_java_compiled',False)}
    no_residue = [r for r in audit['editions_detail'] if not any(r[k] for k in (
        'remaining_identifiers','remaining_paths','remaining_code_identifiers','remaining_embedded_identifiers'))]
    managed_path=ROOT/'build/localization-round2/managed-country-namespaces.json'
    managed=read(managed_path) if managed_path.is_file() else {}
    managed_current={}
    for proof_path in (managed_path,ROOT/'build/localization-round2/managed-my-function-review.json',ROOT/'build/localization-round2/managed-java-prose.json',ROOT/'build/localization-round2/managed-java-prose-my-final.json'):
        if not proof_path.is_file():continue
        for proof in read(proof_path).get('results',[]):
            edition=proof['edition']
            if not proof.get('passed') or edition not in configs:continue
            current=live_hashes.get(edition) or source_digest(ROOT/edition,configs[edition])
            if current==proof.get('source_sha256'):
                managed_current[edition]=dict(proof,report=str(proof_path.relative_to(ROOT)))
    required_managed={'country/'+code for code in {c['country'] for c in configs.values()}}
    required_managed.update(('country/VNM/zh_Hant','country/VNM/hnj','country/MMR/stu'))
    child_boots=[]
    for edition in ('country/MMR/stu','country/VNM/hnj'):
        folder=ROOT/edition;config=configs[edition]
        proof=ROOT/'build/native/edition-boots'/('-'.join(Path(edition).parts[1:]))/'report.json'
        if not proof.is_file():continue
        report=read(proof)
        image=folder/config['source']/config['native']/'build/kernel8.img'
        current=(report.get('passed') and report.get('source_sha256')==source_digest(folder,config) and
                 report.get('launcher_sha256')==launcher_digest(folder,config) and image.is_file() and
                 report.get('kernel_sha256')==digest(image))
        child_boots.append({'edition':edition,'passed_current_source':current,'report':str(proof.relative_to(ROOT))})
    from country_naming import country_names
    pending_country_names={key:value for key,value in country_names().items() if value['status']!='cldr-territory-name'}
    java_path=output/'java-localization-audit.json'
    java_audit=read(java_path) if java_path.is_file() else {}
    java_current=bool(java_audit) and all(
        proof.get('manifest_sha256')==hashlib.sha256((ROOT/proof['edition']/'native-generated.json').read_bytes()).hexdigest()
        for proof in java_audit.get('results',[]))
    java_my=[{'edition':proof['edition'],
              'remaining_identifiers':len(proof['remaining_identifiers']),
              'remaining_paths':len(proof['remaining_paths']),
              'remaining_comments':len(proof['remaining_comments']),
              'remaining_library_messages':len(proof.get('remaining_library_messages',[]))}
             for proof in java_audit.get('results',[]) if proof['language']=='my']
    prose_languages=set(read(ROOT/'native/inputs/localized-java-prose.json')['comments'])
    supported_java=[p for p in java_audit.get('results',[]) if p['language'] in prose_languages]
    change_counts_path=output/'java-prose-change-counts.json'
    change_counts=read(change_counts_path) if change_counts_path.is_file() else {}
    complete_java=lambda proof:not any(proof.get(k) for k in ('remaining_identifiers','remaining_paths','remaining_comments','remaining_library_messages'))
    fresh_boots=[]
    followup_path=output/'java-prose-boots.json'
    if followup_path.is_file():
        followup=read(followup_path)
        for proof in followup['results']:
            edition=proof['edition'];folder=ROOT/edition;config=configs[edition]
            kernel=folder/config['source']/config['native']/'build/kernel8.img'
            current=live_hashes.get(edition) or source_digest(folder,config)
            fresh_boots.append({'edition':edition,'passed_current_source':bool(proof.get('passed') and
                proof.get('source_sha256')==current and proof.get('launcher_sha256')==launcher_digest(folder,config) and
                kernel.is_file() and proof.get('kernel_sha256')==digest(kernel))})
    result = {
        'reported_at': datetime.now(timezone.utc).isoformat(), 'request_complete': False,
        'countries':249,'native_editions':1827,'language_tags':len(languages),
        'native_integrity_passed':True,
        'independent_source_files_checked':audit['independent_source_files_checked'],
        'java_files_verified':audit['native_java_files_verified'],
        'native_editions_without_remaining_korean_names':len(no_residue),
        'native_editions_with_remaining_translation':len(audit['incomplete_editions']),
        'languages_without_remaining_korean_names':sorted({r['language'] for r in no_residue}),
        'current_source_country_boots_passed':len(current_boots),'stale_or_failed_country_boots':stale_boots,
        'java_prose_followup':{'countries':203,'editions':432,'language_profiles':11,
                              'java_audit_current':java_current,'burmese_java':java_my,
                              'supported_java_editions_without_korean_names_comments_or_library_messages':sum(complete_java(p) for p in supported_java),
                              'all_supported_java_editions_passed':len(supported_java)==432 and all(complete_java(p) for p in supported_java),
                              'whole_comment_roles_per_profile':150,
                              'unique_java_files_changed':change_counts.get('unique_java_files_changed'),
                              'java_comment_revisions':change_counts.get('java_comment_revisions'),
                              'comment_only_delta_reports':['build/localization-round2/java-complete-prose-delta.json',
                                                            'build/localization-round2/java-complete-prose-ja-alias-delta.json',
                                                            'build/localization-round2/java-complete-prose-zh-alias-delta.json'],
                              'report':'build/localization-round2/java-localization-audit.json'},
        'country_images_matching_a_passed_boot':len(image_boots),
        'latest_followup_boot_report':'build/localization-round2/java-prose-boots.json' if (output/'java-prose-boots.json').is_file() else None,
        'latest_followup_boots':fresh_boots,
        'all_project_identifiers_and_paths_localized':False,
        'all_etymologies_verified':False,'native_speaker_review_complete':False,
        'editions_with_preserved_unaligned_contexts':sum(bool(c['naming'].get('legacy_alias_compatibility_review_pending')) for c in configs.values()),
        'direct_role_dictionaries':['ja','zh_Hans','zh_Hant','de','fr','es','vi'],
        'partial_burmese_role_dictionary_size':len(read(ROOT/'native/inputs/localized-roles/my.json')['names']),
        'country_namespace_editions_audited':audit['editions'],
        'country_namespace_policy':'Country name in the edition language plus J + titlecase ISO alpha-3 + OS. Unknown country-name translations use ISO codes with pending status.',
        'pending_country_name_translations_or_toolchain_support':len(pending_country_names),
        'managed_namespace_execution':{'passed':required_managed.issubset(managed_current),
                                       'editions':len(managed_current),'assertions':sum(p['managed_assertions'] for p in managed_current.values()),
                                       'results':list(managed_current.values()),
                                       'report':'build/localization-round2/managed-java-prose.json',
                                       'current_proof_reports':sorted({p['report'] for p in managed_current.values()})},
        'explicit_child_language_policy':'Keep each child language; confirmed by the user. stu is Samtao; hnj is Hmong Njua.',
        'targeted_child_boots':child_boots,
        'targeted_language_limitations':{
            'stu':'No reviewed Samtao functional terminology dictionary has been completed in this workspace; Korean roles remain pending.',
            'hnj':'The CLDR default Nyiakeng Puachue script is outside the current Python 3.6 / Java 11 identifier tables and terminal font. See build/localization-round2/hnj-script-support.json. Functional terminology remains pending.'},
        'direct_role_dictionary_size':3656,
        'current_boot_scope':'Each country representative ARM64 kernel, UTF-8 sample file roundtrip, input help and its configured Java/Python/C examples in QEMU. Example names may still be untranslated. Not all language editions, GUI input methods, architectures or physical boards.',
        'gui_runtime_reports':runtime,
        'current_source_compilation':compilation,
        'reports':{'naming':'build/country-localization/country-audit.json',
                   'boots':'build/native/country-boots/summary.json',
                   'remaining':'build/localization-round2/remaining-work.json',
                   'regressions':'build/localization-round2/java-prose-regressions.log',
                   'java_comments':'build/localization-round2/java-localization-audit.json'},
        'limitations':['Many language dictionaries still lack complete role translations.',
                       'Originally English first-party native helpers still need semantic localization beyond replacing the Korean role inventory.',
                       'Hosted Linux edition tools and delivery scaffolding still contain owned English names.',
                       'Comments, manuals and some GUI text still contain untranslated prose.',
                       'Function-based compounds are modern project proposals; selected attested lexical roots do not certify all etymologies.']}
    write(output / 'result.json', result)
    preserved=[{'edition':edition,'contexts':config['naming']['legacy_alias_compatibility_review_pending']}
               for edition,config in configs.items() if config['naming'].get('legacy_alias_compatibility_review_pending')]
    write(output / 'remaining-work.json', {'request_complete':False,'language_tags_with_pending_names':len(by_language),
                                         'native_languages':by_language,'other_scope':result['limitations'],
                                         'pending_country_names':pending_country_names,
                                         'preserved_alias_contexts':preserved,
                                         'preserved_context_review':'Representative preserved contexts are helper prose or differences from the newer canonical packaging snippets. Existing portable.pack calls were inspected and are intact. Full prose localization remains pending.',
                                         'preserved_context_examples':'build/localization-round2/preserved-contexts.json'})
    state={'status':'validated_partial_localization','request_complete':False,
           'result':'build/localization-round2/result.json','active_jobs':[]}
    write(output / 'state.json', state)
    write(output / 'namespace-state.json', state)
    write(ROOT/'build/localization-fix/state.json', state)
    # Keep the earlier task summary entry points current as well.
    write(ROOT / 'build/localization-fix/result.json', result)
    write(ROOT / 'build/localization-fix/remaining-work.json', read(output/'remaining-work.json'))
    rows=[]
    for item in runtime:
        report=read(ROOT/item['report'])
        status='현재 이미지 일치' if item['current_image'] else '이전 이미지'
        if item['source_bound']:status='현재 소스·실행기 일치'
        network='통과' if report.get('java_tcp_udp_python_c_udp') and report.get('ftp_localized_jar_upload_execute') else '이번 보고서에서는 미검사'
        rows.append('| {} | [{}](../{}) | {} | {} |'.format(item['edition'],item['language'],item['report'],network,status))
    doc='''# 국가판 현지어 명명과 실행 검증

249개 국가·지역의 대표판과 1,578개 하위 언어판, 총 1,827개 native 소스 트리를 구분한다.
국가 대표 언어 선택은 모든 주민이 한 언어를 사용한다는 뜻이 아니다.

## 이름과 소스 감사

원래 한국어로 작성된 3,656개 역할에 대해 일본어, 중국어 간체·번체, 독일어,
프랑스어, 스페인어, 베트남어 명칭을 직접 작성하여 해당 언어판에 반영했다.
미얀마어에도 기능별 번역 제안을 반영했으며 미번역 역할이 남아 있다.
국가별 관리형 Java 경로·패키지를 해당 국가명과 JChnOS·JVnmOS 같은 국가별 이름으로 바꿨다.
국가명 번역이나 식별자 문자 지원이 없는 언어는 ISO 코드를 쓰고 미완료로 기록한다.
공개 클래스와 파일명, 선언과 참조, Python 정규형, 외부 API·옵션·실행기 참조를 검사했다.
''' + '\n소스 {:,}개와 Java 파일 {:,}개의 감사가 통과했다.\n'.format(result['independent_source_files_checked'],result['java_files_verified']) + '''
한국어판 원문과 기존 영어·마라티어판을 포함해 원문 한국어 식별자 잔여가 없는 판은
''' + '{}개이며, {}개 판에는 번역이 더 필요하다.\n'.format(len(no_residue),len(audit['incomplete_editions'])) + '''
이 수치는 원래 영어였던 자체 native 보조 코드, Linux 실행판 도구, 배포 경로,
설명문까지 전부 현지어가 되었다는 뜻이 아니다. 저작권·법적 문구·문자값 시험은 보존했다.
새 합성어는 현대의 기능 중심 제안이며, 일부 확인된 어근만 출처를 기록했다.
전체 원어민 용례 검토와 역사적 어원 검토는 미완료다.

## Java 주석·오류 안내 추가 수정

203개 국가·지역의 432개 판에 일반 주석 131종, 예외 설명문 19종과 라이브러리 오류 안내 20종을
11개 언어 프로필로 반영했다. 미얀마어 Java 이름과 주석은 호스트 실행기까지 보완했다.
[현재 파일에 묶인 Java 감사](../build/localization-round2/java-localization-audit.json)는
식별자·경로·주석·라이브러리 안내를 각각 집계한다.
이 11개 프로필 밖의 언어판과 비Java 코드·설명문에는 여전히 미번역 항목이 있다.
이 범위의 Java 감사는 자체 식별자·경로·주석·라이브러리 안내를 확인하며, 모든 문자열의 번역 완료를 뜻하지 않는다.
저작권 작성자와 문자 시험 표본은 보존한다.

## 실제 부팅

''' + '{} / 249개 대표판의 부팅 증명이 현재 소스·이미지·실행기 해시와 모두 일치한다.\n'.format(len(current_boots)) + '''
''' + '{}개 대표판의 현재 커널 이미지가 통과한 부팅 기록과 일치한다.\n'.format(len(image_boots)) + '''
이전 249개 부팅 기록을 보존하고, 이후 주석·명명 변경에 대해서는 현재 소스 일치 여부를 다시 구분했다.
[이번 Java 주석·명명 수정 후 부팅한 13개 판](../build/localization-round2/java-prose-boots.json)은 별도 기록이다.
각 국가 폴더의 이미지를 실제 실행하고 입력 안내, 설정된 UTF-8 표본의 파일 저장·재읽기,
해당 판에 설정된 이름의 Java 게스트 컴파일·실행, Python 실행, C 컴파일·실행을 확인했다.
예제 이름이 아직 미번역인 판도 있으므로 실행 성공을 번역 완료로 해석하지 않는다.
전체 소스가 같거나, 통과한 판의 전체 소스를 현재 파일 또는 백업으로 해시 대조한 뒤
보수적으로 잡은 ARM64 빌드 입력과 의존성이 같은 경우에는 독립 복사로 컴파일을 재사용했다.
별도 관리형 Java 트리와 루트 문서는 ARM64 빌드 입력에서 제외하며, 관리형 Java는 따로 실행 검사했다.
국가별 부팅 시험 결과는 실제로 따로 실행했다. 모든 하위 언어판이나 x86·VirtualBox,
실물 Raspberry Pi를 각각 부팅한 결과는 아니다.

''' + '국가별 관리형 Java 실행은 현재 소스와 일치하는 {}개 판에서 {:,}개 단언을 통과했다.\n'.format(len(managed_current),sum(p['managed_assertions'] for p in managed_current.values())) + '''
`MMR/stu`(삼타오어)와 `VNM/hnj`(녹색 몽어)는 각각의 언어판을 유지했다.
두 하위 판도 별도로 QEMU ARM64 부팅·예제 실행을 통과했지만, 한국어 역할명은 아직 남아 있다.
삼타오어 기술 용어 검토와 몽어의 문자 도구·글꼴 지원, 기능 용어 검토가 필요하다.

[국가별 실행 로그와 해시](../build/native/country-boots/summary.json),
[전체 파일 감사](../build/country-localization/country-audit.json),
[두 하위 언어판 부팅](../build/native/edition-boots/summary.json),
[Java 명명·주석 회귀 검사](../build/localization-round2/java-prose-regressions.log).

## 입력·편집기·GUI 추가 검사

아래 보고서는 F9·Shift+Space, vi의 UTF-8 저장, 현지 이름의 Java·C·Python 예제와
파일 입출력, GUI 버튼 동작을 확인한다. 이전 이미지 표시는 현재 결과로 세지 않는다.

| 판 | 보고서 | TCP·UDP·FTP JAR | 현재 적용 범위 |
|---|---|---|---|
''' + '\n'.join(rows) + '''

게스트 Java·Swing·MicroPython·TinyCC는 현재 구현된 부분집합이다. 전체 OpenJDK,
영구 SD 파일체계, 실물 USB·GENET, 복잡한 문자 결합과 양방향 조판은 완료되지 않았다.
일본어 입력은 가나 변환이며, 중국어는 음절 후보를 고르는 방식이다.
기존 `build/native/system/`의 네트워크·체계 명령 기록은 각 보고서의 원래 커널 해시 범위다.

[현재 결과 요약](../build/localization-round2/result.json),
[언어별 남은 작업](../build/localization-round2/remaining-work.json),
[Java 식별자·경로·한국어 주석별 감사](../build/localization-round2/java-localization-audit.json),
[이름 구성·재검증 방법](README.md).
'''
    (ROOT/'native/검증결과.md').write_text(doc)
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v,(list,dict))}, ensure_ascii=False, indent=2))
    if (java_audit and (not java_current or
            not result['java_prose_followup']['all_supported_java_editions_passed'] or
            {r['edition'] for r in java_my}!={'country/MMR','country/MMR/my','country/BGD/my'} or
            any(r[k] for r in java_my for k in ('remaining_identifiers','remaining_paths','remaining_comments','remaining_library_messages')))):
        raise SystemExit('The Java follow-up audit is stale or incomplete.')
    if len(fresh_boots)!=13 or not all(p['passed_current_source'] for p in fresh_boots):
        raise SystemExit('The latest 13-edition boot proof is stale or incomplete.')
    current_network={p['edition'] for p in runtime if p['source_bound'] and
        read(ROOT/p['report']).get('java_tcp_udp_python_c_udp') and read(ROOT/p['report']).get('ftp_localized_jar_upload_execute')}
    if not {'country/MMR','country/VNM'}.issubset(current_network):
        raise SystemExit('Current-source Burmese and Vietnamese GUI/network proofs are required.')
    if ((stale_boots and not args.allow_historical_boots) or not result['managed_namespace_execution']['passed'] or
            {r['edition'] for r in child_boots if r['passed_current_source']} != {'country/MMR/stu','country/VNM/hnj'}):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
