// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Türkçe.자바.*;
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

public class test_tümleştirme {
    interface değer { long Okuma(); }
    static class ana_değer { protected long değer = 42; }
    static class alt_değer extends ana_değer implements değer { public long Okuma() { return değer; } }
    private static void doğrulamak(boolean koşul, String İsim) {
        if (!koşul) throw new AssertionError(İsim);
        System.out.println("PASS " + İsim);
    }
    public static void main(String[] bağımsız_değişkenler) throws Exception {
        String metin = "한글 日本語 العربية हिन्दी 😀";
        Path depo_değer = Path.of(System.getProperty("user.home"), "doğrulama_veri.txt");
        dosya.Yazma(depo_değer, metin);
        doğrulamak(dosya.Okuma(depo_değer).equals(metin), "UTF8_FILE");
        doğrulamak(문자.kod_öğesi_BAĞ_DEĞ_SAY("한😀") == 2, "UNICODE");
        doğrulamak(문자.normalleştirmek_değer("\u1100\u1161").equals("가"), "NORMALIZATION");
        değer nesne_değer = new alt_değer();
        doğrulamak(nesne_değer.Okuma() == 42 && (long)alt_değer.class.getMethod("Okuma").invoke(nesne_değer) == 42, "OBJECT_INHERITANCE_REFLECTION");
        doğrulamak(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("doğrulamak_5fb2b747"); }
        catch (IOException özel_durum) { doğrulamak(özel_durum.getMessage().equals("doğrulamak_5fb2b747"), "EXCEPTION"); }
        AtomicInteger SUM_değer = new AtomicInteger();
        Thread yazışma_değer = 작업.çalıştır("한글 yazışma_değer", () -> SUM_değer.set(123));
        작업.기다리기(yazışma_değer);
        doğrulamak(SUM_değer.get() == 123, "THREAD");
        ExecutorService çalışan_değer = Executors.newSingleThreadExecutor();
        try (ServerSocket sunucu_değer = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> yanıt = çalışan_değer.submit(() -> {
                try (Socket yuva_değer = sunucu_değer.accept()) {
                    BufferedReader Okuma = new BufferedReader(new InputStreamReader(yuva_değer.getInputStream()));
                    String girdi_satırı;
                    while ((girdi_satırı = Okuma.readLine()) != null && !girdi_satırı.isEmpty()) {}
                    byte[] gövde_metni = 문자.kodlamak(metin);
                    yuva_değer.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + gövde_metni.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    yuva_değer.getOutputStream().write(gövde_metni);
                } catch (IOException hata) { throw new UncheckedIOException(hata); }
            });
            doğrulamak(iletişim.AL_değer(URI.create("http://127.0.0.1:" + sunucu_değer.getLocalPort()), Duration.ofSeconds(30)).body().equals(metin), "HTTP_TCP");
            yanıt.get(30, TimeUnit.SECONDS);
        } finally { çalışan_değer.shutdownNow(); }
        doğrulamak(new ProcessBuilder("/bin/echo", "işlem_değer").start().waitFor() == 0, "PROCESS");
        if (bağımsız_değişkenler.length > 0 && bağımsız_değişkenler[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font yazı_tipi_değer = new Font("Dialog", Font.PLAIN, 18);
                doğrulamak(yazı_tipi_değer.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                doğrulamak(yazı_tipi_değer.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea metin_kutusu = new JTextArea(metin);
                metin_kutusu.setFont(yazı_tipi_değer);
                JFrame Pencere = 화면.Pencere("그래픽 doğrulamak_5fb2b747", metin_kutusu, 800, 240);
                BufferedImage çizim_değer = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D fırça_değer = çizim_değer.createGraphics();
                Pencere.paint(fırça_değer); fırça_değer.dispose();
                try { javax.imageio.ImageIO.write(çizim_değer, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException hata) { throw new UncheckedIOException(hata); }
                Pencere.dispose();
                doğrulamak(metin_kutusu.getText().equals(metin), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
