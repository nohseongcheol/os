// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Swing_test implements Runnable, ActionListener {
    JFrame Okno;
    JLabel 안내;
    JTextField vstup_VALUE;
    public void run() {
        Okno = new JFrame("vlastné jadro_VALUE Swing");
        Okno.setSize(400, 280);
        Okno.setLocationRelativeTo(null);
        Okno.setLayout(null);
        Okno.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        안내 = new JLabel("한글로 Java 코딩");
        안내.setBounds(20, 20, 340, 30);
        vstup_VALUE = new JTextField("Názov");
        vstup_VALUE.setBounds(20, 65, 340, 30);
        JButton Tlačidlo = new JButton("인사하기");
        Tlačidlo.setBounds(20, 110, 180, 32);
        Tlačidlo.addActionListener(this);
        Okno.add(안내); Okno.add(vstup_VALUE); Okno.add(Tlačidlo);
        Okno.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Udalosť) {
        안내.setText("안녕하세요 " + vstup_VALUE.getText());
        System.out.println("SWING CLICK " + vstup_VALUE.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Swing_test());
    }
}
