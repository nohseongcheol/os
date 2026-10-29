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
    interface අගය { long කියවීම(); }
    static class 부모 { protected long අගය = 42; }
    static class දරුවා_අගය extends 부모 implements අගය { public long කියවීම() { return අගය; } }
    private static void තහවුරු_කරන්න(boolean තත්වය, String නම) {
        if (!තත්වය) throw new AssertionError(නම);
        System.out.println("PASS " + නම);
    }
    public static void main(String[] විස්තාරක) throws Exception {
        String පෙළ = "한글 日本語 العربية हिन्दी 😀";
        Path ගබඩා_කරන්න_අගය = Path.of(System.getProperty("user.home"), "වලංගුකරණය_දත්ත.txt");
        ගොනු.ලිවීම(ගබඩා_කරන්න_අගය, පෙළ);
        තහවුරු_කරන්න(ගොනු.කියවීම(ගබඩා_කරන්න_අගය).equals(පෙළ), "UTF8_FILE");
        තහවුරු_කරන්න(문자.코드포인트수("한😀") == 2, "UNICODE");
        තහවුරු_කරන්න(문자.ප්_රමත_කරන්න_අගය("\u1100\u1161").equals("가"), "NORMALIZATION");
        අගය වස්තුව_අගය = new දරුවා_අගය();
        තහවුරු_කරන්න(වස්තුව_අගය.කියවීම() == 42 && (long)දරුවා_අගය.class.getMethod("කියවීම").invoke(වස්තුව_අගය) == 42, "OBJECT_INHERITANCE_REFLECTION");
        තහවුරු_කරන්න(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("වලංගු_කරන්න"); }
        catch (IOException 예외) { තහවුරු_කරන්න(예외.getMessage().equals("වලංගු_කරන්න"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread පොට_අගය = 작업.ක්_රියාත්මක_කරන්න_2("한글 පොට_අගය", () -> 합.set(123));
        작업.기다리기(පොට_අගය);
        තහවුරු_කරන්න(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket සේවාදායකය_අගය = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> පිළිතුරු_දෙන්න = 일꾼.submit(() -> {
                try (Socket 소켓 = සේවාදායකය_අගය.accept()) {
                    BufferedReader කියවීම = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String පේළිය;
                    while ((පේළිය = කියවීම.readLine()) != null && !පේළිය.isEmpty()) {}
                    byte[] කඳ_පෙළ = 문자.부호화(පෙළ);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + කඳ_පෙළ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(කඳ_පෙළ);
                } catch (IOException දෝෂය) { throw new UncheckedIOException(දෝෂය); }
            });
            තහවුරු_කරන්න(통신.가져오기(URI.create("http://127.0.0.1:" + සේවාදායකය_අගය.getLocalPort()), Duration.ofSeconds(30)).body().equals(පෙළ), "HTTP_TCP");
            පිළිතුරු_දෙන්න.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        තහවුරු_කරන්න(new ProcessBuilder("/bin/echo", "ක්_රියාවලිය_අගය").start().waitFor() == 0, "PROCESS");
        if (විස්තාරක.length > 0 && විස්තාරක[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ෆොන්ටය_අගය = new Font("Dialog", Font.PLAIN, 18);
                තහවුරු_කරන්න(ෆොන්ටය_අගය.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                තහවුරු_කරන්න(ෆොන්ටය_අගය.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea පෙළ_කොටුව = new JTextArea(පෙළ);
                පෙළ_කොටුව.setFont(ෆොන්ටය_අගය);
                JFrame කවුළුව = 화면.කවුළුව("그래픽 වලංගු_කරන්න", පෙළ_කොටුව, 800, 240);
                BufferedImage චිත්_රය_අගය = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = චිත්_රය_අගය.createGraphics();
                කවුළුව.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(චිත්_රය_අගය, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException දෝෂය) { throw new UncheckedIOException(දෝෂය); }
                කවුළුව.dispose();
                තහවුරු_කරන්න(පෙළ_කොටුව.getText().equals(පෙළ), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
