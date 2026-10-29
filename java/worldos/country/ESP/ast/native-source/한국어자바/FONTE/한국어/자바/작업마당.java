// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

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

/** 사용자 홈에서 Java 원문을 편집·컴파일·실행하는 작은 Swing 작업마당. */
public final class 작업마당 {
    private final JFrame Ventana = new JFrame("jkoros — 자바 작업마당");
    private final JTextArea FONTE = new JTextArea();
    private final JTextArea Salida = new JTextArea(8, 80);
    private final JTextField 파일이름 = new JTextField("인사.java", 20);
    private final JTextField 클래스이름 = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process 과정;
    private final String 라이브러리 = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Testu) { SwingUtilities.invokeLater(() -> Salida.append(Testu + "\n")); }
    private void Botón(JPanel 판, String Nome, Runnable 행동) {
        JButton Botón = new JButton(Nome);
        Botón.addActionListener(Eventu -> 행동.run());
        판.add(Botón);
    }
    private boolean 저장() {
        try {
            Path Camín = 작업폴더.resolve(파일이름.getText());
            Files.createDirectories(Camín.getParent());
            Ficheru.Escritura(Camín, FONTE.getText());
            알림("저장: " + Camín);
            return true;
        } catch (Exception Fallu) { 알림(Fallu.toString()); return false; }
    }
    private void Abrir() {
        try { FONTE.setText(Ficheru.Llectura(작업폴더.resolve(파일이름.getText()))); }
        catch (Exception Fallu) { 알림(Fallu.toString()); }
    }
    private int Comandu(List<String> Comandu) throws Exception {
        과정 = new ProcessBuilder(Comandu).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Llinia = new BufferedReader(new InputStreamReader(과정.getInputStream(), StandardCharsets.UTF_8))) {
            String Testu;
            while ((Testu = Llinia.readLine()) != null) 알림(Testu);
        }
        int 상태 = 과정.waitFor(); 과정 = null;
        알림("종료 코드: " + 상태);
        return 상태;
    }
    private void 번역(boolean 실행, boolean 실행파일) {
        if (!저장()) return;
        String 입력 = 파일이름.getText(), 진입 = 클래스이름.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Comandu(Arrays.asList("jclassc", "--target", "openjdk", "--entry", 진입,
                        "--classpath", 라이브러리, "-o", "실행프로그램", 입력));
                } else if (Comandu(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", 라이브러리,
                        "-d", "classes", 입력)) == 0 && 실행) {
                    Comandu(Arrays.asList("java", "-cp", "classes:" + 라이브러리, 진입));
                }
            } catch (Exception Fallu) { 알림(Fallu.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = 과정;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private 작업마당() throws IOException {
        Files.createDirectories(작업폴더);
        Font 글꼴 = new Font("Monospaced", Font.PLAIN, 16);
        FONTE.setFont(글꼴); Salida.setFont(글꼴); Salida.setEditable(false);
        FONTE.setTabSize(4);
        FONTE.setMargin(new Insets(10, 12, 10, 12));
        Salida.setMargin(new Insets(8, 12, 8, 12));
        FONTE.setBackground(new Color(250, 251, 252));
        FONTE.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("Ficheru")); 명령판.add(파일이름);
        명령판.add(new JLabel("주 클래스")); 명령판.add(클래스이름);
        Botón(명령판, "Abrir", this::Abrir); Botón(명령판, "저장", this::저장);
        Botón(명령판, "컴파일", () -> 번역(false, false));
        Botón(명령판, "실행", () -> 번역(true, false));
        Botón(명령판, "실행 Ficheru 만들기", () -> 번역(false, true));
        Botón(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(FONTE), new JScrollPane(Salida));
        나눔.setResizeWeight(0.75);
        Ventana.add(명령판, BorderLayout.NORTH); Ventana.add(나눔, BorderLayout.CENTER);
        Ventana.setSize(1200, 750); Ventana.setLocationRelativeTo(null);
        Ventana.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Ventana.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Eventu) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Abrir(); Ventana.setVisible(true);
    }
    public static void main(String[] Argumentu) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource 기본글꼴 = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object 항목 : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(항목) instanceof Font) UIManager.put(항목, 기본글꼴);
                }
                new 작업마당();
            } catch (Exception Fallu) { Fallu.printStackTrace(); }
        });
    }
}
