// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class swing_testi implements Runnable, ActionListener {
    JFrame Ikkuna;
    JLabel Lueminut_eb81d7d9;
    JTextField syöte_ARVO;
    public void run() {
        Ikkuna = new JFrame("oma ydin_ARVO Swing");
        Ikkuna.setSize(400, 280);
        Ikkuna.setLocationRelativeTo(null);
        Ikkuna.setLayout(null);
        Ikkuna.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        Lueminut_eb81d7d9 = new JLabel("한글로 Java 코딩");
        Lueminut_eb81d7d9.setBounds(20, 20, 340, 30);
        syöte_ARVO = new JTextField("Nimi");
        syöte_ARVO.setBounds(20, 65, 340, 30);
        JButton painike = new JButton("인사하기");
        painike.setBounds(20, 110, 180, 32);
        painike.addActionListener(this);
        Ikkuna.add(Lueminut_eb81d7d9); Ikkuna.add(syöte_ARVO); Ikkuna.add(painike);
        Ikkuna.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Tapahtuma) {
        Lueminut_eb81d7d9.setText("안녕하세요 " + syöte_ARVO.getText());
        System.out.println("SWING CLICK " + syöte_ARVO.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new swing_testi());
    }
}
