// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.자바;

import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.List;
import java.util.concurrent.*;
import javax.swing.*;
import javax.swing.plaf.FontUIResource;

/** utilizator 홈에서 Java 원문을 edita_VALUE·compilare_sursă·실행하는 작은 Swing spațiu_de_lucru. */
public final class spațiu_de_lucru {
    private final JFrame Fereastră = new JFrame("jkoros — 자바 spațiu_de_lucru");
    private final JTextArea SURSĂ = new JTextArea();
    private final JTextArea Rezultat = new JTextArea(8, 80);
    private final JTextField Fișier_intrare_nume = new JTextField("인사.java", 20);
    private final JTextField Clasă_intrare_nume = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Proces_VALUE;
    private final String bibliotecă = "/opt/jkoros/lib/한국어자바.jar";

    private void înștiințare(String SMS) { SwingUtilities.invokeLater(() -> Rezultat.append(SMS + "\n")); }
    private void buton(JPanel versiune_VALUE, String Nume, Runnable 행동) {
        JButton buton = new JButton(Nume);
        buton.addActionListener(Eveniment -> 행동.run());
        versiune_VALUE.add(buton);
    }
    private boolean Store_VALUE() {
        try {
            Path Cale = 작업폴더.resolve(Fișier_intrare_nume.getText());
            Files.createDirectories(Cale.getParent());
            Fișier.Scriere(Cale, SURSĂ.getText());
            înștiințare("Store_VALUE: " + Cale);
            return true;
        } catch (Exception eroare) { înștiințare(eroare.toString()); return false; }
    }
    private void Deschide() {
        try { SURSĂ.setText(Fișier.Citire(작업폴더.resolve(Fișier_intrare_nume.getText()))); }
        catch (Exception eroare) { înștiințare(eroare.toString()); }
    }
    private int Comandă(List<String> Comandă) throws Exception {
        Proces_VALUE = new ProcessBuilder(Comandă).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Linie = new BufferedReader(new InputStreamReader(Proces_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String SMS;
            while ((SMS = Linie.readLine()) != null) înștiințare(SMS);
        }
        int Stare_VALUE = Proces_VALUE.waitFor(); Proces_VALUE = null;
        înștiințare("ieși_program cod_VALUE: " + Stare_VALUE);
        return Stare_VALUE;
    }
    private void TRANSLATE_sursă(boolean executa_comandă, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = Fișier_intrare_nume.getText(), intrare_p_VALUE = Clasă_intrare_nume.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Comandă(Arrays.asList("jclassc", "--target", "openjdk", "--entry", intrare_p_VALUE,
                        "--classpath", bibliotecă, "-o", "실행프로그램", 입력));
                } else if (Comandă(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", bibliotecă,
                        "-d", "classes", 입력)) == 0 && executa_comandă) {
                    Comandă(Arrays.asList("java", "-cp", "classes:" + bibliotecă, intrare_p_VALUE));
                }
            } catch (Exception eroare) { înștiințare(eroare.toString()); }
        });
    }
    private void Pauză_executare() {
        Process curent_element = Proces_VALUE;
        if (curent_element != null) { curent_element.descendants().forEach(ProcessHandle::destroy); curent_element.destroy(); }
    }
    private spațiu_de_lucru() throws IOException {
        Files.createDirectories(작업폴더);
        Font font_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        SURSĂ.setFont(font_VALUE); Rezultat.setFont(font_VALUE); Rezultat.setEditable(false);
        SURSĂ.setTabSize(4);
        SURSĂ.setMargin(new Insets(10, 12, 10, 12));
        Rezultat.setMargin(new Insets(8, 12, 8, 12));
        SURSĂ.setBackground(new Color(250, 251, 252));
        SURSĂ.setForeground(new Color(32, 43, 58));
        JPanel comandă_panou = new JPanel();
        comandă_panou.add(new JLabel("Fișier")); comandă_panou.add(Fișier_intrare_nume);
        comandă_panou.add(new JLabel("주 Clasă_VALUE")); comandă_panou.add(Clasă_intrare_nume);
        buton(comandă_panou, "Deschide", this::Deschide); buton(comandă_panou, "Store_VALUE", this::Store_VALUE);
        buton(comandă_panou, "compilare_sursă", () -> TRANSLATE_sursă(false, false));
        buton(comandă_panou, "executa_comandă", () -> TRANSLATE_sursă(true, false));
        buton(comandă_panou, "executa_comandă Fișier crea_intrare", () -> TRANSLATE_sursă(false, true));
        buton(comandă_panou, "Pauză_executare", this::Pauză_executare);
        JSplitPane divizie_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(SURSĂ), new JScrollPane(Rezultat));
        divizie_KR.setResizeWeight(0.75);
        Fereastră.add(comandă_panou, BorderLayout.NORTH); Fereastră.add(divizie_KR, BorderLayout.CENTER);
        Fereastră.setSize(1200, 750); Fereastră.setLocationRelativeTo(null);
        Fereastră.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Fereastră.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Eveniment) { Pauză_executare(); 일꾼.shutdownNow(); }
        });
        Deschide(); Fereastră.setVisible(true);
    }
    public static void main(String[] Argumente) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource font_implicit = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object intrare_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(intrare_VALUE) instanceof Font) UIManager.put(intrare_VALUE, font_implicit);
                }
                new spațiu_de_lucru();
            } catch (Exception eroare) { eroare.printStackTrace(); }
        });
    }
}
