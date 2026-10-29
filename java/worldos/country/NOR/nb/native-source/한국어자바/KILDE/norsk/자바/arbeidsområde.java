// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.자바;

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

/** bruker 홈에서 Java 원문을 Rediger_VERDI·kompilere_kilde·실행하는 작은 Swing arbeidsområde. */
public final class arbeidsområde {
    private final JFrame Vindu = new JFrame("jkoros — 자바 arbeidsområde");
    private final JTextArea KILDE = new JTextArea();
    private final JTextArea Utgang = new JTextArea(8, 80);
    private final JTextField Fil_oppføring_navn = new JTextField("인사.java", 20);
    private final JTextField time_oppføring_navn = new JTextField("인사", 16);
    private final Path arbeidsmappe = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService arbeider_VERDI = Executors.newSingleThreadExecutor();
    private volatile Process Prosess_VERDI;
    private final String bibliotek = "/opt/jkoros/lib/한국어자바.jar";

    private void notice(String Tekst) { SwingUtilities.invokeLater(() -> Utgang.append(Tekst + "\n")); }
    private void Knapp(JPanel versjon_VERDI, String Navn, Runnable 행동) {
        JButton Knapp = new JButton(Navn);
        Knapp.addActionListener(Hendelse -> 행동.run());
        versjon_VERDI.add(Knapp);
    }
    private boolean Store_VERDI() {
        try {
            Path Sti = arbeidsmappe.resolve(Fil_oppføring_navn.getText());
            Files.createDirectories(Sti.getParent());
            Fil.Skriv(Sti, KILDE.getText());
            notice("Store_VERDI: " + Sti);
            return true;
        } catch (Exception feil) { notice(feil.toString()); return false; }
    }
    private void Åpne() {
        try { KILDE.setText(Fil.Les(arbeidsmappe.resolve(Fil_oppføring_navn.getText()))); }
        catch (Exception feil) { notice(feil.toString()); }
    }
    private int Kommando(List<String> Kommando) throws Exception {
        Prosess_VERDI = new ProcessBuilder(Kommando).directory(arbeidsmappe.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Linje = new BufferedReader(new InputStreamReader(Prosess_VERDI.getInputStream(), StandardCharsets.UTF_8))) {
            String Tekst;
            while ((Tekst = Linje.readLine()) != null) notice(Tekst);
        }
        int status_VERDI = Prosess_VERDI.waitFor(); Prosess_VERDI = null;
        notice("Utgang_app KODE_VERDI: " + status_VERDI);
        return status_VERDI;
    }
    private void OVERSETT_kilde(boolean Utfør_kommando, boolean kjørbar_fil) {
        if (!Store_VERDI()) return;
        String inndata_VERDI = Fil_oppføring_navn.getText(), inngangspunkt_VERDI = time_oppføring_navn.getText();
        arbeider_VERDI.submit(() -> {
            try {
                Files.createDirectories(arbeidsmappe.resolve("classes"));
                if (kjørbar_fil) {
                    Kommando(Arrays.asList("jclassc", "--target", "openjdk", "--entry", inngangspunkt_VERDI,
                        "--classpath", bibliotek, "-o", "실행프로그램", inndata_VERDI));
                } else if (Kommando(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", bibliotek,
                        "-d", "classes", inndata_VERDI)) == 0 && Utfør_kommando) {
                    Kommando(Arrays.asList("java", "-cp", "classes:" + bibliotek, inngangspunkt_VERDI));
                }
            } catch (Exception feil) { notice(feil.toString()); }
        });
    }
    private void Pause_kjøring() {
        Process betalt_vare = Prosess_VERDI;
        if (betalt_vare != null) { betalt_vare.descendants().forEach(ProcessHandle::destroy); betalt_vare.destroy(); }
    }
    private arbeidsområde() throws IOException {
        Files.createDirectories(arbeidsmappe);
        Font skrift_VERDI = new Font("Monospaced", Font.PLAIN, 16);
        KILDE.setFont(skrift_VERDI); Utgang.setFont(skrift_VERDI); Utgang.setEditable(false);
        KILDE.setTabSize(4);
        KILDE.setMargin(new Insets(10, 12, 10, 12));
        Utgang.setMargin(new Insets(8, 12, 8, 12));
        KILDE.setBackground(new Color(250, 251, 252));
        KILDE.setForeground(new Color(32, 43, 58));
        JPanel kommando_panel = new JPanel();
        kommando_panel.add(new JLabel("Fil")); kommando_panel.add(Fil_oppføring_navn);
        kommando_panel.add(new JLabel("주 time_VERDI")); kommando_panel.add(time_oppføring_navn);
        Knapp(kommando_panel, "Åpne", this::Åpne); Knapp(kommando_panel, "Store_VERDI", this::Store_VERDI);
        Knapp(kommando_panel, "kompilere_kilde", () -> OVERSETT_kilde(false, false));
        Knapp(kommando_panel, "Utfør_kommando", () -> OVERSETT_kilde(true, false));
        Knapp(kommando_panel, "Utfør_kommando Fil åpne_oppføring", () -> OVERSETT_kilde(false, true));
        Knapp(kommando_panel, "Pause_kjøring", this::Pause_kjøring);
        JSplitPane Divisjon_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(KILDE), new JScrollPane(Utgang));
        Divisjon_KR.setResizeWeight(0.75);
        Vindu.add(kommando_panel, BorderLayout.NORTH); Vindu.add(Divisjon_KR, BorderLayout.CENTER);
        Vindu.setSize(1200, 750); Vindu.setLocationRelativeTo(null);
        Vindu.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Vindu.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Hendelse) { Pause_kjøring(); arbeider_VERDI.shutdownNow(); }
        });
        Åpne(); Vindu.setVisible(true);
    }
    public static void main(String[] Argumenter) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource standardskrift = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object oppføring_VERDI : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(oppføring_VERDI) instanceof Font) UIManager.put(oppføring_VERDI, standardskrift);
                }
                new arbeidsområde();
            } catch (Exception feil) { feil.printStackTrace(); }
        });
    }
}
