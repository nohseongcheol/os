// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.RUS.l_mn;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.List;
import java.util.concurrent.*;
import javax.swing.*;

/** WorldOS project-owned source. Standard Java API names are preserved. */
public final class Workspace {
    private final JFrame window = new JFrame();
    private final JTextArea ЭХ = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField ЗАМ = new JTextField("ЭХ.java", 26);
    private final JTextField Нэр = new JTextField("ЭХ", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Лавлах = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String Тэмдэг(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Бичвэр) {
        SwingUtilities.invokeLater(() -> {
            output.append(Бичвэр);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void Алдаа(Exception exception) {
        append(Тэмдэг("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String key, Runnable Үйлдэл) {
        JButton button = new JButton(Тэмдэг(key));
        button.addActionListener(event -> Үйлдэл.run());
        panel.add(button);
    }

    private void Процессор_ачаалж_байна() {
        try {
            ЭХ.setText(Files.readString(Лавлах.resolve(ЗАМ.getText()), StandardCharsets.UTF_8));
            ЭХ.setCaretPosition(0);
        } catch (Exception exception) { Алдаа(exception); }
    }

    private boolean Хадгалах() {
        try {
            Path Файл = Лавлах.resolve(ЗАМ.getText()).normalize();
            Files.createDirectories(Файл.getParent());
            Files.writeString(Файл, ЭХ.getText(), StandardCharsets.UTF_8);
            append(Тэмдэг("save") + ": " + Файл + "\n");
            return true;
        } catch (Exception exception) { Алдаа(exception); return false; }
    }

    private int execute(List<String> Тушаал) throws Exception {
        process = new ProcessBuilder(Тушаал).directory(Лавлах.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String Шугам;
            while ((Шугам = reader.readLine()) != null) append(Шугам + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(Тэмдэг("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Ажиллуулах) {
        if (!Хадгалах()) return;
        String Файл = Лавлах.resolve(ЗАМ.getText()).toString();
        String Анги = Нэр.getText().trim();
        String Бичвэр = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Лавлах.resolve("classes"));
                int result = execute(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Лавлах.resolve("classes").toString(), Файл));
                if (Ажиллуулах && result == 0) {
                    List<String> Тушаал = new ArrayList<>(Arrays.asList("java", "-cp", Лавлах.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Анги));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Бичвэр));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Тушаал.add(parser.sval);
                    execute(Тушаал);
                }
            } catch (Exception exception) { Алдаа(exception); }
        });
    }

    private void Зогс() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Терминал() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Лавлах.toFile()).start(); }
        catch (Exception exception) { Алдаа(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Лавлах.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            ЗАМ.setText(chooser.getSelectedFile().getAbsolutePath());
            Процессор_ачаалж_байна();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Лавлах);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Тэмдэг("workspace") + " · WorldOS " + Тэмдэг("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Зогс(); worker.shutdownNow(); System.exit(0);
            }
        });
        ЭХ.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ЭХ.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Файл = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Файл.add(new JLabel(Тэмдэг("file"))); Файл.add(ЗАМ);
        panel.add(Файл);
        JPanel Хэрэгслийн_мөр = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Хэрэгслийн_мөр, "open", () -> choose());
        button(Хэрэгслийн_мөр, "save", () -> Хадгалах());
        button(Хэрэгслийн_мөр, "compile", () -> compile(false));
        button(Хэрэгслийн_мөр, "run", () -> compile(true));
        button(Хэрэгслийн_мөр, "stop", () -> Зогс());
        button(Хэрэгслийн_мөр, "terminal", () -> Терминал());
        panel.add(Хэрэгслийн_мөр);
        JPanel Тохиргоо = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Тохиргоо.add(new JLabel(Тэмдэг("class"))); Тохиргоо.add(Нэр);
        Тохиргоо.add(new JLabel(Тэмдэг("arguments"))); Тохиргоо.add(arguments);
        panel.add(Тохиргоо);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ЭХ), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Тэмдэг("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ЭХ.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Хэмжээ = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Хэмжээ.width - 40), Math.min(760, Хэмжээ.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Процессор_ачаалж_байна();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Тэмдэг("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
