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

/** ulanyjy 홈에서 Java 원문을 redaktirle_baha·düz_gor·실행하는 작은 Swing iş_ýeri. */
public final class iş_ýeri {
    private final JFrame penjire = new JFrame("jkoros — 자바 iş_ýeri");
    private final JTextArea Çeşme = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField faýl_girizmeklik_at = new JTextField("인사.java", 20);
    private final JTextField klas_girizmeklik_at = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Proses_baha;
    private final String Kitaphana = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Metin) { SwingUtilities.invokeLater(() -> 출력.append(Metin + "\n")); }
    private void düwme(JPanel wersiýa_baha, String Ad, Runnable 행동) {
        JButton düwme = new JButton(Ad);
        düwme.addActionListener(waka -> 행동.run());
        wersiýa_baha.add(düwme);
    }
    private boolean Store_baha() {
        try {
            Path Ýol = 작업폴더.resolve(faýl_girizmeklik_at.getText());
            Files.createDirectories(Ýol.getParent());
            Faýl.Ýaz(Ýol, Çeşme.getText());
            알림("Store_baha: " + Ýol);
            return true;
        } catch (Exception Hata) { 알림(Hata.toString()); return false; }
    }
    private void Aç() {
        try { Çeşme.setText(Faýl.Oka(작업폴더.resolve(faýl_girizmeklik_at.getText()))); }
        catch (Exception Hata) { 알림(Hata.toString()); }
    }
    private int buýruk(List<String> buýruk) throws Exception {
        Proses_baha = new ProcessBuilder(buýruk).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader setir = new BufferedReader(new InputStreamReader(Proses_baha.getInputStream(), StandardCharsets.UTF_8))) {
            String Metin;
            while ((Metin = setir.readLine()) != null) 알림(Metin);
        }
        int ýagdaý_baha = Proses_baha.waitFor(); Proses_baha = null;
        알림("çyk_programma 코드: " + ýagdaý_baha);
        return ýagdaý_baha;
    }
    private void Terjime_gor(boolean ýerine_ýetir_buýruk, boolean 실행파일) {
        if (!Store_baha()) return;
        String 입력 = faýl_girizmeklik_at.getText(), girizmeklik_utuk_baha = klas_girizmeklik_at.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    buýruk(Arrays.asList("jclassc", "--target", "openjdk", "--entry", girizmeklik_utuk_baha,
                        "--classpath", Kitaphana, "-o", "실행프로그램", 입력));
                } else if (buýruk(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", Kitaphana,
                        "-d", "classes", 입력)) == 0 && ýerine_ýetir_buýruk) {
                    buýruk(Arrays.asList("java", "-cp", "classes:" + Kitaphana, girizmeklik_utuk_baha));
                }
            } catch (Exception Hata) { 알림(Hata.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Proses_baha;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private iş_ýeri() throws IOException {
        Files.createDirectories(작업폴더);
        Font şrift_baha = new Font("Monospaced", Font.PLAIN, 16);
        Çeşme.setFont(şrift_baha); 출력.setFont(şrift_baha); 출력.setEditable(false);
        Çeşme.setTabSize(4);
        Çeşme.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        Çeşme.setBackground(new Color(250, 251, 252));
        Çeşme.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("Faýl")); 명령판.add(faýl_girizmeklik_at);
        명령판.add(new JLabel("주 klas_baha")); 명령판.add(klas_girizmeklik_at);
        düwme(명령판, "Aç", this::Aç); düwme(명령판, "Store_baha", this::Store_baha);
        düwme(명령판, "düz_gor", () -> Terjime_gor(false, false));
        düwme(명령판, "ýerine_ýetir_buýruk", () -> Terjime_gor(true, false));
        düwme(명령판, "ýerine_ýetir_buýruk Faýl döretmek_girizmeklik", () -> Terjime_gor(false, true));
        düwme(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Çeşme), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        penjire.add(명령판, BorderLayout.NORTH); penjire.add(나눔, BorderLayout.CENTER);
        penjire.setSize(1200, 750); penjire.setLocationRelativeTo(null);
        penjire.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        penjire.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent waka) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Aç(); penjire.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource öňünden_kabul_edilen_şrift = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object girizmeklik_baha : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(girizmeklik_baha) instanceof Font) UIManager.put(girizmeklik_baha, öňünden_kabul_edilen_şrift);
                }
                new iş_ýeri();
            } catch (Exception Hata) { Hata.printStackTrace(); }
        });
    }
}
