// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame ifasitela;
    JLabel NGIFUNDE_eb81d7d9;
    JTextField 입력;
    public void run() {
        ifasitela = new JFrame("자체 ikhenela_inani Swing");
        ifasitela.setSize(400, 280);
        ifasitela.setLocationRelativeTo(null);
        ifasitela.setLayout(null);
        ifasitela.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        NGIFUNDE_eb81d7d9 = new JLabel("한글로 Java 코딩");
        NGIFUNDE_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Igama");
        입력.setBounds(20, 65, 340, 30);
        JButton inkinobho = new JButton("인사하기");
        inkinobho.setBounds(20, 110, 180, 32);
        inkinobho.addActionListener(this);
        ifasitela.add(NGIFUNDE_eb81d7d9); ifasitela.add(입력); ifasitela.add(inkinobho);
        ifasitela.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent isigameko) {
        NGIFUNDE_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
