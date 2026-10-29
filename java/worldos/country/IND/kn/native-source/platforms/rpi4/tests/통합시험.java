// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import ಕನ್ನಡ.자바.*;
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
    interface ಮೌಲ್ಯ { long ಓದು(); }
    static class 부모 { protected long ಮೌಲ್ಯ = 42; }
    static class ಮಗು_ಮೌಲ್ಯ extends 부모 implements ಮೌಲ್ಯ { public long ಓದು() { return ಮೌಲ್ಯ; } }
    private static void ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(boolean ಸ್ಥಿತಿ, String ಹೆಸರು) {
        if (!ಸ್ಥಿತಿ) throw new AssertionError(ಹೆಸರು);
        System.out.println("PASS " + ಹೆಸರು);
    }
    public static void main(String[] 인수) throws Exception {
        String ಪಠ್ಯ = "한글 日本語 العربية हिन्दी 😀";
        Path ಸ್ಟೋರ್_ಮೌಲ್ಯ = Path.of(System.getProperty("user.home"), "ದೃಢೀಕರಣ_ಡೇಟಾ.txt");
        ಕಡತ.ಬರೆ(ಸ್ಟೋರ್_ಮೌಲ್ಯ, ಪಠ್ಯ);
        ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಕಡತ.ಓದು(ಸ್ಟೋರ್_ಮೌಲ್ಯ).equals(ಪಠ್ಯ), "UTF8_FILE");
        ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(문자.코드포인트수("한😀") == 2, "UNICODE");
        ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(문자.ಸಮಾನೀಕರಿಸು_ಮೌಲ್ಯ("\u1100\u1161").equals("가"), "NORMALIZATION");
        ಮೌಲ್ಯ ಆಬ್ಜೆಕ್ಟ್_ಮೌಲ್ಯ = new ಮಗು_ಮೌಲ್ಯ();
        ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಆಬ್ಜೆಕ್ಟ್_ಮೌಲ್ಯ.ಓದು() == 42 && (long)ಮಗು_ಮೌಲ್ಯ.class.getMethod("ಓದು").invoke(ಆಬ್ಜೆಕ್ಟ್_ಮೌಲ್ಯ) == 42, "OBJECT_INHERITANCE_REFLECTION");
        ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("ಸಕ್ರಮೀಕರಿಸು"); }
        catch (IOException ವಿನಾಯಿತಿ) { ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ವಿನಾಯಿತಿ.getMessage().equals("ಸಕ್ರಮೀಕರಿಸು"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread ಎಳೆ_ಮೌಲ್ಯ = 작업.ಚಲಾಯಿಸು_2("한글 ಎಳೆ_ಮೌಲ್ಯ", () -> 합.set(123));
        작업.기다리기(ಎಳೆ_ಮೌಲ್ಯ);
        ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket ಸರ್ವರ್_ಮೌಲ್ಯ = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> ಪ್ರತ್ಯುತ್ತರ = 일꾼.submit(() -> {
                try (Socket 소켓 = ಸರ್ವರ್_ಮೌಲ್ಯ.accept()) {
                    BufferedReader ಓದು = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String ಸಾಲು;
                    while ((ಸಾಲು = ಓದು.readLine()) != null && !ಸಾಲು.isEmpty()) {}
                    byte[] ಮುಖ್ಯ_ಪಠ್ಯ = 문자.부호화(ಪಠ್ಯ);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + ಮುಖ್ಯ_ಪಠ್ಯ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(ಮುಖ್ಯ_ಪಠ್ಯ);
                } catch (IOException ದೋಷ) { throw new UncheckedIOException(ದೋಷ); }
            });
            ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(통신.가져오기(URI.create("http://127.0.0.1:" + ಸರ್ವರ್_ಮೌಲ್ಯ.getLocalPort()), Duration.ofSeconds(30)).body().equals(ಪಠ್ಯ), "HTTP_TCP");
            ಪ್ರತ್ಯುತ್ತರ.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(new ProcessBuilder("/bin/echo", "ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ಫಾಂಟ್_ಮೌಲ್ಯ = new Font("Dialog", Font.PLAIN, 18);
                ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಫಾಂಟ್_ಮೌಲ್ಯ.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಫಾಂಟ್_ಮೌಲ್ಯ.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea ಪಠ್ಯ_ಕ್ಷೇತ್ರ_d6e55852 = new JTextArea(ಪಠ್ಯ);
                ಪಠ್ಯ_ಕ್ಷೇತ್ರ_d6e55852.setFont(ಫಾಂಟ್_ಮೌಲ್ಯ);
                JFrame ವಿಂಡೋ = 화면.ವಿಂಡೋ("그래픽 ಸಕ್ರಮೀಕರಿಸು", ಪಠ್ಯ_ಕ್ಷೇತ್ರ_d6e55852, 800, 240);
                BufferedImage ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ.createGraphics();
                ವಿಂಡೋ.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ದೋಷ) { throw new UncheckedIOException(ದೋಷ); }
                ವಿಂಡೋ.dispose();
                ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಪಠ್ಯ_ಕ್ಷೇತ್ರ_d6e55852.getText().equals(ಪಠ್ಯ), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
