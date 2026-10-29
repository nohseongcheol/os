// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame ᏦᎳᏂ;

    private static void ᎰᎯᏳᏓ() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            ᏦᎳᏂ.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window ᎠᏉᏅᏗᎢ : Window.getWindows()) {
                        if (ᎠᏉᏅᏗᎢ instanceof JFrame && ᎠᏉᏅᏗᎢ.isVisible()
                                && ((JFrame) ᎠᏉᏅᏗᎢ).getTitle().equals("다국어 인사")) {
                            ᎠᏉᏅᏗᎢ.toFront();
                            new Thread(() -> {
                                try {
                                    Robot ᎢᏧᎳᎭ_ᏂᏛᎦ = new Robot();
                                    ᎢᏧᎳᎭ_ᏂᏛᎦ.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ᎦᎵᏓᏍᏔᏅ) {
                                    throw new RuntimeException(ᎦᎵᏓᏍᏔᏅ);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ᎦᎵᏓᏍᏔᏅ) {
                throw new RuntimeException(ᎦᎵᏓᏍᏔᏅ);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            ᏦᎳᏂ = new JFrame("QEMU 키보드·마우스 시험");
            JButton ᎠᏐᏅᏍᏙᏗ = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            ᎠᏐᏅᏍᏙᏗ.addActionListener(ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ -> { 누름 = true; ᎰᎯᏳᏓ(); });
            ᏦᎳᏂ.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            ᏦᎳᏂ.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ) { 키입력 = true; ᎰᎯᏳᏓ(); }
            });
            ᏦᎳᏂ.add(ᎠᏐᏅᏍᏙᏗ);
            ᏦᎳᏂ.setSize(600, 180);
            ᏦᎳᏂ.setLocation(120, 120);
            ᏦᎳᏂ.setAlwaysOnTop(true);
            ᏦᎳᏂ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            ᏦᎳᏂ.setVisible(true);
            ᏦᎳᏂ.toFront();
            Timer ᎭᏛᏅᎢᏍᏓ = new Timer(750, ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ -> {
                Point 위치 = ᎠᏐᏅᏍᏙᏗ.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + ᎠᏐᏅᏍᏙᏗ.getWidth() / 2)
                        + " " + (위치.y + ᎠᏐᏅᏍᏙᏗ.getHeight() / 2));
            });
            ᎭᏛᏅᎢᏍᏓ.setRepeats(false);
            ᎭᏛᏅᎢᏍᏓ.start();
        });
    }
}
