// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ThửĐầuVàoĐồHọa {
    private static boolean đầuVàoPhím, giáTrịNhấn;
    private static JFrame cửaSổ;

    private static void xácMinh() {
        if (đầuVàoPhím && giáTrịNhấn) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            cửaSổ.dispose();
            try {
                Class.forName("LờiChào").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window giáTrịĐốiĐích : Window.getWindows()) {
                        if (giáTrịĐốiĐích instanceof JFrame && giáTrịĐốiĐích.isVisible()
                                && ((JFrame) giáTrịĐốiĐích).getTitle().equals("다국어 LờiChào")) {
                            giáTrịĐốiĐích.toFront();
                            new Thread(() -> {
                                try {
                                    Robot đồngBộHóa = new Robot();
                                    đồngBộHóa.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception lỗi) {
                                    throw new RuntimeException(lỗi);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("LờiChào 창이 표시되지 않았습니다");
                });
            } catch (Exception lỗi) {
                throw new RuntimeException(lỗi);
            }
        }
    }

    public static void main(String[] cácĐốiSố) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 MànHình phươngThứcThiếu");
        SwingUtilities.invokeAndWait(() -> {
            cửaSổ = new JFrame("QEMU 키보드·마우스 KiểmThử");
            JButton nút = new JButton("한글 MànHình · 이 단추를 누르고 K를 giáTrịVào");
            nút.addActionListener(sựKiện -> { giáTrịNhấn = true; xácMinh(); });
            cửaSổ.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            cửaSổ.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent sựKiện) { đầuVàoPhím = true; xácMinh(); }
            });
            cửaSổ.add(nút);
            cửaSổ.setSize(600, 180);
            cửaSổ.setLocation(120, 120);
            cửaSổ.setAlwaysOnTop(true);
            cửaSổ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            cửaSổ.setVisible(true);
            cửaSổ.toFront();
            Timer chuẩnBị = new Timer(750, sựKiện -> {
                Point vịTrí = nút.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (vịTrí.x + nút.getWidth() / 2)
                        + " " + (vịTrí.y + nút.getHeight() / 2));
            });
            chuẩnBị.setRepeats(false);
            chuẩnBị.start();
        });
    }
}
