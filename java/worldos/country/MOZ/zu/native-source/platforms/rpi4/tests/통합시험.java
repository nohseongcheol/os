// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Isi_Zulu.자바.*;
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
    interface inani { long Funda(); }
    static class 부모 { protected long inani = 42; }
    static class ingane_inani extends 부모 implements inani { public long Funda() { return inani; } }
    private static void qiniseka(boolean isimo, String Igama) {
        if (!isimo) throw new AssertionError(Igama);
        System.out.println("PASS " + Igama);
    }
    public static void main(String[] 인수) throws Exception {
        String Itekisi = "한글 日本語 العربية हिन्दी 😀";
        Path Store_inani = Path.of(System.getProperty("user.home"), "ukufakazisa_imininingwane.txt");
        Ihele.Bhala(Store_inani, Itekisi);
        qiniseka(Ihele.Funda(Store_inani).equals(Itekisi), "UTF8_FILE");
        qiniseka(문자.코드포인트수("한😀") == 2, "UNICODE");
        qiniseka(문자.beka_kujwayeleke_inani("\u1100\u1161").equals("가"), "NORMALIZATION");
        inani into_inani = new ingane_inani();
        qiniseka(into_inani.Funda() == 42 && (long)ingane_inani.class.getMethod("Funda").invoke(into_inani) == 42, "OBJECT_INHERITANCE_REFLECTION");
        qiniseka(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("qinisekisa"); }
        catch (IOException 예외) { qiniseka(예외.getMessage().equals("qinisekisa"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread uhlu_lwemilayezo_inani = 작업.Sebenzisa("한글 uhlu_lwemilayezo_inani", () -> 합.set(123));
        작업.기다리기(uhlu_lwemilayezo_inani);
        qiniseka(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket Iseva_inani = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> phendula = 일꾼.submit(() -> {
                try (Socket 소켓 = Iseva_inani.accept()) {
                    BufferedReader Funda = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String umugqa;
                    while ((umugqa = Funda.readLine()) != null && !umugqa.isEmpty()) {}
                    byte[] umzimba_wombhalo = 문자.부호화(Itekisi);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + umzimba_wombhalo.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(umzimba_wombhalo);
                } catch (IOException Iphutha) { throw new UncheckedIOException(Iphutha); }
            });
            qiniseka(통신.가져오기(URI.create("http://127.0.0.1:" + Iseva_inani.getLocalPort()), Duration.ofSeconds(30)).body().equals(Itekisi), "HTTP_TCP");
            phendula.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        qiniseka(new ProcessBuilder("/bin/echo", "Inqubo_inani").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ubuso_bohlamvu_ifonti_inani = new Font("Dialog", Font.PLAIN, 18);
                qiniseka(ubuso_bohlamvu_ifonti_inani.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                qiniseka(ubuso_bohlamvu_ifonti_inani.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea indawo_yombhalo = new JTextArea(Itekisi);
                indawo_yombhalo.setFont(ubuso_bohlamvu_ifonti_inani);
                JFrame ifasitela = 화면.ifasitela("그래픽 qinisekisa", indawo_yombhalo, 800, 240);
                BufferedImage umdwebo_inani = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = umdwebo_inani.createGraphics();
                ifasitela.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(umdwebo_inani, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Iphutha) { throw new UncheckedIOException(Iphutha); }
                ifasitela.dispose();
                qiniseka(indawo_yombhalo.getText().equals(Itekisi), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
