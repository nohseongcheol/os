// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame Gluggi;
    JLabel LESTUMIG_eb81d7d9;
    JTextField 입력;
    public void run() {
        Gluggi = new JFrame("eigin kjarni_VALUE Swing");
        Gluggi.setSize(400, 280);
        Gluggi.setLocationRelativeTo(null);
        Gluggi.setLayout(null);
        Gluggi.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        LESTUMIG_eb81d7d9 = new JLabel("한글로 Java 코딩");
        LESTUMIG_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Heiti");
        입력.setBounds(20, 65, 340, 30);
        JButton hnappur = new JButton("인사하기");
        hnappur.setBounds(20, 110, 180, 32);
        hnappur.addActionListener(this);
        Gluggi.add(LESTUMIG_eb81d7d9); Gluggi.add(입력); Gluggi.add(hnappur);
        Gluggi.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent atvik) {
        LESTUMIG_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
