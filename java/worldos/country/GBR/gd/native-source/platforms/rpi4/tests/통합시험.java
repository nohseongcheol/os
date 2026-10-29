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
    static class 부모 { protected long VALUE = 42; }
    static class duine_cloinne_VALUE extends 부모 implements VALUE { public long 읽기() { return VALUE; } }
    private static void dearbh(boolean cumha, String Ainm) {
        if (!cumha) throw new AssertionError(Ainm);
        System.out.println("PASS " + Ainm);
    }
    public static void main(String[] 인수) throws Exception {
        String SMS = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "dearbhadh_dàta.txt");
        faidhle.sgrìobh(Store_VALUE, SMS);
        dearbh(faidhle.읽기(Store_VALUE).equals(SMS), "UTF8_FILE");
        dearbh(문자.còd_a_charactair_COUNT("한😀") == 2, "UNICODE");
        dearbh(문자.àbhaistich_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE nì_VALUE = new duine_cloinne_VALUE();
        dearbh(nì_VALUE.읽기() == 42 && (long)duine_cloinne_VALUE.class.getMethod("읽기").invoke(nì_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        dearbh(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("dearbh_5fb2b747"); }
        catch (IOException 예외) { dearbh(예외.getMessage().equals("dearbh_5fb2b747"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread snàithlean_VALUE = 작업.ruith("한글 snàithlean_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(snàithlean_VALUE);
        dearbh(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket frithealaiche_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> freagair = 일꾼.submit(() -> {
                try (Socket 소켓 = frithealaiche_VALUE.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String loidhne;
                    while ((loidhne = 읽기.readLine()) != null && !loidhne.isEmpty()) {}
                    byte[] bodhaig_an_teacsa = 문자.부호화(SMS);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + bodhaig_an_teacsa.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(bodhaig_an_teacsa);
                } catch (IOException Mearachd) { throw new UncheckedIOException(Mearachd); }
            });
            dearbh(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + frithealaiche_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(SMS), "HTTP_TCP");
            freagair.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        dearbh(new ProcessBuilder("/bin/echo", "Pròiseas_VALUE").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font cruth_clò_VALUE = new Font("Dialog", Font.PLAIN, 18);
                dearbh(cruth_clò_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                dearbh(cruth_clò_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea bogsa_teacsa = new JTextArea(SMS);
                bogsa_teacsa.setFont(cruth_clò_VALUE);
                JFrame uinneag = 화면.uinneag("그래픽 dearbh_5fb2b747", bogsa_teacsa, 800, 240);
                BufferedImage tarraing_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = tarraing_VALUE.createGraphics();
                uinneag.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(tarraing_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Mearachd) { throw new UncheckedIOException(Mearachd); }
                uinneag.dispose();
                dearbh(bogsa_teacsa.getText().equals(SMS), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
