// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, prémer_VALOR;
    private static JFrame Finestra;

    private static void verificar() {
        if (키입력 && prémer_VALOR) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Finestra.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window objectiu : Window.getWindows()) {
                        if (objectiu instanceof JFrame && objectiu.isVisible()
                                && ((JFrame) objectiu).getTitle().equals("다국어 인사")) {
                            objectiu.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sincronitzar = new Robot();
                                    sincronitzar.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception s_ha_produït_un_error) {
                                    throw new RuntimeException(s_ha_produït_un_error);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception s_ha_produït_un_error) {
                throw new RuntimeException(s_ha_produït_un_error);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Finestra = new JFrame("QEMU 키보드·마우스 시험");
            JButton Botó = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            Botó.addActionListener(Esdeveniment -> { prémer_VALOR = true; verificar(); });
            Finestra.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Finestra.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Esdeveniment) { 키입력 = true; verificar(); }
            });
            Finestra.add(Botó);
            Finestra.setSize(600, 180);
            Finestra.setLocation(120, 120);
            Finestra.setAlwaysOnTop(true);
            Finestra.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Finestra.setVisible(true);
            Finestra.toFront();
            Timer Prepara = new Timer(750, Esdeveniment -> {
                Point Posició = Botó.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Posició.x + Botó.getWidth() / 2)
                        + " " + (Posició.y + Botó.getHeight() / 2));
            });
            Prepara.setRepeats(false);
            Prepara.start();
        });
    }
}
