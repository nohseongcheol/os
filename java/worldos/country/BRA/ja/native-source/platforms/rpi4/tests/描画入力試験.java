// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 描画入力試験 {
    private static boolean キー入力, 押下値;
    private static JFrame 窓;

    private static void 検証() {
        if (キー入力 && 押下値) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            窓.dispose();
            try {
                Class.forName("挨拶例").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window 対象値 : Window.getWindows()) {
                        if (対象値 instanceof JFrame && 対象値.isVisible()
                                && ((JFrame) 対象値).getTitle().equals("다국어 挨拶例")) {
                            対象値.toFront();
                            new Thread(() -> {
                                try {
                                    Robot 同期化 = new Robot();
                                    同期化.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception エラー) {
                                    throw new RuntimeException(エラー);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("挨拶例 창이 표시되지 않았습니다");
                });
            } catch (Exception エラー) {
                throw new RuntimeException(エラー);
            }
        }
    }

    public static void main(String[] 引数) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 画面 未存在メソッド");
        SwingUtilities.invokeAndWait(() -> {
            窓 = new JFrame("QEMU 키보드·마우스 試験");
            JButton ボタン = new JButton("한글 画面 · 이 단추를 누르고 K를 入力値");
            ボタン.addActionListener(イベント -> { 押下値 = true; 検証(); });
            窓.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            窓.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent イベント) { キー入力 = true; 検証(); }
            });
            窓.add(ボタン);
            窓.setSize(600, 180);
            窓.setLocation(120, 120);
            窓.setAlwaysOnTop(true);
            窓.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            窓.setVisible(true);
            窓.toFront();
            Timer 用意 = new Timer(750, イベント -> {
                Point 位置 = ボタン.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (位置.x + ボタン.getWidth() / 2)
                        + " " + (位置.y + ボタン.getHeight() / 2));
            });
            用意.setRepeats(false);
            用意.start();
        });
    }
}
