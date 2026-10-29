// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Svenska.자바.*;
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

public class test_integration {
    interface värde { long Läs(); }
    static class överordnad_värde { protected long värde = 42; }
    static class barn_värde extends överordnad_värde implements värde { public long Läs() { return värde; } }
    private static void verifiera(boolean villkor, String Namn) {
        if (!villkor) throw new AssertionError(Namn);
        System.out.println("PASS " + Namn);
    }
    public static void main(String[] argument) throws Exception {
        String text = "한글 日本語 العربية हिन्दी 😀";
        Path Store_värde = Path.of(System.getProperty("user.home"), "validering_data.txt");
        filnamn.Skriv(Store_värde, text);
        verifiera(filnamn.Läs(Store_värde).equals(text), "UTF8_FILE");
        verifiera(문자.kodpunkt_ANTAL("한😀") == 2, "UNICODE");
        verifiera(문자.normalisera_värde("\u1100\u1161").equals("가"), "NORMALIZATION");
        värde objekt_värde = new barn_värde();
        verifiera(objekt_värde.Läs() == 42 && (long)barn_värde.class.getMethod("Läs").invoke(objekt_värde) == 42, "OBJECT_INHERITANCE_REFLECTION");
        verifiera(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("validera"); }
        catch (IOException fel_31f743d2) { verifiera(fel_31f743d2.getMessage().equals("validera"), "EXCEPTION"); }
        AtomicInteger SUM_värde = new AtomicInteger();
        Thread tråd_värde = 작업.Kör("한글 tråd_värde", () -> SUM_värde.set(123));
        작업.기다리기(tråd_värde);
        verifiera(SUM_värde.get() == 123, "THREAD");
        ExecutorService arbete_värde = Executors.newSingleThreadExecutor();
        try (ServerSocket server_värde = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> svara = arbete_värde.submit(() -> {
                try (Socket socket_värde = server_värde.accept()) {
                    BufferedReader Läs = new BufferedReader(new InputStreamReader(socket_värde.getInputStream()));
                    String inmatningsrad;
                    while ((inmatningsrad = Läs.readLine()) != null && !inmatningsrad.isEmpty()) {}
                    byte[] brödtext = 문자.koda(text);
                    socket_värde.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + brödtext.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    socket_värde.getOutputStream().write(brödtext);
                } catch (IOException fel) { throw new UncheckedIOException(fel); }
            });
            verifiera(kommunikation.TA_värde(URI.create("http://127.0.0.1:" + server_värde.getLocalPort()), Duration.ofSeconds(30)).body().equals(text), "HTTP_TCP");
            svara.get(30, TimeUnit.SECONDS);
        } finally { arbete_värde.shutdownNow(); }
        verifiera(new ProcessBuilder("/bin/echo", "Process_värde").start().waitFor() == 0, "PROCESS");
        if (argument.length > 0 && argument[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font teckensnitt_värde = new Font("Dialog", Font.PLAIN, 18);
                verifiera(teckensnitt_värde.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                verifiera(teckensnitt_värde.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea textruta = new JTextArea(text);
                textruta.setFont(teckensnitt_värde);
                JFrame Fönster = skärmbild.Fönster("그래픽 validera", textruta, 800, 240);
                BufferedImage ritning_värde = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D pensel_värde = ritning_värde.createGraphics();
                Fönster.paint(pensel_värde); pensel_värde.dispose();
                try { javax.imageio.ImageIO.write(ritning_värde, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException fel) { throw new UncheckedIOException(fel); }
                Fönster.dispose();
                verifiera(textruta.getText().equals(text), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
