// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.CAN.l_hi;
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
public final class कार्यशाला {
    private final JFrame खिड़की = new JFrame();
    private final JTextArea स्रोत = new JTextArea();
    private final JTextArea निर्गम = new JTextArea();
    private final JTextField पथ = new JTextField("स्रोत.java", 26);
    private final JTextField नाम = new JTextField("स्रोत", 15);
    private final JTextField तर्क = new JTextField(25);
    private final Properties संदेश = new Properties();
    private final Path निर्देशिका = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService कार्यसूत्र = Executors.newSingleThreadExecutor();
    private volatile Process प्रक्रिया;

    private String लेबल(String कुंजी) {
        return संदेश.getProperty(कुंजी, कुंजी);
    }

    private void जोड़ें(String पाठ) {
        SwingUtilities.invokeLater(() -> {
            निर्गम.append(पाठ);
            निर्गम.setCaretPosition(निर्गम.getDocument().getLength());
        });
    }

    private void त्रुटि(Exception अपवाद) {
        जोड़ें(लेबल("error") + ": " + अपवाद.toString() + "\n");
    }

    private void बटन(JPanel पट्ट, String कुंजी, Runnable क्रिया) {
        JButton बटन = new JButton(लेबल(कुंजी));
        बटन.addActionListener(घटना -> क्रिया.run());
        पट्ट.add(बटन);
    }

    private void लोडकरें() {
        try {
            स्रोत.setText(Files.readString(निर्देशिका.resolve(पथ.getText()), StandardCharsets.UTF_8));
            स्रोत.setCaretPosition(0);
        } catch (Exception अपवाद) { त्रुटि(अपवाद); }
    }

    private boolean सहेजें() {
        try {
            Path संचिका = निर्देशिका.resolve(पथ.getText()).normalize();
            Files.createDirectories(संचिका.getParent());
            Files.writeString(संचिका, स्रोत.getText(), StandardCharsets.UTF_8);
            जोड़ें(लेबल("save") + ": " + संचिका + "\n");
            return true;
        } catch (Exception अपवाद) { त्रुटि(अपवाद); return false; }
    }

    private int निष्पादन(List<String> आदेश) throws Exception {
        प्रक्रिया = new ProcessBuilder(आदेश).directory(निर्देशिका.toFile()).redirectErrorStream(true).start();
        try (BufferedReader पाठक = new BufferedReader(new InputStreamReader(प्रक्रिया.getInputStream(), StandardCharsets.UTF_8))) {
            String पंक्ति;
            while ((पंक्ति = पाठक.readLine()) != null) जोड़ें(पंक्ति + "\n");
        }
        int परिणाम = प्रक्रिया.waitFor();
        प्रक्रिया = null;
        जोड़ें(लेबल("result") + ": " + परिणाम + "\n");
        return परिणाम;
    }

