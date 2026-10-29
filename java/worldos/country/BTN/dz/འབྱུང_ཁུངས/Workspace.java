// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.BTN.l_dz;
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
    private final JTextArea འབྱུང_ཁུངས = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField འགྲུལ_ལམ = new JTextField("འབྱུང_ཁུངས.java", 26);
    private final JTextField མིང = new JTextField("འབྱུང_ཁུངས", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path སྣོད_ཐོ = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process ལས_སྦྱོར;

    private String ཁ_ཡིག(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String བརྟག_ཞིབ) {
        SwingUtilities.invokeLater(() -> {
            output.append(བརྟག_ཞིབ);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void འཛོལ_བ(Exception exception) {
        append(ཁ_ཡིག("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel པེ_ནཱལ, String key, Runnable བྱ_བ) {
        JButton button = new JButton(ཁ_ཡིག(key));
        button.addActionListener(event -> བྱ_བ.run());
        པེ_ནཱལ.add(button);
    }

    private void ལྗིད_ཚད() {
        try {
            འབྱུང_ཁུངས.setText(Files.readString(སྣོད_ཐོ.resolve(འགྲུལ_ལམ.getText()), StandardCharsets.UTF_8));
            འབྱུང_ཁུངས.setCaretPosition(0);
        } catch (Exception exception) { འཛོལ_བ(exception); }
    }

    private boolean སྲུངས() {
        try {
            Path ཡིག_སྣོད = སྣོད_ཐོ.resolve(འགྲུལ_ལམ.getText()).normalize();
            Files.createDirectories(ཡིག_སྣོད.getParent());
            Files.writeString(ཡིག_སྣོད, འབྱུང_ཁུངས.getText(), StandardCharsets.UTF_8);
            append(ཁ_ཡིག("save") + ": " + ཡིག_སྣོད + "\n");
            return true;
        } catch (Exception exception) { འཛོལ_བ(exception); return false; }
    }

    private int execute(List<String> བརྡ_བཀོད) throws Exception {
        ལས_སྦྱོར = new ProcessBuilder(བརྡ_བཀོད).directory(སྣོད_ཐོ.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(ལས_སྦྱོར.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = ལས_སྦྱོར.waitFor();
        ལས_སྦྱོར = null;
        append(ཁ_ཡིག("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean གཡོག_བཀོལ) {
        if (!སྲུངས()) return;
        String ཡིག_སྣོད = སྣོད_ཐོ.resolve(འགྲུལ_ལམ.getText()).toString();
        String དབྱེ_རིགས = མིང.getText().trim();
        String བརྟག_ཞིབ = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(སྣོད_ཐོ.resolve("classes"));
                int result = execute(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", སྣོད_ཐོ.resolve("classes").toString(), ཡིག_སྣོད));
                if (གཡོག_བཀོལ && result == 0) {
                    List<String> བརྡ_བཀོད = new ArrayList<>(Arrays.asList("java", "-cp", སྣོད_ཐོ.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", དབྱེ_རིགས));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(བརྟག_ཞིབ));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) བརྡ_བཀོད.add(parser.sval);
                    execute(བརྡ_བཀོད);
                }
            } catch (Exception exception) { འཛོལ_བ(exception); }
        });
    }

    private void བཀག() {
        Process current = ལས_སྦྱོར;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void ཊར_མི_ནཱལ() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(སྣོད_ཐོ.toFile()).start(); }
        catch (Exception exception) { འཛོལ_བ(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(སྣོད_ཐོ.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            འགྲུལ_ལམ.setText(chooser.getSelectedFile().getAbsolutePath());
            ལྗིད_ཚད();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(སྣོད_ཐོ);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(ཁ_ཡིག("workspace") + " · WorldOS " + ཁ_ཡིག("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                བཀག(); worker.shutdownNow(); System.exit(0);
            }
        });
        འབྱུང_ཁུངས.setFont(new Font("Monospaced", Font.PLAIN, 17));
        འབྱུང_ཁུངས.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel པེ_ནཱལ = new JPanel(new GridLayout(0, 1));
        JPanel ཡིག_སྣོད = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ཡིག_སྣོད.add(new JLabel(ཁ_ཡིག("file"))); ཡིག_སྣོད.add(འགྲུལ_ལམ);
        པེ_ནཱལ.add(ཡིག_སྣོད);
        JPanel ལག_ཆས_ཕྲ_རིང = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(ལག_ཆས_ཕྲ_རིང, "open", () -> choose());
        button(ལག_ཆས_ཕྲ_རིང, "save", () -> སྲུངས());
        button(ལག_ཆས_ཕྲ_རིང, "compile", () -> compile(false));
        button(ལག_ཆས_ཕྲ_རིང, "run", () -> compile(true));
        button(ལག_ཆས_ཕྲ_རིང, "stop", () -> བཀག());
        button(ལག_ཆས_ཕྲ_རིང, "terminal", () -> ཊར_མི_ནཱལ());
        པེ_ནཱལ.add(ལག_ཆས_ཕྲ_རིང);
        JPanel གཞི_སྒྲིག_ཚུ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        གཞི_སྒྲིག_ཚུ.add(new JLabel(ཁ_ཡིག("class"))); གཞི_སྒྲིག_ཚུ.add(མིང);
        གཞི_སྒྲིག_ཚུ.add(new JLabel(ཁ_ཡིག("arguments"))); གཞི_སྒྲིག_ཚུ.add(arguments);
        པེ_ནཱལ.add(གཞི_སྒྲིག_ཚུ);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(འབྱུང_ཁུངས), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(པེ_ནཱལ, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        པེ_ནཱལ.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(ཁ_ཡིག("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        འབྱུང_ཁུངས.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension ཚད = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, ཚད.width - 40), Math.min(760, ཚད.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        ལྗིད_ཚད();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(ཁ_ཡིག("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
