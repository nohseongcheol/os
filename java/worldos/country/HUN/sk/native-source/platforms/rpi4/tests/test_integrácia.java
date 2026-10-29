// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Slovenský.자바.*;
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

public class test_integrácia {
    interface VALUE { long Čítanie(); }
    static class nadradený_VALUE { protected long VALUE = 42; }
    static class dieťa_VALUE extends nadradený_VALUE implements VALUE { public long Čítanie() { return VALUE; } }
    private static void overiť(boolean podmienka, String Názov) {
        if (!podmienka) throw new AssertionError(Názov);
        System.out.println("PASS " + Názov);
    }
    public static void main(String[] Argumenty) throws Exception {
        String Spracovanie_textu = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "overenie_údaje.txt");
        Súbor.Zápis(Store_VALUE, Spracovanie_textu);
        overiť(Súbor.Čítanie(Store_VALUE).equals(Spracovanie_textu), "UTF8_FILE");
        overiť(문자.bod_kódu_COUNT("한😀") == 2, "UNICODE");
        overiť(문자.normalizovať_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE objekt_VALUE = new dieťa_VALUE();
        overiť(objekt_VALUE.Čítanie() == 42 && (long)dieťa_VALUE.class.getMethod("Čítanie").invoke(objekt_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        overiť(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("overiť_5fb2b747"); }
        catch (IOException výnimka) { overiť(výnimka.getMessage().equals("overiť_5fb2b747"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread vlákno_VALUE = 작업.Spustiť_2("한글 vlákno_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(vlákno_VALUE);
        overiť(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket server_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> odozva = 일꾼.submit(() -> {
                try (Socket soket_VALUE = server_VALUE.accept()) {
                    BufferedReader Čítanie = new BufferedReader(new InputStreamReader(soket_VALUE.getInputStream()));
                    String riadok;
                    while ((riadok = Čítanie.readLine()) != null && !riadok.isEmpty()) {}
                    byte[] základný_text = 문자.kódovať(Spracovanie_textu);
                    soket_VALUE.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + základný_text.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    soket_VALUE.getOutputStream().write(základný_text);
                } catch (IOException chyba) { throw new UncheckedIOException(chyba); }
            });
            overiť(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + server_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Spracovanie_textu), "HTTP_TCP");
            odozva.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        overiť(new ProcessBuilder("/bin/echo", "Proces_VALUE").start().waitFor() == 0, "PROCESS");
        if (Argumenty.length > 0 && Argumenty[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font písmo_VALUE = new Font("Dialog", Font.PLAIN, 18);
                overiť(písmo_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                overiť(písmo_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea textové_pole_d6e55852 = new JTextArea(Spracovanie_textu);
                textové_pole_d6e55852.setFont(písmo_VALUE);
                JFrame Okno = 화면.Okno("그래픽 overiť_5fb2b747", textové_pole_d6e55852, 800, 240);
                BufferedImage kresba_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = kresba_VALUE.createGraphics();
                Okno.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(kresba_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException chyba) { throw new UncheckedIOException(chyba); }
                Okno.dispose();
                overiť(textové_pole_d6e55852.getText().equals(Spracovanie_textu), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
