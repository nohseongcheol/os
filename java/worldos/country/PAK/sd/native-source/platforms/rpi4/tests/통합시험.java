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
    interface قدر { long 읽기(); }
    static class 부모 { protected long قدر = 42; }
    static class ٻار_قدر extends 부모 implements قدر { public long 읽기() { return قدر; } }
    private static void تصديق_ڪريو(boolean حالت, String نالو) {
        if (!حالت) throw new AssertionError(نالو);
        System.out.println("PASS " + نالو);
    }
    public static void main(String[] 인수) throws Exception {
        String متن = "한글 日本語 العربية हिन्दी 😀";
        Path روڪيو_قدر = Path.of(System.getProperty("user.home"), "ڪارگر_ڪوائف.txt");
        فائل.لکو(روڪيو_قدر, متن);
        تصديق_ڪريو(فائل.읽기(روڪيو_قدر).equals(متن), "UTF8_FILE");
        تصديق_ڪريو(문자.코드포인트수("한😀") == 2, "UNICODE");
        تصديق_ڪريو(문자.عام_ڪرڻ_قدر("\u1100\u1161").equals("가"), "NORMALIZATION");
        قدر عنصر_قدر_2ed200e9 = new ٻار_قدر();
        تصديق_ڪريو(عنصر_قدر_2ed200e9.읽기() == 42 && (long)ٻار_قدر.class.getMethod("읽기").invoke(عنصر_قدر_2ed200e9) == 42, "OBJECT_INHERITANCE_REFLECTION");
        تصديق_ڪريو(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("ڪارگر_ڪريو"); }
        catch (IOException 예외) { تصديق_ڪريو(예외.getMessage().equals("ڪارگر_ڪريو"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread لڙي_قدر = 작업.هلائڻ("한글 لڙي_قدر", () -> 합.set(123));
        작업.기다리기(لڙي_قدر);
        تصديق_ڪريو(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket سرور_قدر = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> جواب_ڏيو = 일꾼.submit(() -> {
                try (Socket 소켓 = سرور_قدر.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String لڪير;
                    while ((لڪير = 읽기.readLine()) != null && !لڪير.isEmpty()) {}
                    byte[] باڊي_متن = 문자.부호화(متن);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + باڊي_متن.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(باڊي_متن);
                } catch (IOException نقص) { throw new UncheckedIOException(نقص); }
            });
            تصديق_ڪريو(통신.가져오기(URI.create("http://127.0.0.1:" + سرور_قدر.getLocalPort()), Duration.ofSeconds(30)).body().equals(متن), "HTTP_TCP");
            جواب_ڏيو.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        تصديق_ڪريو(new ProcessBuilder("/bin/echo", "عمل_قدر").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font فانٽ_قدر = new Font("Dialog", Font.PLAIN, 18);
                تصديق_ڪريو(فانٽ_قدر.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                تصديق_ڪريو(فانٽ_قدر.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea متن_وارو_باڪس = new JTextArea(متن);
                متن_وارو_باڪس.setFont(فانٽ_قدر);
                JFrame دري = 화면.دري("그래픽 ڪارگر_ڪريو", متن_وارو_باڪس, 800, 240);
                BufferedImage ڊرائنگ_قدر = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = ڊرائنگ_قدر.createGraphics();
                دري.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(ڊرائنگ_قدر, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException نقص) { throw new UncheckedIOException(نقص); }
                دري.dispose();
                تصديق_ڪريو(متن_وارو_باڪس.getText().equals(متن), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