    private void संकलन(boolean चलाएँ) {
        if (!सहेजें()) return;
        String संचिका = निर्देशिका.resolve(पथ.getText()).toString();
        String वर्गनाम = नाम.getText().trim();
        String पाठ = तर्क.getText();
        कार्यसूत्र.submit(() -> {
            try {
                Files.createDirectories(निर्देशिका.resolve("classes"));
                int परिणाम = निष्पादन(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", निर्देशिका.resolve("classes").toString(), संचिका));
                if (चलाएँ && परिणाम == 0) {
                    List<String> आदेश = new ArrayList<>(Arrays.asList("java", "-cp", निर्देशिका.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", वर्गनाम));
                    StreamTokenizer विश्लेषक = new StreamTokenizer(new StringReader(पाठ));
                    विश्लेषक.resetSyntax(); विश्लेषक.wordChars(33, 65535); विश्लेषक.whitespaceChars(0, 32);
                    विश्लेषक.quoteChar('"'); विश्लेषक.quoteChar('\'');
                    while (विश्लेषक.nextToken() != StreamTokenizer.TT_EOF) आदेश.add(विश्लेषक.sval);
                    निष्पादन(आदेश);
                }
            } catch (Exception अपवाद) { त्रुटि(अपवाद); }
        });
    }

    private void रोकें() {
        Process वर्तमानप्रक्रिया = प्रक्रिया;
        if (वर्तमानप्रक्रिया != null) {
            वर्तमानप्रक्रिया.descendants().forEach(ProcessHandle::destroyForcibly);
            वर्तमानप्रक्रिया.destroyForcibly();
        }
    }

    private void आदेशपटल() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(निर्देशिका.toFile()).start(); }
        catch (Exception अपवाद) { त्रुटि(अपवाद); }
    }

    private void चुनें() {
        JFileChooser चयनक = new JFileChooser(निर्देशिका.toFile());
        if (चयनक.showOpenDialog(खिड़की) == JFileChooser.APPROVE_OPTION) {
            पथ.setText(चयनक.getSelectedFile().getAbsolutePath());
            लोडकरें();
        }
    }

    private void आरंभ() {
        try (Reader पाठक = new InputStreamReader(कार्यशाला.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            संदेश.load(पाठक);
            Files.createDirectories(निर्देशिका);
        } catch (Exception अपवाद) { throw new IllegalStateException(अपवाद); }
        खिड़की.setTitle(लेबल("workspace") + " · WorldOS " + लेबल("identity"));
        खिड़की.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        खिड़की.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent घटना) {
                रोकें(); कार्यसूत्र.shutdownNow(); System.exit(0);
            }
        });
        स्रोत.setFont(new Font("Monospaced", Font.PLAIN, 17));
        स्रोत.setTabSize(4);
        निर्गम.setFont(new Font("Monospaced", Font.PLAIN, 14));
        निर्गम.setEditable(false);
        JPanel पट्ट = new JPanel(new GridLayout(0, 1));
        JPanel संचिका = new JPanel(new FlowLayout(FlowLayout.LEADING));
        संचिका.add(new JLabel(लेबल("file"))); संचिका.add(पथ);
        पट्ट.add(संचिका);
        JPanel उपकरणपट्टी = new JPanel(new FlowLayout(FlowLayout.LEADING));
        बटन(उपकरणपट्टी, "open", () -> चुनें());
        बटन(उपकरणपट्टी, "save", () -> सहेजें());
        बटन(उपकरणपट्टी, "compile", () -> संकलन(false));
        बटन(उपकरणपट्टी, "run", () -> संकलन(true));
        बटन(उपकरणपट्टी, "stop", () -> रोकें());
        बटन(उपकरणपट्टी, "terminal", () -> आदेशपटल());
        पट्ट.add(उपकरणपट्टी);
        JPanel विन्यास = new JPanel(new FlowLayout(FlowLayout.LEADING));
        विन्यास.add(new JLabel(लेबल("class"))); विन्यास.add(नाम);
        विन्यास.add(new JLabel(लेबल("arguments"))); विन्यास.add(तर्क);
        पट्ट.add(विन्यास);
        JSplitPane विभाजन = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(स्रोत), new JScrollPane(निर्गम));
        विभाजन.setResizeWeight(0.72);
        खिड़की.add(पट्ट, BorderLayout.NORTH);
        खिड़की.add(विभाजन, BorderLayout.CENTER);
        पट्ट.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(लेबल("locale"))));
        विभाजन.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        स्रोत.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        निर्गम.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension आकार = Toolkit.getDefaultToolkit().getScreenSize();
        खिड़की.setSize(Math.min(1240, आकार.width - 40), Math.min(760, आकार.height - 60));
        खिड़की.setLocationRelativeTo(null);
        खिड़की.setVisible(true);
        लोडकरें();
        विभाजन.setDividerLocation(0.72);
        जोड़ें("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        जोड़ें(लेबल("help") + "\n");
    }

    public static void main(String[] तर्क) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new कार्यशाला().आरंभ());
    }
}
