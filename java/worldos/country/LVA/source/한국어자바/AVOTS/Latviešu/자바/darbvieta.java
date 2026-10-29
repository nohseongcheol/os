// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.자바;

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

/** lietotājs 홈에서 Java 원문을 Rediģēt_VALUE·kompilēt_avots·실행하는 작은 Swing darbvieta. */
public final class darbvieta {
    private final JFrame Logs = new JFrame("jkoros — 자바 darbvieta");
    private final JTextArea AVOTS = new JTextArea();
    private final JTextArea Izvade = new JTextArea(8, 80);
    private final JTextField Fails_ievade_nosaukums = new JTextField("인사.java", 20);
    private final JTextField klase_ievade_nosaukums = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService nodarbinātais_VALUE = Executors.newSingleThreadExecutor();
    private volatile Process Process_VALUE;
    private final String bibliotēka = "/opt/jkoros/lib/한국어자바.jar";

    private void informēšana(String Teksts) { SwingUtilities.invokeLater(() -> Izvade.append(Teksts + "\n")); }
    private void Pogas(JPanel versija_VALUE, String Nosaukums, Runnable 행동) {
        JButton Pogas = new JButton(Nosaukums);
        Pogas.addActionListener(Notikums -> 행동.run());
        versija_VALUE.add(Pogas);
    }
    private boolean Store_VALUE() {
        try {
            Path CEĻŠ = 작업폴더.resolve(Fails_ievade_nosaukums.getText());
            Files.createDirectories(CEĻŠ.getParent());
            Fails.Rakstīt(CEĻŠ, AVOTS.getText());
            informēšana("Store_VALUE: " + CEĻŠ);
            return true;
        } catch (Exception Kļūda) { informēšana(Kļūda.toString()); return false; }
    }
    private void Atvērt() {
        try { AVOTS.setText(Fails.Lasīt(작업폴더.resolve(Fails_ievade_nosaukums.getText()))); }
        catch (Exception Kļūda) { informēšana(Kļūda.toString()); }
    }
    private int Komanda(List<String> Komanda) throws Exception {
        Process_VALUE = new ProcessBuilder(Komanda).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Līniju = new BufferedReader(new InputStreamReader(Process_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Teksts;
            while ((Teksts = Līniju.readLine()) != null) informēšana(Teksts);
        }
        int Statuss_VALUE = Process_VALUE.waitFor(); Process_VALUE = null;
        informēšana("Iziet_programma CODE_VALUE: " + Statuss_VALUE);
        return Statuss_VALUE;
    }
    private void translēt_avots(boolean Izpildīt_komanda, boolean izpildāms_fails) {
        if (!Store_VALUE()) return;
        String 입력 = Fails_ievade_nosaukums.getText(), ieejas_punkts_VALUE = klase_ievade_nosaukums.getText();
        nodarbinātais_VALUE.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (izpildāms_fails) {
                    Komanda(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ieejas_punkts_VALUE,
                        "--classpath", bibliotēka, "-o", "실행프로그램", 입력));
                } else if (Komanda(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", bibliotēka,
                        "-d", "classes", 입력)) == 0 && Izpildīt_komanda) {
                    Komanda(Arrays.asList("java", "-cp", "classes:" + bibliotēka, ieejas_punkts_VALUE));
                }
            } catch (Exception Kļūda) { informēšana(Kļūda.toString()); }
        });
    }
    private void 멈춤() {
        Process pašreizējais_krājums = Process_VALUE;
        if (pašreizējais_krājums != null) { pašreizējais_krājums.descendants().forEach(ProcessHandle::destroy); pašreizējais_krājums.destroy(); }
    }
    private darbvieta() throws IOException {
        Files.createDirectories(작업폴더);
        Font fonts_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        AVOTS.setFont(fonts_VALUE); Izvade.setFont(fonts_VALUE); Izvade.setEditable(false);
        AVOTS.setTabSize(4);
        AVOTS.setMargin(new Insets(10, 12, 10, 12));
        Izvade.setMargin(new Insets(8, 12, 8, 12));
        AVOTS.setBackground(new Color(250, 251, 252));
        AVOTS.setForeground(new Color(32, 43, 58));
        JPanel komanda_panelis = new JPanel();
        komanda_panelis.add(new JLabel("Fails")); komanda_panelis.add(Fails_ievade_nosaukums);
        komanda_panelis.add(new JLabel("주 klase_VALUE")); komanda_panelis.add(klase_ievade_nosaukums);
        Pogas(komanda_panelis, "Atvērt", this::Atvērt); Pogas(komanda_panelis, "Store_VALUE", this::Store_VALUE);
        Pogas(komanda_panelis, "kompilēt_avots", () -> translēt_avots(false, false));
        Pogas(komanda_panelis, "Izpildīt_komanda", () -> translēt_avots(true, false));
        Pogas(komanda_panelis, "Izpildīt_komanda Fails atvērt_ievade", () -> translēt_avots(false, true));
        Pogas(komanda_panelis, "멈춤", this::멈춤);
        JSplitPane nodaļa_mērs = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(AVOTS), new JScrollPane(Izvade));
        nodaļa_mērs.setResizeWeight(0.75);
        Logs.add(komanda_panelis, BorderLayout.NORTH); Logs.add(nodaļa_mērs, BorderLayout.CENTER);
        Logs.setSize(1200, 750); Logs.setLocationRelativeTo(null);
        Logs.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Logs.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Notikums) { 멈춤(); nodarbinātais_VALUE.shutdownNow(); }
        });
        Atvērt(); Logs.setVisible(true);
    }
    public static void main(String[] Parametri) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource noklusējuma_fonts = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ievade_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ievade_VALUE) instanceof Font) UIManager.put(ievade_VALUE, noklusējuma_fonts);
                }
                new darbvieta();
            } catch (Exception Kļūda) { Kļūda.printStackTrace(); }
        });
    }
}
