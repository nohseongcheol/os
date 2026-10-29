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
    interface iye { long Kàá(); }
    static class 부모 { protected long iye = 42; }
    static class ọmọ_iye extends 부모 implements iye { public long Kàá() { return iye; } }
    private static void ridájú(boolean kání, String Orúkọ) {
        if (!kání) throw new AssertionError(Orúkọ);
        System.out.println("PASS " + Orúkọ);
    }
    public static void main(String[] 인수) throws Exception {
        String SMS = "한글 日本語 العربية हिन्दी 😀";
        Path Store_iye = Path.of(System.getProperty("user.home"), "Àfọwọ́sí_détà.txt");
        Fáìlì.Kọ(Store_iye, SMS);
        ridájú(Fáìlì.Kàá(Store_iye).equals(SMS), "UTF8_FILE");
        ridájú(문자.코드포인트수("한😀") == 2, "UNICODE");
        ridájú(문자.ṣe_níwọ̀n_iye("\u1100\u1161").equals("가"), "NORMALIZATION");
        iye nǹkan_iye = new ọmọ_iye();
        ridájú(nǹkan_iye.Kàá() == 42 && (long)ọmọ_iye.class.getMethod("Kàá").invoke(nǹkan_iye) == 42, "OBJECT_INHERITANCE_REFLECTION");
        ridájú(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("ìfọwọ́síìwé"); }
        catch (IOException 예외) { ridájú(예외.getMessage().equals("ìfọwọ́síìwé"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread èròjà_atẹ̀lélànà_iye = 작업.Rọ́ọ̀nù("한글 èròjà_atẹ̀lélànà_iye", () -> 합.set(123));
        작업.기다리기(èròjà_atẹ̀lélànà_iye);
        ridájú(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket apèsè_iye = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> Fèsì = 일꾼.submit(() -> {
                try (Socket 소켓 = apèsè_iye.accept()) {
                    BufferedReader Kàá = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String ìlà;
                    while ((ìlà = Kàá.readLine()) != null && !ìlà.isEmpty()) {}
                    byte[] kókó_ọ̀rọ̀_ìkọ = 문자.부호화(SMS);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + kókó_ọ̀rọ̀_ìkọ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(kókó_ọ̀rọ̀_ìkọ);
                } catch (IOException àṣìṣe) { throw new UncheckedIOException(àṣìṣe); }
            });
            ridájú(통신.가져오기(URI.create("http://127.0.0.1:" + apèsè_iye.getLocalPort()), Duration.ofSeconds(30)).body().equals(SMS), "HTTP_TCP");
            Fèsì.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        ridájú(new ProcessBuilder("/bin/echo", "Ìlànà_iye").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ìrísí_lẹ́tà_iye = new Font("Dialog", Font.PLAIN, 18);
                ridájú(ìrísí_lẹ́tà_iye.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                ridájú(ìrísí_lẹ́tà_iye.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea àpótí_àyọkà = new JTextArea(SMS);
                àpótí_àyọkà.setFont(ìrísí_lẹ́tà_iye);
                JFrame wínńdò = 화면.wínńdò("그래픽 ìfọwọ́síìwé", àpótí_àyọkà, 800, 240);
                BufferedImage íyàwòrán_iye = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = íyàwòrán_iye.createGraphics();
                wínńdò.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(íyàwòrán_iye, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException àṣìṣe) { throw new UncheckedIOException(àṣìṣe); }
                wínńdò.dispose();
                ridájú(àpótí_àyọkà.getText().equals(SMS), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
