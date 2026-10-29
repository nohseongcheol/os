// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.QAT.l_ml;
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
    private final JTextArea ഉറവിടം = new JTextArea();
    private final JTextArea ഫലം = new JTextArea();
    private final JTextField വഴി = new JTextField("ഉറവിടം.java", 26);
    private final JTextField പേരു് = new JTextField("ഉറവിടം", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path ഡയറക്ടറി = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process പ്രക്രിയ;

    private String ലേബല്(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String പദാവലി) {
        SwingUtilities.invokeLater(() -> {
            ഫലം.append(പദാവലി);
            ഫലം.setCaretPosition(ഫലം.getDocument().getLength());
        });
    }

    private void പിശക്(Exception exception) {
        append(ലേബല്("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel പാളി, String key, Runnable നടപടി) {
        JButton button = new JButton(ലേബല്(key));
        button.addActionListener(event -> നടപടി.run());
        പാളി.add(button);
    }

    private void ലോഡ്() {
        try {
            ഉറവിടം.setText(Files.readString(ഡയറക്ടറി.resolve(വഴി.getText()), StandardCharsets.UTF_8));
            ഉറവിടം.setCaretPosition(0);
        } catch (Exception exception) { പിശക്(exception); }
    }

    private boolean സൂക്ഷിയ്ക്കുക() {
        try {
            Path ഫയല് = ഡയറക്ടറി.resolve(വഴി.getText()).normalize();
            Files.createDirectories(ഫയല്.getParent());
            Files.writeString(ഫയല്, ഉറവിടം.getText(), StandardCharsets.UTF_8);
            append(ലേബല്("save") + ": " + ഫയല് + "\n");
            return true;
        } catch (Exception exception) { പിശക്(exception); return false; }
    }

    private int പ്രവര്_ത്തിപ്പിയ്ക്കുക(List<String> ആജ്ഞ) throws Exception {
        പ്രക്രിയ = new ProcessBuilder(ആജ്ഞ).directory(ഡയറക്ടറി.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(പ്രക്രിയ.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = പ്രക്രിയ.waitFor();
        പ്രക്രിയ = null;
        append(ലേബല്("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean നടപ്പിലാക്കുക) {
        if (!സൂക്ഷിയ്ക്കുക()) return;
        String ഫയല് = ഡയറക്ടറി.resolve(വഴി.getText()).toString();
        String ക്ലാസ്സ് = പേരു്.getText().trim();
        String പദാവലി = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(ഡയറക്ടറി.resolve("classes"));
                int result = പ്രവര്_ത്തിപ്പിയ്ക്കുക(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", ഡയറക്ടറി.resolve("classes").toString(), ഫയല്));
                if (നടപ്പിലാക്കുക && result == 0) {
                    List<String> ആജ്ഞ = new ArrayList<>(Arrays.asList("java", "-cp", ഡയറക്ടറി.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", ക്ലാസ്സ്));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(പദാവലി));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) ആജ്ഞ.add(parser.sval);
                    പ്രവര്_ത്തിപ്പിയ്ക്കുക(ആജ്ഞ);
                }
            } catch (Exception exception) { പിശക്(exception); }
        });
    }

    private void നിര്_ത്തുക() {
        Process current = പ്രക്രിയ;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void ടെ_ര്മിനല്() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(ഡയറക്ടറി.toFile()).start(); }
        catch (Exception exception) { പിശക്(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(ഡയറക്ടറി.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            വഴി.setText(chooser.getSelectedFile().getAbsolutePath());
            ലോഡ്();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(ഡയറക്ടറി);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(ലേബല്("workspace") + " · WorldOS " + ലേബല്("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                നിര്_ത്തുക(); worker.shutdownNow(); System.exit(0);
            }
        });
        ഉറവിടം.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ഉറവിടം.setTabSize(4);
        ഫലം.setFont(new Font("Monospaced", Font.PLAIN, 14));
        ഫലം.setEditable(false);
        JPanel പാളി = new JPanel(new GridLayout(0, 1));
        JPanel ഫയല് = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ഫയല്.add(new JLabel(ലേബല്("file"))); ഫയല്.add(വഴി);
        പാളി.add(ഫയല്);
        JPanel ടൂള്_ബാര് = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(ടൂള്_ബാര്, "open", () -> choose());
        button(ടൂള്_ബാര്, "save", () -> സൂക്ഷിയ്ക്കുക());
        button(ടൂള്_ബാര്, "compile", () -> compile(false));
        button(ടൂള്_ബാര്, "run", () -> compile(true));
        button(ടൂള്_ബാര്, "stop", () -> നിര്_ത്തുക());
        button(ടൂള്_ബാര്, "terminal", () -> ടെ_ര്മിനല്());
        പാളി.add(ടൂള്_ബാര്);
        JPanel സജ്ജീകരണം = new JPanel(new FlowLayout(FlowLayout.LEADING));
        സജ്ജീകരണം.add(new JLabel(ലേബല്("class"))); സജ്ജീകരണം.add(പേരു്);
        സജ്ജീകരണം.add(new JLabel(ലേബല്("arguments"))); സജ്ജീകരണം.add(arguments);
        പാളി.add(സജ്ജീകരണം);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ഉറവിടം), new JScrollPane(ഫലം));
        split.setResizeWeight(0.72);
        window.add(പാളി, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        പാളി.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(ലേബല്("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ഉറവിടം.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        ഫലം.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension വലിപ്പം = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, വലിപ്പം.width - 40), Math.min(760, വലിപ്പം.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        ലോഡ്();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(ലേബല്("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
