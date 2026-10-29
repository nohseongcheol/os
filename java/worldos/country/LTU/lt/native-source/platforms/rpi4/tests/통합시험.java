// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Lietuvių.자바.*;
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
    interface VALUE { long Skaitymas(); }
    static class pirminis_VALUE { protected long VALUE = 42; }
    static class vaikas_VALUE extends pirminis_VALUE implements VALUE { public long Skaitymas() { return VALUE; } }
    private static void patvirtinti(boolean sąlyga, String Pavadinimas_2) {
        if (!sąlyga) throw new AssertionError(Pavadinimas_2);
        System.out.println("PASS " + Pavadinimas_2);
    }
    public static void main(String[] Argumentai) throws Exception {
        String Tekstas = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "tikrinimas_duomenys.txt");
        Failas.Rašymas(Store_VALUE, Tekstas);
        patvirtinti(Failas.Skaitymas(Store_VALUE).equals(Tekstas), "UTF8_FILE");
        patvirtinti(문자.kodo_elementas_COUNT("한😀") == 2, "UNICODE");
        patvirtinti(문자.normalizuoti_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE objektas_VALUE = new vaikas_VALUE();
        patvirtinti(objektas_VALUE.Skaitymas() == 42 && (long)vaikas_VALUE.class.getMethod("Skaitymas").invoke(objektas_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        patvirtinti(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("tikrinti"); }
        catch (IOException išimtis) { patvirtinti(išimtis.getMessage().equals("tikrinti"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread gija_VALUE = 작업.Paleisti("한글 gija_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(gija_VALUE);
        patvirtinti(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService darbininkas_VALUE = Executors.newSingleThreadExecutor();
        try (ServerSocket serveris_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> atsakyti = darbininkas_VALUE.submit(() -> {
                try (Socket 소켓 = serveris_VALUE.accept()) {
                    BufferedReader Skaitymas = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Eilutė;
                    while ((Eilutė = Skaitymas.readLine()) != null && !Eilutė.isEmpty()) {}
                    byte[] pagrindinis_tekstas = 문자.koduoti(Tekstas);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + pagrindinis_tekstas.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(pagrindinis_tekstas);
                } catch (IOException KLAIDA) { throw new UncheckedIOException(KLAIDA); }
            });
            patvirtinti(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + serveris_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Tekstas), "HTTP_TCP");
            atsakyti.get(30, TimeUnit.SECONDS);
        } finally { darbininkas_VALUE.shutdownNow(); }
        patvirtinti(new ProcessBuilder("/bin/echo", "Procesas_VALUE").start().waitFor() == 0, "PROCESS");
        if (Argumentai.length > 0 && Argumentai[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font šriftas_VALUE = new Font("Dialog", Font.PLAIN, 18);
                patvirtinti(šriftas_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                patvirtinti(šriftas_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea teksto_laukas_d6e55852 = new JTextArea(Tekstas);
                teksto_laukas_d6e55852.setFont(šriftas_VALUE);
                JFrame Langas = 화면.Langas("그래픽 tikrinti", teksto_laukas_d6e55852, 800, 240);
                BufferedImage piešinys_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = piešinys_VALUE.createGraphics();
                Langas.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(piešinys_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException KLAIDA) { throw new UncheckedIOException(KLAIDA); }
                Langas.dispose();
                patvirtinti(teksto_laukas_d6e55852.getText().equals(Tekstas), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
