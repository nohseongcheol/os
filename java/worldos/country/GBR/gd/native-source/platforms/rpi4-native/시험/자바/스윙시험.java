// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame uinneag;
    JLabel LEUGHMI_eb81d7d9;
    JTextField 입력;
    public void run() {
        uinneag = new JFrame("자체 eitean_VALUE Swing");
        uinneag.setSize(400, 280);
        uinneag.setLocationRelativeTo(null);
        uinneag.setLayout(null);
        uinneag.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        LEUGHMI_eb81d7d9 = new JLabel("한글로 Java 코딩");
        LEUGHMI_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Ainm");
        입력.setBounds(20, 65, 340, 30);
        JButton putan = new JButton("인사하기");
        putan.setBounds(20, 110, 180, 32);
        putan.addActionListener(this);
        uinneag.add(LEUGHMI_eb81d7d9); uinneag.add(입력); uinneag.add(putan);
        uinneag.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent tachartas) {
        LEUGHMI_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
