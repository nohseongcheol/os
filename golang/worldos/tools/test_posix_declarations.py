import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from install_posix import canonical_sources, terminology, install
from install_shells import assign, identifier
from native_source import inverse, safe, local_path
from posix_build import c_transform, c_identifiers, application_maps, verify
from posix_declaration_terms import GROUPS, KEYS, PATH_ROWS, explicit
from posix_terms import FUNCTION_KEYS, LOCAL_KEYS
from shell_build import c_transform as shell_transform
from generate_script_variants import rows


class DeclarationNames(unittest.TestCase):
    def test_every_row_is_reversible_and_valid(self):
        keys = set(FUNCTION_KEYS + LOCAL_KEYS + KEYS)
        for language in list(PATH_ROWS) + ['ja_Kana', 'ta_Taml', 'hi_Deva', 'und']:
            with self.subTest(language=language):
                values, paths, _ = terminology(Path('/nonexistent'), language)
                names = assign(keys, values)
                source = ' '.join(sorted(keys))
                self.assertEqual(c_transform(c_transform(source, names), inverse(names)), source)
                for value in paths.values():
                    identifier(value)

    def test_current_roles_and_not_misleading_roots(self):
        names, paths = explicit('ko')
        self.assertEqual(names['in_port_t'], '통신창구번호형')
        self.assertEqual(names['st_ctime'], '마지막상태변경시각')
        self.assertNotIn('생성', names['st_ctime'])
        self.assertEqual(names['INADDR_ANY'], '모든지역주소')
        self.assertEqual(names['INADDR_LOOPBACK'], '자기되돌림주소')
        self.assertEqual(paths['netinet'] + '/' + paths['in'] + '.h', '상호연결망/주소.h')
        self.assertNotEqual(paths['arpa'], '고등연구계획국')

    def test_exact_japanese_scripts(self):
        for language, low, high in [('ja_Hira', 0x3040, 0x309f), ('ja_Kana', 0x30a0, 0x30ff)]:
            names, paths = explicit(language)
            for value in list(names.values()) + list(paths.values()):
                self.assertTrue(all(low <= ord(ch) <= high or ch.isdigit() for ch in value), value)

    def test_identifier_audit_ignores_paths_literals_and_suffixes(self):
        code = '#include <netinet/in.h>\n// ignored\nunsigned value = 0x123UL; char *text = "unchanged";'
        self.assertEqual(c_identifiers(code), {'include', 'unsigned', 'value', 'char', 'text'})

    def test_legacy_headers_and_names_remain_accepted_by_compile(self):
        config = {'names': {'read': '자료읽기'}, 'includes': {'netinet/in.h': '상호연결망/주소.h'},
                  'name_aliases': {'읽기': 'read'}, 'include_aliases': {'netinet/주소.h': 'netinet/in.h'}}
        names, includes = application_maps(config)
        self.assertEqual(c_transform('#include <netinet/주소.h>\n읽기(); 자료읽기();', names, includes),
                         '#include <netinet/in.h>\nread(); read();')
        config['name_aliases']['자료읽기'] = 'write'
        with self.assertRaises(ValueError):
            application_maps(config)

    def test_shell_and_posix_lowering_agree_on_headers_and_literals(self):
        names = {'in_addr_t': '주소형', 'U': '숫자접미사아님', 'IPPROTO_UDP': '전문규약'}
        includes = {'netinet/in.h': '상호연결망/주소.h'}
        code = '#include <netinet/in.h>\nin_addr_t a = 0xffU; /* IPPROTO_UDP */ char *s = "in_addr_t";'
        self.assertEqual(c_transform(code, names, includes), shell_transform(code, names, includes))

    def test_i386_network_layout_survives_native_application_lowering(self):
        root = Path(__file__).resolve().parents[1]
        sources, _ = canonical_sources(local_path(root / '나라/KOR', '소스'))
        code = '''#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/stat.h>
_Static_assert(sizeof(in_addr_t) == 4, "address width");
_Static_assert(sizeof(in_port_t) == 2, "port width");
_Static_assert(sizeof(struct in_addr) == 4, "address structure");
_Static_assert(sizeof(struct sockaddr_in) == 16, "endpoint layout");
_Static_assert(__builtin_offsetof(struct sockaddr_in, sin_port) == 2, "port offset");
_Static_assert(__builtin_offsetof(struct sockaddr_in, sin_addr) == 4, "address offset");
_Static_assert(__builtin_offsetof(struct sockaddr_in, sin_zero) == 8, "padding offset");
_Static_assert(INADDR_LOOPBACK == 0x7f000001U && IPPROTO_UDP == 17, "wire values");
_Static_assert(__builtin_offsetof(struct stat, st_ctime) == 56, "status change layout");
int main(void) { struct sockaddr_in address; address.sin_family = AF_INET;
address.sin_port = htons(7); address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
return address.sin_port == 0; }
'''
        with tempfile.TemporaryDirectory(prefix='posix-declaration-layout-') as temporary:
            directory = Path(temporary)
            for compiler, data in sources.items():
                if compiler.startswith('include/'):
                    path = safe(directory, compiler)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(data)
            for language in ('ko', 'ja_Hira', 'ja_Kana', 'zh_Hans', 'zh_Hant', 'hi_Deva', 'ta_Taml', 'fr', 'en'):
                with self.subTest(language=language):
                    values, _, _ = terminology(Path('/nonexistent'), language)
                    names = assign(set(FUNCTION_KEYS + LOCAL_KEYS + KEYS), values)
                    native = c_transform(code, names)
                    lowered = c_transform(native, inverse(names))
                    self.assertEqual(lowered, code)
                    source = directory / 'layout.c'
                    source.write_text(lowered, encoding='utf-8')
                    subprocess.check_call(['gcc', '-m32', '-std=c11', '-nostdinc', '-ffreestanding',
                        '-Wall', '-Wextra', '-Werror', '-I' + str(directory / 'include'), '-fsyntax-only', str(source)])

    def test_path_migration_backups_and_rollback(self):
        repository = Path(__file__).resolve().parents[1]
        donor = local_path(repository / '나라/KOR', '소스')
        with tempfile.TemporaryDirectory(prefix='posix-declaration-migrate-') as temporary:
            root = Path(temporary)
            parent = root / 'ZZZ'
            tree = parent / '소스'
            tree.mkdir(parents=True)
            (parent / 'Makefile').write_text('all:\n\ttrue\n')
            (root / 'tools').mkdir()
            for name in ('posix_probe.c', 'posix_build.py', 'native_source.py'):
                shutil.copy2(str(repository / 'tools' / name), str(root / 'tools' / name))
            shutil.copytree(str(repository / 'tools/posix_library'), str(root / 'tools/posix_library'))
            shutil.copy2(str(local_path(donor, '파일대응표.tsv')), str(tree / '파일대응표.tsv'))
            for canonical, relative in rows(local_path(donor, '파일대응표.tsv'))[1:]:
                if canonical.startswith('userland/posix/'):
                    destination = safe(tree, relative)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(safe(donor, relative)), str(destination))
            record = ('ZZZ', parent, 'ko')
            install(root, record)
            package = parent / 'posix-ZZZ'
            original = (package / 'posix.json').read_bytes()
            config = json.loads(original.decode('utf-8'))
            (package / '선언/상호연결망/user-note').write_text('keep')
            values, paths, statuses = terminology(tree, 'ko')
            paths['netinet'] = '새주소계열'
            real_copy = shutil.copy2
            real_mkdtemp = tempfile.mkdtemp
            def confined(suffix=None, prefix=None, dir=None):
                return real_mkdtemp(suffix=suffix, prefix=prefix, dir=str(root))
            with patch('install_posix.terminology', return_value=(values, paths, statuses)), patch('install_posix.tempfile.mkdtemp', side_effect=confined):
                with self.assertRaisesRegex(RuntimeError, 'explicit migration'):
                    install(root, record, refresh=True)
                def failed_copy(source, destination, *args, **kwargs):
                    if str(destination).endswith('/posix-ZZZ/선언/새주소계열/주소.h'):
                        raise OSError('simulated publication failure')
                    return real_copy(source, destination, *args, **kwargs)
                with patch('install_posix.shutil.copy2', side_effect=failed_copy):
                    with self.assertRaisesRegex(OSError, 'simulated'):
                        install(root, record, refresh=True, rename=True)
                self.assertEqual((package / 'posix.json').read_bytes(), original)
                verify(package, config)
                install(root, record, refresh=True, rename=True)
            current = json.loads((package / 'posix.json').read_text(encoding='utf-8'))
            verify(package, current)
            self.assertTrue((package / '선언/새주소계열/주소.h').is_file())
            self.assertFalse((package / '선언/상호연결망/주소.h').exists())
            self.assertEqual((package / '선언/상호연결망/user-note').read_text(), 'keep')
            self.assertEqual(current['include_aliases']['상호연결망/주소.h'], 'netinet/in.h')
