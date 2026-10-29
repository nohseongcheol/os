// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] аргументы) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Окно = new JFrame("한글 входные_данные_ЗНАЧЕН · шрифт_ЗНАЧЕН проверять");
            JPanel версия_ЗНАЧЕН_65c6ecdc = new JPanel(new BorderLayout(10, 15));
            версия_ЗНАЧЕН_65c6ecdc.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel файл_сведений_eb81d7d9 = new JLabel("Ctrl+Space → 한글 входные_данные_ЗНАЧЕН → Ctrl+Space → Enter");
            JTextField входные_данные_ЗНАЧЕН = new JTextField();
            Font шрифт_ЗНАЧЕН = new Font("Dialog", Font.PLAIN, 20);
            файл_сведений_eb81d7d9.setFont(шрифт_ЗНАЧЕН.deriveFont(16f)); входные_данные_ЗНАЧЕН.setFont(шрифт_ЗНАЧЕН);
            входные_данные_ЗНАЧЕН.enableInputMethods(true);
            входные_данные_ЗНАЧЕН.addActionListener(Событие -> {
                String результат = входные_данные_ЗНАЧЕН.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), результат, StandardCharsets.UTF_8);
                } catch (Exception ошибка) { throw new RuntimeException(ошибка); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(результат.getBytes(StandardCharsets.UTF_8)));
            });
            версия_ЗНАЧЕН_65c6ecdc.add(файл_сведений_eb81d7d9, BorderLayout.NORTH); версия_ЗНАЧЕН_65c6ecdc.add(входные_данные_ЗНАЧЕН, BorderLayout.CENTER);
            Окно.add(версия_ЗНАЧЕН_65c6ecdc); Окно.setSize(850, 230); Окно.setLocation(100, 100);
            Окно.setAlwaysOnTop(true); Окно.setVisible(true); входные_данные_ЗНАЧЕН.requestFocusInWindow();
            Timer Подготовить = new Timer(1000, Событие -> {
                Point позиция = входные_данные_ЗНАЧЕН.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (позиция.x + 100) + " " + (позиция.y + 30));
            });
            Подготовить.setRepeats(false); Подготовить.start();
        });
    }
}
