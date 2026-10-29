// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Malti.자바.*;
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
    static class tfal_VALUE extends 부모 implements VALUE { public long 읽기() { return VALUE; } }
    private static void vverifika(boolean kondizzjoni, String isem) {
        if (!kondizzjoni) throw new AssertionError(isem);
        System.out.println("PASS " + isem);
    }
    public static void main(String[] 인수) throws Exception {
        String SMS = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "validazzjoni_data.txt");
        fajl.kiteb(Store_VALUE, SMS);
        vverifika(fajl.읽기(Store_VALUE).equals(SMS), "UTF8_FILE");
        vverifika(문자.kodiċi_tal_karattru_COUNT("한😀") == 2, "UNICODE");
        vverifika(문자.nnormalizza_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE oġġett_VALUE = new tfal_VALUE();
        vverifika(oġġett_VALUE.읽기() == 42 && (long)tfal_VALUE.class.getMethod("읽기").invoke(oġġett_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        vverifika(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("vvalida"); }
        catch (IOException 예외) { vverifika(예외.getMessage().equals("vvalida"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread fil_VALUE = 작업.serje("한글 fil_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(fil_VALUE);
        vverifika(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket server_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> wieġeb = 일꾼.submit(() -> {
                try (Socket 소켓 = server_VALUE.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String linja;
                    while ((linja = 읽기.readLine()) != null && !linja.isEmpty()) {}
                    byte[] il_korp_tat_test = 문자.부호화(SMS);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + il_korp_tat_test.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(il_korp_tat_test);
                } catch (IOException żball) { throw new UncheckedIOException(żball); }
            });
            vverifika(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + server_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(SMS), "HTTP_TCP");
            wieġeb.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        vverifika(new ProcessBuilder("/bin/echo", "Proċess_VALUE").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font font_VALUE = new Font("Dialog", Font.PLAIN, 18);
                vverifika(font_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                vverifika(font_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea kaxxa_tat_test = new JTextArea(SMS);
                kaxxa_tat_test.setFont(font_VALUE);
                JFrame tieqa = 화면.tieqa("그래픽 vvalida", kaxxa_tat_test, 800, 240);
                BufferedImage tpinġija_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = tpinġija_VALUE.createGraphics();
                tieqa.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(tpinġija_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException żball) { throw new UncheckedIOException(żball); }
                tieqa.dispose();
                vverifika(kaxxa_tat_test.getText().equals(SMS), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
