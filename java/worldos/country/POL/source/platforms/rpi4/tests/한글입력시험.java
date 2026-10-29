// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] argumenty) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Okno = new JFrame("한글 wejście_WARTOŚĆ · czcionka_WARTOŚĆ 확인");
            JPanel wersja_WARTOŚĆ = new JPanel(new BorderLayout(10, 15));
            wersja_WARTOŚĆ.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel plik_README_eb81d7d9 = new JLabel("Ctrl+Space → 한글 wejście_WARTOŚĆ → Ctrl+Space → Enter");
            JTextField wejście_WARTOŚĆ = new JTextField();
            Font czcionka_WARTOŚĆ = new Font("Dialog", Font.PLAIN, 20);
            plik_README_eb81d7d9.setFont(czcionka_WARTOŚĆ.deriveFont(16f)); wejście_WARTOŚĆ.setFont(czcionka_WARTOŚĆ);
            wejście_WARTOŚĆ.enableInputMethods(true);
            wejście_WARTOŚĆ.addActionListener(Wydarzenie -> {
                String WYNIK = wejście_WARTOŚĆ.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), WYNIK, StandardCharsets.UTF_8);
                } catch (Exception błąd) { throw new RuntimeException(błąd); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(WYNIK.getBytes(StandardCharsets.UTF_8)));
            });
            wersja_WARTOŚĆ.add(plik_README_eb81d7d9, BorderLayout.NORTH); wersja_WARTOŚĆ.add(wejście_WARTOŚĆ, BorderLayout.CENTER);
            Okno.add(wersja_WARTOŚĆ); Okno.setSize(850, 230); Okno.setLocation(100, 100);
            Okno.setAlwaysOnTop(true); Okno.setVisible(true); wejście_WARTOŚĆ.requestFocusInWindow();
            Timer Przygotuj = new Timer(1000, Wydarzenie -> {
                Point pozycja = wejście_WARTOŚĆ.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (pozycja.x + 100) + " " + (pozycja.y + 30));
            });
            Przygotuj.setRepeats(false); Przygotuj.start();
        });
    }
}
