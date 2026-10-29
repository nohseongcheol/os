// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Σουϊνγκ_δοκιμή implements Runnable, ActionListener {
    JFrame Παράθυρο;
    JLabel αρχείο_readme_eb81d7d9;
    JTextField είσοδος_τιμή;
    public void run() {
        Παράθυρο = new JFrame("ίδιο πυρήνας_τιμή Swing");
        Παράθυρο.setSize(400, 280);
        Παράθυρο.setLocationRelativeTo(null);
        Παράθυρο.setLayout(null);
        Παράθυρο.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        αρχείο_readme_eb81d7d9 = new JLabel("한글로 Java 코딩");
        αρχείο_readme_eb81d7d9.setBounds(20, 20, 340, 30);
        είσοδος_τιμή = new JTextField("Όνομα");
        είσοδος_τιμή.setBounds(20, 65, 340, 30);
        JButton κουμπί = new JButton("인사하기");
        κουμπί.setBounds(20, 110, 180, 32);
        κουμπί.addActionListener(this);
        Παράθυρο.add(αρχείο_readme_eb81d7d9); Παράθυρο.add(είσοδος_τιμή); Παράθυρο.add(κουμπί);
        Παράθυρο.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Συμβάν) {
        αρχείο_readme_eb81d7d9.setText("안녕하세요 " + είσοδος_τιμή.getText());
        System.out.println("SWING CLICK " + είσοδος_τιμή.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Σουϊνγκ_δοκιμή());
    }
}
