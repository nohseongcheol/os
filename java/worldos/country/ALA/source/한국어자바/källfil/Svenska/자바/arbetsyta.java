// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.자바;

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

/** användarutrymme 홈에서 Java 원문을 ändring_värde·kompilera_källa·실행하는 작은 Swing arbetsyta. */
public final class arbetsyta {
    private final JFrame Fönster = new JFrame("jkoros — 자바 arbetsyta");
    private final JTextArea källfil = new JTextArea();
    private final JTextArea utmatningsposition = new JTextArea(8, 80);
    private final JTextField fil_post_namn = new JTextField("인사.java", 20);
    private final JTextField Kurs_post_namn = new JTextField("인사", 16);
    private final Path arbetskatalog = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService arbete_värde = Executors.newSingleThreadExecutor();
    private volatile Process Process_värde;
    private final String bibliotek = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String text) { SwingUtilities.invokeLater(() -> utmatningsposition.append(text + "\n")); }
    private void knapp(JPanel version_värde, String Namn, Runnable 행동) {
        JButton knapp = new JButton(Namn);
        knapp.addActionListener(Händelse -> 행동.run());
        version_värde.add(knapp);
    }
    private boolean Store_värde() {
        try {
            Path sökväg_2 = arbetskatalog.resolve(fil_post_namn.getText());
            Files.createDirectories(sökväg_2.getParent());
            filnamn.Skriv(sökväg_2, källfil.getText());
            알림("Store_värde: " + sökväg_2);
            return true;
        } catch (Exception fel) { 알림(fel.toString()); return false; }
    }
    private void Öppna() {
        try { källfil.setText(filnamn.Läs(arbetskatalog.resolve(fil_post_namn.getText()))); }
        catch (Exception fel) { 알림(fel.toString()); }
    }
    private int kommando(List<String> kommando) throws Exception {
        Process_värde = new ProcessBuilder(kommando).directory(arbetskatalog.toFile()).redirectErrorStream(true).start();
        try (BufferedReader inmatningsrad = new BufferedReader(new InputStreamReader(Process_värde.getInputStream(), StandardCharsets.UTF_8))) {
            String text;
            while ((text = inmatningsrad.readLine()) != null) 알림(text);
        }
        int status_värde = Process_värde.waitFor(); Process_värde = null;
        알림("Utgång_app KOD_värde: " + status_värde);
        return status_värde;
    }
    private void ÖVERSÄTT_källa(boolean köra_kommando, boolean körbar_fil_fil) {
        if (!Store_värde()) return;
        String indata_värde = fil_post_namn.getText(), startpunkt_värde = Kurs_post_namn.getText();
        arbete_värde.submit(() -> {
            try {
                Files.createDirectories(arbetskatalog.resolve("classes"));
                if (körbar_fil_fil) {
                    kommando(Arrays.asList("jclassc", "--target", "openjdk", "--entry", startpunkt_värde,
                        "--classpath", bibliotek, "-o", "실행프로그램", indata_värde));
                } else if (kommando(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", bibliotek,
                        "-d", "classes", indata_värde)) == 0 && köra_kommando) {
                    kommando(Arrays.asList("java", "-cp", "classes:" + bibliotek, startpunkt_värde));
                }
            } catch (Exception fel) { 알림(fel.toString()); }
        });
    }
    private void Pausa_körning() {
        Process aktuellt_objekt = Process_värde;
        if (aktuellt_objekt != null) { aktuellt_objekt.descendants().forEach(ProcessHandle::destroy); aktuellt_objekt.destroy(); }
    }
    private arbetsyta() throws IOException {
        Files.createDirectories(arbetskatalog);
        Font teckensnitt_värde = new Font("Monospaced", Font.PLAIN, 16);
        källfil.setFont(teckensnitt_värde); utmatningsposition.setFont(teckensnitt_värde); utmatningsposition.setEditable(false);
        källfil.setTabSize(4);
        källfil.setMargin(new Insets(10, 12, 10, 12));
        utmatningsposition.setMargin(new Insets(8, 12, 8, 12));
        källfil.setBackground(new Color(250, 251, 252));
        källfil.setForeground(new Color(32, 43, 58));
        JPanel kommando_panel = new JPanel();
        kommando_panel.add(new JLabel("filnamn")); kommando_panel.add(fil_post_namn);
        kommando_panel.add(new JLabel("주 Kurs_värde")); kommando_panel.add(Kurs_post_namn);
        knapp(kommando_panel, "Öppna", this::Öppna); knapp(kommando_panel, "Store_värde", this::Store_värde);
        knapp(kommando_panel, "kompilera_källa", () -> ÖVERSÄTT_källa(false, false));
        knapp(kommando_panel, "köra_kommando", () -> ÖVERSÄTT_källa(true, false));
        knapp(kommando_panel, "köra_kommando filnamn Skapa_post", () -> ÖVERSÄTT_källa(false, true));
        knapp(kommando_panel, "Pausa_körning", this::Pausa_körning);
        JSplitPane Division_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(källfil), new JScrollPane(utmatningsposition));
        Division_KR.setResizeWeight(0.75);
        Fönster.add(kommando_panel, BorderLayout.NORTH); Fönster.add(Division_KR, BorderLayout.CENTER);
        Fönster.setSize(1200, 750); Fönster.setLocationRelativeTo(null);
        Fönster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Fönster.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Händelse) { Pausa_körning(); arbete_värde.shutdownNow(); }
        });
        Öppna(); Fönster.setVisible(true);
    }
    public static void main(String[] argument) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource standardteckensnitt = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object post_värde : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(post_värde) instanceof Font) UIManager.put(post_värde, standardteckensnitt);
                }
                new arbetsyta();
            } catch (Exception fel) { fel.printStackTrace(); }
        });
    }
}
