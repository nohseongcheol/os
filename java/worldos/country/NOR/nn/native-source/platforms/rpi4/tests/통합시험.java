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
    interface VALUE { long Les(); }
    static class forelder_VALUE { protected long VALUE = 42; }
    static class underordna_VALUE extends forelder_VALUE implements VALUE { public long Les() { return VALUE; } }
    private static void stadfeste(boolean tilstand, String Namn) {
        if (!tilstand) throw new AssertionError(Namn);
        System.out.println("PASS " + Namn);
    }
    public static void main(String[] Argument) throws Exception {
        String Tekst = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "validering_data.txt");
        Fil.Skriv(Store_VALUE, Tekst);
        stadfeste(Fil.Les(Store_VALUE).equals(Tekst), "UTF8_FILE");
        stadfeste(문자.teiknkode_COUNT("한😀") == 2, "UNICODE");
        stadfeste(문자.normalisere_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE objekt_VALUE = new underordna_VALUE();
        stadfeste(objekt_VALUE.Les() == 42 && (long)underordna_VALUE.class.getMethod("Les").invoke(objekt_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        stadfeste(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("bekrefte"); }
        catch (IOException unntak) { stadfeste(unntak.getMessage().equals("bekrefte"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread tråd_VALUE = 작업.Køyr_2("한글 tråd_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(tråd_VALUE);
        stadfeste(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket tenar_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> svare = 일꾼.submit(() -> {
                try (Socket 소켓 = tenar_VALUE.accept()) {
                    BufferedReader Les = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String linje;
                    while ((linje = Les.readLine()) != null && !linje.isEmpty()) {}
                    byte[] brødtekst = 문자.부호화(Tekst);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + brødtekst.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(brødtekst);
                } catch (IOException FEIL) { throw new UncheckedIOException(FEIL); }
            });
            stadfeste(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + tenar_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Tekst), "HTTP_TCP");
            svare.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        stadfeste(new ProcessBuilder("/bin/echo", "Prosess_VALUE").start().waitFor() == 0, "PROCESS");
        if (Argument.length > 0 && Argument[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font skrift_VALUE = new Font("Dialog", Font.PLAIN, 18);
                stadfeste(skrift_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                stadfeste(skrift_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea tekstboks = new JTextArea(Tekst);
                tekstboks.setFont(skrift_VALUE);
                JFrame vindauge = 화면.vindauge("그래픽 bekrefte", tekstboks, 800, 240);
                BufferedImage teikning_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = teikning_VALUE.createGraphics();
                vindauge.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(teikning_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException FEIL) { throw new UncheckedIOException(FEIL); }
                vindauge.dispose();
                stadfeste(tekstboks.getText().equals(Tekst), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
