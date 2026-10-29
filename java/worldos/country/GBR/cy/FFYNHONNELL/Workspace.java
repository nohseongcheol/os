// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.GBR.l_cy;
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
    private final JTextArea FFYNHONNELL = new JTextArea();
    private final JTextArea Allbwn = new JTextArea();
    private final JTextField LLWYBR = new JTextField("FFYNHONNELL.java", 26);
    private final JTextField Enw = new JTextField("FFYNHONNELL", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Cyfeiriadur = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String label(String Allwed) {
        return messages.getProperty(Allwed, Allwed);
    }

    private void append(String Testun) {
        SwingUtilities.invokeLater(() -> {
            Allbwn.append(Testun);
            Allbwn.setCaretPosition(Allbwn.getDocument().getLength());
        });
    }

    private void Gwall(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String Allwed, Runnable Gweithrediad) {
        JButton button = new JButton(label(Allwed));
        button.addActionListener(event -> Gweithrediad.run());
        panel.add(button);
    }

    private void Llwyth() {
        try {
            FFYNHONNELL.setText(Files.readString(Cyfeiriadur.resolve(LLWYBR.getText()), StandardCharsets.UTF_8));
            FFYNHONNELL.setCaretPosition(0);
        } catch (Exception exception) { Gwall(exception); }
    }

    private boolean Cadw() {
        try {
            Path Ffeil = Cyfeiriadur.resolve(LLWYBR.getText()).normalize();
            Files.createDirectories(Ffeil.getParent());
            Files.writeString(Ffeil, FFYNHONNELL.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + Ffeil + "\n");
            return true;
        } catch (Exception exception) { Gwall(exception); return false; }
    }

    private int Gweithredu(List<String> Gorchymyn) throws Exception {
        process = new ProcessBuilder(Gorchymyn).directory(Cyfeiriadur.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(label("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Gweithredu_2) {
        if (!Cadw()) return;
        String Ffeil = Cyfeiriadur.resolve(LLWYBR.getText()).toString();
        String Dosbarth = Enw.getText().trim();
        String Testun = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Cyfeiriadur.resolve("classes"));
                int result = Gweithredu(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Cyfeiriadur.resolve("classes").toString(), Ffeil));
                if (Gweithredu_2 && result == 0) {
                    List<String> Gorchymyn = new ArrayList<>(Arrays.asList("java", "-cp", Cyfeiriadur.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Dosbarth));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Testun));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Gorchymyn.add(parser.sval);
                    Gweithredu(Gorchymyn);
                }
            } catch (Exception exception) { Gwall(exception); }
        });
    }

    private void Atal() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Terfynell() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Cyfeiriadur.toFile()).start(); }
        catch (Exception exception) { Gwall(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Cyfeiriadur.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            LLWYBR.setText(chooser.getSelectedFile().getAbsolutePath());
            Llwyth();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Cyfeiriadur);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(label("workspace") + " · WorldOS " + label("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Atal(); worker.shutdownNow(); System.exit(0);
            }
        });
        FFYNHONNELL.setFont(new Font("Monospaced", Font.PLAIN, 17));
        FFYNHONNELL.setTabSize(4);
        Allbwn.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Allbwn.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Ffeil = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Ffeil.add(new JLabel(label("file"))); Ffeil.add(LLWYBR);
        panel.add(Ffeil);
        JPanel Bar_Dewis = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Bar_Dewis, "open", () -> choose());
        button(Bar_Dewis, "save", () -> Cadw());
        button(Bar_Dewis, "compile", () -> compile(false));
        button(Bar_Dewis, "run", () -> compile(true));
        button(Bar_Dewis, "stop", () -> Atal());
        button(Bar_Dewis, "terminal", () -> Terfynell());
        panel.add(Bar_Dewis);
        JPanel Gosodiadau = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Gosodiadau.add(new JLabel(label("class"))); Gosodiadau.add(Enw);
        Gosodiadau.add(new JLabel(label("arguments"))); Gosodiadau.add(arguments);
        panel.add(Gosodiadau);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(FFYNHONNELL), new JScrollPane(Allbwn));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(label("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        FFYNHONNELL.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Allbwn.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Maint = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Maint.width - 40), Math.min(760, Maint.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Llwyth();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(label("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
