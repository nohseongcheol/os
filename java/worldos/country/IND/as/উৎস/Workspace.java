// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_as;
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
    private final JTextArea উৎস = new JTextArea();
    private final JTextArea নিৰ্গম = new JTextArea();
    private final JTextField পথ = new JTextField("উৎস.java", 26);
    private final JTextField নাম = new JTextField("উৎস", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path ডিৰেক্টৰি = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process প্ৰসেস;

    private String লেবেল(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String টেক্সট) {
        SwingUtilities.invokeLater(() -> {
            নিৰ্গম.append(টেক্সট);
            নিৰ্গম.setCaretPosition(নিৰ্গম.getDocument().getLength());
        });
    }

    private void ত্ৰুটি(Exception exception) {
        append(লেবেল("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel পেনেল, String key, Runnable কাৰ্য্য) {
        JButton button = new JButton(লেবেল(key));
        button.addActionListener(event -> কাৰ্য্য.run());
        পেনেল.add(button);
    }

    private void তুলি_লওক() {
        try {
            উৎস.setText(Files.readString(ডিৰেক্টৰি.resolve(পথ.getText()), StandardCharsets.UTF_8));
            উৎস.setCaretPosition(0);
        } catch (Exception exception) { ত্ৰুটি(exception); }
    }

    private boolean সংৰক্ষণ() {
        try {
            Path নথিপত্ৰ = ডিৰেক্টৰি.resolve(পথ.getText()).normalize();
            Files.createDirectories(নথিপত্ৰ.getParent());
            Files.writeString(নথিপত্ৰ, উৎস.getText(), StandardCharsets.UTF_8);
            append(লেবেল("save") + ": " + নথিপত্ৰ + "\n");
            return true;
        } catch (Exception exception) { ত্ৰুটি(exception); return false; }
    }

    private int চলাওক(List<String> কমান্ড) throws Exception {
        প্ৰসেস = new ProcessBuilder(কমান্ড).directory(ডিৰেক্টৰি.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(প্ৰসেস.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = প্ৰসেস.waitFor();
        প্ৰসেস = null;
        append(লেবেল("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean সঞ্চালন) {
        if (!সংৰক্ষণ()) return;
        String নথিপত্ৰ = ডিৰেক্টৰি.resolve(পথ.getText()).toString();
        String className = নাম.getText().trim();
        String টেক্সট = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(ডিৰেক্টৰি.resolve("classes"));
                int result = চলাওক(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", ডিৰেক্টৰি.resolve("classes").toString(), নথিপত্ৰ));
                if (সঞ্চালন && result == 0) {
                    List<String> কমান্ড = new ArrayList<>(Arrays.asList("java", "-cp", ডিৰেক্টৰি.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(টেক্সট));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) কমান্ড.add(parser.sval);
                    চলাওক(কমান্ড);
                }
            } catch (Exception exception) { ত্ৰুটি(exception); }
        });
    }

    private void বন্ধ_কৰক_2() {
        Process current = প্ৰসেস;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void টাৰ্মিনেল() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(ডিৰেক্টৰি.toFile()).start(); }
        catch (Exception exception) { ত্ৰুটি(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(ডিৰেক্টৰি.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            পথ.setText(chooser.getSelectedFile().getAbsolutePath());
            তুলি_লওক();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(ডিৰেক্টৰি);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(লেবেল("workspace") + " · WorldOS " + লেবেল("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                বন্ধ_কৰক_2(); worker.shutdownNow(); System.exit(0);
            }
        });
        উৎস.setFont(new Font("Monospaced", Font.PLAIN, 17));
        উৎস.setTabSize(4);
        নিৰ্গম.setFont(new Font("Monospaced", Font.PLAIN, 14));
        নিৰ্গম.setEditable(false);
        JPanel পেনেল = new JPanel(new GridLayout(0, 1));
        JPanel নথিপত্ৰ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        নথিপত্ৰ.add(new JLabel(লেবেল("file"))); নথিপত্ৰ.add(পথ);
        পেনেল.add(নথিপত্ৰ);
        JPanel টুল_বাৰ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(টুল_বাৰ, "open", () -> choose());
        button(টুল_বাৰ, "save", () -> সংৰক্ষণ());
        button(টুল_বাৰ, "compile", () -> compile(false));
        button(টুল_বাৰ, "run", () -> compile(true));
        button(টুল_বাৰ, "stop", () -> বন্ধ_কৰক_2());
        button(টুল_বাৰ, "terminal", () -> টাৰ্মিনেল());
        পেনেল.add(টুল_বাৰ);
        JPanel বৈশিষ্ট্য = new JPanel(new FlowLayout(FlowLayout.LEADING));
        বৈশিষ্ট্য.add(new JLabel(লেবেল("class"))); বৈশিষ্ট্য.add(নাম);
        বৈশিষ্ট্য.add(new JLabel(লেবেল("arguments"))); বৈশিষ্ট্য.add(arguments);
        পেনেল.add(বৈশিষ্ট্য);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(উৎস), new JScrollPane(নিৰ্গম));
        split.setResizeWeight(0.72);
        window.add(পেনেল, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        পেনেল.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(লেবেল("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        উৎস.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        নিৰ্গম.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension মাপ = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, মাপ.width - 40), Math.min(760, মাপ.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        তুলি_লওক();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(লেবেল("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
