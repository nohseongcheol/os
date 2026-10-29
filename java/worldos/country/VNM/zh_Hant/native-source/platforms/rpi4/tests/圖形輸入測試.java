// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 圖形輸入測試 {
    private static boolean 鍵輸入, 按下值;
    private static JFrame 窗口;

    private static void 驗證() {
        if (鍵輸入 && 按下值) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            窗口.dispose();
            try {
                Class.forName("問候例").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window 目標值 : Window.getWindows()) {
                        if (目標值 instanceof JFrame && 目標值.isVisible()
                                && ((JFrame) 目標值).getTitle().equals("다국어 問候例")) {
                            目標值.toFront();
                            new Thread(() -> {
                                try {
                                    Robot 同步化 = new Robot();
                                    同步化.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception 錯誤) {
                                    throw new RuntimeException(錯誤);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("問候例 창이 표시되지 않았습니다");
                });
            } catch (Exception 錯誤) {
                throw new RuntimeException(錯誤);
            }
        }
    }

    public static void main(String[] 實參) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 屏幕 缺失方法");
        SwingUtilities.invokeAndWait(() -> {
            窗口 = new JFrame("QEMU 키보드·마우스 測試");
            JButton 按鈕 = new JButton("한글 屏幕 · 이 단추를 누르고 K를 輸入值");
            按鈕.addActionListener(事件 -> { 按下值 = true; 驗證(); });
            窗口.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            窗口.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent 事件) { 鍵輸入 = true; 驗證(); }
            });
            窗口.add(按鈕);
            窗口.setSize(600, 180);
            窗口.setLocation(120, 120);
            窗口.setAlwaysOnTop(true);
            窗口.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            窗口.setVisible(true);
            窗口.toFront();
            Timer 準備 = new Timer(750, 事件 -> {
                Point 位置 = 按鈕.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (位置.x + 按鈕.getWidth() / 2)
                        + " " + (位置.y + 按鈕.getHeight() / 2));
            });
            準備.setRepeats(false);
            準備.start();
        });
    }
}
