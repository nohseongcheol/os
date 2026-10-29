// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] аргументи) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Вікно = new JFrame("한글 입력 · шрифт_значення перевіряти");
            JPanel версія_значення = new JPanel(new BorderLayout(10, 15));
            версія_значення.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel файл_Readme_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font шрифт_значення = new Font("Dialog", Font.PLAIN, 20);
            файл_Readme_eb81d7d9.setFont(шрифт_значення.deriveFont(16f)); 입력.setFont(шрифт_значення);
            입력.enableInputMethods(true);
            입력.addActionListener(Подія -> {
                String результат = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), результат, StandardCharsets.UTF_8);
                } catch (Exception ПОМИЛКА) { throw new RuntimeException(ПОМИЛКА); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(результат.getBytes(StandardCharsets.UTF_8)));
            });
            версія_значення.add(файл_Readme_eb81d7d9, BorderLayout.NORTH); версія_значення.add(입력, BorderLayout.CENTER);
            Вікно.add(версія_значення); Вікно.setSize(850, 230); Вікно.setLocation(100, 100);
            Вікно.setAlwaysOnTop(true); Вікно.setVisible(true); 입력.requestFocusInWindow();
            Timer Готувати = new Timer(1000, Подія -> {
                Point позиція = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (позиція.x + 100) + " " + (позиція.y + 30));
            });
            Готувати.setRepeats(false); Готувати.start();
        });
    }
}
