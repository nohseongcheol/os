// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ग्राफिक्स_आदान_चाचणी {
    private static boolean कळ_आदान, दाबा_मूल्य;
    private static JFrame विंडो;

    private static void पडताळा() {
        if (कळ_आदान && दाबा_मूल्य) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            विंडो.dispose();
            try {
                Class.forName("अभिवादन_ae353e94").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window लक्ष्य : Window.getWindows()) {
                        if (लक्ष्य instanceof JFrame && लक्ष्य.isVisible()
                                && ((JFrame) लक्ष्य).getTitle().equals("다국어 अभिवादन_ae353e94")) {
                            लक्ष्य.toFront();
                            new Thread(() -> {
                                try {
                                    Robot समन्वय_साधा = new Robot();
                                    समन्वय_साधा.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception त्रुटी) {
                                    throw new RuntimeException(त्रुटी);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("अभिवादन_ae353e94 창이 표시되지 않았습니다");
                });
            } catch (Exception त्रुटी) {
                throw new RuntimeException(त्रुटी);
            }
        }
    }

    public static void main(String[] बाबी) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 पडदा अनुपस्थित_पद्धत");
        SwingUtilities.invokeAndWait(() -> {
            विंडो = new JFrame("QEMU 키보드·마우스 चाचण्या");
            JButton बटण = new JButton("한글 पडदा · 이 단추를 누르고 K를 आदान_मूल्य");
            बटण.addActionListener(इव्हेंट -> { दाबा_मूल्य = true; पडताळा(); });
            विंडो.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            विंडो.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent इव्हेंट) { कळ_आदान = true; पडताळा(); }
            });
            विंडो.add(बटण);
            विंडो.setSize(600, 180);
            विंडो.setLocation(120, 120);
            विंडो.setAlwaysOnTop(true);
            विंडो.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            विंडो.setVisible(true);
            विंडो.toFront();
            Timer तयार_करणे = new Timer(750, इव्हेंट -> {
                Point जागा = बटण.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (जागा.x + बटण.getWidth() / 2)
                        + " " + (जागा.y + बटण.getHeight() / 2));
            });
            तयार_करणे.setRepeats(false);
            तयार_करणे.start();
        });
    }
}
