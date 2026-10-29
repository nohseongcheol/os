// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] 인수) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame fensetere = new JFrame("한글 입력 · mofutatlhaka_Boleng netefatsa");
            JPanel kgaolo_Boleng = new JPanel(new BorderLayout(10, 15));
            kgaolo_Boleng.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel MPUISE_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font mofutatlhaka_Boleng = new Font("Dialog", Font.PLAIN, 20);
            MPUISE_eb81d7d9.setFont(mofutatlhaka_Boleng.deriveFont(16f)); 입력.setFont(mofutatlhaka_Boleng);
            입력.enableInputMethods(true);
            입력.addActionListener(tiragalo -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception phoso) { throw new RuntimeException(phoso); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            kgaolo_Boleng.add(MPUISE_eb81d7d9, BorderLayout.NORTH); kgaolo_Boleng.add(입력, BorderLayout.CENTER);
            fensetere.add(kgaolo_Boleng); fensetere.setSize(850, 230); fensetere.setLocation(100, 100);
            fensetere.setAlwaysOnTop(true); fensetere.setVisible(true); 입력.requestFocusInWindow();
            Timer Baakanya = new Timer(1000, tiragalo -> {
                Point 위치 = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (위치.x + 100) + " " + (위치.y + 30));
            });
            Baakanya.setRepeats(false); Baakanya.start();
        });
    }
}
