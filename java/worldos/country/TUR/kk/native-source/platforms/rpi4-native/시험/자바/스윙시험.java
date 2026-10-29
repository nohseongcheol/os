// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame Терезе;
    JLabel readme_файлы_eb81d7d9;
    JTextField 입력;
    public void run() {
        Терезе = new JFrame("자체 ядро_мән Swing");
        Терезе.setSize(400, 280);
        Терезе.setLocationRelativeTo(null);
        Терезе.setLayout(null);
        Терезе.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        readme_файлы_eb81d7d9 = new JLabel("한글로 Java 코딩");
        readme_файлы_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Аты");
        입력.setBounds(20, 65, 340, 30);
        JButton батырма = new JButton("인사하기");
        батырма.setBounds(20, 110, 180, 32);
        батырма.addActionListener(this);
        Терезе.add(readme_файлы_eb81d7d9); Терезе.add(입력); Терезе.add(батырма);
        Терезе.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Оқиға) {
        readme_файлы_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
