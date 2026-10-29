// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.GBR.l_ga;
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
    private final JTextArea FOINSE = new JTextArea();
    private final JTextArea Aschur = new JTextArea();
    private final JTextField CONAIR = new JTextField("FOINSE.java", 26);
    private final JTextField Ainm = new JTextField("FOINSE", 15);
    private final JTextField Argóintí = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Comhadlann = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Próiseas;

    private String Lipéad(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Téacs) {
        SwingUtilities.invokeLater(() -> {
            Aschur.append(Téacs);
            Aschur.setCaretPosition(Aschur.getDocument().getLength());
        });
    }

    private void ERREÁID(Exception exception) {
        append(Lipéad("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel Painéal, String key, Runnable Gníomh) {
        JButton button = new JButton(Lipéad(key));
        button.addActionListener(event -> Gníomh.run());
        Painéal.add(button);
    }

    private void Lód() {
        try {
            FOINSE.setText(Files.readString(Comhadlann.resolve(CONAIR.getText()), StandardCharsets.UTF_8));
            FOINSE.setCaretPosition(0);
        } catch (Exception exception) { ERREÁID(exception); }
    }

    private boolean Sábháil() {
        try {
            Path Comhad = Comhadlann.resolve(CONAIR.getText()).normalize();
            Files.createDirectories(Comhad.getParent());
            Files.writeString(Comhad, FOINSE.getText(), StandardCharsets.UTF_8);
            append(Lipéad("save") + ": " + Comhad + "\n");
            return true;
        } catch (Exception exception) { ERREÁID(exception); return false; }
    }

    private int Rith(List<String> Ordú) throws Exception {
        Próiseas = new ProcessBuilder(Ordú).directory(Comhadlann.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Próiseas.getInputStream(), StandardCharsets.UTF_8))) {
            String Líne;
            while ((Líne = reader.readLine()) != null) append(Líne + "\n");
        }
        int result = Próiseas.waitFor();
        Próiseas = null;
        append(Lipéad("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Rith_2) {
        if (!Sábháil()) return;
        String Comhad = Comhadlann.resolve(CONAIR.getText()).toString();
        String Aicme = Ainm.getText().trim();
        String Téacs = Argóintí.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Comhadlann.resolve("classes"));
                int result = Rith(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Comhadlann.resolve("classes").toString(), Comhad));
                if (Rith_2 && result == 0) {
                    List<String> Ordú = new ArrayList<>(Arrays.asList("java", "-cp", Comhadlann.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Aicme));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Téacs));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Ordú.add(parser.sval);
                    Rith(Ordú);
                }
            } catch (Exception exception) { ERREÁID(exception); }
        });
    }

    private void Stad() {
        Process current = Próiseas;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Teirminéal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Comhadlann.toFile()).start(); }
        catch (Exception exception) { ERREÁID(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Comhadlann.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            CONAIR.setText(chooser.getSelectedFile().getAbsolutePath());
            Lód();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Comhadlann);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Lipéad("workspace") + " · WorldOS " + Lipéad("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Stad(); worker.shutdownNow(); System.exit(0);
            }
        });
        FOINSE.setFont(new Font("Monospaced", Font.PLAIN, 17));
        FOINSE.setTabSize(4);
        Aschur.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Aschur.setEditable(false);
        JPanel Painéal = new JPanel(new GridLayout(0, 1));
        JPanel Comhad = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Comhad.add(new JLabel(Lipéad("file"))); Comhad.add(CONAIR);
        Painéal.add(Comhad);
        JPanel Barra_Uirlisí = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Barra_Uirlisí, "open", () -> choose());
        button(Barra_Uirlisí, "save", () -> Sábháil());
        button(Barra_Uirlisí, "compile", () -> compile(false));
        button(Barra_Uirlisí, "run", () -> compile(true));
        button(Barra_Uirlisí, "stop", () -> Stad());
        button(Barra_Uirlisí, "terminal", () -> Teirminéal());
        Painéal.add(Barra_Uirlisí);
        JPanel Socruithe = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Socruithe.add(new JLabel(Lipéad("class"))); Socruithe.add(Ainm);
        Socruithe.add(new JLabel(Lipéad("arguments"))); Socruithe.add(Argóintí);
        Painéal.add(Socruithe);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(FOINSE), new JScrollPane(Aschur));
        split.setResizeWeight(0.72);
        window.add(Painéal, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Painéal.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Lipéad("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        FOINSE.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Aschur.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Méid = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Méid.width - 40), Math.min(760, Méid.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Lód();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Lipéad("help") + "\n");
    }

    public static void main(String[] Argóintí) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
