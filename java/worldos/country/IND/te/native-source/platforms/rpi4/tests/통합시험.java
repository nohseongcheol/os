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
    interface మూల్యం { long చదువు(); }
    static class 부모 { protected long మూల్యం = 42; }
    static class ఉపాంశం_మూల్యం extends 부모 implements మూల్యం { public long చదువు() { return మూల్యం; } }
    private static void సరిచూడు(boolean నిబంధన, String పేరు) {
        if (!నిబంధన) throw new AssertionError(పేరు);
        System.out.println("PASS " + పేరు);
    }
    public static void main(String[] 인수) throws Exception {
        String పాఠ్యము = "한글 日本語 العربية हिन्दी 😀";
        Path నిల్వ_మూల్యం = Path.of(System.getProperty("user.home"), "నిర్ధారణ_డేటా.txt");
        దస్త్రం.వ్రాయుము(నిల్వ_మూల్యం, పాఠ్యము);
        సరిచూడు(దస్త్రం.చదువు(నిల్వ_మూల్యం).equals(పాఠ్యము), "UTF8_FILE");
        సరిచూడు(문자.코드포인트수("한😀") == 2, "UNICODE");
        సరిచూడు(문자.సాధారణీకరించు_మూల్యం("\u1100\u1161").equals("가"), "NORMALIZATION");
        మూల్యం అంశం_మూల్యం = new ఉపాంశం_మూల్యం();
        సరిచూడు(అంశం_మూల్యం.చదువు() == 42 && (long)ఉపాంశం_మూల్యం.class.getMethod("చదువు").invoke(అంశం_మూల్యం) == 42, "OBJECT_INHERITANCE_REFLECTION");
        సరిచూడు(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("నిర్థారీకరించు"); }
        catch (IOException మినహాయింపు) { సరిచూడు(మినహాయింపు.getMessage().equals("నిర్థారీకరించు"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread థ్రెడ్_మూల్యం = 작업.నడుపుము("한글 థ్రెడ్_మూల్యం", () -> 합.set(123));
        작업.기다리기(థ్రెడ్_మూల్యం);
        సరిచూడు(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket సర్వర్_మూల్యం = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> ప్రత్యుత్తరం_ఇవ్వు = 일꾼.submit(() -> {
                try (Socket 소켓 = సర్వర్_మూల్యం.accept()) {
                    BufferedReader చదువు = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String పంక్తి;
                    while ((పంక్తి = చదువు.readLine()) != null && !పంక్తి.isEmpty()) {}
                    byte[] ప్రధాన_పాఠం = 문자.부호화(పాఠ్యము);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + ప్రధాన_పాఠం.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(ప్రధాన_పాఠం);
                } catch (IOException దోషం) { throw new UncheckedIOException(దోషం); }
            });
            సరిచూడు(통신.가져오기(URI.create("http://127.0.0.1:" + సర్వర్_మూల్యం.getLocalPort()), Duration.ofSeconds(30)).body().equals(పాఠ్యము), "HTTP_TCP");
            ప్రత్యుత్తరం_ఇవ్వు.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        సరిచూడు(new ProcessBuilder("/bin/echo", "విధానం_మూల్యం").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font అక్షరాకృతి_మూల్యం = new Font("Dialog", Font.PLAIN, 18);
                సరిచూడు(అక్షరాకృతి_మూల్యం.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                సరిచూడు(అక్షరాకృతి_మూల్యం.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea టెక్స్ట్_బాక్స్ = new JTextArea(పాఠ్యము);
                టెక్స్ట్_బాక్స్.setFont(అక్షరాకృతి_మూల్యం);
                JFrame విండో = 화면.విండో("그래픽 నిర్థారీకరించు", టెక్స్ట్_బాక్స్, 800, 240);
                BufferedImage రేఖాచిత్రణ_మూల్యం = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = రేఖాచిత్రణ_మూల్యం.createGraphics();
                విండో.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(రేఖాచిత్రణ_మూల్యం, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException దోషం) { throw new UncheckedIOException(దోషం); }
                విండో.dispose();
                సరిచూడు(టెక్స్ట్_బాక్స్.getText().equals(పాఠ్యము), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
