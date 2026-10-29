// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame উইন্ডো;

    private static void যাচাই_করা() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            উইন্ডো.dispose();
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
                                    Robot সমলয়_করা = new Robot();
                                    সমলয়_করা.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ত্রুটি) {
                                    throw new RuntimeException(ত্রুটি);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ত্রুটি) {
                throw new RuntimeException(ত্রুটি);
            }
        }
    }

    public static void main(String[] আর্গুমেন্ট_তালিকা) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            উইন্ডো = new JFrame("QEMU 키보드·마우스 시험");
            JButton বোতাম = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            বোতাম.addActionListener(ঘটনা -> { 누름 = true; যাচাই_করা(); });
            উইন্ডো.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            উইন্ডো.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ঘটনা) { 키입력 = true; যাচাই_করা(); }
            });
            উইন্ডো.add(বোতাম);
            উইন্ডো.setSize(600, 180);
            উইন্ডো.setLocation(120, 120);
            উইন্ডো.setAlwaysOnTop(true);
            উইন্ডো.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            উইন্ডো.setVisible(true);
            উইন্ডো.toFront();
            Timer প্রস্তুত_করুন = new Timer(750, ঘটনা -> {
                Point অবস্থান = বোতাম.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (অবস্থান.x + বোতাম.getWidth() / 2)
                        + " " + (অবস্থান.y + বোতাম.getHeight() / 2));
            });
            প্রস্তুত_করুন.setRepeats(false);
            প্রস্তুত_করুন.start();
        });
    }
}
