// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame Tetingkap;
    JLabel README_eb81d7d9;
    JTextField 입력;
    public void run() {
        Tetingkap = new JFrame("Asli kernel_VALUE Swing");
        Tetingkap.setSize(400, 280);
        Tetingkap.setLocationRelativeTo(null);
        Tetingkap.setLayout(null);
        Tetingkap.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        README_eb81d7d9 = new JLabel("한글로 Java 코딩");
        README_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Nama");
        입력.setBounds(20, 65, 340, 30);
        JButton Butang = new JButton("인사하기");
        Butang.setBounds(20, 110, 180, 32);
        Butang.addActionListener(this);
        Tetingkap.add(README_eb81d7d9); Tetingkap.add(입력); Tetingkap.add(Butang);
        Tetingkap.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Peristiwa) {
        README_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
