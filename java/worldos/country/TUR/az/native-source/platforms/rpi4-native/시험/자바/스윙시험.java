// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame pəncərə;
    JLabel OXUMƏNİ_eb81d7d9;
    JTextField 입력;
    public void run() {
        pəncərə = new JFrame("자체 nüvə_VALUE Swing");
        pəncərə.setSize(400, 280);
        pəncərə.setLocationRelativeTo(null);
        pəncərə.setLayout(null);
        pəncərə.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        OXUMƏNİ_eb81d7d9 = new JLabel("한글로 Java 코딩");
        OXUMƏNİ_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Ad");
        입력.setBounds(20, 65, 340, 30);
        JButton düymə = new JButton("인사하기");
        düymə.setBounds(20, 110, 180, 32);
        düymə.addActionListener(this);
        pəncərə.add(OXUMƏNİ_eb81d7d9); pəncərə.add(입력); pəncərə.add(düymə);
        pəncərə.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent hadisə) {
        OXUMƏNİ_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
