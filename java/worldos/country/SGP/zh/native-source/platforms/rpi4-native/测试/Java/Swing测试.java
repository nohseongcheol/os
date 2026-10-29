// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Swing测试 implements Runnable, ActionListener {
    JFrame 窗口;
    JLabel 指南;
    JTextField 输入值;
    public void run() {
        窗口 = new JFrame("内置 内核值 Swing");
        窗口.setSize(400, 280);
        窗口.setLocationRelativeTo(null);
        窗口.setLayout(null);
        窗口.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        指南 = new JLabel("한글로 Java 코딩");
        指南.setBounds(20, 20, 340, 30);
        输入值 = new JTextField("名称");
        输入值.setBounds(20, 65, 340, 30);
        JButton 按钮 = new JButton("问候");
        按钮.setBounds(20, 110, 180, 32);
        按钮.addActionListener(this);
        窗口.add(指南); 窗口.add(输入值); 窗口.add(按钮);
        窗口.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent 事件) {
        指南.setText("안녕하세요 " + 输入值.getText());
        System.out.println("SWING CLICK " + 输入值.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Swing测试());
    }
}
