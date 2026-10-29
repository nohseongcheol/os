// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame тәрәз;
    JLabel Белешмә_файлы_eb81d7d9;
    JTextField 입력;
    public void run() {
        тәрәз = new JFrame("자체 төш_VALUE Swing");
        тәрәз.setSize(400, 280);
        тәрәз.setLocationRelativeTo(null);
        тәрәз.setLayout(null);
        тәрәз.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        Белешмә_файлы_eb81d7d9 = new JLabel("한글로 Java 코딩");
        Белешмә_файлы_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("исем");
        입력.setBounds(20, 65, 340, 30);
        JButton төймә = new JButton("인사하기");
        төймә.setBounds(20, 110, 180, 32);
        төймә.addActionListener(this);
        тәрәз.add(Белешмә_файлы_eb81d7d9); тәрәз.add(입력); тәрәз.add(төймә);
        тәрәз.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent вакыйга) {
        Белешмә_файлы_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
