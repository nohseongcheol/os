// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.UZB.l_uz;
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
    private final JTextArea source = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField path = new JTextField("source.java", 26);
    private final JTextField Nomi = new JTextField("source", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Jild = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Jarayon;

    private String Yorliq(String Kalit) {
        return messages.getProperty(Kalit, Kalit);
    }

    private void append(String Matn) {
        SwingUtilities.invokeLater(() -> {
            output.append(Matn);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void Xato(Exception exception) {
        append(Yorliq("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String Kalit, Runnable Amal) {
        JButton button = new JButton(Yorliq(Kalit));
        button.addActionListener(event -> Amal.run());
        panel.add(button);
    }

    private void Yuklash() {
        try {
            source.setText(Files.readString(Jild.resolve(path.getText()), StandardCharsets.UTF_8));
            source.setCaretPosition(0);
        } catch (Exception exception) { Xato(exception); }
    }

    private boolean Saqlash() {
        try {
            Path Fayl = Jild.resolve(path.getText()).normalize();
            Files.createDirectories(Fayl.getParent());
            Files.writeString(Fayl, source.getText(), StandardCharsets.UTF_8);
            append(Yorliq("save") + ": " + Fayl + "\n");
            return true;
        } catch (Exception exception) { Xato(exception); return false; }
    }

    private int Ishga_tushirish(List<String> Buyruq) throws Exception {
        Jarayon = new ProcessBuilder(Buyruq).directory(Jild.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Jarayon.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = Jarayon.waitFor();
        Jarayon = null;
        append(Yorliq("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Bajarish) {
        if (!Saqlash()) return;
        String Fayl = Jild.resolve(path.getText()).toString();
        String Sinf = Nomi.getText().trim();
        String Matn = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Jild.resolve("classes"));
                int result = Ishga_tushirish(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Jild.resolve("classes").toString(), Fayl));
                if (Bajarish && result == 0) {
                    List<String> Buyruq = new ArrayList<>(Arrays.asList("java", "-cp", Jild.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Sinf));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Matn));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Buyruq.add(parser.sval);
                    Ishga_tushirish(Buyruq);
                }
            } catch (Exception exception) { Xato(exception); }
        });
    }

    private void Toʻxtatish() {
        Process current = Jarayon;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Jild.toFile()).start(); }
        catch (Exception exception) { Xato(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Jild.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            path.setText(chooser.getSelectedFile().getAbsolutePath());
            Yuklash();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Jild);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Yorliq("workspace") + " · WorldOS " + Yorliq("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Toʻxtatish(); worker.shutdownNow(); System.exit(0);
            }
        });
        source.setFont(new Font("Monospaced", Font.PLAIN, 17));
        source.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Fayl = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fayl.add(new JLabel(Yorliq("file"))); Fayl.add(path);
        panel.add(Fayl);
        JPanel Asboblar_paneli = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Asboblar_paneli, "open", () -> choose());
        button(Asboblar_paneli, "save", () -> Saqlash());
        button(Asboblar_paneli, "compile", () -> compile(false));
        button(Asboblar_paneli, "run", () -> compile(true));
        button(Asboblar_paneli, "stop", () -> Toʻxtatish());
        button(Asboblar_paneli, "terminal", () -> terminal());
        panel.add(Asboblar_paneli);
        JPanel Moslamalar = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Moslamalar.add(new JLabel(Yorliq("class"))); Moslamalar.add(Nomi);
        Moslamalar.add(new JLabel(Yorliq("arguments"))); Moslamalar.add(arguments);
        panel.add(Moslamalar);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(source), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Yorliq("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        source.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Hajmi = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Hajmi.width - 40), Math.min(760, Hajmi.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Yuklash();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Yorliq("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
