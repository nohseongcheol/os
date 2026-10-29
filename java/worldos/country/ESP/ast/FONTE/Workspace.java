// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ESP.l_ast;
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
    private final JFrame Ventana = new JFrame();
    private final JTextArea FONTE = new JTextArea();
    private final JTextArea Salida = new JTextArea();
    private final JTextField Camín = new JTextField("FONTE.java", 26);
    private final JTextField Nome = new JTextField("FONTE", 15);
    private final JTextField Argumentu = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Direutoriu = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Procesu;

    private String Etiqueta(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Testu) {
        SwingUtilities.invokeLater(() -> {
            Salida.append(Testu);
            Salida.setCaretPosition(Salida.getDocument().getLength());
        });
    }

    private void Fallu(Exception exception) {
        append(Etiqueta("error") + ": " + exception.toString() + "\n");
    }

    private void Botón(JPanel panel, String key, Runnable Aición) {
        JButton Botón = new JButton(Etiqueta(key));
        Botón.addActionListener(Eventu -> Aición.run());
        panel.add(Botón);
    }

    private void Cargar() {
        try {
            FONTE.setText(Files.readString(Direutoriu.resolve(Camín.getText()), StandardCharsets.UTF_8));
            FONTE.setCaretPosition(0);
        } catch (Exception exception) { Fallu(exception); }
    }

    private boolean Guardar() {
        try {
            Path Ficheru = Direutoriu.resolve(Camín.getText()).normalize();
            Files.createDirectories(Ficheru.getParent());
            Files.writeString(Ficheru, FONTE.getText(), StandardCharsets.UTF_8);
            append(Etiqueta("save") + ": " + Ficheru + "\n");
            return true;
        } catch (Exception exception) { Fallu(exception); return false; }
    }

    private int Executar(List<String> Comandu) throws Exception {
        Procesu = new ProcessBuilder(Comandu).directory(Direutoriu.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Procesu.getInputStream(), StandardCharsets.UTF_8))) {
            String Llinia;
            while ((Llinia = reader.readLine()) != null) append(Llinia + "\n");
        }
        int result = Procesu.waitFor();
        Procesu = null;
        append(Etiqueta("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Executar_2) {
        if (!Guardar()) return;
        String Ficheru = Direutoriu.resolve(Camín.getText()).toString();
        String Clas = Nome.getText().trim();
        String Testu = Argumentu.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Direutoriu.resolve("classes"));
                int result = Executar(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Direutoriu.resolve("classes").toString(), Ficheru));
                if (Executar_2 && result == 0) {
                    List<String> Comandu = new ArrayList<>(Arrays.asList("java", "-cp", Direutoriu.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Clas));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Testu));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Comandu.add(parser.sval);
                    Executar(Comandu);
                }
            } catch (Exception exception) { Fallu(exception); }
        });
    }

    private void Parar() {
        Process D_anguaño = Procesu;
        if (D_anguaño != null) {
            D_anguaño.descendants().forEach(ProcessHandle::destroyForcibly);
            D_anguaño.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Direutoriu.toFile()).start(); }
        catch (Exception exception) { Fallu(exception); }
    }

    private void escoyer() {
        JFileChooser chooser = new JFileChooser(Direutoriu.toFile());
        if (chooser.showOpenDialog(Ventana) == JFileChooser.APPROVE_OPTION) {
            Camín.setText(chooser.getSelectedFile().getAbsolutePath());
            Cargar();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Direutoriu);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Ventana.setTitle(Etiqueta("workspace") + " · WorldOS " + Etiqueta("identity"));
        Ventana.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Ventana.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Eventu) {
                Parar(); worker.shutdownNow(); System.exit(0);
            }
        });
        FONTE.setFont(new Font("Monospaced", Font.PLAIN, 17));
        FONTE.setTabSize(4);
        Salida.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Salida.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Ficheru = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Ficheru.add(new JLabel(Etiqueta("file"))); Ficheru.add(Camín);
        panel.add(Ficheru);
        JPanel Barra_Ferramientes = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Botón(Barra_Ferramientes, "open", () -> escoyer());
        Botón(Barra_Ferramientes, "save", () -> Guardar());
        Botón(Barra_Ferramientes, "compile", () -> compile(false));
        Botón(Barra_Ferramientes, "run", () -> compile(true));
        Botón(Barra_Ferramientes, "stop", () -> Parar());
        Botón(Barra_Ferramientes, "terminal", () -> terminal());
        panel.add(Barra_Ferramientes);
        JPanel Axustes = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Axustes.add(new JLabel(Etiqueta("class"))); Axustes.add(Nome);
        Axustes.add(new JLabel(Etiqueta("arguments"))); Axustes.add(Argumentu);
        panel.add(Axustes);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(FONTE), new JScrollPane(Salida));
        split.setResizeWeight(0.72);
        Ventana.add(panel, BorderLayout.NORTH);
        Ventana.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etiqueta("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        FONTE.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Salida.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Tamañu = Toolkit.getDefaultToolkit().getScreenSize();
        Ventana.setSize(Math.min(1240, Tamañu.width - 40), Math.min(760, Tamañu.height - 60));
        Ventana.setLocationRelativeTo(null);
        Ventana.setVisible(true);
        Cargar();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Etiqueta("help") + "\n");
    }

    public static void main(String[] Argumentu) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
