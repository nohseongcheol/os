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
    interface boleng { long Bala(); }
    static class 부모 { protected long boleng = 42; }
    static class ngwana_boleng extends 부모 implements boleng { public long Bala() { return boleng; } }
    private static void kgonthiša(boolean seemo, String Leina) {
        if (!seemo) throw new AssertionError(Leina);
        System.out.println("PASS " + Leina);
    }
    public static void main(String[] 인수) throws Exception {
        String Sengwalwa = "한글 日本語 العربية हिन्दी 😀";
        Path lota_boleng = Path.of(System.getProperty("user.home"), "tiišetšo_data.txt");
        Faele.Ngwala(lota_boleng, Sengwalwa);
        kgonthiša(Faele.Bala(lota_boleng).equals(Sengwalwa), "UTF8_FILE");
        kgonthiša(문자.코드포인트수("한😀") == 2, "UNICODE");
        kgonthiša(문자.fokotša_kopišo_boleng("\u1100\u1161").equals("가"), "NORMALIZATION");
        boleng selo_boleng = new ngwana_boleng();
        kgonthiša(selo_boleng.Bala() == 42 && (long)ngwana_boleng.class.getMethod("Bala").invoke(selo_boleng) == 42, "OBJECT_INHERITANCE_REFLECTION");
        kgonthiša(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("kgonthiša_5fb2b747"); }
        catch (IOException 예외) { kgonthiša(예외.getMessage().equals("kgonthiša_5fb2b747"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread threte_boleng = 작업.Diriša("한글 threte_boleng", () -> 합.set(123));
        작업.기다리기(threte_boleng);
        kgonthiša(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket seba_boleng = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> fetola = 일꾼.submit(() -> {
                try (Socket 소켓 = seba_boleng.accept()) {
                    BufferedReader Bala = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String mothaladi;
                    while ((mothaladi = Bala.readLine()) != null && !mothaladi.isEmpty()) {}
                    byte[] mmele_wa_sengwalwa = 문자.부호화(Sengwalwa);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + mmele_wa_sengwalwa.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(mmele_wa_sengwalwa);
                } catch (IOException Phošo) { throw new UncheckedIOException(Phošo); }
            });
            kgonthiša(통신.가져오기(URI.create("http://127.0.0.1:" + seba_boleng.getLocalPort()), Duration.ofSeconds(30)).body().equals(Sengwalwa), "HTTP_TCP");
            fetola.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        kgonthiša(new ProcessBuilder("/bin/echo", "tiragalo_boleng").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font fonte_boleng = new Font("Dialog", Font.PLAIN, 18);
                kgonthiša(fonte_boleng.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                kgonthiša(fonte_boleng.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea lefelo_la_dingwalwa = new JTextArea(Sengwalwa);
                lefelo_la_dingwalwa.setFont(fonte_boleng);
                JFrame lefastere = 화면.lefastere("그래픽 kgonthiša_5fb2b747", lefelo_la_dingwalwa, 800, 240);
                BufferedImage sethalwa_boleng = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = sethalwa_boleng.createGraphics();
                lefastere.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(sethalwa_boleng, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Phošo) { throw new UncheckedIOException(Phošo); }
                lefastere.dispose();
                kgonthiša(lefelo_la_dingwalwa.getText().equals(Sengwalwa), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
