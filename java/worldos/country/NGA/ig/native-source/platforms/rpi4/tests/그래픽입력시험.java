// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame windò;

    private static void nkwàdo_eziokwū() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            windò.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window ebenlereanya : Window.getWindows()) {
                        if (ebenlereanya instanceof JFrame && ebenlereanya.isVisible()
                                && ((JFrame) ebenlereanya).getTitle().equals("다국어 인사")) {
                            ebenlereanya.toFront();
                            new Thread(() -> {
                                try {
                                    Robot hàkọọ = new Robot();
                                    hàkọọ.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception mmejọ) {
                                    throw new RuntimeException(mmejọ);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception mmejọ) {
                throw new RuntimeException(mmejọ);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            windò = new JFrame("QEMU 키보드·마우스 시험");
            JButton ọdụmbi = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            ọdụmbi.addActionListener(mmèrème -> { 누름 = true; nkwàdo_eziokwū(); });
            windò.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            windò.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent mmèrème) { 키입력 = true; nkwàdo_eziokwū(); }
            });
            windò.add(ọdụmbi);
            windò.setSize(600, 180);
            windò.setLocation(120, 120);
            windò.setAlwaysOnTop(true);
            windò.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            windò.setVisible(true);
            windò.toFront();
            Timer Kwado = new Timer(750, mmèrème -> {
                Point 위치 = ọdụmbi.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + ọdụmbi.getWidth() / 2)
                        + " " + (위치.y + ọdụmbi.getHeight() / 2));
            });
            Kwado.setRepeats(false);
            Kwado.start();
        });
    }
}
