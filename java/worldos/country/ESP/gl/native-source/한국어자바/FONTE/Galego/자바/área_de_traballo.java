// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자바;

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

/** usuario 홈에서 Java 원문을 editar_VALOR·compilar_fonte·실행하는 작은 Swing área_de_traballo. */
public final class área_de_traballo {
    private final JFrame Xanela = new JFrame("jkoros — 자바 área_de_traballo");
    private final JTextArea FONTE = new JTextArea();
    private final JTextArea Saída = new JTextArea(8, 80);
    private final JTextField Ficheiro_introdución_nome = new JTextField("인사.java", 20);
    private final JTextField Clase_introdución_nome = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Proceso_VALOR;
    private final String biblioteca = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Texto) { SwingUtilities.invokeLater(() -> Saída.append(Texto + "\n")); }
    private void botón(JPanel versión_VALOR, String Nome, Runnable 행동) {
        JButton botón = new JButton(Nome);
        botón.addActionListener(Evento -> 행동.run());
        versión_VALOR.add(botón);
    }
    private boolean Store_VALOR() {
        try {
            Path CAMIÑO = 작업폴더.resolve(Ficheiro_introdución_nome.getText());
            Files.createDirectories(CAMIÑO.getParent());
            Ficheiro.Escritura(CAMIÑO, FONTE.getText());
            알림("Store_VALOR: " + CAMIÑO);
            return true;
        } catch (Exception ERRO) { 알림(ERRO.toString()); return false; }
    }
    private void Abrir() {
        try { FONTE.setText(Ficheiro.Lectura(작업폴더.resolve(Ficheiro_introdución_nome.getText()))); }
        catch (Exception ERRO) { 알림(ERRO.toString()); }
    }
    private int Orde(List<String> Orde) throws Exception {
        Proceso_VALOR = new ProcessBuilder(Orde).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Liña = new BufferedReader(new InputStreamReader(Proceso_VALOR.getInputStream(), StandardCharsets.UTF_8))) {
            String Texto;
            while ((Texto = Liña.readLine()) != null) 알림(Texto);
        }
        int Estado_VALOR = Proceso_VALOR.waitFor(); Proceso_VALOR = null;
        알림("saír_apl CÓDIGO_VALOR: " + Estado_VALOR);
        return Estado_VALOR;
    }
    private void TRADUCIR_fonte(boolean executar_comando, boolean 실행파일) {
        if (!Store_VALOR()) return;
        String 입력 = Ficheiro_introdución_nome.getText(), introdución_p_VALOR = Clase_introdución_nome.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Orde(Arrays.asList("jclassc", "--target", "openjdk", "--entry", introdución_p_VALOR,
                        "--classpath", biblioteca, "-o", "실행프로그램", 입력));
                } else if (Orde(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", biblioteca,
                        "-d", "classes", 입력)) == 0 && executar_comando) {
                    Orde(Arrays.asList("java", "-cp", "classes:" + biblioteca, introdución_p_VALOR));
                }
            } catch (Exception ERRO) { 알림(ERRO.toString()); }
        });
    }
    private void 멈춤() {
        Process ao_corrente_elemento = Proceso_VALOR;
        if (ao_corrente_elemento != null) { ao_corrente_elemento.descendants().forEach(ProcessHandle::destroy); ao_corrente_elemento.destroy(); }
    }
    private área_de_traballo() throws IOException {
        Files.createDirectories(작업폴더);
        Font tipo_de_letra_VALOR = new Font("Monospaced", Font.PLAIN, 16);
        FONTE.setFont(tipo_de_letra_VALOR); Saída.setFont(tipo_de_letra_VALOR); Saída.setEditable(false);
        FONTE.setTabSize(4);
        FONTE.setMargin(new Insets(10, 12, 10, 12));
        Saída.setMargin(new Insets(8, 12, 8, 12));
        FONTE.setBackground(new Color(250, 251, 252));
        FONTE.setForeground(new Color(32, 43, 58));
        JPanel comando_panel = new JPanel();
        comando_panel.add(new JLabel("Ficheiro")); comando_panel.add(Ficheiro_introdución_nome);
        comando_panel.add(new JLabel("주 Clase_VALOR")); comando_panel.add(Clase_introdución_nome);
        botón(comando_panel, "Abrir", this::Abrir); botón(comando_panel, "Store_VALOR", this::Store_VALOR);
        botón(comando_panel, "compilar_fonte", () -> TRADUCIR_fonte(false, false));
        botón(comando_panel, "executar_comando", () -> TRADUCIR_fonte(true, false));
        botón(comando_panel, "executar_comando Ficheiro crear_introdución", () -> TRADUCIR_fonte(false, true));
        botón(comando_panel, "멈춤", this::멈춤);
        JSplitPane división_medida = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(FONTE), new JScrollPane(Saída));
        división_medida.setResizeWeight(0.75);
        Xanela.add(comando_panel, BorderLayout.NORTH); Xanela.add(división_medida, BorderLayout.CENTER);
        Xanela.setSize(1200, 750); Xanela.setLocationRelativeTo(null);
        Xanela.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Xanela.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Evento) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Abrir(); Xanela.setVisible(true);
    }
    public static void main(String[] Argumentos) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource tipo_de_letra_predefinido = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object introdución_VALOR : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(introdución_VALOR) instanceof Font) UIManager.put(introdución_VALOR, tipo_de_letra_predefinido);
                }
                new área_de_traballo();
            } catch (Exception ERRO) { ERRO.printStackTrace(); }
        });
    }
}
