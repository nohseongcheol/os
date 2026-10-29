// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class свинг_тест implements Runnable, ActionListener {
    JFrame Окно;
    JLabel файл_сведений_eb81d7d9;
    JTextField входные_данные_ЗНАЧЕН;
    public void run() {
        Окно = new JFrame("свой ядро_ЗНАЧЕН Swing");
        Окно.setSize(400, 280);
        Окно.setLocationRelativeTo(null);
        Окно.setLayout(null);
        Окно.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        файл_сведений_eb81d7d9 = new JLabel("한글로 Java 코딩");
        файл_сведений_eb81d7d9.setBounds(20, 20, 340, 30);
        входные_данные_ЗНАЧЕН = new JTextField("Название");
        входные_данные_ЗНАЧЕН.setBounds(20, 65, 340, 30);
        JButton кнопка = new JButton("인사하기");
        кнопка.setBounds(20, 110, 180, 32);
        кнопка.addActionListener(this);
        Окно.add(файл_сведений_eb81d7d9); Окно.add(входные_данные_ЗНАЧЕН); Окно.add(кнопка);
        Окно.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Событие) {
        файл_сведений_eb81d7d9.setText("안녕하세요 " + входные_данные_ЗНАЧЕН.getText());
        System.out.println("SWING CLICK " + входные_данные_ЗНАЧЕН.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new свинг_тест());
    }
}
