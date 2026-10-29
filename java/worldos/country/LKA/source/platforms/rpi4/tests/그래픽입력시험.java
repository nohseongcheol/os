// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame කවුළුව;

    private static void තහවුරු_කරන්න() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            කවුළුව.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window ඉලක්කය : Window.getWindows()) {
                        if (ඉලක්කය instanceof JFrame && ඉලක්කය.isVisible()
                                && ((JFrame) ඉලක්කය).getTitle().equals("다국어 인사")) {
                            ඉලක්කය.toFront();
                            new Thread(() -> {
                                try {
                                    Robot සමමු = new Robot();
                                    සමමු.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception දෝෂය) {
                                    throw new RuntimeException(දෝෂය);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception දෝෂය) {
                throw new RuntimeException(දෝෂය);
            }
        }
    }

    public static void main(String[] විස්තාරක) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            කවුළුව = new JFrame("QEMU 키보드·마우스 시험");
            JButton බොත්තම = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            බොත්තම.addActionListener(සිදුවීම -> { 누름 = true; තහවුරු_කරන්න(); });
            කවුළුව.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            කවුළුව.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent සිදුවීම) { 키입력 = true; තහවුරු_කරන්න(); }
            });
            කවුළුව.add(බොත්තම);
            කවුළුව.setSize(600, 180);
            කවුළුව.setLocation(120, 120);
            කවුළුව.setAlwaysOnTop(true);
            කවුළුව.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            කවුළුව.setVisible(true);
            කවුළුව.toFront();
            Timer පිළියෙල_කරන්න = new Timer(750, සිදුවීම -> {
                Point පිහිටීම = බොත්තම.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (පිහිටීම.x + බොත්තම.getWidth() / 2)
                        + " " + (පිහිටීම.y + බොත්තම.getHeight() / 2));
            });
            පිළියෙල_කරන්න.setRepeats(false);
            පිළියෙල_කරන්න.start();
        });
    }
}
