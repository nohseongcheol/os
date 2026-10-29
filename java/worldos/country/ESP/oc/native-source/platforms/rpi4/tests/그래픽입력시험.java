// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame 창;

    private static void 확인() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            창.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window 대상 : Window.getWindows()) {
                        if (대상 instanceof JFrame && 대상.isVisible()
                                && ((JFrame) 대상).getTitle().equals("다국어 인사")) {
                            대상.toFront();
                            new Thread(() -> {
                                try {
                                    Robot 동기화 = new Robot();
                                    동기화.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception 오류) {
                                    throw new RuntimeException(오류);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception 오류) {
                throw new RuntimeException(오류);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            창 = new JFrame("QEMU 키보드·마우스 시험");
            JButton Boton = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            Boton.addActionListener(Eveniment -> { 누름 = true; 확인(); });
            창.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            창.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Eveniment) { 키입력 = true; 확인(); }
            });
            창.add(Boton);
            창.setSize(600, 180);
            창.setLocation(120, 120);
            창.setAlwaysOnTop(true);
            창.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            창.setVisible(true);
            창.toFront();
            Timer 준비 = new Timer(750, Eveniment -> {
                Point Posicion = Boton.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Posicion.x + Boton.getWidth() / 2)
                        + " " + (Posicion.y + Boton.getHeight() / 2));
            });
            준비.setRepeats(false);
            준비.start();
        });
    }
}
