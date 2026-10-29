// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame ფანჯარა;
    JLabel წასაკითხი_ფაილი_eb81d7d9;
    JTextField 입력;
    public void run() {
        ფანჯარა = new JFrame("자체 ბირთვი_მნიშვნელობა Swing");
        ფანჯარა.setSize(400, 280);
        ფანჯარა.setLocationRelativeTo(null);
        ფანჯარა.setLayout(null);
        ფანჯარა.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        წასაკითხი_ფაილი_eb81d7d9 = new JLabel("한글로 Java 코딩");
        წასაკითხი_ფაილი_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("სახელი");
        입력.setBounds(20, 65, 340, 30);
        JButton ღილაკი = new JButton("인사하기");
        ღილაკი.setBounds(20, 110, 180, 32);
        ღილაკი.addActionListener(this);
        ფანჯარა.add(წასაკითხი_ფაილი_eb81d7d9); ფანჯარა.add(입력); ფანჯარა.add(ღილაკი);
        ფანჯარა.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent მოვლენა) {
        წასაკითხი_ფაილი_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
