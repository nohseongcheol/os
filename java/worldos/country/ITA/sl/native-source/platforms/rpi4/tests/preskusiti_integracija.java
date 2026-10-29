// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import slovenščina.자바.*;
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

public class preskusiti_integracija {
    interface VALUE { long Branje(); }
    static class nadrejen_VALUE { protected long VALUE = 42; }
    static class otrok_VALUE extends nadrejen_VALUE implements VALUE { public long Branje() { return VALUE; } }
    private static void 확인(boolean pogoj, String Ime) {
        if (!pogoj) throw new AssertionError(Ime);
        System.out.println("PASS " + Ime);
    }
    public static void main(String[] Argumenti) throws Exception {
        String Besedilo = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "preverjanje_veljavnosti_podatki.txt");
        Datoteka.Pisanje(Store_VALUE, Besedilo);
        확인(Datoteka.Branje(Store_VALUE).equals(Besedilo), "UTF8_FILE");
        확인(문자.koda_znaka_COUNT("한😀") == 2, "UNICODE");
        확인(문자.normalizirati_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE predmet_VALUE = new otrok_VALUE();
        확인(predmet_VALUE.Branje() == 42 && (long)otrok_VALUE.class.getMethod("Branje").invoke(predmet_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        확인(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("preveriti_veljavnost"); }
        catch (IOException izjema) { 확인(izjema.getMessage().equals("preveriti_veljavnost"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread nit_VALUE = 작업.Zaženi("한글 nit_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(nit_VALUE);
        확인(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket strežnik_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> odgovor = 일꾼.submit(() -> {
                try (Socket vtičnica_VALUE = strežnik_VALUE.accept()) {
                    BufferedReader Branje = new BufferedReader(new InputStreamReader(vtičnica_VALUE.getInputStream()));
                    String Črtni;
                    while ((Črtni = Branje.readLine()) != null && !Črtni.isEmpty()) {}
                    byte[] telo_besedila = 문자.kodirati(Besedilo);
                    vtičnica_VALUE.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + telo_besedila.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    vtičnica_VALUE.getOutputStream().write(telo_besedila);
                } catch (IOException NAPAKA) { throw new UncheckedIOException(NAPAKA); }
            });
            확인(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + strežnik_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Besedilo), "HTTP_TCP");
            odgovor.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        확인(new ProcessBuilder("/bin/echo", "Proces_VALUE").start().waitFor() == 0, "PROCESS");
        if (Argumenti.length > 0 && Argumenti[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font pisava_VALUE = new Font("Dialog", Font.PLAIN, 18);
                확인(pisava_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                확인(pisava_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea vnosno_polje = new JTextArea(Besedilo);
                vnosno_polje.setFont(pisava_VALUE);
                JFrame okno = 화면.okno("그래픽 preveriti_veljavnost", vnosno_polje, 800, 240);
                BufferedImage risba_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = risba_VALUE.createGraphics();
                okno.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(risba_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException NAPAKA) { throw new UncheckedIOException(NAPAKA); }
                okno.dispose();
                확인(vnosno_polje.getText().equals(Besedilo), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
