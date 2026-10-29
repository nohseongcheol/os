// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.DEU.l_it;
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
public final class SpazioLavoro {
    private final JFrame Finestra = new JFrame();
    private final JTextArea codiceSorgente = new JTextArea();
    private final JTextArea uscitaTesto = new JTextArea();
    private final JTextField percorso = new JTextField("codiceSorgente.java", 26);
    private final JTextField Nome = new JTextField("codiceSorgente", 15);
    private final JTextField argomenti = new JTextField(25);
    private final Properties messaggi = new Properties();
    private final Path cartella = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService esecutoreAsincrono = Executors.newSingleThreadExecutor();
    private volatile Process Processi;

    private String Etichetta(String Chiave) {
        return messaggi.getProperty(Chiave, Chiave);
    }

    private void aggiungi_in_fondo_alla_lista(String testo) {
        SwingUtilities.invokeLater(() -> {
            uscitaTesto.append(testo);
            uscitaTesto.setCaretPosition(uscitaTesto.getDocument().getLength());
        });
    }

    private void errore(Exception exception) {
        aggiungi_in_fondo_alla_lista(Etichetta("error") + ": " + exception.toString() + "\n");
    }

    private void pulsante(JPanel Pannello, String Chiave, Runnable Azione) {
        JButton pulsante = new JButton(Etichetta(Chiave));
        pulsante.addActionListener(Evento -> Azione.run());
        Pannello.add(pulsante);
    }

    private void caricaSorgente() {
        try {
            codiceSorgente.setText(Files.readString(cartella.resolve(percorso.getText()), StandardCharsets.UTF_8));
            codiceSorgente.setCaretPosition(0);
        } catch (Exception exception) { errore(exception); }
    }

    private boolean Salva() {
        try {
            Path file = cartella.resolve(percorso.getText()).normalize();
            Files.createDirectories(file.getParent());
            Files.writeString(file, codiceSorgente.getText(), StandardCharsets.UTF_8);
            aggiungi_in_fondo_alla_lista(Etichetta("save") + ": " + file + "\n");
            return true;
        } catch (Exception exception) { errore(exception); return false; }
    }

    private int Esegui(List<String> comando) throws Exception {
        Processi = new ProcessBuilder(comando).directory(cartella.toFile()).redirectErrorStream(true).start();
        try (BufferedReader lettoreTesto = new BufferedReader(new InputStreamReader(Processi.getInputStream(), StandardCharsets.UTF_8))) {
            String riga_di_ingresso;
            while ((riga_di_ingresso = lettoreTesto.readLine()) != null) aggiungi_in_fondo_alla_lista(riga_di_ingresso + "\n");
        }
        int risultato = Processi.waitFor();
        Processi = null;
        aggiungi_in_fondo_alla_lista(Etichetta("result") + ": " + risultato + "\n");
        return risultato;
    }

    private void compila(boolean avvia) {
        if (!Salva()) return;
        String file = cartella.resolve(percorso.getText()).toString();
        String Classe = Nome.getText().trim();
        String testo = argomenti.getText();
        esecutoreAsincrono.submit(() -> {
            try {
                Files.createDirectories(cartella.resolve("classes"));
                int risultato = Esegui(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", cartella.resolve("classes").toString(), file));
                if (avvia && risultato == 0) {
                    List<String> comando = new ArrayList<>(Arrays.asList("java", "-cp", cartella.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Classe));
                    StreamTokenizer analizzatoreArgomenti = new StreamTokenizer(new StringReader(testo));
                    analizzatoreArgomenti.resetSyntax(); analizzatoreArgomenti.wordChars(33, 65535); analizzatoreArgomenti.whitespaceChars(0, 32);
                    analizzatoreArgomenti.quoteChar('"'); analizzatoreArgomenti.quoteChar('\'');
                    while (analizzatoreArgomenti.nextToken() != StreamTokenizer.TT_EOF) comando.add(analizzatoreArgomenti.sval);
                    Esegui(comando);
                }
            } catch (Exception exception) { errore(exception); }
        });
    }

    private void Ferma() {
        Process processoCorrente = Processi;
        if (processoCorrente != null) {
            processoCorrente.descendants().forEach(ProcessHandle::destroyForcibly);
            processoCorrente.destroyForcibly();
        }
    }

    private void terminale() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(cartella.toFile()).start(); }
        catch (Exception exception) { errore(exception); }
    }

    private void scelta() {
        JFileChooser chooser = new JFileChooser(cartella.toFile());
        if (chooser.showOpenDialog(Finestra) == JFileChooser.APPROVE_OPTION) {
            percorso.setText(chooser.getSelectedFile().getAbsolutePath());
            caricaSorgente();
        }
    }

    private void inizializza() {
        try (Reader lettoreTesto = new InputStreamReader(SpazioLavoro.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messaggi.load(lettoreTesto);
            Files.createDirectories(cartella);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Finestra.setTitle(Etichetta("workspace") + " · WorldOS " + Etichetta("identity"));
        Finestra.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Finestra.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Evento) {
                Ferma(); esecutoreAsincrono.shutdownNow(); System.exit(0);
            }
        });
        codiceSorgente.setFont(new Font("Monospaced", Font.PLAIN, 17));
        codiceSorgente.setTabSize(4);
        uscitaTesto.setFont(new Font("Monospaced", Font.PLAIN, 14));
        uscitaTesto.setEditable(false);
        JPanel Pannello = new JPanel(new GridLayout(0, 1));
        JPanel file = new JPanel(new FlowLayout(FlowLayout.LEADING));
        file.add(new JLabel(Etichetta("file"))); file.add(percorso);
        Pannello.add(file);
        JPanel Barra_degli_strumenti = new JPanel(new FlowLayout(FlowLayout.LEADING));
        pulsante(Barra_degli_strumenti, "open", () -> scelta());
        pulsante(Barra_degli_strumenti, "save", () -> Salva());
        pulsante(Barra_degli_strumenti, "compile", () -> compila(false));
        pulsante(Barra_degli_strumenti, "run", () -> compila(true));
        pulsante(Barra_degli_strumenti, "stop", () -> Ferma());
        pulsante(Barra_degli_strumenti, "terminal", () -> terminale());
        Pannello.add(Barra_degli_strumenti);
        JPanel Impostazioni = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Impostazioni.add(new JLabel(Etichetta("class"))); Impostazioni.add(Nome);
        Impostazioni.add(new JLabel(Etichetta("arguments"))); Impostazioni.add(argomenti);
        Pannello.add(Impostazioni);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(codiceSorgente), new JScrollPane(uscitaTesto));
        split.setResizeWeight(0.72);
        Finestra.add(Pannello, BorderLayout.NORTH);
        Finestra.add(split, BorderLayout.CENTER);
        Pannello.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etichetta("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        codiceSorgente.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        uscitaTesto.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Dimensione = Toolkit.getDefaultToolkit().getScreenSize();
        Finestra.setSize(Math.min(1240, Dimensione.width - 40), Math.min(760, Dimensione.height - 60));
        Finestra.setLocationRelativeTo(null);
        Finestra.setVisible(true);
        caricaSorgente();
        split.setDividerLocation(0.72);
        aggiungi_in_fondo_alla_lista("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        aggiungi_in_fondo_alla_lista(Etichetta("help") + "\n");
    }

    public static void main(String[] argomenti) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new SpazioLavoro().inizializza());
    }
}
