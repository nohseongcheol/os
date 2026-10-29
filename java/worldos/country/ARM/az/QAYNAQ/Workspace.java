// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ARM.l_az;
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
    private final JTextArea QAYNAQ = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField Cığır = new JTextField("QAYNAQ.java", 26);
    private final JTextField Ad = new JTextField("QAYNAQ", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Cərgə = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String Etiket(String Açar) {
        return messages.getProperty(Açar, Açar);
    }

    private void append(String Mətn) {
        SwingUtilities.invokeLater(() -> {
            output.append(Mətn);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void XƏTA(Exception exception) {
        append(Etiket("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String Açar, Runnable Gedişat) {
        JButton button = new JButton(Etiket(Açar));
        button.addActionListener(event -> Gedişat.run());
        panel.add(button);
    }

    private void Yük() {
        try {
            QAYNAQ.setText(Files.readString(Cərgə.resolve(Cığır.getText()), StandardCharsets.UTF_8));
            QAYNAQ.setCaretPosition(0);
        } catch (Exception exception) { XƏTA(exception); }
    }

    private boolean Qeyd_Et() {
        try {
            Path FAYL = Cərgə.resolve(Cığır.getText()).normalize();
            Files.createDirectories(FAYL.getParent());
            Files.writeString(FAYL, QAYNAQ.getText(), StandardCharsets.UTF_8);
            append(Etiket("save") + ": " + FAYL + "\n");
            return true;
        } catch (Exception exception) { XƏTA(exception); return false; }
    }

    private int execute(List<String> Əmr) throws Exception {
        process = new ProcessBuilder(Əmr).directory(Cərgə.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String Giriş;
            while ((Giriş = reader.readLine()) != null) append(Giriş + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(Etiket("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean İcra_Et) {
        if (!Qeyd_Et()) return;
        String FAYL = Cərgə.resolve(Cığır.getText()).toString();
        String Sinif = Ad.getText().trim();
        String Mətn = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Cərgə.resolve("classes"));
                int result = execute(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Cərgə.resolve("classes").toString(), FAYL));
                if (İcra_Et && result == 0) {
                    List<String> Əmr = new ArrayList<>(Arrays.asList("java", "-cp", Cərgə.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Sinif));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Mətn));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Əmr.add(parser.sval);
                    execute(Əmr);
                }
            } catch (Exception exception) { XƏTA(exception); }
        });
    }

    private void Dayan() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Cərgə.toFile()).start(); }
        catch (Exception exception) { XƏTA(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Cərgə.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            Cığır.setText(chooser.getSelectedFile().getAbsolutePath());
            Yük();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Cərgə);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Etiket("workspace") + " · WorldOS " + Etiket("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Dayan(); worker.shutdownNow(); System.exit(0);
            }
        });
        QAYNAQ.setFont(new Font("Monospaced", Font.PLAIN, 17));
        QAYNAQ.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel FAYL = new JPanel(new FlowLayout(FlowLayout.LEADING));
        FAYL.add(new JLabel(Etiket("file"))); FAYL.add(Cığır);
        panel.add(FAYL);
        JPanel Vasitə_Çubuğu = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Vasitə_Çubuğu, "open", () -> choose());
        button(Vasitə_Çubuğu, "save", () -> Qeyd_Et());
        button(Vasitə_Çubuğu, "compile", () -> compile(false));
        button(Vasitə_Çubuğu, "run", () -> compile(true));
        button(Vasitə_Çubuğu, "stop", () -> Dayan());
        button(Vasitə_Çubuğu, "terminal", () -> terminal());
        panel.add(Vasitə_Çubuğu);
        JPanel Sazlama = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Sazlama.add(new JLabel(Etiket("class"))); Sazlama.add(Ad);
        Sazlama.add(new JLabel(Etiket("arguments"))); Sazlama.add(arguments);
        panel.add(Sazlama);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(QAYNAQ), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etiket("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        QAYNAQ.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Böyüklük = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Böyüklük.width - 40), Math.min(760, Böyüklük.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Yük();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Etiket("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
