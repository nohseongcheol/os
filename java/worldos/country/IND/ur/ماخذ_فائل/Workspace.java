// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_ur;
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
    private final JFrame ونڈو = new JFrame();
    private final JTextArea ماخذ_فائل = new JTextArea();
    private final JTextArea اخراج_کا_مقام = new JTextArea();
    private final JTextField راستہ_2 = new JTextField("ماخذ_فائل.java", 26);
    private final JTextField نام = new JTextField("ماخذ_فائل", 15);
    private final JTextField دلائل = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path راستہ = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process عمل_کاری;

    private String سرنامہ(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String متن) {
        SwingUtilities.invokeLater(() -> {
            اخراج_کا_مقام.append(متن);
            اخراج_کا_مقام.setCaretPosition(اخراج_کا_مقام.getDocument().getLength());
        });
    }

    private void غلطی(Exception exception) {
        append(سرنامہ("error") + ": " + exception.toString() + "\n");
    }

    private void بٹن(JPanel پینل, String key, Runnable عمل) {
        JButton بٹن = new JButton(سرنامہ(key));
        بٹن.addActionListener(واقعہ -> عمل.run());
        پینل.add(بٹن);
    }

    private void بوجھ() {
        try {
            ماخذ_فائل.setText(Files.readString(راستہ.resolve(راستہ_2.getText()), StandardCharsets.UTF_8));
            ماخذ_فائل.setCaretPosition(0);
        } catch (Exception exception) { غلطی(exception); }
    }

    private boolean محفوظ_کریں() {
        try {
            Path فائل_کا_نام = راستہ.resolve(راستہ_2.getText()).normalize();
            Files.createDirectories(فائل_کا_نام.getParent());
            Files.writeString(فائل_کا_نام, ماخذ_فائل.getText(), StandardCharsets.UTF_8);
            append(سرنامہ("save") + ": " + فائل_کا_نام + "\n");
            return true;
        } catch (Exception exception) { غلطی(exception); return false; }
    }

    private int اطلاق(List<String> حکم) throws Exception {
        عمل_کاری = new ProcessBuilder(حکم).directory(راستہ.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(عمل_کاری.getInputStream(), StandardCharsets.UTF_8))) {
            String اندراج_کی_سطر;
            while ((اندراج_کی_سطر = reader.readLine()) != null) append(اندراج_کی_سطر + "\n");
        }
        int result = عمل_کاری.waitFor();
        عمل_کاری = null;
        append(سرنامہ("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean چلائیں) {
        if (!محفوظ_کریں()) return;
        String فائل_کا_نام = راستہ.resolve(راستہ_2.getText()).toString();
        String className = نام.getText().trim();
        String متن = دلائل.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(راستہ.resolve("classes"));
                int result = اطلاق(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", راستہ.resolve("classes").toString(), فائل_کا_نام));
                if (چلائیں && result == 0) {
                    List<String> حکم = new ArrayList<>(Arrays.asList("java", "-cp", راستہ.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(متن));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) حکم.add(parser.sval);
                    اطلاق(حکم);
                }
            } catch (Exception exception) { غلطی(exception); }
        });
    }

    private void روکیں() {
        Process موجودہ_مقام = عمل_کاری;
        if (موجودہ_مقام != null) {
            موجودہ_مقام.descendants().forEach(ProcessHandle::destroyForcibly);
            موجودہ_مقام.destroyForcibly();
        }
    }

    private void حکم_کی_تشریح_کرنے_والا() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(راستہ.toFile()).start(); }
        catch (Exception exception) { غلطی(exception); }
    }

    private void منتخب_کریں() {
        JFileChooser chooser = new JFileChooser(راستہ.toFile());
        if (chooser.showOpenDialog(ونڈو) == JFileChooser.APPROVE_OPTION) {
            راستہ_2.setText(chooser.getSelectedFile().getAbsolutePath());
            بوجھ();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(راستہ);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        ونڈو.setTitle(سرنامہ("workspace") + " · WorldOS " + سرنامہ("identity"));
        ونڈو.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ونڈو.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent واقعہ) {
                روکیں(); worker.shutdownNow(); System.exit(0);
            }
        });
        ماخذ_فائل.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ماخذ_فائل.setTabSize(4);
        اخراج_کا_مقام.setFont(new Font("Monospaced", Font.PLAIN, 14));
        اخراج_کا_مقام.setEditable(false);
        JPanel پینل = new JPanel(new GridLayout(0, 1));
        JPanel فائل_کا_نام = new JPanel(new FlowLayout(FlowLayout.LEADING));
        فائل_کا_نام.add(new JLabel(سرنامہ("file"))); فائل_کا_نام.add(راستہ_2);
        پینل.add(فائل_کا_نام);
        JPanel اوزار_پٹی = new JPanel(new FlowLayout(FlowLayout.LEADING));
        بٹن(اوزار_پٹی, "open", () -> منتخب_کریں());
        بٹن(اوزار_پٹی, "save", () -> محفوظ_کریں());
        بٹن(اوزار_پٹی, "compile", () -> compile(false));
        بٹن(اوزار_پٹی, "run", () -> compile(true));
        بٹن(اوزار_پٹی, "stop", () -> روکیں());
        بٹن(اوزار_پٹی, "terminal", () -> حکم_کی_تشریح_کرنے_والا());
        پینل.add(اوزار_پٹی);
        JPanel ترتیبات = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ترتیبات.add(new JLabel(سرنامہ("class"))); ترتیبات.add(نام);
        ترتیبات.add(new JLabel(سرنامہ("arguments"))); ترتیبات.add(دلائل);
        پینل.add(ترتیبات);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ماخذ_فائل), new JScrollPane(اخراج_کا_مقام));
        split.setResizeWeight(0.72);
        ونڈو.add(پینل, BorderLayout.NORTH);
        ونڈو.add(split, BorderLayout.CENTER);
        پینل.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(سرنامہ("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ماخذ_فائل.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        اخراج_کا_مقام.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension حجم = Toolkit.getDefaultToolkit().getScreenSize();
        ونڈو.setSize(Math.min(1240, حجم.width - 40), Math.min(760, حجم.height - 60));
        ونڈو.setLocationRelativeTo(null);
        ونڈو.setVisible(true);
        بوجھ();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(سرنامہ("help") + "\n");
    }

    public static void main(String[] دلائل) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
