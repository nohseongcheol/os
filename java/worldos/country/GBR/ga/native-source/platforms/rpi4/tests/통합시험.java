// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Gaeilge.자바.*;
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
    interface VALUE { long Léigh(); }
    static class 부모 { protected long VALUE = 42; }
    static class leanbh_VALUE extends 부모 implements VALUE { public long Léigh() { return VALUE; } }
    private static void fíoraigh(boolean coinníoll, String Ainm) {
        if (!coinníoll) throw new AssertionError(Ainm);
        System.out.println("PASS " + Ainm);
    }
    public static void main(String[] Argóintí) throws Exception {
        String Téacs = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "bailíochtú_sonraí.txt");
        Comhad.Scríobh(Store_VALUE, Téacs);
        fíoraigh(Comhad.Léigh(Store_VALUE).equals(Téacs), "UTF8_FILE");
        fíoraigh(문자.pointe_cóid_COUNT("한😀") == 2, "UNICODE");
        fíoraigh(문자.normalaigh_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE oibiacht_VALUE = new leanbh_VALUE();
        fíoraigh(oibiacht_VALUE.Léigh() == 42 && (long)leanbh_VALUE.class.getMethod("Léigh").invoke(oibiacht_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        fíoraigh(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("bailíochtaigh"); }
        catch (IOException eisceacht) { fíoraigh(eisceacht.getMessage().equals("bailíochtaigh"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread snáithe_VALUE = 작업.Rith_2("한글 snáithe_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(snáithe_VALUE);
        fíoraigh(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket freastalaí_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> freagair = 일꾼.submit(() -> {
                try (Socket 소켓 = freastalaí_VALUE.accept()) {
                    BufferedReader Léigh = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Líne;
                    while ((Líne = Léigh.readLine()) != null && !Líne.isEmpty()) {}
                    byte[] corpthéacs = 문자.부호화(Téacs);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + corpthéacs.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(corpthéacs);
                } catch (IOException ERREÁID) { throw new UncheckedIOException(ERREÁID); }
            });
            fíoraigh(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + freastalaí_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Téacs), "HTTP_TCP");
            freagair.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        fíoraigh(new ProcessBuilder("/bin/echo", "Próiseas_VALUE").start().waitFor() == 0, "PROCESS");
        if (Argóintí.length > 0 && Argóintí[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font clófhoireann_VALUE = new Font("Dialog", Font.PLAIN, 18);
                fíoraigh(clófhoireann_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                fíoraigh(clófhoireann_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea bosca_téacs = new JTextArea(Téacs);
                bosca_téacs.setFont(clófhoireann_VALUE);
                JFrame fuinneog = 화면.fuinneog("그래픽 bailíochtaigh", bosca_téacs, 800, 240);
                BufferedImage líníocht_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = líníocht_VALUE.createGraphics();
                fuinneog.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(líníocht_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ERREÁID) { throw new UncheckedIOException(ERREÁID); }
                fuinneog.dispose();
                fíoraigh(bosca_téacs.getText().equals(Téacs), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
