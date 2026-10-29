import hashlib
import sys
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from naming_review import COPYRIGHT,matches_owned,apply_terms,review
from apply_native_review import renamer,source_rename

class NamingReviewTests(unittest.TestCase):
    def test_exact_legacy_comment_variant_does_not_modify_literal_fixture(self):
        from java_prose import localize_java_comments
        from country_naming import names_for_country
        import json
        cases=[('JPN','ja','/** 入力値(入力値)과 ストリーム値: 순서대로 들어오는 바이트를 읽는 チャネル入口. */',
                '/** 順番に届くバイトを読み取る入力路。 */'),
               ('CHN','zh','/** 内置 커널의 Swing 窗口: 你好 输入值 → 按钮 → 指南 文本 刷新. */',
                '/** 独立内核上的 Swing 窗口：输入中文、点击按钮、更新提示标签。 */'),
               ('VNM','zh_Hant','/** 字元(文本), 編碼狀態值(符號): UTF-8 바이트와 UTF-16 문자열의 轉換值. 正規化值/組合 입력기는 별개다. */',
                '/** 在 UTF-8 位元組與 UTF-16 字串之間轉換；正規化與組合輸入另行處理。 */')]
        for country,language,alias,expected in cases:
            with self.subTest(language=language):
                fixture='String fixture = '+json.dumps(alias,ensure_ascii=False)+';'
                result=localize_java_comments('Input.java',alias+'\n'+fixture,language,names_for_country(country,language))
                self.assertTrue(result.startswith(expected))
                self.assertIn(fixture,result)

    def test_all_supported_java_prose_profiles_cover_generated_comments(self):
        import json
        import re
        from generate import sources, adapt, translate_source
        from country_naming import names_for_country
        from java_prose import document, TOKENS, localize_java_comments
        editions={'en':'GBR','ja':'JPN','vi':'VNM','de':'DEU','fr':'FRA','es':'ESP',
                  'mr':'IND/mr','my':'MMR','zh':'CHN/zh','zh_Hans':'CHN','zh_Hant':'TWN'}
        original=sources()
        for language,edition in editions.items():
            with self.subTest(language=language):
                folder=ROOT/'country'/edition
                config=json.loads((folder/'native.json').read_text())
                profile=json.loads((folder/config['source']/config['native']/'input.json').read_text())
                mapping=names_for_country(config['country'],language)
                adapted,unused=adapt(original,language,config['native_name'],profile)
                adapted['launcher.java']=(ROOT/'native/국가실행기.java').read_bytes()
                for path,content in adapted.items():
                    if not path.endswith('.java'):continue
                    result=localize_java_comments(path,translate_source(path,content.decode(),mapping),
                                                  language,mapping,config['native_name'])
                    for token in TOKENS.finditer(result):
                        value=token.group()
                        if value.startswith(('//','/*')) and 'Copyright' not in value:
                            self.assertIsNone(re.search('[가-힣]',value),(language,path,value))
                self.assertEqual(set(document()['comments'][language]),set(document()['comments']['my']))

    def test_native_library_messages_do_not_change_fixture_strings(self):
        from java_prose import localize_java_comments
        from source_names import make_renamer, rename_source
        from terms import names
        mapping=names('my')
        original='throw new IllegalArgumentException("잘못된 UTF-8");'
        before=rename_source('fixture.java',original,make_renamer(mapping))
        library=make_renamer(mapping)('platforms/rpi4-native/한국어자바/한국어/자체/문자.java')
        result=localize_java_comments(library,before,'my',mapping)
        self.assertIn('မမှန်သော UTF-8',result)
        self.assertEqual(localize_java_comments('platforms/rpi4-native/한국어자바/한국어/자체/문자.java',before,'my',mapping),result)
        self.assertEqual(localize_java_comments('fixture.java',before,'my',mapping),before)

    def test_burmese_dictionary_covers_owned_java_names_including_host_launcher(self):
        import re
        from generate import sources, identifiers, adapt
        from country_naming import names_for_country
        mapping=names_for_country('MMR','my')
        config=__import__('json').loads((ROOT/'country/MMR/native.json').read_text())
        profile=__import__('json').loads((ROOT/'country/MMR'/config['source']/config['native']/'input.json').read_text())
        originals,unused=adapt(sources(),'my',config['native_name'],profile)
        originals['launcher.java']=(ROOT/'native/국가실행기.java').read_bytes()
        missing=set()
        from java_prose import TOKENS,localize_java_comments
        from generate import translate_source
        for path,data in originals.items():
            if path.endswith('.java'):
                missing.update(t for t in identifiers(path,data.decode())
                               if re.search('[가-힣]',t) and t not in mapping)
                if re.search('[가-힣]',Path(path).stem) and Path(path).stem not in mapping:
                    missing.add(Path(path).stem)
                localized=localize_java_comments(path,translate_source(path,data.decode(),mapping),'my',mapping,config['native_name'])
                for match in TOKENS.finditer(localized):
                    comment=match.group()
                    if comment.startswith(('//','/*')) and 'Copyright' not in comment:
                        self.assertIsNone(re.search('[가-힣]',comment),(path,comment))
        self.assertEqual(missing,set())

    def test_burmese_exception_api_localizes_complete_sentences_and_owned_symbols(self):
        from java_prose import localize_java_comments
        from source_names import make_renamer, rename_source
        from terms import names
        mapping=names('my')
        original='''/** 한국어로 선언·던지기·잡기를 할 수 있는 상태예외. */
public class 상태예외 { public 상태예외(String 설명) { super(설명); }
public String 설명() { return getMessage(); } }'''
        translated=localize_java_comments('상태예외.java',rename_source('상태예외.java',original,make_renamer(mapping)),'my',mapping)
        self.assertFalse(any('\uac00' <= c <= '\ud7a3' for c in translated))
        self.assertIn('String ရှင်းလင်းချက်',translated)
        self.assertIn('super(ရှင်းလင်းချက်)',translated)
        self.assertIn('မြန်မာ API',translated)

    def test_comment_translation_preserves_quoted_fixtures_and_author_attribution(self):
        from java_prose import localize_java_comments
        from source_names import make_renamer, rename_source
        from terms import names
        mapping=names('my')
        original='/** 한국어로 선언·던지기·잡기를 할 수 있는 상태예외. */'
        comment=rename_source('example.java',original,make_renamer(mapping))
        fixture='String fixture = '+__import__('json').dumps(comment,ensure_ascii=False)+';'
        author='// Copyright 2020. 노성철'
        text=author+'\n'+fixture+'\n'+comment
        translated=localize_java_comments('example.java',text,'my',mapping)
        self.assertIn(author,translated)
        self.assertIn(fixture,translated)
        self.assertTrue(translated.endswith('*/'))
        self.assertEqual(localize_java_comments('example.java',translated,'my',mapping),translated)

    def test_exception_prose_uses_each_supported_edition_language(self):
        from java_prose import document, localize_java_comments
        from source_names import make_renamer, rename_source
        from terms import names
        original='/** 한국어로 선언·던지기·잡기를 할 수 있는 상태예외. */'
        for language in document()['exception_templates']:
            mapping=names(language)
            before=rename_source('example.java',original,make_renamer(mapping))
            result=localize_java_comments('example.java',before,language,mapping)
            self.assertNotEqual(result,before,language)
            self.assertFalse(any('\uac00' <= c <= '\ud7a3' for c in result),language)
        self.assertEqual(localize_java_comments('example.java',original,'stu',{}),original)
        self.assertEqual(localize_java_comments('example.java',original,'ko',{}),original)

    def test_korean_namespace_metadata_does_not_mark_korean_as_foreign(self):
        import json
        import tempfile
        from apply_country_naming import namespace_metadata
        config={'source':'source','language':'ko','identifiers':{},'owned_files':[],
                'naming':{'untranslated_identifiers':1}}
        with tempfile.TemporaryDirectory() as temporary:
            folder=Path(temporary)
            for name,value in (('native.json',config),('native-term-evidence.json',{}),('native-generated.json',{})):
                (folder/name).write_text(json.dumps(value))
            (folder/'native-pending.tsv').write_text('identifier\tstatus\n핵심\ttranslation-review-required\n')
            result=namespace_metadata(folder,None,{'namespace':{'os_name':'JChnOS'}},'revision',config)
            self.assertEqual(result['writes']['native-pending.tsv'][0],b'identifier\tstatus\n')
            self.assertEqual(json.loads(result['writes']['native.json'][0])['naming']['untranslated_identifiers'],0)

    def test_burmese_hardware_and_network_terms_do_not_use_unrelated_senses(self):
        import csv
        import json
        from compose_reviewed_roles import compose
        with (ROOT/'native/inputs/burmese-role-words.tsv').open() as stream:
            glossary={row['word']:row['proposal'] for row in csv.DictReader(stream,delimiter='\t')}
        self.assertEqual(compose('networkPort',glossary,'my'),'ကွန်ရက်ဆက်သွယ်ပေါက်')
        self.assertEqual(glossary['register'],'အမြန်မှတ်ကွက်')
        corrections=json.loads((ROOT/'native/inputs/reviewed-roles/my.json').read_text())
        self.assertEqual(corrections['names']['등록'],'ကိုင်တွယ်သူစာရင်းသွင်း')

    def test_namespace_branding_handles_a_planned_new_source_path(self):
        import json
        import tempfile
        from apply_country_naming import namespace_metadata
        config={'source':'source','identifiers':{'원천':'base','한국':'Việt_Nam','제이코로스':'JVnmOS'},
                'owned_files':['base/Việt_Nam/JVnmOS/Info.java'],'naming':{}}
        with tempfile.TemporaryDirectory() as temporary:
            folder=Path(temporary)
            for name,value in (('native.json',config),('native-term-evidence.json',{}),('native-generated.json',{})):
                (folder/name).write_text(json.dumps(value))
            name='source/'+config['owned_files'][0]
            source=b'public class Info { String name = "jkoros"; }'
            result={'folder':folder,'writes':{name:(source,0o644)},'removed':set(),'backups':{},'changes':{}}
            result=namespace_metadata(folder,result,{'namespace':{'os_name':'JVnmOS'}},'revision',config)
            self.assertIn(b'"JVnmOS"',result['writes'][name][0])
            self.assertFalse((folder/name).exists())
            manifest=json.loads(result['writes']['native-generated.json'][0])
            self.assertEqual(manifest[name],hashlib.sha256(result['writes'][name][0]).hexdigest())

    def test_managed_system_identity_is_country_specific_while_native_abi_is_stable(self):
        from country_naming import country_source_identity, names_for_country
        mapping=names_for_country('VNM','vi')
        source='return new Info("jkoros", "jkoros");'
        self.assertEqual(country_source_identity('원천/Info.java',source,mapping),
                         'return new Info("JVnmOS", "JVnmOS");')
        self.assertEqual(country_source_identity('platforms/rpi4-native/abi.c',source,mapping),source)

    def test_vietnamese_and_burmese_role_names_follow_function(self):
        from terms import names
        self.assertEqual(names('vi')['체계호출'],'LờiGọiHệThống')
        self.assertEqual(names('vi')['파일보존'],'LưuGiữTệp')
        self.assertEqual(names('my')['주소'],'လိပ်စာ')
        self.assertEqual(names('my')['보내기'],'ပို့')
        self.assertEqual(names('my')['실행영상'],'စက်ကုဒ်ပုံရိပ်')
        self.assertEqual(len(names('vi')),len(names('en')))
        self.assertFalse(any(__import__('re').search(r'_[0-9a-f]{8}$',v) for v in names('my').values()))

    def test_kernel_input_cache_excludes_only_separate_managed_inputs(self):
        from verify_country_boots import kernel_input_digest
        config={'identifiers':{},'owned_files':['원천/한국/제이코로스/핵심/핵심.java',
            '만들기.mk','문서/구조.md','example/README.md','platforms/rpi4-native/도구/빌드.py']}
        source={name:b'original' for name in config['owned_files']}
        initial=kernel_input_digest(config,source.__getitem__)
        source['원천/한국/제이코로스/핵심/핵심.java']=b'changed managed namespace'
        self.assertEqual(initial,kernel_input_digest(config,source.__getitem__))
        source['example/README.md']=b'changed boot-installed example data'
        self.assertNotEqual(initial,kernel_input_digest(config,source.__getitem__))

    def test_country_namespace_is_independent_of_edition_language(self):
        from country_naming import names_for_country, country_policy
        china = names_for_country('CHN', 'zh')
        vietnam = names_for_country('VNM', 'zh_Hant')
        self.assertEqual((china['한국'], china['제이코로스']), ('中国', 'JChnOS'))
        self.assertEqual((vietnam['한국'], vietnam['제이코로스']), ('越南', 'JVnmOS'))
        self.assertNotEqual(names_for_country('USA', 'en')['한국'], names_for_country('GBR', 'en')['한국'])
        for country, policy in country_policy().items():
            for language in policy['languages']:
                mapping = names_for_country(country, language)
                self.assertEqual(len(mapping), len(set(mapping.values())), (country, language))

    def test_country_package_paths_imports_and_main_references_agree(self):
        from country_naming import names_for_country
        mapping = names_for_country('VNM', 'zh_Hant')
        rename = renamer(mapping)
        self.assertEqual(rename('원천/한국/제이코로스/기억공간/쪽관리자.java'),
                         '基礎原始碼/越南/JVnmOS/記憶體空間/頁管理器.java')
        source = 'package 한국.제이코로스.기억공간; import 한국.제이코로스.기억공간.쪽관리자;'
        result = source_rename('Probe.java', source, rename)
        self.assertIn('package 越南.JVnmOS.記憶體空間;', result)
        self.assertIn('import 越南.JVnmOS.記憶體空間.頁管理器;', result)

    def test_character_values_and_longer_identifiers_are_preserved(self):
        change=renamer({'기억파일':'MemoryFiles','글':'text'})
        source="public class 기억파일 { char 글 = '글'; String 형식 = \"L기억파일;\"; int 기억파일수; }"
        result=source_rename('기억파일.java',source,change)
        self.assertIn('class MemoryFiles',result)
        self.assertIn("char text = '글'",result)
        self.assertIn('"LMemoryFiles;"',result)
        self.assertIn('int 기억파일수;',result)

    def test_unicode_marks_and_simultaneous_renaming(self):
        change=renamer({'พื้นที่ทำงาน':'พื้นที่ใหม่','A':'B','B':'C'})
        self.assertEqual(change('พื้นที่ทำงาน A B'), 'พื้นที่ใหม่ B C')
        self.assertEqual(change('พื้นที่ทำงานเพิ่มเติม AB'), 'พื้นที่ทำงานเพิ่มเติม AB')

    def test_only_authorized_copyright_is_accepted_as_an_ownership_change(self):
        source=b'public class Demo {}\n';expected=hashlib.sha256(source).hexdigest()
        self.assertTrue(matches_owned(COPYRIGHT+source,expected))
        self.assertFalse(matches_owned(COPYRIGHT+source+b'// custom edit\n',expected))

    def test_current_process_does_not_leak_into_generic_native_values(self):
        from terms import names
        self.assertEqual(review()['languages']['nl']['terms']['current'],'huidigProces')
        self.assertEqual(names('nl')['현재값'],'huidigeWaarde')
        self.assertEqual(names('zh_Hans')['현재값'],'当前')

    def test_country_codes_choose_languages_without_overwriting_language_editions(self):
        from country_naming import country_policy,validate_edition
        policy=country_policy()
        self.assertEqual(len(policy),249)
        self.assertEqual(policy['AIA']['name'],'Anguilla')
        self.assertEqual(policy['AIA']['representative_language'],'en')
        self.assertEqual(validate_edition(ROOT/'country/AIA',{'country':'AIA','language':'en'})['selection'],'representative')
        with self.assertRaises(ValueError):
            validate_edition(ROOT/'country/AIA',{'country':'KOR','language':'en'})
        with self.assertRaises(ValueError):
            validate_edition(ROOT/'country/AIA/en',{'country':'AIA','language':'ko'})

    def test_unicode_fixtures_survive_identifier_renaming_in_every_source_language(self):
        change=renamer({'가':'firstOperand','한글':'hangulText'})
        java='int 가; String 한글 = "한글 😀"; char c = \'가\';'
        self.assertEqual(source_rename('Probe.java',java,change),
            'int firstOperand; String hangulText = "한글 😀"; char c = \'가\';')
        python="가 = '가'\n한글 = '한글'\nprogram = 'def f(가): return 가'\n"
        self.assertEqual(source_rename('probe.py',python,change),
            "firstOperand = '가'\nhangulText = '한글'\nprogram = 'def f(firstOperand): return firstOperand'\n")

    def test_trie_keeps_longest_whole_names_and_descriptor_references(self):
        change=renamer({'가':'first','가나다':'longName','가나':'middleName'})
        self.assertEqual(change('가 가나다 가나 가나라마바사 L가나다;'),
            'first longName middleName 가나라마바사 LlongName;')

    def test_direct_translation_preserves_external_start_method(self):
        from generate import translate_source
        value='int 시작점; Process p = new ProcessBuilder(command).start();'
        self.assertEqual(translate_source('Host.java',value,{'시작점':'startingPoint'}),
            'int startingPoint; Process p = new ProcessBuilder(command).start();')

    def test_legacy_charset_alias_preserves_java_packages_and_http_parameters(self):
        text = 'import java.nio.charset.StandardCharsets; int charset; String h = "text/plain; charset=utf-8";'
        result = source_rename('Probe.java', text, renamer({'charset': 'jeuCaractères'}))
        self.assertIn('java.nio.charset.StandardCharsets', result)
        self.assertIn('int jeuCaractères;', result)
        self.assertIn('"text/plain; charset=utf-8"', result)
        embedded = 'program = "import java.nio.charset.StandardCharsets; int charset;"'
        self.assertIn('java.nio.charset.StandardCharsets; int jeuCaractères;', source_rename('test.py', embedded, renamer({'charset':'jeuCaractères'})))

    def test_standard_integer_identity_survives_owned_decoder_localization(self):
        value = 'static int 정수() { return Integer.parseInt("1"); } String owner = "java/lang/Integer";'
        result = source_rename('Probe.java', value, renamer({'정수': 'Ganzzahl', 'Integer': 'MustRemainExternal'}))
        self.assertIn('int Ganzzahl()', result)
        self.assertIn('Integer.parseInt', result)
        self.assertIn('"java/lang/Integer"', result)
        value = 'Stream<Path> paths; boolean 흐름여부 = false;'
        result = source_rename('Probe.java', value, renamer({'Stream': 'broken', '흐름여부': 'istDatenstrom'}))
        self.assertEqual(result, 'Stream<Path> paths; boolean istDatenstrom = false;')

    def test_external_options_and_owned_negative_variables_have_distinct_roles(self):
        text = 'kernel = -kernel\nargs = ["-kernel", "--source", "--output"]\n'
        result = source_rename('run.py', text, renamer({'kernel':'Núcleo','source':'fuente','output':'salida'}))
        self.assertIn('Núcleo = -Núcleo', result)
        self.assertIn('["-kernel", "--source", "--output"]', result)

    def test_build_java_paths_are_not_mistaken_for_standard_jvm_names(self):
        text = 'path = "build/verification/new-java/Swing_probar.class"; owner = "java/lang/Integer"'
        result = source_rename('test.py', text, renamer({'Swing_probar':'PruebaSwing','Integer':'broken'}))
        self.assertIn('new-java/PruebaSwing.class', result)
        self.assertIn('java/lang/Integer', result)

    def test_legacy_cli_and_class_path_repairs_preserve_other_code(self):
        from apply_native_review import repair_legacy_references
        from terms import names
        text = '# custom edit\nargs = ["-Núcleo", "kernel8.img"]; path = "build/my-java/Swing_probar.class"; x = -altura\n'
        items = tuple(sorted(names('es').items()))
        fixed = repair_legacy_references(text, 'es', items, '.py')
        self.assertIn('["-kernel", "kernel8.img"]', fixed)
        self.assertIn('build/my-java/PruebaSwing.class', fixed)
        self.assertIn('# custom edit', fixed)
        self.assertIn('x = -altura', fixed)
        self.assertEqual(repair_legacy_references(fixed, 'es', items, '.py'), fixed)

    def test_context_reconciliation_restores_interfaces_and_keeps_owned_names(self):
        from apply_native_review import reconcile_alias_tokens
        desired = 'Anfitrión = root / "host"\nparser.add_argument("--flag", action="store_true")\nvalues = {"host": "Anfitrión"}\n'
        before = 'Anfitrión = root / "Anfitrión"\nparser.add_argument("--flag", Acción="store_true")\nvalues = {"Anfitrión": "Anfitrión"}\n'
        actual = '# custom edit\n' + before
        fixed,pending = reconcile_alias_tokens(actual,before,desired)
        self.assertEqual(fixed,'# custom edit\n'+desired)
        self.assertEqual(pending,0)
        self.assertEqual(reconcile_alias_tokens(fixed,before,desired),(fixed,0))

    def test_legacy_aliases_are_marked_before_native_roles_are_translated(self):
        from apply_native_review import reconcile_alias_tokens
        raw = '단말.수(번호); String path = "host";'
        native = renamer({'단말':'Terminal','수':'númeroValor','번호':'número'})
        legacy = renamer({'número':'númeroValor','host':'Anfitrión'})
        desired = source_rename('Probe.java',raw,native)
        before = source_rename('Probe.java',legacy(raw),native)
        self.assertIn('Terminal.númeroValor(número)',before)
        fixed,pending = reconcile_alias_tokens(before,before,desired)
        self.assertEqual(fixed,'Terminal.númeroValor(número); String path = "host";')
        self.assertEqual(pending,0)

    def test_x86_processor_names_are_distinct_from_horizontal_coordinates(self):
        from terms import names
        for language in ('ja','zh_Hans','zh_Hant','de','fr','es'):
            self.assertIn('x86', names(language)['엑스문자열표'].lower())
            self.assertNotIn(names(language)['가로'], names(language)['엑스문자열표'])

    def test_default_script_glossaries_do_not_replace_explicit_script_variants(self):
        from terms import names
        self.assertEqual(names('zh'),names('zh_Hans'))
        self.assertEqual(names('ms'),names('ms_Latn'))
        self.assertNotEqual(names('zh'),names('zh_Hant'))

    def test_legal_clauses_are_preserved_while_owned_path_references_follow_renames(self):
        change=renamer({'배포':'distributionValue','수정':'modifyValue','라이선스검토':'LicenseReview'})
        text='수정·배포 권리는 원문을 따른다. See platforms/rpi4-native/라이선스검토.md\n'
        self.assertEqual(source_rename('LICENSE',text,change),
            '수정·배포 권리는 원문을 따른다. See platforms/rpi4-native/LicenseReview.md\n')
        self.assertEqual(source_rename('LICENSE','https://example.test/라이선스검토.md',change),
                         'https://example.test/라이선스검토.md')

    def test_terminology_never_assigns_neighbouring_languages_or_other_scripts(self):
        from collect_terminology_roles import targets
        self.assertEqual(targets('mr', 'MARATHI.tbx'), ['mr'])
        self.assertNotIn('hi', targets('mr', 'MARATHI.tbx'))
        self.assertEqual(targets('pa', 'PUNJABI (ARABIC).tbx'), ['pa_Arab'])
        self.assertNotIn('zh_Hant', targets('zh-CN', 'CHINESE (SIMPLIFIED).tbx'))

    def test_incomplete_functional_names_are_not_half_translated(self):
        from collect_terminology_roles import proposal
        glossary = {'file': 'संचिका', 'read': 'वाचा'}
        value, evidence = proposal(['read', 'File'], glossary, verb_last=True)
        self.assertEqual(value, 'संचिका_वाचा')
        self.assertEqual(proposal(['read', 'UnknownThing'], glossary)[0], None)
        self.assertEqual(proposal(['untranslatable'], {})[0], None)

    def test_python_module_paths_match_normalized_import_identifiers(self):
        import unicodedata
        import tempfile
        from terms import names
        for language in ('th', 'lo', 'hy'):
            mapping = names(language)
            for value in mapping.values():
                self.assertEqual(value, unicodedata.normalize('NFKC', value))
            module = mapping['명령']
            with tempfile.TemporaryDirectory() as directory:
                (Path(directory) / (module + '.py')).write_text('answer = 42\n')
                sys.path.insert(0, directory)
                try:
                    namespace = {}
                    exec('from ' + module + ' import answer', namespace)
                    self.assertEqual(namespace['answer'], 42)
                finally:
                    sys.path.remove(directory)
                    sys.modules.pop(module, None)

    def test_marathi_covers_original_paths_and_program_symbols(self):
        from generate import identifiers, sources
        from terms import names
        import re
        import unicodedata
        mapping = names('mr')
        change = renamer(mapping)
        for value in mapping.values():
            self.assertTrue(value.isidentifier(), value)
            self.assertEqual(unicodedata.normalize('NFC', value), value)
        self.assertEqual(len({unicodedata.normalize('NFKC', v) for v in mapping.values()}), len(mapping))
        owned = sources()
        owned['native-java/국가실행기.java'] = (ROOT / 'native/국가실행기.java').read_bytes()
        for path, data in owned.items():
            self.assertIsNone(re.search('[가-힣]', change(path)), path)
            try:
                text = source_rename(path, data.decode('utf-8'), change)
            except UnicodeDecodeError:
                continue
            remaining = [t for t in identifiers(path, text) if re.search('[가-힣]', t)]
            self.assertEqual(remaining, [], path)

    def test_english_role_inventory_covers_new_launcher_fields_without_merging_roles(self):
        from generate import identifiers, sources
        from terms import names
        import re
        mapping = names('en')
        self.assertNotEqual(mapping['추가인수'], mapping['부가인수'])
        owned = sources()
        owned['launcher.java'] = (ROOT / 'native/국가실행기.java').read_bytes()
        for path, data in owned.items():
            try:
                required = [t for t in identifiers(path, data.decode('utf-8')) if re.search('[가-힣]', t)]
            except UnicodeDecodeError:
                continue
            self.assertEqual(set(required) - set(mapping), set(), path)

    def test_japanese_roles_cover_the_inventory_without_opaque_suffixes(self):
        from terms import names
        import re
        mapping = names('ja')
        self.assertEqual(set(mapping), set(names('en')))
        self.assertEqual(len(set(mapping.values())), len(mapping))
        self.assertFalse(any(re.search(r'_[0-9a-f]{8}$', v) for v in mapping.values()))
        self.assertEqual(mapping['장치'], '装置')
        self.assertEqual(mapping['실행관리'], '実行管理')
        self.assertEqual(mapping['예제'], '用例')
        self.assertEqual(mapping['자바'], 'Java')

    def test_input_help_prose_keeps_its_canonical_language_spelling(self):
        from localization_runtime import repair_input_help
        source = 'static void ajuda() { terminal.escrita("em Português.\\n"); terminal.escrita("PT"); }'
        fixed = repair_input_help(source, {'한글도움말': 'ajuda'}, 'em português.')
        self.assertIn('"em português.\\n"', fixed)
        self.assertIn('terminal.escrita("PT")', fixed)

    def test_chinese_scripts_cover_the_same_roles_with_distinct_vocabulary(self):
        from terms import names
        simplified, traditional = names('zh_Hans'), names('zh_Hant')
        self.assertEqual(set(simplified), set(names('en')))
        self.assertEqual(set(traditional), set(names('en')))
        self.assertEqual(simplified['파일'], '文件')
        self.assertEqual(traditional['파일'], '檔案')
        self.assertEqual(simplified['장치'], '设备')
        self.assertEqual(traditional['장치'], '設備')
        self.assertEqual(names('zh'), simplified)

    def test_untagged_chinese_uses_the_explicit_simplified_pinyin_profile(self):
        from generate import profile
        from terms import HELP
        config = profile('zh')
        self.assertEqual(config['kind'], 'candidates')
        self.assertEqual(config['map']['ni'][0], '你')
        self.assertIn('中文拼音输入', HELP['zh'])

    def test_legacy_local_alias_does_not_rename_standard_set_calls(self):
        from source_names import rename_java_local_alias
        source = 'boolean set = true; if (set) values.set(0, x); invoke("set"); set(1);'
        result = rename_java_local_alias(source, {'set': 'correspondance'})
        self.assertIn('boolean correspondance = true; if (correspondance)', result)
        self.assertIn('values.set(0, x)', result)
        self.assertIn('invoke("set")', result)
        self.assertIn('set(1)', result)

    def test_python_byte_strings_encode_translated_text_without_losing_raw_backslashes(self):
        import ast
        from source_names import escape_python_byte_literals
        text = 'x = b"Desktop update"\ny = rb"Desktop \\n"\n'
        translated = source_rename('probe.py', text, renamer({'Desktop': 'Arbeitsfläche'}))
        module = ast.parse(translated)
        self.assertEqual(ast.literal_eval(module.body[0].value), 'Arbeitsfläche update'.encode())
        self.assertEqual(ast.literal_eval(module.body[1].value), 'Arbeitsfläche \\n'.encode())
        self.assertEqual(escape_python_byte_literals(translated), translated)

    def test_owned_bundle_alias_preserves_standard_calls_and_user_comments(self):
        from apply_native_review import mark_owned_bundle_alias, _ALIAS_MARKER
        before = 'import pack; class pack {}\nx = struct.pack("I", 1); y = "pack"; z = "pack.sh";\n'
        after = 'import ' + _ALIAS_MARKER + '; class ' + _ALIAS_MARKER + ' {}\nx = struct.pack("I", 1); y = "pack"; z = "pack.sh";\n'
        actual = '// user comment\n' + before
        fixed = mark_owned_bundle_alias(actual, before, after).replace(_ALIAS_MARKER, 'Paquete')
        self.assertTrue(fixed.startswith('// user comment\n'))
        self.assertIn('import Paquete; class Paquete {}', fixed)
        self.assertIn('struct.pack("I", 1)', fixed)
        self.assertIn('"pack"; z = "pack.sh"', fixed)

    def test_multibyte_library_name_obeys_flat_guest_lib_path_limit(self):
        import tempfile
        from unittest.mock import patch
        from collect_terminology_roles import fit_guest_limits
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            library = root / 'platforms/rpi4-native/파이썬연결/라이브러리'
            library.mkdir(parents=True)
            (library / '꾸러미.py').write_text('x = 1\n')
            example = root / 'example/python'
            example.mkdir(parents=True)
            (example / '한국어.py').write_text('x = 1\n')
            mapping = {'꾸러미': '長' * 30}
            with patch('collect_terminology_roles.jkoros_root', return_value=root):
                rejected = fit_guest_limits(mapping, set())
            self.assertEqual(rejected, {'꾸러미': 'guest-library-path-63-byte-limit'})
            self.assertNotIn('꾸러미', mapping)

    def test_image_cache_requires_pass_proof_and_exact_source_and_vendor(self):
        import tempfile
        import json
        import verify_country_boots as boots
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cache, build = root / 'cache', root / 'target'
            cache.mkdir()
            image = cache / 'source-vendor.img'
            image.write_bytes(b'verified kernel')
            checksum = boots.digest(image)
            proof = {'passed': True, 'probe_version': boots.PROBE_VERSION,
                     'source_sha256': 'source', 'kernel_sha256': checksum}
            evidence = {'source_sha256': 'source', 'vendor_sha256': 'vendor',
                        'origin_country': 'TEST', 'kernel_sha256': checksum,
                        'origin_pass_report': dict(proof, passed=False)}
            image.with_suffix('.json').write_text(json.dumps(evidence))
            self.assertIsNone(boots.reuse_kernel(cache, build, 'source', 'vendor'))
            self.assertFalse(build.exists())
            evidence['origin_pass_report'] = proof
            image.with_suffix('.json').write_text(json.dumps(evidence))
            self.assertIsNone(boots.reuse_kernel(cache, build, 'source', 'different-vendor'))
            result = boots.reuse_kernel(cache, build, 'source', 'vendor')
            self.assertEqual(result['kernel_sha256'], checksum)
            self.assertEqual(boots.digest(build / 'kernel8.img'), checksum)
            self.assertNotEqual(image.stat().st_ino, (build / 'kernel8.img').stat().st_ino)
            self.assertEqual((build / 'worldos-source.sha256').read_text().strip(), 'source')

    def test_symbol_aliases_are_distinct_from_single_character_fixtures(self):
        change = renamer({'글': 'पाठ्य', '값': 'मूल्य', '한글': 'hangulValue'})
        alias = "aliases = {'text': '글', 'value': '값', 'hangul': '한글'}"
        translated = source_rename('platforms/rpi4-native/tools/desktop.py', alias, change)
        self.assertIn("'text': 'पाठ्य'", translated)
        self.assertIn("'value': 'मूल्य'", translated)
        self.assertIn("'hangul': 'hangulValue'", translated)
        vm = 'if (말(이름상수, "글")) { char c = \'글\'; }'
        translated = source_rename('platforms/rpi4-native/사용자/자바/자바가상기계.java', vm, change)
        self.assertIn('"पाठ्य"', translated)
        self.assertIn("'글'", translated)
        self.assertEqual(source_rename('fixture.py', "s = '글'", change), "s = '글'")

if __name__=='__main__':unittest.main()
