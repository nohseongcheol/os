// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.FRA.l_oc;
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
    private final JTextArea Sorga = new JTextArea();
    private final JTextArea Sortida = new JTextArea();
    private final JTextField CAMIN = new JTextField("Sorga.java", 26);
    private final JTextField Nom = new JTextField("Sorga", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Repertòri = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Processus;

    private String Etiqueta(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Tèxte) {
        SwingUtilities.invokeLater(() -> {
            Sortida.append(Tèxte);
            Sortida.setCaretPosition(Sortida.getDocument().getLength());
        });
    }

    private void error(Exception exception) {
        append(Etiqueta("error") + ": " + exception.toString() + "\n");
    }

    private void Boton(JPanel Panèl, String key, Runnable Accion) {
        JButton Boton = new JButton(Etiqueta(key));
        Boton.addActionListener(Eveniment -> Accion.run());
        Panèl.add(Boton);
    }

    private void Carga() {
        try {
            Sorga.setText(Files.readString(Repertòri.resolve(CAMIN.getText()), StandardCharsets.UTF_8));
            Sorga.setCaretPosition(0);
        } catch (Exception exception) { error(exception); }
    }

    private boolean Enregistrar() {
        try {
            Path Fichièr = Repertòri.resolve(CAMIN.getText()).normalize();
            Files.createDirectories(Fichièr.getParent());
            Files.writeString(Fichièr, Sorga.getText(), StandardCharsets.UTF_8);
            append(Etiqueta("save") + ": " + Fichièr + "\n");
            return true;
        } catch (Exception exception) { error(exception); return false; }
    }

    private int Executar(List<String> Comanda) throws Exception {
        Processus = new ProcessBuilder(Comanda).directory(Repertòri.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Processus.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = Processus.waitFor();
        Processus = null;
        append(Etiqueta("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Executar_2) {
        if (!Enregistrar()) return;
        String Fichièr = Repertòri.resolve(CAMIN.getText()).toString();
        String Classa = Nom.getText().trim();
        String Tèxte = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Repertòri.resolve("classes"));
                int result = Executar(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Repertòri.resolve("classes").toString(), Fichièr));
                if (Executar_2 && result == 0) {
                    List<String> Comanda = new ArrayList<>(Arrays.asList("java", "-cp", Repertòri.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Classa));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Tèxte));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Comanda.add(parser.sval);
                    Executar(Comanda);
                }
            } catch (Exception exception) { error(exception); }
        });
    }

    private void Arrêter() {
        Process Correnta = Processus;
        if (Correnta != null) {
            Correnta.descendants().forEach(ProcessHandle::destroyForcibly);
            Correnta.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Repertòri.toFile()).start(); }
        catch (Exception exception) { error(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Repertòri.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            CAMIN.setText(chooser.getSelectedFile().getAbsolutePath());
            Carga();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Repertòri);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Etiqueta("workspace") + " · WorldOS " + Etiqueta("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Eveniment) {
                Arrêter(); worker.shutdownNow(); System.exit(0);
            }
        });
        Sorga.setFont(new Font("Monospaced", Font.PLAIN, 17));
        Sorga.setTabSize(4);
        Sortida.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Sortida.setEditable(false);
        JPanel Panèl = new JPanel(new GridLayout(0, 1));
        JPanel Fichièr = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fichièr.add(new JLabel(Etiqueta("file"))); Fichièr.add(CAMIN);
        Panèl.add(Fichièr);
        JPanel Barra_d_espleches = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Boton(Barra_d_espleches, "open", () -> choose());
        Boton(Barra_d_espleches, "save", () -> Enregistrar());
        Boton(Barra_d_espleches, "compile", () -> compile(false));
        Boton(Barra_d_espleches, "run", () -> compile(true));
        Boton(Barra_d_espleches, "stop", () -> Arrêter());
        Boton(Barra_d_espleches, "terminal", () -> terminal());
        Panèl.add(Barra_d_espleches);
        JPanel Paramètres = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Paramètres.add(new JLabel(Etiqueta("class"))); Paramètres.add(Nom);
        Paramètres.add(new JLabel(Etiqueta("arguments"))); Paramètres.add(arguments);
        Panèl.add(Paramètres);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Sorga), new JScrollPane(Sortida));
        split.setResizeWeight(0.72);
        window.add(Panèl, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Panèl.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etiqueta("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        Sorga.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Sortida.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Talha = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Talha.width - 40), Math.min(760, Talha.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Carga();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Etiqueta("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
