// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame Ventana;

    private static void 확인() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Ventana.dispose();
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
                                } catch (Exception Fallu) {
                                    throw new RuntimeException(Fallu);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Fallu) {
                throw new RuntimeException(Fallu);
            }
        }
    }

    public static void main(String[] Argumentu) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Ventana = new JFrame("QEMU 키보드·마우스 시험");
            JButton Botón = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            Botón.addActionListener(Eventu -> { 누름 = true; 확인(); });
            Ventana.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Ventana.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Eventu) { 키입력 = true; 확인(); }
            });
            Ventana.add(Botón);
            Ventana.setSize(600, 180);
            Ventana.setLocation(120, 120);
            Ventana.setAlwaysOnTop(true);
            Ventana.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Ventana.setVisible(true);
            Ventana.toFront();
            Timer 준비 = new Timer(750, Eventu -> {
                Point Posición = Botón.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Posición.x + Botón.getWidth() / 2)
                        + " " + (Posición.y + Botón.getHeight() / 2));
            });
            준비.setRepeats(false);
            준비.start();
        });
    }
}
