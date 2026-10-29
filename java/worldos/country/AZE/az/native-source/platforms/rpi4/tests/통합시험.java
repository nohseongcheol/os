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
    interface VALUE { long Oxuma(); }
    static class 부모 { protected long VALUE = 42; }
    static class uşaq_VALUE extends 부모 implements VALUE { public long Oxuma() { return VALUE; } }
    private static void yoxlamaq(boolean şərt, String Ad) {
        if (!şərt) throw new AssertionError(Ad);
        System.out.println("PASS " + Ad);
    }
    public static void main(String[] 인수) throws Exception {
        String Mətn = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "yoxlama_verilənlər.txt");
        FAYL.Yazma(Store_VALUE, Mətn);
        yoxlamaq(FAYL.Oxuma(Store_VALUE).equals(Mətn), "UTF8_FILE");
        yoxlamaq(문자.simvol_kodu_COUNT("한😀") == 2, "UNICODE");
        yoxlamaq(문자.normallaşdırmaq_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE obyekt_VALUE = new uşaq_VALUE();
        yoxlamaq(obyekt_VALUE.Oxuma() == 42 && (long)uşaq_VALUE.class.getMethod("Oxuma").invoke(obyekt_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        yoxlamaq(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("təsdiqlə"); }
        catch (IOException istisna) { yoxlamaq(istisna.getMessage().equals("təsdiqlə"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread axın_VALUE_5b72a632 = 작업.İcra_Et("한글 axın_VALUE_5b72a632", () -> SUM_VALUE.set(123));
        작업.기다리기(axın_VALUE_5b72a632);
        yoxlamaq(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket server_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> cavab = 일꾼.submit(() -> {
                try (Socket 소켓 = server_VALUE.accept()) {
                    BufferedReader Oxuma = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Giriş;
                    while ((Giriş = Oxuma.readLine()) != null && !Giriş.isEmpty()) {}
                    byte[] əsas_mətn = 문자.부호화(Mətn);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + əsas_mətn.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(əsas_mətn);
                } catch (IOException XƏTA) { throw new UncheckedIOException(XƏTA); }
            });
            yoxlamaq(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + server_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Mətn), "HTTP_TCP");
            cavab.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        yoxlamaq(new ProcessBuilder("/bin/echo", "Proses_VALUE").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font şrift_VALUE = new Font("Dialog", Font.PLAIN, 18);
                yoxlamaq(şrift_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                yoxlamaq(şrift_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea mətn_qutusu = new JTextArea(Mətn);
                mətn_qutusu.setFont(şrift_VALUE);
                JFrame pəncərə = 화면.pəncərə("그래픽 təsdiqlə", mətn_qutusu, 800, 240);
                BufferedImage rəsm_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = rəsm_VALUE.createGraphics();
                pəncərə.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(rəsm_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException XƏTA) { throw new UncheckedIOException(XƏTA); }
                pəncərə.dispose();
                yoxlamaq(mətn_qutusu.getText().equals(Mətn), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
