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
    static class بچہ_قدر extends 부모 implements قدر { public long 읽기() { return قدر; } }
    private static void تصدیق_کرو(boolean حالت, String ناں) {
        if (!حالت) throw new AssertionError(ناں);
        System.out.println("PASS " + ناں);
    }
    public static void main(String[] 인수) throws Exception {
        String متن = "한글 日本語 العربية हिन्दी 😀";
        Path ذخیرہ_کرو_قدر = Path.of(System.getProperty("user.home"), "جواز_دہی_کوائف.txt");
        فائل.لکھو(ذخیرہ_کرو_قدر, متن);
        تصدیق_کرو(فائل.읽기(ذخیرہ_کرو_قدر).equals(متن), "UTF8_FILE");
        تصدیق_کرو(문자.코드포인트수("한😀") == 2, "UNICODE");
        تصدیق_کرو(문자.عام_بناؤ_قدر("\u1100\u1161").equals("가"), "NORMALIZATION");
        قدر آبجیکٹ_قدر = new بچہ_قدر();
        تصدیق_کرو(آبجیکٹ_قدر.읽기() == 42 && (long)بچہ_قدر.class.getMethod("읽기").invoke(آبجیکٹ_قدر) == 42, "OBJECT_INHERITANCE_REFLECTION");
        تصدیق_کرو(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("تریخ_دے_مطابق_کرو"); }
        catch (IOException 예외) { تصدیق_کرو(예외.getMessage().equals("تریخ_دے_مطابق_کرو"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread لڑی_قدر = 작업.چلاؤ("한글 لڑی_قدر", () -> 합.set(123));
        작업.기다리기(لڑی_قدر);
        تصدیق_کرو(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket سرور_قدر = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> جواب_دیوؤ = 일꾼.submit(() -> {
                try (Socket 소켓 = سرور_قدر.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String لائن;
                    while ((لائن = 읽기.readLine()) != null && !لائن.isEmpty()) {}
                    byte[] متن_دا_ڈھانچہ = 문자.부호화(متن);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + متن_دا_ڈھانچہ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(متن_دا_ڈھانچہ);
                } catch (IOException نقص) { throw new UncheckedIOException(نقص); }
            });
            تصدیق_کرو(통신.가져오기(URI.create("http://127.0.0.1:" + سرور_قدر.getLocalPort()), Duration.ofSeconds(30)).body().equals(متن), "HTTP_TCP");
            جواب_دیوؤ.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        تصدیق_کرو(new ProcessBuilder("/bin/echo", "عمل_قدر").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font فانٹ_قدر = new Font("Dialog", Font.PLAIN, 18);
                تصدیق_کرو(فانٹ_قدر.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                تصدیق_کرو(فانٹ_قدر.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea ٹیکسٹ_باکس = new JTextArea(متن);
                ٹیکسٹ_باکس.setFont(فانٹ_قدر);
                JFrame کھڑکی = 화면.کھڑکی("그래픽 تریخ_دے_مطابق_کرو", ٹیکسٹ_باکس, 800, 240);
                BufferedImage ڈرائنگ_قدر = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = ڈرائنگ_قدر.createGraphics();
                کھڑکی.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(ڈرائنگ_قدر, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException نقص) { throw new UncheckedIOException(نقص); }
                کھڑکی.dispose();
                تصدیق_کرو(ٹیکسٹ_باکس.getText().equals(متن), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
