// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame vindauge;
    JLabel Viktig_eb81d7d9;
    JTextField 입력;
    public void run() {
        vindauge = new JFrame("자체 kjerne_VALUE Swing");
        vindauge.setSize(400, 280);
        vindauge.setLocationRelativeTo(null);
        vindauge.setLayout(null);
        vindauge.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        Viktig_eb81d7d9 = new JLabel("한글로 Java 코딩");
        Viktig_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Namn");
        입력.setBounds(20, 65, 340, 30);
        JButton knapp = new JButton("인사하기");
        knapp.setBounds(20, 110, 180, 32);
        knapp.addActionListener(this);
        vindauge.add(Viktig_eb81d7d9); vindauge.add(입력); vindauge.add(knapp);
        vindauge.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Hending) {
        Viktig_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
