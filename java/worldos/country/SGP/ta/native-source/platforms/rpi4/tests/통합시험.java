// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import தமிழ்.자바.*;
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
    interface மதிப்பு { long படி(); }
    static class 부모 { protected long மதிப்பு = 42; }
    static class குழந்தை_மதிப்பு extends 부모 implements மதிப்பு { public long படி() { return மதிப்பு; } }
    private static void சரிபார்(boolean நிபந்தனை, String பெயர்) {
        if (!நிபந்தனை) throw new AssertionError(பெயர்);
        System.out.println("PASS " + பெயர்);
    }
    public static void main(String[] செயலுருபுகள்) throws Exception {
        String உரை = "한글 日本語 العربية हिन्दी 😀";
        Path சேகரி_மதிப்பு = Path.of(System.getProperty("user.home"), "செல்லுபடியாக்கம்_தரவு.txt");
        கோப்பின்_பெயர்.எழுது(சேகரி_மதிப்பு, உரை);
        சரிபார்(கோப்பின்_பெயர்.படி(சேகரி_மதிப்பு).equals(உரை), "UTF8_FILE");
        சரிபார்(문자.코드포인트수("한😀") == 2, "UNICODE");
        சரிபார்(문자.சீராக்கு_மதிப்பு("\u1100\u1161").equals("가"), "NORMALIZATION");
        மதிப்பு பொருள்_மதிப்பு = new குழந்தை_மதிப்பு();
        சரிபார்(பொருள்_மதிப்பு.படி() == 42 && (long)குழந்தை_மதிப்பு.class.getMethod("படி").invoke(பொருள்_மதிப்பு) == 42, "OBJECT_INHERITANCE_REFLECTION");
        சரிபார்(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("சரிபார்_5fb2b747"); }
        catch (IOException விதிவிலக்கு) { சரிபார்(விதிவிலக்கு.getMessage().equals("சரிபார்_5fb2b747"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread தொடரிழை_மதிப்பு = 작업.செயல்படுத்துக("한글 தொடரிழை_மதிப்பு", () -> 합.set(123));
        작업.기다리기(தொடரிழை_மதிப்பு);
        சரிபார்(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket சேவையகம்_மதிப்பு = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> பதிலளி = 일꾼.submit(() -> {
                try (Socket 소켓 = சேவையகம்_மதிப்பு.accept()) {
                    BufferedReader படி = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String உள்ளீட்டு_வரி;
                    while ((உள்ளீட்டு_வரி = படி.readLine()) != null && !உள்ளீட்டு_வரி.isEmpty()) {}
                    byte[] தகவல்_உரை = 문자.부호화(உரை);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + தகவல்_உரை.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(தகவல்_உரை);
                } catch (IOException பிழை) { throw new UncheckedIOException(பிழை); }
            });
            சரிபார்(통신.가져오기(URI.create("http://127.0.0.1:" + சேவையகம்_மதிப்பு.getLocalPort()), Duration.ofSeconds(30)).body().equals(உரை), "HTTP_TCP");
            பதிலளி.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        சரிபார்(new ProcessBuilder("/bin/echo", "செயலகம்_மதிப்பு").start().waitFor() == 0, "PROCESS");
        if (செயலுருபுகள்.length > 0 && செயலுருபுகள்[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font எழுத்துரு_மதிப்பு = new Font("Dialog", Font.PLAIN, 18);
                சரிபார்(எழுத்துரு_மதிப்பு.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                சரிபார்(எழுத்துரு_மதிப்பு.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea உரைப்_பகுதி = new JTextArea(உரை);
                உரைப்_பகுதி.setFont(எழுத்துரு_மதிப்பு);
                JFrame சாளரம் = 화면.சாளரம்("그래픽 சரிபார்_5fb2b747", உரைப்_பகுதி, 800, 240);
                BufferedImage வரைதல்_மதிப்பு = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = வரைதல்_மதிப்பு.createGraphics();
                சாளரம்.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(வரைதல்_மதிப்பு, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException பிழை) { throw new UncheckedIOException(பிழை); }
                சாளரம்.dispose();
                சரிபார்(உரைப்_பகுதி.getText().equals(உரை), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
