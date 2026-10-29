// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Ikinyarwanda.자바.*;
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
    interface agaciro { long 읽기(); }
    static class 부모 { protected long agaciro = 42; }
    static class ishami_agaciro_b642f4b4 extends 부모 implements agaciro { public long 읽기() { return agaciro; } }
    private static void gusuzuma(boolean icyangombwa, String Izina) {
        if (!icyangombwa) throw new AssertionError(Izina);
        System.out.println("PASS " + Izina);
    }
    public static void main(String[] 인수) throws Exception {
        String Umwandiko = "한글 日本語 العربية हिन्दी 😀";
        Path Store_agaciro = Path.of(System.getProperty("user.home"), "iyemeza_amakurushingiro.txt");
        Idosiye.kwandika(Store_agaciro, Umwandiko);
        gusuzuma(Idosiye.읽기(Store_agaciro).equals(Umwandiko), "UTF8_FILE");
        gusuzuma(문자.코드포인트수("한😀") == 2, "UNICODE");
        gusuzuma(문자.kuboneza_agaciro("\u1100\u1161").equals("가"), "NORMALIZATION");
        agaciro ikintu_agaciro_2ed200e9 = new ishami_agaciro_b642f4b4();
        gusuzuma(ikintu_agaciro_2ed200e9.읽기() == 42 && (long)ishami_agaciro_b642f4b4.class.getMethod("읽기").invoke(ikintu_agaciro_2ed200e9) == 42, "OBJECT_INHERITANCE_REFLECTION");
        gusuzuma(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("kwemeza"); }
        catch (IOException 예외) { gusuzuma(예외.getMessage().equals("kwemeza"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread mugenaporogaramu_agaciro = 작업.ihuriro("한글 mugenaporogaramu_agaciro", () -> 합.set(123));
        작업.기다리기(mugenaporogaramu_agaciro);
        gusuzuma(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket seriveri_agaciro = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> gusubiza = 일꾼.submit(() -> {
                try (Socket 소켓 = seriveri_agaciro.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String umurongo;
                    while ((umurongo = 읽기.readLine()) != null && !umurongo.isEmpty()) {}
                    byte[] igihimba_cy_umwandiko = 문자.부호화(Umwandiko);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + igihimba_cy_umwandiko.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(igihimba_cy_umwandiko);
                } catch (IOException IKOSA) { throw new UncheckedIOException(IKOSA); }
            });
            gusuzuma(통신.가져오기(URI.create("http://127.0.0.1:" + seriveri_agaciro.getLocalPort()), Duration.ofSeconds(30)).body().equals(Umwandiko), "HTTP_TCP");
            gusubiza.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        gusuzuma(new ProcessBuilder("/bin/echo", "Inzira_agaciro").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font imyandikire_agaciro = new Font("Dialog", Font.PLAIN, 18);
                gusuzuma(imyandikire_agaciro.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                gusuzuma(imyandikire_agaciro.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea akazu_k_umwandiko = new JTextArea(Umwandiko);
                akazu_k_umwandiko.setFont(imyandikire_agaciro);
                JFrame idirishya = 화면.idirishya("그래픽 kwemeza", akazu_k_umwandiko, 800, 240);
                BufferedImage igishushanyo_agaciro = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = igishushanyo_agaciro.createGraphics();
                idirishya.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(igishushanyo_agaciro, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException IKOSA) { throw new UncheckedIOException(IKOSA); }
                idirishya.dispose();
                gusuzuma(akazu_k_umwandiko.getText().equals(Umwandiko), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
