// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Română.자바.*;
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
    interface VALUE { long Citire(); }
    static class părinte_VALUE { protected long VALUE = 42; }
    static class copil_VALUE extends părinte_VALUE implements VALUE { public long Citire() { return VALUE; } }
    private static void verifica(boolean condiție, String Nume) {
        if (!condiție) throw new AssertionError(Nume);
        System.out.println("PASS " + Nume);
    }
    public static void main(String[] Argumente) throws Exception {
        String SMS = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "validare_date.txt");
        Fișier.Scriere(Store_VALUE, SMS);
        verifica(Fișier.Citire(Store_VALUE).equals(SMS), "UTF8_FILE");
        verifica(문자.cod_caracter_COUNT("한😀") == 2, "UNICODE");
        verifica(문자.normaliza_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE obiect_VALUE = new copil_VALUE();
        verifica(obiect_VALUE.Citire() == 42 && (long)copil_VALUE.class.getMethod("Citire").invoke(obiect_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        verifica(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("valida"); }
        catch (IOException excepție) { verifica(excepție.getMessage().equals("valida"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread fir_VALUE = 작업.Pornește("한글 fir_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(fir_VALUE);
        verifica(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket server_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> replică = 일꾼.submit(() -> {
                try (Socket 소켓 = server_VALUE.accept()) {
                    BufferedReader Citire = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Linie;
                    while ((Linie = Citire.readLine()) != null && !Linie.isEmpty()) {}
                    byte[] text_corp = 문자.codifica(SMS);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + text_corp.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(text_corp);
                } catch (IOException eroare) { throw new UncheckedIOException(eroare); }
            });
            verifica(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + server_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(SMS), "HTTP_TCP");
            replică.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        verifica(new ProcessBuilder("/bin/echo", "Proces_VALUE").start().waitFor() == 0, "PROCESS");
        if (Argumente.length > 0 && Argumente[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font font_VALUE = new Font("Dialog", Font.PLAIN, 18);
                verifica(font_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                verifica(font_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea casetă_de_editare = new JTextArea(SMS);
                casetă_de_editare.setFont(font_VALUE);
                JFrame Fereastră = 화면.Fereastră("그래픽 valida", casetă_de_editare, 800, 240);
                BufferedImage desen_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = desen_VALUE.createGraphics();
                Fereastră.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(desen_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException eroare) { throw new UncheckedIOException(eroare); }
                Fereastră.dispose();
                verifica(casetă_de_editare.getText().equals(SMS), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
