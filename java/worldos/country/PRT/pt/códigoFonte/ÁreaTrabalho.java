// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.PRT.l_pt;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.List;
import java.util.concurrent.*;
import javax.swing.*;

/** WorldOS project-owned source. Standard Java API names are preserved. */
public final class ÁreaTrabalho {
    private final JFrame Janela = new JFrame();
    private final JTextArea códigoFonte = new JTextArea();
    private final JTextArea saídaTexto = new JTextArea();
    private final JTextField caminho = new JTextField("códigoFonte.java", 26);
    private final JTextField Nome = new JTextField("códigoFonte", 15);
    private final JTextField argumentos = new JTextField(25);
    private final Properties mensagens = new Properties();
    private final Path diretório = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService tarefaSegundoPlano = Executors.newSingleThreadExecutor();
    private volatile Process Processo;

    private String Etiqueta(String Chave) {
        return mensagens.getProperty(Chave, Chave);
    }

    private void adicionar_ao_fim_da_lista(String texto) {
        SwingUtilities.invokeLater(() -> {
            saídaTexto.append(texto);
            saídaTexto.setCaretPosition(saídaTexto.getDocument().getLength());
        });
    }

    private void erro(Exception exception) {
        adicionar_ao_fim_da_lista(Etiqueta("error") + ": " + exception.toString() + "\n");
    }

    private void botão(JPanel Painel, String Chave, Runnable Acção) {
        JButton botão = new JButton(Etiqueta(Chave));
        botão.addActionListener(Evento -> Acção.run());
        Painel.add(botão);
    }

    private void carregarFonte() {
        try {
            códigoFonte.setText(Files.readString(diretório.resolve(caminho.getText()), StandardCharsets.UTF_8));
            códigoFonte.setCaretPosition(0);
        } catch (Exception exception) { erro(exception); }
    }

    private boolean Gravar() {
        try {
            Path ficheiro = diretório.resolve(caminho.getText()).normalize();
            Files.createDirectories(ficheiro.getParent());
            Files.writeString(ficheiro, códigoFonte.getText(), StandardCharsets.UTF_8);
            adicionar_ao_fim_da_lista(Etiqueta("save") + ": " + ficheiro + "\n");
            return true;
        } catch (Exception exception) { erro(exception); return false; }
    }

    private int Executar(List<String> comando) throws Exception {
        Processo = new ProcessBuilder(comando).directory(diretório.toFile()).redirectErrorStream(true).start();
        try (BufferedReader leitorTexto = new BufferedReader(new InputStreamReader(Processo.getInputStream(), StandardCharsets.UTF_8))) {
            String linha_de_entrada;
            while ((linha_de_entrada = leitorTexto.readLine()) != null) adicionar_ao_fim_da_lista(linha_de_entrada + "\n");
        }
        int resultado = Processo.waitFor();
        Processo = null;
        adicionar_ao_fim_da_lista(Etiqueta("result") + ": " + resultado + "\n");
        return resultado;
    }

    private void compilar(boolean iniciar) {
        if (!Gravar()) return;
        String ficheiro = diretório.resolve(caminho.getText()).toString();
        String Classe = Nome.getText().trim();
        String texto = argumentos.getText();
        tarefaSegundoPlano.submit(() -> {
            try {
                Files.createDirectories(diretório.resolve("classes"));
                int resultado = Executar(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", diretório.resolve("classes").toString(), ficheiro));
                if (iniciar && resultado == 0) {
                    List<String> comando = new ArrayList<>(Arrays.asList("java", "-cp", diretório.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Classe));
                    StreamTokenizer analisadorArgumentos = new StreamTokenizer(new StringReader(texto));
                    analisadorArgumentos.resetSyntax(); analisadorArgumentos.wordChars(33, 65535); analisadorArgumentos.whitespaceChars(0, 32);
                    analisadorArgumentos.quoteChar('"'); analisadorArgumentos.quoteChar('\'');
                    while (analisadorArgumentos.nextToken() != StreamTokenizer.TT_EOF) comando.add(analisadorArgumentos.sval);
                    Executar(comando);
                }
            } catch (Exception exception) { erro(exception); }
        });
    }

    private void Parar() {
        Process processoAtual = Processo;
        if (processoAtual != null) {
            processoAtual.descendants().forEach(ProcessHandle::destroyForcibly);
            processoAtual.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(diretório.toFile()).start(); }
        catch (Exception exception) { erro(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(diretório.toFile());
        if (chooser.showOpenDialog(Janela) == JFileChooser.APPROVE_OPTION) {
            caminho.setText(chooser.getSelectedFile().getAbsolutePath());
            carregarFonte();
        }
    }

    private void inicializar() {
        try (Reader leitorTexto = new InputStreamReader(ÁreaTrabalho.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            mensagens.load(leitorTexto);
            Files.createDirectories(diretório);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Janela.setTitle(Etiqueta("workspace") + " · WorldOS " + Etiqueta("identity"));
        Janela.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Janela.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Evento) {
                Parar(); tarefaSegundoPlano.shutdownNow(); System.exit(0);
            }
        });
        códigoFonte.setFont(new Font("Monospaced", Font.PLAIN, 17));
        códigoFonte.setTabSize(4);
        saídaTexto.setFont(new Font("Monospaced", Font.PLAIN, 14));
        saídaTexto.setEditable(false);
        JPanel Painel = new JPanel(new GridLayout(0, 1));
        JPanel ficheiro = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ficheiro.add(new JLabel(Etiqueta("file"))); ficheiro.add(caminho);
        Painel.add(ficheiro);
        JPanel Barra_de_ferramentas = new JPanel(new FlowLayout(FlowLayout.LEADING));
        botão(Barra_de_ferramentas, "open", () -> choose());
        botão(Barra_de_ferramentas, "save", () -> Gravar());
        botão(Barra_de_ferramentas, "compile", () -> compilar(false));
        botão(Barra_de_ferramentas, "run", () -> compilar(true));
        botão(Barra_de_ferramentas, "stop", () -> Parar());
        botão(Barra_de_ferramentas, "terminal", () -> terminal());
        Painel.add(Barra_de_ferramentas);
        JPanel Definições = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Definições.add(new JLabel(Etiqueta("class"))); Definições.add(Nome);
        Definições.add(new JLabel(Etiqueta("arguments"))); Definições.add(argumentos);
        Painel.add(Definições);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(códigoFonte), new JScrollPane(saídaTexto));
        split.setResizeWeight(0.72);
        Janela.add(Painel, BorderLayout.NORTH);
        Janela.add(split, BorderLayout.CENTER);
        Painel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etiqueta("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        códigoFonte.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        saídaTexto.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Tamanho = Toolkit.getDefaultToolkit().getScreenSize();
        Janela.setSize(Math.min(1240, Tamanho.width - 40), Math.min(760, Tamanho.height - 60));
        Janela.setLocationRelativeTo(null);
        Janela.setVisible(true);
        carregarFonte();
        split.setDividerLocation(0.72);
        adicionar_ao_fim_da_lista("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        adicionar_ao_fim_da_lista(Etiqueta("help") + "\n");
    }

    public static void main(String[] argumentos) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new ÁreaTrabalho().inicializar());
    }
}
