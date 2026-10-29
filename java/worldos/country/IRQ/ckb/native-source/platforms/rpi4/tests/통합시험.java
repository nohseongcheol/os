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
    interface نرخ { long 읽기(); }
    static class 부모 { protected long نرخ = 42; }
    static class منداڵ_نرخ extends 부모 implements نرخ { public long 읽기() { return نرخ; } }
    private static void سەلماندن(boolean دۆخ, String ناو) {
        if (!دۆخ) throw new AssertionError(ناو);
        System.out.println("PASS " + ناو);
    }
    public static void main(String[] 인수) throws Exception {
        String دەق = "한글 日本語 العربية हिन्दी 😀";
        Path Store_نرخ = Path.of(System.getProperty("user.home"), "ڕەواکردن_دەیتا.txt");
        فایل.ڕایت_کردن(Store_نرخ, دەق);
        سەلماندن(فایل.읽기(Store_نرخ).equals(دەق), "UTF8_FILE");
        سەلماندن(문자.코드포인트수("한😀") == 2, "UNICODE");
        سەلماندن(문자.ئاساییکردن_نرخ("\u1100\u1161").equals("가"), "NORMALIZATION");
        نرخ شت_نرخ = new منداڵ_نرخ();
        سەلماندن(شت_نرخ.읽기() == 42 && (long)منداڵ_نرخ.class.getMethod("읽기").invoke(شت_نرخ) == 42, "OBJECT_INHERITANCE_REFLECTION");
        سەلماندن(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("ڕەوایی"); }
        catch (IOException 예외) { سەلماندن(예외.getMessage().equals("ڕەوایی"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread ڕستە_نرخ = 작업.ڕادان("한글 ڕستە_نرخ", () -> 합.set(123));
        작업.기다리기(ڕستە_نرخ);
        سەلماندن(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket ڕاژەکار_نرخ = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> وەڵامدانەوه = 일꾼.submit(() -> {
                try (Socket 소켓 = ڕاژەکار_نرخ.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String دێڕ;
                    while ((دێڕ = 읽기.readLine()) != null && !دێڕ.isEmpty()) {}
                    byte[] دەقی_تێکستەکە = 문자.부호화(دەق);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + دەقی_تێکستەکە.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(دەقی_تێکستەکە);
                } catch (IOException هەڵە) { throw new UncheckedIOException(هەڵە); }
            });
            سەلماندن(통신.가져오기(URI.create("http://127.0.0.1:" + ڕاژەکار_نرخ.getLocalPort()), Duration.ofSeconds(30)).body().equals(دەق), "HTTP_TCP");
            وەڵامدانەوه.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        سەلماندن(new ProcessBuilder("/bin/echo", "پرۆسە_نرخ").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font جۆرەپیت_نرخ = new Font("Dialog", Font.PLAIN, 18);
                سەلماندن(جۆرەپیت_نرخ.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                سەلماندن(جۆرەپیت_نرخ.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea سندوقی_دەق = new JTextArea(دەق);
                سندوقی_دەق.setFont(جۆرەپیت_نرخ);
                JFrame پەنجەرە = 화면.پەنجەرە("그래픽 ڕەوایی", سندوقی_دەق, 800, 240);
                BufferedImage نگار_نرخ = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = نگار_نرخ.createGraphics();
                پەنجەرە.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(نگار_نرخ, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException هەڵە) { throw new UncheckedIOException(هەڵە); }
                پەنجەرە.dispose();
                سەلماندن(سندوقی_دەق.getText().equals(دەق), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
