// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Galego.자바.*;
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

public class 통합시험 {
    interface VALOR { long Lectura(); }
    static class 부모 { protected long VALOR = 42; }
    static class neno_VALOR extends 부모 implements VALOR { public long Lectura() { return VALOR; } }
    private static void verificar(boolean condición, String Nome) {
        if (!condición) throw new AssertionError(Nome);
        System.out.println("PASS " + Nome);
    }
    public static void main(String[] Argumentos) throws Exception {
        String Texto = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALOR = Path.of(System.getProperty("user.home"), "validación_datos.txt");
        Ficheiro.Escritura(Store_VALOR, Texto);
        verificar(Ficheiro.Lectura(Store_VALOR).equals(Texto), "UTF8_FILE");
        verificar(문자.código_de_carácter_CONTAR("한😀") == 2, "UNICODE");
        verificar(문자.organizar_VALOR("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALOR obxecto_VALOR = new neno_VALOR();
        verificar(obxecto_VALOR.Lectura() == 42 && (long)neno_VALOR.class.getMethod("Lectura").invoke(obxecto_VALOR) == 42, "OBJECT_INHERITANCE_REFLECTION");
        verificar(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("validar"); }
        catch (IOException excepción) { verificar(excepción.getMessage().equals("validar"), "EXCEPTION"); }
        AtomicInteger SUMA_VALOR = new AtomicInteger();
        Thread tema_VALOR = 작업.Executar_2("한글 tema_VALOR", () -> SUMA_VALOR.set(123));
        작업.기다리기(tema_VALOR);
        verificar(SUMA_VALOR.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket servidor_VALOR = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> resposta = 일꾼.submit(() -> {
                try (Socket 소켓 = servidor_VALOR.accept()) {
                    BufferedReader Lectura = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Liña;
                    while ((Liña = Lectura.readLine()) != null && !Liña.isEmpty()) {}
                    byte[] corpo_do_texto = 문자.부호화(Texto);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + corpo_do_texto.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(corpo_do_texto);
                } catch (IOException ERRO) { throw new UncheckedIOException(ERRO); }
            });
            verificar(통신.COLLER_VALOR(URI.create("http://127.0.0.1:" + servidor_VALOR.getLocalPort()), Duration.ofSeconds(30)).body().equals(Texto), "HTTP_TCP");
            resposta.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        verificar(new ProcessBuilder("/bin/echo", "Proceso_VALOR").start().waitFor() == 0, "PROCESS");
        if (Argumentos.length > 0 && Argumentos[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font tipo_de_letra_VALOR = new Font("Dialog", Font.PLAIN, 18);
                verificar(tipo_de_letra_VALOR.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                verificar(tipo_de_letra_VALOR.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea área_de_entrada_de_texto = new JTextArea(Texto);
                área_de_entrada_de_texto.setFont(tipo_de_letra_VALOR);
                JFrame Xanela = 화면.Xanela("그래픽 validar", área_de_entrada_de_texto, 800, 240);
                BufferedImage 그림 = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = 그림.createGraphics();
                Xanela.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(그림, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ERRO) { throw new UncheckedIOException(ERRO); }
                Xanela.dispose();
                verificar(área_de_entrada_de_texto.getText().equals(Texto), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
