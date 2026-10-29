// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame ജാലകം;

    private static void പരിശോധിക്കുക() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            ജാലകം.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window ലക്_ഷ്യം : Window.getWindows()) {
                        if (ലക്_ഷ്യം instanceof JFrame && ലക്_ഷ്യം.isVisible()
                                && ((JFrame) ലക്_ഷ്യം).getTitle().equals("다국어 인사")) {
                            ലക്_ഷ്യം.toFront();
                            new Thread(() -> {
                                try {
                                    Robot സമന്വയിപ്പിക്കുക = new Robot();
                                    സമന്വയിപ്പിക്കുക.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception പിശക്) {
                                    throw new RuntimeException(പിശക്);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception പിശക്) {
                throw new RuntimeException(പിശക്);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            ജാലകം = new JFrame("QEMU 키보드·마우스 시험");
            JButton ബട്ടണ് = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            ബട്ടണ്.addActionListener(ഇവന്റ് -> { 누름 = true; പരിശോധിക്കുക(); });
            ജാലകം.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            ജാലകം.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ഇവന്റ്) { 키입력 = true; പരിശോധിക്കുക(); }
            });
            ജാലകം.add(ബട്ടണ്);
            ജാലകം.setSize(600, 180);
            ജാലകം.setLocation(120, 120);
            ജാലകം.setAlwaysOnTop(true);
            ജാലകം.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            ജാലകം.setVisible(true);
            ജാലകം.toFront();
            Timer തയ്യാറാക്കുക = new Timer(750, ഇവന്റ് -> {
                Point സ്ഥാനം = ബട്ടണ്.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (സ്ഥാനം.x + ബട്ടണ്.getWidth() / 2)
                        + " " + (സ്ഥാനം.y + ബട്ടണ്.getHeight() / 2));
            });
            തയ്യാറാക്കുക.setRepeats(false);
            തയ്യാറാക്കുക.start();
        });
    }
}
