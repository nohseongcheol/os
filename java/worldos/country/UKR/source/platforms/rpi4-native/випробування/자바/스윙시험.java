// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame Вікно;
    JLabel файл_Readme_eb81d7d9;
    JTextField 입력;
    public void run() {
        Вікно = new JFrame("своє ядро_значення Swing");
        Вікно.setSize(400, 280);
        Вікно.setLocationRelativeTo(null);
        Вікно.setLayout(null);
        Вікно.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        файл_Readme_eb81d7d9 = new JLabel("한글로 Java 코딩");
        файл_Readme_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Назва");
        입력.setBounds(20, 65, 340, 30);
        JButton кнопка = new JButton("인사하기");
        кнопка.setBounds(20, 110, 180, 32);
        кнопка.addActionListener(this);
        Вікно.add(файл_Readme_eb81d7d9); Вікно.add(입력); Вікно.add(кнопка);
        Вікно.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Подія) {
        файл_Readme_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
