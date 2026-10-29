// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_or;
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
    private final JTextArea ଉତ୍ସ = new JTextArea();
    private final JTextArea ନିର୍ଗମ = new JTextArea();
    private final JTextField ପଥ = new JTextField("ଉତ୍ସ.java", 26);
    private final JTextField ନାମ = new JTextField("ଉତ୍ସ", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path ଡିରେକ୍ଟୋରି = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process ପ୍ରକ୍ରିୟା;

    private String ସୂଚକ(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String ପାଠ୍ଯ) {
        SwingUtilities.invokeLater(() -> {
            ନିର୍ଗମ.append(ପାଠ୍ଯ);
            ନିର୍ଗମ.setCaretPosition(ନିର୍ଗମ.getDocument().getLength());
        });
    }

    private void ତ୍ରୁଟି(Exception exception) {
        append(ସୂଚକ("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel ପଟ୍ଟିକା, String key, Runnable କାମ) {
        JButton button = new JButton(ସୂଚକ(key));
        button.addActionListener(event -> କାମ.run());
        ପଟ୍ଟିକା.add(button);
    }

    private void ଲୋଡ_କର() {
        try {
            ଉତ୍ସ.setText(Files.readString(ଡିରେକ୍ଟୋରି.resolve(ପଥ.getText()), StandardCharsets.UTF_8));
            ଉତ୍ସ.setCaretPosition(0);
        } catch (Exception exception) { ତ୍ରୁଟି(exception); }
    }

    private boolean ସଂରକ୍ଷଣ_କରନ୍ତୁ() {
        try {
            Path ଫାଇଲ = ଡିରେକ୍ଟୋରି.resolve(ପଥ.getText()).normalize();
            Files.createDirectories(ଫାଇଲ.getParent());
            Files.writeString(ଫାଇଲ, ଉତ୍ସ.getText(), StandardCharsets.UTF_8);
            append(ସୂଚକ("save") + ": " + ଫାଇଲ + "\n");
            return true;
        } catch (Exception exception) { ତ୍ରୁଟି(exception); return false; }
    }

    private int ନିଷ୍ପାଦନ_କରନ୍ତୁ(List<String> ନିର୍ଦ୍ଦେଶ) throws Exception {
        ପ୍ରକ୍ରିୟା = new ProcessBuilder(ନିର୍ଦ୍ଦେଶ).directory(ଡିରେକ୍ଟୋରି.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(ପ୍ରକ୍ରିୟା.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = ପ୍ରକ୍ରିୟା.waitFor();
        ପ୍ରକ୍ରିୟା = null;
        append(ସୂଚକ("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean ଚଳାନ୍ତୁ) {
        if (!ସଂରକ୍ଷଣ_କରନ୍ତୁ()) return;
        String ଫାଇଲ = ଡିରେକ୍ଟୋରି.resolve(ପଥ.getText()).toString();
        String className = ନାମ.getText().trim();
        String ପାଠ୍ଯ = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(ଡିରେକ୍ଟୋରି.resolve("classes"));
                int result = ନିଷ୍ପାଦନ_କରନ୍ତୁ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", ଡିରେକ୍ଟୋରି.resolve("classes").toString(), ଫାଇଲ));
                if (ଚଳାନ୍ତୁ && result == 0) {
                    List<String> ନିର୍ଦ୍ଦେଶ = new ArrayList<>(Arrays.asList("java", "-cp", ଡିରେକ୍ଟୋରି.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(ପାଠ୍ଯ));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) ନିର୍ଦ୍ଦେଶ.add(parser.sval);
                    ନିଷ୍ପାଦନ_କରନ୍ତୁ(ନିର୍ଦ୍ଦେଶ);
                }
            } catch (Exception exception) { ତ୍ରୁଟି(exception); }
        });
    }

    private void ଅଟକାନ୍ତୁ() {
        Process current = ପ୍ରକ୍ରିୟା;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void ଟର୍ମିନାଲ() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(ଡିରେକ୍ଟୋରି.toFile()).start(); }
        catch (Exception exception) { ତ୍ରୁଟି(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(ଡିରେକ୍ଟୋରି.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            ପଥ.setText(chooser.getSelectedFile().getAbsolutePath());
            ଲୋଡ_କର();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(ଡିରେକ୍ଟୋରି);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(ସୂଚକ("workspace") + " · WorldOS " + ସୂଚକ("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                ଅଟକାନ୍ତୁ(); worker.shutdownNow(); System.exit(0);
            }
        });
        ଉତ୍ସ.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ଉତ୍ସ.setTabSize(4);
        ନିର୍ଗମ.setFont(new Font("Monospaced", Font.PLAIN, 14));
        ନିର୍ଗମ.setEditable(false);
        JPanel ପଟ୍ଟିକା = new JPanel(new GridLayout(0, 1));
        JPanel ଫାଇଲ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ଫାଇଲ.add(new JLabel(ସୂଚକ("file"))); ଫାଇଲ.add(ପଥ);
        ପଟ୍ଟିକା.add(ଫାଇଲ);
        JPanel ସାଧନ_ପଟି = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(ସାଧନ_ପଟି, "open", () -> choose());
        button(ସାଧନ_ପଟି, "save", () -> ସଂରକ୍ଷଣ_କରନ୍ତୁ());
        button(ସାଧନ_ପଟି, "compile", () -> compile(false));
        button(ସାଧନ_ପଟି, "run", () -> compile(true));
        button(ସାଧନ_ପଟି, "stop", () -> ଅଟକାନ୍ତୁ());
        button(ସାଧନ_ପଟି, "terminal", () -> ଟର୍ମିନାଲ());
        ପଟ୍ଟିକା.add(ସାଧନ_ପଟି);
        JPanel ବିନ୍ଯାସ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ବିନ୍ଯାସ.add(new JLabel(ସୂଚକ("class"))); ବିନ୍ଯାସ.add(ନାମ);
        ବିନ୍ଯାସ.add(new JLabel(ସୂଚକ("arguments"))); ବିନ୍ଯାସ.add(arguments);
        ପଟ୍ଟିକା.add(ବିନ୍ଯାସ);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ଉତ୍ସ), new JScrollPane(ନିର୍ଗମ));
        split.setResizeWeight(0.72);
        window.add(ପଟ୍ଟିକା, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        ପଟ୍ଟିକା.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(ସୂଚକ("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ଉତ୍ସ.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        ନିର୍ଗମ.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension ଆକାର = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, ଆକାର.width - 40), Math.min(760, ଆକାର.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        ଲୋଡ_କର();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(ସୂଚକ("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
