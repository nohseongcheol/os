// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.자바;

import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.List;
import java.util.concurrent.*;
import javax.swing.*;
import javax.swing.plaf.FontUIResource;

/** spazio_utente 홈에서 Java 원문을 Modifica_VALORE·compilare_fonte·실행하는 작은 Swing area_di_lavoro. */
public final class area_di_lavoro {
    private final JFrame Finestra = new JFrame("jkoros — 자바 area_di_lavoro");
    private final JTextArea codiceSorgente = new JTextArea();
    private final JTextArea uscitaTesto = new JTextArea(8, 80);
    private final JTextField File_voce_nome = new JTextField("messaggio_di_saluto_ae353e94.java", 20);
    private final JTextField Corso_voce_nome = new JTextField("messaggio_di_saluto_ae353e94", 16);
    private final Path directory_di_lavoro = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService lavoratore_VALORE = Executors.newSingleThreadExecutor();
    private volatile Process Processi_VALORE;
    private final String Catalogo = "/opt/jkoros/lib/한국어자바.jar";

    private void informativa(String testo) { SwingUtilities.invokeLater(() -> uscitaTesto.append(testo + "\n")); }
    private void pulsante(JPanel versione_VALORE, String Nome, Runnable 행동) {
        JButton pulsante = new JButton(Nome);
        pulsante.addActionListener(Evento -> 행동.run());
        versione_VALORE.add(pulsante);
    }
    private boolean Store_VALORE() {
        try {
            Path percorso = directory_di_lavoro.resolve(File_voce_nome.getText());
            Files.createDirectories(percorso.getParent());
            file.Scrittura(percorso, codiceSorgente.getText());
            informativa("Store_VALORE: " + percorso);
            return true;
        } catch (Exception errore) { informativa(errore.toString()); return false; }
    }
    private void Apri() {
        try { codiceSorgente.setText(file.Lettura(directory_di_lavoro.resolve(File_voce_nome.getText()))); }
        catch (Exception errore) { informativa(errore.toString()); }
    }
    private int comando(List<String> comando) throws Exception {
        Processi_VALORE = new ProcessBuilder(comando).directory(directory_di_lavoro.toFile()).redirectErrorStream(true).start();
        try (BufferedReader riga_di_ingresso = new BufferedReader(new InputStreamReader(Processi_VALORE.getInputStream(), StandardCharsets.UTF_8))) {
            String testo;
            while ((testo = riga_di_ingresso.readLine()) != null) informativa(testo);
        }
        int Stato_VALORE = Processi_VALORE.waitFor(); Processi_VALORE = null;
        informativa("Esci_app CODICE_VALORE: " + Stato_VALORE);
        return Stato_VALORE;
    }
    private void TRADUCI_fonte(boolean Esegui_comando, boolean eseguibile) {
        if (!Store_VALORE()) return;
        String input_VALORE = File_voce_nome.getText(), punto_di_ingresso_VALORE = Corso_voce_nome.getText();
        lavoratore_VALORE.submit(() -> {
            try {
                Files.createDirectories(directory_di_lavoro.resolve("classes"));
                if (eseguibile) {
                    comando(Arrays.asList("jclassc", "--target", "openjdk", "--entry", punto_di_ingresso_VALORE,
                        "--classpath", Catalogo, "-o", "실행프로그램", input_VALORE));
                } else if (comando(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", Catalogo,
                        "-d", "classes", input_VALORE)) == 0 && Esegui_comando) {
                    comando(Arrays.asList("java", "-cp", "classes:" + Catalogo, punto_di_ingresso_VALORE));
                }
            } catch (Exception errore) { informativa(errore.toString()); }
        });
    }
    private void Pause_esecuzione() {
        Process Regolari_articolo = Processi_VALORE;
        if (Regolari_articolo != null) { Regolari_articolo.descendants().forEach(ProcessHandle::destroy); Regolari_articolo.destroy(); }
    }
    private area_di_lavoro() throws IOException {
        Files.createDirectories(directory_di_lavoro);
        Font tipo_di_carattere_VALORE = new Font("Monospaced", Font.PLAIN, 16);
        codiceSorgente.setFont(tipo_di_carattere_VALORE); uscitaTesto.setFont(tipo_di_carattere_VALORE); uscitaTesto.setEditable(false);
        codiceSorgente.setTabSize(4);
        codiceSorgente.setMargin(new Insets(10, 12, 10, 12));
        uscitaTesto.setMargin(new Insets(8, 12, 8, 12));
        codiceSorgente.setBackground(new Color(250, 251, 252));
        codiceSorgente.setForeground(new Color(32, 43, 58));
        JPanel comando_pannello = new JPanel();
        comando_pannello.add(new JLabel("file")); comando_pannello.add(File_voce_nome);
        comando_pannello.add(new JLabel("주 Corso_VALORE")); comando_pannello.add(Corso_voce_nome);
        pulsante(comando_pannello, "Apri", this::Apri); pulsante(comando_pannello, "Store_VALORE", this::Store_VALORE);
        pulsante(comando_pannello, "compilare_fonte", () -> TRADUCI_fonte(false, false));
        pulsante(comando_pannello, "Esegui_comando", () -> TRADUCI_fonte(true, false));
        pulsante(comando_pannello, "Esegui_comando file Crea_voce", () -> TRADUCI_fonte(false, true));
        pulsante(comando_pannello, "Pause_esecuzione", this::Pause_esecuzione);
        JSplitPane Divisione_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(codiceSorgente), new JScrollPane(uscitaTesto));
        Divisione_KR.setResizeWeight(0.75);
        Finestra.add(comando_pannello, BorderLayout.NORTH); Finestra.add(Divisione_KR, BorderLayout.CENTER);
        Finestra.setSize(1200, 750); Finestra.setLocationRelativeTo(null);
        Finestra.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Finestra.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Evento) { Pause_esecuzione(); lavoratore_VALORE.shutdownNow(); }
        });
        Apri(); Finestra.setVisible(true);
    }
    public static void main(String[] argomenti) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource tipo_di_carattere_predefinito = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object voce_VALORE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(voce_VALORE) instanceof Font) UIManager.put(voce_VALORE, tipo_di_carattere_predefinito);
                }
                new area_di_lavoro();
            } catch (Exception errore) { errore.printStackTrace(); }
        });
    }
}
