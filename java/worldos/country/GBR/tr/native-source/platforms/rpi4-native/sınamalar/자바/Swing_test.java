// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Swing_test implements Runnable, ActionListener {
    JFrame Pencere;
    JLabel 안내;
    JTextField artış_değer;
    public void run() {
        Pencere = new JFrame("Öz çekirdek_değer Swing");
        Pencere.setSize(400, 280);
        Pencere.setLocationRelativeTo(null);
        Pencere.setLayout(null);
        Pencere.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        안내 = new JLabel("한글로 Java 코딩");
        안내.setBounds(20, 20, 340, 30);
        artış_değer = new JTextField("İsim");
        artış_değer.setBounds(20, 65, 340, 30);
        JButton düğme = new JButton("인사하기");
        düğme.setBounds(20, 110, 180, 32);
        düğme.addActionListener(this);
        Pencere.add(안내); Pencere.add(artış_değer); Pencere.add(düğme);
        Pencere.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Olay) {
        안내.setText("안녕하세요 " + artış_değer.getText());
        System.out.println("SWING CLICK " + artış_değer.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Swing_test());
    }
}
