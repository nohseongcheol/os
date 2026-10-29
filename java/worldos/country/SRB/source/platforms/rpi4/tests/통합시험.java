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
    interface вриједност { long Чита(); }
    static class родитељ_вриједност { protected long вриједност = 42; }
    static class дете_вриједност extends родитељ_вриједност implements вриједност { public long Чита() { return вриједност; } }
    private static void потврдити(boolean стање, String Назив) {
        if (!стање) throw new AssertionError(Назив);
        System.out.println("PASS " + Назив);
    }
    public static void main(String[] Аргументи) throws Exception {
        String Текст = "한글 日本語 العربية हिन्दी 😀";
        Path похранити_вриједност = Path.of(System.getProperty("user.home"), "провјера_подаци.txt");
        Датотека.Пише(похранити_вриједност, Текст);
        потврдити(Датотека.Чита(похранити_вриједност).equals(Текст), "UTF8_FILE");
        потврдити(문자.코드포인트수("한😀") == 2, "UNICODE");
        потврдити(문자.нормализовати_вриједност("\u1100\u1161").equals("가"), "NORMALIZATION");
        вриједност објекат_вриједност = new дете_вриједност();
        потврдити(објекат_вриједност.Чита() == 42 && (long)дете_вриједност.class.getMethod("Чита").invoke(објекат_вриједност) == 42, "OBJECT_INHERITANCE_REFLECTION");
        потврдити(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("потврдити_5fb2b747"); }
        catch (IOException изузетак) { потврдити(изузетак.getMessage().equals("потврдити_5fb2b747"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread нит_вриједност = 작업.Покрени("한글 нит_вриједност", () -> 합.set(123));
        작업.기다리기(нит_вриједност);
        потврдити(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket сервер_вриједност = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> одговор = 일꾼.submit(() -> {
                try (Socket 소켓 = сервер_вриједност.accept()) {
                    BufferedReader Чита = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Ред;
                    while ((Ред = Чита.readLine()) != null && !Ред.isEmpty()) {}
                    byte[] тело_текста = 문자.부호화(Текст);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + тело_текста.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(тело_текста);
                } catch (IOException ГРЕШКА) { throw new UncheckedIOException(ГРЕШКА); }
            });
            потврдити(통신.가져오기(URI.create("http://127.0.0.1:" + сервер_вриједност.getLocalPort()), Duration.ofSeconds(30)).body().equals(Текст), "HTTP_TCP");
            одговор.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        потврдити(new ProcessBuilder("/bin/echo", "Процес_вриједност").start().waitFor() == 0, "PROCESS");
        if (Аргументи.length > 0 && Аргументи[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font фонт_вриједност = new Font("Dialog", Font.PLAIN, 18);
                потврдити(фонт_вриједност.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                потврдити(фонт_вриједност.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea област_текста = new JTextArea(Текст);
                област_текста.setFont(фонт_вриједност);
                JFrame Прозор = 화면.Прозор("그래픽 потврдити_5fb2b747", област_текста, 800, 240);
                BufferedImage цртеж_вриједност = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = цртеж_вриједност.createGraphics();
                Прозор.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(цртеж_вриједност, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ГРЕШКА) { throw new UncheckedIOException(ГРЕШКА); }
                Прозор.dispose();
                потврдити(област_текста.getText().equals(Текст), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
