// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Deutsch.Java.*;
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

public class integrationPrüfung {
    interface Wert { long lesen(); }
    static class elternknotenWert { protected long Wert = 42; }
    static class kindWert extends elternknotenWert implements Wert { public long lesen() { return Wert; } }
    private static void überprüfen(boolean bedingung, String Name) {
        if (!bedingung) throw new AssertionError(Name);
        System.out.println("PASS " + Name);
    }
    public static void main(String[] argumente) throws Exception {
        String Text = "한글 日本語 العربية हिन्दी 😀";
        Path ablegenDatenWert = Path.of(System.getProperty("user.home"), "validierungDaten.txt");
        Datei.schreiben(ablegenDatenWert, Text);
        überprüfen(Datei.lesen(ablegenDatenWert).equals(Text), "UTF8_FILE");
        überprüfen(Zeichen.kodePunktAnzahl("한😀") == 2, "UNICODE");
        überprüfen(Zeichen.wertNormalisieren("\u1100\u1161").equals("가"), "NORMALIZATION");
        Wert objektWert = new kindWert();
        überprüfen(objektWert.lesen() == 42 && (long)kindWert.class.getMethod("lesen").invoke(objektWert) == 42, "OBJECT_INHERITANCE_REFLECTION");
        überprüfen(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("validieren"); }
        catch (IOException ausnahme) { überprüfen(ausnahme.getMessage().equals("validieren"), "EXCEPTION"); }
        AtomicInteger summeWert = new AtomicInteger();
        Thread ausführungsfadenWert = Aufgabe.ausführenVorgang("한글 ausführungsfadenWert", () -> summeWert.set(123));
        Aufgabe.abwarten(ausführungsfadenWert);
        überprüfen(summeWert.get() == 123, "THREAD");
        ExecutorService hintergrundarbeiterWert = Executors.newSingleThreadExecutor();
        try (ServerSocket dienstanbieterWert = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> antwort = hintergrundarbeiterWert.submit(() -> {
                try (Socket netzbuchseWert = dienstanbieterWert.accept()) {
                    BufferedReader lesen = new BufferedReader(new InputStreamReader(netzbuchseWert.getInputStream()));
                    String zeile;
                    while ((zeile = lesen.readLine()) != null && !zeile.isEmpty()) {}
                    byte[] rumpfText = Zeichen.kodieren(Text);
                    netzbuchseWert.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + rumpfText.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    netzbuchseWert.getOutputStream().write(rumpfText);
                } catch (IOException fehler) { throw new UncheckedIOException(fehler); }
            });
            überprüfen(Kommunikation.entnehmenWert(URI.create("http://127.0.0.1:" + dienstanbieterWert.getLocalPort()), Duration.ofSeconds(30)).body().equals(Text), "HTTP_TCP");
            antwort.get(30, TimeUnit.SECONDS);
        } finally { hintergrundarbeiterWert.shutdownNow(); }
        überprüfen(new ProcessBuilder("/bin/echo", "prozessWert").start().waitFor() == 0, "PROCESS");
        if (argumente.length > 0 && argumente[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font schriftartWert = new Font("Dialog", Font.PLAIN, 18);
                überprüfen(schriftartWert.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                überprüfen(schriftartWert.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea TextKasten = new JTextArea(Text);
                TextKasten.setFont(schriftartWert);
                JFrame fenster = Bildschirm.fenster("그래픽 validieren", TextKasten, 800, 240);
                BufferedImage Zeichnung = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D pinselWert = Zeichnung.createGraphics();
                fenster.paint(pinselWert); pinselWert.dispose();
                try { javax.imageio.ImageIO.write(Zeichnung, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException fehler) { throw new UncheckedIOException(fehler); }
                fenster.dispose();
                überprüfen(TextKasten.getText().equals(Text), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
