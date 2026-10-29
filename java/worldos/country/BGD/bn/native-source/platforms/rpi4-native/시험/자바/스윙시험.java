// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame উইন্ডো;
    JLabel স্বনিবন্ধ_eb81d7d9;
    JTextField 입력;
    public void run() {
        উইন্ডো = new JFrame("নিজ কারনেল_মান Swing");
        উইন্ডো.setSize(400, 280);
        উইন্ডো.setLocationRelativeTo(null);
        উইন্ডো.setLayout(null);
        উইন্ডো.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        স্বনিবন্ধ_eb81d7d9 = new JLabel("한글로 Java 코딩");
        স্বনিবন্ধ_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("নাম");
        입력.setBounds(20, 65, 340, 30);
        JButton বোতাম = new JButton("인사하기");
        বোতাম.setBounds(20, 110, 180, 32);
        বোতাম.addActionListener(this);
        উইন্ডো.add(স্বনিবন্ধ_eb81d7d9); উইন্ডো.add(입력); উইন্ডো.add(বোতাম);
        উইন্ডো.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ঘটনা) {
        স্বনিবন্ধ_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
