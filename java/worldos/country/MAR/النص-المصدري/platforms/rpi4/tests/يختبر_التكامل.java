// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import العربية.자바.*;
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

public class يختبر_التكامل {
    interface قيمة { long قراءة(); }
    static class أصل_قيمة { protected long قيمة = 42; }
    static class طفل_قيمة extends أصل_قيمة implements قيمة { public long قراءة() { return قيمة; } }
    private static void يتحقق(boolean شرط, String اسم) {
        if (!شرط) throw new AssertionError(اسم);
        System.out.println("PASS " + اسم);
    }
    public static void main(String[] وسائط) throws Exception {
        String نص = "한글 日本語 العربية हिन्दी 😀";
        Path مخزن_قيمة = Path.of(System.getProperty("user.home"), "التحقق_من_صحة_بيانات.txt");
        ملف.كتابة(مخزن_قيمة, نص);
        يتحقق(ملف.قراءة(مخزن_قيمة).equals(نص), "UTF8_FILE");
        يتحقق(문자.코드포인트수("한😀") == 2, "UNICODE");
        يتحقق(문자.يقلل_التكرار_قيمة("\u1100\u1161").equals("가"), "NORMALIZATION");
        قيمة عنصر_قيمة_2ed200e9 = new طفل_قيمة();
        يتحقق(عنصر_قيمة_2ed200e9.قراءة() == 42 && (long)طفل_قيمة.class.getMethod("قراءة").invoke(عنصر_قيمة_2ed200e9) == 42, "OBJECT_INHERITANCE_REFLECTION");
        يتحقق(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("التحقق_من_صحة"); }
        catch (IOException استثناء) { يتحقق(استثناء.getMessage().equals("التحقق_من_صحة"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread محادثة_قيمة = 작업.تشغيل("한글 محادثة_قيمة", () -> 합.set(123));
        작업.기다리기(محادثة_قيمة);
        يتحقق(합.get() == 123, "THREAD");
        ExecutorService عامل_قيمة = Executors.newSingleThreadExecutor();
        try (ServerSocket خادم_قيمة = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> رد = عامل_قيمة.submit(() -> {
                try (Socket مأخذ_التوصيل_قيمة = خادم_قيمة.accept()) {
                    BufferedReader قراءة = new BufferedReader(new InputStreamReader(مأخذ_التوصيل_قيمة.getInputStream()));
                    String سطر;
                    while ((سطر = قراءة.readLine()) != null && !سطر.isEmpty()) {}
                    byte[] نص_أساسي = 문자.يرمّز(نص);
                    مأخذ_التوصيل_قيمة.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + نص_أساسي.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    مأخذ_التوصيل_قيمة.getOutputStream().write(نص_أساسي);
                } catch (IOException خطأ) { throw new UncheckedIOException(خطأ); }
            });
            يتحقق(통신.가져오기(URI.create("http://127.0.0.1:" + خادم_قيمة.getLocalPort()), Duration.ofSeconds(30)).body().equals(نص), "HTTP_TCP");
            رد.get(30, TimeUnit.SECONDS);
        } finally { عامل_قيمة.shutdownNow(); }
        يتحقق(new ProcessBuilder("/bin/echo", "عملية_قيمة").start().waitFor() == 0, "PROCESS");
        if (وسائط.length > 0 && وسائط[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font خط_قيمة = new Font("Dialog", Font.PLAIN, 18);
                يتحقق(خط_قيمة.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                يتحقق(خط_قيمة.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea مربع_نص = new JTextArea(نص);
                مربع_نص.setFont(خط_قيمة);
                JFrame نافذة = 화면.نافذة("그래픽 التحقق_من_صحة", مربع_نص, 800, 240);
                BufferedImage رسم_قيمة = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D فرشاة_قيمة = رسم_قيمة.createGraphics();
                نافذة.paint(فرشاة_قيمة); فرشاة_قيمة.dispose();
                try { javax.imageio.ImageIO.write(رسم_قيمة, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException خطأ) { throw new UncheckedIOException(خطأ); }
                نافذة.dispose();
                يتحقق(مربع_نص.getText().equals(نص), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
