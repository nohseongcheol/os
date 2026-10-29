// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame ວິນໂດ;

    private static void 확인() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            ວິນໂດ.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window ເປົ້າ_ຫມາຍ : Window.getWindows()) {
                        if (ເປົ້າ_ຫມາຍ instanceof JFrame && ເປົ້າ_ຫມາຍ.isVisible()
                                && ((JFrame) ເປົ້າ_ຫມາຍ).getTitle().equals("다국어 인사")) {
                            ເປົ້າ_ຫມາຍ.toFront();
                            new Thread(() -> {
                                try {
                                    Robot ຊິງໂຄຣໄນ = new Robot();
                                    ຊິງໂຄຣໄນ.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ຂໍ້ຜິດພາດ) {
                                    throw new RuntimeException(ຂໍ້ຜິດພາດ);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ຂໍ້ຜິດພາດ) {
                throw new RuntimeException(ຂໍ້ຜິດພາດ);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            ວິນໂດ = new JFrame("QEMU 키보드·마우스 시험");
            JButton ປຸ່ມ = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            ປຸ່ມ.addActionListener(ງານ -> { 누름 = true; 확인(); });
            ວິນໂດ.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            ວິນໂດ.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ງານ) { 키입력 = true; 확인(); }
            });
            ວິນໂດ.add(ປຸ່ມ);
            ວິນໂດ.setSize(600, 180);
            ວິນໂດ.setLocation(120, 120);
            ວິນໂດ.setAlwaysOnTop(true);
            ວິນໂດ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            ວິນໂດ.setVisible(true);
            ວິນໂດ.toFront();
            Timer ກະ_ກຽມ = new Timer(750, ງານ -> {
                Point ຈັດຕໍາແຫນ່ງ = ປຸ່ມ.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (ຈັດຕໍາແຫນ່ງ.x + ປຸ່ມ.getWidth() / 2)
                        + " " + (ຈັດຕໍາແຫນ່ງ.y + ປຸ່ມ.getHeight() / 2));
            });
            ກະ_ກຽມ.setRepeats(false);
            ກະ_ກຽມ.start();
        });
    }
}
