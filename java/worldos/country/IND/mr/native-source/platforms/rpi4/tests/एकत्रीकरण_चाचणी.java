// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import मराठी.जावा.*;
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

public class एकत्रीकरण_चाचणी {
    interface मूल्य { long वाचन(); }
    static class जनक_मूल्य { protected long मूल्य = 42; }
    static class उपघटक_मूल्य extends जनक_मूल्य implements मूल्य { public long वाचन() { return मूल्य; } }
    private static void पडताळा(boolean सशर्त, String नाव) {
        if (!सशर्त) throw new AssertionError(नाव);
        System.out.println("PASS " + नाव);
    }
    public static void main(String[] बाबी) throws Exception {
        String पाठ्य = "한글 日本語 العربية हिन्दी 😀";
        Path साठवणे_मूल्य = Path.of(System.getProperty("user.home"), "पडताळणी_डेटा.txt");
        फाइल.लेखन(साठवणे_मूल्य, पाठ्य);
        पडताळा(फाइल.वाचन(साठवणे_मूल्य).equals(पाठ्य), "UTF8_FILE");
        पडताळा(वर्ण.वर्ण_कोड_संख्या("한😀") == 2, "UNICODE");
        पडताळा(वर्ण.सामान्यीकरण_करा_मूल्य("\u1100\u1161").equals("가"), "NORMALIZATION");
        मूल्य ऑब्जेक्ट_मूल्य = new उपघटक_मूल्य();
        पडताळा(ऑब्जेक्ट_मूल्य.वाचन() == 42 && (long)उपघटक_मूल्य.class.getMethod("वाचन").invoke(ऑब्जेक्ट_मूल्य) == 42, "OBJECT_INHERITANCE_REFLECTION");
        पडताळा(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("प्रमाणित"); }
        catch (IOException अपवाद) { पडताळा(अपवाद.getMessage().equals("प्रमाणित"), "EXCEPTION"); }
        AtomicInteger बेरीज_मूल्य = new AtomicInteger();
        Thread कार्यसूत्र_मूल्य_5b72a632 = पारपाडा_कार्य.सुरू_करा("한글 कार्यसूत्र_मूल्य_5b72a632", () -> बेरीज_मूल्य.set(123));
        पारपाडा_कार्य.प्रतीक्षाकरा(कार्यसूत्र_मूल्य_5b72a632);
        पडताळा(बेरीज_मूल्य.get() == 123, "THREAD");
        ExecutorService कार्यसूत्र_मूल्य = Executors.newSingleThreadExecutor();
        try (ServerSocket सर्व्हर_मूल्य = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> प्रत्युत्तर_द्या = कार्यसूत्र_मूल्य.submit(() -> {
                try (Socket संचारद्वार_मूल्य = सर्व्हर_मूल्य.accept()) {
                    BufferedReader वाचन = new BufferedReader(new InputStreamReader(संचारद्वार_मूल्य.getInputStream()));
                    String ओळ;
                    while ((ओळ = वाचन.readLine()) != null && !ओळ.isEmpty()) {}
                    byte[] मुख्य_मजकूर = वर्ण.संकेतन(पाठ्य);
                    संचारद्वार_मूल्य.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + मुख्य_मजकूर.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    संचारद्वार_मूल्य.getOutputStream().write(मुख्य_मजकूर);
                } catch (IOException त्रुटी) { throw new UncheckedIOException(त्रुटी); }
            });
            पडताळा(संचार.घ्या_मूल्य(URI.create("http://127.0.0.1:" + सर्व्हर_मूल्य.getLocalPort()), Duration.ofSeconds(30)).body().equals(पाठ्य), "HTTP_TCP");
            प्रत्युत्तर_द्या.get(30, TimeUnit.SECONDS);
        } finally { कार्यसूत्र_मूल्य.shutdownNow(); }
        पडताळा(new ProcessBuilder("/bin/echo", "प्रक्रिया_मूल्य").start().waitFor() == 0, "PROCESS");
        if (बाबी.length > 0 && बाबी[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font फॉन्ट_मूल्य = new Font("Dialog", Font.PLAIN, 18);
                पडताळा(फॉन्ट_मूल्य.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                पडताळा(फॉन्ट_मूल्य.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea मजकूर_बॉक्स = new JTextArea(पाठ्य);
                मजकूर_बॉक्स.setFont(फॉन्ट_मूल्य);
                JFrame विंडो = पडदा.विंडो("그래픽 प्रमाणित", मजकूर_बॉक्स, 800, 240);
                BufferedImage रेखांकन_मूल्य = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D कुंचला_मूल्य = रेखांकन_मूल्य.createGraphics();
                विंडो.paint(कुंचला_मूल्य); कुंचला_मूल्य.dispose();
                try { javax.imageio.ImageIO.write(रेखांकन_मूल्य, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException त्रुटी) { throw new UncheckedIOException(त्रुटी); }
                विंडो.dispose();
                पडताळा(मजकूर_बॉक्स.getText().equals(पाठ्य), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
