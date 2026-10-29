// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame lefastere;
    JLabel faele_ya_MPALE_eb81d7d9;
    JTextField 입력;
    public void run() {
        lefastere = new JFrame("자체 khenele_boleng Swing");
        lefastere.setSize(400, 280);
        lefastere.setLocationRelativeTo(null);
        lefastere.setLayout(null);
        lefastere.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        faele_ya_MPALE_eb81d7d9 = new JLabel("한글로 Java 코딩");
        faele_ya_MPALE_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Leina");
        입력.setBounds(20, 65, 340, 30);
        JButton konope = new JButton("인사하기");
        konope.setBounds(20, 110, 180, 32);
        konope.addActionListener(this);
        lefastere.add(faele_ya_MPALE_eb81d7d9); lefastere.add(입력); lefastere.add(konope);
        lefastere.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent tiragalo) {
        faele_ya_MPALE_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
