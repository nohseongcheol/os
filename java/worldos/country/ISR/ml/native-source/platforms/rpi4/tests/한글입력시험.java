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
            JFrame ജാലകം = new JFrame("한글 입력 · ഫോണ്ട്_മൂല്യം പരിശോധിക്കുക");
            JPanel പതിപ്പ്_മൂല്യം = new JPanel(new BorderLayout(10, 15));
            പതിപ്പ്_മൂല്യം.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel readme_ഫയല്_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ഫോണ്ട്_മൂല്യം = new Font("Dialog", Font.PLAIN, 20);
            readme_ഫയല്_eb81d7d9.setFont(ഫോണ്ട്_മൂല്യം.deriveFont(16f)); 입력.setFont(ഫോണ്ട്_മൂല്യം);
            입력.enableInputMethods(true);
            입력.addActionListener(ഇവന്റ് -> {
                String അളവ് = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), അളവ്, StandardCharsets.UTF_8);
                } catch (Exception പിശക്) { throw new RuntimeException(പിശക്); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(അളവ്.getBytes(StandardCharsets.UTF_8)));
            });
            പതിപ്പ്_മൂല്യം.add(readme_ഫയല്_eb81d7d9, BorderLayout.NORTH); പതിപ്പ്_മൂല്യം.add(입력, BorderLayout.CENTER);
            ജാലകം.add(പതിപ്പ്_മൂല്യം); ജാലകം.setSize(850, 230); ജാലകം.setLocation(100, 100);
            ജാലകം.setAlwaysOnTop(true); ജാലകം.setVisible(true); 입력.requestFocusInWindow();
            Timer തയ്യാറാക്കുക = new Timer(1000, ഇവന്റ് -> {
                Point സ്ഥാനം = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (സ്ഥാനം.x + 100) + " " + (സ്ഥാനം.y + 30));
            });
            തയ്യാറാക്കുക.setRepeats(false); തയ്യാറാക്കുക.start();
        });
    }
}
