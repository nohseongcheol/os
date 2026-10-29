// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.DNK.l_sv;
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
    private final JFrame Fönster = new JFrame();
    private final JTextArea källfil = new JTextArea();
    private final JTextArea utmatningsposition = new JTextArea();
    private final JTextField sökväg_2 = new JTextField("källfil.java", 26);
    private final JTextField Namn = new JTextField("källfil", 15);
    private final JTextField argument = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path sökväg = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String Etikett(String Nyckel) {
        return messages.getProperty(Nyckel, Nyckel);
    }

    private void lägg_till_sist_i_listan(String text) {
        SwingUtilities.invokeLater(() -> {
            utmatningsposition.append(text);
            utmatningsposition.setCaretPosition(utmatningsposition.getDocument().getLength());
        });
    }

    private void fel(Exception exception) {
        lägg_till_sist_i_listan(Etikett("error") + ": " + exception.toString() + "\n");
    }

    private void knapp(JPanel panel, String Nyckel, Runnable Åtgärd) {
        JButton knapp = new JButton(Etikett(Nyckel));
        knapp.addActionListener(Händelse -> Åtgärd.run());
        panel.add(knapp);
    }

    private void Belastning() {
        try {
            källfil.setText(Files.readString(sökväg.resolve(sökväg_2.getText()), StandardCharsets.UTF_8));
            källfil.setCaretPosition(0);
        } catch (Exception exception) { fel(exception); }
    }

    private boolean Spara() {
        try {
            Path filnamn = sökväg.resolve(sökväg_2.getText()).normalize();
            Files.createDirectories(filnamn.getParent());
            Files.writeString(filnamn, källfil.getText(), StandardCharsets.UTF_8);
            lägg_till_sist_i_listan(Etikett("save") + ": " + filnamn + "\n");
            return true;
        } catch (Exception exception) { fel(exception); return false; }
    }

    private int Starta(List<String> kommando) throws Exception {
        process = new ProcessBuilder(kommando).directory(sökväg.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String inmatningsrad;
            while ((inmatningsrad = reader.readLine()) != null) lägg_till_sist_i_listan(inmatningsrad + "\n");
        }
        int RESULTAT = process.waitFor();
        process = null;
        lägg_till_sist_i_listan(Etikett("result") + ": " + RESULTAT + "\n");
        return RESULTAT;
    }

    private void compile(boolean Kör) {
        if (!Spara()) return;
        String filnamn = sökväg.resolve(sökväg_2.getText()).toString();
        String Klass = Namn.getText().trim();
        String text = argument.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(sökväg.resolve("classes"));
                int RESULTAT = Starta(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", sökväg.resolve("classes").toString(), filnamn));
                if (Kör && RESULTAT == 0) {
                    List<String> kommando = new ArrayList<>(Arrays.asList("java", "-cp", sökväg.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klass));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(text));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) kommando.add(parser.sval);
                    Starta(kommando);
                }
            } catch (Exception exception) { fel(exception); }
        });
    }

    private void Stopp() {
        Process aktuell_position = process;
        if (aktuell_position != null) {
            aktuell_position.descendants().forEach(ProcessHandle::destroyForcibly);
            aktuell_position.destroyForcibly();
        }
    }

    private void kommandotolk() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(sökväg.toFile()).start(); }
        catch (Exception exception) { fel(exception); }
    }

    private void välj() {
        JFileChooser chooser = new JFileChooser(sökväg.toFile());
        if (chooser.showOpenDialog(Fönster) == JFileChooser.APPROVE_OPTION) {
            sökväg_2.setText(chooser.getSelectedFile().getAbsolutePath());
            Belastning();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(sökväg);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Fönster.setTitle(Etikett("workspace") + " · WorldOS " + Etikett("identity"));
        Fönster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Fönster.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Händelse) {
                Stopp(); worker.shutdownNow(); System.exit(0);
            }
        });
        källfil.setFont(new Font("Monospaced", Font.PLAIN, 17));
        källfil.setTabSize(4);
        utmatningsposition.setFont(new Font("Monospaced", Font.PLAIN, 14));
        utmatningsposition.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel filnamn = new JPanel(new FlowLayout(FlowLayout.LEADING));
        filnamn.add(new JLabel(Etikett("file"))); filnamn.add(sökväg_2);
        panel.add(filnamn);
        JPanel Verktygsrad = new JPanel(new FlowLayout(FlowLayout.LEADING));
        knapp(Verktygsrad, "open", () -> välj());
        knapp(Verktygsrad, "save", () -> Spara());
        knapp(Verktygsrad, "compile", () -> compile(false));
        knapp(Verktygsrad, "run", () -> compile(true));
        knapp(Verktygsrad, "stop", () -> Stopp());
        knapp(Verktygsrad, "terminal", () -> kommandotolk());
        panel.add(Verktygsrad);
        JPanel Inställningar = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Inställningar.add(new JLabel(Etikett("class"))); Inställningar.add(Namn);
        Inställningar.add(new JLabel(Etikett("arguments"))); Inställningar.add(argument);
        panel.add(Inställningar);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(källfil), new JScrollPane(utmatningsposition));
        split.setResizeWeight(0.72);
        Fönster.add(panel, BorderLayout.NORTH);
        Fönster.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etikett("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        källfil.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        utmatningsposition.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Storlek = Toolkit.getDefaultToolkit().getScreenSize();
        Fönster.setSize(Math.min(1240, Storlek.width - 40), Math.min(760, Storlek.height - 60));
        Fönster.setLocationRelativeTo(null);
        Fönster.setVisible(true);
        Belastning();
        split.setDividerLocation(0.72);
        lägg_till_sist_i_listan("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        lägg_till_sist_i_listan(Etikett("help") + "\n");
    }

    public static void main(String[] argument) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
