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

/** Mai_anfani_da_kwamfuta 홈에서 Java 원문을 gyaran_Daraja·Gina_tushe·실행하는 작은 Swing sararin_aiki. */
public final class sararin_aiki {
    private final JFrame taga = new JFrame("jkoros — 자바 sararin_aiki");
    private final JTextArea tushe = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField Fayil_Mashigar_bayanai_Suna = new JTextField("인사.java", 20);
    private final JTextField Aji_Mashigar_bayanai_Suna = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process haryar_aikin_na_ura_Daraja;
    private final String laburare = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String SMS) { SwingUtilities.invokeLater(() -> 출력.append(SMS + "\n")); }
    private void maɓali(JPanel siga_Daraja, String Suna, Runnable 행동) {
        JButton maɓali = new JButton(Suna);
        maɓali.addActionListener(Faruwa -> 행동.run());
        siga_Daraja.add(maɓali);
    }
    private boolean Ajiye_Daraja() {
        try {
            Path Hanyar_shiga = 작업폴더.resolve(Fayil_Mashigar_bayanai_Suna.getText());
            Files.createDirectories(Hanyar_shiga.getParent());
            Fayil.Yi_Rubutu(Hanyar_shiga, tushe.getText());
            알림("Ajiye_Daraja: " + Hanyar_shiga);
            return true;
        } catch (Exception Kuskure) { 알림(Kuskure.toString()); return false; }
    }
    private void Buɗe() {
        try { tushe.setText(Fayil.Yi_Karatu(작업폴더.resolve(Fayil_Mashigar_bayanai_Suna.getText()))); }
        catch (Exception Kuskure) { 알림(Kuskure.toString()); }
    }
    private int Umarni(List<String> Umarni) throws Exception {
        haryar_aikin_na_ura_Daraja = new ProcessBuilder(Umarni).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Layi = new BufferedReader(new InputStreamReader(haryar_aikin_na_ura_Daraja.getInputStream(), StandardCharsets.UTF_8))) {
            String SMS;
            while ((SMS = Layi.readLine()) != null) 알림(SMS);
        }
        int Matsayi_Daraja = haryar_aikin_na_ura_Daraja.waitFor(); haryar_aikin_na_ura_Daraja = null;
        알림("Mafita_Shiri lambar_sirri_Daraja: " + Matsayi_Daraja);
        return Matsayi_Daraja;
    }
    private void Fasara_tushe(boolean gudanar_Umarni, boolean 실행파일) {
        if (!Ajiye_Daraja()) return;
        String 입력 = Fayil_Mashigar_bayanai_Suna.getText(), Mashigar_bayanai_maki_Daraja = Aji_Mashigar_bayanai_Suna.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Umarni(Arrays.asList("jclassc", "--target", "openjdk", "--entry", Mashigar_bayanai_maki_Daraja,
                        "--classpath", laburare, "-o", "실행프로그램", 입력));
                } else if (Umarni(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", laburare,
                        "-d", "classes", 입력)) == 0 && gudanar_Umarni) {
                    Umarni(Arrays.asList("java", "-cp", "classes:" + laburare, Mashigar_bayanai_maki_Daraja));
                }
            } catch (Exception Kuskure) { 알림(Kuskure.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = haryar_aikin_na_ura_Daraja;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private sararin_aiki() throws IOException {
        Files.createDirectories(작업폴더);
        Font salon_rubutu_Daraja = new Font("Monospaced", Font.PLAIN, 16);
        tushe.setFont(salon_rubutu_Daraja); 출력.setFont(salon_rubutu_Daraja); 출력.setEditable(false);
        tushe.setTabSize(4);
        tushe.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        tushe.setBackground(new Color(250, 251, 252));
        tushe.setForeground(new Color(32, 43, 58));
        JPanel Umarni_fanel = new JPanel();
        Umarni_fanel.add(new JLabel("Fayil")); Umarni_fanel.add(Fayil_Mashigar_bayanai_Suna);
        Umarni_fanel.add(new JLabel("주 Aji_Daraja")); Umarni_fanel.add(Aji_Mashigar_bayanai_Suna);
        maɓali(Umarni_fanel, "Buɗe", this::Buɗe); maɓali(Umarni_fanel, "Ajiye_Daraja", this::Ajiye_Daraja);
        maɓali(Umarni_fanel, "Gina_tushe", () -> Fasara_tushe(false, false));
        maɓali(Umarni_fanel, "gudanar_Umarni", () -> Fasara_tushe(true, false));
        maɓali(Umarni_fanel, "gudanar_Umarni Fayil ƙirƙíra_Mashigar_bayanai", () -> Fasara_tushe(false, true));
        maɓali(Umarni_fanel, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(tushe), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        taga.add(Umarni_fanel, BorderLayout.NORTH); taga.add(나눔, BorderLayout.CENTER);
        taga.setSize(1200, 750); taga.setLocationRelativeTo(null);
        taga.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        taga.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Faruwa) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Buɗe(); taga.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource Tanadaddiyar_sigar_rubutu = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object Mashigar_bayanai_Daraja : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(Mashigar_bayanai_Daraja) instanceof Font) UIManager.put(Mashigar_bayanai_Daraja, Tanadaddiyar_sigar_rubutu);
                }
                new sararin_aiki();
            } catch (Exception Kuskure) { Kuskure.printStackTrace(); }
        });
    }
}
