// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.CAN.l_pa;
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
    private final JTextArea ਸਰੋਤ = new JTextArea();
    private final JTextArea ਆਉਟਪੁੱਟ = new JTextArea();
    private final JTextField ਮਾਰਗ = new JTextField("ਸਰੋਤ.java", 26);
    private final JTextField ਨਾਂ = new JTextField("ਸਰੋਤ", 15);
    private final JTextField ਆਰਗੂਮੈਂਟ = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path ਡਾਇਰੈਕਟਰੀ = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process ਪਰੋਸੈੱਸ;

    private String ਲੇਬਲ(String ਸਵਿੱਚ) {
        return messages.getProperty(ਸਵਿੱਚ, ਸਵਿੱਚ);
    }

    private void append(String ਟੈਕਸਟ) {
        SwingUtilities.invokeLater(() -> {
            ਆਉਟਪੁੱਟ.append(ਟੈਕਸਟ);
            ਆਉਟਪੁੱਟ.setCaretPosition(ਆਉਟਪੁੱਟ.getDocument().getLength());
        });
    }

    private void ਗਲਤੀ(Exception exception) {
        append(ਲੇਬਲ("error") + ": " + exception.toString() + "\n");
    }

    private void ਬਟਨ(JPanel ਪੈਨਲ, String ਸਵਿੱਚ, Runnable ਐਕਸ਼ਨ) {
        JButton ਬਟਨ = new JButton(ਲੇਬਲ(ਸਵਿੱਚ));
        ਬਟਨ.addActionListener(event -> ਐਕਸ਼ਨ.run());
        ਪੈਨਲ.add(ਬਟਨ);
    }

    private void ਲੋਡ() {
        try {
            ਸਰੋਤ.setText(Files.readString(ਡਾਇਰੈਕਟਰੀ.resolve(ਮਾਰਗ.getText()), StandardCharsets.UTF_8));
            ਸਰੋਤ.setCaretPosition(0);
        } catch (Exception exception) { ਗਲਤੀ(exception); }
    }

    private boolean ਸੰਭਾਲੋ() {
        try {
            Path ਫਾਇਲ = ਡਾਇਰੈਕਟਰੀ.resolve(ਮਾਰਗ.getText()).normalize();
            Files.createDirectories(ਫਾਇਲ.getParent());
            Files.writeString(ਫਾਇਲ, ਸਰੋਤ.getText(), StandardCharsets.UTF_8);
            append(ਲੇਬਲ("save") + ": " + ਫਾਇਲ + "\n");
            return true;
        } catch (Exception exception) { ਗਲਤੀ(exception); return false; }
    }

    private int ਚਲਾਓ(List<String> ਕਮਾਂਡ) throws Exception {
        ਪਰੋਸੈੱਸ = new ProcessBuilder(ਕਮਾਂਡ).directory(ਡਾਇਰੈਕਟਰੀ.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(ਪਰੋਸੈੱਸ.getInputStream(), StandardCharsets.UTF_8))) {
            String ਲਾਈਨ;
            while ((ਲਾਈਨ = reader.readLine()) != null) append(ਲਾਈਨ + "\n");
        }
        int result = ਪਰੋਸੈੱਸ.waitFor();
        ਪਰੋਸੈੱਸ = null;
        append(ਲੇਬਲ("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean ਚਲਾਓ_2) {
        if (!ਸੰਭਾਲੋ()) return;
        String ਫਾਇਲ = ਡਾਇਰੈਕਟਰੀ.resolve(ਮਾਰਗ.getText()).toString();
        String ਕਲਾਸ = ਨਾਂ.getText().trim();
        String ਟੈਕਸਟ = ਆਰਗੂਮੈਂਟ.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(ਡਾਇਰੈਕਟਰੀ.resolve("classes"));
                int result = ਚਲਾਓ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", ਡਾਇਰੈਕਟਰੀ.resolve("classes").toString(), ਫਾਇਲ));
                if (ਚਲਾਓ_2 && result == 0) {
                    List<String> ਕਮਾਂਡ = new ArrayList<>(Arrays.asList("java", "-cp", ਡਾਇਰੈਕਟਰੀ.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", ਕਲਾਸ));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(ਟੈਕਸਟ));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) ਕਮਾਂਡ.add(parser.sval);
                    ਚਲਾਓ(ਕਮਾਂਡ);
                }
            } catch (Exception exception) { ਗਲਤੀ(exception); }
        });
    }

    private void ਰੋਕੋ() {
        Process current = ਪਰੋਸੈੱਸ;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void ਟਰਮੀਨਲ() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(ਡਾਇਰੈਕਟਰੀ.toFile()).start(); }
        catch (Exception exception) { ਗਲਤੀ(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(ਡਾਇਰੈਕਟਰੀ.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            ਮਾਰਗ.setText(chooser.getSelectedFile().getAbsolutePath());
            ਲੋਡ();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(ਡਾਇਰੈਕਟਰੀ);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(ਲੇਬਲ("workspace") + " · WorldOS " + ਲੇਬਲ("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                ਰੋਕੋ(); worker.shutdownNow(); System.exit(0);
            }
        });
        ਸਰੋਤ.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ਸਰੋਤ.setTabSize(4);
        ਆਉਟਪੁੱਟ.setFont(new Font("Monospaced", Font.PLAIN, 14));
        ਆਉਟਪੁੱਟ.setEditable(false);
        JPanel ਪੈਨਲ = new JPanel(new GridLayout(0, 1));
        JPanel ਫਾਇਲ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ਫਾਇਲ.add(new JLabel(ਲੇਬਲ("file"))); ਫਾਇਲ.add(ਮਾਰਗ);
        ਪੈਨਲ.add(ਫਾਇਲ);
        JPanel ਟੂਲਬਾਰ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ਬਟਨ(ਟੂਲਬਾਰ, "open", () -> choose());
        ਬਟਨ(ਟੂਲਬਾਰ, "save", () -> ਸੰਭਾਲੋ());
        ਬਟਨ(ਟੂਲਬਾਰ, "compile", () -> compile(false));
        ਬਟਨ(ਟੂਲਬਾਰ, "run", () -> compile(true));
        ਬਟਨ(ਟੂਲਬਾਰ, "stop", () -> ਰੋਕੋ());
        ਬਟਨ(ਟੂਲਬਾਰ, "terminal", () -> ਟਰਮੀਨਲ());
        ਪੈਨਲ.add(ਟੂਲਬਾਰ);
        JPanel ਸੈਟਿੰਗ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ਸੈਟਿੰਗ.add(new JLabel(ਲੇਬਲ("class"))); ਸੈਟਿੰਗ.add(ਨਾਂ);
        ਸੈਟਿੰਗ.add(new JLabel(ਲੇਬਲ("arguments"))); ਸੈਟਿੰਗ.add(ਆਰਗੂਮੈਂਟ);
        ਪੈਨਲ.add(ਸੈਟਿੰਗ);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ਸਰੋਤ), new JScrollPane(ਆਉਟਪੁੱਟ));
        split.setResizeWeight(0.72);
        window.add(ਪੈਨਲ, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        ਪੈਨਲ.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(ਲੇਬਲ("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ਸਰੋਤ.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        ਆਉਟਪੁੱਟ.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension ਆਕਾਰ = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, ਆਕਾਰ.width - 40), Math.min(760, ਆਕਾਰ.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        ਲੋਡ();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(ਲੇਬਲ("help") + "\n");
    }

    public static void main(String[] ਆਰਗੂਮੈਂਟ) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
