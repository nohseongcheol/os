// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import русский.자바.*;
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

public class тест_интеграция {
    interface ЗНАЧЕН { long Чтение(); }
    static class родительский_ЗНАЧЕН { protected long ЗНАЧЕН = 42; }
    static class ребенок_ЗНАЧЕН extends родительский_ЗНАЧЕН implements ЗНАЧЕН { public long Чтение() { return ЗНАЧЕН; } }
    private static void проверять(boolean условие, String Название) {
        if (!условие) throw new AssertionError(Название);
        System.out.println("PASS " + Название);
    }
    public static void main(String[] аргументы) throws Exception {
        String текст = "한글 日本語 العربية हिन्दी 😀";
        Path Store_ЗНАЧЕН = Path.of(System.getProperty("user.home"), "проверка_данные.txt");
        файл.Запись(Store_ЗНАЧЕН, текст);
        проверять(файл.Чтение(Store_ЗНАЧЕН).equals(текст), "UTF8_FILE");
        проверять(문자.код_знака_СЧЁТ("한😀") == 2, "UNICODE");
        проверять(문자.нормализовать_ЗНАЧЕН("\u1100\u1161").equals("가"), "NORMALIZATION");
        ЗНАЧЕН объект_ЗНАЧЕН = new ребенок_ЗНАЧЕН();
        проверять(объект_ЗНАЧЕН.Чтение() == 42 && (long)ребенок_ЗНАЧЕН.class.getMethod("Чтение").invoke(объект_ЗНАЧЕН) == 42, "OBJECT_INHERITANCE_REFLECTION");
        проверять(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("проверить"); }
        catch (IOException исключение) { проверять(исключение.getMessage().equals("проверить"), "EXCEPTION"); }
        AtomicInteger SUM_ЗНАЧЕН = new AtomicInteger();
        Thread поток_ЗНАЧЕН_5b72a632 = 작업.запустить("한글 поток_ЗНАЧЕН_5b72a632", () -> SUM_ЗНАЧЕН.set(123));
        작업.기다리기(поток_ЗНАЧЕН_5b72a632);
        проверять(SUM_ЗНАЧЕН.get() == 123, "THREAD");
        ExecutorService работник_ЗНАЧЕН = Executors.newSingleThreadExecutor();
        try (ServerSocket сервер_ЗНАЧЕН = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> ответ = работник_ЗНАЧЕН.submit(() -> {
                try (Socket сокет_ЗНАЧЕН = сервер_ЗНАЧЕН.accept()) {
                    BufferedReader Чтение = new BufferedReader(new InputStreamReader(сокет_ЗНАЧЕН.getInputStream()));
                    String строка_ввода;
                    while ((строка_ввода = Чтение.readLine()) != null && !строка_ввода.isEmpty()) {}
                    byte[] основной_текст = 문자.кодировать(текст);
                    сокет_ЗНАЧЕН.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + основной_текст.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    сокет_ЗНАЧЕН.getOutputStream().write(основной_текст);
                } catch (IOException ошибка) { throw new UncheckedIOException(ошибка); }
            });
            проверять(коммуникация.ВЗЯТЬ_ЗНАЧЕН(URI.create("http://127.0.0.1:" + сервер_ЗНАЧЕН.getLocalPort()), Duration.ofSeconds(30)).body().equals(текст), "HTTP_TCP");
            ответ.get(30, TimeUnit.SECONDS);
        } finally { работник_ЗНАЧЕН.shutdownNow(); }
        проверять(new ProcessBuilder("/bin/echo", "Процесс_ЗНАЧЕН").start().waitFor() == 0, "PROCESS");
        if (аргументы.length > 0 && аргументы[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font шрифт_ЗНАЧЕН = new Font("Dialog", Font.PLAIN, 18);
                проверять(шрифт_ЗНАЧЕН.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                проверять(шрифт_ЗНАЧЕН.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea поле_ввода = new JTextArea(текст);
                поле_ввода.setFont(шрифт_ЗНАЧЕН);
                JFrame Окно = экран.Окно("그래픽 проверить", поле_ввода, 800, 240);
                BufferedImage рисунок_ЗНАЧЕН = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D кисть_ЗНАЧЕН = рисунок_ЗНАЧЕН.createGraphics();
                Окно.paint(кисть_ЗНАЧЕН); кисть_ЗНАЧЕН.dispose();
                try { javax.imageio.ImageIO.write(рисунок_ЗНАЧЕН, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ошибка) { throw new UncheckedIOException(ошибка); }
                Окно.dispose();
                проверять(поле_ввода.getText().equals(текст), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
