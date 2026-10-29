// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.PRT.l_gl;
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
    private final JFrame Xanela = new JFrame();
    private final JTextArea FONTE = new JTextArea();
    private final JTextArea Saída = new JTextArea();
    private final JTextField CAMIÑO = new JTextField("FONTE.java", 26);
    private final JTextField Nome = new JTextField("FONTE", 15);
    private final JTextField Argumentos = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Directorio = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Proceso;

    private String Etiqueta(String Chave) {
        return messages.getProperty(Chave, Chave);
    }

    private void append(String Texto) {
        SwingUtilities.invokeLater(() -> {
            Saída.append(Texto);
            Saída.setCaretPosition(Saída.getDocument().getLength());
        });
    }

    private void ERRO(Exception exception) {
        append(Etiqueta("error") + ": " + exception.toString() + "\n");
    }

    private void botón(JPanel panel, String Chave, Runnable Acción) {
        JButton botón = new JButton(Etiqueta(Chave));
        botón.addActionListener(Evento -> Acción.run());
        panel.add(botón);
    }

    private void Carga() {
        try {
            FONTE.setText(Files.readString(Directorio.resolve(CAMIÑO.getText()), StandardCharsets.UTF_8));
            FONTE.setCaretPosition(0);
        } catch (Exception exception) { ERRO(exception); }
    }

    private boolean Gardar() {
        try {
            Path Ficheiro = Directorio.resolve(CAMIÑO.getText()).normalize();
            Files.createDirectories(Ficheiro.getParent());
            Files.writeString(Ficheiro, FONTE.getText(), StandardCharsets.UTF_8);
            append(Etiqueta("save") + ": " + Ficheiro + "\n");
            return true;
        } catch (Exception exception) { ERRO(exception); return false; }
    }

    private int Executar(List<String> Orde) throws Exception {
        Proceso = new ProcessBuilder(Orde).directory(Directorio.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Proceso.getInputStream(), StandardCharsets.UTF_8))) {
            String Liña;
            while ((Liña = reader.readLine()) != null) append(Liña + "\n");
        }
        int RESULTANTE = Proceso.waitFor();
        Proceso = null;
        append(Etiqueta("result") + ": " + RESULTANTE + "\n");
        return RESULTANTE;
    }

    private void compile(boolean Executar_2) {
        if (!Gardar()) return;
        String Ficheiro = Directorio.resolve(CAMIÑO.getText()).toString();
        String Clase = Nome.getText().trim();
        String Texto = Argumentos.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Directorio.resolve("classes"));
                int RESULTANTE = Executar(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Directorio.resolve("classes").toString(), Ficheiro));
                if (Executar_2 && RESULTANTE == 0) {
                    List<String> Orde = new ArrayList<>(Arrays.asList("java", "-cp", Directorio.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Clase));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Texto));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Orde.add(parser.sval);
                    Executar(Orde);
                }
            } catch (Exception exception) { ERRO(exception); }
        });
    }

    private void Deter() {
        Process Actual = Proceso;
        if (Actual != null) {
            Actual.descendants().forEach(ProcessHandle::destroyForcibly);
            Actual.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Directorio.toFile()).start(); }
        catch (Exception exception) { ERRO(exception); }
    }

    private void escoller() {
        JFileChooser chooser = new JFileChooser(Directorio.toFile());
        if (chooser.showOpenDialog(Xanela) == JFileChooser.APPROVE_OPTION) {
            CAMIÑO.setText(chooser.getSelectedFile().getAbsolutePath());
            Carga();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Directorio);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Xanela.setTitle(Etiqueta("workspace") + " · WorldOS " + Etiqueta("identity"));
        Xanela.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Xanela.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Evento) {
                Deter(); worker.shutdownNow(); System.exit(0);
            }
        });
        FONTE.setFont(new Font("Monospaced", Font.PLAIN, 17));
        FONTE.setTabSize(4);
        Saída.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Saída.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Ficheiro = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Ficheiro.add(new JLabel(Etiqueta("file"))); Ficheiro.add(CAMIÑO);
        panel.add(Ficheiro);
        JPanel Barra_de_ferramentas = new JPanel(new FlowLayout(FlowLayout.LEADING));
        botón(Barra_de_ferramentas, "open", () -> escoller());
        botón(Barra_de_ferramentas, "save", () -> Gardar());
        botón(Barra_de_ferramentas, "compile", () -> compile(false));
        botón(Barra_de_ferramentas, "run", () -> compile(true));
        botón(Barra_de_ferramentas, "stop", () -> Deter());
        botón(Barra_de_ferramentas, "terminal", () -> terminal());
        panel.add(Barra_de_ferramentas);
        JPanel Configuración = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Configuración.add(new JLabel(Etiqueta("class"))); Configuración.add(Nome);
        Configuración.add(new JLabel(Etiqueta("arguments"))); Configuración.add(Argumentos);
        panel.add(Configuración);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(FONTE), new JScrollPane(Saída));
        split.setResizeWeight(0.72);
        Xanela.add(panel, BorderLayout.NORTH);
        Xanela.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etiqueta("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        FONTE.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Saída.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Tamaño = Toolkit.getDefaultToolkit().getScreenSize();
        Xanela.setSize(Math.min(1240, Tamaño.width - 40), Math.min(760, Tamaño.height - 60));
        Xanela.setLocationRelativeTo(null);
        Xanela.setVisible(true);
        Carga();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Etiqueta("help") + "\n");
    }

    public static void main(String[] Argumentos) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
