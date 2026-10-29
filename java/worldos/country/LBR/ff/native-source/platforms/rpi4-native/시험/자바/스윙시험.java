// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame falanteere;
    JLabel TARƊOO_eb81d7d9;
    JTextField 입력;
    public void run() {
        falanteere = new JFrame("자체 aaluude_njaru Swing");
        falanteere.setSize(400, 280);
        falanteere.setLocationRelativeTo(null);
        falanteere.setLayout(null);
        falanteere.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        TARƊOO_eb81d7d9 = new JLabel("한글로 Java 코딩");
        TARƊOO_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("innde");
        입력.setBounds(20, 65, 340, 30);
        JButton feɗoode = new JButton("인사하기");
        feɗoode.setBounds(20, 110, 180, 32);
        feɗoode.addActionListener(this);
        falanteere.add(TARƊOO_eb81d7d9); falanteere.add(입력); falanteere.add(feɗoode);
        falanteere.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent saɗteende) {
        TARƊOO_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
