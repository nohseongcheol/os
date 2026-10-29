// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.CUW.l_es;
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
public final class Taller {
    private final JFrame ventana = new JFrame();
    private final JTextArea fuente = new JTextArea();
    private final JTextArea salida = new JTextArea();
    private final JTextField ruta = new JTextField("fuente.java", 26);
    private final JTextField nombre = new JTextField("fuente", 15);
    private final JTextField argumentos = new JTextField(25);
    private final Properties mensajes = new Properties();
    private final Path directorio = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService hiloTrabajo = Executors.newSingleThreadExecutor();
    private volatile Process proceso;

    private String etiqueta(String clave) {
        return mensajes.getProperty(clave, clave);
    }

    private void añadir(String texto) {
        SwingUtilities.invokeLater(() -> {
            salida.append(texto);
            salida.setCaretPosition(salida.getDocument().getLength());
        });
    }

    private void error(Exception excepción) {
        añadir(etiqueta("error") + ": " + excepción.toString() + "\n");
    }

    private void botón(JPanel panel, String clave, Runnable acción) {
        JButton botón = new JButton(etiqueta(clave));
        botón.addActionListener(suceso -> acción.run());
        panel.add(botón);
    }

    private void cargar() {
        try {
            fuente.setText(Files.readString(directorio.resolve(ruta.getText()), StandardCharsets.UTF_8));
            fuente.setCaretPosition(0);
        } catch (Exception excepción) { error(excepción); }
    }

    private boolean guardar() {
        try {
            Path archivo = directorio.resolve(ruta.getText()).normalize();
            Files.createDirectories(archivo.getParent());
            Files.writeString(archivo, fuente.getText(), StandardCharsets.UTF_8);
            añadir(etiqueta("save") + ": " + archivo + "\n");
            return true;
        } catch (Exception excepción) { error(excepción); return false; }
    }

    private int ejecutar(List<String> orden) throws Exception {
        proceso = new ProcessBuilder(orden).directory(directorio.toFile()).redirectErrorStream(true).start();
        try (BufferedReader lector = new BufferedReader(new InputStreamReader(proceso.getInputStream(), StandardCharsets.UTF_8))) {
            String línea;
            while ((línea = lector.readLine()) != null) añadir(línea + "\n");
        }
        int resultado = proceso.waitFor();
        proceso = null;
        añadir(etiqueta("result") + ": " + resultado + "\n");
        return resultado;
    }

    private void compilar(boolean iniciar) {
        if (!guardar()) return;
        String archivo = directorio.resolve(ruta.getText()).toString();
        String nombreClase = nombre.getText().trim();
        String texto = argumentos.getText();
        hiloTrabajo.submit(() -> {
            try {
                Files.createDirectories(directorio.resolve("classes"));
                int resultado = ejecutar(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", directorio.resolve("classes").toString(), archivo));
                if (iniciar && resultado == 0) {
                    List<String> orden = new ArrayList<>(Arrays.asList("java", "-cp", directorio.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", nombreClase));
                    StreamTokenizer analizador = new StreamTokenizer(new StringReader(texto));
                    analizador.resetSyntax(); analizador.wordChars(33, 65535); analizador.whitespaceChars(0, 32);
                    analizador.quoteChar('"'); analizador.quoteChar('\'');
                    while (analizador.nextToken() != StreamTokenizer.TT_EOF) orden.add(analizador.sval);
                    ejecutar(orden);
                }
            } catch (Exception excepción) { error(excepción); }
        });
    }

    private void detener() {
        Process procesoActual = proceso;
        if (procesoActual != null) {
            procesoActual.descendants().forEach(ProcessHandle::destroyForcibly);
            procesoActual.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(directorio.toFile()).start(); }
        catch (Exception excepción) { error(excepción); }
    }

    private void elegir() {
        JFileChooser selector = new JFileChooser(directorio.toFile());
        if (selector.showOpenDialog(ventana) == JFileChooser.APPROVE_OPTION) {
            ruta.setText(selector.getSelectedFile().getAbsolutePath());
            cargar();
        }
    }

    private void inicializar() {
        try (Reader lector = new InputStreamReader(Taller.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            mensajes.load(lector);
            Files.createDirectories(directorio);
        } catch (Exception excepción) { throw new IllegalStateException(excepción); }
        ventana.setTitle(etiqueta("workspace") + " · WorldOS " + etiqueta("identity"));
        ventana.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ventana.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent suceso) {
                detener(); hiloTrabajo.shutdownNow(); System.exit(0);
            }
        });
        fuente.setFont(new Font("Monospaced", Font.PLAIN, 17));
        fuente.setTabSize(4);
        salida.setFont(new Font("Monospaced", Font.PLAIN, 14));
        salida.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel archivo = new JPanel(new FlowLayout(FlowLayout.LEADING));
        archivo.add(new JLabel(etiqueta("file"))); archivo.add(ruta);
        panel.add(archivo);
        JPanel barraHerramientas = new JPanel(new FlowLayout(FlowLayout.LEADING));
        botón(barraHerramientas, "open", () -> elegir());
        botón(barraHerramientas, "save", () -> guardar());
        botón(barraHerramientas, "compile", () -> compilar(false));
        botón(barraHerramientas, "run", () -> compilar(true));
        botón(barraHerramientas, "stop", () -> detener());
        botón(barraHerramientas, "terminal", () -> terminal());
        panel.add(barraHerramientas);
        JPanel ajustes = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ajustes.add(new JLabel(etiqueta("class"))); ajustes.add(nombre);
        ajustes.add(new JLabel(etiqueta("arguments"))); ajustes.add(argumentos);
        panel.add(ajustes);
        JSplitPane separar = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(fuente), new JScrollPane(salida));
        separar.setResizeWeight(0.72);
        ventana.add(panel, BorderLayout.NORTH);
        ventana.add(separar, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(etiqueta("locale"))));
        separar.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        fuente.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        salida.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension tamaño = Toolkit.getDefaultToolkit().getScreenSize();
        ventana.setSize(Math.min(1240, tamaño.width - 40), Math.min(760, tamaño.height - 60));
        ventana.setLocationRelativeTo(null);
        ventana.setVisible(true);
        cargar();
        separar.setDividerLocation(0.72);
        añadir("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        añadir(etiqueta("help") + "\n");
    }

    public static void main(String[] argumentos) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Taller().inicializar());
    }
}
