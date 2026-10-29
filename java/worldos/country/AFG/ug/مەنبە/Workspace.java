// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.AFG.l_ug;
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
    private final JFrame كۆزنەك = new JFrame();
    private final JTextArea مەنبە = new JTextArea();
    private final JTextArea چىقار = new JTextArea();
    private final JTextField يول = new JTextField("مەنبە.java", 26);
    private final JTextField ئاتى = new JTextField("مەنبە", 15);
    private final JTextField ئۆزگەرگۈچىلەر = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path مۇندەرىجە = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String ئەن(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String تېكىست) {
        SwingUtilities.invokeLater(() -> {
            چىقار.append(تېكىست);
            چىقار.setCaretPosition(چىقار.getDocument().getLength());
        });
    }

    private void خاتالىق(Exception exception) {
        append(ئەن("error") + ": " + exception.toString() + "\n");
    }

    private void كۇنۇپكا(JPanel تاختا, String key, Runnable مەشغۇلات) {
        JButton كۇنۇپكا = new JButton(ئەن(key));
        كۇنۇپكا.addActionListener(ھادىسە -> مەشغۇلات.run());
        تاختا.add(كۇنۇپكا);
    }

    private void يۈك() {
        try {
            مەنبە.setText(Files.readString(مۇندەرىجە.resolve(يول.getText()), StandardCharsets.UTF_8));
            مەنبە.setCaretPosition(0);
        } catch (Exception exception) { خاتالىق(exception); }
    }

    private boolean ساقلاش() {
        try {
            Path ھۆججەت = مۇندەرىجە.resolve(يول.getText()).normalize();
            Files.createDirectories(ھۆججەت.getParent());
            Files.writeString(ھۆججەت, مەنبە.getText(), StandardCharsets.UTF_8);
            append(ئەن("save") + ": " + ھۆججەت + "\n");
            return true;
        } catch (Exception exception) { خاتالىق(exception); return false; }
    }

    private int ئىجرا_قىل(List<String> بۇيرۇق) throws Exception {
        process = new ProcessBuilder(بۇيرۇق).directory(مۇندەرىجە.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String قۇر;
            while ((قۇر = reader.readLine()) != null) append(قۇر + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(ئەن("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean ئىجرا_قىل_2) {
        if (!ساقلاش()) return;
        String ھۆججەت = مۇندەرىجە.resolve(يول.getText()).toString();
        String تىپ = ئاتى.getText().trim();
        String تېكىست = ئۆزگەرگۈچىلەر.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(مۇندەرىجە.resolve("classes"));
                int result = ئىجرا_قىل(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", مۇندەرىجە.resolve("classes").toString(), ھۆججەت));
                if (ئىجرا_قىل_2 && result == 0) {
                    List<String> بۇيرۇق = new ArrayList<>(Arrays.asList("java", "-cp", مۇندەرىجە.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", تىپ));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(تېكىست));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) بۇيرۇق.add(parser.sval);
                    ئىجرا_قىل(بۇيرۇق);
                }
            } catch (Exception exception) { خاتالىق(exception); }
        });
    }

    private void توختا() {
        Process ھازىرقى_ۋاقىت = process;
        if (ھازىرقى_ۋاقىت != null) {
            ھازىرقى_ۋاقىت.descendants().forEach(ProcessHandle::destroyForcibly);
            ھازىرقى_ۋاقىت.destroyForcibly();
        }
    }

    private void تېرمىنال() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(مۇندەرىجە.toFile()).start(); }
        catch (Exception exception) { خاتالىق(exception); }
    }

    private void تاللا() {
        JFileChooser chooser = new JFileChooser(مۇندەرىجە.toFile());
        if (chooser.showOpenDialog(كۆزنەك) == JFileChooser.APPROVE_OPTION) {
            يول.setText(chooser.getSelectedFile().getAbsolutePath());
            يۈك();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(مۇندەرىجە);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        كۆزنەك.setTitle(ئەن("workspace") + " · WorldOS " + ئەن("identity"));
        كۆزنەك.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        كۆزنەك.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent ھادىسە) {
                توختا(); worker.shutdownNow(); System.exit(0);
            }
        });
        مەنبە.setFont(new Font("Monospaced", Font.PLAIN, 17));
        مەنبە.setTabSize(4);
        چىقار.setFont(new Font("Monospaced", Font.PLAIN, 14));
        چىقار.setEditable(false);
        JPanel تاختا = new JPanel(new GridLayout(0, 1));
        JPanel ھۆججەت = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ھۆججەت.add(new JLabel(ئەن("file"))); ھۆججەت.add(يول);
        تاختا.add(ھۆججەت);
        JPanel قورال_بالداق = new JPanel(new FlowLayout(FlowLayout.LEADING));
        كۇنۇپكا(قورال_بالداق, "open", () -> تاللا());
        كۇنۇپكا(قورال_بالداق, "save", () -> ساقلاش());
        كۇنۇپكا(قورال_بالداق, "compile", () -> compile(false));
        كۇنۇپكا(قورال_بالداق, "run", () -> compile(true));
        كۇنۇپكا(قورال_بالداق, "stop", () -> توختا());
        كۇنۇپكا(قورال_بالداق, "terminal", () -> تېرمىنال());
        تاختا.add(قورال_بالداق);
        JPanel تەڭشەكلەر = new JPanel(new FlowLayout(FlowLayout.LEADING));
        تەڭشەكلەر.add(new JLabel(ئەن("class"))); تەڭشەكلەر.add(ئاتى);
        تەڭشەكلەر.add(new JLabel(ئەن("arguments"))); تەڭشەكلەر.add(ئۆزگەرگۈچىلەر);
        تاختا.add(تەڭشەكلەر);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(مەنبە), new JScrollPane(چىقار));
        split.setResizeWeight(0.72);
        كۆزنەك.add(تاختا, BorderLayout.NORTH);
        كۆزنەك.add(split, BorderLayout.CENTER);
        تاختا.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(ئەن("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        مەنبە.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        چىقار.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension چوڭلۇقى = Toolkit.getDefaultToolkit().getScreenSize();
        كۆزنەك.setSize(Math.min(1240, چوڭلۇقى.width - 40), Math.min(760, چوڭلۇقى.height - 60));
        كۆزنەك.setLocationRelativeTo(null);
        كۆزنەك.setVisible(true);
        يۈك();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(ئەن("help") + "\n");
    }

    public static void main(String[] ئۆزگەرگۈچىلەر) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
