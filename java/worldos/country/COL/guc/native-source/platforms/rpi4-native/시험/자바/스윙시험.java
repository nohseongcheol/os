// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame analaaya;
    JLabel PAASHAJE_ERAN_eb81d7d9;
    JTextField 입력;
    public void run() {
        analaaya = new JFrame("자체 keetnerü_ajutuu Swing");
        analaaya.setSize(400, 280);
        analaaya.setLocationRelativeTo(null);
        analaaya.setLayout(null);
        analaaya.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        PAASHAJE_ERAN_eb81d7d9 = new JLabel("한글로 Java 코딩");
        PAASHAJE_ERAN_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("이름");
        입력.setBounds(20, 65, 340, 30);
        JButton ajüttülee = new JButton("인사하기");
        ajüttülee.setBounds(20, 110, 180, 32);
        ajüttülee.addActionListener(this);
        analaaya.add(PAASHAJE_ERAN_eb81d7d9); analaaya.add(입력); analaaya.add(ajüttülee);
        analaaya.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent kasachiki) {
        PAASHAJE_ERAN_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
