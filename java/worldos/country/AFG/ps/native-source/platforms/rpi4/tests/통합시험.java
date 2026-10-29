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
    interface ارزښت { long لوستل(); }
    static class 부모 { protected long ارزښت = 42; }
    static class زوی_توکی_ارزښت extends 부모 implements ارزښت { public long لوستل() { return ارزښت; } }
    private static void 확인(boolean آړ, String نوم) {
        if (!آړ) throw new AssertionError(نوم);
        System.out.println("PASS " + نوم);
    }
    public static void main(String[] 인수) throws Exception {
        String ليکنه = "한글 日本語 العربية हिन्दी 😀";
        Path 저장 = Path.of(System.getProperty("user.home"), "باورکړن_اومتوک.txt");
        دوتنه.لوستل_2(저장, ليکنه);
        확인(دوتنه.لوستل(저장).equals(ليکنه), "UTF8_FILE");
        확인(문자.코드포인트수("한😀") == 2, "UNICODE");
        확인(문자.لیوی_کول_ارزښت("\u1100\u1161").equals("가"), "NORMALIZATION");
        ارزښت 객체 = new زوی_توکی_ارزښت();
        확인(객체.لوستل() == 42 && (long)زوی_توکی_ارزښت.class.getMethod("لوستل").invoke(객체) == 42, "OBJECT_INHERITANCE_REFLECTION");
        확인(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("검증"); }
        catch (IOException 예외) { 확인(예외.getMessage().equals("검증"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread مزى_ارزښت = 작업.ځغلول("한글 مزى_ارزښت", () -> 합.set(123));
        작업.기다리기(مزى_ارزښت);
        확인(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket 서버 = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> 응답 = 일꾼.submit(() -> {
                try (Socket 소켓 = 서버.accept()) {
                    BufferedReader لوستل = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String ليکه;
                    while ((ليکه = لوستل.readLine()) != null && !ليکه.isEmpty()) {}
                    byte[] تنه_متن = 문자.부호화(ليکنه);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + تنه_متن.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(تنه_متن);
                } catch (IOException تېروتنه) { throw new UncheckedIOException(تېروتنه); }
            });
            확인(통신.가져오기(URI.create("http://127.0.0.1:" + 서버.getLocalPort()), Duration.ofSeconds(30)).body().equals(ليکنه), "HTTP_TCP");
            응답.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        확인(new ProcessBuilder("/bin/echo", "과정").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ليکبڼه_ارزښت = new Font("Dialog", Font.PLAIN, 18);
                확인(ليکبڼه_ارزښت.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                확인(ليکبڼه_ارزښت.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea 글상자 = new JTextArea(ليکنه);
                글상자.setFont(ليکبڼه_ارزښت);
                JFrame کړکۍ = 화면.کړکۍ("그래픽 검증", 글상자, 800, 240);
                BufferedImage 그림 = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = 그림.createGraphics();
                کړکۍ.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(그림, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException تېروتنه) { throw new UncheckedIOException(تېروتنه); }
                کړکۍ.dispose();
                확인(글상자.getText().equals(ليکنه), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
