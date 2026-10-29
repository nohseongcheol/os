// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame Jendela;
    JLabel baca_saya_eb81d7d9;
    JTextField 입력;
    public void run() {
        Jendela = new JFrame("Asli kernel_VALUE Swing");
        Jendela.setSize(400, 280);
        Jendela.setLocationRelativeTo(null);
        Jendela.setLayout(null);
        Jendela.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        baca_saya_eb81d7d9 = new JLabel("한글로 Java 코딩");
        baca_saya_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Nama_2");
        입력.setBounds(20, 65, 340, 30);
        JButton tombol = new JButton("인사하기");
        tombol.setBounds(20, 110, 180, 32);
        tombol.addActionListener(this);
        Jendela.add(baca_saya_eb81d7d9); Jendela.add(입력); Jendela.add(tombol);
        Jendela.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Even) {
        baca_saya_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
