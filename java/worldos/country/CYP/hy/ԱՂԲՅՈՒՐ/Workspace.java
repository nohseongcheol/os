// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.CYP.l_hy;
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
    private final JTextArea ԱՂԲՅՈՒՐ = new JTextArea();
    private final JTextArea Ելք = new JTextArea();
    private final JTextField Ճանապարհ = new JTextField("ԱՂԲՅՈՒՐ.java", 26);
    private final JTextField Անուն = new JTextField("ԱՂԲՅՈՒՐ", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path ֆայլապանակ = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Գործընթաց;

    private String Պիտակ(String Բանալի) {
        return messages.getProperty(Բանալի, Բանալի);
    }

    private void append(String Տեքստ) {
        SwingUtilities.invokeLater(() -> {
            Ելք.append(Տեքստ);
            Ելք.setCaretPosition(Ելք.getDocument().getLength());
        });
    }

    private void Սխալ(Exception exception) {
        append(Պիտակ("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel Վահանակ, String Բանալի, Runnable Գործողություն) {
        JButton button = new JButton(Պիտակ(Բանալի));
        button.addActionListener(event -> Գործողություն.run());
        Վահանակ.add(button);
    }

    private void Բեռնում() {
        try {
            ԱՂԲՅՈՒՐ.setText(Files.readString(ֆայլապանակ.resolve(Ճանապարհ.getText()), StandardCharsets.UTF_8));
            ԱՂԲՅՈՒՐ.setCaretPosition(0);
        } catch (Exception exception) { Սխալ(exception); }
    }

    private boolean Պահել() {
        try {
            Path Ֆայլ = ֆայլապանակ.resolve(Ճանապարհ.getText()).normalize();
            Files.createDirectories(Ֆայլ.getParent());
            Files.writeString(Ֆայլ, ԱՂԲՅՈՒՐ.getText(), StandardCharsets.UTF_8);
            append(Պիտակ("save") + ": " + Ֆայլ + "\n");
            return true;
        } catch (Exception exception) { Սխալ(exception); return false; }
    }

    private int Կատարել(List<String> Հրահանգ) throws Exception {
        Գործընթաց = new ProcessBuilder(Հրահանգ).directory(ֆայլապանակ.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Գործընթաց.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = Գործընթաց.waitFor();
        Գործընթաց = null;
        append(Պիտակ("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Գործարկել) {
        if (!Պահել()) return;
        String Ֆայլ = ֆայլապանակ.resolve(Ճանապարհ.getText()).toString();
        String Կարգ = Անուն.getText().trim();
        String Տեքստ = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(ֆայլապանակ.resolve("classes"));
                int result = Կատարել(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", ֆայլապանակ.resolve("classes").toString(), Ֆայլ));
                if (Գործարկել && result == 0) {
                    List<String> Հրահանգ = new ArrayList<>(Arrays.asList("java", "-cp", ֆայլապանակ.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Կարգ));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Տեքստ));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Հրահանգ.add(parser.sval);
                    Կատարել(Հրահանգ);
                }
            } catch (Exception exception) { Սխալ(exception); }
        });
    }

    private void Կանգառ() {
        Process current = Գործընթաց;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Տերմինալ() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(ֆայլապանակ.toFile()).start(); }
        catch (Exception exception) { Սխալ(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(ֆայլապանակ.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            Ճանապարհ.setText(chooser.getSelectedFile().getAbsolutePath());
            Բեռնում();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(ֆայլապանակ);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Պիտակ("workspace") + " · WorldOS " + Պիտակ("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Կանգառ(); worker.shutdownNow(); System.exit(0);
            }
        });
        ԱՂԲՅՈՒՐ.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ԱՂԲՅՈՒՐ.setTabSize(4);
        Ելք.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Ելք.setEditable(false);
        JPanel Վահանակ = new JPanel(new GridLayout(0, 1));
        JPanel Ֆայլ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Ֆայլ.add(new JLabel(Պիտակ("file"))); Ֆայլ.add(Ճանապարհ);
        Վահանակ.add(Ֆայլ);
        JPanel Գործիքների_վահանակ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Գործիքների_վահանակ, "open", () -> choose());
        button(Գործիքների_վահանակ, "save", () -> Պահել());
        button(Գործիքների_վահանակ, "compile", () -> compile(false));
        button(Գործիքների_վահանակ, "run", () -> compile(true));
        button(Գործիքների_վահանակ, "stop", () -> Կանգառ());
        button(Գործիքների_վահանակ, "terminal", () -> Տերմինալ());
        Վահանակ.add(Գործիքների_վահանակ);
        JPanel Նախընտրանքներ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Նախընտրանքներ.add(new JLabel(Պիտակ("class"))); Նախընտրանքներ.add(Անուն);
        Նախընտրանքներ.add(new JLabel(Պիտակ("arguments"))); Նախընտրանքներ.add(arguments);
        Վահանակ.add(Նախընտրանքներ);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ԱՂԲՅՈՒՐ), new JScrollPane(Ելք));
        split.setResizeWeight(0.72);
        window.add(Վահանակ, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Վահանակ.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Պիտակ("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ԱՂԲՅՈՒՐ.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Ելք.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Չափս = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Չափս.width - 40), Math.min(760, Չափս.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Բեռնում();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Պիտակ("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
