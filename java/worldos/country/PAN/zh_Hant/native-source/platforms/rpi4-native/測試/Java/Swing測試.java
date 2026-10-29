// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Swing測試 implements Runnable, ActionListener {
    JFrame 窗口;
    JLabel 指南;
    JTextField 輸入值;
    public void run() {
        窗口 = new JFrame("內建 內核值 Swing");
        窗口.setSize(400, 280);
        窗口.setLocationRelativeTo(null);
        窗口.setLayout(null);
        窗口.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        指南 = new JLabel("한글로 Java 코딩");
        指南.setBounds(20, 20, 340, 30);
        輸入值 = new JTextField("名稱");
        輸入值.setBounds(20, 65, 340, 30);
        JButton 按鈕 = new JButton("問候");
        按鈕.setBounds(20, 110, 180, 32);
        按鈕.addActionListener(this);
        窗口.add(指南); 窗口.add(輸入值); 窗口.add(按鈕);
        窗口.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent 事件) {
        指南.setText("안녕하세요 " + 輸入值.getText());
        System.out.println("SWING CLICK " + 輸入值.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Swing測試());
    }
}
