// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import فارسی.자바.*;
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
    interface مقدار { long خواندن(); }
    static class 부모 { protected long مقدار = 42; }
    static class فرزند_مقدار extends 부모 implements مقدار { public long خواندن() { return مقدار; } }
    private static void تأیید_صحت(boolean شرط, String نام) {
        if (!شرط) throw new AssertionError(نام);
        System.out.println("PASS " + نام);
    }
    public static void main(String[] نشانوندها) throws Exception {
        String متن = "한글 日本語 العربية हिन्दी 😀";
        Path ذخیره_مقدار = Path.of(System.getProperty("user.home"), "اعتبارسنجی_داده_ها.txt");
        پرونده.نوشتن(ذخیره_مقدار, متن);
        تأیید_صحت(پرونده.خواندن(ذخیره_مقدار).equals(متن), "UTF8_FILE");
        تأیید_صحت(문자.코드포인트수("한😀") == 2, "UNICODE");
        تأیید_صحت(문자.بهنجار_کردن_مقدار("\u1100\u1161").equals("가"), "NORMALIZATION");
        مقدار شئ_مقدار = new فرزند_مقدار();
        تأیید_صحت(شئ_مقدار.خواندن() == 42 && (long)فرزند_مقدار.class.getMethod("خواندن").invoke(شئ_مقدار) == 42, "OBJECT_INHERITANCE_REFLECTION");
        تأیید_صحت(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("ارزیابی_کردن"); }
        catch (IOException استثنا) { تأیید_صحت(استثنا.getMessage().equals("ارزیابی_کردن"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread رشته_مقدار = 작업.اجرا_2("한글 رشته_مقدار", () -> 합.set(123));
        작업.기다리기(رشته_مقدار);
        تأیید_صحت(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket سرور_مقدار = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> پاسخ_دادن = 일꾼.submit(() -> {
                try (Socket 소켓 = سرور_مقدار.accept()) {
                    BufferedReader خواندن = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String خط;
                    while ((خط = خواندن.readLine()) != null && !خط.isEmpty()) {}
                    byte[] متن_اصلی = 문자.부호화(متن);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + متن_اصلی.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(متن_اصلی);
                } catch (IOException خطا) { throw new UncheckedIOException(خطا); }
            });
            تأیید_صحت(통신.가져오기(URI.create("http://127.0.0.1:" + سرور_مقدار.getLocalPort()), Duration.ofSeconds(30)).body().equals(متن), "HTTP_TCP");
            پاسخ_دادن.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        تأیید_صحت(new ProcessBuilder("/bin/echo", "فرآیند_مقدار").start().waitFor() == 0, "PROCESS");
        if (نشانوندها.length > 0 && نشانوندها[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font قلم_مقدار = new Font("Dialog", Font.PLAIN, 18);
                تأیید_صحت(قلم_مقدار.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                تأیید_صحت(قلم_مقدار.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea قسمت_متن = new JTextArea(متن);
                قسمت_متن.setFont(قلم_مقدار);
                JFrame پنجره = 화면.پنجره("그래픽 ارزیابی_کردن", قسمت_متن, 800, 240);
                BufferedImage نقاشی_مقدار = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = نقاشی_مقدار.createGraphics();
                پنجره.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(نقاشی_مقدار, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException خطا) { throw new UncheckedIOException(خطا); }
                پنجره.dispose();
                تأیید_صحت(قسمت_متن.getText().equals(متن), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
