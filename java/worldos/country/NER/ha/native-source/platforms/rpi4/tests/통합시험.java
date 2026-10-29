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
    interface Daraja { long Yi_Karatu(); }
    static class 부모 { protected long Daraja = 42; }
    static class yaro_Daraja extends 부모 implements Daraja { public long Yi_Karatu() { return Daraja; } }
    private static void Tabbatar_da(boolean Yanayi, String Suna) {
        if (!Yanayi) throw new AssertionError(Suna);
        System.out.println("PASS " + Suna);
    }
    public static void main(String[] 인수) throws Exception {
        String SMS = "한글 日本語 العربية हिन्दी 😀";
        Path Ajiye_Daraja = Path.of(System.getProperty("user.home"), "amincewa_Tarin_bayani.txt");
        Fayil.Yi_Rubutu(Ajiye_Daraja, SMS);
        Tabbatar_da(Fayil.Yi_Karatu(Ajiye_Daraja).equals(SMS), "UTF8_FILE");
        Tabbatar_da(문자.코드포인트수("한😀") == 2, "UNICODE");
        Tabbatar_da(문자.Gajarta_kimar_bayanai_Daraja("\u1100\u1161").equals("가"), "NORMALIZATION");
        Daraja abu_Daraja = new yaro_Daraja();
        Tabbatar_da(abu_Daraja.Yi_Karatu() == 42 && (long)yaro_Daraja.class.getMethod("Yi_Karatu").invoke(abu_Daraja) == 42, "OBJECT_INHERITANCE_REFLECTION");
        Tabbatar_da(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("inganta"); }
        catch (IOException banbanchi) { Tabbatar_da(banbanchi.getMessage().equals("inganta"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread hira_Daraja = 작업.Tafiyar_da("한글 hira_Daraja", () -> 합.set(123));
        작업.기다리기(hira_Daraja);
        Tabbatar_da(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket Saba_Daraja = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> mayar_da_martani = 일꾼.submit(() -> {
                try (Socket 소켓 = Saba_Daraja.accept()) {
                    BufferedReader Yi_Karatu = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Layi;
                    while ((Layi = Yi_Karatu.readLine()) != null && !Layi.isEmpty()) {}
                    byte[] Gundarin_zube = 문자.부호화(SMS);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + Gundarin_zube.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(Gundarin_zube);
                } catch (IOException Kuskure) { throw new UncheckedIOException(Kuskure); }
            });
            Tabbatar_da(통신.가져오기(URI.create("http://127.0.0.1:" + Saba_Daraja.getLocalPort()), Duration.ofSeconds(30)).body().equals(SMS), "HTTP_TCP");
            mayar_da_martani.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        Tabbatar_da(new ProcessBuilder("/bin/echo", "haryar_aikin_na_ura_Daraja").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font salon_rubutu_Daraja = new Font("Dialog", Font.PLAIN, 18);
                Tabbatar_da(salon_rubutu_Daraja.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                Tabbatar_da(salon_rubutu_Daraja.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea filin_rubutu = new JTextArea(SMS);
                filin_rubutu.setFont(salon_rubutu_Daraja);
                JFrame taga = 화면.taga("그래픽 inganta", filin_rubutu, 800, 240);
                BufferedImage zane_Daraja = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = zane_Daraja.createGraphics();
                taga.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(zane_Daraja, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Kuskure) { throw new UncheckedIOException(Kuskure); }
                taga.dispose();
                Tabbatar_da(filin_rubutu.getText().equals(SMS), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
