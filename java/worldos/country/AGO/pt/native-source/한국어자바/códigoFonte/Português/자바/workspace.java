// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.자바;

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

/** espaço_do_utilizador 홈에서 Java 원문을 Editar_VALOR·compilar_fonte·실행하는 작은 Swing workspace. */
public final class workspace {
    private final JFrame Janela = new JFrame("jkoros — 자바 workspace");
    private final JTextArea códigoFonte = new JTextArea();
    private final JTextArea saídaTexto = new JTextArea(8, 80);
    private final JTextField Arquivo_entrada_nome = new JTextField("saudação_ae353e94.java", 20);
    private final JTextField aula_entrada_nome = new JTextField("saudação_ae353e94", 16);
    private final Path diretório_de_trabalho = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService trabalho_VALOR = Executors.newSingleThreadExecutor();
    private volatile Process Processo_VALOR;
    private final String biblioteca = "/opt/jkoros/lib/한국어자바.jar";

    private void aviso(String texto) { SwingUtilities.invokeLater(() -> saídaTexto.append(texto + "\n")); }
    private void botão(JPanel versão_VALOR, String Nome, Runnable 행동) {
        JButton botão = new JButton(Nome);
        botão.addActionListener(Evento -> 행동.run());
        versão_VALOR.add(botão);
    }
    private boolean Store_VALOR() {
        try {
            Path caminho = diretório_de_trabalho.resolve(Arquivo_entrada_nome.getText());
            Files.createDirectories(caminho.getParent());
            ficheiro.Escrita(caminho, códigoFonte.getText());
            aviso("Store_VALOR: " + caminho);
            return true;
        } catch (Exception erro) { aviso(erro.toString()); return false; }
    }
    private void Abrir() {
        try { códigoFonte.setText(ficheiro.Leitura(diretório_de_trabalho.resolve(Arquivo_entrada_nome.getText()))); }
        catch (Exception erro) { aviso(erro.toString()); }
    }
    private int comando(List<String> comando) throws Exception {
        Processo_VALOR = new ProcessBuilder(comando).directory(diretório_de_trabalho.toFile()).redirectErrorStream(true).start();
        try (BufferedReader linha_de_entrada = new BufferedReader(new InputStreamReader(Processo_VALOR.getInputStream(), StandardCharsets.UTF_8))) {
            String texto;
            while ((texto = linha_de_entrada.readLine()) != null) aviso(texto);
        }
        int Estado_VALOR = Processo_VALOR.waitFor(); Processo_VALOR = null;
        aviso("sair_app valor_do_código: " + Estado_VALOR);
        return Estado_VALOR;
    }
    private void mover_fonte(boolean Executar_comando, boolean executável) {
        if (!Store_VALOR()) return;
        String entrada_VALOR = Arquivo_entrada_nome.getText(), ponto_de_entrada_VALOR = aula_entrada_nome.getText();
        trabalho_VALOR.submit(() -> {
            try {
                Files.createDirectories(diretório_de_trabalho.resolve("classes"));
                if (executável) {
                    comando(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ponto_de_entrada_VALOR,
                        "--classpath", biblioteca, "-o", "실행프로그램", entrada_VALOR));
                } else if (comando(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", biblioteca,
                        "-d", "classes", entrada_VALOR)) == 0 && Executar_comando) {
                    comando(Arrays.asList("java", "-cp", "classes:" + biblioteca, ponto_de_entrada_VALOR));
                }
            } catch (Exception erro) { aviso(erro.toString()); }
        });
    }
    private void Pausar_execução() {
        Process em_dia_item = Processo_VALOR;
        if (em_dia_item != null) { em_dia_item.descendants().forEach(ProcessHandle::destroy); em_dia_item.destroy(); }
    }
    private workspace() throws IOException {
        Files.createDirectories(diretório_de_trabalho);
        Font fonte_VALOR = new Font("Monospaced", Font.PLAIN, 16);
        códigoFonte.setFont(fonte_VALOR); saídaTexto.setFont(fonte_VALOR); saídaTexto.setEditable(false);
        códigoFonte.setTabSize(4);
        códigoFonte.setMargin(new Insets(10, 12, 10, 12));
        saídaTexto.setMargin(new Insets(8, 12, 8, 12));
        códigoFonte.setBackground(new Color(250, 251, 252));
        códigoFonte.setForeground(new Color(32, 43, 58));
        JPanel comando_painel = new JPanel();
        comando_painel.add(new JLabel("ficheiro")); comando_painel.add(Arquivo_entrada_nome);
        comando_painel.add(new JLabel("주 aula_VALOR")); comando_painel.add(aula_entrada_nome);
        botão(comando_painel, "Abrir", this::Abrir); botão(comando_painel, "Store_VALOR", this::Store_VALOR);
        botão(comando_painel, "compilar_fonte", () -> mover_fonte(false, false));
        botão(comando_painel, "Executar_comando", () -> mover_fonte(true, false));
        botão(comando_painel, "Executar_comando ficheiro Criar_entrada", () -> mover_fonte(false, true));
        botão(comando_painel, "Pausar_execução", this::Pausar_execução);
        JSplitPane Divisão_RC = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(códigoFonte), new JScrollPane(saídaTexto));
        Divisão_RC.setResizeWeight(0.75);
        Janela.add(comando_painel, BorderLayout.NORTH); Janela.add(Divisão_RC, BorderLayout.CENTER);
        Janela.setSize(1200, 750); Janela.setLocationRelativeTo(null);
        Janela.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Janela.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Evento) { Pausar_execução(); trabalho_VALOR.shutdownNow(); }
        });
        Abrir(); Janela.setVisible(true);
    }
    public static void main(String[] argumentos) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource fonte_padrão = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object entrada_VALOR_962f286b : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(entrada_VALOR_962f286b) instanceof Font) UIManager.put(entrada_VALOR_962f286b, fonte_padrão);
                }
                new workspace();
            } catch (Exception erro) { erro.printStackTrace(); }
        });
    }
}
