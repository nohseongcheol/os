// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame ਵਿੰਡੋ;

    private static void ਤਸਦੀਕ() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            ਵਿੰਡੋ.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window ਟੀਚਾ : Window.getWindows()) {
                        if (ਟੀਚਾ instanceof JFrame && ਟੀਚਾ.isVisible()
                                && ((JFrame) ਟੀਚਾ).getTitle().equals("다국어 인사")) {
                            ਟੀਚਾ.toFront();
                            new Thread(() -> {
                                try {
                                    Robot ਸਿੰਕ_ਕਰੋ = new Robot();
                                    ਸਿੰਕ_ਕਰੋ.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ਗਲਤੀ) {
                                    throw new RuntimeException(ਗਲਤੀ);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ਗਲਤੀ) {
                throw new RuntimeException(ਗਲਤੀ);
            }
        }
    }

    public static void main(String[] ਆਰਗੂਮੈਂਟ) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            ਵਿੰਡੋ = new JFrame("QEMU 키보드·마우스 시험");
            JButton ਬਟਨ = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            ਬਟਨ.addActionListener(ਇਵੈਂਟ -> { 누름 = true; ਤਸਦੀਕ(); });
            ਵਿੰਡੋ.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            ਵਿੰਡੋ.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ਇਵੈਂਟ) { 키입력 = true; ਤਸਦੀਕ(); }
            });
            ਵਿੰਡੋ.add(ਬਟਨ);
            ਵਿੰਡੋ.setSize(600, 180);
            ਵਿੰਡੋ.setLocation(120, 120);
            ਵਿੰਡੋ.setAlwaysOnTop(true);
            ਵਿੰਡੋ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            ਵਿੰਡੋ.setVisible(true);
            ਵਿੰਡੋ.toFront();
            Timer ਤਿਆਰ_ਕਰੋ = new Timer(750, ਇਵੈਂਟ -> {
                Point ਸਥਿਤੀ = ਬਟਨ.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (ਸਥਿਤੀ.x + ਬਟਨ.getWidth() / 2)
                        + " " + (ਸਥਿਤੀ.y + ਬਟਨ.getHeight() / 2));
            });
            ਤਿਆਰ_ਕਰੋ.setRepeats(false);
            ਤਿਆਰ_ਕਰੋ.start();
        });
    }
}
