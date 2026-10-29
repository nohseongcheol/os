// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.TUR.l_kk;
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
    private final JFrame Терезе = new JFrame();
    private final JTextArea Неден = new JTextArea();
    private final JTextArea Шығысы = new JTextArea();
    private final JTextField Жол_2 = new JTextField("Неден.java", 26);
    private final JTextField Аты = new JTextField("Неден", 15);
    private final JTextField Аргументтер = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Қапшық = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Үрдіс;

    private String Белгі(String Кілт) {
        return messages.getProperty(Кілт, Кілт);
    }

    private void append(String Мәтін) {
        SwingUtilities.invokeLater(() -> {
            Шығысы.append(Мәтін);
            Шығысы.setCaretPosition(Шығысы.getDocument().getLength());
        });
    }

    private void Қате(Exception exception) {
        append(Белгі("error") + ": " + exception.toString() + "\n");
    }

    private void батырма(JPanel Панель, String Кілт, Runnable Әрекет) {
        JButton батырма = new JButton(Белгі(Кілт));
        батырма.addActionListener(Оқиға -> Әрекет.run());
        Панель.add(батырма);
    }

    private void Жүктеу() {
        try {
            Неден.setText(Files.readString(Қапшық.resolve(Жол_2.getText()), StandardCharsets.UTF_8));
            Неден.setCaretPosition(0);
        } catch (Exception exception) { Қате(exception); }
    }

    private boolean Сақтау() {
        try {
            Path Файл = Қапшық.resolve(Жол_2.getText()).normalize();
            Files.createDirectories(Файл.getParent());
            Files.writeString(Файл, Неден.getText(), StandardCharsets.UTF_8);
            append(Белгі("save") + ": " + Файл + "\n");
            return true;
        } catch (Exception exception) { Қате(exception); return false; }
    }

    private int Орындау(List<String> Команда) throws Exception {
        Үрдіс = new ProcessBuilder(Команда).directory(Қапшық.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Үрдіс.getInputStream(), StandardCharsets.UTF_8))) {
            String Жол;
            while ((Жол = reader.readLine()) != null) append(Жол + "\n");
        }
        int НӘТИЖЕ = Үрдіс.waitFor();
        Үрдіс = null;
        append(Белгі("result") + ": " + НӘТИЖЕ + "\n");
        return НӘТИЖЕ;
    }

    private void compile(boolean Орындау_2) {
        if (!Сақтау()) return;
        String Файл = Қапшық.resolve(Жол_2.getText()).toString();
        String Санат = Аты.getText().trim();
        String Мәтін = Аргументтер.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Қапшық.resolve("classes"));
                int НӘТИЖЕ = Орындау(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Қапшық.resolve("classes").toString(), Файл));
                if (Орындау_2 && НӘТИЖЕ == 0) {
                    List<String> Команда = new ArrayList<>(Arrays.asList("java", "-cp", Қапшық.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Санат));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Мәтін));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Команда.add(parser.sval);
                    Орындау(Команда);
                }
            } catch (Exception exception) { Қате(exception); }
        });
    }

    private void Тоқтату() {
        Process Ағымдағы = Үрдіс;
        if (Ағымдағы != null) {
            Ағымдағы.descendants().forEach(ProcessHandle::destroyForcibly);
            Ағымдағы.destroyForcibly();
        }
    }

    private void Терминал() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Қапшық.toFile()).start(); }
        catch (Exception exception) { Қате(exception); }
    }

    private void таңдау() {
        JFileChooser chooser = new JFileChooser(Қапшық.toFile());
        if (chooser.showOpenDialog(Терезе) == JFileChooser.APPROVE_OPTION) {
            Жол_2.setText(chooser.getSelectedFile().getAbsolutePath());
            Жүктеу();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Қапшық);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Терезе.setTitle(Белгі("workspace") + " · WorldOS " + Белгі("identity"));
        Терезе.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Терезе.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Оқиға) {
                Тоқтату(); worker.shutdownNow(); System.exit(0);
            }
        });
        Неден.setFont(new Font("Monospaced", Font.PLAIN, 17));
        Неден.setTabSize(4);
        Шығысы.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Шығысы.setEditable(false);
        JPanel Панель = new JPanel(new GridLayout(0, 1));
        JPanel Файл = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Файл.add(new JLabel(Белгі("file"))); Файл.add(Жол_2);
        Панель.add(Файл);
        JPanel Панель_2 = new JPanel(new FlowLayout(FlowLayout.LEADING));
        батырма(Панель_2, "open", () -> таңдау());
        батырма(Панель_2, "save", () -> Сақтау());
        батырма(Панель_2, "compile", () -> compile(false));
        батырма(Панель_2, "run", () -> compile(true));
        батырма(Панель_2, "stop", () -> Тоқтату());
        батырма(Панель_2, "terminal", () -> Терминал());
        Панель.add(Панель_2);
        JPanel Баптаулар = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Баптаулар.add(new JLabel(Белгі("class"))); Баптаулар.add(Аты);
        Баптаулар.add(new JLabel(Белгі("arguments"))); Баптаулар.add(Аргументтер);
        Панель.add(Баптаулар);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Неден), new JScrollPane(Шығысы));
        split.setResizeWeight(0.72);
        Терезе.add(Панель, BorderLayout.NORTH);
        Терезе.add(split, BorderLayout.CENTER);
        Панель.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Белгі("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        Неден.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Шығысы.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Өлшемі = Toolkit.getDefaultToolkit().getScreenSize();
        Терезе.setSize(Math.min(1240, Өлшемі.width - 40), Math.min(760, Өлшемі.height - 60));
        Терезе.setLocationRelativeTo(null);
        Терезе.setVisible(true);
        Жүктеу();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Белгі("help") + "\n");
    }

    public static void main(String[] Аргументтер) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
