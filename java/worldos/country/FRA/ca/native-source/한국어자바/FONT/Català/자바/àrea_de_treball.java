// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.자바;

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

/** usuari 홈에서 Java 원문을 Editar_VALOR·generar_font·실행하는 작은 Swing àrea_de_treball. */
public final class àrea_de_treball {
    private final JFrame Finestra = new JFrame("jkoros — 자바 àrea_de_treball");
    private final JTextArea FONT = new JTextArea();
    private final JTextArea Sortida = new JTextArea(8, 80);
    private final JTextField arxiu_introducció_nom = new JTextField("인사.java", 20);
    private final JTextField Classe_introducció_nom = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Procés_VALOR;
    private final String biblioteca = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String SMS) { SwingUtilities.invokeLater(() -> Sortida.append(SMS + "\n")); }
    private void Botó(JPanel versió_VALOR, String Nom, Runnable 행동) {
        JButton Botó = new JButton(Nom);
        Botó.addActionListener(Esdeveniment -> 행동.run());
        versió_VALOR.add(Botó);
    }
    private boolean Store_VALOR() {
        try {
            Path Camí = 작업폴더.resolve(arxiu_introducció_nom.getText());
            Files.createDirectories(Camí.getParent());
            Fitxer.Escriptura(Camí, FONT.getText());
            알림("Store_VALOR: " + Camí);
            return true;
        } catch (Exception s_ha_produït_un_error) { 알림(s_ha_produït_un_error.toString()); return false; }
    }
    private void Obre() {
        try { FONT.setText(Fitxer.Lectura(작업폴더.resolve(arxiu_introducció_nom.getText()))); }
        catch (Exception s_ha_produït_un_error) { 알림(s_ha_produït_un_error.toString()); }
    }
    private int Ordre(List<String> Ordre) throws Exception {
        Procés_VALOR = new ProcessBuilder(Ordre).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader línia = new BufferedReader(new InputStreamReader(Procés_VALOR.getInputStream(), StandardCharsets.UTF_8))) {
            String SMS;
            while ((SMS = línia.readLine()) != null) 알림(SMS);
        }
        int Estat_VALOR = Procés_VALOR.waitFor(); Procés_VALOR = null;
        알림("Surt_programa CODI_VALOR: " + Estat_VALOR);
        return Estat_VALOR;
    }
    private void TRADUEIX_font(boolean Executa_ordre, boolean 실행파일) {
        if (!Store_VALOR()) return;
        String 입력 = arxiu_introducció_nom.getText(), introducció_p_VALOR = Classe_introducció_nom.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Ordre(Arrays.asList("jclassc", "--target", "openjdk", "--entry", introducció_p_VALOR,
                        "--classpath", biblioteca, "-o", "실행프로그램", 입력));
                } else if (Ordre(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", biblioteca,
                        "-d", "classes", 입력)) == 0 && Executa_ordre) {
                    Ordre(Arrays.asList("java", "-cp", "classes:" + biblioteca, introducció_p_VALOR));
                }
            } catch (Exception s_ha_produït_un_error) { 알림(s_ha_produït_un_error.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Procés_VALOR;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private àrea_de_treball() throws IOException {
        Files.createDirectories(작업폴더);
        Font tipus_de_lletra_VALOR = new Font("Monospaced", Font.PLAIN, 16);
        FONT.setFont(tipus_de_lletra_VALOR); Sortida.setFont(tipus_de_lletra_VALOR); Sortida.setEditable(false);
        FONT.setTabSize(4);
        FONT.setMargin(new Insets(10, 12, 10, 12));
        Sortida.setMargin(new Insets(8, 12, 8, 12));
        FONT.setBackground(new Color(250, 251, 252));
        FONT.setForeground(new Color(32, 43, 58));
        JPanel ordre_tauler = new JPanel();
        ordre_tauler.add(new JLabel("Fitxer")); ordre_tauler.add(arxiu_introducció_nom);
        ordre_tauler.add(new JLabel("주 Classe_VALOR")); ordre_tauler.add(Classe_introducció_nom);
        Botó(ordre_tauler, "Obre", this::Obre); Botó(ordre_tauler, "Store_VALOR", this::Store_VALOR);
        Botó(ordre_tauler, "generar_font", () -> TRADUEIX_font(false, false));
        Botó(ordre_tauler, "Executa_ordre", () -> TRADUEIX_font(true, false));
        Botó(ordre_tauler, "Executa_ordre Fitxer Crear_introducció", () -> TRADUEIX_font(false, true));
        Botó(ordre_tauler, "멈춤", this::멈춤);
        JSplitPane divisió_mesura = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(FONT), new JScrollPane(Sortida));
        divisió_mesura.setResizeWeight(0.75);
        Finestra.add(ordre_tauler, BorderLayout.NORTH); Finestra.add(divisió_mesura, BorderLayout.CENTER);
        Finestra.setSize(1200, 750); Finestra.setLocationRelativeTo(null);
        Finestra.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Finestra.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Esdeveniment) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Obre(); Finestra.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource tipus_de_lletra_per_defecte = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object introducció_VALOR : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(introducció_VALOR) instanceof Font) UIManager.put(introducció_VALOR, tipus_de_lletra_per_defecte);
                }
                new àrea_de_treball();
            } catch (Exception s_ha_produït_un_error) { s_ha_produït_un_error.printStackTrace(); }
        });
    }
}
