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
    interface قىممىتى { long ئوقۇ(); }
    static class 부모 { protected long قىممىتى = 42; }
    static class بالا_قىممىتى extends 부모 implements قىممىتى { public long ئوقۇ() { return قىممىتى; } }
    private static void دەلىللىمەك(boolean شەرت, String ئاتى) {
        if (!شەرت) throw new AssertionError(ئاتى);
        System.out.println("PASS " + ئاتى);
    }
    public static void main(String[] ئۆزگەرگۈچىلەر) throws Exception {
        String تېكىست = "한글 日本語 العربية हिन्दी 😀";
        Path ساقلىماق_قىممىتى = Path.of(System.getProperty("user.home"), "دەلىللەش_مەلۇمات.txt");
        ھۆججەت.ياز(ساقلىماق_قىممىتى, تېكىست);
        دەلىللىمەك(ھۆججەت.ئوقۇ(ساقلىماق_قىممىتى).equals(تېكىست), "UTF8_FILE");
        دەلىللىمەك(문자.코드포인트수("한😀") == 2, "UNICODE");
        دەلىللىمەك(문자.نورماللاشتۇرماق_قىممىتى("\u1100\u1161").equals("가"), "NORMALIZATION");
        قىممىتى ئوبيېكت_قىممىتى = new بالا_قىممىتى();
        دەلىللىمەك(ئوبيېكت_قىممىتى.ئوقۇ() == 42 && (long)بالا_قىممىتى.class.getMethod("ئوقۇ").invoke(ئوبيېكت_قىممىتى) == 42, "OBJECT_INHERITANCE_REFLECTION");
        دەلىللىمەك(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("دەلىللەش"); }
        catch (IOException 예외) { دەلىللىمەك(예외.getMessage().equals("دەلىللەش"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread ئېقىم_قىممىتى_5b72a632 = 작업.ئىجرا_قىل_2("한글 ئېقىم_قىممىتى_5b72a632", () -> 합.set(123));
        작업.기다리기(ئېقىم_قىممىتى_5b72a632);
        دەلىللىمەك(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket مۇلازىمىتېر_قىممىتى = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> جاۋابلاش = 일꾼.submit(() -> {
                try (Socket 소켓 = مۇلازىمىتېر_قىممىتى.accept()) {
                    BufferedReader ئوقۇ = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String قۇر;
                    while ((قۇر = ئوقۇ.readLine()) != null && !قۇر.isEmpty()) {}
                    byte[] مەزمۇن = 문자.부호화(تېكىست);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + مەزمۇن.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(مەزمۇن);
                } catch (IOException خاتالىق) { throw new UncheckedIOException(خاتالىق); }
            });
            دەلىللىمەك(통신.가져오기(URI.create("http://127.0.0.1:" + مۇلازىمىتېر_قىممىتى.getLocalPort()), Duration.ofSeconds(30)).body().equals(تېكىست), "HTTP_TCP");
            جاۋابلاش.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        دەلىللىمەك(new ProcessBuilder("/bin/echo", "جەريان_قىممىتى").start().waitFor() == 0, "PROCESS");
        if (ئۆزگەرگۈچىلەر.length > 0 && ئۆزگەرگۈچىلەر[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font خەت_نۇسخا_قىممىتى = new Font("Dialog", Font.PLAIN, 18);
                دەلىللىمەك(خەت_نۇسخا_قىممىتى.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                دەلىللىمەك(خەت_نۇسخا_قىممىتى.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea تېكست_رايونى = new JTextArea(تېكىست);
                تېكست_رايونى.setFont(خەت_نۇسخا_قىممىتى);
                JFrame كۆزنەك = 화면.كۆزنەك("그래픽 دەلىللەش", تېكست_رايونى, 800, 240);
                BufferedImage سىزىش_قىممىتى = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = سىزىش_قىممىتى.createGraphics();
                كۆزنەك.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(سىزىش_قىممىتى, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException خاتالىق) { throw new UncheckedIOException(خاتالىق); }
                كۆزنەك.dispose();
                دەلىللىمەك(تېكست_رايونى.getText().equals(تېكىست), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
