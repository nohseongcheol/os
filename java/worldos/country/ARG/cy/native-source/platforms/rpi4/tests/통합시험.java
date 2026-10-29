// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Cymraeg.자바.*;
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
    interface VALUE { long Darllen(); }
    static class 부모 { protected long VALUE = 42; }
    static class iselfen_VALUE extends 부모 implements VALUE { public long Darllen() { return VALUE; } }
    private static void dilysu(boolean cyflwr, String Enw) {
        if (!cyflwr) throw new AssertionError(Enw);
        System.out.println("PASS " + Enw);
    }
    public static void main(String[] 인수) throws Exception {
        String Testun = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "dilysu_data.txt");
        Ffeil.Ysgrifennu(Store_VALUE, Testun);
        dilysu(Ffeil.Darllen(Store_VALUE).equals(Testun), "UTF8_FILE");
        dilysu(문자.cod_nod_COUNT("한😀") == 2, "UNICODE");
        dilysu(문자.normaleiddio_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE gwrthrych_VALUE = new iselfen_VALUE();
        dilysu(gwrthrych_VALUE.Darllen() == 42 && (long)iselfen_VALUE.class.getMethod("Darllen").invoke(gwrthrych_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        dilysu(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("dilysu_5fb2b747"); }
        catch (IOException eithriad) { dilysu(eithriad.getMessage().equals("dilysu_5fb2b747"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread edefyn_VALUE = 작업.Gweithredu_2("한글 edefyn_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(edefyn_VALUE);
        dilysu(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket gweinydd_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> ateb = 일꾼.submit(() -> {
                try (Socket 소켓 = gweinydd_VALUE.accept()) {
                    BufferedReader Darllen = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String llinell;
                    while ((llinell = Darllen.readLine()) != null && !llinell.isEmpty()) {}
                    byte[] corff_y_testun = 문자.부호화(Testun);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + corff_y_testun.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(corff_y_testun);
                } catch (IOException Gwall) { throw new UncheckedIOException(Gwall); }
            });
            dilysu(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + gweinydd_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Testun), "HTTP_TCP");
            ateb.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        dilysu(new ProcessBuilder("/bin/echo", "Proses_VALUE").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ffont_VALUE = new Font("Dialog", Font.PLAIN, 18);
                dilysu(ffont_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                dilysu(ffont_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea ardal_testun = new JTextArea(Testun);
                ardal_testun.setFont(ffont_VALUE);
                JFrame ffenestr = 화면.ffenestr("그래픽 dilysu_5fb2b747", ardal_testun, 800, 240);
                BufferedImage lluniad_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = lluniad_VALUE.createGraphics();
                ffenestr.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(lluniad_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Gwall) { throw new UncheckedIOException(Gwall); }
                ffenestr.dispose();
                dilysu(ardal_testun.getText().equals(Testun), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
