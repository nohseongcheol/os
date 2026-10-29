// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.CAN.l_bn;
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
    private final JTextArea উৎস_নথি = new JTextArea();
    private final JTextArea নির্গমের_অবস্থান = new JTextArea();
    private final JTextField পথ_2 = new JTextField("উৎস_নথি.java", 26);
    private final JTextField নাম = new JTextField("উৎস_নথি", 15);
    private final JTextField আর্গুমেন্ট_তালিকা = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path পথ = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process প্রসেস;

    private String লেবেল(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String পাঠ) {
        SwingUtilities.invokeLater(() -> {
            নির্গমের_অবস্থান.append(পাঠ);
            নির্গমের_অবস্থান.setCaretPosition(নির্গমের_অবস্থান.getDocument().getLength());
        });
    }

    private void ত্রুটি(Exception exception) {
        append(লেবেল("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel প্যানেল, String key, Runnable কাজ) {
        JButton button = new JButton(লেবেল(key));
        button.addActionListener(event -> কাজ.run());
        প্যানেল.add(button);
    }

    private void লোড() {
        try {
            উৎস_নথি.setText(Files.readString(পথ.resolve(পথ_2.getText()), StandardCharsets.UTF_8));
            উৎস_নথি.setCaretPosition(0);
        } catch (Exception exception) { ত্রুটি(exception); }
    }

    private boolean সংরক্ষণ() {
        try {
            Path নথির_নাম = পথ.resolve(পথ_2.getText()).normalize();
            Files.createDirectories(নথির_নাম.getParent());
            Files.writeString(নথির_নাম, উৎস_নথি.getText(), StandardCharsets.UTF_8);
            append(লেবেল("save") + ": " + নথির_নাম + "\n");
            return true;
        } catch (Exception exception) { ত্রুটি(exception); return false; }
    }

    private int চালানো(List<String> আদেশ) throws Exception {
        প্রসেস = new ProcessBuilder(আদেশ).directory(পথ.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(প্রসেস.getInputStream(), StandardCharsets.UTF_8))) {
            String নিবেশের_পঙ্_ক্তি;
            while ((নিবেশের_পঙ্_ক্তি = reader.readLine()) != null) append(নিবেশের_পঙ্_ক্তি + "\n");
        }
        int result = প্রসেস.waitFor();
        প্রসেস = null;
        append(লেবেল("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean চালনা) {
        if (!সংরক্ষণ()) return;
        String নথির_নাম = পথ.resolve(পথ_2.getText()).toString();
        String className = নাম.getText().trim();
        String পাঠ = আর্গুমেন্ট_তালিকা.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(পথ.resolve("classes"));
                int result = চালানো(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", পথ.resolve("classes").toString(), নথির_নাম));
                if (চালনা && result == 0) {
                    List<String> আদেশ = new ArrayList<>(Arrays.asList("java", "-cp", পথ.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(পাঠ));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) আদেশ.add(parser.sval);
                    চালানো(আদেশ);
                }
            } catch (Exception exception) { ত্রুটি(exception); }
        });
    }

    private void বন্ধ_করুন_2() {
        Process বর্তমান_অবস্থান = প্রসেস;
        if (বর্তমান_অবস্থান != null) {
            বর্তমান_অবস্থান.descendants().forEach(ProcessHandle::destroyForcibly);
            বর্তমান_অবস্থান.destroyForcibly();
        }
    }

    private void আদেশ_ব্যাখ্যাকারী() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(পথ.toFile()).start(); }
        catch (Exception exception) { ত্রুটি(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(পথ.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            পথ_2.setText(chooser.getSelectedFile().getAbsolutePath());
            লোড();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(পথ);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(লেবেল("workspace") + " · WorldOS " + লেবেল("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                বন্ধ_করুন_2(); worker.shutdownNow(); System.exit(0);
            }
        });
        উৎস_নথি.setFont(new Font("Monospaced", Font.PLAIN, 17));
        উৎস_নথি.setTabSize(4);
        নির্গমের_অবস্থান.setFont(new Font("Monospaced", Font.PLAIN, 14));
        নির্গমের_অবস্থান.setEditable(false);
        JPanel প্যানেল = new JPanel(new GridLayout(0, 1));
        JPanel নথির_নাম = new JPanel(new FlowLayout(FlowLayout.LEADING));
        নথির_নাম.add(new JLabel(লেবেল("file"))); নথির_নাম.add(পথ_2);
        প্যানেল.add(নথির_নাম);
        JPanel টুলবার = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(টুলবার, "open", () -> choose());
        button(টুলবার, "save", () -> সংরক্ষণ());
        button(টুলবার, "compile", () -> compile(false));
        button(টুলবার, "run", () -> compile(true));
        button(টুলবার, "stop", () -> বন্ধ_করুন_2());
        button(টুলবার, "terminal", () -> আদেশ_ব্যাখ্যাকারী());
        প্যানেল.add(টুলবার);
        JPanel সেটিংস = new JPanel(new FlowLayout(FlowLayout.LEADING));
        সেটিংস.add(new JLabel(লেবেল("class"))); সেটিংস.add(নাম);
        সেটিংস.add(new JLabel(লেবেল("arguments"))); সেটিংস.add(আর্গুমেন্ট_তালিকা);
        প্যানেল.add(সেটিংস);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(উৎস_নথি), new JScrollPane(নির্গমের_অবস্থান));
        split.setResizeWeight(0.72);
        window.add(প্যানেল, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        প্যানেল.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(লেবেল("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        উৎস_নথি.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        নির্গমের_অবস্থান.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension আকার = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, আকার.width - 40), Math.min(760, আকার.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        লোড();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(লেবেল("help") + "\n");
    }

    public static void main(String[] আর্গুমেন্ট_তালিকা) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
