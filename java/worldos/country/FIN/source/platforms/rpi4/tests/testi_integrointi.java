// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import suomi.자바.*;
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

public class testi_integrointi {
    interface ARVO { long Luku(); }
    static class pää_ARVO { protected long ARVO = 42; }
    static class ali_ARVO extends pää_ARVO implements ARVO { public long Luku() { return ARVO; } }
    private static void tarkistaa(boolean ehto, String Nimi) {
        if (!ehto) throw new AssertionError(Nimi);
        System.out.println("PASS " + Nimi);
    }
    public static void main(String[] argumentit) throws Exception {
        String teksti = "한글 日本語 العربية हिन्दी 😀";
        Path Store_ARVO = Path.of(System.getProperty("user.home"), "vahvistus_data.txt");
        tiedoston_nimi.Kirjoitus(Store_ARVO, teksti);
        tarkistaa(tiedoston_nimi.Luku(Store_ARVO).equals(teksti), "UTF8_FILE");
        tarkistaa(문자.koodipiste_LASKE("한😀") == 2, "UNICODE");
        tarkistaa(문자.normalisoida_ARVO("\u1100\u1161").equals("가"), "NORMALIZATION");
        ARVO objekti_ARVO = new ali_ARVO();
        tarkistaa(objekti_ARVO.Luku() == 42 && (long)ali_ARVO.class.getMethod("Luku").invoke(objekti_ARVO) == 42, "OBJECT_INHERITANCE_REFLECTION");
        tarkistaa(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("vahvista"); }
        catch (IOException poikkeus) { tarkistaa(poikkeus.getMessage().equals("vahvista"), "EXCEPTION"); }
        AtomicInteger SUM_ARVO = new AtomicInteger();
        Thread säie_ARVO = 작업.Suorita_2("한글 säie_ARVO", () -> SUM_ARVO.set(123));
        작업.기다리기(säie_ARVO);
        tarkistaa(SUM_ARVO.get() == 123, "THREAD");
        ExecutorService työntekijä_ARVO = Executors.newSingleThreadExecutor();
        try (ServerSocket palvelin_ARVO = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> palaute = työntekijä_ARVO.submit(() -> {
                try (Socket vastake_ARVO = palvelin_ARVO.accept()) {
                    BufferedReader Luku = new BufferedReader(new InputStreamReader(vastake_ARVO.getInputStream()));
                    String syöterivi;
                    while ((syöterivi = Luku.readLine()) != null && !syöterivi.isEmpty()) {}
                    byte[] leipäteksti = 문자.koodata(teksti);
                    vastake_ARVO.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + leipäteksti.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    vastake_ARVO.getOutputStream().write(leipäteksti);
                } catch (IOException VIRHE) { throw new UncheckedIOException(VIRHE); }
            });
            tarkistaa(통신.OTA_ARVO(URI.create("http://127.0.0.1:" + palvelin_ARVO.getLocalPort()), Duration.ofSeconds(30)).body().equals(teksti), "HTTP_TCP");
            palaute.get(30, TimeUnit.SECONDS);
        } finally { työntekijä_ARVO.shutdownNow(); }
        tarkistaa(new ProcessBuilder("/bin/echo", "prosessi_ARVO").start().waitFor() == 0, "PROCESS");
        if (argumentit.length > 0 && argumentit[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font fontti_ARVO = new Font("Dialog", Font.PLAIN, 18);
                tarkistaa(fontti_ARVO.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                tarkistaa(fontti_ARVO.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea tekstiruutu = new JTextArea(teksti);
                tekstiruutu.setFont(fontti_ARVO);
                JFrame Ikkuna = 화면.Ikkuna("그래픽 vahvista", tekstiruutu, 800, 240);
                BufferedImage piirustus_ARVO = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D sivellin_ARVO = piirustus_ARVO.createGraphics();
                Ikkuna.paint(sivellin_ARVO); sivellin_ARVO.dispose();
                try { javax.imageio.ImageIO.write(piirustus_ARVO, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException VIRHE) { throw new UncheckedIOException(VIRHE); }
                Ikkuna.dispose();
                tarkistaa(tekstiruutu.getText().equals(teksti), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
