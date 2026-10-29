// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_mai;
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
    private final JTextArea श्रोोत = new JTextArea();
    private final JTextArea आउटपुट = new JTextArea();
    private final JTextField पथ = new JTextField("श्रोोत.java", 26);
    private final JTextField नाम = new JTextField("श्रोोत", 15);
    private final JTextField आर्गुमेंट्स = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path निर्देशिका = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process प्रक्रिया;

    private String लेबल(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String पाठ) {
        SwingUtilities.invokeLater(() -> {
            आउटपुट.append(पाठ);
            आउटपुट.setCaretPosition(आउटपुट.getDocument().getLength());
        });
    }

    private void त्रुटि(Exception exception) {
        append(लेबल("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel पटल, String key, Runnable क्रिया) {
        JButton button = new JButton(लेबल(key));
        button.addActionListener(event -> क्रिया.run());
        पटल.add(button);
    }

    private void लोड() {
        try {
            श्रोोत.setText(Files.readString(निर्देशिका.resolve(पथ.getText()), StandardCharsets.UTF_8));
            श्रोोत.setCaretPosition(0);
        } catch (Exception exception) { त्रुटि(exception); }
    }

    private boolean सहेजू() {
        try {
            Path फाइल = निर्देशिका.resolve(पथ.getText()).normalize();
            Files.createDirectories(फाइल.getParent());
            Files.writeString(फाइल, श्रोोत.getText(), StandardCharsets.UTF_8);
            append(लेबल("save") + ": " + फाइल + "\n");
            return true;
        } catch (Exception exception) { त्रुटि(exception); return false; }
    }

    private int चलाउ(List<String> कमांड) throws Exception {
        प्रक्रिया = new ProcessBuilder(कमांड).directory(निर्देशिका.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(प्रक्रिया.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = प्रक्रिया.waitFor();
        प्रक्रिया = null;
        append(लेबल("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean चलाबू) {
        if (!सहेजू()) return;
        String फाइल = निर्देशिका.resolve(पथ.getText()).toString();
        String वर्ग = नाम.getText().trim();
        String पाठ = आर्गुमेंट्स.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(निर्देशिका.resolve("classes"));
                int result = चलाउ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", निर्देशिका.resolve("classes").toString(), फाइल));
                if (चलाबू && result == 0) {
                    List<String> कमांड = new ArrayList<>(Arrays.asList("java", "-cp", निर्देशिका.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", वर्ग));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(पाठ));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) कमांड.add(parser.sval);
                    चलाउ(कमांड);
                }
            } catch (Exception exception) { त्रुटि(exception); }
        });
    }

    private void रोकू() {
        Process current = प्रक्रिया;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void टर्मिनल() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(निर्देशिका.toFile()).start(); }
        catch (Exception exception) { त्रुटि(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(निर्देशिका.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            पथ.setText(chooser.getSelectedFile().getAbsolutePath());
            लोड();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(निर्देशिका);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(लेबल("workspace") + " · WorldOS " + लेबल("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                रोकू(); worker.shutdownNow(); System.exit(0);
            }
        });
        श्रोोत.setFont(new Font("Monospaced", Font.PLAIN, 17));
        श्रोोत.setTabSize(4);
        आउटपुट.setFont(new Font("Monospaced", Font.PLAIN, 14));
        आउटपुट.setEditable(false);
        JPanel पटल = new JPanel(new GridLayout(0, 1));
        JPanel फाइल = new JPanel(new FlowLayout(FlowLayout.LEADING));
        फाइल.add(new JLabel(लेबल("file"))); फाइल.add(पथ);
        पटल.add(फाइल);
        JPanel अओजारपट्टी = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(अओजारपट्टी, "open", () -> choose());
        button(अओजारपट्टी, "save", () -> सहेजू());
        button(अओजारपट्टी, "compile", () -> compile(false));
        button(अओजारपट्टी, "run", () -> compile(true));
        button(अओजारपट्टी, "stop", () -> रोकू());
        button(अओजारपट्टी, "terminal", () -> टर्मिनल());
        पटल.add(अओजारपट्टी);
        JPanel जमावट = new JPanel(new FlowLayout(FlowLayout.LEADING));
        जमावट.add(new JLabel(लेबल("class"))); जमावट.add(नाम);
        जमावट.add(new JLabel(लेबल("arguments"))); जमावट.add(आर्गुमेंट्स);
        पटल.add(जमावट);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(श्रोोत), new JScrollPane(आउटपुट));
        split.setResizeWeight(0.72);
        window.add(पटल, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        पटल.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(लेबल("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        श्रोोत.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        आउटपुट.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension आकार = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, आकार.width - 40), Math.min(760, आकार.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        लोड();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(लेबल("help") + "\n");
    }

    public static void main(String[] आर्गुमेंट्स) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
