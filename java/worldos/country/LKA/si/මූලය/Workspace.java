// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.LKA.l_si;
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
    private final JFrame කවුළුව = new JFrame();
    private final JTextArea මූලය = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField මාර්_ගය = new JTextField("මූලය.java", 26);
    private final JTextField නම = new JTextField("මූලය", 15);
    private final JTextField විස්තාරක = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path බහලුම = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process සැකසුම;

    private String ලේබලය(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String පෙළ) {
        SwingUtilities.invokeLater(() -> {
            output.append(පෙළ);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void දෝෂය(Exception exception) {
        append(ලේබලය("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel පුවරුව, String key, Runnable ක්_රීයාව) {
        JButton button = new JButton(ලේබලය(key));
        button.addActionListener(සිදුවීම -> ක්_රීයාව.run());
        පුවරුව.add(button);
    }

    private void පූරණය() {
        try {
            මූලය.setText(Files.readString(බහලුම.resolve(මාර්_ගය.getText()), StandardCharsets.UTF_8));
            මූලය.setCaretPosition(0);
        } catch (Exception exception) { දෝෂය(exception); }
    }

    private boolean සුරකීම() {
        try {
            Path ගොනු = බහලුම.resolve(මාර්_ගය.getText()).normalize();
            Files.createDirectories(ගොනු.getParent());
            Files.writeString(ගොනු, මූලය.getText(), StandardCharsets.UTF_8);
            append(ලේබලය("save") + ": " + ගොනු + "\n");
            return true;
        } catch (Exception exception) { දෝෂය(exception); return false; }
    }

    private int ක්_රියාත්මක_කරන්න(List<String> විධානය) throws Exception {
        සැකසුම = new ProcessBuilder(විධානය).directory(බහලුම.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(සැකසුම.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = සැකසුම.waitFor();
        සැකසුම = null;
        append(ලේබලය("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean ක්_රියාත්මක_කරන්න_2) {
        if (!සුරකීම()) return;
        String ගොනු = බහලුම.resolve(මාර්_ගය.getText()).toString();
        String පන්තිය = නම.getText().trim();
        String පෙළ = විස්තාරක.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(බහලුම.resolve("classes"));
                int result = ක්_රියාත්මක_කරන්න(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", බහලුම.resolve("classes").toString(), ගොනු));
                if (ක්_රියාත්මක_කරන්න_2 && result == 0) {
                    List<String> විධානය = new ArrayList<>(Arrays.asList("java", "-cp", බහලුම.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", පන්තිය));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(පෙළ));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) විධානය.add(parser.sval);
                    ක්_රියාත්මක_කරන්න(විධානය);
                }
            } catch (Exception exception) { දෝෂය(exception); }
        });
    }

    private void නවතන්න() {
        Process current = සැකසුම;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void අග්_රය() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(බහලුම.toFile()).start(); }
        catch (Exception exception) { දෝෂය(exception); }
    }

    private void තෝරන්න() {
        JFileChooser chooser = new JFileChooser(බහලුම.toFile());
        if (chooser.showOpenDialog(කවුළුව) == JFileChooser.APPROVE_OPTION) {
            මාර්_ගය.setText(chooser.getSelectedFile().getAbsolutePath());
            පූරණය();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(බහලුම);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        කවුළුව.setTitle(ලේබලය("workspace") + " · WorldOS " + ලේබලය("identity"));
        කවුළුව.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        කවුළුව.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent සිදුවීම) {
                නවතන්න(); worker.shutdownNow(); System.exit(0);
            }
        });
        මූලය.setFont(new Font("Monospaced", Font.PLAIN, 17));
        මූලය.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel පුවරුව = new JPanel(new GridLayout(0, 1));
        JPanel ගොනු = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ගොනු.add(new JLabel(ලේබලය("file"))); ගොනු.add(මාර්_ගය);
        පුවරුව.add(ගොනු);
        JPanel මෙවලම්_පුවරුව = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(මෙවලම්_පුවරුව, "open", () -> තෝරන්න());
        button(මෙවලම්_පුවරුව, "save", () -> සුරකීම());
        button(මෙවලම්_පුවරුව, "compile", () -> compile(false));
        button(මෙවලම්_පුවරුව, "run", () -> compile(true));
        button(මෙවලම්_පුවරුව, "stop", () -> නවතන්න());
        button(මෙවලම්_පුවරුව, "terminal", () -> අග්_රය());
        පුවරුව.add(මෙවලම්_පුවරුව);
        JPanel සැකසුම් = new JPanel(new FlowLayout(FlowLayout.LEADING));
        සැකසුම්.add(new JLabel(ලේබලය("class"))); සැකසුම්.add(නම);
        සැකසුම්.add(new JLabel(ලේබලය("arguments"))); සැකසුම්.add(විස්තාරක);
        පුවරුව.add(සැකසුම්);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(මූලය), new JScrollPane(output));
        split.setResizeWeight(0.72);
        කවුළුව.add(පුවරුව, BorderLayout.NORTH);
        කවුළුව.add(split, BorderLayout.CENTER);
        පුවරුව.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(ලේබලය("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        මූලය.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension ප්_රමාණය = Toolkit.getDefaultToolkit().getScreenSize();
        කවුළුව.setSize(Math.min(1240, ප්_රමාණය.width - 40), Math.min(760, ප්_රමාණය.height - 60));
        කවුළුව.setLocationRelativeTo(null);
        කවුළුව.setVisible(true);
        පූරණය();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(ලේබලය("help") + "\n");
    }

    public static void main(String[] විස්තාරක) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
