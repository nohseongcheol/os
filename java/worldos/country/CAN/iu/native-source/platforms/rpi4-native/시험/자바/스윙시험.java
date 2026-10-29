// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame igalaangujaq;
    JLabel README_eb81d7d9;
    JTextField 입력;
    public void run() {
        igalaangujaq = new JFrame("자체 kernel_atuutilik Swing");
        igalaangujaq.setSize(400, 280);
        igalaangujaq.setLocationRelativeTo(null);
        igalaangujaq.setLayout(null);
        igalaangujaq.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        README_eb81d7d9 = new JLabel("한글로 Java 코딩");
        README_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("atiq");
        입력.setBounds(20, 65, 340, 30);
        JButton tikkuagaq = new JButton("인사하기");
        tikkuagaq.setBounds(20, 110, 180, 32);
        tikkuagaq.addActionListener(this);
        igalaangujaq.add(README_eb81d7d9); igalaangujaq.add(입력); igalaangujaq.add(tikkuagaq);
        igalaangujaq.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent piniku) {
        README_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
