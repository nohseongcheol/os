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
    interface маани { long Окуу(); }
    static class 부모 { protected long маани = 42; }
    static class бала_маани extends 부모 implements маани { public long Окуу() { return маани; } }
    private static void тууралыгын_аныктоо(boolean шарт, String Аты) {
        if (!шарт) throw new AssertionError(Аты);
        System.out.println("PASS " + Аты);
    }
    public static void main(String[] 인수) throws Exception {
        String Текст = "한글 日本語 العربية हिन्दी 😀";
        Path сактагыч_маани = Path.of(System.getProperty("user.home"), "ырастоо_берилмелер.txt");
        Файл.Жазуу(сактагыч_маани, Текст);
        тууралыгын_аныктоо(Файл.Окуу(сактагыч_маани).equals(Текст), "UTF8_FILE");
        тууралыгын_аныктоо(문자.코드포인트수("한😀") == 2, "UNICODE");
        тууралыгын_аныктоо(문자.нормалдаштыруу_маани("\u1100\u1161").equals("가"), "NORMALIZATION");
        маани объект_маани = new бала_маани();
        тууралыгын_аныктоо(объект_маани.Окуу() == 42 && (long)бала_маани.class.getMethod("Окуу").invoke(объект_маани) == 42, "OBJECT_INHERITANCE_REFLECTION");
        тууралыгын_аныктоо(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("жарактуулугун_текшерүү"); }
        catch (IOException 예외) { тууралыгын_аныктоо(예외.getMessage().equals("жарактуулугун_текшерүү"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread трэд_маани = 작업.Жүргүзүү("한글 трэд_маани", () -> 합.set(123));
        작업.기다리기(трэд_маани);
        тууралыгын_аныктоо(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket сервер_маани = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> жооп_берүү = 일꾼.submit(() -> {
                try (Socket 소켓 = сервер_маани.accept()) {
                    BufferedReader Окуу = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String сап;
                    while ((сап = Окуу.readLine()) != null && !сап.isEmpty()) {}
                    byte[] негизги_текст = 문자.부호화(Текст);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + негизги_текст.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(негизги_текст);
                } catch (IOException Ката) { throw new UncheckedIOException(Ката); }
            });
            тууралыгын_аныктоо(통신.가져오기(URI.create("http://127.0.0.1:" + сервер_маани.getLocalPort()), Duration.ofSeconds(30)).body().equals(Текст), "HTTP_TCP");
            жооп_берүү.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        тууралыгын_аныктоо(new ProcessBuilder("/bin/echo", "Процесс_маани").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font арип_маани = new Font("Dialog", Font.PLAIN, 18);
                тууралыгын_аныктоо(арип_маани.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                тууралыгын_аныктоо(арип_маани.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea текст_аймагы = new JTextArea(Текст);
                текст_аймагы.setFont(арип_маани);
                JFrame терезе = 화면.терезе("그래픽 жарактуулугун_текшерүү", текст_аймагы, 800, 240);
                BufferedImage чийүү_маани = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = чийүү_маани.createGraphics();
                терезе.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(чийүү_маани, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Ката) { throw new UncheckedIOException(Ката); }
                терезе.dispose();
                тууралыгын_аныктоо(текст_аймагы.getText().equals(Текст), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
