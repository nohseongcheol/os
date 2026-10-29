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
            JFrame విండో = new JFrame("한글 입력 · అక్షరాకృతి_మూల్యం సరిచూడు");
            JPanel సంస్కరణ_మూల్యం = new JPanel(new BorderLayout(10, 15));
            సంస్కరణ_మూల్యం.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel మార్గదర్శక_సమాచారం_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font అక్షరాకృతి_మూల్యం = new Font("Dialog", Font.PLAIN, 20);
            మార్గదర్శక_సమాచారం_eb81d7d9.setFont(అక్షరాకృతి_మూల్యం.deriveFont(16f)); 입력.setFont(అక్షరాకృతి_మూల్యం);
            입력.enableInputMethods(true);
            입력.addActionListener(ఈవెంట్ -> {
                String ప్రమాణం = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), ప్రమాణం, StandardCharsets.UTF_8);
                } catch (Exception దోషం) { throw new RuntimeException(దోషం); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(ప్రమాణం.getBytes(StandardCharsets.UTF_8)));
            });
            సంస్కరణ_మూల్యం.add(మార్గదర్శక_సమాచారం_eb81d7d9, BorderLayout.NORTH); సంస్కరణ_మూల్యం.add(입력, BorderLayout.CENTER);
            విండో.add(సంస్కరణ_మూల్యం); విండో.setSize(850, 230); విండో.setLocation(100, 100);
            విండో.setAlwaysOnTop(true); విండో.setVisible(true); 입력.requestFocusInWindow();
            Timer సిద్ధం_చేయు = new Timer(1000, ఈవెంట్ -> {
                Point స్థానము = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (స్థానము.x + 100) + " " + (స్థానము.y + 30));
            });
            సిద్ధం_చేయు.setRepeats(false); సిద్ధం_చేయు.start();
        });
    }
}
