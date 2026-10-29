// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.자바;

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

/** ruang_pengguna 홈에서 Java 원문을 edit_VALUE·bina_sumber·실행하는 작은 Swing ruang_kerja. */
public final class ruang_kerja {
    private final JFrame Tetingkap = new JFrame("jkoros — 자바 ruang_kerja");
    private final JTextArea SUMBER = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField fail_pemasukan_nama = new JTextField("인사.java", 20);
    private final JTextField Kelas_pemasukan_nama = new JTextField("인사", 16);
    private final Path direktori_kerja = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Proses_VALUE;
    private final String pustaka = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Teks) { SwingUtilities.invokeLater(() -> 출력.append(Teks + "\n")); }
    private void Butang(JPanel versi_VALUE, String Nama, Runnable 행동) {
        JButton Butang = new JButton(Nama);
        Butang.addActionListener(Peristiwa -> 행동.run());
        versi_VALUE.add(Butang);
    }
    private boolean stor_VALUE() {
        try {
            Path LALUAN = direktori_kerja.resolve(fail_pemasukan_nama.getText());
            Files.createDirectories(LALUAN.getParent());
            Fail.Tulis(LALUAN, SUMBER.getText());
            알림("stor_VALUE: " + LALUAN);
            return true;
        } catch (Exception RALAT) { 알림(RALAT.toString()); return false; }
    }
    private void Buka() {
        try { SUMBER.setText(Fail.Baca(direktori_kerja.resolve(fail_pemasukan_nama.getText()))); }
        catch (Exception RALAT) { 알림(RALAT.toString()); }
    }
    private int Perintah(List<String> Perintah) throws Exception {
        Proses_VALUE = new ProcessBuilder(Perintah).directory(direktori_kerja.toFile()).redirectErrorStream(true).start();
        try (BufferedReader baris = new BufferedReader(new InputStreamReader(Proses_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Teks;
            while ((Teks = baris.readLine()) != null) 알림(Teks);
        }
        int status_VALUE = Proses_VALUE.waitFor(); Proses_VALUE = null;
        알림("Keluar_aplikasi kod_VALUE: " + status_VALUE);
        return status_VALUE;
    }
    private void Terjemah_sumber(boolean laksanakan_perintah, boolean fail_boleh_laku) {
        if (!stor_VALUE()) return;
        String 입력 = fail_pemasukan_nama.getText(), titik_permulaan_VALUE = Kelas_pemasukan_nama.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(direktori_kerja.resolve("classes"));
                if (fail_boleh_laku) {
                    Perintah(Arrays.asList("jclassc", "--target", "openjdk", "--entry", titik_permulaan_VALUE,
                        "--classpath", pustaka, "-o", "실행프로그램", 입력));
                } else if (Perintah(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", pustaka,
                        "-d", "classes", 입력)) == 0 && laksanakan_perintah) {
                    Perintah(Arrays.asList("java", "-cp", "classes:" + pustaka, titik_permulaan_VALUE));
                }
            } catch (Exception RALAT) { 알림(RALAT.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Proses_VALUE;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private ruang_kerja() throws IOException {
        Files.createDirectories(direktori_kerja);
        Font fon_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        SUMBER.setFont(fon_VALUE); 출력.setFont(fon_VALUE); 출력.setEditable(false);
        SUMBER.setTabSize(4);
        SUMBER.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        SUMBER.setBackground(new Color(250, 251, 252));
        SUMBER.setForeground(new Color(32, 43, 58));
        JPanel perintah_panel = new JPanel();
        perintah_panel.add(new JLabel("Fail")); perintah_panel.add(fail_pemasukan_nama);
        perintah_panel.add(new JLabel("주 Kelas_VALUE")); perintah_panel.add(Kelas_pemasukan_nama);
        Butang(perintah_panel, "Buka", this::Buka); Butang(perintah_panel, "stor_VALUE", this::stor_VALUE);
        Butang(perintah_panel, "bina_sumber", () -> Terjemah_sumber(false, false));
        Butang(perintah_panel, "laksanakan_perintah", () -> Terjemah_sumber(true, false));
        Butang(perintah_panel, "laksanakan_perintah Fail cipta_pemasukan", () -> Terjemah_sumber(false, true));
        Butang(perintah_panel, "멈춤", this::멈춤);
        JSplitPane divisyen_ukuran = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(SUMBER), new JScrollPane(출력));
        divisyen_ukuran.setResizeWeight(0.75);
        Tetingkap.add(perintah_panel, BorderLayout.NORTH); Tetingkap.add(divisyen_ukuran, BorderLayout.CENTER);
        Tetingkap.setSize(1200, 750); Tetingkap.setLocationRelativeTo(null);
        Tetingkap.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Tetingkap.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Peristiwa) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Buka(); Tetingkap.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource fon_lalai = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object pemasukan_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(pemasukan_VALUE) instanceof Font) UIManager.put(pemasukan_VALUE, fon_lalai);
                }
                new ruang_kerja();
            } catch (Exception RALAT) { RALAT.printStackTrace(); }
        });
    }
}
