// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자바;

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

/** umsebenzisi 홈에서 Java 원문을 hlela_ixabiso·yakha_umthombo·실행하는 작은 Swing indawo_yomsebenzi. */
public final class indawo_yomsebenzi {
    private final JFrame i_window = new JFrame("jkoros — 자바 indawo_yomsebenzi");
    private final JTextArea UMTHOMBO = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField ifayile_ufako_nkcukacha_igama = new JTextField("인사.java", 20);
    private final JTextField iklasi_ufako_nkcukacha_igama = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Inkqubo_ixabiso;
    private final String ilayibhrari = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Umbhalo) { SwingUtilities.invokeLater(() -> 출력.append(Umbhalo + "\n")); }
    private void iqhosha(JPanel inguqulelo_ixabiso, String Igama, Runnable 행동) {
        JButton iqhosha = new JButton(Igama);
        iqhosha.addActionListener(umcimbi -> 행동.run());
        inguqulelo_ixabiso.add(iqhosha);
    }
    private boolean Store_ixabiso() {
        try {
            Path INDLELA = 작업폴더.resolve(ifayile_ufako_nkcukacha_igama.getText());
            Files.createDirectories(INDLELA.getParent());
            iFayili.Bhala(INDLELA, UMTHOMBO.getText());
            알림("Store_ixabiso: " + INDLELA);
            return true;
        } catch (Exception Impazamo) { 알림(Impazamo.toString()); return false; }
    }
    private void Vula() {
        try { UMTHOMBO.setText(iFayili.Funda(작업폴더.resolve(ifayile_ufako_nkcukacha_igama.getText()))); }
        catch (Exception Impazamo) { 알림(Impazamo.toString()); }
    }
    private int Umyalelo(List<String> Umyalelo) throws Exception {
        Inkqubo_ixabiso = new ProcessBuilder(Umyalelo).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader umgca = new BufferedReader(new InputStreamReader(Inkqubo_ixabiso.getInputStream(), StandardCharsets.UTF_8))) {
            String Umbhalo;
            while ((Umbhalo = umgca.readLine()) != null) 알림(Umbhalo);
        }
        int imo_ixabiso = Inkqubo_ixabiso.waitFor(); Inkqubo_ixabiso = null;
        알림("phuma_inkqubo 코드: " + imo_ixabiso);
        return imo_ixabiso;
    }
    private void Ukuguqulela_umthombo(boolean ukwenza_umyalelo, boolean 실행파일) {
        if (!Store_ixabiso()) return;
        String 입력 = ifayile_ufako_nkcukacha_igama.getText(), ufako_nkcukacha_inqaku_ixabiso = iklasi_ufako_nkcukacha_igama.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Umyalelo(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ufako_nkcukacha_inqaku_ixabiso,
                        "--classpath", ilayibhrari, "-o", "실행프로그램", 입력));
                } else if (Umyalelo(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ilayibhrari,
                        "-d", "classes", 입력)) == 0 && ukwenza_umyalelo) {
                    Umyalelo(Arrays.asList("java", "-cp", "classes:" + ilayibhrari, ufako_nkcukacha_inqaku_ixabiso));
                }
            } catch (Exception Impazamo) { 알림(Impazamo.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Inkqubo_ixabiso;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private indawo_yomsebenzi() throws IOException {
        Files.createDirectories(작업폴더);
        Font ifonti_ixabiso = new Font("Monospaced", Font.PLAIN, 16);
        UMTHOMBO.setFont(ifonti_ixabiso); 출력.setFont(ifonti_ixabiso); 출력.setEditable(false);
        UMTHOMBO.setTabSize(4);
        UMTHOMBO.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        UMTHOMBO.setBackground(new Color(250, 251, 252));
        UMTHOMBO.setForeground(new Color(32, 43, 58));
        JPanel umyalelo_iphaneli = new JPanel();
        umyalelo_iphaneli.add(new JLabel("iFayili")); umyalelo_iphaneli.add(ifayile_ufako_nkcukacha_igama);
        umyalelo_iphaneli.add(new JLabel("주 iklasi_ixabiso")); umyalelo_iphaneli.add(iklasi_ufako_nkcukacha_igama);
        iqhosha(umyalelo_iphaneli, "Vula", this::Vula); iqhosha(umyalelo_iphaneli, "Store_ixabiso", this::Store_ixabiso);
        iqhosha(umyalelo_iphaneli, "yakha_umthombo", () -> Ukuguqulela_umthombo(false, false));
        iqhosha(umyalelo_iphaneli, "ukwenza_umyalelo", () -> Ukuguqulela_umthombo(true, false));
        iqhosha(umyalelo_iphaneli, "ukwenza_umyalelo iFayili yila_ufako_nkcukacha", () -> Ukuguqulela_umthombo(false, true));
        iqhosha(umyalelo_iphaneli, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(UMTHOMBO), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        i_window.add(umyalelo_iphaneli, BorderLayout.NORTH); i_window.add(나눔, BorderLayout.CENTER);
        i_window.setSize(1200, 750); i_window.setLocationRelativeTo(null);
        i_window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        i_window.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent umcimbi) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Vula(); i_window.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ifonti_ehleli_ihleli = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ufako_nkcukacha_ixabiso : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ufako_nkcukacha_ixabiso) instanceof Font) UIManager.put(ufako_nkcukacha_ixabiso, ifonti_ehleli_ihleli);
                }
                new indawo_yomsebenzi();
            } catch (Exception Impazamo) { Impazamo.printStackTrace(); }
        });
    }
}
