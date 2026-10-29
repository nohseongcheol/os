import json
import os
import shutil
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from shell_build import c_transform, shell_transform
from shell_terms import vocabulary, FUNCTIONS, FIELDS, HOST
from install_shells import assign, PRIVATE, proposal, install
from fix_shell_kernel_paths import patch_cow, patch_slash, patch_aligned, function_span


class ShellSourceTests(unittest.TestCase):
    def test_all_terminology_rows_have_correct_arity(self):
        for language in set(FUNCTIONS) | set(FIELDS) | set(HOST):
            vocabulary(language)

    def test_korean_private_names_have_explicit_proposals(self):
        self.assertFalse(PRIVATE - set(vocabulary('ko')))

    def test_all_proposed_languages_cover_private_and_host_names(self):
        from install_shells import HOST_PRIVATE
        for language in FUNCTIONS:
            with self.subTest(language=language):
                self.assertFalse((PRIVATE | set(HOST_PRIVATE)) - set(vocabulary(language)))
                mapping = assign(PRIVATE, vocabulary(language))
                self.assertEqual(len(set(mapping.values())), len(PRIVATE))

    def test_length_name_describes_bytes_not_unicode_characters(self):
        self.assertEqual(vocabulary('en')['text_length'], 'text byte length')
        self.assertIn('여덟자리묶음', vocabulary('ko')['text_length'])

    def test_japanese_compound_readings_are_explicit(self):
        from install_shells import JAPANESE_READINGS
        self.assertEqual(JAPANESE_READINGS['shell_name'], 'めいれいかいしゃくき')
        self.assertEqual(JAPANESE_READINGS['arguments'], 'ひきすうれつ')
        self.assertEqual(JAPANESE_READINGS['source_file'], 'げんぶんしょ')

    def test_generated_directory_rename_is_guarded_and_preserves_local_files(self):
        from shell_build import verify
        with tempfile.TemporaryDirectory(prefix='worldos-shell-migration-test-') as temporary:
            root = Path(temporary)
            (root / 'tools').mkdir()
            for name in ('shell_template.c', 'shell_build_template.sh.in', 'shell_build.py',
                         'native_source.py', 'shell_idle.c', 'shell_probe.c'):
                shutil.copy2(str(Path(__file__).parent / name), str(root / 'tools' / name))
            parent = root / 'ZZZ'
            parent.mkdir()
            record = ('ZZZ', parent, 'en')
            install(root, record, root)
            before = parent / 'command_interpreter'
            (before / 'keep.txt').write_text('user note', encoding='utf-8')
            (before / 'build').mkdir()
            (before / 'build' / 'keep.bin').write_bytes(b'local artifact')
            values, aliases = proposal('en', root)
            values['shell_name'] = 'renamed interpreter'
            original_mkdtemp = tempfile.mkdtemp
            def confined_mkdtemp(suffix=None, prefix=None, dir=None):
                return original_mkdtemp(suffix=suffix, prefix=prefix, dir=str(root))
            with patch('install_shells.proposal', return_value=(values, aliases)), patch('install_shells.tempfile.mkdtemp', side_effect=confined_mkdtemp):
                with self.assertRaises(RuntimeError):
                    install(root, record, root, refresh=True)
                install(root, record, root, refresh=True, rename=True)
            after = parent / 'renamed_interpreter'
            self.assertFalse(before.exists())
            self.assertEqual((after / 'keep.txt').read_text(), 'user note')
            self.assertEqual((after / 'build' / 'keep.bin').read_bytes(), b'local artifact')
            config = json.loads((after / 'shell.json').read_text())
            verify(after, config)
            self.assertFalse((after / 'command_interpreter.c').exists())
            self.assertIn('renamed_interpreter', (parent / 'Makefile').read_text())
            (after / config['source']).write_text('user changed this', encoding='utf-8')
            with self.assertRaises(RuntimeError):
                install(root, record, root, refresh=True, rename=True)
            self.assertEqual((after / config['source']).read_text(), 'user changed this')

    def test_c_literals_and_abi_are_not_rewritten(self):
        source = '/* text */ char *text = "text"; write(1, text, 4);\n'
        self.assertEqual(c_transform(source, {'text': '문자열'}), '/* text */ char *문자열 = "text"; write(1, 문자열, 4);\n')

    def test_combining_marks_are_preserved(self):
        source = 'int पाठ_की_लंबाई = 1;'
        self.assertEqual(c_transform(source, {'पाठ_की_लंबाई': 'text_length'}), 'int text_length = 1;')

    def test_host_template_requires_explicit_names(self):
        self.assertEqual(shell_transform('@{원문}=$1\necho "$@{원문}"', {'원문': 'source_file'}), 'source_file=$1\necho "$source_file"')
        with self.assertRaises(ValueError):
            shell_transform('@{미등록}', {})

    def test_identifier_collisions_are_kept_distinct(self):
        mapping = assign(['first', 'second'], {'first': '같음', 'second': '같음'})
        self.assertNotEqual(mapping['first'], mapping['second'])

    def test_uncovered_language_is_not_filled_with_hindi(self):
        values, aliases = proposal('sat_Olck', Path('/tmp/worldos-variants-resources'))
        self.assertFalse(values)
        self.assertEqual(aliases['echo'], 'echo')

    def test_cow_reload_is_scoped_and_idempotent(self):
        source = 'func other() bool { return true }\nfunc private() bool {\n\tsetPTE()\n\treturn true\n}\n'
        patched = patch_cow(source, 'private', 'reload')
        self.assertEqual(patched.count('reload()'), 1)
        self.assertIn('setPTE()\n\t// Publish', patched)
        self.assertEqual(patch_cow(patched, 'private', 'reload'), patched)
        self.assertTrue(patched.startswith('func other() bool { return true }'))

    def test_polled_slash_fix_is_scoped(self):
        source = "func unrelated() byte { return '-' }\nfunc decode(sc uint8) byte {\n\tswitch sc {\n\tcase 0x35:\n\t\treturn '-'\n\t}\n\treturn 0\n}\n"
        patched = patch_slash(source, 'decode')
        self.assertIn("func unrelated() byte { return '-' }", patched)
        self.assertIn("case 0x35:\n\t\treturn '/'", patched)
        self.assertEqual(patch_slash(patched, 'decode'), patched)

    def test_aligned_allocator_method_patch_is_idempotent(self):
        source = 'func other() {}\nfunc (self *TMemoryManager) AlignedMalloc(size uint32) (Pointer, uint32) { return nil, 0 }\n'
        patched = patch_aligned(source, {'AlignedMalloc': 'AlignedMalloc'})
        self.assertTrue(patched.startswith('func other() {}\n'))
        self.assertEqual(patch_aligned(patched, {'AlignedMalloc': 'AlignedMalloc'}), patched)

    def test_real_32bit_allocator_accounts_for_alignment_padding(self):
        tools = Path(__file__).parent
        harness = (tools / 'aligned_allocator_test.go.in').read_text(encoding='utf-8')
        body = (tools / 'aligned_allocator_body.go.in').read_text(encoding='utf-8')
        with tempfile.TemporaryDirectory(prefix='worldos-alignment-test-') as temporary:
            source = Path(temporary) / 'main.go'
            source.write_text(harness.replace('@BODY@', body), encoding='utf-8')
            environment = dict(os.environ, GOARCH='386', CGO_ENABLED='0', GO111MODULE='off')
            result = subprocess.run(['go', 'run', str(source)], env=environment, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout.decode())
            self.assertIn(b'ALIGNED-ALLOCATION:PASS', result.stdout)


class InterpreterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='worldos-shell-tests-')
        cls.directory = Path(cls.temporary.name)
        source = Path(__file__).with_name('shell_template.c').read_text(encoding='utf-8')
        (cls.directory / 'shell.c').write_text(source, encoding='utf-8')
        commands = ['echo', 'exit', 'source']
        aliases = ['출력', '나가기', '해석']
        header = 'static const char *command_names[] = {' + ','.join(json.dumps(s) for s in commands) + '};\n'
        header += 'static const char *command_aliases[] = {' + ','.join(json.dumps(s, ensure_ascii=False) for s in aliases) + '};\n'
        (cls.directory / 'shell_locale.h').write_text(header, encoding='utf-8')
        cls.program = cls.directory / 'shell'
        subprocess.check_call(['gcc', '-std=c99', '-D_POSIX_C_SOURCE=200809L', '-Wall', '-Wextra', '-Werror', str(cls.directory / 'shell.c'), '-o', str(cls.program)])

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def run_shell(self, commands):
        process = subprocess.run([str(self.program)], input=commands.encode() if isinstance(commands, str) else commands,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        self.assertEqual(process.returncode, 0)
        return process.stdout.decode('utf-8')

    def test_quotes_adjacent_fragments_empty_words_and_escape(self):
        output = self.run_shell('echo one"two" \'three four\' a\\ b "" X\nexit\n')
        self.assertIn('onetwo three four a b  X\n', output)

    def test_native_commands_and_payload(self):
        output = self.run_shell('출력 "한글 हिन्दी தமிழ்"\n나가기\n')
        self.assertIn('한글 हिन्दी தமிழ்', output)
        self.assertIn('WORLDOS-SHELL:EXIT', output)

    def test_bad_quote_does_not_execute_prefix(self):
        output = self.run_shell('echo NEVER_PRINT "unfinished\necho NEXT_OK\nexit\n')
        self.assertNotIn('NEVER_PRINT', output)
        self.assertIn('syntax error', output)
        self.assertIn('NEXT_OK', output)

    def test_trailing_escape_is_rejected(self):
        output = self.run_shell('echo NEVER_PRINT \\\nexit\n')
        self.assertIn('syntax error', output)
        self.assertNotIn('NEVER_PRINT', output)

    def test_argument_overflow_does_not_execute_prefix(self):
        output = self.run_shell('echo NEVER_PRINT ' + 'x ' * 16 + '\necho NEXT_OK\nexit\n')
        self.assertNotIn('NEVER_PRINT', output)
        self.assertIn('NEXT_OK', output)

    def test_line_overflow_is_drained(self):
        output = self.run_shell('echo NEVER_PRINT' + 'x' * 600 + '\necho NEXT_OK\nexit\n')
        self.assertNotIn('NEVER_PRINT', output)
        self.assertIn('input rejected', output)
        self.assertIn('NEXT_OK', output)

    def test_binary_line_does_not_execute_prefix(self):
        output = self.run_shell(b'echo NEVER_PRINT\x00\necho NEXT_OK\nexit\n')
        self.assertNotIn('NEVER_PRINT', output)
        self.assertIn('NEXT_OK', output)

    def test_end_of_file_after_partial_line(self):
        self.assertIn('EOF_OK', self.run_shell('echo EOF_OK'))

    def test_input_buffer_boundaries(self):
        value = 'a' * 255 + '한글' + 'b' * 220
        self.assertIn(value, self.run_shell('echo "' + value + '"\nexit\n'))

    def test_oversize_datagram_is_rejected_without_truncation(self):
        self.assertIn('udp: message exceeds 95 bytes', self.run_shell('udp "' + '가' * 32 + '"\nexit\n'))

    def test_comment_boundary(self):
        output = self.run_shell('echo yes#part # NEVER_PRINT\nexit\n')
        self.assertIn('yes#part\n', output)
        self.assertNotIn('NEVER_PRINT', output)

    def test_utf8_backspace_removes_a_codepoint(self):
        output = self.run_shell('echo 한글\b국\nexit\n')
        self.assertIn('한국\n', output)

    def test_script_nesting_is_bounded(self):
        script = self.directory / 'recursive'
        script.write_text('source ' + str(script) + '\n', encoding='utf-8')
        output = self.run_shell('source ' + str(script) + '\necho NEXT_OK\nexit\n')
        self.assertIn('nesting limit', output)
        self.assertIn('NEXT_OK', output)

    def test_exit_propagates_out_of_command_file(self):
        script = self.directory / 'script'
        script.write_text('출력 FROM_SCRIPT\n나가기\n출력 NEVER_PRINT\n', encoding='utf-8')
        output = self.run_shell('해석 ' + str(script) + '\necho NEVER_PRINT\n')
        self.assertIn('FROM_SCRIPT', output)
        self.assertNotIn('NEVER_PRINT', output)


if __name__ == '__main__':
    unittest.main()
