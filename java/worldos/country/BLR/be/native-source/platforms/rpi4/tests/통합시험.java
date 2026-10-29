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
    interface значэнне { long Чытанне(); }
    static class 부모 { protected long значэнне = 42; }
    static class дзіця_значэнне extends 부모 implements значэнне { public long Чытанне() { return значэнне; } }
    private static void праверыць(boolean умова, String Назва) {
        if (!умова) throw new AssertionError(Назва);
        System.out.println("PASS " + Назва);
    }
    public static void main(String[] 인수) throws Exception {
        String Тэкст = "한글 日本語 العربية हिन्दी 😀";
        Path сховішча_значэнне = Path.of(System.getProperty("user.home"), "праверка_дадзеныя.txt");
        Файл.Запіс(сховішча_значэнне, Тэкст);
        праверыць(Файл.Чытанне(сховішча_значэнне).equals(Тэкст), "UTF8_FILE");
        праверыць(문자.코드포인트수("한😀") == 2, "UNICODE");
        праверыць(문자.нармалізаваць_значэнне("\u1100\u1161").equals("가"), "NORMALIZATION");
        значэнне аб_ект_значэнне = new дзіця_значэнне();
        праверыць(аб_ект_значэнне.Чытанне() == 42 && (long)дзіця_значэнне.class.getMethod("Чытанне").invoke(аб_ект_значэнне) == 42, "OBJECT_INHERITANCE_REFLECTION");
        праверыць(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("праверыць_5fb2b747"); }
        catch (IOException выключэнне) { праверыць(выключэнне.getMessage().equals("праверыць_5fb2b747"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread паток_значэнне_5b72a632 = 작업.Выканаць("한글 паток_значэнне_5b72a632", () -> 합.set(123));
        작업.기다리기(паток_значэнне_5b72a632);
        праверыць(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket сервер_значэнне = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> адказаць = 일꾼.submit(() -> {
                try (Socket 소켓 = сервер_значэнне.accept()) {
                    BufferedReader Чытанне = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String лінія;
                    while ((лінія = Чытанне.readLine()) != null && !лінія.isEmpty()) {}
                    byte[] асноўны_тэкст = 문자.부호화(Тэкст);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + асноўны_тэкст.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(асноўны_тэкст);
                } catch (IOException ПАМЫЛКА) { throw new UncheckedIOException(ПАМЫЛКА); }
            });
            праверыць(통신.가져오기(URI.create("http://127.0.0.1:" + сервер_значэнне.getLocalPort()), Duration.ofSeconds(30)).body().equals(Тэкст), "HTTP_TCP");
            адказаць.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        праверыць(new ProcessBuilder("/bin/echo", "Працэс_значэнне").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font шрыфт_значэнне = new Font("Dialog", Font.PLAIN, 18);
                праверыць(шрыфт_значэнне.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                праверыць(шрыфт_значэнне.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea тэкставае_поле = new JTextArea(Тэкст);
                тэкставае_поле.setFont(шрыфт_значэнне);
                JFrame акно = 화면.акно("그래픽 праверыць_5fb2b747", тэкставае_поле, 800, 240);
                BufferedImage рукапісная_графіка_значэнне = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = рукапісная_графіка_значэнне.createGraphics();
                акно.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(рукапісная_графіка_значэнне, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ПАМЫЛКА) { throw new UncheckedIOException(ПАМЫЛКА); }
                акно.dispose();
                праверыць(тэкставае_поле.getText().equals(Тэкст), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
