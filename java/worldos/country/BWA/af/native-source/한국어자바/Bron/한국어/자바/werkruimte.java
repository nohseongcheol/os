// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

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

/** gebruiker 홈에서 Java 원문을 redigeer_VALUE·bou_bron·실행하는 작은 Swing werkruimte. */
public final class werkruimte {
    private final JFrame venster = new JFrame("jkoros — 자바 werkruimte");
    private final JTextArea Bron = new JTextArea();
    private final JTextArea Afvoer = new JTextArea(8, 80);
    private final JTextField lêer_inskrywing_naam = new JTextField("인사.java", 20);
    private final JTextField Klas_inskrywing_naam = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Proses_VALUE;
    private final String biblioteek = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Teks) { SwingUtilities.invokeLater(() -> Afvoer.append(Teks + "\n")); }
    private void knoppie(JPanel weergawe_VALUE, String Naam, Runnable 행동) {
        JButton knoppie = new JButton(Naam);
        knoppie.addActionListener(gebeurtenis -> 행동.run());
        weergawe_VALUE.add(knoppie);
    }
    private boolean bêre_VALUE() {
        try {
            Path Pad = 작업폴더.resolve(lêer_inskrywing_naam.getText());
            Files.createDirectories(Pad.getParent());
            Lêer.Skryf(Pad, Bron.getText());
            알림("bêre_VALUE: " + Pad);
            return true;
        } catch (Exception Fout) { 알림(Fout.toString()); return false; }
    }
    private void skep() {
        try { Bron.setText(Lêer.Lees(작업폴더.resolve(lêer_inskrywing_naam.getText()))); }
        catch (Exception Fout) { 알림(Fout.toString()); }
    }
    private int Opdrag(List<String> Opdrag) throws Exception {
        Proses_VALUE = new ProcessBuilder(Opdrag).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader lyn = new BufferedReader(new InputStreamReader(Proses_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Teks;
            while ((Teks = lyn.readLine()) != null) 알림(Teks);
        }
        int stand_VALUE = Proses_VALUE.waitFor(); Proses_VALUE = null;
        알림("Verlaat_program CODE_VALUE: " + stand_VALUE);
        return stand_VALUE;
    }
    private void Vertaal_bron(boolean uitvoer_bevel, boolean 실행파일) {
        if (!bêre_VALUE()) return;
        String 입력 = lêer_inskrywing_naam.getText(), inskrywing_p_VALUE = Klas_inskrywing_naam.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Opdrag(Arrays.asList("jclassc", "--target", "openjdk", "--entry", inskrywing_p_VALUE,
                        "--classpath", biblioteek, "-o", "실행프로그램", 입력));
                } else if (Opdrag(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", biblioteek,
                        "-d", "classes", 입력)) == 0 && uitvoer_bevel) {
                    Opdrag(Arrays.asList("java", "-cp", "classes:" + biblioteek, inskrywing_p_VALUE));
                }
            } catch (Exception Fout) { 알림(Fout.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Proses_VALUE;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private werkruimte() throws IOException {
        Files.createDirectories(작업폴더);
        Font font_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        Bron.setFont(font_VALUE); Afvoer.setFont(font_VALUE); Afvoer.setEditable(false);
        Bron.setTabSize(4);
        Bron.setMargin(new Insets(10, 12, 10, 12));
        Afvoer.setMargin(new Insets(8, 12, 8, 12));
        Bron.setBackground(new Color(250, 251, 252));
        Bron.setForeground(new Color(32, 43, 58));
        JPanel bevel_paneel = new JPanel();
        bevel_paneel.add(new JLabel("Lêer")); bevel_paneel.add(lêer_inskrywing_naam);
        bevel_paneel.add(new JLabel("주 Klas_VALUE")); bevel_paneel.add(Klas_inskrywing_naam);
        knoppie(bevel_paneel, "skep", this::skep); knoppie(bevel_paneel, "bêre_VALUE", this::bêre_VALUE);
        knoppie(bevel_paneel, "bou_bron", () -> Vertaal_bron(false, false));
        knoppie(bevel_paneel, "uitvoer_bevel", () -> Vertaal_bron(true, false));
        knoppie(bevel_paneel, "uitvoer_bevel Lêer Skep_inskrywing", () -> Vertaal_bron(false, true));
        knoppie(bevel_paneel, "멈춤", this::멈춤);
        JSplitPane deling_maatreël = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Bron), new JScrollPane(Afvoer));
        deling_maatreël.setResizeWeight(0.75);
        venster.add(bevel_paneel, BorderLayout.NORTH); venster.add(deling_maatreël, BorderLayout.CENTER);
        venster.setSize(1200, 750); venster.setLocationRelativeTo(null);
        venster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        venster.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent gebeurtenis) { 멈춤(); 일꾼.shutdownNow(); }
        });
        skep(); venster.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource verstekfont = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object inskrywing_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(inskrywing_VALUE) instanceof Font) UIManager.put(inskrywing_VALUE, verstekfont);
                }
                new werkruimte();
            } catch (Exception Fout) { Fout.printStackTrace(); }
        });
    }
}
