// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Български.자바.*;
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
    interface стойност { long Четене(); }
    static class родител_стойност { protected long стойност = 42; }
    static class дете_стойност extends родител_стойност implements стойност { public long Четене() { return стойност; } }
    private static void проверявам(boolean условие, String Име) {
        if (!условие) throw new AssertionError(Име);
        System.out.println("PASS " + Име);
    }
    public static void main(String[] Параметри) throws Exception {
        String Текст = "한글 日本語 العربية हिन्दी 😀";
        Path хранилище_стойност = Path.of(System.getProperty("user.home"), "проверка_данни.txt");
        Файл.Писане(хранилище_стойност, Текст);
        проверявам(Файл.Четене(хранилище_стойност).equals(Текст), "UTF8_FILE");
        проверявам(문자.코드포인트수("한😀") == 2, "UNICODE");
        проверявам(문자.нормализирам_стойност("\u1100\u1161").equals("가"), "NORMALIZATION");
        стойност обект_стойност = new дете_стойност();
        проверявам(обект_стойност.Четене() == 42 && (long)дете_стойност.class.getMethod("Четене").invoke(обект_стойност) == 42, "OBJECT_INHERITANCE_REFLECTION");
        проверявам(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("проверка"); }
        catch (IOException изключение) { проверявам(изключение.getMessage().equals("проверка"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread нишка_стойност = 작업.Стартиране("한글 нишка_стойност", () -> 합.set(123));
        작업.기다리기(нишка_стойност);
        проверявам(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket сървър_стойност = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> отговор = 일꾼.submit(() -> {
                try (Socket 소켓 = сървър_стойност.accept()) {
                    BufferedReader Четене = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String ред;
                    while ((ред = Четене.readLine()) != null && !ред.isEmpty()) {}
                    byte[] основен_текст = 문자.кодирам(Текст);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + основен_текст.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(основен_текст);
                } catch (IOException ГРЕШКА) { throw new UncheckedIOException(ГРЕШКА); }
            });
            проверявам(통신.가져오기(URI.create("http://127.0.0.1:" + сървър_стойност.getLocalPort()), Duration.ofSeconds(30)).body().equals(Текст), "HTTP_TCP");
            отговор.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        проверявам(new ProcessBuilder("/bin/echo", "Процес_стойност").start().waitFor() == 0, "PROCESS");
        if (Параметри.length > 0 && Параметри[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font шрифт_стойност = new Font("Dialog", Font.PLAIN, 18);
                проверявам(шрифт_стойност.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                проверявам(шрифт_стойност.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea поле_за_редактиране = new JTextArea(Текст);
                поле_за_редактиране.setFont(шрифт_стойност);
                JFrame Прозорец = 화면.Прозорец("그래픽 проверка", поле_за_редактиране, 800, 240);
                BufferedImage чертеж_стойност = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = чертеж_стойност.createGraphics();
                Прозорец.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(чертеж_стойност, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ГРЕШКА) { throw new UncheckedIOException(ГРЕШКА); }
                Прозорец.dispose();
                проверявам(поле_за_редактиране.getText().equals(Текст), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
