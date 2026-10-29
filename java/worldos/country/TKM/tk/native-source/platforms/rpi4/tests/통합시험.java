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
    interface baha { long Oka(); }
    static class 부모 { protected long baha = 42; }
    static class çaga_baha extends 부모 implements baha { public long Oka() { return baha; } }
    private static void barla(boolean şert, String Ad) {
        if (!şert) throw new AssertionError(Ad);
        System.out.println("PASS " + Ad);
    }
    public static void main(String[] 인수) throws Exception {
        String Metin = "한글 日本語 العربية हिन्दी 😀";
        Path Store_baha = Path.of(System.getProperty("user.home"), "barlag_maglumat.txt");
        Faýl.Ýaz(Store_baha, Metin);
        barla(Faýl.Oka(Store_baha).equals(Metin), "UTF8_FILE");
        barla(문자.코드포인트수("한😀") == 2, "UNICODE");
        barla(문자.adaty_ýagdaýa_getir_baha("\u1100\u1161").equals("가"), "NORMALIZATION");
        baha obýekt_baha = new çaga_baha();
        barla(obýekt_baha.Oka() == 42 && (long)çaga_baha.class.getMethod("Oka").invoke(obýekt_baha) == 42, "OBJECT_INHERITANCE_REFLECTION");
        barla(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("tassykla"); }
        catch (IOException 예외) { barla(예외.getMessage().equals("tassykla"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread akym_baha = 작업.Bitir("한글 akym_baha", () -> 합.set(123));
        작업.기다리기(akym_baha);
        barla(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket serwer_baha = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> jogap_bermek = 일꾼.submit(() -> {
                try (Socket 소켓 = serwer_baha.accept()) {
                    BufferedReader Oka = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String setir;
                    while ((setir = Oka.readLine()) != null && !setir.isEmpty()) {}
                    byte[] göwre_teksti = 문자.부호화(Metin);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + göwre_teksti.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(göwre_teksti);
                } catch (IOException Hata) { throw new UncheckedIOException(Hata); }
            });
            barla(통신.가져오기(URI.create("http://127.0.0.1:" + serwer_baha.getLocalPort()), Duration.ofSeconds(30)).body().equals(Metin), "HTTP_TCP");
            jogap_bermek.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        barla(new ProcessBuilder("/bin/echo", "Proses_baha").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font şrift_baha = new Font("Dialog", Font.PLAIN, 18);
                barla(şrift_baha.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                barla(şrift_baha.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea tekst_gutusy = new JTextArea(Metin);
                tekst_gutusy.setFont(şrift_baha);
                JFrame penjire = 화면.penjire("그래픽 tassykla", tekst_gutusy, 800, 240);
                BufferedImage çyzgy_baha = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = çyzgy_baha.createGraphics();
                penjire.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(çyzgy_baha, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Hata) { throw new UncheckedIOException(Hata); }
                penjire.dispose();
                barla(tekst_gutusy.getText().equals(Metin), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
