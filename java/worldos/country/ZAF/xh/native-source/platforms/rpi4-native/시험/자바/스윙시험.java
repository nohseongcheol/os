// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame i_window;
    JLabel i_README_eb81d7d9;
    JTextField 입력;
    public void run() {
        i_window = new JFrame("자체 ikheneli_ixabiso Swing");
        i_window.setSize(400, 280);
        i_window.setLocationRelativeTo(null);
        i_window.setLayout(null);
        i_window.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        i_README_eb81d7d9 = new JLabel("한글로 Java 코딩");
        i_README_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Igama");
        입력.setBounds(20, 65, 340, 30);
        JButton iqhosha = new JButton("인사하기");
        iqhosha.setBounds(20, 110, 180, 32);
        iqhosha.addActionListener(this);
        i_window.add(i_README_eb81d7d9); i_window.add(입력); i_window.add(iqhosha);
        i_window.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent umcimbi) {
        i_README_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
