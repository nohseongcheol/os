// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.KGZ.l_ky;
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
    private final JTextArea Булак = new JTextArea();
    private final JTextArea Чыгыш = new JTextArea();
    private final JTextField ЖОЛ = new JTextField("Булак.java", 26);
    private final JTextField Аты = new JTextField("Булак", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Каталогу = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Процесси;

    private String label(String Ачкыч) {
        return messages.getProperty(Ачкыч, Ачкыч);
    }

    private void append(String Текст) {
        SwingUtilities.invokeLater(() -> {
            Чыгыш.append(Текст);
            Чыгыш.setCaretPosition(Чыгыш.getDocument().getLength());
        });
    }

    private void Ката(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel Панель, String Ачкыч, Runnable Аракети) {
        JButton button = new JButton(label(Ачкыч));
        button.addActionListener(event -> Аракети.run());
        Панель.add(button);
    }

    private void Жүктөө() {
        try {
            Булак.setText(Files.readString(Каталогу.resolve(ЖОЛ.getText()), StandardCharsets.UTF_8));
            Булак.setCaretPosition(0);
        } catch (Exception exception) { Ката(exception); }
    }

    private boolean Сактоо() {
        try {
            Path Файл = Каталогу.resolve(ЖОЛ.getText()).normalize();
            Files.createDirectories(Файл.getParent());
            Files.writeString(Файл, Булак.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + Файл + "\n");
            return true;
        } catch (Exception exception) { Ката(exception); return false; }
    }

    private int execute(List<String> Команда) throws Exception {
        Процесси = new ProcessBuilder(Команда).directory(Каталогу.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Процесси.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = Процесси.waitFor();
        Процесси = null;
        append(label("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Жүргүзүү) {
        if (!Сактоо()) return;
        String Файл = Каталогу.resolve(ЖОЛ.getText()).toString();
        String className = Аты.getText().trim();
        String Текст = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Каталогу.resolve("classes"));
                int result = execute(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Каталогу.resolve("classes").toString(), Файл));
                if (Жүргүзүү && result == 0) {
                    List<String> Команда = new ArrayList<>(Arrays.asList("java", "-cp", Каталогу.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Текст));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Команда.add(parser.sval);
                    execute(Команда);
                }
            } catch (Exception exception) { Ката(exception); }
        });
    }

    private void Токтотуу() {
        Process current = Процесси;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Терминал() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Каталогу.toFile()).start(); }
        catch (Exception exception) { Ката(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Каталогу.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            ЖОЛ.setText(chooser.getSelectedFile().getAbsolutePath());
            Жүктөө();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Каталогу);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(label("workspace") + " · WorldOS " + label("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Токтотуу(); worker.shutdownNow(); System.exit(0);
            }
        });
        Булак.setFont(new Font("Monospaced", Font.PLAIN, 17));
        Булак.setTabSize(4);
        Чыгыш.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Чыгыш.setEditable(false);
        JPanel Панель = new JPanel(new GridLayout(0, 1));
        JPanel Файл = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Файл.add(new JLabel(label("file"))); Файл.add(ЖОЛ);
        Панель.add(Файл);
        JPanel Аспап_панели = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Аспап_панели, "open", () -> choose());
        button(Аспап_панели, "save", () -> Сактоо());
        button(Аспап_панели, "compile", () -> compile(false));
        button(Аспап_панели, "run", () -> compile(true));
        button(Аспап_панели, "stop", () -> Токтотуу());
        button(Аспап_панели, "terminal", () -> Терминал());
        Панель.add(Аспап_панели);
        JPanel settings = new JPanel(new FlowLayout(FlowLayout.LEADING));
        settings.add(new JLabel(label("class"))); settings.add(Аты);
        settings.add(new JLabel(label("arguments"))); settings.add(arguments);
        Панель.add(settings);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Булак), new JScrollPane(Чыгыш));
        split.setResizeWeight(0.72);
        window.add(Панель, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Панель.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(label("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        Булак.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Чыгыш.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Өлчөмү = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Өлчөмү.width - 40), Math.min(760, Өлчөмү.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Жүктөө();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(label("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
