// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame tieqa;

    private static void vverifika() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            tieqa.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window mira : Window.getWindows()) {
                        if (mira instanceof JFrame && mira.isVisible()
                                && ((JFrame) mira).getTitle().equals("다국어 인사")) {
                            mira.toFront();
                            new Thread(() -> {
                                try {
                                    Robot ssinkronizza = new Robot();
                                    ssinkronizza.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception żball) {
                                    throw new RuntimeException(żball);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception żball) {
                throw new RuntimeException(żball);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            tieqa = new JFrame("QEMU 키보드·마우스 시험");
            JButton buttuna = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            buttuna.addActionListener(avveniment -> { 누름 = true; vverifika(); });
            tieqa.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            tieqa.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent avveniment) { 키입력 = true; vverifika(); }
            });
            tieqa.add(buttuna);
            tieqa.setSize(600, 180);
            tieqa.setLocation(120, 120);
            tieqa.setAlwaysOnTop(true);
            tieqa.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            tieqa.setVisible(true);
            tieqa.toFront();
            Timer Ħejji = new Timer(750, avveniment -> {
                Point pożizzjoni = buttuna.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (pożizzjoni.x + buttuna.getWidth() / 2)
                        + " " + (pożizzjoni.y + buttuna.getHeight() / 2));
            });
            Ħejji.setRepeats(false);
            Ħejji.start();
        });
    }
}
