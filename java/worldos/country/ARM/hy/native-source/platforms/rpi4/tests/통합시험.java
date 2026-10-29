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
    interface արժեք { long Ընթերցում(); }
    static class 부모 { protected long արժեք = 42; }
    static class երեխա_արժեք extends 부모 implements արժեք { public long Ընթերցում() { return արժեք; } }
    private static void հաստատել(boolean պայման, String Անուն) {
        if (!պայման) throw new AssertionError(Անուն);
        System.out.println("PASS " + Անուն);
    }
    public static void main(String[] 인수) throws Exception {
        String Տեքստ = "한글 日本語 العربية हिन्दी 😀";
        Path պահեստավորել_արժեք = Path.of(System.getProperty("user.home"), "վավերացում_տվյալ.txt");
        Ֆայլ.Գրել(պահեստավորել_արժեք, Տեքստ);
        հաստատել(Ֆայլ.Ընթերցում(պահեստավորել_արժեք).equals(Տեքստ), "UTF8_FILE");
        հաստատել(문자.코드포인트수("한😀") == 2, "UNICODE");
        հաստատել(문자.կարգավորել_արժեք("\u1100\u1161").equals("가"), "NORMALIZATION");
        արժեք առարկա_արժեք = new երեխա_արժեք();
        հաստատել(առարկա_արժեք.Ընթերցում() == 42 && (long)երեխա_արժեք.class.getMethod("Ընթերցում").invoke(առարկա_արժեք) == 42, "OBJECT_INHERITANCE_REFLECTION");
        հաստատել(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("վավերացնել"); }
        catch (IOException 예외) { հաստատել(예외.getMessage().equals("վավերացնել"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread շղթա_արժեք = 작업.Գործարկել("한글 շղթա_արժեք", () -> 합.set(123));
        작업.기다리기(շղթա_արժեք);
        հաստատել(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket սպասարկիչ_արժեք = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> պատասխանել = 일꾼.submit(() -> {
                try (Socket 소켓 = սպասարկիչ_արժեք.accept()) {
                    BufferedReader Ընթերցում = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String կապ;
                    while ((կապ = Ընթերցում.readLine()) != null && !կապ.isEmpty()) {}
                    byte[] հիմնական_գրվածք = 문자.부호화(Տեքստ);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + հիմնական_գրվածք.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(հիմնական_գրվածք);
                } catch (IOException Սխալ) { throw new UncheckedIOException(Սխալ); }
            });
            հաստատել(통신.가져오기(URI.create("http://127.0.0.1:" + սպասարկիչ_արժեք.getLocalPort()), Duration.ofSeconds(30)).body().equals(Տեքստ), "HTTP_TCP");
            պատասխանել.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        հաստատել(new ProcessBuilder("/bin/echo", "Ընթացք_արժեք").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font տառատեսակ_արժեք = new Font("Dialog", Font.PLAIN, 18);
                հաստատել(տառատեսակ_արժեք.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                հաստատել(տառատեսակ_արժեք.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea գրվածքի_տուփ = new JTextArea(Տեքստ);
                գրվածքի_տուփ.setFont(տառատեսակ_արժեք);
                JFrame պատուհան = 화면.պատուհան("그래픽 վավերացնել", գրվածքի_տուփ, 800, 240);
                BufferedImage նկար_արժեք_c143fe9e = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = նկար_արժեք_c143fe9e.createGraphics();
                պատուհան.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(նկար_արժեք_c143fe9e, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Սխալ) { throw new UncheckedIOException(Սխալ); }
                պատուհան.dispose();
                հաստատել(գրվածքի_տուփ.getText().equals(Տեքստ), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
