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
    interface VALUE { long Lees(); }
    static class 부모 { protected long VALUE = 42; }
    static class kind_VALUE extends 부모 implements VALUE { public long Lees() { return VALUE; } }
    private static void verifieer(boolean toestand, String Naam) {
        if (!toestand) throw new AssertionError(Naam);
        System.out.println("PASS " + Naam);
    }
    public static void main(String[] 인수) throws Exception {
        String Teks = "한글 日本語 العربية हिन्दी 😀";
        Path bêre_VALUE = Path.of(System.getProperty("user.home"), "validering_data.txt");
        Lêer.Skryf(bêre_VALUE, Teks);
        verifieer(Lêer.Lees(bêre_VALUE).equals(Teks), "UTF8_FILE");
        verifieer(문자.karakterkode_COUNT("한😀") == 2, "UNICODE");
        verifieer(문자.normaliseer_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE objek_VALUE = new kind_VALUE();
        verifieer(objek_VALUE.Lees() == 42 && (long)kind_VALUE.class.getMethod("Lees").invoke(objek_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        verifieer(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("valideer"); }
        catch (IOException uitsondering) { verifieer(uitsondering.getMessage().equals("valideer"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread draad_VALUE = 작업.Loop("한글 draad_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(draad_VALUE);
        verifieer(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket bediener_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> antwoord = 일꾼.submit(() -> {
                try (Socket 소켓 = bediener_VALUE.accept()) {
                    BufferedReader Lees = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String lyn;
                    while ((lyn = Lees.readLine()) != null && !lyn.isEmpty()) {}
                    byte[] inhoudteks = 문자.부호화(Teks);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + inhoudteks.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(inhoudteks);
                } catch (IOException Fout) { throw new UncheckedIOException(Fout); }
            });
            verifieer(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + bediener_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Teks), "HTTP_TCP");
            antwoord.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        verifieer(new ProcessBuilder("/bin/echo", "Proses_VALUE").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font font_VALUE = new Font("Dialog", Font.PLAIN, 18);
                verifieer(font_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                verifieer(font_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea teksarea = new JTextArea(Teks);
                teksarea.setFont(font_VALUE);
                JFrame venster = 화면.venster("그래픽 valideer", teksarea, 800, 240);
                BufferedImage tekening_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = tekening_VALUE.createGraphics();
                venster.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(tekening_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Fout) { throw new UncheckedIOException(Fout); }
                venster.dispose();
                verifieer(teksarea.getText().equals(Teks), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
