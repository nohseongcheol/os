// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.RUS.l_sr;
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
    private final JFrame Прозор = new JFrame();
    private final JTextArea ИЗВОР = new JTextArea();
    private final JTextArea Излаз = new JTextArea();
    private final JTextField ПУТАЊА = new JTextField("ИЗВОР.java", 26);
    private final JTextField Назив = new JTextField("ИЗВОР", 15);
    private final JTextField Аргументи = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Фасцикла = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Процес;

    private String Натпис(String Кључ) {
        return messages.getProperty(Кључ, Кључ);
    }

    private void append(String Текст) {
        SwingUtilities.invokeLater(() -> {
            Излаз.append(Текст);
            Излаз.setCaretPosition(Излаз.getDocument().getLength());
        });
    }

    private void ГРЕШКА(Exception exception) {
        append(Натпис("error") + ": " + exception.toString() + "\n");
    }

    private void дугме(JPanel Панел, String Кључ, Runnable радња) {
        JButton дугме = new JButton(Натпис(Кључ));
        дугме.addActionListener(Догађај -> радња.run());
        Панел.add(дугме);
    }

    private void Оптерећење() {
        try {
            ИЗВОР.setText(Files.readString(Фасцикла.resolve(ПУТАЊА.getText()), StandardCharsets.UTF_8));
            ИЗВОР.setCaretPosition(0);
        } catch (Exception exception) { ГРЕШКА(exception); }
    }

    private boolean Сачувај() {
        try {
            Path Датотека = Фасцикла.resolve(ПУТАЊА.getText()).normalize();
            Files.createDirectories(Датотека.getParent());
            Files.writeString(Датотека, ИЗВОР.getText(), StandardCharsets.UTF_8);
            append(Натпис("save") + ": " + Датотека + "\n");
            return true;
        } catch (Exception exception) { ГРЕШКА(exception); return false; }
    }

    private int Изврши(List<String> Наредба) throws Exception {
        Процес = new ProcessBuilder(Наредба).directory(Фасцикла.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Процес.getInputStream(), StandardCharsets.UTF_8))) {
            String Ред;
            while ((Ред = reader.readLine()) != null) append(Ред + "\n");
        }
        int ИСХОД = Процес.waitFor();
        Процес = null;
        append(Натпис("result") + ": " + ИСХОД + "\n");
        return ИСХОД;
    }

    private void compile(boolean Покрени) {
        if (!Сачувај()) return;
        String Датотека = Фасцикла.resolve(ПУТАЊА.getText()).toString();
        String класа = Назив.getText().trim();
        String Текст = Аргументи.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Фасцикла.resolve("classes"));
                int ИСХОД = Изврши(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Фасцикла.resolve("classes").toString(), Датотека));
                if (Покрени && ИСХОД == 0) {
                    List<String> Наредба = new ArrayList<>(Arrays.asList("java", "-cp", Фасцикла.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", класа));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Текст));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Наредба.add(parser.sval);
                    Изврши(Наредба);
                }
            } catch (Exception exception) { ГРЕШКА(exception); }
        });
    }

    private void Заустави() {
        Process Тренутно = Процес;
        if (Тренутно != null) {
            Тренутно.descendants().forEach(ProcessHandle::destroyForcibly);
            Тренутно.destroyForcibly();
        }
    }

    private void Терминал() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Фасцикла.toFile()).start(); }
        catch (Exception exception) { ГРЕШКА(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Фасцикла.toFile());
        if (chooser.showOpenDialog(Прозор) == JFileChooser.APPROVE_OPTION) {
            ПУТАЊА.setText(chooser.getSelectedFile().getAbsolutePath());
            Оптерећење();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Фасцикла);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Прозор.setTitle(Натпис("workspace") + " · WorldOS " + Натпис("identity"));
        Прозор.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Прозор.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Догађај) {
                Заустави(); worker.shutdownNow(); System.exit(0);
            }
        });
        ИЗВОР.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ИЗВОР.setTabSize(4);
        Излаз.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Излаз.setEditable(false);
        JPanel Панел = new JPanel(new GridLayout(0, 1));
        JPanel Датотека = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Датотека.add(new JLabel(Натпис("file"))); Датотека.add(ПУТАЊА);
        Панел.add(Датотека);
        JPanel Трака_алата = new JPanel(new FlowLayout(FlowLayout.LEADING));
        дугме(Трака_алата, "open", () -> choose());
        дугме(Трака_алата, "save", () -> Сачувај());
        дугме(Трака_алата, "compile", () -> compile(false));
        дугме(Трака_алата, "run", () -> compile(true));
        дугме(Трака_алата, "stop", () -> Заустави());
        дугме(Трака_алата, "terminal", () -> Терминал());
        Панел.add(Трака_алата);
        JPanel Поставке = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Поставке.add(new JLabel(Натпис("class"))); Поставке.add(Назив);
        Поставке.add(new JLabel(Натпис("arguments"))); Поставке.add(Аргументи);
        Панел.add(Поставке);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ИЗВОР), new JScrollPane(Излаз));
        split.setResizeWeight(0.72);
        Прозор.add(Панел, BorderLayout.NORTH);
        Прозор.add(split, BorderLayout.CENTER);
        Панел.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Натпис("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ИЗВОР.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Излаз.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Величина = Toolkit.getDefaultToolkit().getScreenSize();
        Прозор.setSize(Math.min(1240, Величина.width - 40), Math.min(760, Величина.height - 60));
        Прозор.setLocationRelativeTo(null);
        Прозор.setVisible(true);
        Оптерећење();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Натпис("help") + "\n");
    }

    public static void main(String[] Аргументи) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
