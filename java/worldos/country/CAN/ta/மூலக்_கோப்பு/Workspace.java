// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.CAN.l_ta;
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
    private final JTextArea மூலக்_கோப்பு = new JTextArea();
    private final JTextArea வெளியீட்டு_இடம் = new JTextArea();
    private final JTextField பாதை_2 = new JTextField("மூலக்_கோப்பு.java", 26);
    private final JTextField பெயர் = new JTextField("மூலக்_கோப்பு", 15);
    private final JTextField செயலுருபுகள் = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path பாதை = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process செயல்பாடு;

    private String விளக்கச்சீட்டு(String விசை) {
        return messages.getProperty(விசை, விசை);
    }

    private void append(String உரை) {
        SwingUtilities.invokeLater(() -> {
            வெளியீட்டு_இடம்.append(உரை);
            வெளியீட்டு_இடம்.setCaretPosition(வெளியீட்டு_இடம்.getDocument().getLength());
        });
    }

    private void பிழை(Exception exception) {
        append(விளக்கச்சீட்டு("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel பலகம், String விசை, Runnable செயல்) {
        JButton button = new JButton(விளக்கச்சீட்டு(விசை));
        button.addActionListener(event -> செயல்.run());
        பலகம்.add(button);
    }

    private void பளு்றி() {
        try {
            மூலக்_கோப்பு.setText(Files.readString(பாதை.resolve(பாதை_2.getText()), StandardCharsets.UTF_8));
            மூலக்_கோப்பு.setCaretPosition(0);
        } catch (Exception exception) { பிழை(exception); }
    }

    private boolean S_சேமிக்கவும்() {
        try {
            Path கோப்பின்_பெயர் = பாதை.resolve(பாதை_2.getText()).normalize();
            Files.createDirectories(கோப்பின்_பெயர்.getParent());
            Files.writeString(கோப்பின்_பெயர், மூலக்_கோப்பு.getText(), StandardCharsets.UTF_8);
            append(விளக்கச்சீட்டு("save") + ": " + கோப்பின்_பெயர் + "\n");
            return true;
        } catch (Exception exception) { பிழை(exception); return false; }
    }

    private int செயற்படுத்துக(List<String> கட்டளை) throws Exception {
        செயல்பாடு = new ProcessBuilder(கட்டளை).directory(பாதை.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(செயல்பாடு.getInputStream(), StandardCharsets.UTF_8))) {
            String உள்ளீட்டு_வரி;
            while ((உள்ளீட்டு_வரி = reader.readLine()) != null) append(உள்ளீட்டு_வரி + "\n");
        }
        int result = செயல்பாடு.waitFor();
        செயல்பாடு = null;
        append(விளக்கச்சீட்டு("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean செயல்படுத்துக) {
        if (!S_சேமிக்கவும்()) return;
        String கோப்பின்_பெயர் = பாதை.resolve(பாதை_2.getText()).toString();
        String வகுப்பு = பெயர்.getText().trim();
        String உரை = செயலுருபுகள்.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(பாதை.resolve("classes"));
                int result = செயற்படுத்துக(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", பாதை.resolve("classes").toString(), கோப்பின்_பெயர்));
                if (செயல்படுத்துக && result == 0) {
                    List<String> கட்டளை = new ArrayList<>(Arrays.asList("java", "-cp", பாதை.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", வகுப்பு));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(உரை));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) கட்டளை.add(parser.sval);
                    செயற்படுத்துக(கட்டளை);
                }
            } catch (Exception exception) { பிழை(exception); }
        });
    }

    private void நிறுத்து() {
        Process நடப்பு_இடம் = செயல்பாடு;
        if (நடப்பு_இடம் != null) {
            நடப்பு_இடம்.descendants().forEach(ProcessHandle::destroyForcibly);
            நடப்பு_இடம்.destroyForcibly();
        }
    }

    private void கட்டளை_விளக்கி() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(பாதை.toFile()).start(); }
        catch (Exception exception) { பிழை(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(பாதை.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            பாதை_2.setText(chooser.getSelectedFile().getAbsolutePath());
            பளு்றி();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(பாதை);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(விளக்கச்சீட்டு("workspace") + " · WorldOS " + விளக்கச்சீட்டு("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                நிறுத்து(); worker.shutdownNow(); System.exit(0);
            }
        });
        மூலக்_கோப்பு.setFont(new Font("Monospaced", Font.PLAIN, 17));
        மூலக்_கோப்பு.setTabSize(4);
        வெளியீட்டு_இடம்.setFont(new Font("Monospaced", Font.PLAIN, 14));
        வெளியீட்டு_இடம்.setEditable(false);
        JPanel பலகம் = new JPanel(new GridLayout(0, 1));
        JPanel கோப்பின்_பெயர் = new JPanel(new FlowLayout(FlowLayout.LEADING));
        கோப்பின்_பெயர்.add(new JLabel(விளக்கச்சீட்டு("file"))); கோப்பின்_பெயர்.add(பாதை_2);
        பலகம்.add(கோப்பின்_பெயர்);
        JPanel கருவிப்பட்டை = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(கருவிப்பட்டை, "open", () -> choose());
        button(கருவிப்பட்டை, "save", () -> S_சேமிக்கவும்());
        button(கருவிப்பட்டை, "compile", () -> compile(false));
        button(கருவிப்பட்டை, "run", () -> compile(true));
        button(கருவிப்பட்டை, "stop", () -> நிறுத்து());
        button(கருவிப்பட்டை, "terminal", () -> கட்டளை_விளக்கி());
        பலகம்.add(கருவிப்பட்டை);
        JPanel அமைப்புகள் = new JPanel(new FlowLayout(FlowLayout.LEADING));
        அமைப்புகள்.add(new JLabel(விளக்கச்சீட்டு("class"))); அமைப்புகள்.add(பெயர்);
        அமைப்புகள்.add(new JLabel(விளக்கச்சீட்டு("arguments"))); அமைப்புகள்.add(செயலுருபுகள்);
        பலகம்.add(அமைப்புகள்);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(மூலக்_கோப்பு), new JScrollPane(வெளியீட்டு_இடம்));
        split.setResizeWeight(0.72);
        window.add(பலகம், BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        பலகம்.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(விளக்கச்சீட்டு("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        மூலக்_கோப்பு.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        வெளியீட்டு_இடம்.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension அளவு = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, அளவு.width - 40), Math.min(760, அளவு.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        பளு்றி();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(விளக்கச்சீட்டு("help") + "\n");
    }

    public static void main(String[] செயலுருபுகள்) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
