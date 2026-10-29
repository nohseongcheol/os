// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Swing試験 implements Runnable, ActionListener {
    JFrame 窓;
    JLabel 案内;
    JTextField 入力値;
    public void run() {
        窓 = new JFrame("内蔵 中核値 Swing");
        窓.setSize(400, 280);
        窓.setLocationRelativeTo(null);
        窓.setLayout(null);
        窓.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        案内 = new JLabel("한글로 Java 코딩");
        案内.setBounds(20, 20, 340, 30);
        入力値 = new JTextField("名前");
        入力値.setBounds(20, 65, 340, 30);
        JButton ボタン = new JButton("挨拶");
        ボタン.setBounds(20, 110, 180, 32);
        ボタン.addActionListener(this);
        窓.add(案内); 窓.add(入力値); 窓.add(ボタン);
        窓.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent イベント) {
        案内.setText("안녕하세요 " + 入力値.getText());
        System.out.println("SWING CLICK " + 入力値.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Swing試験());
    }
}
