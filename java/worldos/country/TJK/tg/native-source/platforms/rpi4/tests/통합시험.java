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
    interface қимат { long Хондан(); }
    static class 부모 { protected long қимат = 42; }
    static class кӯдак_қимат extends 부모 implements қимат { public long Хондан() { return қимат; } }
    private static void тасдиқ_кардан(boolean шарт, String Ном) {
        if (!шарт) throw new AssertionError(Ном);
        System.out.println("PASS " + Ном);
    }
    public static void main(String[] 인수) throws Exception {
        String Матн = "한글 日本語 العربية हिन्दी 😀";
        Path ҳифз_кардан_қимат = Path.of(System.getProperty("user.home"), "санҷиши_эътибор_иттилоот.txt");
        Файл.Навиштан(ҳифз_кардан_қимат, Матн);
        тасдиқ_кардан(Файл.Хондан(ҳифз_кардан_қимат).equals(Матн), "UTF8_FILE");
        тасдиқ_кардан(문자.코드포인트수("한😀") == 2, "UNICODE");
        тасдиқ_кардан(문자.ба_тартиб_даровардан_қимат("\u1100\u1161").equals("가"), "NORMALIZATION");
        қимат объект_қимат = new кӯдак_қимат();
        тасдиқ_кардан(объект_қимат.Хондан() == 42 && (long)кӯдак_қимат.class.getMethod("Хондан").invoke(объект_қимат) == 42, "OBJECT_INHERITANCE_REFLECTION");
        тасдиқ_кардан(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("санҷидани_эътибор"); }
        catch (IOException 예외) { тасдиқ_кардан(예외.getMessage().equals("санҷидани_эътибор"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread ришта_қимат = 작업.порча("한글 ришта_қимат", () -> 합.set(123));
        작업.기다리기(ришта_қимат);
        тасдиқ_кардан(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket сервер_қимат = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> ҷавоб_додан = 일꾼.submit(() -> {
                try (Socket 소켓 = сервер_қимат.accept()) {
                    BufferedReader Хондан = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String хат;
                    while ((хат = Хондан.readLine()) != null && !хат.isEmpty()) {}
                    byte[] матни_асосӣ = 문자.부호화(Матн);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + матни_асосӣ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(матни_асосӣ);
                } catch (IOException Хато) { throw new UncheckedIOException(Хато); }
            });
            тасдиқ_кардан(통신.가져오기(URI.create("http://127.0.0.1:" + сервер_қимат.getLocalPort()), Duration.ofSeconds(30)).body().equals(Матн), "HTTP_TCP");
            ҷавоб_додан.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        тасдиқ_кардан(new ProcessBuilder("/bin/echo", "Раванд_қимат").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font шрифт_қимат = new Font("Dialog", Font.PLAIN, 18);
                тасдиқ_кардан(шрифт_қимат.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                тасдиқ_кардан(шрифт_қимат.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea қитъаи_матн = new JTextArea(Матн);
                қитъаи_матн.setFont(шрифт_қимат);
                JFrame равзана = 화면.равзана("그래픽 санҷидани_эътибор", қитъаи_матн, 800, 240);
                BufferedImage нақша_қимат = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = нақша_қимат.createGraphics();
                равзана.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(нақша_қимат, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Хато) { throw new UncheckedIOException(Хато); }
                равзана.dispose();
                тасдиқ_кардан(қитъаи_матн.getText().equals(Матн), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
