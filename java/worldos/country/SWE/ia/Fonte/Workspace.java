// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.SWE.l_ia;
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
    private final JTextArea Fonte = new JTextArea();
    private final JTextArea Exito = new JTextArea();
    private final JTextField Percurso = new JTextField("Fonte.java", 26);
    private final JTextField Nomine = new JTextField("Fonte", 15);
    private final JTextField Argumentos = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Directorio = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String label(String Clave) {
        return messages.getProperty(Clave, Clave);
    }

    private void append(String texto) {
        SwingUtilities.invokeLater(() -> {
            Exito.append(texto);
            Exito.setCaretPosition(Exito.getDocument().getLength());
        });
    }

    private void error(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String Clave, Runnable action) {
        JButton button = new JButton(label(Clave));
        button.addActionListener(event -> action.run());
        panel.add(button);
    }

    private void load() {
        try {
            Fonte.setText(Files.readString(Directorio.resolve(Percurso.getText()), StandardCharsets.UTF_8));
            Fonte.setCaretPosition(0);
        } catch (Exception exception) { error(exception); }
    }

    private boolean save() {
        try {
            Path file = Directorio.resolve(Percurso.getText()).normalize();
            Files.createDirectories(file.getParent());
            Files.writeString(file, Fonte.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + file + "\n");
            return true;
        } catch (Exception exception) { error(exception); return false; }
    }

    private int Executa(List<String> Commando) throws Exception {
        process = new ProcessBuilder(Commando).directory(Directorio.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String rango;
            while ((rango = reader.readLine()) != null) append(rango + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(label("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Exeque) {
        if (!save()) return;
        String file = Directorio.resolve(Percurso.getText()).toString();
        String Classe = Nomine.getText().trim();
        String texto = Argumentos.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Directorio.resolve("classes"));
                int result = Executa(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Directorio.resolve("classes").toString(), file));
                if (Exeque && result == 0) {
                    List<String> Commando = new ArrayList<>(Arrays.asList("java", "-cp", Directorio.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Classe));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(texto));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Commando.add(parser.sval);
                    Executa(Commando);
                }
            } catch (Exception exception) { error(exception); }
        });
    }

    private void Stoppa() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Directorio.toFile()).start(); }
        catch (Exception exception) { error(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Directorio.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            Percurso.setText(chooser.getSelectedFile().getAbsolutePath());
            load();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Directorio);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(label("workspace") + " · WorldOS " + label("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Stoppa(); worker.shutdownNow(); System.exit(0);
            }
        });
        Fonte.setFont(new Font("Monospaced", Font.PLAIN, 17));
        Fonte.setTabSize(4);
        Exito.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Exito.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel file = new JPanel(new FlowLayout(FlowLayout.LEADING));
        file.add(new JLabel(label("file"))); file.add(Percurso);
        panel.add(file);
        JPanel Barra_de_Instrumento = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Barra_de_Instrumento, "open", () -> choose());
        button(Barra_de_Instrumento, "save", () -> save());
        button(Barra_de_Instrumento, "compile", () -> compile(false));
        button(Barra_de_Instrumento, "run", () -> compile(true));
        button(Barra_de_Instrumento, "stop", () -> Stoppa());
        button(Barra_de_Instrumento, "terminal", () -> terminal());
        panel.add(Barra_de_Instrumento);
        JPanel settings = new JPanel(new FlowLayout(FlowLayout.LEADING));
        settings.add(new JLabel(label("class"))); settings.add(Nomine);
        settings.add(new JLabel(label("arguments"))); settings.add(Argumentos);
        panel.add(settings);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Fonte), new JScrollPane(Exito));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(label("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        Fonte.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Exito.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Grandor = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Grandor.width - 40), Math.min(760, Grandor.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        load();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(label("help") + "\n");
    }

    public static void main(String[] Argumentos) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
