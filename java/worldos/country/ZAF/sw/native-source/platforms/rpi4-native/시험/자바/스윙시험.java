// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame dirisha;
    JLabel NISOME_eb81d7d9;
    JTextField 입력;
    public void run() {
        dirisha = new JFrame("자체 kiini_thamani_0611a8a8 Swing");
        dirisha.setSize(400, 280);
        dirisha.setLocationRelativeTo(null);
        dirisha.setLayout(null);
        dirisha.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        NISOME_eb81d7d9 = new JLabel("한글로 Java 코딩");
        NISOME_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Jina");
        입력.setBounds(20, 65, 340, 30);
        JButton kitufe = new JButton("인사하기");
        kitufe.setBounds(20, 110, 180, 32);
        kitufe.addActionListener(this);
        dirisha.add(NISOME_eb81d7d9); dirisha.add(입력); dirisha.add(kitufe);
        dirisha.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent tukio) {
        NISOME_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
