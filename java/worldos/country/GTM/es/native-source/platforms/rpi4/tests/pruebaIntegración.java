// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import español.Java.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import javax.swing.*;
import java.net.*;
import java.io.*;
import java.nio.file.*;
import java.time.Duration;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class pruebaIntegración {
    interface valor { long leer(); }
    static class valorPadre { protected long valor = 42; }
    static class valorHijo extends valorPadre implements valor { public long leer() { return valor; } }
    private static void verificar(boolean condición, String nombre) {
        if (!condición) throw new AssertionError(nombre);
        System.out.println("PASS " + nombre);
    }
    public static void main(String[] argumentos) throws Exception {
        String texto = "한글 日本語 العربية हिन्दी 😀";
        Path valorAlmacenar = Path.of(System.getProperty("user.home"), "datosValidación.txt");
        Archivo.escribir(valorAlmacenar, texto);
        verificar(Archivo.leer(valorAlmacenar).equals(texto), "UTF8_FILE");
        verificar(Caracteres.númeroElementosPuntoCódigo("한😀") == 2, "UNICODE");
        verificar(Caracteres.normalizarValor("\u1100\u1161").equals("가"), "NORMALIZATION");
        valor valorObjeto = new valorHijo();
        verificar(valorObjeto.leer() == 42 && (long)valorHijo.class.getMethod("leer").invoke(valorObjeto) == 42, "OBJECT_INHERITANCE_REFLECTION");
        verificar(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("validar"); }
        catch (IOException excepción) { verificar(excepción.getMessage().equals("validar"), "EXCEPTION"); }
        AtomicInteger valorTotalSuma = new AtomicInteger();
        Thread valorHiloEjecución = Tarea.ponerEnMarcha("한글 valorHiloEjecución", () -> valorTotalSuma.set(123));
        Tarea.esperarFin(valorHiloEjecución);
        verificar(valorTotalSuma.get() == 123, "THREAD");
        ExecutorService valorTareaFondo = Executors.newSingleThreadExecutor();
        try (ServerSocket valorServidor = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> respuesta = valorTareaFondo.submit(() -> {
                try (Socket valorConectorRed = valorServidor.accept()) {
                    BufferedReader leer = new BufferedReader(new InputStreamReader(valorConectorRed.getInputStream()));
                    String línea;
                    while ((línea = leer.readLine()) != null && !línea.isEmpty()) {}
                    byte[] textoCuerpo = Caracteres.codificar(texto);
                    valorConectorRed.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + textoCuerpo.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    valorConectorRed.getOutputStream().write(textoCuerpo);
                } catch (IOException error) { throw new UncheckedIOException(error); }
            });
            verificar(Comunicación.valorTomar(URI.create("http://127.0.0.1:" + valorServidor.getLocalPort()), Duration.ofSeconds(30)).body().equals(texto), "HTTP_TCP");
            respuesta.get(30, TimeUnit.SECONDS);
        } finally { valorTareaFondo.shutdownNow(); }
        verificar(new ProcessBuilder("/bin/echo", "valorProceso").start().waitFor() == 0, "PROCESS");
        if (argumentos.length > 0 && argumentos[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font valorFuenteTipográfica = new Font("Dialog", Font.PLAIN, 18);
                verificar(valorFuenteTipográfica.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                verificar(valorFuenteTipográfica.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea CajaTexto = new JTextArea(texto);
                CajaTexto.setFont(valorFuenteTipográfica);
                JFrame ventana = Pantalla.ventana("그래픽 validar", CajaTexto, 800, 240);
                BufferedImage Dibujo = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D valorPincel = Dibujo.createGraphics();
                ventana.paint(valorPincel); valorPincel.dispose();
                try { javax.imageio.ImageIO.write(Dibujo, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException error) { throw new UncheckedIOException(error); }
                ventana.dispose();
                verificar(CajaTexto.getText().equals(texto), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
