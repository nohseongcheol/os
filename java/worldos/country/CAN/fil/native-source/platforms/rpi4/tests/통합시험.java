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
    interface VALUE { long 읽기(); }
    static class 부모 { protected long VALUE = 42; }
    static class anak_VALUE extends 부모 implements VALUE { public long 읽기() { return VALUE; } }
    private static void tiyakin_kumpirmahin(boolean kondisyon, String pangalan) {
        if (!kondisyon) throw new AssertionError(pangalan);
        System.out.println("PASS " + pangalan);
    }
    public static void main(String[] 인수) throws Exception {
        String SMS = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "pagpapatibay_data.txt");
        file.sumulat(Store_VALUE, SMS);
        tiyakin_kumpirmahin(file.읽기(Store_VALUE).equals(SMS), "UTF8_FILE");
        tiyakin_kumpirmahin(문자.character_code_COUNT("한😀") == 2, "UNICODE");
        tiyakin_kumpirmahin(문자.normalisahin_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE bagay_VALUE = new anak_VALUE();
        tiyakin_kumpirmahin(bagay_VALUE.읽기() == 42 && (long)anak_VALUE.class.getMethod("읽기").invoke(bagay_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        tiyakin_kumpirmahin(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("patunayan"); }
        catch (IOException pagbubukod) { tiyakin_kumpirmahin(pagbubukod.getMessage().equals("patunayan"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread thread_VALUE = 작업.run("한글 thread_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(thread_VALUE);
        tiyakin_kumpirmahin(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket server_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> tumugon = 일꾼.submit(() -> {
                try (Socket 소켓 = server_VALUE.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String linya;
                    while ((linya = 읽기.readLine()) != null && !linya.isEmpty()) {}
                    byte[] teksto_ng_nilalaman = 문자.부호화(SMS);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + teksto_ng_nilalaman.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(teksto_ng_nilalaman);
                } catch (IOException error) { throw new UncheckedIOException(error); }
            });
            tiyakin_kumpirmahin(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + server_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(SMS), "HTTP_TCP");
            tumugon.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        tiyakin_kumpirmahin(new ProcessBuilder("/bin/echo", "Proseso_VALUE").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font font_VALUE = new Font("Dialog", Font.PLAIN, 18);
                tiyakin_kumpirmahin(font_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                tiyakin_kumpirmahin(font_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea text_box = new JTextArea(SMS);
                text_box.setFont(font_VALUE);
                JFrame window = 화면.window("그래픽 patunayan", text_box, 800, 240);
                BufferedImage iginuhit_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = iginuhit_VALUE.createGraphics();
                window.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(iginuhit_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException error) { throw new UncheckedIOException(error); }
                window.dispose();
                tiyakin_kumpirmahin(text_box.getText().equals(SMS), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
