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
    interface Boleng { long 읽기(); }
    static class 부모 { protected long Boleng = 42; }
    static class ngwana_Boleng extends 부모 implements Boleng { public long 읽기() { return Boleng; } }
    private static void netefatsa(boolean boemo, String leina) {
        if (!boemo) throw new AssertionError(leina);
        System.out.println("PASS " + leina);
    }
    public static void main(String[] 인수) throws Exception {
        String SMS = "한글 日本語 العربية हिन्दी 😀";
        Path Store_Boleng = Path.of(System.getProperty("user.home"), "netefatso_tshedimosetso.txt");
        faele.kwala(Store_Boleng, SMS);
        netefatsa(faele.읽기(Store_Boleng).equals(SMS), "UTF8_FILE");
        netefatsa(문자.코드포인트수("한😀") == 2, "UNICODE");
        netefatsa(문자.fokotsa_ntsifatso_Boleng("\u1100\u1161").equals("가"), "NORMALIZATION");
        Boleng selwana_Boleng = new ngwana_Boleng();
        netefatsa(selwana_Boleng.읽기() == 42 && (long)ngwana_Boleng.class.getMethod("읽기").invoke(selwana_Boleng) == 42, "OBJECT_INHERITANCE_REFLECTION");
        netefatsa(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("netefatsa_5fb2b747"); }
        catch (IOException 예외) { netefatsa(예외.getMessage().equals("netefatsa_5fb2b747"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread tlhale_Boleng = 작업.dirisa("한글 tlhale_Boleng", () -> 합.set(123));
        작업.기다리기(tlhale_Boleng);
        netefatsa(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket sefara_Boleng = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> araba = 일꾼.submit(() -> {
                try (Socket 소켓 = sefara_Boleng.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Mola;
                    while ((Mola = 읽기.readLine()) != null && !Mola.isEmpty()) {}
                    byte[] diteng_tsa_mokwalo = 문자.부호화(SMS);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + diteng_tsa_mokwalo.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(diteng_tsa_mokwalo);
                } catch (IOException phoso) { throw new UncheckedIOException(phoso); }
            });
            netefatsa(통신.가져오기(URI.create("http://127.0.0.1:" + sefara_Boleng.getLocalPort()), Duration.ofSeconds(30)).body().equals(SMS), "HTTP_TCP");
            araba.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        netefatsa(new ProcessBuilder("/bin/echo", "Thulaganyo_Boleng").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font mofutatlhaka_Boleng = new Font("Dialog", Font.PLAIN, 18);
                netefatsa(mofutatlhaka_Boleng.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                netefatsa(mofutatlhaka_Boleng.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea lefelo_la_mokwalo = new JTextArea(SMS);
                lefelo_la_mokwalo.setFont(mofutatlhaka_Boleng);
                JFrame fensetere = 화면.fensetere("그래픽 netefatsa_5fb2b747", lefelo_la_mokwalo, 800, 240);
                BufferedImage sethalo_Boleng = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = sethalo_Boleng.createGraphics();
                fensetere.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(sethalo_Boleng, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException phoso) { throw new UncheckedIOException(phoso); }
                fensetere.dispose();
                netefatsa(lefelo_la_mokwalo.getText().equals(SMS), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
