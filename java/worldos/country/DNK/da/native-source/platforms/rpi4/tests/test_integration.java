// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Dansk.자바.*;
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
    interface VÆRDI { long Læse(); }
    static class overordnet_VÆRDI { protected long VÆRDI = 42; }
    static class barn_VÆRDI extends overordnet_VÆRDI implements VÆRDI { public long Læse() { return VÆRDI; } }
    private static void bekræfte(boolean lidelse, String Navn) {
        if (!lidelse) throw new AssertionError(Navn);
        System.out.println("PASS " + Navn);
    }
    public static void main(String[] Argumenter) throws Exception {
        String Tekst = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VÆRDI = Path.of(System.getProperty("user.home"), "validering_data.txt");
        Fil.Skrive(Store_VÆRDI, Tekst);
        bekræfte(Fil.Læse(Store_VÆRDI).equals(Tekst), "UTF8_FILE");
        bekræfte(문자.tegnkode_TÆL("한😀") == 2, "UNICODE");
        bekræfte(문자.normalisere_VÆRDI("\u1100\u1161").equals("가"), "NORMALIZATION");
        VÆRDI objekt_VÆRDI = new barn_VÆRDI();
        bekræfte(objekt_VÆRDI.Læse() == 42 && (long)barn_VÆRDI.class.getMethod("Læse").invoke(objekt_VÆRDI) == 42, "OBJECT_INHERITANCE_REFLECTION");
        bekræfte(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("bekræfte_5fb2b747"); }
        catch (IOException undtagelse) { bekræfte(undtagelse.getMessage().equals("bekræfte_5fb2b747"), "EXCEPTION"); }
        AtomicInteger SUM_VÆRDI = new AtomicInteger();
        Thread tråd_VÆRDI = 작업.Kør_2("한글 tråd_VÆRDI", () -> SUM_VÆRDI.set(123));
        작업.기다리기(tråd_VÆRDI);
        bekræfte(SUM_VÆRDI.get() == 123, "THREAD");
        ExecutorService arbejder_VÆRDI = Executors.newSingleThreadExecutor();
        try (ServerSocket server_VÆRDI = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> svar = arbejder_VÆRDI.submit(() -> {
                try (Socket socket_VÆRDI = server_VÆRDI.accept()) {
                    BufferedReader Læse = new BufferedReader(new InputStreamReader(socket_VÆRDI.getInputStream()));
                    String Linje;
                    while ((Linje = Læse.readLine()) != null && !Linje.isEmpty()) {}
                    byte[] brødtekst = 문자.kode(Tekst);
                    socket_VÆRDI.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + brødtekst.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    socket_VÆRDI.getOutputStream().write(brødtekst);
                } catch (IOException fejl) { throw new UncheckedIOException(fejl); }
            });
            bekræfte(통신.TAG_VÆRDI(URI.create("http://127.0.0.1:" + server_VÆRDI.getLocalPort()), Duration.ofSeconds(30)).body().equals(Tekst), "HTTP_TCP");
            svar.get(30, TimeUnit.SECONDS);
        } finally { arbejder_VÆRDI.shutdownNow(); }
        bekræfte(new ProcessBuilder("/bin/echo", "Proces_VÆRDI").start().waitFor() == 0, "PROCESS");
        if (Argumenter.length > 0 && Argumenter[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font skrifttype_VÆRDI = new Font("Dialog", Font.PLAIN, 18);
                bekræfte(skrifttype_VÆRDI.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                bekræfte(skrifttype_VÆRDI.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea tekstfelt_d6e55852 = new JTextArea(Tekst);
                tekstfelt_d6e55852.setFont(skrifttype_VÆRDI);
                JFrame Vindue = skærmbillede.Vindue("그래픽 bekræfte_5fb2b747", tekstfelt_d6e55852, 800, 240);
                BufferedImage tegning_VÆRDI = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D pensel_VÆRDI = tegning_VÆRDI.createGraphics();
                Vindue.paint(pensel_VÆRDI); pensel_VÆRDI.dispose();
                try { javax.imageio.ImageIO.write(tegning_VÆRDI, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException fejl) { throw new UncheckedIOException(fejl); }
                Vindue.dispose();
                bekræfte(tekstfelt_d6e55852.getText().equals(Tekst), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
