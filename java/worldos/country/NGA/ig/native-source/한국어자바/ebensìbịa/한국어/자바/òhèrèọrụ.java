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

/** òjìàrụ 홈에서 Java 원문을 dezìmà_valuu·wue_ebensìbịa·실행하는 작은 Swing òhèrèọrụ. */
public final class òhèrèọrụ {
    private final JFrame windò = new JFrame("jkoros — 자바 òhèrèọrụ");
    private final JTextArea ebensìbịa = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField ọbọakwụkwọ_ndebà_akara_ahà = new JTextField("인사.java", 20);
    private final JTextField klaàsị_ndebà_akara_ahà = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process ùsòrò_valuu_6712bde7;
    private final String ọbaakwụkwọ = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String SMS) { SwingUtilities.invokeLater(() -> 출력.append(SMS + "\n")); }
    private void ọdụmbi(JPanel ụdị_valuu, String Aha, Runnable 행동) {
        JButton ọdụmbi = new JButton(Aha);
        ọdụmbi.addActionListener(mmèrème -> 행동.run());
        ụdị_valuu.add(ọdụmbi);
    }
    private boolean Store_valuu() {
        try {
            Path ụzọ_ozi = 작업폴더.resolve(ọbọakwụkwọ_ndebà_akara_ahà.getText());
            Files.createDirectories(ụzọ_ozi.getParent());
            Faịlụ.Chekwaa_ozi(ụzọ_ozi, ebensìbịa.getText());
            알림("Store_valuu: " + ụzọ_ozi);
            return true;
        } catch (Exception mmejọ) { 알림(mmejọ.toString()); return false; }
    }
    private void Mepee() {
        try { ebensìbịa.setText(Faịlụ.Wepụta_ọzi(작업폴더.resolve(ọbọakwụkwọ_ndebà_akara_ahà.getText()))); }
        catch (Exception mmejọ) { 알림(mmejọ.toString()); }
    }
    private int Ntiiwu(List<String> Ntiiwu) throws Exception {
        ùsòrò_valuu_6712bde7 = new ProcessBuilder(Ntiiwu).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader ahịrī = new BufferedReader(new InputStreamReader(ùsòrò_valuu_6712bde7.getInputStream(), StandardCharsets.UTF_8))) {
            String SMS;
            while ((SMS = ahịrī.readLine()) != null) 알림(SMS);
        }
        int ọnọdụ_valuu = ùsòrò_valuu_6712bde7.waitFor(); ùsòrò_valuu_6712bde7 = null;
        알림("pụọ_app 코드: " + ọnọdụ_valuu);
        return ọnọdụ_valuu;
    }
    private void Tụgharia_ebensìbịa(boolean mee_nnyemiwu, boolean 실행파일) {
        if (!Store_valuu()) return;
        String 입력 = ọbọakwụkwọ_ndebà_akara_ahà.getText(), ndebà_akara_valuu = klaàsị_ndebà_akara_ahà.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Ntiiwu(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ndebà_akara_valuu,
                        "--classpath", ọbaakwụkwọ, "-o", "실행프로그램", 입력));
                } else if (Ntiiwu(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ọbaakwụkwọ,
                        "-d", "classes", 입력)) == 0 && mee_nnyemiwu) {
                    Ntiiwu(Arrays.asList("java", "-cp", "classes:" + ọbaakwụkwọ, ndebà_akara_valuu));
                }
            } catch (Exception mmejọ) { 알림(mmejọ.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = ùsòrò_valuu_6712bde7;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private òhèrèọrụ() throws IOException {
        Files.createDirectories(작업폴더);
        Font ọnụndèe_valuu = new Font("Monospaced", Font.PLAIN, 16);
        ebensìbịa.setFont(ọnụndèe_valuu); 출력.setFont(ọnụndèe_valuu); 출력.setEditable(false);
        ebensìbịa.setTabSize(4);
        ebensìbịa.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        ebensìbịa.setBackground(new Color(250, 251, 252));
        ebensìbịa.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("Faịlụ")); 명령판.add(ọbọakwụkwọ_ndebà_akara_ahà);
        명령판.add(new JLabel("주 klaàsị_valuu")); 명령판.add(klaàsị_ndebà_akara_ahà);
        ọdụmbi(명령판, "Mepee", this::Mepee); ọdụmbi(명령판, "Store_valuu", this::Store_valuu);
        ọdụmbi(명령판, "wue_ebensìbịa", () -> Tụgharia_ebensìbịa(false, false));
        ọdụmbi(명령판, "mee_nnyemiwu", () -> Tụgharia_ebensìbịa(true, false));
        ọdụmbi(명령판, "mee_nnyemiwu Faịlụ mepụta_ndebà", () -> Tụgharia_ebensìbịa(false, true));
        ọdụmbi(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ebensìbịa), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        windò.add(명령판, BorderLayout.NORTH); windò.add(나눔, BorderLayout.CENTER);
        windò.setSize(1200, 750); windò.setLocationRelativeTo(null);
        windò.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        windò.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent mmèrème) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Mepee(); windò.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ọnụnde_difọlt = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ndebà_valuu : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ndebà_valuu) instanceof Font) UIManager.put(ndebà_valuu, ọnụnde_difọlt);
                }
                new òhèrèọrụ();
            } catch (Exception mmejọ) { mmejọ.printStackTrace(); }
        });
    }
}
