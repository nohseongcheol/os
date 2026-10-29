// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Reo_Māori.자바.*;
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
    interface uara { long Pānuitia(); }
    static class 부모 { protected long uara = 42; }
    static class tamaiti_uara extends 부모 implements uara { public long Pānuitia() { return uara; } }
    private static void manatoko(boolean here, String Ingoa) {
        if (!here) throw new AssertionError(Ingoa);
        System.out.println("PASS " + Ingoa);
    }
    public static void main(String[] 인수) throws Exception {
        String Ngā_kupu = "한글 日本語 العربية हिन्दी 😀";
        Path Store_uara = Path.of(System.getProperty("user.home"), "whakamana_raraunga.txt");
        Kōnae.Tuhia(Store_uara, Ngā_kupu);
        manatoko(Kōnae.Pānuitia(Store_uara).equals(Ngā_kupu), "UTF8_FILE");
        manatoko(문자.waehere_pūāhua_COUNT("한😀") == 2, "UNICODE");
        manatoko(문자.whakanoa_uara("\u1100\u1161").equals("가"), "NORMALIZATION");
        uara ahanoa_uara = new tamaiti_uara();
        manatoko(ahanoa_uara.Pānuitia() == 42 && (long)tamaiti_uara.class.getMethod("Pānuitia").invoke(ahanoa_uara) == 42, "OBJECT_INHERITANCE_REFLECTION");
        manatoko(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("whakamana"); }
        catch (IOException 예외) { manatoko(예외.getMessage().equals("whakamana"), "EXCEPTION"); }
        AtomicInteger SUM_uara = new AtomicInteger();
        Thread miro_uara = 작업.whakahaere("한글 miro_uara", () -> SUM_uara.set(123));
        작업.기다리기(miro_uara);
        manatoko(SUM_uara.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket tūmau_uara = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> whakautu = 일꾼.submit(() -> {
                try (Socket 소켓 = tūmau_uara.accept()) {
                    BufferedReader Pānuitia = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String hononga;
                    while ((hononga = Pānuitia.readLine()) != null && !hononga.isEmpty()) {}
                    byte[] kuputuhi_tinana = 문자.부호화(Ngā_kupu);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + kuputuhi_tinana.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(kuputuhi_tinana);
                } catch (IOException Pōhēhē) { throw new UncheckedIOException(Pōhēhē); }
            });
            manatoko(통신.TAKE_uara(URI.create("http://127.0.0.1:" + tūmau_uara.getLocalPort()), Duration.ofSeconds(30)).body().equals(Ngā_kupu), "HTTP_TCP");
            whakautu.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        manatoko(new ProcessBuilder("/bin/echo", "Hātepe_uara").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font momotuhi_uara = new Font("Dialog", Font.PLAIN, 18);
                manatoko(momotuhi_uara.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                manatoko(momotuhi_uara.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea pouaka_kuputuhi = new JTextArea(Ngā_kupu);
                pouaka_kuputuhi.setFont(momotuhi_uara);
                JFrame matapihi = 화면.matapihi("그래픽 whakamana", pouaka_kuputuhi, 800, 240);
                BufferedImage tātuhi_uara = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = tātuhi_uara.createGraphics();
                matapihi.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(tātuhi_uara, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Pōhēhē) { throw new UncheckedIOException(Pōhēhē); }
                matapihi.dispose();
                manatoko(pouaka_kuputuhi.getText().equals(Ngā_kupu), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
