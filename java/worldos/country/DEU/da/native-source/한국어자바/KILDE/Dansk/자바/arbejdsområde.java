// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.자바;

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

/** bruger 홈에서 Java 원문을 Rediger_VÆRDI·kompilere_kilde·실행하는 작은 Swing arbejdsområde. */
public final class arbejdsområde {
    private final JFrame Vindue = new JFrame("jkoros — 자바 arbejdsområde");
    private final JTextArea KILDE = new JTextArea();
    private final JTextArea Udgang = new JTextArea(8, 80);
    private final JTextField fil_post_navn = new JTextField("인사.java", 20);
    private final JTextField Hold_post_navn = new JTextField("인사", 16);
    private final Path arbejdsmappe = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService arbejder_VÆRDI = Executors.newSingleThreadExecutor();
    private volatile Process Proces_VÆRDI;
    private final String bibliotek = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Tekst) { SwingUtilities.invokeLater(() -> Udgang.append(Tekst + "\n")); }
    private void knap(JPanel version_VÆRDI, String Navn, Runnable 행동) {
        JButton knap = new JButton(Navn);
        knap.addActionListener(hændelse -> 행동.run());
        version_VÆRDI.add(knap);
    }
    private boolean Store_VÆRDI() {
        try {
            Path Sti = arbejdsmappe.resolve(fil_post_navn.getText());
            Files.createDirectories(Sti.getParent());
            Fil.Skrive(Sti, KILDE.getText());
            알림("Store_VÆRDI: " + Sti);
            return true;
        } catch (Exception fejl) { 알림(fejl.toString()); return false; }
    }
    private void Åbn() {
        try { KILDE.setText(Fil.Læse(arbejdsmappe.resolve(fil_post_navn.getText()))); }
        catch (Exception fejl) { 알림(fejl.toString()); }
    }
    private int Kommando(List<String> Kommando) throws Exception {
        Proces_VÆRDI = new ProcessBuilder(Kommando).directory(arbejdsmappe.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Linje = new BufferedReader(new InputStreamReader(Proces_VÆRDI.getInputStream(), StandardCharsets.UTF_8))) {
            String Tekst;
            while ((Tekst = Linje.readLine()) != null) 알림(Tekst);
        }
        int status_VÆRDI = Proces_VÆRDI.waitFor(); Proces_VÆRDI = null;
        알림("Afslut_app KODE_VÆRDI: " + status_VÆRDI);
        return status_VÆRDI;
    }
    private void OVERSÆT_kilde(boolean Udfør_kommando, boolean eksekverbar_fil) {
        if (!Store_VÆRDI()) return;
        String input_VÆRDI = fil_post_navn.getText(), indgangspunkt_VÆRDI = Hold_post_navn.getText();
        arbejder_VÆRDI.submit(() -> {
            try {
                Files.createDirectories(arbejdsmappe.resolve("classes"));
                if (eksekverbar_fil) {
                    Kommando(Arrays.asList("jclassc", "--target", "openjdk", "--entry", indgangspunkt_VÆRDI,
                        "--classpath", bibliotek, "-o", "실행프로그램", input_VÆRDI));
                } else if (Kommando(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", bibliotek,
                        "-d", "classes", input_VÆRDI)) == 0 && Udfør_kommando) {
                    Kommando(Arrays.asList("java", "-cp", "classes:" + bibliotek, indgangspunkt_VÆRDI));
                }
            } catch (Exception fejl) { 알림(fejl.toString()); }
        });
    }
    private void Afbryd_midlertidigt_udførelse() {
        Process aktuel_vare = Proces_VÆRDI;
        if (aktuel_vare != null) { aktuel_vare.descendants().forEach(ProcessHandle::destroy); aktuel_vare.destroy(); }
    }
    private arbejdsområde() throws IOException {
        Files.createDirectories(arbejdsmappe);
        Font skrifttype_VÆRDI = new Font("Monospaced", Font.PLAIN, 16);
        KILDE.setFont(skrifttype_VÆRDI); Udgang.setFont(skrifttype_VÆRDI); Udgang.setEditable(false);
        KILDE.setTabSize(4);
        KILDE.setMargin(new Insets(10, 12, 10, 12));
        Udgang.setMargin(new Insets(8, 12, 8, 12));
        KILDE.setBackground(new Color(250, 251, 252));
        KILDE.setForeground(new Color(32, 43, 58));
        JPanel kommando_panel = new JPanel();
        kommando_panel.add(new JLabel("Fil")); kommando_panel.add(fil_post_navn);
        kommando_panel.add(new JLabel("주 Hold_VÆRDI")); kommando_panel.add(Hold_post_navn);
        knap(kommando_panel, "Åbn", this::Åbn); knap(kommando_panel, "Store_VÆRDI", this::Store_VÆRDI);
        knap(kommando_panel, "kompilere_kilde", () -> OVERSÆT_kilde(false, false));
        knap(kommando_panel, "Udfør_kommando", () -> OVERSÆT_kilde(true, false));
        knap(kommando_panel, "Udfør_kommando Fil åbne_post_81b8d99b", () -> OVERSÆT_kilde(false, true));
        knap(kommando_panel, "Afbryd_midlertidigt_udførelse", this::Afbryd_midlertidigt_udførelse);
        JSplitPane Division_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(KILDE), new JScrollPane(Udgang));
        Division_KR.setResizeWeight(0.75);
        Vindue.add(kommando_panel, BorderLayout.NORTH); Vindue.add(Division_KR, BorderLayout.CENTER);
        Vindue.setSize(1200, 750); Vindue.setLocationRelativeTo(null);
        Vindue.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Vindue.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent hændelse) { Afbryd_midlertidigt_udførelse(); arbejder_VÆRDI.shutdownNow(); }
        });
        Åbn(); Vindue.setVisible(true);
    }
    public static void main(String[] Argumenter) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource standardskrifttype = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object post_VÆRDI_962f286b : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(post_VÆRDI_962f286b) instanceof Font) UIManager.put(post_VÆRDI_962f286b, standardskrifttype);
                }
                new arbejdsområde();
            } catch (Exception fejl) { fejl.printStackTrace(); }
        });
    }
}
