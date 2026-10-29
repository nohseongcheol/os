// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.자바;

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

/** käyttäjätila 홈에서 Java 원문을 muutos_ARVO·kääntää_lähde·실행하는 작은 Swing työtila. */
public final class työtila {
    private final JFrame Ikkuna = new JFrame("jkoros — 자바 työtila");
    private final JTextArea lähdetiedosto = new JTextArea();
    private final JTextArea tulostuspaikka = new JTextArea(8, 80);
    private final JTextField Tiedosto_merkintä_nimi = new JTextField("인사.java", 20);
    private final JTextField Luokka_merkintä_nimi = new JTextField("인사", 16);
    private final Path työhakemisto = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService työntekijä_ARVO = Executors.newSingleThreadExecutor();
    private volatile Process prosessi_ARVO;
    private final String kirjasto = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String teksti) { SwingUtilities.invokeLater(() -> tulostuspaikka.append(teksti + "\n")); }
    private void painike(JPanel versio_ARVO, String Nimi, Runnable 행동) {
        JButton painike = new JButton(Nimi);
        painike.addActionListener(Tapahtuma -> 행동.run());
        versio_ARVO.add(painike);
    }
    private boolean Store_ARVO() {
        try {
            Path polku_2 = työhakemisto.resolve(Tiedosto_merkintä_nimi.getText());
            Files.createDirectories(polku_2.getParent());
            tiedoston_nimi.Kirjoitus(polku_2, lähdetiedosto.getText());
            알림("Store_ARVO: " + polku_2);
            return true;
        } catch (Exception VIRHE) { 알림(VIRHE.toString()); return false; }
    }
    private void Avaa() {
        try { lähdetiedosto.setText(tiedoston_nimi.Luku(työhakemisto.resolve(Tiedosto_merkintä_nimi.getText()))); }
        catch (Exception VIRHE) { 알림(VIRHE.toString()); }
    }
    private int komento(List<String> komento) throws Exception {
        prosessi_ARVO = new ProcessBuilder(komento).directory(työhakemisto.toFile()).redirectErrorStream(true).start();
        try (BufferedReader syöterivi = new BufferedReader(new InputStreamReader(prosessi_ARVO.getInputStream(), StandardCharsets.UTF_8))) {
            String teksti;
            while ((teksti = syöterivi.readLine()) != null) 알림(teksti);
        }
        int Tila_ARVO = prosessi_ARVO.waitFor(); prosessi_ARVO = null;
        알림("Lopeta_ohjelma KOODI_ARVO: " + Tila_ARVO);
        return Tila_ARVO;
    }
    private void KÄÄNNÄ_lähde(boolean Suorita_komento, boolean suoritettava_tiedosto) {
        if (!Store_ARVO()) return;
        String syöte_ARVO = Tiedosto_merkintä_nimi.getText(), aloituskohta_ARVO = Luokka_merkintä_nimi.getText();
        työntekijä_ARVO.submit(() -> {
            try {
                Files.createDirectories(työhakemisto.resolve("classes"));
                if (suoritettava_tiedosto) {
                    komento(Arrays.asList("jclassc", "--target", "openjdk", "--entry", aloituskohta_ARVO,
                        "--classpath", kirjasto, "-o", "실행프로그램", syöte_ARVO));
                } else if (komento(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", kirjasto,
                        "-d", "classes", syöte_ARVO)) == 0 && Suorita_komento) {
                    komento(Arrays.asList("java", "-cp", "classes:" + kirjasto, aloituskohta_ARVO));
                }
            } catch (Exception VIRHE) { 알림(VIRHE.toString()); }
        });
    }
    private void Keskeytä_suoritus() {
        Process nykyinen_kohde = prosessi_ARVO;
        if (nykyinen_kohde != null) { nykyinen_kohde.descendants().forEach(ProcessHandle::destroy); nykyinen_kohde.destroy(); }
    }
    private työtila() throws IOException {
        Files.createDirectories(työhakemisto);
        Font fontti_ARVO = new Font("Monospaced", Font.PLAIN, 16);
        lähdetiedosto.setFont(fontti_ARVO); tulostuspaikka.setFont(fontti_ARVO); tulostuspaikka.setEditable(false);
        lähdetiedosto.setTabSize(4);
        lähdetiedosto.setMargin(new Insets(10, 12, 10, 12));
        tulostuspaikka.setMargin(new Insets(8, 12, 8, 12));
        lähdetiedosto.setBackground(new Color(250, 251, 252));
        lähdetiedosto.setForeground(new Color(32, 43, 58));
        JPanel komento_ruutu = new JPanel();
        komento_ruutu.add(new JLabel("tiedoston_nimi")); komento_ruutu.add(Tiedosto_merkintä_nimi);
        komento_ruutu.add(new JLabel("주 Luokka_ARVO")); komento_ruutu.add(Luokka_merkintä_nimi);
        painike(komento_ruutu, "Avaa", this::Avaa); painike(komento_ruutu, "Store_ARVO", this::Store_ARVO);
        painike(komento_ruutu, "kääntää_lähde", () -> KÄÄNNÄ_lähde(false, false));
        painike(komento_ruutu, "Suorita_komento", () -> KÄÄNNÄ_lähde(true, false));
        painike(komento_ruutu, "Suorita_komento tiedoston_nimi Luo_merkintä", () -> KÄÄNNÄ_lähde(false, true));
        painike(komento_ruutu, "Keskeytä_suoritus", this::Keskeytä_suoritus);
        JSplitPane jako_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(lähdetiedosto), new JScrollPane(tulostuspaikka));
        jako_KR.setResizeWeight(0.75);
        Ikkuna.add(komento_ruutu, BorderLayout.NORTH); Ikkuna.add(jako_KR, BorderLayout.CENTER);
        Ikkuna.setSize(1200, 750); Ikkuna.setLocationRelativeTo(null);
        Ikkuna.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Ikkuna.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Tapahtuma) { Keskeytä_suoritus(); työntekijä_ARVO.shutdownNow(); }
        });
        Avaa(); Ikkuna.setVisible(true);
    }
    public static void main(String[] argumentit) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource oletusfontti = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object merkintä_ARVO_962f286b : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(merkintä_ARVO_962f286b) instanceof Font) UIManager.put(merkintä_ARVO_962f286b, oletusfontti);
                }
                new työtila();
            } catch (Exception VIRHE) { VIRHE.printStackTrace(); }
        });
    }
}
