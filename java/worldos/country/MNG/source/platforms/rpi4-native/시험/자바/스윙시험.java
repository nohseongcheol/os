// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame цонх;
    JLabel заавал_унших_eb81d7d9;
    JTextField 입력;
    public void run() {
        цонх = new JFrame("자체 кернел_утга Swing");
        цонх.setSize(400, 280);
        цонх.setLocationRelativeTo(null);
        цонх.setLayout(null);
        цонх.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        заавал_унших_eb81d7d9 = new JLabel("한글로 Java 코딩");
        заавал_унших_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Нэр");
        입력.setBounds(20, 65, 340, 30);
        JButton товч = new JButton("인사하기");
        товч.setBounds(20, 110, 180, 32);
        товч.addActionListener(this);
        цонх.add(заавал_унших_eb81d7d9); цонх.add(입력); цонх.add(товч);
        цонх.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent үйлдэл) {
        заавал_унших_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
