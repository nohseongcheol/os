// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame ജാലകം;
    JLabel readme_ഫയല്_eb81d7d9;
    JTextField 입력;
    public void run() {
        ജാലകം = new JFrame("자체 കെര്_ണല്_മൂല്യം Swing");
        ജാലകം.setSize(400, 280);
        ജാലകം.setLocationRelativeTo(null);
        ജാലകം.setLayout(null);
        ജാലകം.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        readme_ഫയല്_eb81d7d9 = new JLabel("한글로 Java 코딩");
        readme_ഫയല്_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("പേരു്");
        입력.setBounds(20, 65, 340, 30);
        JButton ബട്ടണ് = new JButton("인사하기");
        ബട്ടണ്.setBounds(20, 110, 180, 32);
        ബട്ടണ്.addActionListener(this);
        ജാലകം.add(readme_ഫയല്_eb81d7d9); ജാലകം.add(입력); ജാലകം.add(ബട്ടണ്);
        ജാലകം.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ഇവന്റ്) {
        readme_ഫയല്_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
