// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame વિંડો;
    JLabel રીડમી_eb81d7d9;
    JTextField 입력;
    public void run() {
        વિંડો = new JFrame("자체 કર્નેલ_મૂલ્ય Swing");
        વિંડો.setSize(400, 280);
        વિંડો.setLocationRelativeTo(null);
        વિંડો.setLayout(null);
        વિંડો.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        રીડમી_eb81d7d9 = new JLabel("한글로 Java 코딩");
        રીડમી_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("નામ");
        입력.setBounds(20, 65, 340, 30);
        JButton બટન = new JButton("인사하기");
        બટન.setBounds(20, 110, 180, 32);
        બટન.addActionListener(this);
        વિંડો.add(રીડમી_eb81d7d9); વિંડો.add(입력); વિંડો.add(બટન);
        વિંડો.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ઇવેંટ) {
        રીડમી_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
