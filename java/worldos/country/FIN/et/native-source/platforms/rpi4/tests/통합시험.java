// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Eesti.자바.*;
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
    interface VALUE { long Lugemine(); }
    static class ema_VALUE { protected long VALUE = 42; }
    static class laps_VALUE extends ema_VALUE implements VALUE { public long Lugemine() { return VALUE; } }
    private static void kinnitama(boolean tingimus, String Nimi_2) {
        if (!tingimus) throw new AssertionError(Nimi_2);
        System.out.println("PASS " + Nimi_2);
    }
    public static void main(String[] Argumendid) throws Exception {
        String Tekst = "한글 日本語 العربية हिन्दी 😀";
        Path salv_VALUE = Path.of(System.getProperty("user.home"), "kinnitamine_andmed.txt");
        Fail.Kirjutamine(salv_VALUE, Tekst);
        kinnitama(Fail.Lugemine(salv_VALUE).equals(Tekst), "UTF8_FILE");
        kinnitama(문자.koodipunkt_COUNT("한😀") == 2, "UNICODE");
        kinnitama(문자.normaliseerima_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE objekt_VALUE = new laps_VALUE();
        kinnitama(objekt_VALUE.Lugemine() == 42 && (long)laps_VALUE.class.getMethod("Lugemine").invoke(objekt_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        kinnitama(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("valideerima"); }
        catch (IOException erand) { kinnitama(erand.getMessage().equals("valideerima"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread lõim_VALUE = 작업.Käivita_2("한글 lõim_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(lõim_VALUE);
        kinnitama(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService töötaja_VALUE = Executors.newSingleThreadExecutor();
        try (ServerSocket server_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> vastus = töötaja_VALUE.submit(() -> {
                try (Socket 소켓 = server_VALUE.accept()) {
                    BufferedReader Lugemine = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Joon;
                    while ((Joon = Lugemine.readLine()) != null && !Joon.isEmpty()) {}
                    byte[] sisu_SMS = 문자.kodeerima(Tekst);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + sisu_SMS.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(sisu_SMS);
                } catch (IOException VIGA) { throw new UncheckedIOException(VIGA); }
            });
            kinnitama(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + server_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Tekst), "HTTP_TCP");
            vastus.get(30, TimeUnit.SECONDS);
        } finally { töötaja_VALUE.shutdownNow(); }
        kinnitama(new ProcessBuilder("/bin/echo", "Joonis_VALUE").start().waitFor() == 0, "PROCESS");
        if (Argumendid.length > 0 && Argumendid[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font font_VALUE = new Font("Dialog", Font.PLAIN, 18);
                kinnitama(font_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                kinnitama(font_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea tekstiala = new JTextArea(Tekst);
                tekstiala.setFont(font_VALUE);
                JFrame aken = 화면.aken("그래픽 valideerima", tekstiala, 800, 240);
                BufferedImage joonis_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = joonis_VALUE.createGraphics();
                aken.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(joonis_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException VIGA) { throw new UncheckedIOException(VIGA); }
                aken.dispose();
                kinnitama(tekstiala.getText().equals(Tekst), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
