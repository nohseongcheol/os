// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IRN.l_ps;
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
    private final JTextArea سرچينه = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField يونلور = new JTextField("سرچينه.java", 26);
    private final JTextField نوم = new JTextField("سرچينه", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path درکموند = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process بهير;

    private String نښکه(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String ليکنه) {
        SwingUtilities.invokeLater(() -> {
            output.append(ليکنه);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void تېروتنه(Exception exception) {
        append(نښکه("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel چوکاټ, String key, Runnable چار) {
        JButton button = new JButton(نښکه(key));
        button.addActionListener(event -> چار.run());
        چوکاټ.add(button);
    }

    private void لېښل() {
        try {
            سرچينه.setText(Files.readString(درکموند.resolve(يونلور.getText()), StandardCharsets.UTF_8));
            سرچينه.setCaretPosition(0);
        } catch (Exception exception) { تېروتنه(exception); }
    }

    private boolean ساتل() {
        try {
            Path دوتنه = درکموند.resolve(يونلور.getText()).normalize();
            Files.createDirectories(دوتنه.getParent());
            Files.writeString(دوتنه, سرچينه.getText(), StandardCharsets.UTF_8);
            append(نښکه("save") + ": " + دوتنه + "\n");
            return true;
        } catch (Exception exception) { تېروتنه(exception); return false; }
    }

    private int چلول(List<String> بولۍ) throws Exception {
        بهير = new ProcessBuilder(بولۍ).directory(درکموند.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(بهير.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = بهير.waitFor();
        بهير = null;
        append(نښکه("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean ځغلول) {
        if (!ساتل()) return;
        String دوتنه = درکموند.resolve(يونلور.getText()).toString();
        String className = نوم.getText().trim();
        String ليکنه = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(درکموند.resolve("classes"));
                int result = چلول(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", درکموند.resolve("classes").toString(), دوتنه));
                if (ځغلول && result == 0) {
                    List<String> بولۍ = new ArrayList<>(Arrays.asList("java", "-cp", درکموند.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(ليکنه));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) بولۍ.add(parser.sval);
                    چلول(بولۍ);
                }
            } catch (Exception exception) { تېروتنه(exception); }
        });
    }

    private void تمول() {
        Process current = بهير;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void پايالی() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(درکموند.toFile()).start(); }
        catch (Exception exception) { تېروتنه(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(درکموند.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            يونلور.setText(chooser.getSelectedFile().getAbsolutePath());
            لېښل();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(درکموند);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(نښکه("workspace") + " · WorldOS " + نښکه("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                تمول(); worker.shutdownNow(); System.exit(0);
            }
        });
        سرچينه.setFont(new Font("Monospaced", Font.PLAIN, 17));
        سرچينه.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel چوکاټ = new JPanel(new GridLayout(0, 1));
        JPanel دوتنه = new JPanel(new FlowLayout(FlowLayout.LEADING));
        دوتنه.add(new JLabel(نښکه("file"))); دوتنه.add(يونلور);
        چوکاټ.add(دوتنه);
        JPanel توکپټه = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(توکپټه, "open", () -> choose());
        button(توکپټه, "save", () -> ساتل());
        button(توکپټه, "compile", () -> compile(false));
        button(توکپټه, "run", () -> compile(true));
        button(توکپټه, "stop", () -> تمول());
        button(توکپټه, "terminal", () -> پايالی());
        چوکاټ.add(توکپټه);
        JPanel امستنې = new JPanel(new FlowLayout(FlowLayout.LEADING));
        امستنې.add(new JLabel(نښکه("class"))); امستنې.add(نوم);
        امستنې.add(new JLabel(نښکه("arguments"))); امستنې.add(arguments);
        چوکاټ.add(امستنې);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(سرچينه), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(چوکاټ, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        چوکاټ.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(نښکه("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        سرچينه.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension کچ = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, کچ.width - 40), Math.min(760, کچ.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        لېښل();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(نښکه("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
