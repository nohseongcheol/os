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
            JFrame i_window = new JFrame("한글 입력 · ifonti_ixabiso ngqinisisa");
            JPanel inguqulelo_ixabiso = new JPanel(new BorderLayout(10, 15));
            inguqulelo_ixabiso.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel i_README_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ifonti_ixabiso = new Font("Dialog", Font.PLAIN, 20);
            i_README_eb81d7d9.setFont(ifonti_ixabiso.deriveFont(16f)); 입력.setFont(ifonti_ixabiso);
            입력.enableInputMethods(true);
            입력.addActionListener(umcimbi -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception Impazamo) { throw new RuntimeException(Impazamo); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            inguqulelo_ixabiso.add(i_README_eb81d7d9, BorderLayout.NORTH); inguqulelo_ixabiso.add(입력, BorderLayout.CENTER);
            i_window.add(inguqulelo_ixabiso); i_window.setSize(850, 230); i_window.setLocation(100, 100);
            i_window.setAlwaysOnTop(true); i_window.setVisible(true); 입력.requestFocusInWindow();
            Timer lungisa = new Timer(1000, umcimbi -> {
                Point 위치 = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (위치.x + 100) + " " + (위치.y + 30));
            });
            lungisa.setRepeats(false); lungisa.start();
        });
    }
}
