// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ရုပ်ပုံအဝင်စမ်းသပ် {
    private static boolean သော့အဝင်, နှိပ်ထားမှု;
    private static JFrame ဝင်း;

    private static void အတည်ပြု() {
        if (သော့အဝင် && နှိပ်ထားမှု) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            ဝင်း.dispose();
            try {
                Class.forName("နှုတ်ဆက်").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window ဦးတည်ချက်တန်ဖိုး : Window.getWindows()) {
                        if (ဦးတည်ချက်တန်ဖိုး instanceof JFrame && ဦးတည်ချက်တန်ဖိုး.isVisible()
                                && ((JFrame) ဦးတည်ချက်တန်ဖိုး).getTitle().equals("다국어 နှုတ်ဆက်")) {
                            ဦးတည်ချက်တန်ဖိုး.toFront();
                            new Thread(() -> {
                                try {
                                    Robot တစ်ပြေးညီလုပ် = new Robot();
                                    တစ်ပြေးညီလုပ်.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception အမှား) {
                                    throw new RuntimeException(အမှား);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("နှုတ်ဆက် 창이 표시되지 않았습니다");
                });
            } catch (Exception အမှား) {
                throw new RuntimeException(အမှား);
            }
        }
    }

    public static void main(String[] အချက်များ) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 မျက်နှာပြင် 없음");
        SwingUtilities.invokeAndWait(() -> {
            ဝင်း = new JFrame("QEMU 키보드·마우스 စမ်းသပ်မှု");
            JButton ခလုတ် = new JButton("한글 မျက်နှာပြင် · 이 단추를 누르고 K를 ဝင်ဒေတာ");
            ခလုတ်.addActionListener(ဖြစ်ရပ် -> { နှိပ်ထားမှု = true; အတည်ပြု(); });
            ဝင်း.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            ဝင်း.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ဖြစ်ရပ်) { သော့အဝင် = true; အတည်ပြု(); }
            });
            ဝင်း.add(ခလုတ်);
            ဝင်း.setSize(600, 180);
            ဝင်း.setLocation(120, 120);
            ဝင်း.setAlwaysOnTop(true);
            ဝင်း.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            ဝင်း.setVisible(true);
            ဝင်း.toFront();
            Timer ပြင်ဆင် = new Timer(750, ဖြစ်ရပ် -> {
                Point နေရာ = ခလုတ်.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (နေရာ.x + ခလုတ်.getWidth() / 2)
                        + " " + (နေရာ.y + ခလုတ်.getHeight() / 2));
            });
            ပြင်ဆင်.setRepeats(false);
            ပြင်ဆင်.start();
        });
    }
}
