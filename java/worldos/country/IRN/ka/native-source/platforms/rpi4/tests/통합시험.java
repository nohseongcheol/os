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
    interface მნიშვნელობა { long კითხვა(); }
    static class 부모 { protected long მნიშვნელობა = 42; }
    static class ბავშვი_მნიშვნელობა extends 부모 implements მნიშვნელობა { public long კითხვა() { return მნიშვნელობა; } }
    private static void გადამოწმება(boolean პირობა, String სახელი) {
        if (!პირობა) throw new AssertionError(სახელი);
        System.out.println("PASS " + სახელი);
    }
    public static void main(String[] 인수) throws Exception {
        String ტექსტი = "한글 日本語 العربية हिन्दी 😀";
        Path შენახვა_მნიშვნელობა = Path.of(System.getProperty("user.home"), "გადამოწმება_მონაცემები.txt");
        ფაილი.ჩაწერა(შენახვა_მნიშვნელობა, ტექსტი);
        გადამოწმება(ფაილი.კითხვა(შენახვა_მნიშვნელობა).equals(ტექსტი), "UTF8_FILE");
        გადამოწმება(문자.코드포인트수("한😀") == 2, "UNICODE");
        გადამოწმება(문자.მოწესრიგება_მნიშვნელობა("\u1100\u1161").equals("가"), "NORMALIZATION");
        მნიშვნელობა ობიექტი_მნიშვნელობა = new ბავშვი_მნიშვნელობა();
        გადამოწმება(ობიექტი_მნიშვნელობა.კითხვა() == 42 && (long)ბავშვი_მნიშვნელობა.class.getMethod("კითხვა").invoke(ობიექტი_მნიშვნელობა) == 42, "OBJECT_INHERITANCE_REFLECTION");
        გადამოწმება(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("შემოწმება"); }
        catch (IOException 예외) { გადამოწმება(예외.getMessage().equals("შემოწმება"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread თემა_მნიშვნელობა = 작업.გაშვება("한글 თემა_მნიშვნელობა", () -> 합.set(123));
        작업.기다리기(თემა_მნიშვნელობა);
        გადამოწმება(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket სერვერი_მნიშვნელობა = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> პასუხი = 일꾼.submit(() -> {
                try (Socket 소켓 = სერვერი_მნიშვნელობა.accept()) {
                    BufferedReader კითხვა = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String ხაზი;
                    while ((ხაზი = კითხვა.readLine()) != null && !ხაზი.isEmpty()) {}
                    byte[] ძირითადი_ტექსტი = 문자.부호화(ტექსტი);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + ძირითადი_ტექსტი.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(ძირითადი_ტექსტი);
                } catch (IOException შეცდომა) { throw new UncheckedIOException(შეცდომა); }
            });
            გადამოწმება(통신.가져오기(URI.create("http://127.0.0.1:" + სერვერი_მნიშვნელობა.getLocalPort()), Duration.ofSeconds(30)).body().equals(ტექსტი), "HTTP_TCP");
            პასუხი.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        გადამოწმება(new ProcessBuilder("/bin/echo", "პროცესი_მნიშვნელობა").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font შრიფტი_მნიშვნელობა = new Font("Dialog", Font.PLAIN, 18);
                გადამოწმება(შრიფტი_მნიშვნელობა.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                გადამოწმება(შრიფტი_მნიშვნელობა.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea ტექსტის_არე = new JTextArea(ტექსტი);
                ტექსტის_არე.setFont(შრიფტი_მნიშვნელობა);
                JFrame ფანჯარა = 화면.ფანჯარა("그래픽 შემოწმება", ტექსტის_არე, 800, 240);
                BufferedImage ნახატი_მნიშვნელობა_c143fe9e = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = ნახატი_მნიშვნელობა_c143fe9e.createGraphics();
                ფანჯარა.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(ნახატი_მნიშვნელობა_c143fe9e, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException შეცდომა) { throw new UncheckedIOException(შეცდომა); }
                ფანჯარა.dispose();
                გადამოწმება(ტექსტის_არე.getText().equals(ტექსტი), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
