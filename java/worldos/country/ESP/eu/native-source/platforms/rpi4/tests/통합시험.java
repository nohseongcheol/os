// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Euskara.자바.*;
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
    interface balio { long Irakurri(); }
    static class 부모 { protected long balio = 42; }
    static class haur_balio extends 부모 implements balio { public long Irakurri() { return balio; } }
    private static void egiaztatu(boolean baldintza, String Izena) {
        if (!baldintza) throw new AssertionError(Izena);
        System.out.println("PASS " + Izena);
    }
    public static void main(String[] Argumentuak) throws Exception {
        String Testua = "한글 日本語 العربية हिन्दी 😀";
        Path Store_balio = Path.of(System.getProperty("user.home"), "balidazio_datuak.txt");
        Fitxategia.Idatzi(Store_balio, Testua);
        egiaztatu(Fitxategia.Irakurri(Store_balio).equals(Testua), "UTF8_FILE");
        egiaztatu(문자.karaktere_kode_ZENBATU("한😀") == 2, "UNICODE");
        egiaztatu(문자.normalizatu_balio("\u1100\u1161").equals("가"), "NORMALIZATION");
        balio objektu_balio = new haur_balio();
        egiaztatu(objektu_balio.Irakurri() == 42 && (long)haur_balio.class.getMethod("Irakurri").invoke(objektu_balio) == 42, "OBJECT_INHERITANCE_REFLECTION");
        egiaztatu(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("baliozkotu"); }
        catch (IOException salbuespen) { egiaztatu(salbuespen.getMessage().equals("baliozkotu"), "EXCEPTION"); }
        AtomicInteger BATU_balio = new AtomicInteger();
        Thread hari_balio = 작업.Exekutatu_2("한글 hari_balio", () -> BATU_balio.set(123));
        작업.기다리기(hari_balio);
        egiaztatu(BATU_balio.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket zerbitzari_balio = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> erantzun = 일꾼.submit(() -> {
                try (Socket 소켓 = zerbitzari_balio.accept()) {
                    BufferedReader Irakurri = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Marra;
                    while ((Marra = Irakurri.readLine()) != null && !Marra.isEmpty()) {}
                    byte[] testu_nagusi = 문자.부호화(Testua);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + testu_nagusi.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(testu_nagusi);
                } catch (IOException errorea) { throw new UncheckedIOException(errorea); }
            });
            egiaztatu(통신.HARTU_balio(URI.create("http://127.0.0.1:" + zerbitzari_balio.getLocalPort()), Duration.ofSeconds(30)).body().equals(Testua), "HTTP_TCP");
            erantzun.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        egiaztatu(new ProcessBuilder("/bin/echo", "prozesu_balio").start().waitFor() == 0, "PROCESS");
        if (Argumentuak.length > 0 && Argumentuak[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font letra_tipo_balio = new Font("Dialog", Font.PLAIN, 18);
                egiaztatu(letra_tipo_balio.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                egiaztatu(letra_tipo_balio.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea testua_idazteko_eremu = new JTextArea(Testua);
                testua_idazteko_eremu.setFont(letra_tipo_balio);
                JFrame Leihoa = 화면.Leihoa("그래픽 baliozkotu", testua_idazteko_eremu, 800, 240);
                BufferedImage 그림 = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = 그림.createGraphics();
                Leihoa.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(그림, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException errorea) { throw new UncheckedIOException(errorea); }
                Leihoa.dispose();
                egiaztatu(testua_idazteko_eremu.getText().equals(Testua), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
