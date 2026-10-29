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

/** cleachdaiche 홈에서 Java 원문을 deasaich_VALUE·tog_tùs·실행하는 작은 Swing spàs_obrach. */
public final class spàs_obrach {
    private final JFrame uinneag = new JFrame("jkoros — 자바 spàs_obrach");
    private final JTextArea tùs = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField faidhle_cur_a_steach_ainm = new JTextField("인사.java", 20);
    private final JTextField clas_cur_a_steach_ainm = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Pròiseas_VALUE;
    private final String leabhar_lann = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String SMS) { SwingUtilities.invokeLater(() -> 출력.append(SMS + "\n")); }
    private void putan(JPanel tionndadh_VALUE, String Ainm, Runnable 행동) {
        JButton putan = new JButton(Ainm);
        putan.addActionListener(tachartas -> 행동.run());
        tionndadh_VALUE.add(putan);
    }
    private boolean Store_VALUE() {
        try {
            Path Slighe = 작업폴더.resolve(faidhle_cur_a_steach_ainm.getText());
            Files.createDirectories(Slighe.getParent());
            faidhle.sgrìobh(Slighe, tùs.getText());
            알림("Store_VALUE: " + Slighe);
            return true;
        } catch (Exception Mearachd) { 알림(Mearachd.toString()); return false; }
    }
    private void fosgail() {
        try { tùs.setText(faidhle.읽기(작업폴더.resolve(faidhle_cur_a_steach_ainm.getText()))); }
        catch (Exception Mearachd) { 알림(Mearachd.toString()); }
    }
    private int àithne(List<String> àithne) throws Exception {
        Pròiseas_VALUE = new ProcessBuilder(àithne).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader loidhne = new BufferedReader(new InputStreamReader(Pròiseas_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String SMS;
            while ((SMS = loidhne.readLine()) != null) 알림(SMS);
        }
        int cor_VALUE = Pròiseas_VALUE.waitFor(); Pròiseas_VALUE = null;
        알림("fàg_ap CODE_VALUE: " + cor_VALUE);
        return cor_VALUE;
    }
    private void TRANSLATE_tùs(boolean gnìomhaich_àithne, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = faidhle_cur_a_steach_ainm.getText(), cur_a_steach_puing_VALUE = clas_cur_a_steach_ainm.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    àithne(Arrays.asList("jclassc", "--target", "openjdk", "--entry", cur_a_steach_puing_VALUE,
                        "--classpath", leabhar_lann, "-o", "실행프로그램", 입력));
                } else if (àithne(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", leabhar_lann,
                        "-d", "classes", 입력)) == 0 && gnìomhaich_àithne) {
                    àithne(Arrays.asList("java", "-cp", "classes:" + leabhar_lann, cur_a_steach_puing_VALUE));
                }
            } catch (Exception Mearachd) { 알림(Mearachd.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Pròiseas_VALUE;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private spàs_obrach() throws IOException {
        Files.createDirectories(작업폴더);
        Font cruth_clò_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        tùs.setFont(cruth_clò_VALUE); 출력.setFont(cruth_clò_VALUE); 출력.setEditable(false);
        tùs.setTabSize(4);
        tùs.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        tùs.setBackground(new Color(250, 251, 252));
        tùs.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("faidhle")); 명령판.add(faidhle_cur_a_steach_ainm);
        명령판.add(new JLabel("주 clas_VALUE")); 명령판.add(clas_cur_a_steach_ainm);
        putan(명령판, "fosgail", this::fosgail); putan(명령판, "Store_VALUE", this::Store_VALUE);
        putan(명령판, "tog_tùs", () -> TRANSLATE_tùs(false, false));
        putan(명령판, "gnìomhaich_àithne", () -> TRANSLATE_tùs(true, false));
        putan(명령판, "gnìomhaich_àithne faidhle Create_cur_a_steach", () -> TRANSLATE_tùs(false, true));
        putan(명령판, "멈춤", this::멈춤);
        JSplitPane roinneadh_tomhas = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(tùs), new JScrollPane(출력));
        roinneadh_tomhas.setResizeWeight(0.75);
        uinneag.add(명령판, BorderLayout.NORTH); uinneag.add(roinneadh_tomhas, BorderLayout.CENTER);
        uinneag.setSize(1200, 750); uinneag.setLocationRelativeTo(null);
        uinneag.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        uinneag.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent tachartas) { 멈춤(); 일꾼.shutdownNow(); }
        });
        fosgail(); uinneag.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource cruth_clò_bunaiteach = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object cur_a_steach_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(cur_a_steach_VALUE) instanceof Font) UIManager.put(cur_a_steach_VALUE, cruth_clò_bunaiteach);
                }
                new spàs_obrach();
            } catch (Exception Mearachd) { Mearachd.printStackTrace(); }
        });
    }
}
