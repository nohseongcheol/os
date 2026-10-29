// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame উইণ্ড;

    private static void প্ৰমাণিত_কৰক() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            উইণ্ড.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window লক্ষ্য : Window.getWindows()) {
                        if (লক্ষ্য instanceof JFrame && লক্ষ্য.isVisible()
                                && ((JFrame) লক্ষ্য).getTitle().equals("다국어 인사")) {
                            লক্ষ্য.toFront();
                            new Thread(() -> {
                                try {
                                    Robot সকালীকৄত_কৰক = new Robot();
                                    সকালীকৄত_কৰক.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ত্ৰুটি) {
                                    throw new RuntimeException(ত্ৰুটি);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ত্ৰুটি) {
                throw new RuntimeException(ত্ৰুটি);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            উইণ্ড = new JFrame("QEMU 키보드·마우스 시험");
            JButton বুটাম = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            বুটাম.addActionListener(ইভেণ্ট -> { 누름 = true; প্ৰমাণিত_কৰক(); });
            উইণ্ড.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            উইণ্ড.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ইভেণ্ট) { 키입력 = true; প্ৰমাণিত_কৰক(); }
            });
            উইণ্ড.add(বুটাম);
            উইণ্ড.setSize(600, 180);
            উইণ্ড.setLocation(120, 120);
            উইণ্ড.setAlwaysOnTop(true);
            উইণ্ড.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            উইণ্ড.setVisible(true);
            উইণ্ড.toFront();
            Timer প্ৰস্তুত_কৰক = new Timer(750, ইভেণ্ট -> {
                Point অৱস্থান = বুটাম.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (অৱস্থান.x + বুটাম.getWidth() / 2)
                        + " " + (অৱস্থান.y + বুটাম.getHeight() / 2));
            });
            প্ৰস্তুত_কৰক.setRepeats(false);
            প্ৰস্তুত_কৰক.start();
        });
    }
}
