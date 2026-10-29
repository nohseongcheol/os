// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.UKR.l_crh;
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
    private final JTextArea Kaynak = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField Yolçıq = new JTextField("Kaynak.java", 26);
    private final JTextField İsim = new JTextField("Kaynak", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path cilbent = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String Etiket(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Metin) {
        SwingUtilities.invokeLater(() -> {
            output.append(Metin);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void Hata(Exception exception) {
        append(Etiket("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String key, Runnable Amel) {
        JButton button = new JButton(Etiket(key));
        button.addActionListener(event -> Amel.run());
        panel.add(button);
    }

    private void Yük() {
        try {
            Kaynak.setText(Files.readString(cilbent.resolve(Yolçıq.getText()), StandardCharsets.UTF_8));
            Kaynak.setCaretPosition(0);
        } catch (Exception exception) { Hata(exception); }
    }

    private boolean Saqla() {
        try {
            Path Dosya = cilbent.resolve(Yolçıq.getText()).normalize();
            Files.createDirectories(Dosya.getParent());
            Files.writeString(Dosya, Kaynak.getText(), StandardCharsets.UTF_8);
            append(Etiket("save") + ": " + Dosya + "\n");
            return true;
        } catch (Exception exception) { Hata(exception); return false; }
    }

    private int İcra_et(List<String> Komut) throws Exception {
        process = new ProcessBuilder(Komut).directory(cilbent.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(Etiket("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Çaptır) {
        if (!Saqla()) return;
        String Dosya = cilbent.resolve(Yolçıq.getText()).toString();
        String SINIF = İsim.getText().trim();
        String Metin = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(cilbent.resolve("classes"));
                int result = İcra_et(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", cilbent.resolve("classes").toString(), Dosya));
                if (Çaptır && result == 0) {
                    List<String> Komut = new ArrayList<>(Arrays.asList("java", "-cp", cilbent.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", SINIF));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Metin));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Komut.add(parser.sval);
                    İcra_et(Komut);
                }
            } catch (Exception exception) { Hata(exception); }
        });
    }

    private void Toqtat() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(cilbent.toFile()).start(); }
        catch (Exception exception) { Hata(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(cilbent.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            Yolçıq.setText(chooser.getSelectedFile().getAbsolutePath());
            Yük();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(cilbent);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Etiket("workspace") + " · WorldOS " + Etiket("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Toqtat(); worker.shutdownNow(); System.exit(0);
            }
        });
        Kaynak.setFont(new Font("Monospaced", Font.PLAIN, 17));
        Kaynak.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Dosya = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Dosya.add(new JLabel(Etiket("file"))); Dosya.add(Yolçıq);
        panel.add(Dosya);
        JPanel Alet_çubuğı = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Alet_çubuğı, "open", () -> choose());
        button(Alet_çubuğı, "save", () -> Saqla());
        button(Alet_çubuğı, "compile", () -> compile(false));
        button(Alet_çubuğı, "run", () -> compile(true));
        button(Alet_çubuğı, "stop", () -> Toqtat());
        button(Alet_çubuğı, "terminal", () -> terminal());
        panel.add(Alet_çubuğı);
        JPanel Tesbitler = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Tesbitler.add(new JLabel(Etiket("class"))); Tesbitler.add(İsim);
        Tesbitler.add(new JLabel(Etiket("arguments"))); Tesbitler.add(arguments);
        panel.add(Tesbitler);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Kaynak), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etiket("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        Kaynak.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Boyut = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Boyut.width - 40), Math.min(760, Boyut.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Yük();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Etiket("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
