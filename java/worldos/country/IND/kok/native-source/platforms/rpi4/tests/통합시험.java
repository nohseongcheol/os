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
    interface मोल { long 읽기(); }
    static class 부모 { protected long मोल = 42; }
    static class भुरगें_मोल extends 부모 implements मोल { public long 읽기() { return मोल; } }
    private static void पुनर्तपासणी_करची(boolean स्थिती_291ac971, String नांव) {
        if (!स्थिती_291ac971) throw new AssertionError(नांव);
        System.out.println("PASS " + नांव);
    }
    public static void main(String[] 인수) throws Exception {
        String SMS = "한글 日本語 العربية हिन्दी 😀";
        Path Store_मोल = Path.of(System.getProperty("user.home"), "वैधताय_डेटा.txt");
        फायल.बरोवचें(Store_मोल, SMS);
        पुनर्तपासणी_करची(फायल.읽기(Store_मोल).equals(SMS), "UTF8_FILE");
        पुनर्तपासणी_करची(문자.वर्ण_कोड_COUNT("한😀") == 2, "UNICODE");
        पुनर्तपासणी_करची(문자.सामान्य_स्थितीर_येवचें_मोल("\u1100\u1161").equals("가"), "NORMALIZATION");
        मोल ऑब्जॅक्ट_मोल = new भुरगें_मोल();
        पुनर्तपासणी_करची(ऑब्जॅक्ट_मोल.읽기() == 42 && (long)भुरगें_मोल.class.getMethod("읽기").invoke(ऑब्जॅक्ट_मोल) == 42, "OBJECT_INHERITANCE_REFLECTION");
        पुनर्तपासणी_करची(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("पुनर्तपासणी_करची_5fb2b747"); }
        catch (IOException 예외) { पुनर्तपासणी_करची(예외.getMessage().equals("पुनर्तपासणी_करची_5fb2b747"), "EXCEPTION"); }
        AtomicInteger SUM_मोल = new AtomicInteger();
        Thread थ्रॅड_मोल = 작업.चलोवप("한글 थ्रॅड_मोल", () -> SUM_मोल.set(123));
        작업.기다리기(थ्रॅड_मोल);
        पुनर्तपासणी_करची(SUM_मोल.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket सर्वर_मोल = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> जाप_दिवप = 일꾼.submit(() -> {
                try (Socket 소켓 = सर्वर_मोल.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String रेग;
                    while ((रेग = 읽기.readLine()) != null && !रेग.isEmpty()) {}
                    byte[] देखीचो_उतारो = 문자.부호화(SMS);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + देखीचो_उतारो.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(देखीचो_उतारो);
                } catch (IOException चूक) { throw new UncheckedIOException(चूक); }
            });
            पुनर्तपासणी_करची(통신.TAKE_मोल(URI.create("http://127.0.0.1:" + सर्वर_मोल.getLocalPort()), Duration.ofSeconds(30)).body().equals(SMS), "HTTP_TCP");
            जाप_दिवप.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        पुनर्तपासणी_करची(new ProcessBuilder("/bin/echo", "प्रक्रिया_मोल").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font फाँट_मोल = new Font("Dialog", Font.PLAIN, 18);
                पुनर्तपासणी_करची(फाँट_मोल.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                पुनर्तपासणी_करची(फाँट_मोल.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea उतारो_बॉक्स = new JTextArea(SMS);
                उतारो_बॉक्स.setFont(फाँट_मोल);
                JFrame विंडो = 화면.विंडो("그래픽 पुनर्तपासणी_करची_5fb2b747", उतारो_बॉक्स, 800, 240);
                BufferedImage रेखाटन_मोल = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = रेखाटन_मोल.createGraphics();
                विंडो.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(रेखाटन_मोल, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException चूक) { throw new UncheckedIOException(चूक); }
                विंडो.dispose();
                पुनर्तपासणी_करची(उतारो_बॉक्स.getText().equals(SMS), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
