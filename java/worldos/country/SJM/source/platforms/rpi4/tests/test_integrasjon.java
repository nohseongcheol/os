// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import norsk.자바.*;
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

public class test_integrasjon {
    interface VERDI { long Les(); }
    static class overordnet_VERDI_881a8172 { protected long VERDI = 42; }
    static class barn_VERDI extends overordnet_VERDI_881a8172 implements VERDI { public long Les() { return VERDI; } }
    private static void bekrefte(boolean vilkår, String Navn) {
        if (!vilkår) throw new AssertionError(Navn);
        System.out.println("PASS " + Navn);
    }
    public static void main(String[] Argumenter) throws Exception {
        String Tekst = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VERDI = Path.of(System.getProperty("user.home"), "validering_data.txt");
        Fil.Skriv(Store_VERDI, Tekst);
        bekrefte(Fil.Les(Store_VERDI).equals(Tekst), "UTF8_FILE");
        bekrefte(문자.tegnkode_ANTALL("한😀") == 2, "UNICODE");
        bekrefte(문자.normalisere_VERDI("\u1100\u1161").equals("가"), "NORMALIZATION");
        VERDI objekt_VERDI = new barn_VERDI();
        bekrefte(objekt_VERDI.Les() == 42 && (long)barn_VERDI.class.getMethod("Les").invoke(objekt_VERDI) == 42, "OBJECT_INHERITANCE_REFLECTION");
        bekrefte(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("bekrefte_5fb2b747"); }
        catch (IOException unntak) { bekrefte(unntak.getMessage().equals("bekrefte_5fb2b747"), "EXCEPTION"); }
        AtomicInteger SUMMER_VERDI = new AtomicInteger();
        Thread tråd_VERDI = 작업.Kjør_2("한글 tråd_VERDI", () -> SUMMER_VERDI.set(123));
        작업.기다리기(tråd_VERDI);
        bekrefte(SUMMER_VERDI.get() == 123, "THREAD");
        ExecutorService arbeider_VERDI = Executors.newSingleThreadExecutor();
        try (ServerSocket server_VERDI = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> svar = arbeider_VERDI.submit(() -> {
                try (Socket socket_VERDI = server_VERDI.accept()) {
                    BufferedReader Les = new BufferedReader(new InputStreamReader(socket_VERDI.getInputStream()));
                    String Linje;
                    while ((Linje = Les.readLine()) != null && !Linje.isEmpty()) {}
                    byte[] brødtekst = 문자.부호화(Tekst);
                    socket_VERDI.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + brødtekst.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    socket_VERDI.getOutputStream().write(brødtekst);
                } catch (IOException feil) { throw new UncheckedIOException(feil); }
            });
            bekrefte(통신.TA_VERDI(URI.create("http://127.0.0.1:" + server_VERDI.getLocalPort()), Duration.ofSeconds(30)).body().equals(Tekst), "HTTP_TCP");
            svar.get(30, TimeUnit.SECONDS);
        } finally { arbeider_VERDI.shutdownNow(); }
        bekrefte(new ProcessBuilder("/bin/echo", "Prosess_VERDI").start().waitFor() == 0, "PROCESS");
        if (Argumenter.length > 0 && Argumenter[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font skrift_VERDI = new Font("Dialog", Font.PLAIN, 18);
                bekrefte(skrift_VERDI.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                bekrefte(skrift_VERDI.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea tekstboks = new JTextArea(Tekst);
                tekstboks.setFont(skrift_VERDI);
                JFrame Vindu = skjermbilde.Vindu("그래픽 bekrefte_5fb2b747", tekstboks, 800, 240);
                BufferedImage tegning_VERDI = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = tegning_VERDI.createGraphics();
                Vindu.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(tegning_VERDI, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException feil) { throw new UncheckedIOException(feil); }
                Vindu.dispose();
                bekrefte(tekstboks.getText().equals(Tekst), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
