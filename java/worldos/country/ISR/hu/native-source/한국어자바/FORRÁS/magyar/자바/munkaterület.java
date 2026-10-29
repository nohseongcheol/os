// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.자바;

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

/** felhasználó 홈에서 Java 원문을 szerkeszt_ÉRTÉK·épít_forrás·실행하는 작은 Swing munkaterület. */
public final class munkaterület {
    private final JFrame Ablak = new JFrame("jkoros — 자바 munkaterület");
    private final JTextArea FORRÁS = new JTextArea();
    private final JTextArea Kimenet = new JTextArea(8, 80);
    private final JTextField Fájl_bejegyzés_név = new JTextField("인사.java", 20);
    private final JTextField tanóra_bejegyzés_név = new JTextField("인사", 16);
    private final Path munkakönyvtár = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService dolgozó_ÉRTÉK = Executors.newSingleThreadExecutor();
    private volatile Process folyamat_ÉRTÉK;
    private final String kódtár = "/opt/jkoros/lib/한국어자바.jar";

    private void alapelv(String Szöveg) { SwingUtilities.invokeLater(() -> Kimenet.append(Szöveg + "\n")); }
    private void gomb(JPanel verzió_ÉRTÉK, String Név, Runnable 행동) {
        JButton gomb = new JButton(Név);
        gomb.addActionListener(Esemény -> 행동.run());
        verzió_ÉRTÉK.add(gomb);
    }
    private boolean tár_ÉRTÉK() {
        try {
            Path ÚTVONAL = munkakönyvtár.resolve(Fájl_bejegyzés_név.getText());
            Files.createDirectories(ÚTVONAL.getParent());
            Fájl.Írás(ÚTVONAL, FORRÁS.getText());
            alapelv("tár_ÉRTÉK: " + ÚTVONAL);
            return true;
        } catch (Exception HIBA) { alapelv(HIBA.toString()); return false; }
    }
    private void Megnyitás() {
        try { FORRÁS.setText(Fájl.Olvasás(munkakönyvtár.resolve(Fájl_bejegyzés_név.getText()))); }
        catch (Exception HIBA) { alapelv(HIBA.toString()); }
    }
    private int Parancs(List<String> Parancs) throws Exception {
        folyamat_ÉRTÉK = new ProcessBuilder(Parancs).directory(munkakönyvtár.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Vonal = new BufferedReader(new InputStreamReader(folyamat_ÉRTÉK.getInputStream(), StandardCharsets.UTF_8))) {
            String Szöveg;
            while ((Szöveg = Vonal.readLine()) != null) alapelv(Szöveg);
        }
        int Állapot_ÉRTÉK = folyamat_ÉRTÉK.waitFor(); folyamat_ÉRTÉK = null;
        alapelv("kilép_app KÓD_ÉRTÉK: " + Állapot_ÉRTÉK);
        return Állapot_ÉRTÉK;
    }
    private void FORDÍTÁS_forrás(boolean végrehajt_parancs, boolean végrehajtható_Fájl) {
        if (!tár_ÉRTÉK()) return;
        String bevitel_ÉRTÉK = Fájl_bejegyzés_név.getText(), belépési_pont_ÉRTÉK = tanóra_bejegyzés_név.getText();
        dolgozó_ÉRTÉK.submit(() -> {
            try {
                Files.createDirectories(munkakönyvtár.resolve("classes"));
                if (végrehajtható_Fájl) {
                    Parancs(Arrays.asList("jclassc", "--target", "openjdk", "--entry", belépési_pont_ÉRTÉK,
                        "--classpath", kódtár, "-o", "실행프로그램", bevitel_ÉRTÉK));
                } else if (Parancs(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", kódtár,
                        "-d", "classes", bevitel_ÉRTÉK)) == 0 && végrehajt_parancs) {
                    Parancs(Arrays.asList("java", "-cp", "classes:" + kódtár, belépési_pont_ÉRTÉK));
                }
            } catch (Exception HIBA) { alapelv(HIBA.toString()); }
        });
    }
    private void Szünet_végrehajtás() {
        Process aktuális_cikk = folyamat_ÉRTÉK;
        if (aktuális_cikk != null) { aktuális_cikk.descendants().forEach(ProcessHandle::destroy); aktuális_cikk.destroy(); }
    }
    private munkaterület() throws IOException {
        Files.createDirectories(munkakönyvtár);
        Font betűkészlet_ÉRTÉK = new Font("Monospaced", Font.PLAIN, 16);
        FORRÁS.setFont(betűkészlet_ÉRTÉK); Kimenet.setFont(betűkészlet_ÉRTÉK); Kimenet.setEditable(false);
        FORRÁS.setTabSize(4);
        FORRÁS.setMargin(new Insets(10, 12, 10, 12));
        Kimenet.setMargin(new Insets(8, 12, 8, 12));
        FORRÁS.setBackground(new Color(250, 251, 252));
        FORRÁS.setForeground(new Color(32, 43, 58));
        JPanel parancs_panel = new JPanel();
        parancs_panel.add(new JLabel("Fájl")); parancs_panel.add(Fájl_bejegyzés_név);
        parancs_panel.add(new JLabel("주 tanóra_ÉRTÉK")); parancs_panel.add(tanóra_bejegyzés_név);
        gomb(parancs_panel, "Megnyitás", this::Megnyitás); gomb(parancs_panel, "tár_ÉRTÉK", this::tár_ÉRTÉK);
        gomb(parancs_panel, "épít_forrás", () -> FORDÍTÁS_forrás(false, false));
        gomb(parancs_panel, "végrehajt_parancs", () -> FORDÍTÁS_forrás(true, false));
        gomb(parancs_panel, "végrehajt_parancs Fájl készít_bejegyzés", () -> FORDÍTÁS_forrás(false, true));
        gomb(parancs_panel, "Szünet_végrehajtás", this::Szünet_végrehajtás);
        JSplitPane osztás_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(FORRÁS), new JScrollPane(Kimenet));
        osztás_KR.setResizeWeight(0.75);
        Ablak.add(parancs_panel, BorderLayout.NORTH); Ablak.add(osztás_KR, BorderLayout.CENTER);
        Ablak.setSize(1200, 750); Ablak.setLocationRelativeTo(null);
        Ablak.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Ablak.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Esemény) { Szünet_végrehajtás(); dolgozó_ÉRTÉK.shutdownNow(); }
        });
        Megnyitás(); Ablak.setVisible(true);
    }
    public static void main(String[] Argumentumok) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource alapértelmezett_betűtípus = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object bejegyzés_ÉRTÉK : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(bejegyzés_ÉRTÉK) instanceof Font) UIManager.put(bejegyzés_ÉRTÉK, alapértelmezett_betűtípus);
                }
                new munkaterület();
            } catch (Exception HIBA) { HIBA.printStackTrace(); }
        });
    }
}
