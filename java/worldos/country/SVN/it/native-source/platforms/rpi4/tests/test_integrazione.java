// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Italiano.자바.*;
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

public class test_integrazione {
    interface VALORE { long Lettura(); }
    static class padre_VALORE { protected long VALORE = 42; }
    static class figlio_VALORE extends padre_VALORE implements VALORE { public long Lettura() { return VALORE; } }
    private static void verificare(boolean condizione, String Nome) {
        if (!condizione) throw new AssertionError(Nome);
        System.out.println("PASS " + Nome);
    }
    public static void main(String[] argomenti) throws Exception {
        String testo = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALORE = Path.of(System.getProperty("user.home"), "convalida_dati.txt");
        file.Scrittura(Store_VALORE, testo);
        verificare(file.Lettura(Store_VALORE).equals(testo), "UTF8_FILE");
        verificare(문자.punto_di_codice_CONTA_NUMERI("한😀") == 2, "UNICODE");
        verificare(문자.normalizzare_VALORE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALORE oggetto_VALORE = new figlio_VALORE();
        verificare(oggetto_VALORE.Lettura() == 42 && (long)figlio_VALORE.class.getMethod("Lettura").invoke(oggetto_VALORE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        verificare(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("convalidare"); }
        catch (IOException eccezione) { verificare(eccezione.getMessage().equals("convalidare"), "EXCEPTION"); }
        AtomicInteger SUM_VALORE = new AtomicInteger();
        Thread thread_VALORE = 작업.avvia("한글 thread_VALORE", () -> SUM_VALORE.set(123));
        작업.기다리기(thread_VALORE);
        verificare(SUM_VALORE.get() == 123, "THREAD");
        ExecutorService lavoratore_VALORE = Executors.newSingleThreadExecutor();
        try (ServerSocket server_VALORE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> replica = lavoratore_VALORE.submit(() -> {
                try (Socket socket_VALORE = server_VALORE.accept()) {
                    BufferedReader Lettura = new BufferedReader(new InputStreamReader(socket_VALORE.getInputStream()));
                    String riga_di_ingresso;
                    while ((riga_di_ingresso = Lettura.readLine()) != null && !riga_di_ingresso.isEmpty()) {}
                    byte[] corpo_del_testo = 문자.codificare(testo);
                    socket_VALORE.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + corpo_del_testo.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    socket_VALORE.getOutputStream().write(corpo_del_testo);
                } catch (IOException errore) { throw new UncheckedIOException(errore); }
            });
            verificare(comunicazione.INCLUDI_VALORE(URI.create("http://127.0.0.1:" + server_VALORE.getLocalPort()), Duration.ofSeconds(30)).body().equals(testo), "HTTP_TCP");
            replica.get(30, TimeUnit.SECONDS);
        } finally { lavoratore_VALORE.shutdownNow(); }
        verificare(new ProcessBuilder("/bin/echo", "Processi_VALORE").start().waitFor() == 0, "PROCESS");
        if (argomenti.length > 0 && argomenti[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font tipo_di_carattere_VALORE = new Font("Dialog", Font.PLAIN, 18);
                verificare(tipo_di_carattere_VALORE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                verificare(tipo_di_carattere_VALORE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea area_di_testo = new JTextArea(testo);
                area_di_testo.setFont(tipo_di_carattere_VALORE);
                JFrame Finestra = schermata.Finestra("그래픽 convalidare", area_di_testo, 800, 240);
                BufferedImage disegno_VALORE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D pennello_VALORE = disegno_VALORE.createGraphics();
                Finestra.paint(pennello_VALORE); pennello_VALORE.dispose();
                try { javax.imageio.ImageIO.write(disegno_VALORE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException errore) { throw new UncheckedIOException(errore); }
                Finestra.dispose();
                verificare(area_di_testo.getText().equals(testo), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
