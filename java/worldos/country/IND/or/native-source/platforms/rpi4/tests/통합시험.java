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
    interface ମୂଲ୍ୟ { long ପଢନ୍ତୁ(); }
    static class 부모 { protected long ମୂଲ୍ୟ = 42; }
    static class ଶିଶୁ_ମୂଲ୍ୟ extends 부모 implements ମୂଲ୍ୟ { public long ପଢନ୍ତୁ() { return ମୂଲ୍ୟ; } }
    private static void ଯାଞ୍ଚ୍_କରିବା(boolean ସର୍ତ୍ତ, String ନାମ) {
        if (!ସର୍ତ୍ତ) throw new AssertionError(ନାମ);
        System.out.println("PASS " + ନାମ);
    }
    public static void main(String[] 인수) throws Exception {
        String ପାଠ୍ଯ = "한글 日本語 العربية हिन्दी 😀";
        Path ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ = Path.of(System.getProperty("user.home"), "ବୈଧକରଣ_ଡାଟା.txt");
        ଫାଇଲ.ଲେଖନ୍ତୁ(ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ, ପାଠ୍ଯ);
        ଯାଞ୍ଚ୍_କରିବା(ଫାଇଲ.ପଢନ୍ତୁ(ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ).equals(ପାଠ୍ଯ), "UTF8_FILE");
        ଯାଞ୍ଚ୍_କରିବା(문자.코드포인트수("한😀") == 2, "UNICODE");
        ଯାଞ୍ଚ୍_କରିବା(문자.ସ୍ୱାଭାବିକ_ମୂଲ୍ୟ("\u1100\u1161").equals("가"), "NORMALIZATION");
        ମୂଲ୍ୟ ଅବଜେକ୍ଟ_ମୂଲ୍ୟ = new ଶିଶୁ_ମୂଲ୍ୟ();
        ଯାଞ୍ଚ୍_କରିବା(ଅବଜେକ୍ଟ_ମୂଲ୍ୟ.ପଢନ୍ତୁ() == 42 && (long)ଶିଶୁ_ମୂଲ୍ୟ.class.getMethod("ପଢନ୍ତୁ").invoke(ଅବଜେକ୍ଟ_ମୂଲ୍ୟ) == 42, "OBJECT_INHERITANCE_REFLECTION");
        ଯାଞ୍ଚ୍_କରିବା(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("ବୈଧକରଣ"); }
        catch (IOException ବ୍ୟତିକ୍ରମ) { ଯାଞ୍ଚ୍_କରିବା(ବ୍ୟତିକ୍ରମ.getMessage().equals("ବୈଧକରଣ"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread ଧାରା_ମୂଲ୍ୟ = 작업.ଚଳାନ୍ତୁ("한글 ଧାରା_ମୂଲ୍ୟ", () -> 합.set(123));
        작업.기다리기(ଧାରା_ମୂଲ୍ୟ);
        ଯାଞ୍ଚ୍_କରିବା(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket ସର୍ଭର୍_ମୂଲ୍ୟ = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ = 일꾼.submit(() -> {
                try (Socket 소켓 = ସର୍ଭର୍_ମୂଲ୍ୟ.accept()) {
                    BufferedReader ପଢନ୍ତୁ = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String ରେଖା;
                    while ((ରେଖା = ପଢନ୍ତୁ.readLine()) != null && !ରେଖା.isEmpty()) {}
                    byte[] ମୂଳ_ପାଠ = 문자.부호화(ପାଠ୍ଯ);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + ମୂଳ_ପାଠ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(ମୂଳ_ପାଠ);
                } catch (IOException ତ୍ରୁଟି) { throw new UncheckedIOException(ତ୍ରୁଟି); }
            });
            ଯାଞ୍ଚ୍_କରିବା(통신.가져오기(URI.create("http://127.0.0.1:" + ସର୍ଭର୍_ମୂଲ୍ୟ.getLocalPort()), Duration.ofSeconds(30)).body().equals(ପାଠ୍ଯ), "HTTP_TCP");
            ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        ଯାଞ୍ଚ୍_କରିବା(new ProcessBuilder("/bin/echo", "ପ୍ରୋସେସ୍_ମୂଲ୍ୟ").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ଫଣ୍ଟ_ମୂଲ୍ୟ = new Font("Dialog", Font.PLAIN, 18);
                ଯାଞ୍ଚ୍_କରିବା(ଫଣ୍ଟ_ମୂଲ୍ୟ.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                ଯାଞ୍ଚ୍_କରିବା(ଫଣ୍ଟ_ମୂଲ୍ୟ.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea ପାଠ୍ୟ_ବାକ୍ସ = new JTextArea(ପାଠ୍ଯ);
                ପାଠ୍ୟ_ବାକ୍ସ.setFont(ଫଣ୍ଟ_ମୂଲ୍ୟ);
                JFrame ଓ୍ୱିଣ୍ଡୋ = 화면.ଓ୍ୱିଣ୍ଡୋ("그래픽 ବୈଧକରଣ", ପାଠ୍ୟ_ବାକ୍ସ, 800, 240);
                BufferedImage ଅଙ୍କନ_ମୂଲ୍ୟ = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = ଅଙ୍କନ_ମୂଲ୍ୟ.createGraphics();
                ଓ୍ୱିଣ୍ଡୋ.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(ଅଙ୍କନ_ମୂଲ୍ୟ, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ତ୍ରୁଟି) { throw new UncheckedIOException(ତ୍ରୁଟି); }
                ଓ୍ୱିଣ୍ଡୋ.dispose();
                ଯାଞ୍ଚ୍_କରିବା(ପାଠ୍ୟ_ବାକ୍ସ.getText().equals(ପାଠ୍ଯ), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
