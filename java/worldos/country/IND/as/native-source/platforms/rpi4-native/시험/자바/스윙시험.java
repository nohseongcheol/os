// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame উইণ্ড;
    JLabel ৰিডমি_ফাইল_eb81d7d9;
    JTextField 입력;
    public void run() {
        উইণ্ড = new JFrame("자체 কাৰ্ণেল_মান Swing");
        উইণ্ড.setSize(400, 280);
        উইণ্ড.setLocationRelativeTo(null);
        উইণ্ড.setLayout(null);
        উইণ্ড.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        ৰিডমি_ফাইল_eb81d7d9 = new JLabel("한글로 Java 코딩");
        ৰিডমি_ফাইল_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("নাম");
        입력.setBounds(20, 65, 340, 30);
        JButton বুটাম = new JButton("인사하기");
        বুটাম.setBounds(20, 110, 180, 32);
        বুটাম.addActionListener(this);
        উইণ্ড.add(ৰিডমি_ফাইল_eb81d7d9); উইণ্ড.add(입력); উইণ্ড.add(বুটাম);
        উইণ্ড.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ইভেণ্ট) {
        ৰিডমি_ফাইল_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
