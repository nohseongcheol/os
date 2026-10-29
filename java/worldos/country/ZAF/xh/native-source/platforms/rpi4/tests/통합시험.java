// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import isiXhosa.자바.*;
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
    interface ixabiso { long Funda(); }
    static class 부모 { protected long ixabiso = 42; }
    static class umntwana_ixabiso extends 부모 implements ixabiso { public long Funda() { return ixabiso; } }
    private static void ngqinisisa(boolean imo, String Igama) {
        if (!imo) throw new AssertionError(Igama);
        System.out.println("PASS " + Igama);
    }
    public static void main(String[] 인수) throws Exception {
        String Umbhalo = "한글 日本語 العربية हिन्दी 😀";
        Path Store_ixabiso = Path.of(System.getProperty("user.home"), "uqinisekiso_iingcombolo.txt");
        iFayili.Bhala(Store_ixabiso, Umbhalo);
        ngqinisisa(iFayili.Funda(Store_ixabiso).equals(Umbhalo), "UTF8_FILE");
        ngqinisisa(문자.코드포인트수("한😀") == 2, "UNICODE");
        ngqinisisa(문자.qhelekisa_ixabiso("\u1100\u1161").equals("가"), "NORMALIZATION");
        ixabiso into_ixabiso = new umntwana_ixabiso();
        ngqinisisa(into_ixabiso.Funda() == 42 && (long)umntwana_ixabiso.class.getMethod("Funda").invoke(into_ixabiso) == 42, "OBJECT_INHERITANCE_REFLECTION");
        ngqinisisa(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("qinisekisa"); }
        catch (IOException 예외) { ngqinisisa(예외.getMessage().equals("qinisekisa"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread ithredi_ixabiso = 작업.Phumeza("한글 ithredi_ixabiso", () -> 합.set(123));
        작업.기다리기(ithredi_ixabiso);
        ngqinisisa(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket iseva_ixabiso = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> phendula = 일꾼.submit(() -> {
                try (Socket 소켓 = iseva_ixabiso.accept()) {
                    BufferedReader Funda = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String umgca;
                    while ((umgca = Funda.readLine()) != null && !umgca.isEmpty()) {}
                    byte[] isiqu_sombhalo = 문자.부호화(Umbhalo);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + isiqu_sombhalo.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(isiqu_sombhalo);
                } catch (IOException Impazamo) { throw new UncheckedIOException(Impazamo); }
            });
            ngqinisisa(통신.가져오기(URI.create("http://127.0.0.1:" + iseva_ixabiso.getLocalPort()), Duration.ofSeconds(30)).body().equals(Umbhalo), "HTTP_TCP");
            phendula.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        ngqinisisa(new ProcessBuilder("/bin/echo", "Inkqubo_ixabiso").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ifonti_ixabiso = new Font("Dialog", Font.PLAIN, 18);
                ngqinisisa(ifonti_ixabiso.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                ngqinisisa(ifonti_ixabiso.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea indawo_yombhalo = new JTextArea(Umbhalo);
                indawo_yombhalo.setFont(ifonti_ixabiso);
                JFrame i_window = 화면.i_window("그래픽 qinisekisa", indawo_yombhalo, 800, 240);
                BufferedImage umzobo_ixabiso = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = umzobo_ixabiso.createGraphics();
                i_window.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(umzobo_ixabiso, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Impazamo) { throw new UncheckedIOException(Impazamo); }
                i_window.dispose();
                ngqinisisa(indawo_yombhalo.getText().equals(Umbhalo), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
