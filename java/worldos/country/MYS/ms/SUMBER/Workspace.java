// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.MYS.l_ms;
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
    private final JFrame Tetingkap = new JFrame();
    private final JTextArea SUMBER = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField LALUAN = new JTextField("SUMBER.java", 26);
    private final JTextField Nama = new JTextField("SUMBER", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Direktori = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Proses;

    private String label(String Kunci) {
        return messages.getProperty(Kunci, Kunci);
    }

    private void append(String Teks) {
        SwingUtilities.invokeLater(() -> {
            output.append(Teks);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void RALAT(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void Butang(JPanel panel, String Kunci, Runnable Aksi) {
        JButton Butang = new JButton(label(Kunci));
        Butang.addActionListener(Peristiwa -> Aksi.run());
        panel.add(Butang);
    }

    private void Muatan() {
        try {
            SUMBER.setText(Files.readString(Direktori.resolve(LALUAN.getText()), StandardCharsets.UTF_8));
            SUMBER.setCaretPosition(0);
        } catch (Exception exception) { RALAT(exception); }
    }

    private boolean Simpan() {
        try {
            Path Fail = Direktori.resolve(LALUAN.getText()).normalize();
            Files.createDirectories(Fail.getParent());
            Files.writeString(Fail, SUMBER.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + Fail + "\n");
            return true;
        } catch (Exception exception) { RALAT(exception); return false; }
    }

    private int Lakukan(List<String> Perintah) throws Exception {
        Proses = new ProcessBuilder(Perintah).directory(Direktori.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Proses.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = Proses.waitFor();
        Proses = null;
        append(label("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Jalan) {
        if (!Simpan()) return;
        String Fail = Direktori.resolve(LALUAN.getText()).toString();
        String Kelas = Nama.getText().trim();
        String Teks = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Direktori.resolve("classes"));
                int result = Lakukan(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Direktori.resolve("classes").toString(), Fail));
                if (Jalan && result == 0) {
                    List<String> Perintah = new ArrayList<>(Arrays.asList("java", "-cp", Direktori.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Kelas));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Teks));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Perintah.add(parser.sval);
                    Lakukan(Perintah);
                }
            } catch (Exception exception) { RALAT(exception); }
        });
    }

    private void Henti() {
        Process Semasa = Proses;
        if (Semasa != null) {
            Semasa.descendants().forEach(ProcessHandle::destroyForcibly);
            Semasa.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Direktori.toFile()).start(); }
        catch (Exception exception) { RALAT(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Direktori.toFile());
        if (chooser.showOpenDialog(Tetingkap) == JFileChooser.APPROVE_OPTION) {
            LALUAN.setText(chooser.getSelectedFile().getAbsolutePath());
            Muatan();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Direktori);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Tetingkap.setTitle(label("workspace") + " · WorldOS " + label("identity"));
        Tetingkap.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Tetingkap.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Peristiwa) {
                Henti(); worker.shutdownNow(); System.exit(0);
            }
        });
        SUMBER.setFont(new Font("Monospaced", Font.PLAIN, 17));
        SUMBER.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Fail = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fail.add(new JLabel(label("file"))); Fail.add(LALUAN);
        panel.add(Fail);
        JPanel Palang_Alat = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Butang(Palang_Alat, "open", () -> choose());
        Butang(Palang_Alat, "save", () -> Simpan());
        Butang(Palang_Alat, "compile", () -> compile(false));
        Butang(Palang_Alat, "run", () -> compile(true));
        Butang(Palang_Alat, "stop", () -> Henti());
        Butang(Palang_Alat, "terminal", () -> terminal());
        panel.add(Palang_Alat);
        JPanel Tetapan = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Tetapan.add(new JLabel(label("class"))); Tetapan.add(Nama);
        Tetapan.add(new JLabel(label("arguments"))); Tetapan.add(arguments);
        panel.add(Tetapan);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(SUMBER), new JScrollPane(output));
        split.setResizeWeight(0.72);
        Tetingkap.add(panel, BorderLayout.NORTH);
        Tetingkap.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(label("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        SUMBER.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Saiz = Toolkit.getDefaultToolkit().getScreenSize();
        Tetingkap.setSize(Math.min(1240, Saiz.width - 40), Math.min(760, Saiz.height - 60));
        Tetingkap.setLocationRelativeTo(null);
        Tetingkap.setVisible(true);
        Muatan();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(label("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
