// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import hrvatski.자바.*;
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
    interface VALUE { long Čitaj(); }
    static class roditeljski_VALUE { protected long VALUE = 42; }
    static class dijete_VALUE extends roditeljski_VALUE implements VALUE { public long Čitaj() { return VALUE; } }
    private static void provjeriti(boolean uvjet, String Ime) {
        if (!uvjet) throw new AssertionError(Ime);
        System.out.println("PASS " + Ime);
    }
    public static void main(String[] Argumenti) throws Exception {
        String Tekst = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "provjera_podaci.txt");
        Datoteka.Zapisuj(Store_VALUE, Tekst);
        provjeriti(Datoteka.Čitaj(Store_VALUE).equals(Tekst), "UTF8_FILE");
        provjeriti(문자.točka_koda_COUNT("한😀") == 2, "UNICODE");
        provjeriti(문자.normalizirati_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE objekt_VALUE = new dijete_VALUE();
        provjeriti(objekt_VALUE.Čitaj() == 42 && (long)dijete_VALUE.class.getMethod("Čitaj").invoke(objekt_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        provjeriti(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("potvrditi"); }
        catch (IOException iznimka) { provjeriti(iznimka.getMessage().equals("potvrditi"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread nit_VALUE = 작업.Pokreni("한글 nit_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(nit_VALUE);
        provjeriti(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket server_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> odgovor = 일꾼.submit(() -> {
                try (Socket 소켓 = server_VALUE.accept()) {
                    BufferedReader Čitaj = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String red;
                    while ((red = Čitaj.readLine()) != null && !red.isEmpty()) {}
                    byte[] tijelo_teksta = 문자.kodirati(Tekst);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + tijelo_teksta.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(tijelo_teksta);
                } catch (IOException GREŠKA) { throw new UncheckedIOException(GREŠKA); }
            });
            provjeriti(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + server_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Tekst), "HTTP_TCP");
            odgovor.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        provjeriti(new ProcessBuilder("/bin/echo", "Proces_VALUE").start().waitFor() == 0, "PROCESS");
        if (Argumenti.length > 0 && Argumenti[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font font_VALUE = new Font("Dialog", Font.PLAIN, 18);
                provjeriti(font_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                provjeriti(font_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea okvir_za_uređivanje = new JTextArea(Tekst);
                okvir_za_uređivanje.setFont(font_VALUE);
                JFrame Prozor = 화면.Prozor("그래픽 potvrditi", okvir_za_uređivanje, 800, 240);
                BufferedImage crtež_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = crtež_VALUE.createGraphics();
                Prozor.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(crtež_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException GREŠKA) { throw new UncheckedIOException(GREŠKA); }
                Prozor.dispose();
                provjeriti(okvir_za_uređivanje.getText().equals(Tekst), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
