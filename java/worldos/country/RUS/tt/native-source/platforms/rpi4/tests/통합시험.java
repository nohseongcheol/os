// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Татарча.자바.*;
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
    interface VALUE { long 읽기(); }
    static class 부모 { protected long VALUE = 42; }
    static class бала_VALUE extends 부모 implements VALUE { public long 읽기() { return VALUE; } }
    private static void раслау(boolean шарт, String исем) {
        if (!шарт) throw new AssertionError(исем);
        System.out.println("PASS " + исем);
    }
    public static void main(String[] 인수) throws Exception {
        String Mäten = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "раслау_мәгълүмат.txt");
        Birem.язу(Store_VALUE, Mäten);
        раслау(Birem.읽기(Store_VALUE).equals(Mäten), "UTF8_FILE");
        раслау(문자.символ_коды_COUNT("한😀") == 2, "UNICODE");
        раслау(문자.нормальләштерү_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE объект_VALUE = new бала_VALUE();
        раслау(объект_VALUE.읽기() == 42 && (long)бала_VALUE.class.getMethod("읽기").invoke(объект_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        раслау(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("тикшерү"); }
        catch (IOException 예외) { раслау(예외.getMessage().equals("тикшерү"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread агым_VALUE_5b72a632 = 작업.эшләтү("한글 агым_VALUE_5b72a632", () -> SUM_VALUE.set(123));
        작업.기다리기(агым_VALUE_5b72a632);
        раслау(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket сервер_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> җавап_бирү = 일꾼.submit(() -> {
                try (Socket 소켓 = сервер_VALUE.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String юл;
                    while ((юл = 읽기.readLine()) != null && !юл.isEmpty()) {}
                    byte[] төп_текст = 문자.부호화(Mäten);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + төп_текст.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(төп_текст);
                } catch (IOException Хата) { throw new UncheckedIOException(Хата); }
            });
            раслау(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + сервер_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Mäten), "HTTP_TCP");
            җавап_бирү.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        раслау(new ProcessBuilder("/bin/echo", "Процесс_VALUE").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font шрифт_VALUE = new Font("Dialog", Font.PLAIN, 18);
                раслау(шрифт_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                раслау(шрифт_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea текст_кыры_d6e55852 = new JTextArea(Mäten);
                текст_кыры_d6e55852.setFont(шрифт_VALUE);
                JFrame тәрәз = 화면.тәрәз("그래픽 тикшерү", текст_кыры_d6e55852, 800, 240);
                BufferedImage сызым_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = сызым_VALUE.createGraphics();
                тәрәз.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(сызым_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Хата) { throw new UncheckedIOException(Хата); }
                тәрәз.dispose();
                раслау(текст_кыры_d6e55852.getText().equals(Mäten), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
