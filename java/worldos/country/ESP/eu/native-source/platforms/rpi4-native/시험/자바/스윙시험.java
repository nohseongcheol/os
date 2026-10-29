// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame Leihoa;
    JLabel IRAKHAU_eb81d7d9;
    JTextField 입력;
    public void run() {
        Leihoa = new JFrame("자체 nukleo_balio Swing");
        Leihoa.setSize(400, 280);
        Leihoa.setLocationRelativeTo(null);
        Leihoa.setLayout(null);
        Leihoa.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        IRAKHAU_eb81d7d9 = new JLabel("한글로 Java 코딩");
        IRAKHAU_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Izena");
        입력.setBounds(20, 65, 340, 30);
        JButton botoia = new JButton("인사하기");
        botoia.setBounds(20, 110, 180, 32);
        botoia.addActionListener(this);
        Leihoa.add(IRAKHAU_eb81d7d9); Leihoa.add(입력); Leihoa.add(botoia);
        Leihoa.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Gertaera) {
        IRAKHAU_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
