// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ISR.l_am;
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
    private final JTextArea ምንጭ = new JTextArea();
    private final JTextArea ውጤት = new JTextArea();
    private final JTextField መተላለፊያ = new JTextField("ምንጭ.java", 26);
    private final JTextField ስም = new JTextField("ምንጭ", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path ዳይሬክቶሪ = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process ሂደቶች;

    private String ምልክት(String ቁልፍ) {
        return messages.getProperty(ቁልፍ, ቁልፍ);
    }

    private void append(String ጽሁፍ) {
        SwingUtilities.invokeLater(() -> {
            ውጤት.append(ጽሁፍ);
            ውጤት.setCaretPosition(ውጤት.getDocument().getLength());
        });
    }

    private void ስህተት(Exception exception) {
        append(ምልክት("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel ፓነል, String ቁልፍ, Runnable ተግባር) {
        JButton button = new JButton(ምልክት(ቁልፍ));
        button.addActionListener(event -> ተግባር.run());
        ፓነል.add(button);
    }

    private void መጫኛ() {
        try {
            ምንጭ.setText(Files.readString(ዳይሬክቶሪ.resolve(መተላለፊያ.getText()), StandardCharsets.UTF_8));
            ምንጭ.setCaretPosition(0);
        } catch (Exception exception) { ስህተት(exception); }
    }

    private boolean ማስቀመጫ() {
        try {
            Path ፋይል = ዳይሬክቶሪ.resolve(መተላለፊያ.getText()).normalize();
            Files.createDirectories(ፋይል.getParent());
            Files.writeString(ፋይል, ምንጭ.getText(), StandardCharsets.UTF_8);
            append(ምልክት("save") + ": " + ፋይል + "\n");
            return true;
        } catch (Exception exception) { ስህተት(exception); return false; }
    }

    private int መፈጸሚያ(List<String> ትእዛዝ) throws Exception {
        ሂደቶች = new ProcessBuilder(ትእዛዝ).directory(ዳይሬክቶሪ.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(ሂደቶች.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = ሂደቶች.waitFor();
        ሂደቶች = null;
        append(ምልክት("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean ማስኬጃ) {
        if (!ማስቀመጫ()) return;
        String ፋይል = ዳይሬክቶሪ.resolve(መተላለፊያ.getText()).toString();
        String መደብ = ስም.getText().trim();
        String ጽሁፍ = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(ዳይሬክቶሪ.resolve("classes"));
                int result = መፈጸሚያ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", ዳይሬክቶሪ.resolve("classes").toString(), ፋይል));
                if (ማስኬጃ && result == 0) {
                    List<String> ትእዛዝ = new ArrayList<>(Arrays.asList("java", "-cp", ዳይሬክቶሪ.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", መደብ));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(ጽሁፍ));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) ትእዛዝ.add(parser.sval);
                    መፈጸሚያ(ትእዛዝ);
                }
            } catch (Exception exception) { ስህተት(exception); }
        });
    }

    private void ማስቆሚያ() {
        Process current = ሂደቶች;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void ተርሚናል() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(ዳይሬክቶሪ.toFile()).start(); }
        catch (Exception exception) { ስህተት(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(ዳይሬክቶሪ.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            መተላለፊያ.setText(chooser.getSelectedFile().getAbsolutePath());
            መጫኛ();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(ዳይሬክቶሪ);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(ምልክት("workspace") + " · WorldOS " + ምልክት("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                ማስቆሚያ(); worker.shutdownNow(); System.exit(0);
            }
        });
        ምንጭ.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ምንጭ.setTabSize(4);
        ውጤት.setFont(new Font("Monospaced", Font.PLAIN, 14));
        ውጤት.setEditable(false);
        JPanel ፓነል = new JPanel(new GridLayout(0, 1));
        JPanel ፋይል = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ፋይል.add(new JLabel(ምልክት("file"))); ፋይል.add(መተላለፊያ);
        ፓነል.add(ፋይል);
        JPanel እቃ_መደርደሪያ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(እቃ_መደርደሪያ, "open", () -> choose());
        button(እቃ_መደርደሪያ, "save", () -> ማስቀመጫ());
        button(እቃ_መደርደሪያ, "compile", () -> compile(false));
        button(እቃ_መደርደሪያ, "run", () -> compile(true));
        button(እቃ_መደርደሪያ, "stop", () -> ማስቆሚያ());
        button(እቃ_መደርደሪያ, "terminal", () -> ተርሚናል());
        ፓነል.add(እቃ_መደርደሪያ);
        JPanel ማሰናጃዎች = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ማሰናጃዎች.add(new JLabel(ምልክት("class"))); ማሰናጃዎች.add(ስም);
        ማሰናጃዎች.add(new JLabel(ምልክት("arguments"))); ማሰናጃዎች.add(arguments);
        ፓነል.add(ማሰናጃዎች);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ምንጭ), new JScrollPane(ውጤት));
        split.setResizeWeight(0.72);
        window.add(ፓነል, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        ፓነል.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(ምልክት("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ምንጭ.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        ውጤት.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension መጠን = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, መጠን.width - 40), Math.min(760, መጠን.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        መጫኛ();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(ምልክት("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
