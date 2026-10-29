// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame равзана;
    JLabel файли_тафсилот_eb81d7d9;
    JTextField 입력;
    public void run() {
        равзана = new JFrame("자체 ҳаста_қимат Swing");
        равзана.setSize(400, 280);
        равзана.setLocationRelativeTo(null);
        равзана.setLayout(null);
        равзана.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        файли_тафсилот_eb81d7d9 = new JLabel("한글로 Java 코딩");
        файли_тафсилот_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Ном");
        입력.setBounds(20, 65, 340, 30);
        JButton тугма = new JButton("인사하기");
        тугма.setBounds(20, 110, 180, 32);
        тугма.addActionListener(this);
        равзана.add(файли_тафсилот_eb81d7d9); равзана.add(입력); равзана.add(тугма);
        равзана.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent рӯйдод) {
        файли_тафсилот_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
