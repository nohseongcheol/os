// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.GEO.l_ka;
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
    private final JTextArea წყარო = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField გეზი = new JTextField("წყარო.java", 26);
    private final JTextField სახელი = new JTextField("წყარო", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path დასტა = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process პროცესი;

    private String სათაური(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String ტექსტი) {
        SwingUtilities.invokeLater(() -> {
            output.append(ტექსტი);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void შეცდომა(Exception exception) {
        append(სათაური("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel პანელი, String key, Runnable ქმედება) {
        JButton button = new JButton(სათაური(key));
        button.addActionListener(event -> ქმედება.run());
        პანელი.add(button);
    }

    private void ჩატვირთვა() {
        try {
            წყარო.setText(Files.readString(დასტა.resolve(გეზი.getText()), StandardCharsets.UTF_8));
            წყარო.setCaretPosition(0);
        } catch (Exception exception) { შეცდომა(exception); }
    }

    private boolean შეინახე() {
        try {
            Path ფაილი = დასტა.resolve(გეზი.getText()).normalize();
            Files.createDirectories(ფაილი.getParent());
            Files.writeString(ფაილი, წყარო.getText(), StandardCharsets.UTF_8);
            append(სათაური("save") + ": " + ფაილი + "\n");
            return true;
        } catch (Exception exception) { შეცდომა(exception); return false; }
    }

    private int შესრულება(List<String> ბრძანება) throws Exception {
        პროცესი = new ProcessBuilder(ბრძანება).directory(დასტა.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(პროცესი.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = პროცესი.waitFor();
        პროცესი = null;
        append(სათაური("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean გაშვება) {
        if (!შეინახე()) return;
        String ფაილი = დასტა.resolve(გეზი.getText()).toString();
        String კლასი = სახელი.getText().trim();
        String ტექსტი = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(დასტა.resolve("classes"));
                int result = შესრულება(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", დასტა.resolve("classes").toString(), ფაილი));
                if (გაშვება && result == 0) {
                    List<String> ბრძანება = new ArrayList<>(Arrays.asList("java", "-cp", დასტა.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", კლასი));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(ტექსტი));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) ბრძანება.add(parser.sval);
                    შესრულება(ბრძანება);
                }
            } catch (Exception exception) { შეცდომა(exception); }
        });
    }

    private void შეჩერება() {
        Process current = პროცესი;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void ტერმინალი() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(დასტა.toFile()).start(); }
        catch (Exception exception) { შეცდომა(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(დასტა.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            გეზი.setText(chooser.getSelectedFile().getAbsolutePath());
            ჩატვირთვა();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(დასტა);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(სათაური("workspace") + " · WorldOS " + სათაური("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                შეჩერება(); worker.shutdownNow(); System.exit(0);
            }
        });
        წყარო.setFont(new Font("Monospaced", Font.PLAIN, 17));
        წყარო.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel პანელი = new JPanel(new GridLayout(0, 1));
        JPanel ფაილი = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ფაილი.add(new JLabel(სათაური("file"))); ფაილი.add(გეზი);
        პანელი.add(ფაილი);
        JPanel ხელსაწყოთა_ველი = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(ხელსაწყოთა_ველი, "open", () -> choose());
        button(ხელსაწყოთა_ველი, "save", () -> შეინახე());
        button(ხელსაწყოთა_ველი, "compile", () -> compile(false));
        button(ხელსაწყოთა_ველი, "run", () -> compile(true));
        button(ხელსაწყოთა_ველი, "stop", () -> შეჩერება());
        button(ხელსაწყოთა_ველი, "terminal", () -> ტერმინალი());
        პანელი.add(ხელსაწყოთა_ველი);
        JPanel პარამეტრები = new JPanel(new FlowLayout(FlowLayout.LEADING));
        პარამეტრები.add(new JLabel(სათაური("class"))); პარამეტრები.add(სახელი);
        პარამეტრები.add(new JLabel(სათაური("arguments"))); პარამეტრები.add(arguments);
        პანელი.add(პარამეტრები);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(წყარო), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(პანელი, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        პანელი.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(სათაური("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        წყარო.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension ზომა = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, ზომა.width - 40), Math.min(760, ზომა.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        ჩატვირთვა();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(სათაური("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
