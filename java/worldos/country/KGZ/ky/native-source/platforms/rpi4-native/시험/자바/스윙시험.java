// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame терезе;
    JLabel readme_файл_eb81d7d9;
    JTextField 입력;
    public void run() {
        терезе = new JFrame("자체 өзөк_маани Swing");
        терезе.setSize(400, 280);
        терезе.setLocationRelativeTo(null);
        терезе.setLayout(null);
        терезе.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        readme_файл_eb81d7d9 = new JLabel("한글로 Java 코딩");
        readme_файл_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Аты");
        입력.setBounds(20, 65, 340, 30);
        JButton баскыч = new JButton("인사하기");
        баскыч.setBounds(20, 110, 180, 32);
        баскыч.addActionListener(this);
        терезе.add(readme_файл_eb81d7d9); терезе.add(입력); терезе.add(баскыч);
        терезе.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent окуя) {
        readme_файл_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
