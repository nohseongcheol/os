// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import čeština.자바.*;
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

public class test_integrace {
    interface HODNOTA { long Čtení(); }
    static class nadřazený_HODNOTA { protected long HODNOTA = 42; }
    static class dítě_HODNOTA extends nadřazený_HODNOTA implements HODNOTA { public long Čtení() { return HODNOTA; } }
    private static void ověřit(boolean podmínka, String Název) {
        if (!podmínka) throw new AssertionError(Název);
        System.out.println("PASS " + Název);
    }
    public static void main(String[] argumenty) throws Exception {
        String text = "한글 日本語 العربية हिन्दी 😀";
        Path Store_HODNOTA = Path.of(System.getProperty("user.home"), "ověření_data.txt");
        název_souboru.Zápis(Store_HODNOTA, text);
        ověřit(název_souboru.Čtení(Store_HODNOTA).equals(text), "UTF8_FILE");
        ověřit(문자.bod_kódu_POČET("한😀") == 2, "UNICODE");
        ověřit(문자.normalizovat_HODNOTA("\u1100\u1161").equals("가"), "NORMALIZATION");
        HODNOTA objekt_HODNOTA = new dítě_HODNOTA();
        ověřit(objekt_HODNOTA.Čtení() == 42 && (long)dítě_HODNOTA.class.getMethod("Čtení").invoke(objekt_HODNOTA) == 42, "OBJECT_INHERITANCE_REFLECTION");
        ověřit(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("ověřit_5fb2b747"); }
        catch (IOException výjimka) { ověřit(výjimka.getMessage().equals("ověřit_5fb2b747"), "EXCEPTION"); }
        AtomicInteger SUMA_HODNOTA = new AtomicInteger();
        Thread vlákno_HODNOTA = 작업.Spustit_2("한글 vlákno_HODNOTA", () -> SUMA_HODNOTA.set(123));
        작업.기다리기(vlákno_HODNOTA);
        ověřit(SUMA_HODNOTA.get() == 123, "THREAD");
        ExecutorService pracovník_HODNOTA = Executors.newSingleThreadExecutor();
        try (ServerSocket server_HODNOTA = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> odezva = pracovník_HODNOTA.submit(() -> {
                try (Socket soket_HODNOTA = server_HODNOTA.accept()) {
                    BufferedReader Čtení = new BufferedReader(new InputStreamReader(soket_HODNOTA.getInputStream()));
                    String vstupní_řádek;
                    while ((vstupní_řádek = Čtení.readLine()) != null && !vstupní_řádek.isEmpty()) {}
                    byte[] základní_text = 문자.kódovat(text);
                    soket_HODNOTA.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + základní_text.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    soket_HODNOTA.getOutputStream().write(základní_text);
                } catch (IOException chyba) { throw new UncheckedIOException(chyba); }
            });
            ověřit(komunikace.VZÍT_HODNOTA(URI.create("http://127.0.0.1:" + server_HODNOTA.getLocalPort()), Duration.ofSeconds(30)).body().equals(text), "HTTP_TCP");
            odezva.get(30, TimeUnit.SECONDS);
        } finally { pracovník_HODNOTA.shutdownNow(); }
        ověřit(new ProcessBuilder("/bin/echo", "Proces_HODNOTA").start().waitFor() == 0, "PROCESS");
        if (argumenty.length > 0 && argumenty[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font písmo_HODNOTA = new Font("Dialog", Font.PLAIN, 18);
                ověřit(písmo_HODNOTA.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                ověřit(písmo_HODNOTA.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea textové_pole_d6e55852 = new JTextArea(text);
                textové_pole_d6e55852.setFont(písmo_HODNOTA);
                JFrame Okno = 화면.Okno("그래픽 ověřit_5fb2b747", textové_pole_d6e55852, 800, 240);
                BufferedImage kreslení_HODNOTA = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D štětec_HODNOTA = kreslení_HODNOTA.createGraphics();
                Okno.paint(štětec_HODNOTA); štětec_HODNOTA.dispose();
                try { javax.imageio.ImageIO.write(kreslení_HODNOTA, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException chyba) { throw new UncheckedIOException(chyba); }
                Okno.dispose();
                ověřit(textové_pole_d6e55852.getText().equals(text), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
