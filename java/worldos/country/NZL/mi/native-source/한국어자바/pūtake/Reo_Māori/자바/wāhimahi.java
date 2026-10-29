// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자바;

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

/** kaiwhakamahi 홈에서 Java 원문을 whakatika_uara·hanga_pūtake·실행하는 작은 Swing wāhimahi. */
public final class wāhimahi {
    private final JFrame matapihi = new JFrame("jkoros — 자바 wāhimahi");
    private final JTextArea pūtake = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField kōnae_tāurunga_ingoa = new JTextField("인사.java", 20);
    private final JTextField tauaha_tāurunga_ingoa = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Hātepe_uara;
    private final String puna = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Ngā_kupu) { SwingUtilities.invokeLater(() -> 출력.append(Ngā_kupu + "\n")); }
    private void pātene(JPanel putanga_uara, String Ingoa, Runnable 행동) {
        JButton pātene = new JButton(Ingoa);
        pātene.addActionListener(hui -> 행동.run());
        putanga_uara.add(pātene);
    }
    private boolean Store_uara() {
        try {
            Path ara = 작업폴더.resolve(kōnae_tāurunga_ingoa.getText());
            Files.createDirectories(ara.getParent());
            Kōnae.Tuhia(ara, pūtake.getText());
            알림("Store_uara: " + ara);
            return true;
        } catch (Exception Pōhēhē) { 알림(Pōhēhē.toString()); return false; }
    }
    private void Huaki() {
        try { pūtake.setText(Kōnae.Pānuitia(작업폴더.resolve(kōnae_tāurunga_ingoa.getText()))); }
        catch (Exception Pōhēhē) { 알림(Pōhēhē.toString()); }
    }
    private int tono(List<String> tono) throws Exception {
        Hātepe_uara = new ProcessBuilder(tono).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader hononga = new BufferedReader(new InputStreamReader(Hātepe_uara.getInputStream(), StandardCharsets.UTF_8))) {
            String Ngā_kupu;
            while ((Ngā_kupu = hononga.readLine()) != null) 알림(Ngā_kupu);
        }
        int tūnga_uara = Hātepe_uara.waitFor(); Hātepe_uara = null;
        알림("Putaatu_kaupapa CODE_uara: " + tūnga_uara);
        return tūnga_uara;
    }
    private void TRANSLATE_pūtake(boolean kawe_tono, boolean 실행파일) {
        if (!Store_uara()) return;
        String 입력 = kōnae_tāurunga_ingoa.getText(), tāurunga_ira_uara = tauaha_tāurunga_ingoa.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    tono(Arrays.asList("jclassc", "--target", "openjdk", "--entry", tāurunga_ira_uara,
                        "--classpath", puna, "-o", "실행프로그램", 입력));
                } else if (tono(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", puna,
                        "-d", "classes", 입력)) == 0 && kawe_tono) {
                    tono(Arrays.asList("java", "-cp", "classes:" + puna, tāurunga_ira_uara));
                }
            } catch (Exception Pōhēhē) { 알림(Pōhēhē.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Hātepe_uara;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private wāhimahi() throws IOException {
        Files.createDirectories(작업폴더);
        Font momotuhi_uara = new Font("Monospaced", Font.PLAIN, 16);
        pūtake.setFont(momotuhi_uara); 출력.setFont(momotuhi_uara); 출력.setEditable(false);
        pūtake.setTabSize(4);
        pūtake.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        pūtake.setBackground(new Color(250, 251, 252));
        pūtake.setForeground(new Color(32, 43, 58));
        JPanel tono_paepae = new JPanel();
        tono_paepae.add(new JLabel("Kōnae")); tono_paepae.add(kōnae_tāurunga_ingoa);
        tono_paepae.add(new JLabel("주 tauaha_uara")); tono_paepae.add(tauaha_tāurunga_ingoa);
        pātene(tono_paepae, "Huaki", this::Huaki); pātene(tono_paepae, "Store_uara", this::Store_uara);
        pātene(tono_paepae, "hanga_pūtake", () -> TRANSLATE_pūtake(false, false));
        pātene(tono_paepae, "kawe_tono", () -> TRANSLATE_pūtake(true, false));
        pātene(tono_paepae, "kawe_tono Kōnae Waihanga_tāurunga", () -> TRANSLATE_pūtake(false, true));
        pātene(tono_paepae, "멈춤", this::멈춤);
        JSplitPane whakawehenga_mēhua = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(pūtake), new JScrollPane(출력));
        whakawehenga_mēhua.setResizeWeight(0.75);
        matapihi.add(tono_paepae, BorderLayout.NORTH); matapihi.add(whakawehenga_mēhua, BorderLayout.CENTER);
        matapihi.setSize(1200, 750); matapihi.setLocationRelativeTo(null);
        matapihi.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        matapihi.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent hui) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Huaki(); matapihi.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource momotuhi_taunoa = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object tāurunga_uara : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(tāurunga_uara) instanceof Font) UIManager.put(tāurunga_uara, momotuhi_taunoa);
                }
                new wāhimahi();
            } catch (Exception Pōhēhē) { Pōhēhē.printStackTrace(); }
        });
    }
}
