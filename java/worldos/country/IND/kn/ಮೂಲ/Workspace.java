// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_kn;
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
    private final JTextArea ಮೂಲ = new JTextArea();
    private final JTextArea ಔಟ್_ಪುಟ್ = new JTextArea();
    private final JTextField ಮಾರ್ಗ = new JTextField("ಮೂಲ.java", 26);
    private final JTextField ಹೆಸರು = new JTextField("ಮೂಲ", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path ಕೋಶ = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process ಪ್ರಕ್ರಿಯೆ;

    private String ಲೇಬಲ್(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String ಪಠ್ಯ) {
        SwingUtilities.invokeLater(() -> {
            ಔಟ್_ಪುಟ್.append(ಪಠ್ಯ);
            ಔಟ್_ಪುಟ್.setCaretPosition(ಔಟ್_ಪುಟ್.getDocument().getLength());
        });
    }

    private void ದೋಷ(Exception exception) {
        append(ಲೇಬಲ್("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel ಫಲಕ, String key, Runnable ಹಕ್ರಿಯೆ) {
        JButton button = new JButton(ಲೇಬಲ್(key));
        button.addActionListener(event -> ಹಕ್ರಿಯೆ.run());
        ಫಲಕ.add(button);
    }

    private void ಲೋಡ್() {
        try {
            ಮೂಲ.setText(Files.readString(ಕೋಶ.resolve(ಮಾರ್ಗ.getText()), StandardCharsets.UTF_8));
            ಮೂಲ.setCaretPosition(0);
        } catch (Exception exception) { ದೋಷ(exception); }
    }

    private boolean ಉಳಿಸು() {
        try {
            Path ಕಡತ = ಕೋಶ.resolve(ಮಾರ್ಗ.getText()).normalize();
            Files.createDirectories(ಕಡತ.getParent());
            Files.writeString(ಕಡತ, ಮೂಲ.getText(), StandardCharsets.UTF_8);
            append(ಲೇಬಲ್("save") + ": " + ಕಡತ + "\n");
            return true;
        } catch (Exception exception) { ದೋಷ(exception); return false; }
    }

    private int ಚಲಾಯಿಸು(List<String> ಆಜ್ಞೆ) throws Exception {
        ಪ್ರಕ್ರಿಯೆ = new ProcessBuilder(ಆಜ್ಞೆ).directory(ಕೋಶ.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(ಪ್ರಕ್ರಿಯೆ.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = ಪ್ರಕ್ರಿಯೆ.waitFor();
        ಪ್ರಕ್ರಿಯೆ = null;
        append(ಲೇಬಲ್("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean ಚಲಾಯಿಸು_2) {
        if (!ಉಳಿಸು()) return;
        String ಕಡತ = ಕೋಶ.resolve(ಮಾರ್ಗ.getText()).toString();
        String className = ಹೆಸರು.getText().trim();
        String ಪಠ್ಯ = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(ಕೋಶ.resolve("classes"));
                int result = ಚಲಾಯಿಸು(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", ಕೋಶ.resolve("classes").toString(), ಕಡತ));
                if (ಚಲಾಯಿಸು_2 && result == 0) {
                    List<String> ಆಜ್ಞೆ = new ArrayList<>(Arrays.asList("java", "-cp", ಕೋಶ.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(ಪಠ್ಯ));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) ಆಜ್ಞೆ.add(parser.sval);
                    ಚಲಾಯಿಸು(ಆಜ್ಞೆ);
                }
            } catch (Exception exception) { ದೋಷ(exception); }
        });
    }

    private void ನಿಲ್ಲು() {
        Process current = ಪ್ರಕ್ರಿಯೆ;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void ಟರ್ಮಿನಲ್() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(ಕೋಶ.toFile()).start(); }
        catch (Exception exception) { ದೋಷ(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(ಕೋಶ.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            ಮಾರ್ಗ.setText(chooser.getSelectedFile().getAbsolutePath());
            ಲೋಡ್();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(ಕೋಶ);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(ಲೇಬಲ್("workspace") + " · WorldOS " + ಲೇಬಲ್("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                ನಿಲ್ಲು(); worker.shutdownNow(); System.exit(0);
            }
        });
        ಮೂಲ.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ಮೂಲ.setTabSize(4);
        ಔಟ್_ಪುಟ್.setFont(new Font("Monospaced", Font.PLAIN, 14));
        ಔಟ್_ಪುಟ್.setEditable(false);
        JPanel ಫಲಕ = new JPanel(new GridLayout(0, 1));
        JPanel ಕಡತ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ಕಡತ.add(new JLabel(ಲೇಬಲ್("file"))); ಕಡತ.add(ಮಾರ್ಗ);
        ಫಲಕ.add(ಕಡತ);
        JPanel ಉಪಕರಣಪಟ್ಟಿ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(ಉಪಕರಣಪಟ್ಟಿ, "open", () -> choose());
        button(ಉಪಕರಣಪಟ್ಟಿ, "save", () -> ಉಳಿಸು());
        button(ಉಪಕರಣಪಟ್ಟಿ, "compile", () -> compile(false));
        button(ಉಪಕರಣಪಟ್ಟಿ, "run", () -> compile(true));
        button(ಉಪಕರಣಪಟ್ಟಿ, "stop", () -> ನಿಲ್ಲು());
        button(ಉಪಕರಣಪಟ್ಟಿ, "terminal", () -> ಟರ್ಮಿನಲ್());
        ಫಲಕ.add(ಉಪಕರಣಪಟ್ಟಿ);
        JPanel ಸಿದ್ಧತೆಗಳು = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ಸಿದ್ಧತೆಗಳು.add(new JLabel(ಲೇಬಲ್("class"))); ಸಿದ್ಧತೆಗಳು.add(ಹೆಸರು);
        ಸಿದ್ಧತೆಗಳು.add(new JLabel(ಲೇಬಲ್("arguments"))); ಸಿದ್ಧತೆಗಳು.add(arguments);
        ಫಲಕ.add(ಸಿದ್ಧತೆಗಳು);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ಮೂಲ), new JScrollPane(ಔಟ್_ಪುಟ್));
        split.setResizeWeight(0.72);
        window.add(ಫಲಕ, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        ಫಲಕ.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(ಲೇಬಲ್("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ಮೂಲ.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        ಔಟ್_ಪುಟ್.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension ಗಾತ್ರ = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, ಗಾತ್ರ.width - 40), Math.min(760, ಗಾತ್ರ.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        ಲೋಡ್();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(ಲೇಬಲ್("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
