// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.CAN.l_gu;
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
    private final JTextArea સ્રોત = new JTextArea();
    private final JTextArea આઉટપુટ = new JTextArea();
    private final JTextField પથ = new JTextField("સ્રોત.java", 26);
    private final JTextField નામ = new JTextField("સ્રોત", 15);
    private final JTextField દલીલો = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path ડિરેક્ટરી = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process પ્રક્રિયા;

    private String લેબલ(String કી) {
        return messages.getProperty(કી, કી);
    }

    private void append(String લખાણ) {
        SwingUtilities.invokeLater(() -> {
            આઉટપુટ.append(લખાણ);
            આઉટપુટ.setCaretPosition(આઉટપુટ.getDocument().getLength());
        });
    }

    private void ભૂલ(Exception exception) {
        append(લેબલ("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel પેનલ, String કી, Runnable ક્રિયા) {
        JButton button = new JButton(લેબલ(કી));
        button.addActionListener(event -> ક્રિયા.run());
        પેનલ.add(button);
    }

    private void લાવો() {
        try {
            સ્રોત.setText(Files.readString(ડિરેક્ટરી.resolve(પથ.getText()), StandardCharsets.UTF_8));
            સ્રોત.setCaretPosition(0);
        } catch (Exception exception) { ભૂલ(exception); }
    }

    private boolean સંગ્રહ_કરો() {
        try {
            Path ફાઈલ = ડિરેક્ટરી.resolve(પથ.getText()).normalize();
            Files.createDirectories(ફાઈલ.getParent());
            Files.writeString(ફાઈલ, સ્રોત.getText(), StandardCharsets.UTF_8);
            append(લેબલ("save") + ": " + ફાઈલ + "\n");
            return true;
        } catch (Exception exception) { ભૂલ(exception); return false; }
    }

    private int ચલાવો(List<String> આદેશ) throws Exception {
        પ્રક્રિયા = new ProcessBuilder(આદેશ).directory(ડિરેક્ટરી.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(પ્રક્રિયા.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = પ્રક્રિયા.waitFor();
        પ્રક્રિયા = null;
        append(લેબલ("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean ચલાવો_2) {
        if (!સંગ્રહ_કરો()) return;
        String ફાઈલ = ડિરેક્ટરી.resolve(પથ.getText()).toString();
        String વર્ગ = નામ.getText().trim();
        String લખાણ = દલીલો.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(ડિરેક્ટરી.resolve("classes"));
                int result = ચલાવો(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", ડિરેક્ટરી.resolve("classes").toString(), ફાઈલ));
                if (ચલાવો_2 && result == 0) {
                    List<String> આદેશ = new ArrayList<>(Arrays.asList("java", "-cp", ડિરેક્ટરી.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", વર્ગ));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(લખાણ));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) આદેશ.add(parser.sval);
                    ચલાવો(આદેશ);
                }
            } catch (Exception exception) { ભૂલ(exception); }
        });
    }

    private void અટકાવો() {
        Process current = પ્રક્રિયા;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void ટર્મિનલ() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(ડિરેક્ટરી.toFile()).start(); }
        catch (Exception exception) { ભૂલ(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(ડિરેક્ટરી.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            પથ.setText(chooser.getSelectedFile().getAbsolutePath());
            લાવો();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(ડિરેક્ટરી);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(લેબલ("workspace") + " · WorldOS " + લેબલ("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                અટકાવો(); worker.shutdownNow(); System.exit(0);
            }
        });
        સ્રોત.setFont(new Font("Monospaced", Font.PLAIN, 17));
        સ્રોત.setTabSize(4);
        આઉટપુટ.setFont(new Font("Monospaced", Font.PLAIN, 14));
        આઉટપુટ.setEditable(false);
        JPanel પેનલ = new JPanel(new GridLayout(0, 1));
        JPanel ફાઈલ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ફાઈલ.add(new JLabel(લેબલ("file"))); ફાઈલ.add(પથ);
        પેનલ.add(ફાઈલ);
        JPanel સાધનપટ્ટી = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(સાધનપટ્ટી, "open", () -> choose());
        button(સાધનપટ્ટી, "save", () -> સંગ્રહ_કરો());
        button(સાધનપટ્ટી, "compile", () -> compile(false));
        button(સાધનપટ્ટી, "run", () -> compile(true));
        button(સાધનપટ્ટી, "stop", () -> અટકાવો());
        button(સાધનપટ્ટી, "terminal", () -> ટર્મિનલ());
        પેનલ.add(સાધનપટ્ટી);
        JPanel સુયોજના = new JPanel(new FlowLayout(FlowLayout.LEADING));
        સુયોજના.add(new JLabel(લેબલ("class"))); સુયોજના.add(નામ);
        સુયોજના.add(new JLabel(લેબલ("arguments"))); સુયોજના.add(દલીલો);
        પેનલ.add(સુયોજના);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(સ્રોત), new JScrollPane(આઉટપુટ));
        split.setResizeWeight(0.72);
        window.add(પેનલ, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        પેનલ.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(લેબલ("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        સ્રોત.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        આઉટપુટ.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension માપ = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, માપ.width - 40), Math.min(760, માપ.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        લાવો();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(લેબલ("help") + "\n");
    }

    public static void main(String[] દલીલો) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
