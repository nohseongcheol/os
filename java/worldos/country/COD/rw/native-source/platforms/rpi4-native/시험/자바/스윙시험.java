// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame idirishya;
    JLabel NSOMA_eb81d7d9;
    JTextField 입력;
    public void run() {
        idirishya = new JFrame("자체 intima_agaciro Swing");
        idirishya.setSize(400, 280);
        idirishya.setLocationRelativeTo(null);
        idirishya.setLayout(null);
        idirishya.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        NSOMA_eb81d7d9 = new JLabel("한글로 Java 코딩");
        NSOMA_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Izina");
        입력.setBounds(20, 65, 340, 30);
        JButton buto = new JButton("인사하기");
        buto.setBounds(20, 110, 180, 32);
        buto.addActionListener(this);
        idirishya.add(NSOMA_eb81d7d9); idirishya.add(입력); idirishya.add(buto);
        idirishya.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent icyabaye) {
        NSOMA_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
