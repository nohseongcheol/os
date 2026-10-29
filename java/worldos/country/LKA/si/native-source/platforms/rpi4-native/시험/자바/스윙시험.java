// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame කවුළුව;
    JLabel README_ගොනුව_eb81d7d9;
    JTextField 입력;
    public void run() {
        කවුළුව = new JFrame("자체 කර්නලය_අගය Swing");
        කවුළුව.setSize(400, 280);
        කවුළුව.setLocationRelativeTo(null);
        කවුළුව.setLayout(null);
        කවුළුව.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        README_ගොනුව_eb81d7d9 = new JLabel("한글로 Java 코딩");
        README_ගොනුව_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("නම");
        입력.setBounds(20, 65, 340, 30);
        JButton බොත්තම = new JButton("인사하기");
        බොත්තම.setBounds(20, 110, 180, 32);
        බොත්තම.addActionListener(this);
        කවුළුව.add(README_ගොනුව_eb81d7d9); කවුළුව.add(입력); කවුළුව.add(බොත්තම);
        කවුළුව.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent සිදුවීම) {
        README_ගොනුව_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
