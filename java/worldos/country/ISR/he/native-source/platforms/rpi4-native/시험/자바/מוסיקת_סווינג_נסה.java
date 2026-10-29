// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class מוסיקת_סווינג_נסה implements Runnable, ActionListener {
    JFrame חלון;
    JLabel 안내;
    JTextField קלט_ערך;
    public void run() {
        חלון = new JFrame("עצמי ליבה_ערך Swing");
        חלון.setSize(400, 280);
        חלון.setLocationRelativeTo(null);
        חלון.setLayout(null);
        חלון.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        안내 = new JLabel("한글로 Java 코딩");
        안내.setBounds(20, 20, 340, 30);
        קלט_ערך = new JTextField("שם");
        קלט_ערך.setBounds(20, 65, 340, 30);
        JButton לחצן = new JButton("인사하기");
        לחצן.setBounds(20, 110, 180, 32);
        לחצן.addActionListener(this);
        חלון.add(안내); חלון.add(קלט_ערך); חלון.add(לחצן);
        חלון.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent אירוע) {
        안내.setText("안녕하세요 " + קלט_ערך.getText());
        System.out.println("SWING CLICK " + קלט_ערך.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new מוסיקת_סווינג_נסה());
    }
}
