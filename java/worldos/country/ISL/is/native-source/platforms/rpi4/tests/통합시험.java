// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Íslenska.자바.*;
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
    interface VALUE { long Lestur(); }
    static class yfireining_VALUE { protected long VALUE = 42; }
    static class barn_VALUE extends yfireining_VALUE implements VALUE { public long Lestur() { return VALUE; } }
    private static void sannprófa(boolean skilyrði, String Heiti) {
        if (!skilyrði) throw new AssertionError(Heiti);
        System.out.println("PASS " + Heiti);
    }
    public static void main(String[] Viðföng) throws Exception {
        String Texti = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "prófun_gögn.txt");
        Skrá.Skrift(Store_VALUE, Texti);
        sannprófa(Skrá.Lestur(Store_VALUE).equals(Texti), "UTF8_FILE");
        sannprófa(문자.stafkóði_COUNT("한😀") == 2, "UNICODE");
        sannprófa(문자.staðla_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE hlutur_VALUE = new barn_VALUE();
        sannprófa(hlutur_VALUE.Lestur() == 42 && (long)barn_VALUE.class.getMethod("Lestur").invoke(hlutur_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        sannprófa(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("staðfesta"); }
        catch (IOException undantekning) { sannprófa(undantekning.getMessage().equals("staðfesta"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread þráður_VALUE = 작업.Keyra_2("한글 þráður_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(þráður_VALUE);
        sannprófa(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService starfskraftur_VALUE = Executors.newSingleThreadExecutor();
        try (ServerSocket þjónn_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> svara = starfskraftur_VALUE.submit(() -> {
                try (Socket 소켓 = þjónn_VALUE.accept()) {
                    BufferedReader Lestur = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Lína;
                    while ((Lína = Lestur.readLine()) != null && !Lína.isEmpty()) {}
                    byte[] meginmál = 문자.부호화(Texti);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + meginmál.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(meginmál);
                } catch (IOException Villa) { throw new UncheckedIOException(Villa); }
            });
            sannprófa(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + þjónn_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Texti), "HTTP_TCP");
            svara.get(30, TimeUnit.SECONDS);
        } finally { starfskraftur_VALUE.shutdownNow(); }
        sannprófa(new ProcessBuilder("/bin/echo", "Ferli_VALUE").start().waitFor() == 0, "PROCESS");
        if (Viðföng.length > 0 && Viðföng[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font leturgerð_VALUE = new Font("Dialog", Font.PLAIN, 18);
                sannprófa(leturgerð_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                sannprófa(leturgerð_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea textasvæði = new JTextArea(Texti);
                textasvæði.setFont(leturgerð_VALUE);
                JFrame Gluggi = 화면.Gluggi("그래픽 staðfesta", textasvæði, 800, 240);
                BufferedImage teikning_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = teikning_VALUE.createGraphics();
                Gluggi.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(teikning_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Villa) { throw new UncheckedIOException(Villa); }
                Gluggi.dispose();
                sannprófa(textasvæði.getText().equals(Texti), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
