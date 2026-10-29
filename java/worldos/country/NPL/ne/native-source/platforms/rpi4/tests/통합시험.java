// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import नेपाली.자바.*;
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
    interface मान { long पढनुहोस्(); }
    static class 부모 { protected long मान = 42; }
    static class बच्चा_मान extends 부모 implements मान { public long पढनुहोस्() { return मान; } }
    private static void रुजू_गर्नुहोस्(boolean सर्त, String नाम) {
        if (!सर्त) throw new AssertionError(नाम);
        System.out.println("PASS " + नाम);
    }
    public static void main(String[] तर्क) throws Exception {
        String पाठ = "한글 日本語 العربية हिन्दी 😀";
        Path भण्डार_गर्नुहोस्_मान = Path.of(System.getProperty("user.home"), "वैधानिकता_लगत.txt");
        फाइल.लेख्नुहोस्(भण्डार_गर्नुहोस्_मान, पाठ);
        रुजू_गर्नुहोस्(फाइल.पढनुहोस्(भण्डार_गर्नुहोस्_मान).equals(पाठ), "UTF8_FILE");
        रुजू_गर्नुहोस्(문자.코드포인트수("한😀") == 2, "UNICODE");
        रुजू_गर्नुहोस्(문자.सामान्यकरण_गर्नुहोस्_मान("\u1100\u1161").equals("가"), "NORMALIZATION");
        मान वस्तु_मान = new बच्चा_मान();
        रुजू_गर्नुहोस्(वस्तु_मान.पढनुहोस्() == 42 && (long)बच्चा_मान.class.getMethod("पढनुहोस्").invoke(वस्तु_मान) == 42, "OBJECT_INHERITANCE_REFLECTION");
        रुजू_गर्नुहोस्(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("वैध_गर्नुहोस्"); }
        catch (IOException 예외) { रुजू_गर्नुहोस्(예외.getMessage().equals("वैध_गर्नुहोस्"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread धागो_मान = 작업.चलाउनुहोस्("한글 धागो_मान", () -> 합.set(123));
        작업.기다리기(धागो_मान);
        रुजू_गर्नुहोस्(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket सर्भर_मान = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> जवाफ_दिनुहोस् = 일꾼.submit(() -> {
                try (Socket 소켓 = सर्भर_मान.accept()) {
                    BufferedReader पढनुहोस् = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String रेखा;
                    while ((रेखा = पढनुहोस्.readLine()) != null && !रेखा.isEmpty()) {}
                    byte[] मुख्य_पाठ = 문자.부호화(पाठ);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + मुख्य_पाठ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(मुख्य_पाठ);
                } catch (IOException त्रुटि) { throw new UncheckedIOException(त्रुटि); }
            });
            रुजू_गर्नुहोस्(통신.가져오기(URI.create("http://127.0.0.1:" + सर्भर_मान.getLocalPort()), Duration.ofSeconds(30)).body().equals(पाठ), "HTTP_TCP");
            जवाफ_दिनुहोस्.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        रुजू_गर्नुहोस्(new ProcessBuilder("/bin/echo", "प्रक्रिया_मान").start().waitFor() == 0, "PROCESS");
        if (तर्क.length > 0 && तर्क[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font फन्ट_मान = new Font("Dialog", Font.PLAIN, 18);
                रुजू_गर्नुहोस्(फन्ट_मान.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                रुजू_गर्नुहोस्(फन्ट_मान.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea पाठ_बाकस = new JTextArea(पाठ);
                पाठ_बाकस.setFont(फन्ट_मान);
                JFrame सन्झ्याल = 화면.सन्झ्याल("그래픽 वैध_गर्नुहोस्", पाठ_बाकस, 800, 240);
                BufferedImage चित्रकारी_मान = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = चित्रकारी_मान.createGraphics();
                सन्झ्याल.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(चित्रकारी_मान, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException त्रुटि) { throw new UncheckedIOException(त्रुटि); }
                सन्झ्याल.dispose();
                रुजू_गर्नुहोस्(पाठ_बाकस.getText().equals(पाठ), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
