// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame វីនដូ;

    private static void ផ្ទៀងផ្ទាត់() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            វីនដូ.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window គោលដៅ : Window.getWindows()) {
                        if (គោលដៅ instanceof JFrame && គោលដៅ.isVisible()
                                && ((JFrame) គោលដៅ).getTitle().equals("다국어 인사")) {
                            គោលដៅ.toFront();
                            new Thread(() -> {
                                try {
                                    Robot សមកាលកម្ម = new Robot();
                                    សមកាលកម្ម.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception កំហុស) {
                                    throw new RuntimeException(កំហុស);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception កំហុស) {
                throw new RuntimeException(កំហុស);
            }
        }
    }

    public static void main(String[] អាគុយម៉ង់) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            វីនដូ = new JFrame("QEMU 키보드·마우스 시험");
            JButton ប៊ូតុង = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            ប៊ូតុង.addActionListener(ព្រឹត្តិការណ៍ -> { 누름 = true; ផ្ទៀងផ្ទាត់(); });
            វីនដូ.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            វីនដូ.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ព្រឹត្តិការណ៍) { 키입력 = true; ផ្ទៀងផ្ទាត់(); }
            });
            វីនដូ.add(ប៊ូតុង);
            វីនដូ.setSize(600, 180);
            វីនដូ.setLocation(120, 120);
            វីនដូ.setAlwaysOnTop(true);
            វីនដូ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            វីនដូ.setVisible(true);
            វីនដូ.toFront();
            Timer រៀបចំ = new Timer(750, ព្រឹត្តិការណ៍ -> {
                Point កំណត់ទីតាំង = ប៊ូតុង.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (កំណត់ទីតាំង.x + ប៊ូតុង.getWidth() / 2)
                        + " " + (កំណត់ទីតាំង.y + ប៊ូតុង.getHeight() / 2));
            });
            រៀបចំ.setRepeats(false);
            រៀបចំ.start();
        });
    }
}
