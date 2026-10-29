// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_ne;
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
    private final JTextArea स्रोत = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField मार्ग = new JTextField("स्रोत.java", 26);
    private final JTextField नाम = new JTextField("स्रोत", 15);
    private final JTextField तर्क = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path डाइरेक्टरी = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String लेबुल(String साँचो) {
        return messages.getProperty(साँचो, साँचो);
    }

    private void append(String पाठ) {
        SwingUtilities.invokeLater(() -> {
            output.append(पाठ);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void त्रुटि(Exception exception) {
        append(लेबुल("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel प्यानल, String साँचो, Runnable कार्य) {
        JButton button = new JButton(लेबुल(साँचो));
        button.addActionListener(event -> कार्य.run());
        प्यानल.add(button);
    }

    private void लोड_गर्नुहोस्() {
        try {
            स्रोत.setText(Files.readString(डाइरेक्टरी.resolve(मार्ग.getText()), StandardCharsets.UTF_8));
            स्रोत.setCaretPosition(0);
        } catch (Exception exception) { त्रुटि(exception); }
    }

    private boolean बचत_गर्नुहोस्() {
        try {
            Path फाइल = डाइरेक्टरी.resolve(मार्ग.getText()).normalize();
            Files.createDirectories(फाइल.getParent());
            Files.writeString(फाइल, स्रोत.getText(), StandardCharsets.UTF_8);
            append(लेबुल("save") + ": " + फाइल + "\n");
            return true;
        } catch (Exception exception) { त्रुटि(exception); return false; }
    }

    private int कार्यान्वयन_गर्नुहोस्(List<String> आदेश) throws Exception {
        process = new ProcessBuilder(आदेश).directory(डाइरेक्टरी.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(लेबुल("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean चलाउनुहोस्) {
        if (!बचत_गर्नुहोस्()) return;
        String फाइल = डाइरेक्टरी.resolve(मार्ग.getText()).toString();
        String वर्ग = नाम.getText().trim();
        String पाठ = तर्क.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(डाइरेक्टरी.resolve("classes"));
                int result = कार्यान्वयन_गर्नुहोस्(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", डाइरेक्टरी.resolve("classes").toString(), फाइल));
                if (चलाउनुहोस् && result == 0) {
                    List<String> आदेश = new ArrayList<>(Arrays.asList("java", "-cp", डाइरेक्टरी.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", वर्ग));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(पाठ));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) आदेश.add(parser.sval);
                    कार्यान्वयन_गर्नुहोस्(आदेश);
                }
            } catch (Exception exception) { त्रुटि(exception); }
        });
    }

    private void रोक्नुहोस्() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void टर्मिनल() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(डाइरेक्टरी.toFile()).start(); }
        catch (Exception exception) { त्रुटि(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(डाइरेक्टरी.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            मार्ग.setText(chooser.getSelectedFile().getAbsolutePath());
            लोड_गर्नुहोस्();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(डाइरेक्टरी);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(लेबुल("workspace") + " · WorldOS " + लेबुल("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                रोक्नुहोस्(); worker.shutdownNow(); System.exit(0);
            }
        });
        स्रोत.setFont(new Font("Monospaced", Font.PLAIN, 17));
        स्रोत.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel प्यानल = new JPanel(new GridLayout(0, 1));
        JPanel फाइल = new JPanel(new FlowLayout(FlowLayout.LEADING));
        फाइल.add(new JLabel(लेबुल("file"))); फाइल.add(मार्ग);
        प्यानल.add(फाइल);
        JPanel उपकरणपट्टी = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(उपकरणपट्टी, "open", () -> choose());
        button(उपकरणपट्टी, "save", () -> बचत_गर्नुहोस्());
        button(उपकरणपट्टी, "compile", () -> compile(false));
        button(उपकरणपट्टी, "run", () -> compile(true));
        button(उपकरणपट्टी, "stop", () -> रोक्नुहोस्());
        button(उपकरणपट्टी, "terminal", () -> टर्मिनल());
        प्यानल.add(उपकरणपट्टी);
        JPanel सेटिङ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        सेटिङ.add(new JLabel(लेबुल("class"))); सेटिङ.add(नाम);
        सेटिङ.add(new JLabel(लेबुल("arguments"))); सेटिङ.add(तर्क);
        प्यानल.add(सेटिङ);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(स्रोत), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(प्यानल, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        प्यानल.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(लेबुल("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        स्रोत.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension आकार = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, आकार.width - 40), Math.min(760, आकार.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        लोड_गर्नुहोस्();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(लेबुल("help") + "\n");
    }

    public static void main(String[] तर्क) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
