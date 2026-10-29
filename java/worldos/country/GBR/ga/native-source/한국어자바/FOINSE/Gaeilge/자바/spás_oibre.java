// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자바;

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

/** úsáideoir 홈에서 Java 원문을 cuir_in_eagar_VALUE·tóg_foinse·실행하는 작은 Swing spás_oibre. */
public final class spás_oibre {
    private final JFrame fuinneog = new JFrame("jkoros — 자바 spás_oibre");
    private final JTextArea FOINSE = new JTextArea();
    private final JTextArea Aschur = new JTextArea(8, 80);
    private final JTextField comhad_iontráil_ainm = new JTextField("인사.java", 20);
    private final JTextField aicme_iontráil_ainm = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Próiseas_VALUE;
    private final String leabharlann = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Téacs) { SwingUtilities.invokeLater(() -> Aschur.append(Téacs + "\n")); }
    private void cnaipe(JPanel leagan_VALUE, String Ainm, Runnable 행동) {
        JButton cnaipe = new JButton(Ainm);
        cnaipe.addActionListener(ócáid -> 행동.run());
        leagan_VALUE.add(cnaipe);
    }
    private boolean Store_VALUE() {
        try {
            Path CONAIR = 작업폴더.resolve(comhad_iontráil_ainm.getText());
            Files.createDirectories(CONAIR.getParent());
            Comhad.Scríobh(CONAIR, FOINSE.getText());
            알림("Store_VALUE: " + CONAIR);
            return true;
        } catch (Exception ERREÁID) { 알림(ERREÁID.toString()); return false; }
    }
    private void Oscail() {
        try { FOINSE.setText(Comhad.Léigh(작업폴더.resolve(comhad_iontráil_ainm.getText()))); }
        catch (Exception ERREÁID) { 알림(ERREÁID.toString()); }
    }
    private int Ordú(List<String> Ordú) throws Exception {
        Próiseas_VALUE = new ProcessBuilder(Ordú).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Líne = new BufferedReader(new InputStreamReader(Próiseas_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Téacs;
            while ((Téacs = Líne.readLine()) != null) 알림(Téacs);
        }
        int staid_VALUE = Próiseas_VALUE.waitFor(); Próiseas_VALUE = null;
        알림("scoir_clár CODE_VALUE: " + staid_VALUE);
        return staid_VALUE;
    }
    private void Aistrigh_foinse(boolean Rith_ordú, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = comhad_iontráil_ainm.getText(), iontráil_pointe_VALUE = aicme_iontráil_ainm.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Ordú(Arrays.asList("jclassc", "--target", "openjdk", "--entry", iontráil_pointe_VALUE,
                        "--classpath", leabharlann, "-o", "실행프로그램", 입력));
                } else if (Ordú(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", leabharlann,
                        "-d", "classes", 입력)) == 0 && Rith_ordú) {
                    Ordú(Arrays.asList("java", "-cp", "classes:" + leabharlann, iontráil_pointe_VALUE));
                }
            } catch (Exception ERREÁID) { 알림(ERREÁID.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Próiseas_VALUE;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private spás_oibre() throws IOException {
        Files.createDirectories(작업폴더);
        Font clófhoireann_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        FOINSE.setFont(clófhoireann_VALUE); Aschur.setFont(clófhoireann_VALUE); Aschur.setEditable(false);
        FOINSE.setTabSize(4);
        FOINSE.setMargin(new Insets(10, 12, 10, 12));
        Aschur.setMargin(new Insets(8, 12, 8, 12));
        FOINSE.setBackground(new Color(250, 251, 252));
        FOINSE.setForeground(new Color(32, 43, 58));
        JPanel ordú_painéal = new JPanel();
        ordú_painéal.add(new JLabel("Comhad")); ordú_painéal.add(comhad_iontráil_ainm);
        ordú_painéal.add(new JLabel("주 aicme_VALUE")); ordú_painéal.add(aicme_iontráil_ainm);
        cnaipe(ordú_painéal, "Oscail", this::Oscail); cnaipe(ordú_painéal, "Store_VALUE", this::Store_VALUE);
        cnaipe(ordú_painéal, "tóg_foinse", () -> Aistrigh_foinse(false, false));
        cnaipe(ordú_painéal, "Rith_ordú", () -> Aistrigh_foinse(true, false));
        cnaipe(ordú_painéal, "Rith_ordú Comhad Create_iontráil", () -> Aistrigh_foinse(false, true));
        cnaipe(ordú_painéal, "멈춤", this::멈춤);
        JSplitPane roinnt_tomhas = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(FOINSE), new JScrollPane(Aschur));
        roinnt_tomhas.setResizeWeight(0.75);
        fuinneog.add(ordú_painéal, BorderLayout.NORTH); fuinneog.add(roinnt_tomhas, BorderLayout.CENTER);
        fuinneog.setSize(1200, 750); fuinneog.setLocationRelativeTo(null);
        fuinneog.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        fuinneog.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ócáid) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Oscail(); fuinneog.setVisible(true);
    }
    public static void main(String[] Argóintí) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource clófhoireann_réamhshocraithe = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object iontráil_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(iontráil_VALUE) instanceof Font) UIManager.put(iontráil_VALUE, clófhoireann_réamhshocraithe);
                }
                new spás_oibre();
            } catch (Exception ERREÁID) { ERREÁID.printStackTrace(); }
        });
    }
}
