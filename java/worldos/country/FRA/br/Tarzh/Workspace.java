// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.FRA.l_br;
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
    private final JTextArea Tarzh = new JTextArea();
    private final JTextArea Ec_hankad = new JTextArea();
    private final JTextField TREUG = new JTextField("Tarzh.java", 26);
    private final JTextField Anv = new JTextField("Tarzh", 15);
    private final JTextField Arventennoù = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Renkell = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String Skritellig(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Testenn) {
        SwingUtilities.invokeLater(() -> {
            Ec_hankad.append(Testenn);
            Ec_hankad.setCaretPosition(Ec_hankad.getDocument().getLength());
        });
    }

    private void Fazi(Exception exception) {
        append(Skritellig("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel Penel_lankañ, String key, Runnable Gwezhiad) {
        JButton button = new JButton(Skritellig(key));
        button.addActionListener(event -> Gwezhiad.run());
        Penel_lankañ.add(button);
    }

    private void Kargañ() {
        try {
            Tarzh.setText(Files.readString(Renkell.resolve(TREUG.getText()), StandardCharsets.UTF_8));
            Tarzh.setCaretPosition(0);
        } catch (Exception exception) { Fazi(exception); }
    }

    private boolean Enrollañ() {
        try {
            Path Restr = Renkell.resolve(TREUG.getText()).normalize();
            Files.createDirectories(Restr.getParent());
            Files.writeString(Restr, Tarzh.getText(), StandardCharsets.UTF_8);
            append(Skritellig("save") + ": " + Restr + "\n");
            return true;
        } catch (Exception exception) { Fazi(exception); return false; }
    }

    private int Seveniñ(List<String> Arc_had) throws Exception {
        process = new ProcessBuilder(Arc_had).directory(Renkell.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(Skritellig("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Seveniñ_2) {
        if (!Enrollañ()) return;
        String Restr = Renkell.resolve(TREUG.getText()).toString();
        String Renkad = Anv.getText().trim();
        String Testenn = Arventennoù.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Renkell.resolve("classes"));
                int result = Seveniñ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Renkell.resolve("classes").toString(), Restr));
                if (Seveniñ_2 && result == 0) {
                    List<String> Arc_had = new ArrayList<>(Arrays.asList("java", "-cp", Renkell.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Renkad));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Testenn));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Arc_had.add(parser.sval);
                    Seveniñ(Arc_had);
                }
            } catch (Exception exception) { Fazi(exception); }
        });
    }

    private void Harz() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Termenell() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Renkell.toFile()).start(); }
        catch (Exception exception) { Fazi(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Renkell.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            TREUG.setText(chooser.getSelectedFile().getAbsolutePath());
            Kargañ();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Renkell);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Skritellig("workspace") + " · WorldOS " + Skritellig("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Harz(); worker.shutdownNow(); System.exit(0);
            }
        });
        Tarzh.setFont(new Font("Monospaced", Font.PLAIN, 17));
        Tarzh.setTabSize(4);
        Ec_hankad.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Ec_hankad.setEditable(false);
        JPanel Penel_lankañ = new JPanel(new GridLayout(0, 1));
        JPanel Restr = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Restr.add(new JLabel(Skritellig("file"))); Restr.add(TREUG);
        Penel_lankañ.add(Restr);
        JPanel Barrenn_ostilhoù = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Barrenn_ostilhoù, "open", () -> choose());
        button(Barrenn_ostilhoù, "save", () -> Enrollañ());
        button(Barrenn_ostilhoù, "compile", () -> compile(false));
        button(Barrenn_ostilhoù, "run", () -> compile(true));
        button(Barrenn_ostilhoù, "stop", () -> Harz());
        button(Barrenn_ostilhoù, "terminal", () -> Termenell());
        Penel_lankañ.add(Barrenn_ostilhoù);
        JPanel Arventennoù_2 = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Arventennoù_2.add(new JLabel(Skritellig("class"))); Arventennoù_2.add(Anv);
        Arventennoù_2.add(new JLabel(Skritellig("arguments"))); Arventennoù_2.add(Arventennoù);
        Penel_lankañ.add(Arventennoù_2);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Tarzh), new JScrollPane(Ec_hankad));
        split.setResizeWeight(0.72);
        window.add(Penel_lankañ, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Penel_lankañ.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Skritellig("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        Tarzh.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Ec_hankad.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Ment = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Ment.width - 40), Math.min(760, Ment.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Kargañ();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Skritellig("help") + "\n");
    }

    public static void main(String[] Arventennoù) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
