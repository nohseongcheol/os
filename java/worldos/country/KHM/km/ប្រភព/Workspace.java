// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.KHM.l_km;
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
    private final JTextArea ប្រភព = new JTextArea();
    private final JTextArea លទ្ធផល = new JTextArea();
    private final JTextField path = new JTextField("ប្រភព.java", 26);
    private final JTextField ឈ្មោះ = new JTextField("ប្រភព", 15);
    private final JTextField អាគុយម៉ង់ = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path ថត = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String label(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String អត្ថបទ) {
        SwingUtilities.invokeLater(() -> {
            លទ្ធផល.append(អត្ថបទ);
            លទ្ធផល.setCaretPosition(លទ្ធផល.getDocument().getLength());
        });
    }

    private void កំហុស(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel បន្ទះ, String key, Runnable អំពើ) {
        JButton button = new JButton(label(key));
        button.addActionListener(event -> អំពើ.run());
        បន្ទះ.add(button);
    }

    private void load() {
        try {
            ប្រភព.setText(Files.readString(ថត.resolve(path.getText()), StandardCharsets.UTF_8));
            ប្រភព.setCaretPosition(0);
        } catch (Exception exception) { កំហុស(exception); }
    }

    private boolean save() {
        try {
            Path ឯកសារ = ថត.resolve(path.getText()).normalize();
            Files.createDirectories(ឯកសារ.getParent());
            Files.writeString(ឯកសារ, ប្រភព.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + ឯកសារ + "\n");
            return true;
        } catch (Exception exception) { កំហុស(exception); return false; }
    }

    private int ប្រតិបត្តិ(List<String> ពាក្យ_បញ្ជា) throws Exception {
        process = new ProcessBuilder(ពាក្យ_បញ្ជា).directory(ថត.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String បន្ទាត់;
            while ((បន្ទាត់ = reader.readLine()) != null) append(បន្ទាត់ + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(label("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean រត់) {
        if (!save()) return;
        String ឯកសារ = ថត.resolve(path.getText()).toString();
        String ថ្នាក់ = ឈ្មោះ.getText().trim();
        String អត្ថបទ = អាគុយម៉ង់.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(ថត.resolve("classes"));
                int result = ប្រតិបត្តិ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", ថត.resolve("classes").toString(), ឯកសារ));
                if (រត់ && result == 0) {
                    List<String> ពាក្យ_បញ្ជា = new ArrayList<>(Arrays.asList("java", "-cp", ថត.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", ថ្នាក់));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(អត្ថបទ));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) ពាក្យ_បញ្ជា.add(parser.sval);
                    ប្រតិបត្តិ(ពាក្យ_បញ្ជា);
                }
            } catch (Exception exception) { កំហុស(exception); }
        });
    }

    private void បញ្ឈប់() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void ស្ថានីយ() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(ថត.toFile()).start(); }
        catch (Exception exception) { កំហុស(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(ថត.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            path.setText(chooser.getSelectedFile().getAbsolutePath());
            load();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(ថត);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(label("workspace") + " · WorldOS " + label("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                បញ្ឈប់(); worker.shutdownNow(); System.exit(0);
            }
        });
        ប្រភព.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ប្រភព.setTabSize(4);
        លទ្ធផល.setFont(new Font("Monospaced", Font.PLAIN, 14));
        លទ្ធផល.setEditable(false);
        JPanel បន្ទះ = new JPanel(new GridLayout(0, 1));
        JPanel ឯកសារ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ឯកសារ.add(new JLabel(label("file"))); ឯកសារ.add(path);
        បន្ទះ.add(ឯកសារ);
        JPanel របារ_ឧបករណ៍ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(របារ_ឧបករណ៍, "open", () -> choose());
        button(របារ_ឧបករណ៍, "save", () -> save());
        button(របារ_ឧបករណ៍, "compile", () -> compile(false));
        button(របារ_ឧបករណ៍, "run", () -> compile(true));
        button(របារ_ឧបករណ៍, "stop", () -> បញ្ឈប់());
        button(របារ_ឧបករណ៍, "terminal", () -> ស្ថានីយ());
        បន្ទះ.add(របារ_ឧបករណ៍);
        JPanel settings = new JPanel(new FlowLayout(FlowLayout.LEADING));
        settings.add(new JLabel(label("class"))); settings.add(ឈ្មោះ);
        settings.add(new JLabel(label("arguments"))); settings.add(អាគុយម៉ង់);
        បន្ទះ.add(settings);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ប្រភព), new JScrollPane(លទ្ធផល));
        split.setResizeWeight(0.72);
        window.add(បន្ទះ, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        បន្ទះ.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(label("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ប្រភព.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        លទ្ធផល.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension size = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, size.width - 40), Math.min(760, size.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        load();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(label("help") + "\n");
    }

    public static void main(String[] អាគុយម៉ង់) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
