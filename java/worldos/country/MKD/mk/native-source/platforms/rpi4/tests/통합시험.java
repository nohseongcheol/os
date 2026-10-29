// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Македонски.자바.*;
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
    interface VALUE { long Читај(); }
    static class 부모 { protected long VALUE = 42; }
    static class дете_VALUE extends 부모 implements VALUE { public long Читај() { return VALUE; } }
    private static void провери(boolean услов, String Име) {
        if (!услов) throw new AssertionError(Име);
        System.out.println("PASS " + Име);
    }
    public static void main(String[] Аргументи) throws Exception {
        String Текст = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "проверка_податоци.txt");
        Датотека.Запиши(Store_VALUE, Текст);
        провери(Датотека.Читај(Store_VALUE).equals(Текст), "UTF8_FILE");
        провери(문자.кодна_точка_COUNT("한😀") == 2, "UNICODE");
        провери(문자.нормализирање_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE објект_VALUE = new дете_VALUE();
        провери(објект_VALUE.Читај() == 42 && (long)дете_VALUE.class.getMethod("Читај").invoke(објект_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        провери(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("потврди"); }
        catch (IOException исклучок) { провери(исклучок.getMessage().equals("потврди"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread нишка_VALUE = 작업.Изврши_2("한글 нишка_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(нишка_VALUE);
        провери(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket сервер_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> одговори = 일꾼.submit(() -> {
                try (Socket 소켓 = сервер_VALUE.accept()) {
                    BufferedReader Читај = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String ред;
                    while ((ред = Читај.readLine()) != null && !ред.isEmpty()) {}
                    byte[] основен_текст = 문자.부호화(Текст);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + основен_текст.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(основен_текст);
                } catch (IOException ГРЕШКА) { throw new UncheckedIOException(ГРЕШКА); }
            });
            провери(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + сервер_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Текст), "HTTP_TCP");
            одговори.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        провери(new ProcessBuilder("/bin/echo", "Процес_VALUE").start().waitFor() == 0, "PROCESS");
        if (Аргументи.length > 0 && Аргументи[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font фонт_VALUE = new Font("Dialog", Font.PLAIN, 18);
                провери(фонт_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                провери(фонт_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea област_со_текст = new JTextArea(Текст);
                област_со_текст.setFont(фонт_VALUE);
                JFrame прозорец = 화면.прозорец("그래픽 потврди", област_со_текст, 800, 240);
                BufferedImage цртеж_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = цртеж_VALUE.createGraphics();
                прозорец.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(цртеж_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ГРЕШКА) { throw new UncheckedIOException(ГРЕШКА); }
                прозорец.dispose();
                провери(област_со_текст.getText().equals(Текст), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
