// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.자바;

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

/** kullanıcı_alanı 홈에서 Java 원문을 Düzenle_değer·derlemek_kaynak·실행하는 작은 Swing çalışma_alanı. */
public final class çalışma_alanı {
    private final JFrame Pencere = new JFrame("jkoros — 자바 çalışma_alanı");
    private final JTextArea kaynakKod = new JTextArea();
    private final JTextArea metinÇıktısı = new JTextArea(8, 80);
    private final JTextField Dosya_girdi_ad = new JTextField("인사.java", 20);
    private final JTextField Sınıf_girdi_ad = new JTextField("인사", 16);
    private final Path çalışma_dizini = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService çalışan_değer = Executors.newSingleThreadExecutor();
    private volatile Process işlem_değer;
    private final String kitaplık = "/opt/jkoros/lib/한국어자바.jar";

    private void uyarı(String metin) { SwingUtilities.invokeLater(() -> metinÇıktısı.append(metin + "\n")); }
    private void düğme(JPanel sürüm_değer, String İsim, Runnable 행동) {
        JButton düğme = new JButton(İsim);
        düğme.addActionListener(Olay -> 행동.run());
        sürüm_değer.add(düğme);
    }
    private boolean depo_değer() {
        try {
            Path yol = çalışma_dizini.resolve(Dosya_girdi_ad.getText());
            Files.createDirectories(yol.getParent());
            dosya.Yazma(yol, kaynakKod.getText());
            uyarı("depo_değer: " + yol);
            return true;
        } catch (Exception hata) { uyarı(hata.toString()); return false; }
    }
    private void Aç() {
        try { kaynakKod.setText(dosya.Okuma(çalışma_dizini.resolve(Dosya_girdi_ad.getText()))); }
        catch (Exception hata) { uyarı(hata.toString()); }
    }
    private int komut(List<String> komut) throws Exception {
        işlem_değer = new ProcessBuilder(komut).directory(çalışma_dizini.toFile()).redirectErrorStream(true).start();
        try (BufferedReader girdi_satırı = new BufferedReader(new InputStreamReader(işlem_değer.getInputStream(), StandardCharsets.UTF_8))) {
            String metin;
            while ((metin = girdi_satırı.readLine()) != null) uyarı(metin);
        }
        int Durum_değer = işlem_değer.waitFor(); işlem_değer = null;
        uyarı("Çıkış_program KOD_değer: " + Durum_değer);
        return Durum_değer;
    }
    private void çevir_kaynak(boolean yürütmek_komut, boolean çalıştırılabilir) {
        if (!depo_değer()) return;
        String artış_değer = Dosya_girdi_ad.getText(), giriş_noktası_değer = Sınıf_girdi_ad.getText();
        çalışan_değer.submit(() -> {
            try {
                Files.createDirectories(çalışma_dizini.resolve("classes"));
                if (çalıştırılabilir) {
                    komut(Arrays.asList("jclassc", "--target", "openjdk", "--entry", giriş_noktası_değer,
                        "--classpath", kitaplık, "-o", "실행프로그램", artış_değer));
                } else if (komut(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", kitaplık,
                        "-d", "classes", artış_değer)) == 0 && yürütmek_komut) {
                    komut(Arrays.asList("java", "-cp", "classes:" + kitaplık, giriş_noktası_değer));
                }
            } catch (Exception hata) { uyarı(hata.toString()); }
        });
    }
    private void Duraklat_yürütme() {
        Process geçerli_öğe = işlem_değer;
        if (geçerli_öğe != null) { geçerli_öğe.descendants().forEach(ProcessHandle::destroy); geçerli_öğe.destroy(); }
    }
    private çalışma_alanı() throws IOException {
        Files.createDirectories(çalışma_dizini);
        Font yazı_tipi_değer = new Font("Monospaced", Font.PLAIN, 16);
        kaynakKod.setFont(yazı_tipi_değer); metinÇıktısı.setFont(yazı_tipi_değer); metinÇıktısı.setEditable(false);
        kaynakKod.setTabSize(4);
        kaynakKod.setMargin(new Insets(10, 12, 10, 12));
        metinÇıktısı.setMargin(new Insets(8, 12, 8, 12));
        kaynakKod.setBackground(new Color(250, 251, 252));
        kaynakKod.setForeground(new Color(32, 43, 58));
        JPanel komut_panel = new JPanel();
        komut_panel.add(new JLabel("dosya")); komut_panel.add(Dosya_girdi_ad);
        komut_panel.add(new JLabel("주 Sınıf_değer")); komut_panel.add(Sınıf_girdi_ad);
        düğme(komut_panel, "Aç", this::Aç); düğme(komut_panel, "depo_değer", this::depo_değer);
        düğme(komut_panel, "derlemek_kaynak", () -> çevir_kaynak(false, false));
        düğme(komut_panel, "yürütmek_komut", () -> çevir_kaynak(true, false));
        düğme(komut_panel, "yürütmek_komut dosya açmak_girdi", () -> çevir_kaynak(false, true));
        düğme(komut_panel, "Duraklat_yürütme", this::Duraklat_yürütme);
        JSplitPane Bölge_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(kaynakKod), new JScrollPane(metinÇıktısı));
        Bölge_KR.setResizeWeight(0.75);
        Pencere.add(komut_panel, BorderLayout.NORTH); Pencere.add(Bölge_KR, BorderLayout.CENTER);
        Pencere.setSize(1200, 750); Pencere.setLocationRelativeTo(null);
        Pencere.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Pencere.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Olay) { Duraklat_yürütme(); çalışan_değer.shutdownNow(); }
        });
        Aç(); Pencere.setVisible(true);
    }
    public static void main(String[] bağımsız_değişkenler) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource varsayılan_yazı_tipi = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object girdi_değer : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(girdi_değer) instanceof Font) UIManager.put(girdi_değer, varsayılan_yazı_tipi);
                }
                new çalışma_alanı();
            } catch (Exception hata) { hata.printStackTrace(); }
        });
    }
}
