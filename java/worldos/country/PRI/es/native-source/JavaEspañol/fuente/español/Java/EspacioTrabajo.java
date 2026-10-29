// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.Java;

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

/** Pequeño espacio de trabajo Swing para editar, compilar y ejecutar fuentes Java en el directorio personal. */
public final class EspacioTrabajo {
    private final JFrame ventana = new JFrame("jkoros — Java EspacioTrabajo");
    private final JTextArea fuente = new JTextArea();
    private final JTextArea Salida = new JTextArea(8, 80);
    private final JTextField nombreEntradaElementoArchivo = new JTextField("Saludo.java", 20);
    private final JTextField nombreEntradaElementoClase = new JTextField("Saludo", 16);
    private final Path directorioTrabajoEnCurso = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService valorTareaFondo = Executors.newSingleThreadExecutor();
    private volatile Process valorProceso;
    private final String biblioteca = "/opt/jkoros/lib/JavaEspañol.jar";

    private void notificación(String texto) { SwingUtilities.invokeLater(() -> Salida.append(texto + "\n")); }
    private void botón(JPanel valorVersión, String nombre, Runnable valorComportamiento) {
        JButton botón = new JButton(nombre);
        botón.addActionListener(evento -> valorComportamiento.run());
        valorVersión.add(botón);
    }
    private boolean valorAlmacenar() {
        try {
            Path ruta = directorioTrabajoEnCurso.resolve(nombreEntradaElementoArchivo.getText());
            Files.createDirectories(ruta.getParent());
            Archivo.escribir(ruta, fuente.getText());
            notificación("valorAlmacenar: " + ruta);
            return true;
        } catch (Exception error) { notificación(error.toString()); return false; }
    }
    private void abrir() {
        try { fuente.setText(Archivo.leer(directorioTrabajoEnCurso.resolve(nombreEntradaElementoArchivo.getText()))); }
        catch (Exception error) { notificación(error.toString()); }
    }
    private int comando(List<String> comando) throws Exception {
        valorProceso = new ProcessBuilder(comando).directory(directorioTrabajoEnCurso.toFile()).redirectErrorStream(true).start();
        try (BufferedReader línea = new BufferedReader(new InputStreamReader(valorProceso.getInputStream(), StandardCharsets.UTF_8))) {
            String texto;
            while ((texto = línea.readLine()) != null) notificación(texto);
        }
        int valorEstadoValor = valorProceso.waitFor(); valorProceso = null;
        notificación("programaSalir valorCódigo: " + valorEstadoValor);
        return valorEstadoValor;
    }
    private void traducirFuente(boolean ejecutarComando, boolean archivoCódigoEjecutable) {
        if (!valorAlmacenar()) return;
        String valorEntrada = nombreEntradaElementoArchivo.getText(), valorPuntoEntradaElemento = nombreEntradaElementoClase.getText();
        valorTareaFondo.submit(() -> {
            try {
                Files.createDirectories(directorioTrabajoEnCurso.resolve("classes"));
                if (archivoCódigoEjecutable) {
                    comando(Arrays.asList("jclassc", "--target", "openjdk", "--entry", valorPuntoEntradaElemento,
                        "--classpath", biblioteca, "-o", "실행프로그램", valorEntrada));
                } else if (comando(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", biblioteca,
                        "-d", "classes", valorEntrada)) == 0 && ejecutarComando) {
                    comando(Arrays.asList("java", "-cp", "classes:" + biblioteca, valorPuntoEntradaElemento));
                }
            } catch (Exception error) { notificación(error.toString()); }
        });
    }
    private void ejecuciónPausar() {
        Process elementoListaActual = valorProceso;
        if (elementoListaActual != null) { elementoListaActual.descendants().forEach(ProcessHandle::destroy); elementoListaActual.destroy(); }
    }
    private EspacioTrabajo() throws IOException {
        Files.createDirectories(directorioTrabajoEnCurso);
        Font valorFuenteTipográfica = new Font("Monospaced", Font.PLAIN, 16);
        fuente.setFont(valorFuenteTipográfica); Salida.setFont(valorFuenteTipográfica); Salida.setEditable(false);
        fuente.setTabSize(4);
        fuente.setMargin(new Insets(10, 12, 10, 12));
        Salida.setMargin(new Insets(8, 12, 8, 12));
        fuente.setBackground(new Color(250, 251, 252));
        fuente.setForeground(new Color(32, 43, 58));
        JPanel panelComando = new JPanel();
        panelComando.add(new JLabel("Archivo")); panelComando.add(nombreEntradaElementoArchivo);
        panelComando.add(new JLabel("주 valorClase")); panelComando.add(nombreEntradaElementoClase);
        botón(panelComando, "abrir", this::abrir); botón(panelComando, "valorAlmacenar", this::valorAlmacenar);
        botón(panelComando, "compilarFuente", () -> traducirFuente(false, false));
        botón(panelComando, "ejecutarComando", () -> traducirFuente(true, false));
        botón(panelComando, "ejecutarComando Archivo crearEntradaElemento", () -> traducirFuente(false, true));
        botón(panelComando, "ejecuciónPausar", this::ejecuciónPausar);
        JSplitPane resultadoDivisión = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(fuente), new JScrollPane(Salida));
        resultadoDivisión.setResizeWeight(0.75);
        ventana.add(panelComando, BorderLayout.NORTH); ventana.add(resultadoDivisión, BorderLayout.CENTER);
        ventana.setSize(1200, 750); ventana.setLocationRelativeTo(null);
        ventana.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ventana.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent evento) { ejecuciónPausar(); valorTareaFondo.shutdownNow(); }
        });
        abrir(); ventana.setVisible(true);
    }
    public static void main(String[] argumentos) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource fuenteTipográficaPredeterminado = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object valorEntradaElemento : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(valorEntradaElemento) instanceof Font) UIManager.put(valorEntradaElemento, fuenteTipográficaPredeterminado);
                }
                new EspacioTrabajo();
            } catch (Exception error) { error.printStackTrace(); }
        });
    }
}
