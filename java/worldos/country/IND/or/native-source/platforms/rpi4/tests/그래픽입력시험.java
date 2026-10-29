// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame ଓ୍ୱିଣ୍ଡୋ;

    private static void ଯାଞ୍ଚ୍_କରିବା() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            ଓ୍ୱିଣ୍ଡୋ.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window ଲକ୍ଷ୍ୟସ୍ଥଳ : Window.getWindows()) {
                        if (ଲକ୍ଷ୍ୟସ୍ଥଳ instanceof JFrame && ଲକ୍ଷ୍ୟସ୍ଥଳ.isVisible()
                                && ((JFrame) ଲକ୍ଷ୍ୟସ୍ଥଳ).getTitle().equals("다국어 인사")) {
                            ଲକ୍ଷ୍ୟସ୍ଥଳ.toFront();
                            new Thread(() -> {
                                try {
                                    Robot ସିଂକ୍ରୋନାଇଜ୍_କରନ୍ତୁ = new Robot();
                                    ସିଂକ୍ରୋନାଇଜ୍_କରନ୍ତୁ.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ତ୍ରୁଟି) {
                                    throw new RuntimeException(ତ୍ରୁଟି);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ତ୍ରୁଟି) {
                throw new RuntimeException(ତ୍ରୁଟି);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            ଓ୍ୱିଣ୍ଡୋ = new JFrame("QEMU 키보드·마우스 시험");
            JButton ବଟନ୍ = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            ବଟନ୍.addActionListener(ଘଟଣା -> { 누름 = true; ଯାଞ୍ଚ୍_କରିବା(); });
            ଓ୍ୱିଣ୍ଡୋ.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            ଓ୍ୱିଣ୍ଡୋ.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ଘଟଣା) { 키입력 = true; ଯାଞ୍ଚ୍_କରିବା(); }
            });
            ଓ୍ୱିଣ୍ଡୋ.add(ବଟନ୍);
            ଓ୍ୱିଣ୍ଡୋ.setSize(600, 180);
            ଓ୍ୱିଣ୍ଡୋ.setLocation(120, 120);
            ଓ୍ୱିଣ୍ଡୋ.setAlwaysOnTop(true);
            ଓ୍ୱିଣ୍ଡୋ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            ଓ୍ୱିଣ୍ଡୋ.setVisible(true);
            ଓ୍ୱିଣ୍ଡୋ.toFront();
            Timer ପ୍ରସ୍ତୁତ = new Timer(750, ଘଟଣା -> {
                Point ଅବସ୍ଥାନ = ବଟନ୍.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (ଅବସ୍ଥାନ.x + ବଟନ୍.getWidth() / 2)
                        + " " + (ଅବସ୍ଥାନ.y + ବଟନ୍.getHeight() / 2));
            });
            ପ୍ରସ୍ତୁତ.setRepeats(false);
            ପ୍ରସ୍ତୁତ.start();
        });
    }
}
