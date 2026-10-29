// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame palanteer;
    JLabel JANG_MA_eb81d7d9;
    JTextField 입력;
    public void run() {
        palanteer = new JFrame("자체 xoox_xëyma Swing");
        palanteer.setSize(400, 280);
        palanteer.setLocationRelativeTo(null);
        palanteer.setLayout(null);
        palanteer.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        JANG_MA_eb81d7d9 = new JLabel("한글로 Java 코딩");
        JANG_MA_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("tur_253d1510");
        입력.setBounds(20, 65, 340, 30);
        JButton butoñ = new JButton("인사하기");
        butoñ.setBounds(20, 110, 180, 32);
        butoñ.addActionListener(this);
        palanteer.add(JANG_MA_eb81d7d9); palanteer.add(입력); palanteer.add(butoñ);
        palanteer.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent xewxew) {
        JANG_MA_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
