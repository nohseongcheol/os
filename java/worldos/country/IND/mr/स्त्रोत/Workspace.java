// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_mr;
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
    private final JTextArea स्त्रोत = new JTextArea();
    private final JTextArea आउटपुट = new JTextArea();
    private final JTextField मार्ग = new JTextField("स्त्रोत.java", 26);
    private final JTextField नाव = new JTextField("स्त्रोत", 15);
    private final JTextField बाबी = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path संचयीका = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process प्रक्रिया;

    private String लेबल(String किल्ली) {
        return messages.getProperty(किल्ली, किल्ली);
    }

    private void append(String पाठ्य) {
        SwingUtilities.invokeLater(() -> {
            आउटपुट.append(पाठ्य);
            आउटपुट.setCaretPosition(आउटपुट.getDocument().getLength());
        });
    }

    private void त्रुटी(Exception exception) {
        append(लेबल("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel पटल, String किल्ली, Runnable कृती) {
        JButton button = new JButton(लेबल(किल्ली));
        button.addActionListener(event -> कृती.run());
        पटल.add(button);
    }

    private void भार() {
        try {
            स्त्रोत.setText(Files.readString(संचयीका.resolve(मार्ग.getText()), StandardCharsets.UTF_8));
            स्त्रोत.setCaretPosition(0);
        } catch (Exception exception) { त्रुटी(exception); }
    }

    private boolean संचयीता_करा() {
        try {
            Path फाइल = संचयीका.resolve(मार्ग.getText()).normalize();
            Files.createDirectories(फाइल.getParent());
            Files.writeString(फाइल, स्त्रोत.getText(), StandardCharsets.UTF_8);
            append(लेबल("save") + ": " + फाइल + "\n");
            return true;
        } catch (Exception exception) { त्रुटी(exception); return false; }
    }

    private int कार्यान्वित_करा(List<String> आदेश) throws Exception {
        प्रक्रिया = new ProcessBuilder(आदेश).directory(संचयीका.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(प्रक्रिया.getInputStream(), StandardCharsets.UTF_8))) {
            String ओळ;
            while ((ओळ = reader.readLine()) != null) append(ओळ + "\n");
        }
        int result = प्रक्रिया.waitFor();
        प्रक्रिया = null;
        append(लेबल("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean सुरू_करा) {
        if (!संचयीता_करा()) return;
        String फाइल = संचयीका.resolve(मार्ग.getText()).toString();
        String वर्ग = नाव.getText().trim();
        String पाठ्य = बाबी.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(संचयीका.resolve("classes"));
                int result = कार्यान्वित_करा(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", संचयीका.resolve("classes").toString(), फाइल));
                if (सुरू_करा && result == 0) {
                    List<String> आदेश = new ArrayList<>(Arrays.asList("java", "-cp", संचयीका.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", वर्ग));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(पाठ्य));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) आदेश.add(parser.sval);
                    कार्यान्वित_करा(आदेश);
                }
            } catch (Exception exception) { त्रुटी(exception); }
        });
    }

    private void थांबा() {
        Process current = प्रक्रिया;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void टर्मिनल() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(संचयीका.toFile()).start(); }
        catch (Exception exception) { त्रुटी(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(संचयीका.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            मार्ग.setText(chooser.getSelectedFile().getAbsolutePath());
            भार();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(संचयीका);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(लेबल("workspace") + " · WorldOS " + लेबल("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                थांबा(); worker.shutdownNow(); System.exit(0);
            }
        });
        स्त्रोत.setFont(new Font("Monospaced", Font.PLAIN, 17));
        स्त्रोत.setTabSize(4);
        आउटपुट.setFont(new Font("Monospaced", Font.PLAIN, 14));
        आउटपुट.setEditable(false);
        JPanel पटल = new JPanel(new GridLayout(0, 1));
        JPanel फाइल = new JPanel(new FlowLayout(FlowLayout.LEADING));
        फाइल.add(new JLabel(लेबल("file"))); फाइल.add(मार्ग);
        पटल.add(फाइल);
        JPanel साधनपट्टी = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(साधनपट्टी, "open", () -> choose());
        button(साधनपट्टी, "save", () -> संचयीता_करा());
        button(साधनपट्टी, "compile", () -> compile(false));
        button(साधनपट्टी, "run", () -> compile(true));
        button(साधनपट्टी, "stop", () -> थांबा());
        button(साधनपट्टी, "terminal", () -> टर्मिनल());
        पटल.add(साधनपट्टी);
        JPanel संयोजना = new JPanel(new FlowLayout(FlowLayout.LEADING));
        संयोजना.add(new JLabel(लेबल("class"))); संयोजना.add(नाव);
        संयोजना.add(new JLabel(लेबल("arguments"))); संयोजना.add(बाबी);
        पटल.add(संयोजना);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(स्त्रोत), new JScrollPane(आउटपुट));
        split.setResizeWeight(0.72);
        window.add(पटल, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        पटल.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(लेबल("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        स्त्रोत.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        आउटपुट.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension आकार = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, आकार.width - 40), Math.min(760, आकार.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        भार();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(लेबल("help") + "\n");
    }

    public static void main(String[] बाबी) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
