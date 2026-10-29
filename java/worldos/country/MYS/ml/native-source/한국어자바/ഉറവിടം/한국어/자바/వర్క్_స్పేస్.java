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

/** ഉപയോക്താവ് 홈에서 Java 원문을 ചിട്ടപ്പെടുത്തല്_മൂല്യം·കംപൈല്_ചെയ്യുക_ഉറവിടം·실행하는 작은 Swing వర్క్_స్పేస్. */
public final class వర్క్_స్పేస్ {
    private final JFrame ജാലകം = new JFrame("jkoros — 자바 వర్క్_స్పేస్");
    private final JTextArea ഉറവിടം = new JTextArea();
    private final JTextArea ഫലം = new JTextArea(8, 80);
    private final JTextField ഫയല്_എന്_ട്രി_നാ_മം = new JTextField("인사.java", 20);
    private final JTextField ക്ലാസ്_എന്_ട്രി_നാ_മം = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process പ്രോസസ്_മൂല്യം;
    private final String లైబ్రరీ = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String പദാവലി) { SwingUtilities.invokeLater(() -> ഫലം.append(പദാവലി + "\n")); }
    private void ബട്ടണ്(JPanel പതിപ്പ്_മൂല്യം, String പേരു്, Runnable 행동) {
        JButton ബട്ടണ് = new JButton(പേരു്);
        ബട്ടണ്.addActionListener(ഇവന്റ് -> 행동.run());
        പതിപ്പ്_മൂല്യം.add(ബട്ടണ്);
    }
    private boolean സ്_റ്റോർ_മൂല്യം() {
        try {
            Path വഴി = 작업폴더.resolve(ഫയല്_എന്_ട്രി_നാ_മം.getText());
            Files.createDirectories(വഴി.getParent());
            ഫയല്.എഴുത്തു്(വഴി, ഉറവിടം.getText());
            알림("സ്_റ്റോർ_മൂല്യം: " + വഴി);
            return true;
        } catch (Exception പിശക്) { 알림(പിശക്.toString()); return false; }
    }
    private void തുറക്കുക() {
        try { ഉറവിടം.setText(ഫയല്.വായന(작업폴더.resolve(ഫയല്_എന്_ട്രി_നാ_മം.getText()))); }
        catch (Exception പിശക്) { 알림(പിശക്.toString()); }
    }
    private int ആജ്ഞ(List<String> ആജ്ഞ) throws Exception {
        പ്രോസസ്_മൂല്യം = new ProcessBuilder(ആജ്ഞ).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader ലൈൻ = new BufferedReader(new InputStreamReader(പ്രോസസ്_മൂല്യം.getInputStream(), StandardCharsets.UTF_8))) {
            String പദാവലി;
            while ((പദാവലി = ലൈൻ.readLine()) != null) 알림(പദാവലി);
        }
        int അവസ്ഥ_മൂല്യം = പ്രോസസ്_മൂല്യം.waitFor(); പ്രോസസ്_മൂല്യം = null;
        알림("പുറത്തുകടക്കൽ_പ്രോഗ്രാം കോഡ്_മൂല്യം: " + അവസ്ഥ_മൂല്യം);
        return അവസ്ഥ_മൂല്യം;
    }
    private void വിവർത്തനം_ചെയ്യുക_ഉറവിടം(boolean നടപ്പാക്കുക_കമാന്_ഡ്, boolean നിര്_വ്വഹണക്ഷമമായ_ഫയല്) {
        if (!സ്_റ്റോർ_മൂല്യം()) return;
        String 입력 = ഫയല്_എന്_ട്രി_നാ_മം.getText(), എന്_ട്രി_പോയിന്_റ്_മൂല്യം = ക്ലാസ്_എന്_ട്രി_നാ_മം.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (നിര്_വ്വഹണക്ഷമമായ_ഫയല്) {
                    ആജ്ഞ(Arrays.asList("jclassc", "--target", "openjdk", "--entry", എന്_ട്രി_പോയിന്_റ്_മൂല്യം,
                        "--classpath", లైబ్రరీ, "-o", "실행프로그램", 입력));
                } else if (ആജ്ഞ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", లైబ్రరీ,
                        "-d", "classes", 입력)) == 0 && നടപ്പാക്കുക_കമാന്_ഡ്) {
                    ആജ്ഞ(Arrays.asList("java", "-cp", "classes:" + లైబ్రరీ, എന്_ട്രി_പോയിന്_റ്_മൂല്യം));
                }
            } catch (Exception പിശക്) { 알림(പിശക്.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = പ്രോസസ്_മൂല്യം;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private వర్క్_స్పేస్() throws IOException {
        Files.createDirectories(작업폴더);
        Font ഫോണ്ട്_മൂല്യം = new Font("Monospaced", Font.PLAIN, 16);
        ഉറവിടം.setFont(ഫോണ്ട്_മൂല്യം); ഫലം.setFont(ഫോണ്ട്_മൂല്യം); ഫലം.setEditable(false);
        ഉറവിടം.setTabSize(4);
        ഉറവിടം.setMargin(new Insets(10, 12, 10, 12));
        ഫലം.setMargin(new Insets(8, 12, 8, 12));
        ഉറവിടം.setBackground(new Color(250, 251, 252));
        ഉറവിടം.setForeground(new Color(32, 43, 58));
        JPanel കമാന്_ഡ്_പാനൽ = new JPanel();
        കമാന്_ഡ്_പാനൽ.add(new JLabel("ഫയല്")); കമാന്_ഡ്_പാനൽ.add(ഫയല്_എന്_ട്രി_നാ_മം);
        കമാന്_ഡ്_പാനൽ.add(new JLabel("주 ക്ലാസ്_മൂല്യം")); കമാന്_ഡ്_പാനൽ.add(ക്ലാസ്_എന്_ട്രി_നാ_മം);
        ബട്ടണ്(കമാന്_ഡ്_പാനൽ, "തുറക്കുക", this::തുറക്കുക); ബട്ടണ്(കമാന്_ഡ്_പാനൽ, "സ്_റ്റോർ_മൂല്യം", this::സ്_റ്റോർ_മൂല്യം);
        ബട്ടണ്(കമാന്_ഡ്_പാനൽ, "കംപൈല്_ചെയ്യുക_ഉറവിടം", () -> വിവർത്തനം_ചെയ്യുക_ഉറവിടം(false, false));
        ബട്ടണ്(കമാന്_ഡ്_പാനൽ, "നടപ്പാക്കുക_കമാന്_ഡ്", () -> വിവർത്തനം_ചെയ്യുക_ഉറവിടം(true, false));
        ബട്ടണ്(കമാന്_ഡ്_പാനൽ, "നടപ്പാക്കുക_കമാന്_ഡ് ഫയല് സൃഷ്_ടിക്കുക_എന്_ട്രി", () -> വിവർത്തനം_ചെയ്യുക_ഉറവിടം(false, true));
        ബട്ടണ്(കമാന്_ഡ്_പാനൽ, "멈춤", this::멈춤);
        JSplitPane ഹരണം_അളവ് = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ഉറവിടം), new JScrollPane(ഫലം));
        ഹരണം_അളവ്.setResizeWeight(0.75);
        ജാലകം.add(കമാന്_ഡ്_പാനൽ, BorderLayout.NORTH); ജാലകം.add(ഹരണം_അളവ്, BorderLayout.CENTER);
        ജാലകം.setSize(1200, 750); ജാലകം.setLocationRelativeTo(null);
        ജാലകം.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ജാലകം.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ഇവന്റ്) { 멈춤(); 일꾼.shutdownNow(); }
        });
        തുറക്കുക(); ജാലകം.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource സ്ഥിരസ്ഥിതി_ഫോണ്ട് = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object എന്_ട്രി_മൂല്യം : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(എന്_ട്രി_മൂല്യം) instanceof Font) UIManager.put(എന്_ട്രി_മൂല്യം, സ്ഥിരസ്ഥിതി_ഫോണ്ട്);
                }
                new వర్క్_స్పేస్();
            } catch (Exception പിശക്) { പിശക്.printStackTrace(); }
        });
    }
}
