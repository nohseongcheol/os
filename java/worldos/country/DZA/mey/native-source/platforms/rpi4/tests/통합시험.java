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
    interface 값 { long 읽기(); }
    static class 부모 { protected long 값 = 42; }
    static class 자식 extends 부모 implements 값 { public long 읽기() { return 값; } }
    private static void 확인(boolean 조건, String 이름) {
        if (!조건) throw new AssertionError(이름);
        System.out.println("PASS " + 이름);
    }
    public static void main(String[] 인수) throws Exception {
        String 글 = "한글 日本語 العربية हिन्दी 😀";
        Path 저장 = Path.of(System.getProperty("user.home"), "검증자료.txt");
        파일.쓰기(저장, 글);
        확인(파일.읽기(저장).equals(글), "UTF8_FILE");
        확인(문자.코드포인트수("한😀") == 2, "UNICODE");
        확인(문자.정규화("\u1100\u1161").equals("가"), "NORMALIZATION");
        값 객체 = new 자식();
        확인(객체.읽기() == 42 && (long)자식.class.getMethod("읽기").invoke(객체) == 42, "OBJECT_INHERITANCE_REFLECTION");
        확인(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("검증"); }
        catch (IOException 예외) { 확인(예외.getMessage().equals("검증"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread 가닥 = 작업.시작("한글 가닥", () -> 합.set(123));
        작업.기다리기(가닥);
        확인(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket 서버 = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> 응답 = 일꾼.submit(() -> {
                try (Socket 소켓 = 서버.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String 줄;
                    while ((줄 = 읽기.readLine()) != null && !줄.isEmpty()) {}
                    byte[] 본문 = 문자.부호화(글);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + 본문.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(본문);
                } catch (IOException 오류) { throw new UncheckedIOException(오류); }
            });
            확인(통신.가져오기(URI.create("http://127.0.0.1:" + 서버.getLocalPort()), Duration.ofSeconds(30)).body().equals(글), "HTTP_TCP");
            응답.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        확인(new ProcessBuilder("/bin/echo", "과정").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font 글꼴 = new Font("Dialog", Font.PLAIN, 18);
                확인(글꼴.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                확인(글꼴.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea 글상자 = new JTextArea(글);
                글상자.setFont(글꼴);
                JFrame 창 = 화면.창("그래픽 검증", 글상자, 800, 240);
                BufferedImage 그림 = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = 그림.createGraphics();
                창.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(그림, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException 오류) { throw new UncheckedIOException(오류); }
                창.dispose();
                확인(글상자.getText().equals(글), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
