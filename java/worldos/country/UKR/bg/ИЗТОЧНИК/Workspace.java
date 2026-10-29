// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.UKR.l_bg;
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
    private final JFrame Прозорец = new JFrame();
    private final JTextArea ИЗТОЧНИК = new JTextArea();
    private final JTextArea Изход = new JTextArea();
    private final JTextField ПЪТ = new JTextField("ИЗТОЧНИК.java", 26);
    private final JTextField Име = new JTextField("ИЗТОЧНИК", 15);
    private final JTextField Параметри = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Директория = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Процес;

    private String Етикет(String Ключ) {
        return messages.getProperty(Ключ, Ключ);
    }

    private void append(String Текст) {
        SwingUtilities.invokeLater(() -> {
            Изход.append(Текст);
            Изход.setCaretPosition(Изход.getDocument().getLength());
        });
    }

    private void ГРЕШКА(Exception exception) {
        append(Етикет("error") + ": " + exception.toString() + "\n");
    }

    private void бутон(JPanel Панел, String Ключ, Runnable Операция) {
        JButton бутон = new JButton(Етикет(Ключ));
        бутон.addActionListener(Събитие -> Операция.run());
        Панел.add(бутон);
    }

    private void Натовареност() {
        try {
            ИЗТОЧНИК.setText(Files.readString(Директория.resolve(ПЪТ.getText()), StandardCharsets.UTF_8));
            ИЗТОЧНИК.setCaretPosition(0);
        } catch (Exception exception) { ГРЕШКА(exception); }
    }

    private boolean Запазване() {
        try {
            Path Файл = Директория.resolve(ПЪТ.getText()).normalize();
            Files.createDirectories(Файл.getParent());
            Files.writeString(Файл, ИЗТОЧНИК.getText(), StandardCharsets.UTF_8);
            append(Етикет("save") + ": " + Файл + "\n");
            return true;
        } catch (Exception exception) { ГРЕШКА(exception); return false; }
    }

    private int Изпълнение(List<String> Команда) throws Exception {
        Процес = new ProcessBuilder(Команда).directory(Директория.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Процес.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int РЕЗУЛТАТ = Процес.waitFor();
        Процес = null;
        append(Етикет("result") + ": " + РЕЗУЛТАТ + "\n");
        return РЕЗУЛТАТ;
    }

    private void compile(boolean Стартиране) {
        if (!Запазване()) return;
        String Файл = Директория.resolve(ПЪТ.getText()).toString();
        String Клас = Име.getText().trim();
        String Текст = Параметри.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Директория.resolve("classes"));
                int РЕЗУЛТАТ = Изпълнение(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Директория.resolve("classes").toString(), Файл));
                if (Стартиране && РЕЗУЛТАТ == 0) {
                    List<String> Команда = new ArrayList<>(Arrays.asList("java", "-cp", Директория.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Клас));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Текст));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Команда.add(parser.sval);
                    Изпълнение(Команда);
                }
            } catch (Exception exception) { ГРЕШКА(exception); }
        });
    }

    private void Спиране() {
        Process Текуща_дата = Процес;
        if (Текуща_дата != null) {
            Текуща_дата.descendants().forEach(ProcessHandle::destroyForcibly);
            Текуща_дата.destroyForcibly();
        }
    }

    private void Терминал() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Директория.toFile()).start(); }
        catch (Exception exception) { ГРЕШКА(exception); }
    }

    private void избор() {
        JFileChooser chooser = new JFileChooser(Директория.toFile());
        if (chooser.showOpenDialog(Прозорец) == JFileChooser.APPROVE_OPTION) {
            ПЪТ.setText(chooser.getSelectedFile().getAbsolutePath());
            Натовареност();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Директория);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Прозорец.setTitle(Етикет("workspace") + " · WorldOS " + Етикет("identity"));
        Прозорец.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Прозорец.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Събитие) {
                Спиране(); worker.shutdownNow(); System.exit(0);
            }
        });
        ИЗТОЧНИК.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ИЗТОЧНИК.setTabSize(4);
        Изход.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Изход.setEditable(false);
        JPanel Панел = new JPanel(new GridLayout(0, 1));
        JPanel Файл = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Файл.add(new JLabel(Етикет("file"))); Файл.add(ПЪТ);
        Панел.add(Файл);
        JPanel Лента_с_инструменти = new JPanel(new FlowLayout(FlowLayout.LEADING));
        бутон(Лента_с_инструменти, "open", () -> избор());
        бутон(Лента_с_инструменти, "save", () -> Запазване());
        бутон(Лента_с_инструменти, "compile", () -> compile(false));
        бутон(Лента_с_инструменти, "run", () -> compile(true));
        бутон(Лента_с_инструменти, "stop", () -> Спиране());
        бутон(Лента_с_инструменти, "terminal", () -> Терминал());
        Панел.add(Лента_с_инструменти);
        JPanel Настройки = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Настройки.add(new JLabel(Етикет("class"))); Настройки.add(Име);
        Настройки.add(new JLabel(Етикет("arguments"))); Настройки.add(Параметри);
        Панел.add(Настройки);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ИЗТОЧНИК), new JScrollPane(Изход));
        split.setResizeWeight(0.72);
        Прозорец.add(Панел, BorderLayout.NORTH);
        Прозорец.add(split, BorderLayout.CENTER);
        Панел.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Етикет("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ИЗТОЧНИК.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Изход.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Размер = Toolkit.getDefaultToolkit().getScreenSize();
        Прозорец.setSize(Math.min(1240, Размер.width - 40), Math.min(760, Размер.height - 60));
        Прозорец.setLocationRelativeTo(null);
        Прозорец.setVisible(true);
        Натовареност();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Етикет("help") + "\n");
    }

    public static void main(String[] Параметри) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
