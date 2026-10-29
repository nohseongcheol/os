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
    interface atuutilik { long 읽기(); }
    static class 부모 { protected long atuutilik = 42; }
    static class surusiq_atuutilik extends 부모 implements atuutilik { public long 읽기() { return atuutilik; } }
    private static void nalunairli_1aacb54c(boolean qanuinniq, String atiq) {
        if (!qanuinniq) throw new AssertionError(atiq);
        System.out.println("PASS " + atiq);
    }
    public static void main(String[] 인수) throws Exception {
        String titiqqaq = "한글 日本語 العربية हिन्दी 😀";
        Path tuqqurli_atuutilik = Path.of(System.getProperty("user.home"), "naammannirainiq_titiqqat.txt");
        ini.titiraq(tuqqurli_atuutilik, titiqqaq);
        nalunairli_1aacb54c(ini.읽기(tuqqurli_atuutilik).equals(titiqqaq), "UTF8_FILE");
        nalunairli_1aacb54c(문자.코드포인트수("한😀") == 2, "UNICODE");
        nalunairli_1aacb54c(문자.naammasitilli_atuutilik("\u1100\u1161").equals("가"), "NORMALIZATION");
        atuutilik kisu_atuutilik = new surusiq_atuutilik();
        nalunairli_1aacb54c(kisu_atuutilik.읽기() == 42 && (long)surusiq_atuutilik.class.getMethod("읽기").invoke(kisu_atuutilik) == 42, "OBJECT_INHERITANCE_REFLECTION");
        nalunairli_1aacb54c(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("naammannirarli"); }
        catch (IOException 예외) { nalunairli_1aacb54c(예외.getMessage().equals("naammannirarli"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread aqqusiqtarvik_atuutilik = 작업.시작("한글 aqqusiqtarvik_atuutilik", () -> 합.set(123));
        작업.기다리기(aqqusiqtarvik_atuutilik);
        nalunairli_1aacb54c(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket ikiaqqitittivik_atuutilik = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> 응답 = 일꾼.submit(() -> {
                try (Socket 소켓 = ikiaqqitittivik_atuutilik.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String titikutaak;
                    while ((titikutaak = 읽기.readLine()) != null && !titikutaak.isEmpty()) {}
                    byte[] Titiqqaup_ilulilluataa = 문자.부호화(titiqqaq);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + Titiqqaup_ilulilluataa.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(Titiqqaup_ilulilluataa);
                } catch (IOException tammarniq) { throw new UncheckedIOException(tammarniq); }
            });
            nalunairli_1aacb54c(통신.가져오기(URI.create("http://127.0.0.1:" + ikiaqqitittivik_atuutilik.getLocalPort()), Duration.ofSeconds(30)).body().equals(titiqqaq), "HTTP_TCP");
            응답.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        nalunairli_1aacb54c(new ProcessBuilder("/bin/echo", "Pivallianiq_atuutilik").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font titirausiq_atuutilik = new Font("Dialog", Font.PLAIN, 18);
                nalunairli_1aacb54c(titirausiq_atuutilik.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                nalunairli_1aacb54c(titirausiq_atuutilik.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea 글상자 = new JTextArea(titiqqaq);
                글상자.setFont(titirausiq_atuutilik);
                JFrame igalaangujaq = 화면.igalaangujaq("그래픽 naammannirarli", 글상자, 800, 240);
                BufferedImage titiraujarniq_atuutilik = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = titiraujarniq_atuutilik.createGraphics();
                igalaangujaq.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(titiraujarniq_atuutilik, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException tammarniq) { throw new UncheckedIOException(tammarniq); }
                igalaangujaq.dispose();
                nalunairli_1aacb54c(글상자.getText().equals(titiqqaq), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
