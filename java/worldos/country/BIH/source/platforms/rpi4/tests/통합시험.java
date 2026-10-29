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
    interface вриједност { long 읽기(); }
    static class 부모 { protected long вриједност = 42; }
    static class дијете_вриједност extends 부모 implements вриједност { public long 읽기() { return вриједност; } }
    private static void потврдити(boolean увјет, String назив) {
        if (!увјет) throw new AssertionError(назив);
        System.out.println("PASS " + назив);
    }
    public static void main(String[] 인수) throws Exception {
        String текст = "한글 日本語 العربية हिन्दी 😀";
        Path похранити_вриједност = Path.of(System.getProperty("user.home"), "провјера_подаци.txt");
        фајл.писати(похранити_вриједност, текст);
        потврдити(фајл.읽기(похранити_вриједност).equals(текст), "UTF8_FILE");
        потврдити(문자.코드포인트수("한😀") == 2, "UNICODE");
        потврдити(문자.нормализирати_вриједност("\u1100\u1161").equals("가"), "NORMALIZATION");
        вриједност објект_вриједност = new дијете_вриједност();
        потврдити(објект_вриједност.읽기() == 42 && (long)дијете_вриједност.class.getMethod("읽기").invoke(објект_вриједност) == 42, "OBJECT_INHERITANCE_REFLECTION");
        потврдити(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("овјерити"); }
        catch (IOException 예외) { потврдити(예외.getMessage().equals("овјерити"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread нит_вриједност = 작업.시작("한글 нит_вриједност", () -> 합.set(123));
        작업.기다리기(нит_вриједност);
        потврдити(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket сервер_вриједност = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> 응답 = 일꾼.submit(() -> {
                try (Socket 소켓 = сервер_вриједност.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String редак;
                    while ((редак = 읽기.readLine()) != null && !редак.isEmpty()) {}
                    byte[] Тијело_текста = 문자.부호화(текст);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + Тијело_текста.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(Тијело_текста);
                } catch (IOException грешка) { throw new UncheckedIOException(грешка); }
            });
            потврдити(통신.가져오기(URI.create("http://127.0.0.1:" + сервер_вриједност.getLocalPort()), Duration.ofSeconds(30)).body().equals(текст), "HTTP_TCP");
            응답.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        потврдити(new ProcessBuilder("/bin/echo", "процес_вриједност").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font фонт_вриједност = new Font("Dialog", Font.PLAIN, 18);
                потврдити(фонт_вриједност.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                потврдити(фонт_вриједност.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea 글상자 = new JTextArea(текст);
                글상자.setFont(фонт_вриједност);
                JFrame прозор = 화면.прозор("그래픽 овјерити", 글상자, 800, 240);
                BufferedImage уцртавање_вриједност = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = уцртавање_вриједност.createGraphics();
                прозор.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(уцртавање_вриједност, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException грешка) { throw new UncheckedIOException(грешка); }
                прозор.dispose();
                потврдити(글상자.getText().equals(текст), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
