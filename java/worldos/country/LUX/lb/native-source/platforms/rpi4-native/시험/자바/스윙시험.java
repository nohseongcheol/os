// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame Fënster;
    JLabel LIESMECH_eb81d7d9;
    JTextField 입력;
    public void run() {
        Fënster = new JFrame("자체 Kernel_VALUE Swing");
        Fënster.setSize(400, 280);
        Fënster.setLocationRelativeTo(null);
        Fënster.setLayout(null);
        Fënster.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        LIESMECH_eb81d7d9 = new JLabel("한글로 Java 코딩");
        LIESMECH_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Numm");
        입력.setBounds(20, 65, 340, 30);
        JButton Tast = new JButton("인사하기");
        Tast.setBounds(20, 110, 180, 32);
        Tast.addActionListener(this);
        Fënster.add(LIESMECH_eb81d7d9); Fënster.add(입력); Fënster.add(Tast);
        Fënster.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Evenement) {
        LIESMECH_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
