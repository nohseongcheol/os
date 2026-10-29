// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import magyar.자바.*;
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

public class teszt_integráció {
    interface ÉRTÉK { long Olvasás(); }
    static class szülő_ÉRTÉK { protected long ÉRTÉK = 42; }
    static class gyermek_ÉRTÉK extends szülő_ÉRTÉK implements ÉRTÉK { public long Olvasás() { return ÉRTÉK; } }
    private static void igazol(boolean állapot, String Név) {
        if (!állapot) throw new AssertionError(Név);
        System.out.println("PASS " + Név);
    }
    public static void main(String[] Argumentumok) throws Exception {
        String Szöveg = "한글 日本語 العربية हिन्दी 😀";
        Path tár_ÉRTÉK = Path.of(System.getProperty("user.home"), "ellenőrzés_adat.txt");
        Fájl.Írás(tár_ÉRTÉK, Szöveg);
        igazol(Fájl.Olvasás(tár_ÉRTÉK).equals(Szöveg), "UTF8_FILE");
        igazol(문자.kódpont_DARAB("한😀") == 2, "UNICODE");
        igazol(문자.normalizál_ÉRTÉK("\u1100\u1161").equals("가"), "NORMALIZATION");
        ÉRTÉK objektum_ÉRTÉK = new gyermek_ÉRTÉK();
        igazol(objektum_ÉRTÉK.Olvasás() == 42 && (long)gyermek_ÉRTÉK.class.getMethod("Olvasás").invoke(objektum_ÉRTÉK) == 42, "OBJECT_INHERITANCE_REFLECTION");
        igazol(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("ellenőriz"); }
        catch (IOException kivétel) { igazol(kivétel.getMessage().equals("ellenőriz"), "EXCEPTION"); }
        AtomicInteger SUM_ÉRTÉK = new AtomicInteger();
        Thread szál_ÉRTÉK = 작업.Futtatás("한글 szál_ÉRTÉK", () -> SUM_ÉRTÉK.set(123));
        작업.기다리기(szál_ÉRTÉK);
        igazol(SUM_ÉRTÉK.get() == 123, "THREAD");
        ExecutorService dolgozó_ÉRTÉK = Executors.newSingleThreadExecutor();
        try (ServerSocket kiszolgáló_ÉRTÉK = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> válasz = dolgozó_ÉRTÉK.submit(() -> {
                try (Socket szoftvercsatorna_ÉRTÉK = kiszolgáló_ÉRTÉK.accept()) {
                    BufferedReader Olvasás = new BufferedReader(new InputStreamReader(szoftvercsatorna_ÉRTÉK.getInputStream()));
                    String Vonal;
                    while ((Vonal = Olvasás.readLine()) != null && !Vonal.isEmpty()) {}
                    byte[] törzsszöveg = 문자.kódolás(Szöveg);
                    szoftvercsatorna_ÉRTÉK.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + törzsszöveg.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    szoftvercsatorna_ÉRTÉK.getOutputStream().write(törzsszöveg);
                } catch (IOException HIBA) { throw new UncheckedIOException(HIBA); }
            });
            igazol(kommunikáció.ÁTHELYEZ_ÉRTÉK(URI.create("http://127.0.0.1:" + kiszolgáló_ÉRTÉK.getLocalPort()), Duration.ofSeconds(30)).body().equals(Szöveg), "HTTP_TCP");
            válasz.get(30, TimeUnit.SECONDS);
        } finally { dolgozó_ÉRTÉK.shutdownNow(); }
        igazol(new ProcessBuilder("/bin/echo", "folyamat_ÉRTÉK").start().waitFor() == 0, "PROCESS");
        if (Argumentumok.length > 0 && Argumentumok[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font betűkészlet_ÉRTÉK = new Font("Dialog", Font.PLAIN, 18);
                igazol(betűkészlet_ÉRTÉK.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                igazol(betűkészlet_ÉRTÉK.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea szövegmező_d6e55852 = new JTextArea(Szöveg);
                szövegmező_d6e55852.setFont(betűkészlet_ÉRTÉK);
                JFrame Ablak = 화면.Ablak("그래픽 ellenőriz", szövegmező_d6e55852, 800, 240);
                BufferedImage rajz_ÉRTÉK = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = rajz_ÉRTÉK.createGraphics();
                Ablak.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(rajz_ÉRTÉK, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException HIBA) { throw new UncheckedIOException(HIBA); }
                Ablak.dispose();
                igazol(szövegmező_d6e55852.getText().equals(Szöveg), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
