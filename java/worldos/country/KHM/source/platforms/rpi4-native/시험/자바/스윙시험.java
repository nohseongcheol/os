// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame វីនដូ;
    JLabel អានខ្ញុំ_eb81d7d9;
    JTextField 입력;
    public void run() {
        វីនដូ = new JFrame("자체 ខឺណេល_តំលៃ Swing");
        វីនដូ.setSize(400, 280);
        វីនដូ.setLocationRelativeTo(null);
        វីនដូ.setLayout(null);
        វីនដូ.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        អានខ្ញុំ_eb81d7d9 = new JLabel("한글로 Java 코딩");
        អានខ្ញុំ_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("ឈ្មោះ");
        입력.setBounds(20, 65, 340, 30);
        JButton ប៊ូតុង = new JButton("인사하기");
        ប៊ូតុង.setBounds(20, 110, 180, 32);
        ប៊ូតុង.addActionListener(this);
        វីនដូ.add(អានខ្ញុំ_eb81d7d9); វីនដូ.add(입력); វីនដូ.add(ប៊ូតុង);
        វីនដូ.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ព្រឹត្តិការណ៍) {
        អានខ្ញុំ_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
