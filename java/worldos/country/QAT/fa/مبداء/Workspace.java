// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.QAT.l_fa;
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
    private final JTextArea مبداء = new JTextArea();
    private final JTextArea خروجی = new JTextArea();
    private final JTextField مسیر = new JTextField("مبداء.java", 26);
    private final JTextField نام = new JTextField("مبداء", 15);
    private final JTextField نشانوندها = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path فهرست_راهنما = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String برچسب(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String متن) {
        SwingUtilities.invokeLater(() -> {
            خروجی.append(متن);
            خروجی.setCaretPosition(خروجی.getDocument().getLength());
        });
    }

    private void خطا(Exception exception) {
        append(برچسب("error") + ": " + exception.toString() + "\n");
    }

    private void دکمه(JPanel تابلو, String key, Runnable کنش) {
        JButton دکمه = new JButton(برچسب(key));
        دکمه.addActionListener(event -> کنش.run());
        تابلو.add(دکمه);
    }

    private void بار() {
        try {
            مبداء.setText(Files.readString(فهرست_راهنما.resolve(مسیر.getText()), StandardCharsets.UTF_8));
            مبداء.setCaretPosition(0);
        } catch (Exception exception) { خطا(exception); }
    }

    private boolean ذخیره() {
        try {
            Path پرونده = فهرست_راهنما.resolve(مسیر.getText()).normalize();
            Files.createDirectories(پرونده.getParent());
            Files.writeString(پرونده, مبداء.getText(), StandardCharsets.UTF_8);
            append(برچسب("save") + ": " + پرونده + "\n");
            return true;
        } catch (Exception exception) { خطا(exception); return false; }
    }

    private int اجرا(List<String> فرمان) throws Exception {
        process = new ProcessBuilder(فرمان).directory(فهرست_راهنما.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String خط;
            while ((خط = reader.readLine()) != null) append(خط + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(برچسب("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean اجرا_2) {
        if (!ذخیره()) return;
        String پرونده = فهرست_راهنما.resolve(مسیر.getText()).toString();
        String رده = نام.getText().trim();
        String متن = نشانوندها.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(فهرست_راهنما.resolve("classes"));
                int result = اجرا(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", فهرست_راهنما.resolve("classes").toString(), پرونده));
                if (اجرا_2 && result == 0) {
                    List<String> فرمان = new ArrayList<>(Arrays.asList("java", "-cp", فهرست_راهنما.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", رده));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(متن));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) فرمان.add(parser.sval);
                    اجرا(فرمان);
                }
            } catch (Exception exception) { خطا(exception); }
        });
    }

    private void توقف() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void پایانه() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(فهرست_راهنما.toFile()).start(); }
        catch (Exception exception) { خطا(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(فهرست_راهنما.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            مسیر.setText(chooser.getSelectedFile().getAbsolutePath());
            بار();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(فهرست_راهنما);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(برچسب("workspace") + " · WorldOS " + برچسب("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                توقف(); worker.shutdownNow(); System.exit(0);
            }
        });
        مبداء.setFont(new Font("Monospaced", Font.PLAIN, 17));
        مبداء.setTabSize(4);
        خروجی.setFont(new Font("Monospaced", Font.PLAIN, 14));
        خروجی.setEditable(false);
        JPanel تابلو = new JPanel(new GridLayout(0, 1));
        JPanel پرونده = new JPanel(new FlowLayout(FlowLayout.LEADING));
        پرونده.add(new JLabel(برچسب("file"))); پرونده.add(مسیر);
        تابلو.add(پرونده);
        JPanel نوار_ابزار = new JPanel(new FlowLayout(FlowLayout.LEADING));
        دکمه(نوار_ابزار, "open", () -> choose());
        دکمه(نوار_ابزار, "save", () -> ذخیره());
        دکمه(نوار_ابزار, "compile", () -> compile(false));
        دکمه(نوار_ابزار, "run", () -> compile(true));
        دکمه(نوار_ابزار, "stop", () -> توقف());
        دکمه(نوار_ابزار, "terminal", () -> پایانه());
        تابلو.add(نوار_ابزار);
        JPanel تنظیمات = new JPanel(new FlowLayout(FlowLayout.LEADING));
        تنظیمات.add(new JLabel(برچسب("class"))); تنظیمات.add(نام);
        تنظیمات.add(new JLabel(برچسب("arguments"))); تنظیمات.add(نشانوندها);
        تابلو.add(تنظیمات);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(مبداء), new JScrollPane(خروجی));
        split.setResizeWeight(0.72);
        window.add(تابلو, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        تابلو.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(برچسب("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        مبداء.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        خروجی.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension اندازه = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, اندازه.width - 40), Math.min(760, اندازه.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        بار();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(برچسب("help") + "\n");
    }

    public static void main(String[] نشانوندها) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
