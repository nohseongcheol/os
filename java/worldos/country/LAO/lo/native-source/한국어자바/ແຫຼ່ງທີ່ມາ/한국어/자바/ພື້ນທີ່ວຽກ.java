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

/** ຜູ້ໃຊ້ 홈에서 Java 원문을 ແກ້ໄຂ_ຄ່າ·ສ້າງ_ແຫຼ່ງທີ່ມາ·실행하는 작은 Swing ພື້ນທີ່ວຽກ. */
public final class ພື້ນທີ່ວຽກ {
    private final JFrame ວິນໂດ = new JFrame("jkoros — 자바 ພື້ນທີ່ວຽກ");
    private final JTextArea ແຫຼ່ງທີ່ມາ = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField ຟາຍ_ເຂົ້າໃນ_ຊື່ = new JTextField("인사.java", 20);
    private final JTextField ປະເພດສິ່ງຂອງ_ເຂົ້າໃນ_ຊື່ = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process ຂະ_ບວນ_ການ_ຄ່າ;
    private final String ຫໍສະຫມຸດ = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String ຂໍ້ຄວາມ) { SwingUtilities.invokeLater(() -> 출력.append(ຂໍ້ຄວາມ + "\n")); }
    private void ປຸ່ມ(JPanel 판, String ຊື່, Runnable 행동) {
        JButton ປຸ່ມ = new JButton(ຊື່);
        ປຸ່ມ.addActionListener(ງານ -> 행동.run());
        판.add(ປຸ່ມ);
    }
    private boolean ຮ້ານຄ້າ_ຄ່າ() {
        try {
            Path ທາງໂຄຈອນ = 작업폴더.resolve(ຟາຍ_ເຂົ້າໃນ_ຊື່.getText());
            Files.createDirectories(ທາງໂຄຈອນ.getParent());
            ຟາຍ.ຂຽນ(ທາງໂຄຈອນ, ແຫຼ່ງທີ່ມາ.getText());
            알림("ຮ້ານຄ້າ_ຄ່າ: " + ທາງໂຄຈອນ);
            return true;
        } catch (Exception ຂໍ້ຜິດພາດ) { 알림(ຂໍ້ຜິດພາດ.toString()); return false; }
    }
    private void ສ້າງ() {
        try { ແຫຼ່ງທີ່ມາ.setText(ຟາຍ.읽기(작업폴더.resolve(ຟາຍ_ເຂົ້າໃນ_ຊື່.getText()))); }
        catch (Exception ຂໍ້ຜິດພາດ) { 알림(ຂໍ້ຜິດພາດ.toString()); }
    }
    private int ຄໍາສັ່ງ_1f12b8e2(List<String> ຄໍາສັ່ງ_1f12b8e2) throws Exception {
        ຂະ_ບວນ_ການ_ຄ່າ = new ProcessBuilder(ຄໍາສັ່ງ_1f12b8e2).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader ສາຍ = new BufferedReader(new InputStreamReader(ຂະ_ບວນ_ການ_ຄ່າ.getInputStream(), StandardCharsets.UTF_8))) {
            String ຂໍ້ຄວາມ;
            while ((ຂໍ້ຄວາມ = ສາຍ.readLine()) != null) 알림(ຂໍ້ຄວາມ);
        }
        int ສະຖານະ_ຄ່າ = ຂະ_ບວນ_ການ_ຄ່າ.waitFor(); ຂະ_ບວນ_ການ_ຄ່າ = null;
        알림("ອອກ_ແອັບ ລະຫັດ_ຄ່າ: " + ສະຖານະ_ຄ່າ);
        return ສະຖານະ_ຄ່າ;
    }
    private void ແປພາສາ_ແຫຼ່ງທີ່ມາ(boolean ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ, boolean 실행파일) {
        if (!ຮ້ານຄ້າ_ຄ່າ()) return;
        String 입력 = ຟາຍ_ເຂົ້າໃນ_ຊື່.getText(), ເຂົ້າໃນ_ຈຸດ_ຄ່າ = ປະເພດສິ່ງຂອງ_ເຂົ້າໃນ_ຊື່.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    ຄໍາສັ່ງ_1f12b8e2(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ເຂົ້າໃນ_ຈຸດ_ຄ່າ,
                        "--classpath", ຫໍສະຫມຸດ, "-o", "실행프로그램", 입력));
                } else if (ຄໍາສັ່ງ_1f12b8e2(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ຫໍສະຫມຸດ,
                        "-d", "classes", 입력)) == 0 && ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ) {
                    ຄໍາສັ່ງ_1f12b8e2(Arrays.asList("java", "-cp", "classes:" + ຫໍສະຫມຸດ, ເຂົ້າໃນ_ຈຸດ_ຄ່າ));
                }
            } catch (Exception ຂໍ້ຜິດພາດ) { 알림(ຂໍ້ຜິດພາດ.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = ຂະ_ບວນ_ການ_ຄ່າ;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private ພື້ນທີ່ວຽກ() throws IOException {
        Files.createDirectories(작업폴더);
        Font ຮູບແບບຕົວຫນັງສື_ຄ່າ = new Font("Monospaced", Font.PLAIN, 16);
        ແຫຼ່ງທີ່ມາ.setFont(ຮູບແບບຕົວຫນັງສື_ຄ່າ); 출력.setFont(ຮູບແບບຕົວຫນັງສື_ຄ່າ); 출력.setEditable(false);
        ແຫຼ່ງທີ່ມາ.setTabSize(4);
        ແຫຼ່ງທີ່ມາ.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        ແຫຼ່ງທີ່ມາ.setBackground(new Color(250, 251, 252));
        ແຫຼ່ງທີ່ມາ.setForeground(new Color(32, 43, 58));
        JPanel ຄໍາສັ່ງ_ແຜງ = new JPanel();
        ຄໍາສັ່ງ_ແຜງ.add(new JLabel("ຟາຍ")); ຄໍາສັ່ງ_ແຜງ.add(ຟາຍ_ເຂົ້າໃນ_ຊື່);
        ຄໍາສັ່ງ_ແຜງ.add(new JLabel("주 ປະເພດສິ່ງຂອງ_ຄ່າ")); ຄໍາສັ່ງ_ແຜງ.add(ປະເພດສິ່ງຂອງ_ເຂົ້າໃນ_ຊື່);
        ປຸ່ມ(ຄໍາສັ່ງ_ແຜງ, "ສ້າງ", this::ສ້າງ); ປຸ່ມ(ຄໍາສັ່ງ_ແຜງ, "ຮ້ານຄ້າ_ຄ່າ", this::ຮ້ານຄ້າ_ຄ່າ);
        ປຸ່ມ(ຄໍາສັ່ງ_ແຜງ, "ສ້າງ_ແຫຼ່ງທີ່ມາ", () -> ແປພາສາ_ແຫຼ່ງທີ່ມາ(false, false));
        ປຸ່ມ(ຄໍາສັ່ງ_ແຜງ, "ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ", () -> ແປພາສາ_ແຫຼ່ງທີ່ມາ(true, false));
        ປຸ່ມ(ຄໍາສັ່ງ_ແຜງ, "ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ ຟາຍ ສ້າງ_ເຂົ້າໃນ", () -> ແປພາສາ_ແຫຼ່ງທີ່ມາ(false, true));
        ປຸ່ມ(ຄໍາສັ່ງ_ແຜງ, "멈춤", this::멈춤);
        JSplitPane ການຫານ_ມາດຕະການ = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ແຫຼ່ງທີ່ມາ), new JScrollPane(출력));
        ການຫານ_ມາດຕະການ.setResizeWeight(0.75);
        ວິນໂດ.add(ຄໍາສັ່ງ_ແຜງ, BorderLayout.NORTH); ວິນໂດ.add(ການຫານ_ມາດຕະການ, BorderLayout.CENTER);
        ວິນໂດ.setSize(1200, 750); ວິນໂດ.setLocationRelativeTo(null);
        ວິນໂດ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ວິນໂດ.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ງານ) { 멈춤(); 일꾼.shutdownNow(); }
        });
        ສ້າງ(); ວິນໂດ.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ຟອນເລີ່ມຕົ້ນ = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ເຂົ້າໃນ_ຄ່າ : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ເຂົ້າໃນ_ຄ່າ) instanceof Font) UIManager.put(ເຂົ້າໃນ_ຄ່າ, ຟອນເລີ່ມຕົ້ນ);
                }
                new ພື້ນທີ່ວຽກ();
            } catch (Exception ຂໍ້ຜິດພາດ) { ຂໍ້ຜິດພາດ.printStackTrace(); }
        });
    }
}
