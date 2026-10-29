// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class GraphicsInputTest {
    private static boolean keyInput, pressValue;
    private static JFrame window;

    private static void verify() {
        if (keyInput && pressValue) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            window.dispose();
            try {
                Class.forName("Greeting").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window targetValue : Window.getWindows()) {
                        if (targetValue instanceof JFrame && targetValue.isVisible()
                                && ((JFrame) targetValue).getTitle().equals("다국어 Greeting")) {
                            targetValue.toFront();
                            new Thread(() -> {
                                try {
                                    Robot synchronize = new Robot();
                                    synchronize.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception error) {
                                    throw new RuntimeException(error);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("Greeting 창이 표시되지 않았습니다");
                });
            } catch (Exception error) {
                throw new RuntimeException(error);
            }
        }
    }

    public static void main(String[] arguments) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 Screen missingMethod");
        SwingUtilities.invokeAndWait(() -> {
            window = new JFrame("QEMU 키보드·마우스 tests");
            JButton button = new JButton("한글 Screen · 이 단추를 누르고 K를 inputValue");
            button.addActionListener(event -> { pressValue = true; verify(); });
            window.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            window.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent event) { keyInput = true; verify(); }
            });
            window.add(button);
            window.setSize(600, 180);
            window.setLocation(120, 120);
            window.setAlwaysOnTop(true);
            window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            window.setVisible(true);
            window.toFront();
            Timer prepare = new Timer(750, event -> {
                Point position = button.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (position.x + button.getWidth() / 2)
                        + " " + (position.y + button.getHeight() / 2));
            });
            prepare.setRepeats(false);
            prepare.start();
        });
    }
}
