// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Català.자바.*;
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
    static class nen_VALOR extends 부모 implements VALOR { public long Lectura() { return VALOR; } }
    private static void verificar(boolean condició, String Nom) {
        if (!condició) throw new AssertionError(Nom);
        System.out.println("PASS " + Nom);
    }
    public static void main(String[] 인수) throws Exception {
        String SMS = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALOR = Path.of(System.getProperty("user.home"), "validació_dades.txt");
        Fitxer.Escriptura(Store_VALOR, SMS);
        verificar(Fitxer.Lectura(Store_VALOR).equals(SMS), "UTF8_FILE");
        verificar(문자.codi_de_caràcter_COMPT("한😀") == 2, "UNICODE");
        verificar(문자.normalitzar_VALOR("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALOR objecte_VALOR = new nen_VALOR();
        verificar(objecte_VALOR.Lectura() == 42 && (long)nen_VALOR.class.getMethod("Lectura").invoke(objecte_VALOR) == 42, "OBJECT_INHERITANCE_REFLECTION");
        verificar(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("validar"); }
        catch (IOException excepció) { verificar(excepció.getMessage().equals("validar"), "EXCEPTION"); }
        AtomicInteger SUMA_VALOR = new AtomicInteger();
        Thread fil_VALOR = 작업.Executa_2("한글 fil_VALOR", () -> SUMA_VALOR.set(123));
        작업.기다리기(fil_VALOR);
        verificar(SUMA_VALOR.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket servidor_VALOR = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> resposta = 일꾼.submit(() -> {
                try (Socket 소켓 = servidor_VALOR.accept()) {
                    BufferedReader Lectura = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String línia;
                    while ((línia = Lectura.readLine()) != null && !línia.isEmpty()) {}
                    byte[] text_del_cos = 문자.부호화(SMS);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + text_del_cos.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(text_del_cos);
                } catch (IOException s_ha_produït_un_error) { throw new UncheckedIOException(s_ha_produït_un_error); }
            });
            verificar(통신.PREN_VALOR(URI.create("http://127.0.0.1:" + servidor_VALOR.getLocalPort()), Duration.ofSeconds(30)).body().equals(SMS), "HTTP_TCP");
            resposta.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        verificar(new ProcessBuilder("/bin/echo", "Procés_VALOR").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font tipus_de_lletra_VALOR = new Font("Dialog", Font.PLAIN, 18);
                verificar(tipus_de_lletra_VALOR.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                verificar(tipus_de_lletra_VALOR.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea àrea_d_entrada_de_text = new JTextArea(SMS);
                àrea_d_entrada_de_text.setFont(tipus_de_lletra_VALOR);
                JFrame Finestra = 화면.Finestra("그래픽 validar", àrea_d_entrada_de_text, 800, 240);
                BufferedImage dibuix_VALOR = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = dibuix_VALOR.createGraphics();
                Finestra.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(dibuix_VALOR, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException s_ha_produït_un_error) { throw new UncheckedIOException(s_ha_produït_un_error); }
                Finestra.dispose();
                verificar(àrea_d_entrada_de_text.getText().equals(SMS), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
