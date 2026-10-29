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

/** aṣàmúlò 홈에서 Java 원문을 ṣàtúnṣe_iye·ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun·실행하는 작은 Swing ààyèiṣẹ́. */
public final class ààyèiṣẹ́ {
    private final JFrame wínńdò = new JFrame("jkoros — 자바 ààyèiṣẹ́");
    private final JTextArea orísun = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField fáìlì_ìgbéwọlé_orúkọ = new JTextField("인사.java", 20);
    private final JTextField ọ̀wọ́_ìgbéwọlé_orúkọ = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Ìlànà_iye;
    private final String ibi_ìpamọ́ = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String SMS) { SwingUtilities.invokeLater(() -> 출력.append(SMS + "\n")); }
    private void bọ́tìnnì(JPanel ẹ̀yà_iye, String Orúkọ, Runnable 행동) {
        JButton bọ́tìnnì = new JButton(Orúkọ);
        bọ́tìnnì.addActionListener(ìgbéṣẹ̀ -> 행동.run());
        ẹ̀yà_iye.add(bọ́tìnnì);
    }
    private boolean Store_iye() {
        try {
            Path ọ̀nà = 작업폴더.resolve(fáìlì_ìgbéwọlé_orúkọ.getText());
            Files.createDirectories(ọ̀nà.getParent());
            Fáìlì.Kọ(ọ̀nà, orísun.getText());
            알림("Store_iye: " + ọ̀nà);
            return true;
        } catch (Exception àṣìṣe) { 알림(àṣìṣe.toString()); return false; }
    }
    private void Ṣi() {
        try { orísun.setText(Fáìlì.Kàá(작업폴더.resolve(fáìlì_ìgbéwọlé_orúkọ.getText()))); }
        catch (Exception àṣìṣe) { 알림(àṣìṣe.toString()); }
    }
    private int Àṣẹ(List<String> Àṣẹ) throws Exception {
        Ìlànà_iye = new ProcessBuilder(Àṣẹ).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader ìlà = new BufferedReader(new InputStreamReader(Ìlànà_iye.getInputStream(), StandardCharsets.UTF_8))) {
            String SMS;
            while ((SMS = ìlà.readLine()) != null) 알림(SMS);
        }
        int ipò_iye = Ìlànà_iye.waitFor(); Ìlànà_iye = null;
        알림("jáde_àtòjọ_ètò 코드: " + ipò_iye);
        return ipò_iye;
    }
    private void Aṣàtúmọ̀_èdè_orísun(boolean ṣiṣẹ́_àṣẹ, boolean 실행파일) {
        if (!Store_iye()) return;
        String 입력 = fáìlì_ìgbéwọlé_orúkọ.getText(), ìgbéwọlé_kókó_iye = ọ̀wọ́_ìgbéwọlé_orúkọ.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Àṣẹ(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ìgbéwọlé_kókó_iye,
                        "--classpath", ibi_ìpamọ́, "-o", "실행프로그램", 입력));
                } else if (Àṣẹ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ibi_ìpamọ́,
                        "-d", "classes", 입력)) == 0 && ṣiṣẹ́_àṣẹ) {
                    Àṣẹ(Arrays.asList("java", "-cp", "classes:" + ibi_ìpamọ́, ìgbéwọlé_kókó_iye));
                }
            } catch (Exception àṣìṣe) { 알림(àṣìṣe.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Ìlànà_iye;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private ààyèiṣẹ́() throws IOException {
        Files.createDirectories(작업폴더);
        Font ìrísí_lẹ́tà_iye = new Font("Monospaced", Font.PLAIN, 16);
        orísun.setFont(ìrísí_lẹ́tà_iye); 출력.setFont(ìrísí_lẹ́tà_iye); 출력.setEditable(false);
        orísun.setTabSize(4);
        orísun.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        orísun.setBackground(new Color(250, 251, 252));
        orísun.setForeground(new Color(32, 43, 58));
        JPanel àṣẹ_pánẹ́ẹ̀lì = new JPanel();
        àṣẹ_pánẹ́ẹ̀lì.add(new JLabel("Fáìlì")); àṣẹ_pánẹ́ẹ̀lì.add(fáìlì_ìgbéwọlé_orúkọ);
        àṣẹ_pánẹ́ẹ̀lì.add(new JLabel("주 ọ̀wọ́_iye")); àṣẹ_pánẹ́ẹ̀lì.add(ọ̀wọ́_ìgbéwọlé_orúkọ);
        bọ́tìnnì(àṣẹ_pánẹ́ẹ̀lì, "Ṣi", this::Ṣi); bọ́tìnnì(àṣẹ_pánẹ́ẹ̀lì, "Store_iye", this::Store_iye);
        bọ́tìnnì(àṣẹ_pánẹ́ẹ̀lì, "ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun", () -> Aṣàtúmọ̀_èdè_orísun(false, false));
        bọ́tìnnì(àṣẹ_pánẹ́ẹ̀lì, "ṣiṣẹ́_àṣẹ", () -> Aṣàtúmọ̀_èdè_orísun(true, false));
        bọ́tìnnì(àṣẹ_pánẹ́ẹ̀lì, "ṣiṣẹ́_àṣẹ Fáìlì Ṣẹ̀dá_ìgbéwọlé", () -> Aṣàtúmọ̀_èdè_orísun(false, true));
        bọ́tìnnì(àṣẹ_pánẹ́ẹ̀lì, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(orísun), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        wínńdò.add(àṣẹ_pánẹ́ẹ̀lì, BorderLayout.NORTH); wínńdò.add(나눔, BorderLayout.CENTER);
        wínńdò.setSize(1200, 750); wínńdò.setLocationRelativeTo(null);
        wínńdò.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        wínńdò.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ìgbéṣẹ̀) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Ṣi(); wínńdò.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ìrísí_lẹ́tà_àkùnàyàn = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ìgbéwọlé_iye : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ìgbéwọlé_iye) instanceof Font) UIManager.put(ìgbéwọlé_iye, ìrísí_lẹ́tà_àkùnàyàn);
                }
                new ààyèiṣẹ́();
            } catch (Exception àṣìṣe) { àṣìṣe.printStackTrace(); }
        });
    }
}
