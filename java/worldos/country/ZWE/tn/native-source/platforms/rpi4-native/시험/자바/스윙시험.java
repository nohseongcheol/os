// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame fensetere;
    JLabel MPUISE_eb81d7d9;
    JTextField 입력;
    public void run() {
        fensetere = new JFrame("자체 Khenele_Boleng Swing");
        fensetere.setSize(400, 280);
        fensetere.setLocationRelativeTo(null);
        fensetere.setLayout(null);
        fensetere.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        MPUISE_eb81d7d9 = new JLabel("한글로 Java 코딩");
        MPUISE_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("leina");
        입력.setBounds(20, 65, 340, 30);
        JButton konopo = new JButton("인사하기");
        konopo.setBounds(20, 110, 180, 32);
        konopo.addActionListener(this);
        fensetere.add(MPUISE_eb81d7d9); fensetere.add(입력); fensetere.add(konopo);
        fensetere.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent tiragalo) {
        MPUISE_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
