// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Swing_test implements Runnable, ActionListener {
    JFrame Okno;
    JLabel plik_README_eb81d7d9;
    JTextField wejście_WARTOŚĆ;
    public void run() {
        Okno = new JFrame("własny jądro_WARTOŚĆ Swing");
        Okno.setSize(400, 280);
        Okno.setLocationRelativeTo(null);
        Okno.setLayout(null);
        Okno.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        plik_README_eb81d7d9 = new JLabel("한글로 Java 코딩");
        plik_README_eb81d7d9.setBounds(20, 20, 340, 30);
        wejście_WARTOŚĆ = new JTextField("Nazwa");
        wejście_WARTOŚĆ.setBounds(20, 65, 340, 30);
        JButton przycisk = new JButton("인사하기");
        przycisk.setBounds(20, 110, 180, 32);
        przycisk.addActionListener(this);
        Okno.add(plik_README_eb81d7d9); Okno.add(wejście_WARTOŚĆ); Okno.add(przycisk);
        Okno.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Wydarzenie) {
        plik_README_eb81d7d9.setText("안녕하세요 " + wejście_WARTOŚĆ.getText());
        System.out.println("SWING CLICK " + wejście_WARTOŚĆ.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Swing_test());
    }
}
