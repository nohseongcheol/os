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
    interface мән { long Оқу(); }
    static class басты_мән { protected long мән = 42; }
    static class еншілес_элемент_мән extends басты_мән implements мән { public long Оқу() { return мән; } }
    private static void тексеру(boolean шарт, String Аты) {
        if (!шарт) throw new AssertionError(Аты);
        System.out.println("PASS " + Аты);
    }
    public static void main(String[] Аргументтер) throws Exception {
        String Мәтін = "한글 日本語 العربية हिन्दी 😀";
        Path сақтау_мән = Path.of(System.getProperty("user.home"), "тексерім_деректер.txt");
        Файл.Жазу(сақтау_мән, Мәтін);
        тексеру(Файл.Оқу(сақтау_мән).equals(Мәтін), "UTF8_FILE");
        тексеру(문자.코드포인트수("한😀") == 2, "UNICODE");
        тексеру(문자.нормалдау_мән("\u1100\u1161").equals("가"), "NORMALIZATION");
        мән нысан_мән = new еншілес_элемент_мән();
        тексеру(нысан_мән.Оқу() == 42 && (long)еншілес_элемент_мән.class.getMethod("Оқу").invoke(нысан_мән) == 42, "OBJECT_INHERITANCE_REFLECTION");
        тексеру(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("тексеру_5fb2b747"); }
        catch (IOException ерекшелік) { тексеру(ерекшелік.getMessage().equals("тексеру_5fb2b747"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread ағын_мән = 작업.Орындау_2("한글 ағын_мән", () -> 합.set(123));
        작업.기다리기(ағын_мән);
        тексеру(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket сервер_мән = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> жауап = 일꾼.submit(() -> {
                try (Socket 소켓 = сервер_мән.accept()) {
                    BufferedReader Оқу = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Жол;
                    while ((Жол = Оқу.readLine()) != null && !Жол.isEmpty()) {}
                    byte[] негізгі_мәтін = 문자.부호화(Мәтін);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + негізгі_мәтін.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(негізгі_мәтін);
                } catch (IOException Қате) { throw new UncheckedIOException(Қате); }
            });
            тексеру(통신.가져오기(URI.create("http://127.0.0.1:" + сервер_мән.getLocalPort()), Duration.ofSeconds(30)).body().equals(Мәтін), "HTTP_TCP");
            жауап.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        тексеру(new ProcessBuilder("/bin/echo", "Процесс_мән").start().waitFor() == 0, "PROCESS");
        if (Аргументтер.length > 0 && Аргументтер[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font қаріп_мән = new Font("Dialog", Font.PLAIN, 18);
                тексеру(қаріп_мән.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                тексеру(қаріп_мән.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea өңдеу_өрісі = new JTextArea(Мәтін);
                өңдеу_өрісі.setFont(қаріп_мән);
                JFrame Терезе = 화면.Терезе("그래픽 тексеру_5fb2b747", өңдеу_өрісі, 800, 240);
                BufferedImage сызба_мән = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = сызба_мән.createGraphics();
                Терезе.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(сызба_мән, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Қате) { throw new UncheckedIOException(Қате); }
                Терезе.dispose();
                тексеру(өңдеу_өрісі.getText().equals(Мәтін), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
