// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자바.*;
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
    interface VALUE { long 읽기(); }
    static class nadređen_VALUE { protected long VALUE = 42; }
    static class dete_VALUE extends nadređen_VALUE implements VALUE { public long 읽기() { return VALUE; } }
    private static void verifikovati(boolean stanje, String ime) {
        if (!stanje) throw new AssertionError(ime);
        System.out.println("PASS " + ime);
    }
    public static void main(String[] 인수) throws Exception {
        String SMS = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "provera_valjanosti_podaci.txt");
        Datoteka.쓰기(Store_VALUE, SMS);
        verifikovati(Datoteka.읽기(Store_VALUE).equals(SMS), "UTF8_FILE");
        verifikovati(문자.kôd_znaka_COUNT("한😀") == 2, "UNICODE");
        verifikovati(문자.normalizovati_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE objekat_VALUE = new dete_VALUE();
        verifikovati(objekat_VALUE.읽기() == 42 && (long)dete_VALUE.class.getMethod("읽기").invoke(objekat_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        verifikovati(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("potvrditi"); }
        catch (IOException izuzetak) { verifikovati(izuzetak.getMessage().equals("potvrditi"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread nit_VALUE = 작업.koristiti("한글 nit_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(nit_VALUE);
        verifikovati(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket server_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> odgovor = 일꾼.submit(() -> {
                try (Socket 소켓 = server_VALUE.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String red;
                    while ((red = 읽기.readLine()) != null && !red.isEmpty()) {}
                    byte[] telo_teksta = 문자.kodirati(SMS);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + telo_teksta.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(telo_teksta);
                } catch (IOException greška) { throw new UncheckedIOException(greška); }
            });
            verifikovati(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + server_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(SMS), "HTTP_TCP");
            odgovor.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        verifikovati(new ProcessBuilder("/bin/echo", "Proces_VALUE").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font font_VALUE = new Font("Dialog", Font.PLAIN, 18);
                verifikovati(font_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                verifikovati(font_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea polje_za_uređivanje = new JTextArea(SMS);
                polje_za_uređivanje.setFont(font_VALUE);
                JFrame prozor = 화면.prozor("그래픽 potvrditi", polje_za_uređivanje, 800, 240);
                BufferedImage crtež_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = crtež_VALUE.createGraphics();
                prozor.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(crtež_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException greška) { throw new UncheckedIOException(greška); }
                prozor.dispose();
                verifikovati(polje_za_uređivanje.getText().equals(SMS), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
