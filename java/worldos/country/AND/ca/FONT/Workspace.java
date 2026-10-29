// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.AND.l_ca;
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
    private final JFrame Finestra = new JFrame();
    private final JTextArea FONT = new JTextArea();
    private final JTextArea Sortida = new JTextArea();
    private final JTextField Camí = new JTextField("FONT.java", 26);
    private final JTextField Nom = new JTextField("FONT", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Directori = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Procés;

    private String Etiqueta(String Clau) {
        return messages.getProperty(Clau, Clau);
    }

    private void append(String text) {
        SwingUtilities.invokeLater(() -> {
            Sortida.append(text);
            Sortida.setCaretPosition(Sortida.getDocument().getLength());
        });
    }

    private void s_ha_produït_un_error(Exception exception) {
        append(Etiqueta("error") + ": " + exception.toString() + "\n");
    }

    private void Botó(JPanel Quadre, String Clau, Runnable Acció) {
        JButton Botó = new JButton(Etiqueta(Clau));
        Botó.addActionListener(Esdeveniment -> Acció.run());
        Quadre.add(Botó);
    }

    private void Càrrega() {
        try {
            FONT.setText(Files.readString(Directori.resolve(Camí.getText()), StandardCharsets.UTF_8));
            FONT.setCaretPosition(0);
        } catch (Exception exception) { s_ha_produït_un_error(exception); }
    }

    private boolean Desa() {
        try {
            Path Fitxer = Directori.resolve(Camí.getText()).normalize();
            Files.createDirectories(Fitxer.getParent());
            Files.writeString(Fitxer, FONT.getText(), StandardCharsets.UTF_8);
            append(Etiqueta("save") + ": " + Fitxer + "\n");
            return true;
        } catch (Exception exception) { s_ha_produït_un_error(exception); return false; }
    }

    private int Executa(List<String> Ordre) throws Exception {
        Procés = new ProcessBuilder(Ordre).directory(Directori.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Procés.getInputStream(), StandardCharsets.UTF_8))) {
            String línia;
            while ((línia = reader.readLine()) != null) append(línia + "\n");
        }
        int RESULTAT = Procés.waitFor();
        Procés = null;
        append(Etiqueta("result") + ": " + RESULTAT + "\n");
        return RESULTAT;
    }

    private void compile(boolean Executa_2) {
        if (!Desa()) return;
        String Fitxer = Directori.resolve(Camí.getText()).toString();
        String Classe = Nom.getText().trim();
        String text = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Directori.resolve("classes"));
                int RESULTAT = Executa(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Directori.resolve("classes").toString(), Fitxer));
                if (Executa_2 && RESULTAT == 0) {
                    List<String> Ordre = new ArrayList<>(Arrays.asList("java", "-cp", Directori.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Classe));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(text));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Ordre.add(parser.sval);
                    Executa(Ordre);
                }
            } catch (Exception exception) { s_ha_produït_un_error(exception); }
        });
    }

    private void Atura() {
        Process Actual = Procés;
        if (Actual != null) {
            Actual.descendants().forEach(ProcessHandle::destroyForcibly);
            Actual.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Directori.toFile()).start(); }
        catch (Exception exception) { s_ha_produït_un_error(exception); }
    }

    private void escull() {
        JFileChooser chooser = new JFileChooser(Directori.toFile());
        if (chooser.showOpenDialog(Finestra) == JFileChooser.APPROVE_OPTION) {
            Camí.setText(chooser.getSelectedFile().getAbsolutePath());
            Càrrega();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Directori);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Finestra.setTitle(Etiqueta("workspace") + " · WorldOS " + Etiqueta("identity"));
        Finestra.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Finestra.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Esdeveniment) {
                Atura(); worker.shutdownNow(); System.exit(0);
            }
        });
        FONT.setFont(new Font("Monospaced", Font.PLAIN, 17));
        FONT.setTabSize(4);
        Sortida.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Sortida.setEditable(false);
        JPanel Quadre = new JPanel(new GridLayout(0, 1));
        JPanel Fitxer = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fitxer.add(new JLabel(Etiqueta("file"))); Fitxer.add(Camí);
        Quadre.add(Fitxer);
        JPanel Barra_d_eines = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Botó(Barra_d_eines, "open", () -> escull());
        Botó(Barra_d_eines, "save", () -> Desa());
        Botó(Barra_d_eines, "compile", () -> compile(false));
        Botó(Barra_d_eines, "run", () -> compile(true));
        Botó(Barra_d_eines, "stop", () -> Atura());
        Botó(Barra_d_eines, "terminal", () -> terminal());
        Quadre.add(Barra_d_eines);
        JPanel Ajusts = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Ajusts.add(new JLabel(Etiqueta("class"))); Ajusts.add(Nom);
        Ajusts.add(new JLabel(Etiqueta("arguments"))); Ajusts.add(arguments);
        Quadre.add(Ajusts);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(FONT), new JScrollPane(Sortida));
        split.setResizeWeight(0.72);
        Finestra.add(Quadre, BorderLayout.NORTH);
        Finestra.add(split, BorderLayout.CENTER);
        Quadre.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etiqueta("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        FONT.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Sortida.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Mida = Toolkit.getDefaultToolkit().getScreenSize();
        Finestra.setSize(Math.min(1240, Mida.width - 40), Math.min(760, Mida.height - 60));
        Finestra.setLocationRelativeTo(null);
        Finestra.setVisible(true);
        Càrrega();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Etiqueta("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
