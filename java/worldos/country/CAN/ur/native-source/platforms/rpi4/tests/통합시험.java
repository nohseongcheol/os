// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import اردو.자바.*;
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
    interface قدر { long پڑھیں(); }
    static class 부모 { protected long قدر = 42; }
    static class بچہ_قدر extends 부모 implements قدر { public long پڑھیں() { return قدر; } }
    private static void تصدیق_کریں(boolean شرط, String نام) {
        if (!شرط) throw new AssertionError(نام);
        System.out.println("PASS " + نام);
    }
    public static void main(String[] دلائل) throws Exception {
        String متن = "한글 日本語 العربية हिन्दी 😀";
        Path ذخیرہ_کریں_قدر = Path.of(System.getProperty("user.home"), "توثیق_کوائف.txt");
        فائل_کا_نام.لکھیں(ذخیرہ_کریں_قدر, متن);
        تصدیق_کریں(فائل_کا_نام.پڑھیں(ذخیرہ_کریں_قدر).equals(متن), "UTF8_FILE");
        تصدیق_کریں(문자.코드포인트수("한😀") == 2, "UNICODE");
        تصدیق_کریں(문자.عمومی_بنائيں_قدر("\u1100\u1161").equals("가"), "NORMALIZATION");
        قدر آبجیکٹ_قدر = new بچہ_قدر();
        تصدیق_کریں(آبجیکٹ_قدر.پڑھیں() == 42 && (long)بچہ_قدر.class.getMethod("پڑھیں").invoke(آبجیکٹ_قدر) == 42, "OBJECT_INHERITANCE_REFLECTION");
        تصدیق_کریں(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("جواز_دہی_کریں"); }
        catch (IOException استثنا) { تصدیق_کریں(استثنا.getMessage().equals("جواز_دہی_کریں"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread تھریڈ_قدر = 작업.چلائیں("한글 تھریڈ_قدر", () -> 합.set(123));
        작업.기다리기(تھریڈ_قدر);
        تصدیق_کریں(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket سرور_قدر = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> جواب_دیں = 일꾼.submit(() -> {
                try (Socket 소켓 = سرور_قدر.accept()) {
                    BufferedReader پڑھیں = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String اندراج_کی_سطر;
                    while ((اندراج_کی_سطر = پڑھیں.readLine()) != null && !اندراج_کی_سطر.isEmpty()) {}
                    byte[] بنیادی_متن = 문자.부호화(متن);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + بنیادی_متن.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(بنیادی_متن);
                } catch (IOException غلطی) { throw new UncheckedIOException(غلطی); }
            });
            تصدیق_کریں(통신.가져오기(URI.create("http://127.0.0.1:" + سرور_قدر.getLocalPort()), Duration.ofSeconds(30)).body().equals(متن), "HTTP_TCP");
            جواب_دیں.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        تصدیق_کریں(new ProcessBuilder("/bin/echo", "عمل_قدر").start().waitFor() == 0, "PROCESS");
        if (دلائل.length > 0 && دلائل[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font فانٹ_قدر = new Font("Dialog", Font.PLAIN, 18);
                تصدیق_کریں(فانٹ_قدر.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                تصدیق_کریں(فانٹ_قدر.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea متن_خانہ = new JTextArea(متن);
                متن_خانہ.setFont(فانٹ_قدر);
                JFrame ونڈو = 화면.ونڈو("그래픽 جواز_دہی_کریں", متن_خانہ, 800, 240);
                BufferedImage ڈرائنگ_قدر = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = ڈرائنگ_قدر.createGraphics();
                ونڈو.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(ڈرائنگ_قدر, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException غلطی) { throw new UncheckedIOException(غلطی); }
                ونڈو.dispose();
                تصدیق_کریں(متن_خانہ.getText().equals(متن), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
