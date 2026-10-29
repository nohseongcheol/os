// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Latviešu.자바.*;
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
    interface VALUE { long Lasīt(); }
    static class vecākobjekts_VALUE { protected long VALUE = 42; }
    static class bērns_VALUE extends vecākobjekts_VALUE implements VALUE { public long Lasīt() { return VALUE; } }
    private static void verificēt(boolean nosacījums, String Nosaukums) {
        if (!nosacījums) throw new AssertionError(Nosaukums);
        System.out.println("PASS " + Nosaukums);
    }
    public static void main(String[] Parametri) throws Exception {
        String Teksts = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "validācija_dati.txt");
        Fails.Rakstīt(Store_VALUE, Teksts);
        verificēt(Fails.Lasīt(Store_VALUE).equals(Teksts), "UTF8_FILE");
        verificēt(문자.koda_punkts_COUNT("한😀") == 2, "UNICODE");
        verificēt(문자.normalizēt_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE objekts_VALUE = new bērns_VALUE();
        verificēt(objekts_VALUE.Lasīt() == 42 && (long)bērns_VALUE.class.getMethod("Lasīt").invoke(objekts_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        verificēt(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("validēt"); }
        catch (IOException izņēmums) { verificēt(izņēmums.getMessage().equals("validēt"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread saruna_VALUE = 작업.Palaist("한글 saruna_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(saruna_VALUE);
        verificēt(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService nodarbinātais_VALUE = Executors.newSingleThreadExecutor();
        try (ServerSocket serveris_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> atbilde = nodarbinātais_VALUE.submit(() -> {
                try (Socket 소켓 = serveris_VALUE.accept()) {
                    BufferedReader Lasīt = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Līniju;
                    while ((Līniju = Lasīt.readLine()) != null && !Līniju.isEmpty()) {}
                    byte[] pamatteksts = 문자.kodēt(Teksts);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + pamatteksts.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(pamatteksts);
                } catch (IOException Kļūda) { throw new UncheckedIOException(Kļūda); }
            });
            verificēt(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + serveris_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Teksts), "HTTP_TCP");
            atbilde.get(30, TimeUnit.SECONDS);
        } finally { nodarbinātais_VALUE.shutdownNow(); }
        verificēt(new ProcessBuilder("/bin/echo", "Process_VALUE").start().waitFor() == 0, "PROCESS");
        if (Parametri.length > 0 && Parametri[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font fonts_VALUE = new Font("Dialog", Font.PLAIN, 18);
                verificēt(fonts_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                verificēt(fonts_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea rediģēšanas_lodziņš = new JTextArea(Teksts);
                rediģēšanas_lodziņš.setFont(fonts_VALUE);
                JFrame Logs = 화면.Logs("그래픽 validēt", rediģēšanas_lodziņš, 800, 240);
                BufferedImage zīmējums_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = zīmējums_VALUE.createGraphics();
                Logs.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(zīmējums_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Kļūda) { throw new UncheckedIOException(Kļūda); }
                Logs.dispose();
                verificēt(rediģēšanas_lodziņš.getText().equals(Teksts), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
