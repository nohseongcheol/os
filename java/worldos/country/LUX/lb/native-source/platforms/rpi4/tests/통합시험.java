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
    interface VALUE { long 읽기(); }
    static class 부모 { protected long VALUE = 42; }
    static class Kand_VALUE extends 부모 implements VALUE { public long 읽기() { return VALUE; } }
    private static void verifizéieren(boolean Bedéngung, String Numm) {
        if (!Bedéngung) throw new AssertionError(Numm);
        System.out.println("PASS " + Numm);
    }
    public static void main(String[] 인수) throws Exception {
        String SMS = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "Validatioun_Daten.txt");
        Fichier.schreiwen(Store_VALUE, SMS);
        verifizéieren(Fichier.읽기(Store_VALUE).equals(SMS), "UTF8_FILE");
        verifizéieren(문자.Zeechecode_COUNT("한😀") == 2, "UNICODE");
        verifizéieren(문자.normaliséieren_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE Objet_VALUE = new Kand_VALUE();
        verifizéieren(Objet_VALUE.읽기() == 42 && (long)Kand_VALUE.class.getMethod("읽기").invoke(Objet_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        verifizéieren(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("validéieren"); }
        catch (IOException 예외) { verifizéieren(예외.getMessage().equals("validéieren"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread Thread_VALUE = 작업.Laf("한글 Thread_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(Thread_VALUE);
        verifizéieren(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket Server_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> äntweren = 일꾼.submit(() -> {
                try (Socket 소켓 = Server_VALUE.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Zeil;
                    while ((Zeil = 읽기.readLine()) != null && !Zeil.isEmpty()) {}
                    byte[] Textkierper = 문자.부호화(SMS);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + Textkierper.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(Textkierper);
                } catch (IOException Feeler) { throw new UncheckedIOException(Feeler); }
            });
            verifizéieren(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + Server_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(SMS), "HTTP_TCP");
            äntweren.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        verifizéieren(new ProcessBuilder("/bin/echo", "Prozess_VALUE").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font Schrëftaart_VALUE = new Font("Dialog", Font.PLAIN, 18);
                verifizéieren(Schrëftaart_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                verifizéieren(Schrëftaart_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea Textfeld_d6e55852 = new JTextArea(SMS);
                Textfeld_d6e55852.setFont(Schrëftaart_VALUE);
                JFrame Fënster = 화면.Fënster("그래픽 validéieren", Textfeld_d6e55852, 800, 240);
                BufferedImage Zeechnung_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = Zeechnung_VALUE.createGraphics();
                Fënster.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(Zeechnung_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Feeler) { throw new UncheckedIOException(Feeler); }
                Fënster.dispose();
                verifizéieren(Textfeld_d6e55852.getText().equals(SMS), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
