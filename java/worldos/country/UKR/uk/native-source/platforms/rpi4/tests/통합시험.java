// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import українська.자바.*;
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
    interface значення { long Читання(); }
    static class батьківський_значення { protected long значення = 42; }
    static class дитина_значення extends батьківський_значення implements значення { public long Читання() { return значення; } }
    private static void перевіряти(boolean умова, String Назва) {
        if (!умова) throw new AssertionError(Назва);
        System.out.println("PASS " + Назва);
    }
    public static void main(String[] аргументи) throws Exception {
        String текст = "한글 日本語 العربية हिन्दी 😀";
        Path сховище_значення = Path.of(System.getProperty("user.home"), "перевірка_дані.txt");
        файл.Запис(сховище_значення, текст);
        перевіряти(файл.Читання(сховище_значення).equals(текст), "UTF8_FILE");
        перевіряти(문자.코드포인트수("한😀") == 2, "UNICODE");
        перевіряти(문자.нормалізувати_значення("\u1100\u1161").equals("가"), "NORMALIZATION");
        значення об_єкт_значення = new дитина_значення();
        перевіряти(об_єкт_значення.Читання() == 42 && (long)дитина_значення.class.getMethod("Читання").invoke(об_єкт_значення) == 42, "OBJECT_INHERITANCE_REFLECTION");
        перевіряти(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("затвердити"); }
        catch (IOException виняток) { перевіряти(виняток.getMessage().equals("затвердити"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread потік_значення_5b72a632 = 작업.запустити("한글 потік_значення_5b72a632", () -> 합.set(123));
        작업.기다리기(потік_значення_5b72a632);
        перевіряти(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket сервер_значення = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> відповідь = 일꾼.submit(() -> {
                try (Socket сокет_значення = сервер_значення.accept()) {
                    BufferedReader Читання = new BufferedReader(new InputStreamReader(сокет_значення.getInputStream()));
                    String рядок_введення;
                    while ((рядок_введення = Читання.readLine()) != null && !рядок_введення.isEmpty()) {}
                    byte[] основний_текст = 문자.кодувати(текст);
                    сокет_значення.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + основний_текст.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    сокет_значення.getOutputStream().write(основний_текст);
                } catch (IOException ПОМИЛКА) { throw new UncheckedIOException(ПОМИЛКА); }
            });
            перевіряти(통신.가져오기(URI.create("http://127.0.0.1:" + сервер_значення.getLocalPort()), Duration.ofSeconds(30)).body().equals(текст), "HTTP_TCP");
            відповідь.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        перевіряти(new ProcessBuilder("/bin/echo", "процес_значення").start().waitFor() == 0, "PROCESS");
        if (аргументи.length > 0 && аргументи[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font шрифт_значення = new Font("Dialog", Font.PLAIN, 18);
                перевіряти(шрифт_значення.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                перевіряти(шрифт_значення.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea текстове_поле_d6e55852 = new JTextArea(текст);
                текстове_поле_d6e55852.setFont(шрифт_значення);
                JFrame Вікно = 화면.Вікно("그래픽 затвердити", текстове_поле_d6e55852, 800, 240);
                BufferedImage малювання_значення = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = малювання_значення.createGraphics();
                Вікно.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(малювання_значення, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ПОМИЛКА) { throw new UncheckedIOException(ПОМИЛКА); }
                Вікно.dispose();
                перевіряти(текстове_поле_d6e55852.getText().equals(текст), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
