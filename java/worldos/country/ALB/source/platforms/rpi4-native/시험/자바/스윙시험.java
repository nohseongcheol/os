// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame Dritare;
    JLabel LEXOMË_eb81d7d9;
    JTextField 입력;
    public void run() {
        Dritare = new JFrame("자체 bërthamë_VALUE Swing");
        Dritare.setSize(400, 280);
        Dritare.setLocationRelativeTo(null);
        Dritare.setLayout(null);
        Dritare.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        LEXOMË_eb81d7d9 = new JLabel("한글로 Java 코딩");
        LEXOMË_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Emër");
        입력.setBounds(20, 65, 340, 30);
        JButton Buton = new JButton("인사하기");
        Buton.setBounds(20, 110, 180, 32);
        Buton.addActionListener(this);
        Dritare.add(LEXOMË_eb81d7d9); Dritare.add(입력); Dritare.add(Buton);
        Dritare.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Ngjarje) {
        LEXOMË_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
