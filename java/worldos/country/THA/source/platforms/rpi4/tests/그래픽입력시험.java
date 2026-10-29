// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, กด_ค่า;
    private static JFrame หน้าต่าง;

    private static void ยืนยัน() {
        if (키입력 && กด_ค่า) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            หน้าต่าง.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window เป้าหมาย : Window.getWindows()) {
                        if (เป้าหมาย instanceof JFrame && เป้าหมาย.isVisible()
                                && ((JFrame) เป้าหมาย).getTitle().equals("다국어 인사")) {
                            เป้าหมาย.toFront();
                            new Thread(() -> {
                                try {
                                    Robot ซิงค์ = new Robot();
                                    ซิงค์.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ข้อผิดพลาด) {
                                    throw new RuntimeException(ข้อผิดพลาด);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ข้อผิดพลาด) {
                throw new RuntimeException(ข้อผิดพลาด);
            }
        }
    }

    public static void main(String[] อาร์กิวเมนต์) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            หน้าต่าง = new JFrame("QEMU 키보드·마우스 시험");
            JButton ปุ่ม = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            ปุ่ม.addActionListener(เหตุการณ์ -> { กด_ค่า = true; ยืนยัน(); });
            หน้าต่าง.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            หน้าต่าง.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent เหตุการณ์) { 키입력 = true; ยืนยัน(); }
            });
            หน้าต่าง.add(ปุ่ม);
            หน้าต่าง.setSize(600, 180);
            หน้าต่าง.setLocation(120, 120);
            หน้าต่าง.setAlwaysOnTop(true);
            หน้าต่าง.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            หน้าต่าง.setVisible(true);
            หน้าต่าง.toFront();
            Timer จัดเตรียม = new Timer(750, เหตุการณ์ -> {
                Point ตําแหน่ง = ปุ่ม.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (ตําแหน่ง.x + ปุ่ม.getWidth() / 2)
                        + " " + (ตําแหน่ง.y + ปุ่ม.getHeight() / 2));
            });
            จัดเตรียม.setRepeats(false);
            จัดเตรียม.start();
        });
    }
}
