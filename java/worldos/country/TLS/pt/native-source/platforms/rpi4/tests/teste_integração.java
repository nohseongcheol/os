// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Português.자바.*;
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

public class teste_integração {
    interface VALOR { long Leitura(); }
    static class pai_VALOR { protected long VALOR = 42; }
    static class filho_VALOR extends pai_VALOR implements VALOR { public long Leitura() { return VALOR; } }
    private static void verificar(boolean doença, String Nome) {
        if (!doença) throw new AssertionError(Nome);
        System.out.println("PASS " + Nome);
    }
    public static void main(String[] argumentos) throws Exception {
        String texto = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALOR = Path.of(System.getProperty("user.home"), "validação_dados.txt");
        ficheiro.Escrita(Store_VALOR, texto);
        verificar(ficheiro.Leitura(Store_VALOR).equals(texto), "UTF8_FILE");
        verificar(문자.ponto_de_código_CONT_NÚM("한😀") == 2, "UNICODE");
        verificar(문자.normalizar_VALOR("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALOR objeto_VALOR = new filho_VALOR();
        verificar(objeto_VALOR.Leitura() == 42 && (long)filho_VALOR.class.getMethod("Leitura").invoke(objeto_VALOR) == 42, "OBJECT_INHERITANCE_REFLECTION");
        verificar(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("validar"); }
        catch (IOException exceção) { verificar(exceção.getMessage().equals("validar"), "EXCEPTION"); }
        AtomicInteger SUM_VALOR = new AtomicInteger();
        Thread thread_VALOR = 작업.iniciar("한글 thread_VALOR", () -> SUM_VALOR.set(123));
        작업.기다리기(thread_VALOR);
        verificar(SUM_VALOR.get() == 123, "THREAD");
        ExecutorService trabalho_VALOR = Executors.newSingleThreadExecutor();
        try (ServerSocket servidor_VALOR = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> resposta = trabalho_VALOR.submit(() -> {
                try (Socket soquete_VALOR = servidor_VALOR.accept()) {
                    BufferedReader Leitura = new BufferedReader(new InputStreamReader(soquete_VALOR.getInputStream()));
                    String linha_de_entrada;
                    while ((linha_de_entrada = Leitura.readLine()) != null && !linha_de_entrada.isEmpty()) {}
                    byte[] corpo_de_texto = 문자.codificar(texto);
                    soquete_VALOR.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + corpo_de_texto.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    soquete_VALOR.getOutputStream().write(corpo_de_texto);
                } catch (IOException erro) { throw new UncheckedIOException(erro); }
            });
            verificar(comunicação.PEGAR_VALOR(URI.create("http://127.0.0.1:" + servidor_VALOR.getLocalPort()), Duration.ofSeconds(30)).body().equals(texto), "HTTP_TCP");
            resposta.get(30, TimeUnit.SECONDS);
        } finally { trabalho_VALOR.shutdownNow(); }
        verificar(new ProcessBuilder("/bin/echo", "Processo_VALOR").start().waitFor() == 0, "PROCESS");
        if (argumentos.length > 0 && argumentos[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font fonte_VALOR = new Font("Dialog", Font.PLAIN, 18);
                verificar(fonte_VALOR.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                verificar(fonte_VALOR.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea área_de_texto = new JTextArea(texto);
                área_de_texto.setFont(fonte_VALOR);
                JFrame Janela = tela.Janela("그래픽 validar", área_de_texto, 800, 240);
                BufferedImage desenho_VALOR = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D pincel_VALOR = desenho_VALOR.createGraphics();
                Janela.paint(pincel_VALOR); pincel_VALOR.dispose();
                try { javax.imageio.ImageIO.write(desenho_VALOR, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException erro) { throw new UncheckedIOException(erro); }
                Janela.dispose();
                verificar(área_de_texto.getText().equals(texto), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
