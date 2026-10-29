// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.MKD.l_mk;
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
    private final JTextArea ИЗВОР = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField ПАТЕКА = new JTextField("ИЗВОР.java", 26);
    private final JTextField Име = new JTextField("ИЗВОР", 15);
    private final JTextField Аргументи = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Папка = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Процес;

    private String Ознака(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Текст) {
        SwingUtilities.invokeLater(() -> {
            output.append(Текст);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void ГРЕШКА(Exception exception) {
        append(Ознака("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel Панел, String key, Runnable Дејство) {
        JButton button = new JButton(Ознака(key));
        button.addActionListener(event -> Дејство.run());
        Панел.add(button);
    }

    private void Искористување() {
        try {
            ИЗВОР.setText(Files.readString(Папка.resolve(ПАТЕКА.getText()), StandardCharsets.UTF_8));
            ИЗВОР.setCaretPosition(0);
        } catch (Exception exception) { ГРЕШКА(exception); }
    }

    private boolean Зачувај() {
        try {
            Path Датотека = Папка.resolve(ПАТЕКА.getText()).normalize();
            Files.createDirectories(Датотека.getParent());
            Files.writeString(Датотека, ИЗВОР.getText(), StandardCharsets.UTF_8);
            append(Ознака("save") + ": " + Датотека + "\n");
            return true;
        } catch (Exception exception) { ГРЕШКА(exception); return false; }
    }

    private int Изврши(List<String> Команда) throws Exception {
        Процес = new ProcessBuilder(Команда).directory(Папка.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Процес.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = Процес.waitFor();
        Процес = null;
        append(Ознака("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Изврши_2) {
        if (!Зачувај()) return;
        String Датотека = Папка.resolve(ПАТЕКА.getText()).toString();
        String Класа = Име.getText().trim();
        String Текст = Аргументи.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Папка.resolve("classes"));
                int result = Изврши(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Папка.resolve("classes").toString(), Датотека));
                if (Изврши_2 && result == 0) {
                    List<String> Команда = new ArrayList<>(Arrays.asList("java", "-cp", Папка.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Класа));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Текст));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Команда.add(parser.sval);
                    Изврши(Команда);
                }
            } catch (Exception exception) { ГРЕШКА(exception); }
        });
    }

    private void Стоп() {
        Process current = Процес;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Терминал() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Папка.toFile()).start(); }
        catch (Exception exception) { ГРЕШКА(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Папка.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            ПАТЕКА.setText(chooser.getSelectedFile().getAbsolutePath());
            Искористување();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Папка);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Ознака("workspace") + " · WorldOS " + Ознака("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Стоп(); worker.shutdownNow(); System.exit(0);
            }
        });
        ИЗВОР.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ИЗВОР.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel Панел = new JPanel(new GridLayout(0, 1));
        JPanel Датотека = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Датотека.add(new JLabel(Ознака("file"))); Датотека.add(ПАТЕКА);
        Панел.add(Датотека);
        JPanel Лента_со_алатки = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Лента_со_алатки, "open", () -> choose());
        button(Лента_со_алатки, "save", () -> Зачувај());
        button(Лента_со_алатки, "compile", () -> compile(false));
        button(Лента_со_алатки, "run", () -> compile(true));
        button(Лента_со_алатки, "stop", () -> Стоп());
        button(Лента_со_алатки, "terminal", () -> Терминал());
        Панел.add(Лента_со_алатки);
        JPanel Подесувања = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Подесувања.add(new JLabel(Ознака("class"))); Подесувања.add(Име);
        Подесувања.add(new JLabel(Ознака("arguments"))); Подесувања.add(Аргументи);
        Панел.add(Подесувања);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ИЗВОР), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(Панел, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Панел.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Ознака("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ИЗВОР.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Големина = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Големина.width - 40), Math.min(760, Големина.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Искористување();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Ознака("help") + "\n");
    }

    public static void main(String[] Аргументи) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
