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
            JFrame цонх = new JFrame("한글 입력 · үсгийн_хэв_утга шалгах");
            JPanel хувилбар_утга = new JPanel(new BorderLayout(10, 15));
            хувилбар_утга.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel заавал_унших_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font үсгийн_хэв_утга = new Font("Dialog", Font.PLAIN, 20);
            заавал_унших_eb81d7d9.setFont(үсгийн_хэв_утга.deriveFont(16f)); 입력.setFont(үсгийн_хэв_утга);
            입력.enableInputMethods(true);
            입력.addActionListener(үйлдэл -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception Алдаа) { throw new RuntimeException(Алдаа); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            хувилбар_утга.add(заавал_унших_eb81d7d9, BorderLayout.NORTH); хувилбар_утга.add(입력, BorderLayout.CENTER);
            цонх.add(хувилбар_утга); цонх.setSize(850, 230); цонх.setLocation(100, 100);
            цонх.setAlwaysOnTop(true); цонх.setVisible(true); 입력.requestFocusInWindow();
            Timer Бэлтгэх = new Timer(1000, үйлдэл -> {
                Point 위치 = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (위치.x + 100) + " " + (위치.y + 30));
            });
            Бэлтгэх.setRepeats(false); Бэлтгэх.start();
        });
    }
}
