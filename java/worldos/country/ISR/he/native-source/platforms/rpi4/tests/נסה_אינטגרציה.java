// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import עברית.자바.*;
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

public class נסה_אינטגרציה {
    interface ערך { long קרא(); }
    static class אב_ערך { protected long ערך = 42; }
    static class ילד_ערך extends אב_ערך implements ערך { public long קרא() { return ערך; } }
    private static void ודא_אמת(boolean תנאי, String שם) {
        if (!תנאי) throw new AssertionError(שם);
        System.out.println("PASS " + שם);
    }
    public static void main(String[] ארגומנטים) throws Exception {
        String טקסט = "한글 日本語 العربية हिन्दी 😀";
        Path מאגר_ערך = Path.of(System.getProperty("user.home"), "אימות_נתונים.txt");
        קובץ.כתוב(מאגר_ערך, טקסט);
        ודא_אמת(קובץ.קרא(מאגר_ערך).equals(טקסט), "UTF8_FILE");
        ודא_אמת(문자.코드포인트수("한😀") == 2, "UNICODE");
        ודא_אמת(문자.לנרמל_ערך("\u1100\u1161").equals("가"), "NORMALIZATION");
        ערך אובייקט_ערך = new ילד_ערך();
        ודא_אמת(אובייקט_ערך.קרא() == 42 && (long)ילד_ערך.class.getMethod("קרא").invoke(אובייקט_ערך) == 42, "OBJECT_INHERITANCE_REFLECTION");
        ודא_אמת(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("לאמת"); }
        catch (IOException חריגה) { ודא_אמת(חריגה.getMessage().equals("לאמת"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread שרשור_ערך = 작업.הפעלה("한글 שרשור_ערך", () -> 합.set(123));
        작업.기다리기(שרשור_ערך);
        ודא_אמת(합.get() == 123, "THREAD");
        ExecutorService עובד_ערך = Executors.newSingleThreadExecutor();
        try (ServerSocket שרת_ערך = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> מענה = עובד_ערך.submit(() -> {
                try (Socket 소켓 = שרת_ערך.accept()) {
                    BufferedReader קרא = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String שורה;
                    while ((שורה = קרא.readLine()) != null && !שורה.isEmpty()) {}
                    byte[] גוף_הטקסט = 문자.לקדד(טקסט);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + גוף_הטקסט.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(גוף_הטקסט);
                } catch (IOException שגיאה) { throw new UncheckedIOException(שגיאה); }
            });
            ודא_אמת(통신.가져오기(URI.create("http://127.0.0.1:" + שרת_ערך.getLocalPort()), Duration.ofSeconds(30)).body().equals(טקסט), "HTTP_TCP");
            מענה.get(30, TimeUnit.SECONDS);
        } finally { עובד_ערך.shutdownNow(); }
        ודא_אמת(new ProcessBuilder("/bin/echo", "תהליך_ערך").start().waitFor() == 0, "PROCESS");
        if (ארגומנטים.length > 0 && ארגומנטים[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font גופן_ערך = new Font("Dialog", Font.PLAIN, 18);
                ודא_אמת(גופן_ערך.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                ודא_אמת(גופן_ערך.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea תיבת_טקסט = new JTextArea(טקסט);
                תיבת_טקסט.setFont(גופן_ערך);
                JFrame חלון = 화면.חלון("그래픽 לאמת", תיבת_טקסט, 800, 240);
                BufferedImage ציור_ערך = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D מברשת_ערך = ציור_ערך.createGraphics();
                חלון.paint(מברשת_ערך); מברשת_ערך.dispose();
                try { javax.imageio.ImageIO.write(ציור_ערך, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException שגיאה) { throw new UncheckedIOException(שגיאה); }
                חלון.dispose();
                ודא_אמת(תיבת_טקסט.getText().equals(טקסט), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
