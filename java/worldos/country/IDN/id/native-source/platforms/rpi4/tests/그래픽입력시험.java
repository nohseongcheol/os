// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, tekan_VALUE;
    private static JFrame Jendela;

    private static void periksa() {
        if (키입력 && tekan_VALUE) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Jendela.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window target : Window.getWindows()) {
                        if (target instanceof JFrame && target.isVisible()
                                && ((JFrame) target).getTitle().equals("다국어 인사")) {
                            target.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sinkro = new Robot();
                                    sinkro.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception galat) {
                                    throw new RuntimeException(galat);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception galat) {
                throw new RuntimeException(galat);
            }
        }
    }

    public static void main(String[] argumen) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Jendela = new JFrame("QEMU 키보드·마우스 pengujian");
            JButton tombol = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            tombol.addActionListener(Even -> { tekan_VALUE = true; periksa(); });
            Jendela.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Jendela.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Even) { 키입력 = true; periksa(); }
            });
            Jendela.add(tombol);
            Jendela.setSize(600, 180);
            Jendela.setLocation(120, 120);
            Jendela.setAlwaysOnTop(true);
            Jendela.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Jendela.setVisible(true);
            Jendela.toFront();
            Timer Siapkan = new Timer(750, Even -> {
                Point posisi = tombol.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (posisi.x + tombol.getWidth() / 2)
                        + " " + (posisi.y + tombol.getHeight() / 2));
            });
            Siapkan.setRepeats(false);
            Siapkan.start();
        });
    }
}
