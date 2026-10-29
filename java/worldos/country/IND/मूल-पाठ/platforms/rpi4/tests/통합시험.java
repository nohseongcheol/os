// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import हिंदी.자바.*;
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
    interface मान { long पढ़ें(); }
    static class पैरेंट_मान { protected long मान = 42; }
    static class बच्चा_मान extends पैरेंट_मान implements मान { public long पढ़ें() { return मान; } }
    private static void सत्यापित_करें(boolean शर्त, String नाम) {
        if (!शर्त) throw new AssertionError(नाम);
        System.out.println("PASS " + नाम);
    }
    public static void main(String[] तर्क) throws Exception {
        String पाठ = "한글 日本語 العربية हिन्दी 😀";
        Path स्टोर_मान = Path.of(System.getProperty("user.home"), "प्रमाणीकरण_डेटा.txt");
        संचिका.लिखें(स्टोर_मान, पाठ);
        सत्यापित_करें(संचिका.पढ़ें(स्टोर_मान).equals(पाठ), "UTF8_FILE");
        सत्यापित_करें(문자.코드포인트수("한😀") == 2, "UNICODE");
        सत्यापित_करें(문자.सामान्य_करें_मान("\u1100\u1161").equals("가"), "NORMALIZATION");
        मान ऑब्जेक्ट_मान = new बच्चा_मान();
        सत्यापित_करें(ऑब्जेक्ट_मान.पढ़ें() == 42 && (long)बच्चा_मान.class.getMethod("पढ़ें").invoke(ऑब्जेक्ट_मान) == 42, "OBJECT_INHERITANCE_REFLECTION");
        सत्यापित_करें(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("मान्य_करें"); }
        catch (IOException अपवाद) { सत्यापित_करें(अपवाद.getMessage().equals("मान्य_करें"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread थ्रेड_मान = 작업.चलाएँ("한글 थ्रेड_मान", () -> 합.set(123));
        작업.기다리기(थ्रेड_मान);
        सत्यापित_करें(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket 서버 = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> उत्तर = 일꾼.submit(() -> {
                try (Socket सॉकेट_मान = 서버.accept()) {
                    BufferedReader पढ़ें = new BufferedReader(new InputStreamReader(सॉकेट_मान.getInputStream()));
                    String पंक्ति;
                    while ((पंक्ति = पढ़ें.readLine()) != null && !पंक्ति.isEmpty()) {}
                    byte[] मुख्य_पाठ = 문자.부호화(पाठ);
                    सॉकेट_मान.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + मुख्य_पाठ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    सॉकेट_मान.getOutputStream().write(मुख्य_पाठ);
                } catch (IOException त्रुटि) { throw new UncheckedIOException(त्रुटि); }
            });
            सत्यापित_करें(통신.가져오기(URI.create("http://127.0.0.1:" + 서버.getLocalPort()), Duration.ofSeconds(30)).body().equals(पाठ), "HTTP_TCP");
            उत्तर.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        सत्यापित_करें(new ProcessBuilder("/bin/echo", "प्रक्रिया_मान").start().waitFor() == 0, "PROCESS");
        if (तर्क.length > 0 && तर्क[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font फ़ॉन्ट_मान = new Font("Dialog", Font.PLAIN, 18);
                सत्यापित_करें(फ़ॉन्ट_मान.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                सत्यापित_करें(फ़ॉन्ट_मान.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea संपादन_बॉक्_स = new JTextArea(पाठ);
                संपादन_बॉक्_स.setFont(फ़ॉन्ट_मान);
                JFrame खिड़की = 화면.खिड़की("그래픽 मान्य_करें", संपादन_बॉक्_स, 800, 240);
                BufferedImage ड्रॉइंग_मान = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = ड्रॉइंग_मान.createGraphics();
                खिड़की.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(ड्रॉइंग_मान, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException त्रुटि) { throw new UncheckedIOException(त्रुटि); }
                खिड़की.dispose();
                सत्यापित_करें(संपादन_बॉक्_स.getText().equals(पाठ), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
