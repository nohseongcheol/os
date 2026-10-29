// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.BLR.l_be;
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
    private final JTextArea КРЫНІЦА = new JTextArea();
    private final JTextArea Выхад = new JTextArea();
    private final JTextField ШЛЯХ = new JTextField("КРЫНІЦА.java", 26);
    private final JTextField Назва = new JTextField("КРЫНІЦА", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Тэчка = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Працэс;

    private String Адмеціна(String Ключ) {
        return messages.getProperty(Ключ, Ключ);
    }

    private void append(String Тэкст) {
        SwingUtilities.invokeLater(() -> {
            Выхад.append(Тэкст);
            Выхад.setCaretPosition(Выхад.getDocument().getLength());
        });
    }

    private void ПАМЫЛКА(Exception exception) {
        append(Адмеціна("error") + ": " + exception.toString() + "\n");
    }

    private void кнопка(JPanel Панэль, String Ключ, Runnable Дзеянне) {
        JButton кнопка = new JButton(Адмеціна(Ключ));
        кнопка.addActionListener(Падзея -> Дзеянне.run());
        Панэль.add(кнопка);
    }

    private void Загрузка() {
        try {
            КРЫНІЦА.setText(Files.readString(Тэчка.resolve(ШЛЯХ.getText()), StandardCharsets.UTF_8));
            КРЫНІЦА.setCaretPosition(0);
        } catch (Exception exception) { ПАМЫЛКА(exception); }
    }

    private boolean Захаваць() {
        try {
            Path Файл = Тэчка.resolve(ШЛЯХ.getText()).normalize();
            Files.createDirectories(Файл.getParent());
            Files.writeString(Файл, КРЫНІЦА.getText(), StandardCharsets.UTF_8);
            append(Адмеціна("save") + ": " + Файл + "\n");
            return true;
        } catch (Exception exception) { ПАМЫЛКА(exception); return false; }
    }

    private int Выкананне(List<String> Загад) throws Exception {
        Працэс = new ProcessBuilder(Загад).directory(Тэчка.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Працэс.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = Працэс.waitFor();
        Працэс = null;
        append(Адмеціна("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Выканаць) {
        if (!Захаваць()) return;
        String Файл = Тэчка.resolve(ШЛЯХ.getText()).toString();
        String Клас = Назва.getText().trim();
        String Тэкст = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Тэчка.resolve("classes"));
                int result = Выкананне(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Тэчка.resolve("classes").toString(), Файл));
                if (Выканаць && result == 0) {
                    List<String> Загад = new ArrayList<>(Arrays.asList("java", "-cp", Тэчка.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Клас));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Тэкст));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Загад.add(parser.sval);
                    Выкананне(Загад);
                }
            } catch (Exception exception) { ПАМЫЛКА(exception); }
        });
    }

    private void Спыніць() {
        Process Дзейны = Працэс;
        if (Дзейны != null) {
            Дзейны.descendants().forEach(ProcessHandle::destroyForcibly);
            Дзейны.destroyForcibly();
        }
    }

    private void Тэрмінал() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Тэчка.toFile()).start(); }
        catch (Exception exception) { ПАМЫЛКА(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Тэчка.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            ШЛЯХ.setText(chooser.getSelectedFile().getAbsolutePath());
            Загрузка();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Тэчка);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Адмеціна("workspace") + " · WorldOS " + Адмеціна("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Падзея) {
                Спыніць(); worker.shutdownNow(); System.exit(0);
            }
        });
        КРЫНІЦА.setFont(new Font("Monospaced", Font.PLAIN, 17));
        КРЫНІЦА.setTabSize(4);
        Выхад.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Выхад.setEditable(false);
        JPanel Панэль = new JPanel(new GridLayout(0, 1));
        JPanel Файл = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Файл.add(new JLabel(Адмеціна("file"))); Файл.add(ШЛЯХ);
        Панэль.add(Файл);
        JPanel Панэль_начыння = new JPanel(new FlowLayout(FlowLayout.LEADING));
        кнопка(Панэль_начыння, "open", () -> choose());
        кнопка(Панэль_начыння, "save", () -> Захаваць());
        кнопка(Панэль_начыння, "compile", () -> compile(false));
        кнопка(Панэль_начыння, "run", () -> compile(true));
        кнопка(Панэль_начыння, "stop", () -> Спыніць());
        кнопка(Панэль_начыння, "terminal", () -> Тэрмінал());
        Панэль.add(Панэль_начыння);
        JPanel Усталёўкі = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Усталёўкі.add(new JLabel(Адмеціна("class"))); Усталёўкі.add(Назва);
        Усталёўкі.add(new JLabel(Адмеціна("arguments"))); Усталёўкі.add(arguments);
        Панэль.add(Усталёўкі);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(КРЫНІЦА), new JScrollPane(Выхад));
        split.setResizeWeight(0.72);
        window.add(Панэль, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Панэль.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Адмеціна("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        КРЫНІЦА.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Выхад.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Памер = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Памер.width - 40), Math.min(760, Памер.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Загрузка();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Адмеціна("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
