from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

COMPILER = Path(__file__).resolve().parents[1] / 'derleyici.py'


class OpenJDKPackaging(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='jkoros-full-java-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def run_command(self, args, expected=0):
        result = subprocess.run([str(p) for p in args], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=60, universal_newlines=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def package(self, inputs, entry='예제.Main', extra=()):
        output = self.root / 'dağıtım_değer dizin_değer' / 'program_f5044b9b'
        self.run_command([sys.executable, COMPILER, '--target', 'openjdk', '--entry', entry,
                          '-o', output] + list(extra) + list(inputs))
        self.assertEqual(output.read_bytes()[:4], b'\x7fELF')
        return output

    def test_objects_lambdas_reflection_threads_resources_and_relocation(self):
        source = self.root / 'Main.java'
        source.write_text('''package 예제;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.*;
interface Number { double value(); }
class Base { protected long value = 42; }
public class Main extends Base implements Number {
 public double value() { return value + 0.5; }
 public static void main(String[] args) throws Exception {
  Number x = (Number)Class.forName("예제.Main").getConstructor().newInstance();
  ExecutorService e = Executors.newSingleThreadExecutor();
  try {
   double v = e.submit(() -> x.value()).get();
   String text = new String(Main.class.getResourceAsStream("/veri.txt").readAllBytes(), StandardCharsets.UTF_8);
   System.out.println(text + ":" + v + ":" + args[0]);
  } finally { e.shutdown(); }
 }
}''')
        classes = self.root / 'classes'
        self.run_command(['javac', '-encoding', 'UTF-8', '-d', classes, source])
        (classes / 'veri.txt').write_text('한글😀')
        output = self.package([classes])
        moved = self.root / '다른 장소'
        output.parent.rename(moved)
        actual = self.run_command([moved / output.name, 'bağımsız_değişkenler $() `그대로`'])
        self.assertEqual(actual.strip(), '한글😀:42.5:bağımsız_değişkenler $() `그대로`')
        metadata = json.loads((moved / (output.name + '.app') / 'jkoros-application.json').read_text())
        self.assertTrue(metadata['runtime_jvm'])
        self.assertFalse(metadata['bytecode_aot'])

    def test_class_input_and_process_exit_status(self):
        source = self.root / 'Exit.java'
        source.write_text('public class Exit {public static void main(String[] a){System.exit(37);}}')
        self.run_command(['javac', source])
        output = self.package([source.with_suffix('.class')], entry='Exit')
        self.run_command([output], expected=37)

    def test_jar_dependency_and_java_input(self):
        dep = self.root / 'Helper.java'
        dep.write_text('public class Helper {public static String get(){return "jar dependency";}}')
        classes = self.root / 'dep'
        self.run_command(['javac', '-d', classes, dep])
        jar = self.root / 'helper.jar'
        self.run_command(['jar', 'cf', jar, '-C', classes, '.'])
        source = self.root / 'Main.java'
        source.write_text('public class Main {public static void main(String[] a){System.out.println(Helper.get());}}')
        output = self.package([source], entry='Main', extra=['--classpath', jar])
        self.assertEqual(self.run_command([output]).strip(), 'jar dependency')

    def test_native_aot_class_input(self):
        source = self.root / 'Value.java'
        source.write_text('public class Value {public static int start(){return 42;}}')
        self.run_command(['javac', '--release', '8', source])
        output = self.root / 'native'
        self.run_command([sys.executable, COMPILER, '--entry', 'Value.start', '-o', output, source.with_suffix('.class')])
        self.run_command([output], expected=42)

    def test_missing_entry_preserves_previous_output(self):
        source = self.root / 'Good.java'
        source.write_text('public class Good {public static void main(String[] a){System.out.println("good");}}')
        output = self.package([source], entry='Good')
        before = output.read_bytes()
        self.run_command([sys.executable, COMPILER, '--target', 'openjdk', '--entry', 'Missing', '-o', output, source], expected=1)
        self.assertEqual(output.read_bytes(), before)
        self.assertEqual(self.run_command([output]).strip(), 'good')


if __name__ == '__main__':
    unittest.main()
