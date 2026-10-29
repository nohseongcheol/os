// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame சாளரம்;
    JLabel பயனர்_உதவிக்_கோப்பு_eb81d7d9;
    JTextField 입력;
    public void run() {
        சாளரம் = new JFrame("자체 கரு_மதிப்பு Swing");
        சாளரம்.setSize(400, 280);
        சாளரம்.setLocationRelativeTo(null);
        சாளரம்.setLayout(null);
        சாளரம்.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        பயனர்_உதவிக்_கோப்பு_eb81d7d9 = new JLabel("한글로 Java 코딩");
        பயனர்_உதவிக்_கோப்பு_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("பெயர்");
        입력.setBounds(20, 65, 340, 30);
        JButton பொத்தான் = new JButton("인사하기");
        பொத்தான்.setBounds(20, 110, 180, 32);
        பொத்தான்.addActionListener(this);
        சாளரம்.add(பயனர்_உதவிக்_கோப்பு_eb81d7d9); சாளரம்.add(입력); சாளரம்.add(பொத்தான்);
        சாளரம்.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent நிகழ்வு) {
        பயனர்_உதவிக்_கோப்பு_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
