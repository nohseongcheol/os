// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame ونڈو;
    JLabel مجھے_پڑھیں_eb81d7d9;
    JTextField 입력;
    public void run() {
        ونڈو = new JFrame("اپنا کرنیل_قدر Swing");
        ونڈو.setSize(400, 280);
        ونڈو.setLocationRelativeTo(null);
        ونڈو.setLayout(null);
        ونڈو.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        مجھے_پڑھیں_eb81d7d9 = new JLabel("한글로 Java 코딩");
        مجھے_پڑھیں_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("نام");
        입력.setBounds(20, 65, 340, 30);
        JButton بٹن = new JButton("인사하기");
        بٹن.setBounds(20, 110, 180, 32);
        بٹن.addActionListener(this);
        ونڈو.add(مجھے_پڑھیں_eb81d7d9); ونڈو.add(입력); ونڈو.add(بٹن);
        ونڈو.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent واقعہ) {
        مجھے_پڑھیں_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
