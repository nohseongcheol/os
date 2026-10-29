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
    interface xëyma { long 읽기(); }
    static class 부모 { protected long xëyma = 42; }
    static class xale_xëyma extends 부모 implements xëyma { public long 읽기() { return xëyma; } }
    private static void luñutu(boolean anam, String tur_253d1510) {
        if (!anam) throw new AssertionError(tur_253d1510);
        System.out.println("PASS " + tur_253d1510);
    }
    public static void main(String[] 인수) throws Exception {
        String Tekst = "한글 日本語 العربية हिन्दी 😀";
        Path Store_xëyma = Path.of(System.getProperty("user.home"), "wéral_mbir.txt");
        bara_denc.biir(Store_xëyma, Tekst);
        luñutu(bara_denc.읽기(Store_xëyma).equals(Tekst), "UTF8_FILE");
        luñutu(문자.코드포인트수("한😀") == 2, "UNICODE");
        luñutu(문자.yonnal_xëyma("\u1100\u1161").equals("가"), "NORMALIZATION");
        xëyma yëf_xëyma = new xale_xëyma();
        luñutu(yëf_xëyma.읽기() == 42 && (long)xale_xëyma.class.getMethod("읽기").invoke(yëf_xëyma) == 42, "OBJECT_INHERITANCE_REFLECTION");
        luñutu(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("wéral"); }
        catch (IOException 예외) { luñutu(예외.getMessage().equals("wéral"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread buumug_jokkale_xëyma = 작업.daw("한글 buumug_jokkale_xëyma", () -> 합.set(123));
        작업.기다리기(buumug_jokkale_xëyma);
        luñutu(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket dëggu_xëyma = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> tontu = 일꾼.submit(() -> {
                try (Socket 소켓 = dëggu_xëyma.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String buum;
                    while ((buum = 읽기.readLine()) != null && !buum.isEmpty()) {}
                    byte[] yaxub_mool = 문자.부호화(Tekst);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + yaxub_mool.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(yaxub_mool);
                } catch (IOException njumte) { throw new UncheckedIOException(njumte); }
            });
            luñutu(통신.가져오기(URI.create("http://127.0.0.1:" + dëggu_xëyma.getLocalPort()), Duration.ofSeconds(30)).body().equals(Tekst), "HTTP_TCP");
            tontu.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        luñutu(new ProcessBuilder("/bin/echo", "yokkute_xëyma").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font mbindin_xëyma = new Font("Dialog", Font.PLAIN, 18);
                luñutu(mbindin_xëyma.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                luñutu(mbindin_xëyma.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea barabu_bindukaay = new JTextArea(Tekst);
                barabu_bindukaay.setFont(mbindin_xëyma);
                JFrame palanteer = 화면.palanteer("그래픽 wéral", barabu_bindukaay, 800, 240);
                BufferedImage deseñ_xëyma = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = deseñ_xëyma.createGraphics();
                palanteer.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(deseñ_xëyma, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException njumte) { throw new UncheckedIOException(njumte); }
                palanteer.dispose();
                luñutu(barabu_bindukaay.getText().equals(Tekst), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
