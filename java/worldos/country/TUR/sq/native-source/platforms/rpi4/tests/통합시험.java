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
    interface VALUE { long Leximi(); }
    static class 부모 { protected long VALUE = 42; }
    static class fëmijë_VALUE extends 부모 implements VALUE { public long Leximi() { return VALUE; } }
    private static void verifikoj(boolean kusht, String Emër) {
        if (!kusht) throw new AssertionError(Emër);
        System.out.println("PASS " + Emër);
    }
    public static void main(String[] Argumente) throws Exception {
        String Teksti = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "miratim_të_dhëna.txt");
        Kartelë.Shkrimi(Store_VALUE, Teksti);
        verifikoj(Kartelë.Leximi(Store_VALUE).equals(Teksti), "UTF8_FILE");
        verifikoj(문자.kodi_i_karakterit_COUNT("한😀") == 2, "UNICODE");
        verifikoj(문자.normalizoj_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE objekt_VALUE = new fëmijë_VALUE();
        verifikoj(objekt_VALUE.Leximi() == 42 && (long)fëmijë_VALUE.class.getMethod("Leximi").invoke(objekt_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        verifikoj(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("vlerësoj"); }
        catch (IOException përjashtim) { verifikoj(përjashtim.getMessage().equals("vlerësoj"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread thread_VALUE = 작업.Ekzekuto("한글 thread_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(thread_VALUE);
        verifikoj(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket server_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> replikë = 일꾼.submit(() -> {
                try (Socket 소켓 = server_VALUE.accept()) {
                    BufferedReader Leximi = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String linjë;
                    while ((linjë = Leximi.readLine()) != null && !linjë.isEmpty()) {}
                    byte[] trupi_i_tekstit = 문자.부호화(Teksti);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + trupi_i_tekstit.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(trupi_i_tekstit);
                } catch (IOException GABIM) { throw new UncheckedIOException(GABIM); }
            });
            verifikoj(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + server_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Teksti), "HTTP_TCP");
            replikë.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        verifikoj(new ProcessBuilder("/bin/echo", "Proces_VALUE").start().waitFor() == 0, "PROCESS");
        if (Argumente.length > 0 && Argumente[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font font_VALUE = new Font("Dialog", Font.PLAIN, 18);
                verifikoj(font_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                verifikoj(font_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea fushë_shkrimi = new JTextArea(Teksti);
                fushë_shkrimi.setFont(font_VALUE);
                JFrame Dritare = 화면.Dritare("그래픽 vlerësoj", fushë_shkrimi, 800, 240);
                BufferedImage vizatim_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = vizatim_VALUE.createGraphics();
                Dritare.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(vizatim_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException GABIM) { throw new UncheckedIOException(GABIM); }
                Dritare.dispose();
                verifikoj(fushë_shkrimi.getText().equals(Teksti), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
