// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Nederlands.자바.*;
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

public class test_integratie {
    interface WAARDE { long Lezen(); }
    static class bovenliggend_WAARDE { protected long WAARDE = 42; }
    static class kind_WAARDE extends bovenliggend_WAARDE implements WAARDE { public long Lezen() { return WAARDE; } }
    private static void bevestigen(boolean toestand, String Naam) {
        if (!toestand) throw new AssertionError(Naam);
        System.out.println("PASS " + Naam);
    }
    public static void main(String[] argumenten) throws Exception {
        String tekst = "한글 日本語 العربية हिन्दी 😀";
        Path Store_WAARDE = Path.of(System.getProperty("user.home"), "validatie_gegevens.txt");
        bestand.Schrijven(Store_WAARDE, tekst);
        bevestigen(bestand.Lezen(Store_WAARDE).equals(tekst), "UTF8_FILE");
        bevestigen(문자.codepoint_AANTAL("한😀") == 2, "UNICODE");
        bevestigen(문자.normaliseren_WAARDE("\u1100\u1161").equals("가"), "NORMALIZATION");
        WAARDE object_WAARDE = new kind_WAARDE();
        bevestigen(object_WAARDE.Lezen() == 42 && (long)kind_WAARDE.class.getMethod("Lezen").invoke(object_WAARDE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        bevestigen(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("valideren"); }
        catch (IOException uitzondering) { bevestigen(uitzondering.getMessage().equals("valideren"), "EXCEPTION"); }
        AtomicInteger SOM_WAARDE = new AtomicInteger();
        Thread thread_WAARDE = 작업.starten("한글 thread_WAARDE", () -> SOM_WAARDE.set(123));
        작업.기다리기(thread_WAARDE);
        bevestigen(SOM_WAARDE.get() == 123, "THREAD");
        ExecutorService werkrol_WAARDE = Executors.newSingleThreadExecutor();
        try (ServerSocket server_WAARDE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> reactie = werkrol_WAARDE.submit(() -> {
                try (Socket socket_WAARDE = server_WAARDE.accept()) {
                    BufferedReader Lezen = new BufferedReader(new InputStreamReader(socket_WAARDE.getInputStream()));
                    String invoerregel;
                    while ((invoerregel = Lezen.readLine()) != null && !invoerregel.isEmpty()) {}
                    byte[] hoofdtekst = 문자.coderen(tekst);
                    socket_WAARDE.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + hoofdtekst.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    socket_WAARDE.getOutputStream().write(hoofdtekst);
                } catch (IOException fout) { throw new UncheckedIOException(fout); }
            });
            bevestigen(communicatie.NEMEN_WAARDE(URI.create("http://127.0.0.1:" + server_WAARDE.getLocalPort()), Duration.ofSeconds(30)).body().equals(tekst), "HTTP_TCP");
            reactie.get(30, TimeUnit.SECONDS);
        } finally { werkrol_WAARDE.shutdownNow(); }
        bevestigen(new ProcessBuilder("/bin/echo", "Proces_WAARDE").start().waitFor() == 0, "PROCESS");
        if (argumenten.length > 0 && argumenten[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font lettertype_WAARDE = new Font("Dialog", Font.PLAIN, 18);
                bevestigen(lettertype_WAARDE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                bevestigen(lettertype_WAARDE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea tekstvak = new JTextArea(tekst);
                tekstvak.setFont(lettertype_WAARDE);
                JFrame Venster = scherm.Venster("그래픽 valideren", tekstvak, 800, 240);
                BufferedImage tekening_WAARDE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = tekening_WAARDE.createGraphics();
                Venster.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(tekening_WAARDE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException fout) { throw new UncheckedIOException(fout); }
                Venster.dispose();
                bevestigen(tekstvak.getText().equals(tekst), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
