// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.자바;

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

/** ผู้ใช้ 홈에서 Java 원문을 แก้ไข_ค่า·คอมไพล์_แหล่ง·실행하는 작은 Swing พื้นที่ทํางาน. */
public final class พื้นที่ทํางาน {
    private final JFrame หน้าต่าง = new JFrame("jkoros — 자바 พื้นที่ทํางาน");
    private final JTextArea รหัสต้นฉบับ = new JTextArea();
    private final JTextArea ข้อความออก = new JTextArea(8, 80);
    private final JTextField แฟ้ม_รายการ_ชื่อ = new JTextField("인사.java", 20);
    private final JTextField คลาส_รายการ_ชื่อ = new JTextField("인사", 16);
    private final Path ไดเรกทอรีการทํางาน = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService ผู้ปฏิบัติงาน_ค่า = Executors.newSingleThreadExecutor();
    private volatile Process กระบวนการ_ค่า;
    private final String ไลบรารี = "/opt/jkoros/lib/한국어자바.jar";

    private void ข้อสังเกต(String ข้อความ) { SwingUtilities.invokeLater(() -> ข้อความออก.append(ข้อความ + "\n")); }
    private void ปุ่ม(JPanel รุ่น_ค่า, String ชื่อ, Runnable 행동) {
        JButton ปุ่ม = new JButton(ชื่อ);
        ปุ่ม.addActionListener(เหตุการณ์ -> 행동.run());
        รุ่น_ค่า.add(ปุ่ม);
    }
    private boolean เก็บ_ค่า() {
        try {
            Path เส้นทาง = ไดเรกทอรีการทํางาน.resolve(แฟ้ม_รายการ_ชื่อ.getText());
            Files.createDirectories(เส้นทาง.getParent());
            แฟ้ม.เขียน(เส้นทาง, รหัสต้นฉบับ.getText());
            ข้อสังเกต("เก็บ_ค่า: " + เส้นทาง);
            return true;
        } catch (Exception ข้อผิดพลาด) { ข้อสังเกต(ข้อผิดพลาด.toString()); return false; }
    }
    private void เปิด() {
        try { รหัสต้นฉบับ.setText(แฟ้ม.อ่าน(ไดเรกทอรีการทํางาน.resolve(แฟ้ม_รายการ_ชื่อ.getText()))); }
        catch (Exception ข้อผิดพลาด) { ข้อสังเกต(ข้อผิดพลาด.toString()); }
    }
    private int คําสั่ง(List<String> คําสั่ง) throws Exception {
        กระบวนการ_ค่า = new ProcessBuilder(คําสั่ง).directory(ไดเรกทอรีการทํางาน.toFile()).redirectErrorStream(true).start();
        try (BufferedReader บรรทัด = new BufferedReader(new InputStreamReader(กระบวนการ_ค่า.getInputStream(), StandardCharsets.UTF_8))) {
            String ข้อความ;
            while ((ข้อความ = บรรทัด.readLine()) != null) ข้อสังเกต(ข้อความ);
        }
        int สถานะ_ค่า = กระบวนการ_ค่า.waitFor(); กระบวนการ_ค่า = null;
        ข้อสังเกต("ออก_แอป รหัส_ค่า: " + สถานะ_ค่า);
        return สถานะ_ค่า;
    }
    private void แปล_แหล่ง(boolean ดําเนินการ_คําสั่ง, boolean แฟ้มปฏิบัติการ) {
        if (!เก็บ_ค่า()) return;
        String 입력 = แฟ้ม_รายการ_ชื่อ.getText(), จุดเข้าใช้งาน_ค่า = คลาส_รายการ_ชื่อ.getText();
        ผู้ปฏิบัติงาน_ค่า.submit(() -> {
            try {
                Files.createDirectories(ไดเรกทอรีการทํางาน.resolve("classes"));
                if (แฟ้มปฏิบัติการ) {
                    คําสั่ง(Arrays.asList("jclassc", "--target", "openjdk", "--entry", จุดเข้าใช้งาน_ค่า,
                        "--classpath", ไลบรารี, "-o", "실행프로그램", 입력));
                } else if (คําสั่ง(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ไลบรารี,
                        "-d", "classes", 입력)) == 0 && ดําเนินการ_คําสั่ง) {
                    คําสั่ง(Arrays.asList("java", "-cp", "classes:" + ไลบรารี, จุดเข้าใช้งาน_ค่า));
                }
            } catch (Exception ข้อผิดพลาด) { ข้อสังเกต(ข้อผิดพลาด.toString()); }
        });
    }
    private void 멈춤() {
        Process ปัจจุบัน_รายการ = กระบวนการ_ค่า;
        if (ปัจจุบัน_รายการ != null) { ปัจจุบัน_รายการ.descendants().forEach(ProcessHandle::destroy); ปัจจุบัน_รายการ.destroy(); }
    }
    private พื้นที่ทํางาน() throws IOException {
        Files.createDirectories(ไดเรกทอรีการทํางาน);
        Font ฟอนต์_ค่า = new Font("Monospaced", Font.PLAIN, 16);
        รหัสต้นฉบับ.setFont(ฟอนต์_ค่า); ข้อความออก.setFont(ฟอนต์_ค่า); ข้อความออก.setEditable(false);
        รหัสต้นฉบับ.setTabSize(4);
        รหัสต้นฉบับ.setMargin(new Insets(10, 12, 10, 12));
        ข้อความออก.setMargin(new Insets(8, 12, 8, 12));
        รหัสต้นฉบับ.setBackground(new Color(250, 251, 252));
        รหัสต้นฉบับ.setForeground(new Color(32, 43, 58));
        JPanel คําสั่ง_แผง = new JPanel();
        คําสั่ง_แผง.add(new JLabel("แฟ้ม")); คําสั่ง_แผง.add(แฟ้ม_รายการ_ชื่อ);
        คําสั่ง_แผง.add(new JLabel("주 คลาส_ค่า")); คําสั่ง_แผง.add(คลาส_รายการ_ชื่อ);
        ปุ่ม(คําสั่ง_แผง, "เปิด", this::เปิด); ปุ่ม(คําสั่ง_แผง, "เก็บ_ค่า", this::เก็บ_ค่า);
        ปุ่ม(คําสั่ง_แผง, "คอมไพล์_แหล่ง", () -> แปล_แหล่ง(false, false));
        ปุ่ม(คําสั่ง_แผง, "ดําเนินการ_คําสั่ง", () -> แปล_แหล่ง(true, false));
        ปุ่ม(คําสั่ง_แผง, "ดําเนินการ_คําสั่ง แฟ้ม เปิด_รายการ", () -> แปล_แหล่ง(false, true));
        ปุ่ม(คําสั่ง_แผง, "멈춤", this::멈춤);
        JSplitPane ฝ่าย_เมตริก = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(รหัสต้นฉบับ), new JScrollPane(ข้อความออก));
        ฝ่าย_เมตริก.setResizeWeight(0.75);
        หน้าต่าง.add(คําสั่ง_แผง, BorderLayout.NORTH); หน้าต่าง.add(ฝ่าย_เมตริก, BorderLayout.CENTER);
        หน้าต่าง.setSize(1200, 750); หน้าต่าง.setLocationRelativeTo(null);
        หน้าต่าง.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        หน้าต่าง.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent เหตุการณ์) { 멈춤(); ผู้ปฏิบัติงาน_ค่า.shutdownNow(); }
        });
        เปิด(); หน้าต่าง.setVisible(true);
    }
    public static void main(String[] อาร์กิวเมนต์) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ฟอนต์เริ่มต้น = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object รายการ_ค่า : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(รายการ_ค่า) instanceof Font) UIManager.put(รายการ_ค่า, ฟอนต์เริ่มต้น);
                }
                new พื้นที่ทํางาน();
            } catch (Exception ข้อผิดพลาด) { ข้อผิดพลาด.printStackTrace(); }
        });
    }
}
