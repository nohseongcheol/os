// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.자바;

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

/** ruang_pengguna 홈에서 Java 원문을 Edit_VALUE·bangun_sumber·실행하는 작은 Swing workspace. */
public final class workspace {
    private final JFrame Jendela = new JFrame("jkoros — 자바 workspace");
    private final JTextArea kodeSumber = new JTextArea();
    private final JTextArea keluaranTeks = new JTextArea(8, 80);
    private final JTextField file_entri_nama = new JTextField("인사.java", 20);
    private final JTextField Kelas_entri_nama = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Proses_VALUE;
    private final String pustaka = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String teks) { SwingUtilities.invokeLater(() -> keluaranTeks.append(teks + "\n")); }
    private void tombol(JPanel versi_VALUE, String Nama_2, Runnable 행동) {
        JButton tombol = new JButton(Nama_2);
        tombol.addActionListener(Even -> 행동.run());
        versi_VALUE.add(tombol);
    }
    private boolean Store_VALUE() {
        try {
            Path jalur = 작업폴더.resolve(file_entri_nama.getText());
            Files.createDirectories(jalur.getParent());
            berkas.Tulis(jalur, kodeSumber.getText());
            알림("Store_VALUE: " + jalur);
            return true;
        } catch (Exception galat) { 알림(galat.toString()); return false; }
    }
    private void Buka() {
        try { kodeSumber.setText(berkas.Baca(작업폴더.resolve(file_entri_nama.getText()))); }
        catch (Exception galat) { 알림(galat.toString()); }
    }
    private int perintah(List<String> perintah) throws Exception {
        Proses_VALUE = new ProcessBuilder(perintah).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader baris_masukan = new BufferedReader(new InputStreamReader(Proses_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String teks;
            while ((teks = baris_masukan.readLine()) != null) 알림(teks);
        }
        int Status_VALUE = Proses_VALUE.waitFor(); Proses_VALUE = null;
        알림("Keluar_apl CODE_VALUE: " + Status_VALUE);
        return Status_VALUE;
    }
    private void TRANSLATE_sumber(boolean Jalankan_perintah, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = file_entri_nama.getText(), entri_p_VALUE = Kelas_entri_nama.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    perintah(Arrays.asList("jclassc", "--target", "openjdk", "--entry", entri_p_VALUE,
                        "--classpath", pustaka, "-o", "실행프로그램", 입력));
                } else if (perintah(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", pustaka,
                        "-d", "classes", 입력)) == 0 && Jalankan_perintah) {
                    perintah(Arrays.asList("java", "-cp", "classes:" + pustaka, entri_p_VALUE));
                }
            } catch (Exception galat) { 알림(galat.toString()); }
        });
    }
    private void 멈춤() {
        Process saat_ini_item = Proses_VALUE;
        if (saat_ini_item != null) { saat_ini_item.descendants().forEach(ProcessHandle::destroy); saat_ini_item.destroy(); }
    }
    private workspace() throws IOException {
        Files.createDirectories(작업폴더);
        Font font_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        kodeSumber.setFont(font_VALUE); keluaranTeks.setFont(font_VALUE); keluaranTeks.setEditable(false);
        kodeSumber.setTabSize(4);
        kodeSumber.setMargin(new Insets(10, 12, 10, 12));
        keluaranTeks.setMargin(new Insets(8, 12, 8, 12));
        kodeSumber.setBackground(new Color(250, 251, 252));
        kodeSumber.setForeground(new Color(32, 43, 58));
        JPanel perintah_panel = new JPanel();
        perintah_panel.add(new JLabel("berkas")); perintah_panel.add(file_entri_nama);
        perintah_panel.add(new JLabel("주 Kelas_VALUE")); perintah_panel.add(Kelas_entri_nama);
        tombol(perintah_panel, "Buka", this::Buka); tombol(perintah_panel, "Store_VALUE", this::Store_VALUE);
        tombol(perintah_panel, "bangun_sumber", () -> TRANSLATE_sumber(false, false));
        tombol(perintah_panel, "Jalankan_perintah", () -> TRANSLATE_sumber(true, false));
        tombol(perintah_panel, "Jalankan_perintah berkas Buat_entri", () -> TRANSLATE_sumber(false, true));
        tombol(perintah_panel, "멈춤", this::멈춤);
        JSplitPane Divisi_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(kodeSumber), new JScrollPane(keluaranTeks));
        Divisi_KR.setResizeWeight(0.75);
        Jendela.add(perintah_panel, BorderLayout.NORTH); Jendela.add(Divisi_KR, BorderLayout.CENTER);
        Jendela.setSize(1200, 750); Jendela.setLocationRelativeTo(null);
        Jendela.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Jendela.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Even) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Buka(); Jendela.setVisible(true);
    }
    public static void main(String[] argumen) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource font_default = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object entri_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(entri_VALUE) instanceof Font) UIManager.put(entri_VALUE, font_default);
                }
                new workspace();
            } catch (Exception galat) { galat.printStackTrace(); }
        });
    }
}
