// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_te;
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
    private final JFrame విండో = new JFrame();
    private final JTextArea వనరు = new JTextArea();
    private final JTextArea అవుట్పుట్ = new JTextArea();
    private final JTextField పాత్ = new JTextField("వనరు.java", 26);
    private final JTextField పేరు = new JTextField("వనరు", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path డైరెక్టరీ = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process క్రమణం;

    private String లేబుల్(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String పాఠ్యము) {
        SwingUtilities.invokeLater(() -> {
            అవుట్పుట్.append(పాఠ్యము);
            అవుట్పుట్.setCaretPosition(అవుట్పుట్.getDocument().getLength());
        });
    }

    private void దోషం(Exception exception) {
        append(లేబుల్("error") + ": " + exception.toString() + "\n");
    }

    private void బటన్(JPanel ప్యానల్, String key, Runnable చర్య) {
        JButton బటన్ = new JButton(లేబుల్(key));
        బటన్.addActionListener(event -> చర్య.run());
        ప్యానల్.add(బటన్);
    }

    private void భారం() {
        try {
            వనరు.setText(Files.readString(డైరెక్టరీ.resolve(పాత్.getText()), StandardCharsets.UTF_8));
            వనరు.setCaretPosition(0);
        } catch (Exception exception) { దోషం(exception); }
    }

    private boolean దాచు() {
        try {
            Path దస్త్రం = డైరెక్టరీ.resolve(పాత్.getText()).normalize();
            Files.createDirectories(దస్త్రం.getParent());
            Files.writeString(దస్త్రం, వనరు.getText(), StandardCharsets.UTF_8);
            append(లేబుల్("save") + ": " + దస్త్రం + "\n");
            return true;
        } catch (Exception exception) { దోషం(exception); return false; }
    }

    private int అమలుపరుచు(List<String> ఆదేశము) throws Exception {
        క్రమణం = new ProcessBuilder(ఆదేశము).directory(డైరెక్టరీ.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(క్రమణం.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = క్రమణం.waitFor();
        క్రమణం = null;
        append(లేబుల్("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean నడుపుము) {
        if (!దాచు()) return;
        String దస్త్రం = డైరెక్టరీ.resolve(పాత్.getText()).toString();
        String తరగతి = పేరు.getText().trim();
        String పాఠ్యము = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(డైరెక్టరీ.resolve("classes"));
                int result = అమలుపరుచు(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", డైరెక్టరీ.resolve("classes").toString(), దస్త్రం));
                if (నడుపుము && result == 0) {
                    List<String> ఆదేశము = new ArrayList<>(Arrays.asList("java", "-cp", డైరెక్టరీ.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", తరగతి));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(పాఠ్యము));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) ఆదేశము.add(parser.sval);
                    అమలుపరుచు(ఆదేశము);
                }
            } catch (Exception exception) { దోషం(exception); }
        });
    }

    private void నిలిపి_వేయు() {
        Process ప్రస్తుతం = క్రమణం;
        if (ప్రస్తుతం != null) {
            ప్రస్తుతం.descendants().forEach(ProcessHandle::destroyForcibly);
            ప్రస్తుతం.destroyForcibly();
        }
    }

    private void టెర్మినల్() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(డైరెక్టరీ.toFile()).start(); }
        catch (Exception exception) { దోషం(exception); }
    }

    private void ఎన్నుకొను() {
        JFileChooser chooser = new JFileChooser(డైరెక్టరీ.toFile());
        if (chooser.showOpenDialog(విండో) == JFileChooser.APPROVE_OPTION) {
            పాత్.setText(chooser.getSelectedFile().getAbsolutePath());
            భారం();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(డైరెక్టరీ);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        విండో.setTitle(లేబుల్("workspace") + " · WorldOS " + లేబుల్("identity"));
        విండో.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        విండో.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                నిలిపి_వేయు(); worker.shutdownNow(); System.exit(0);
            }
        });
        వనరు.setFont(new Font("Monospaced", Font.PLAIN, 17));
        వనరు.setTabSize(4);
        అవుట్పుట్.setFont(new Font("Monospaced", Font.PLAIN, 14));
        అవుట్పుట్.setEditable(false);
        JPanel ప్యానల్ = new JPanel(new GridLayout(0, 1));
        JPanel దస్త్రం = new JPanel(new FlowLayout(FlowLayout.LEADING));
        దస్త్రం.add(new JLabel(లేబుల్("file"))); దస్త్రం.add(పాత్);
        ప్యానల్.add(దస్త్రం);
        JPanel పనిముట్ల_పట్టా = new JPanel(new FlowLayout(FlowLayout.LEADING));
        బటన్(పనిముట్ల_పట్టా, "open", () -> ఎన్నుకొను());
        బటన్(పనిముట్ల_పట్టా, "save", () -> దాచు());
        బటన్(పనిముట్ల_పట్టా, "compile", () -> compile(false));
        బటన్(పనిముట్ల_పట్టా, "run", () -> compile(true));
        బటన్(పనిముట్ల_పట్టా, "stop", () -> నిలిపి_వేయు());
        బటన్(పనిముట్ల_పట్టా, "terminal", () -> టెర్మినల్());
        ప్యానల్.add(పనిముట్ల_పట్టా);
        JPanel అమరికలు = new JPanel(new FlowLayout(FlowLayout.LEADING));
        అమరికలు.add(new JLabel(లేబుల్("class"))); అమరికలు.add(పేరు);
        అమరికలు.add(new JLabel(లేబుల్("arguments"))); అమరికలు.add(arguments);
        ప్యానల్.add(అమరికలు);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(వనరు), new JScrollPane(అవుట్పుట్));
        split.setResizeWeight(0.72);
        విండో.add(ప్యానల్, BorderLayout.NORTH);
        విండో.add(split, BorderLayout.CENTER);
        ప్యానల్.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(లేబుల్("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        వనరు.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        అవుట్పుట్.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension పరిమాణం = Toolkit.getDefaultToolkit().getScreenSize();
        విండో.setSize(Math.min(1240, పరిమాణం.width - 40), Math.min(760, పరిమాణం.height - 60));
        విండో.setLocationRelativeTo(null);
        విండో.setVisible(true);
        భారం();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(లేబుల్("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
