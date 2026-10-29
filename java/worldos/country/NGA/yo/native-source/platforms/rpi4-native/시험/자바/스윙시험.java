// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame wínńdò;
    JLabel KÀ_MÍ_eb81d7d9;
    JTextField 입력;
    public void run() {
        wínńdò = new JFrame("자체 kánẹ́ẹ̀lì_iye Swing");
        wínńdò.setSize(400, 280);
        wínńdò.setLocationRelativeTo(null);
        wínńdò.setLayout(null);
        wínńdò.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        KÀ_MÍ_eb81d7d9 = new JLabel("한글로 Java 코딩");
        KÀ_MÍ_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Orúkọ");
        입력.setBounds(20, 65, 340, 30);
        JButton bọ́tìnnì = new JButton("인사하기");
        bọ́tìnnì.setBounds(20, 110, 180, 32);
        bọ́tìnnì.addActionListener(this);
        wínńdò.add(KÀ_MÍ_eb81d7d9); wínńdò.add(입력); wínńdò.add(bọ́tìnnì);
        wínńdò.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ìgbéṣẹ̀) {
        KÀ_MÍ_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
