// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import polski.자바.*;
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

public class test_całkowanie {
    interface WARTOŚĆ { long Odczyt(); }
    static class nadrzędny_WARTOŚĆ { protected long WARTOŚĆ = 42; }
    static class dziecko_WARTOŚĆ extends nadrzędny_WARTOŚĆ implements WARTOŚĆ { public long Odczyt() { return WARTOŚĆ; } }
    private static void 확인(boolean choroba, String Nazwa) {
        if (!choroba) throw new AssertionError(Nazwa);
        System.out.println("PASS " + Nazwa);
    }
    public static void main(String[] argumenty) throws Exception {
        String tekst = "한글 日本語 العربية हिन्दी 😀";
        Path Store_WARTOŚĆ = Path.of(System.getProperty("user.home"), "walidacja_dane.txt");
        nazwa_pliku.Zapis(Store_WARTOŚĆ, tekst);
        확인(nazwa_pliku.Odczyt(Store_WARTOŚĆ).equals(tekst), "UTF8_FILE");
        확인(문자.kod_znaku_ILE_LICZB("한😀") == 2, "UNICODE");
        확인(문자.normalizować_WARTOŚĆ("\u1100\u1161").equals("가"), "NORMALIZATION");
        WARTOŚĆ obiekt_WARTOŚĆ = new dziecko_WARTOŚĆ();
        확인(obiekt_WARTOŚĆ.Odczyt() == 42 && (long)dziecko_WARTOŚĆ.class.getMethod("Odczyt").invoke(obiekt_WARTOŚĆ) == 42, "OBJECT_INHERITANCE_REFLECTION");
        확인(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("walidować"); }
        catch (IOException wyjątek) { 확인(wyjątek.getMessage().equals("walidować"), "EXCEPTION"); }
        AtomicInteger SUMA_WARTOŚĆ = new AtomicInteger();
        Thread wątek_WARTOŚĆ = 작업.Uruchom_2("한글 wątek_WARTOŚĆ", () -> SUMA_WARTOŚĆ.set(123));
        작업.기다리기(wątek_WARTOŚĆ);
        확인(SUMA_WARTOŚĆ.get() == 123, "THREAD");
        ExecutorService pracownik_WARTOŚĆ = Executors.newSingleThreadExecutor();
        try (ServerSocket serwer_WARTOŚĆ = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> odpowiedź = pracownik_WARTOŚĆ.submit(() -> {
                try (Socket gniazdo_WARTOŚĆ = serwer_WARTOŚĆ.accept()) {
                    BufferedReader Odczyt = new BufferedReader(new InputStreamReader(gniazdo_WARTOŚĆ.getInputStream()));
                    String wiersz_wejścia;
                    while ((wiersz_wejścia = Odczyt.readLine()) != null && !wiersz_wejścia.isEmpty()) {}
                    byte[] tekst_podstawowy = 문자.kodować(tekst);
                    gniazdo_WARTOŚĆ.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + tekst_podstawowy.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    gniazdo_WARTOŚĆ.getOutputStream().write(tekst_podstawowy);
                } catch (IOException błąd) { throw new UncheckedIOException(błąd); }
            });
            확인(komunikacja.WYCINEK_WARTOŚĆ(URI.create("http://127.0.0.1:" + serwer_WARTOŚĆ.getLocalPort()), Duration.ofSeconds(30)).body().equals(tekst), "HTTP_TCP");
            odpowiedź.get(30, TimeUnit.SECONDS);
        } finally { pracownik_WARTOŚĆ.shutdownNow(); }
        확인(new ProcessBuilder("/bin/echo", "Proces_WARTOŚĆ").start().waitFor() == 0, "PROCESS");
        if (argumenty.length > 0 && argumenty[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font czcionka_WARTOŚĆ = new Font("Dialog", Font.PLAIN, 18);
                확인(czcionka_WARTOŚĆ.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                확인(czcionka_WARTOŚĆ.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea pole_edycji = new JTextArea(tekst);
                pole_edycji.setFont(czcionka_WARTOŚĆ);
                JFrame Okno = 화면.Okno("그래픽 walidować", pole_edycji, 800, 240);
                BufferedImage rysunek_WARTOŚĆ = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D pędzel_WARTOŚĆ = rysunek_WARTOŚĆ.createGraphics();
                Okno.paint(pędzel_WARTOŚĆ); pędzel_WARTOŚĆ.dispose();
                try { javax.imageio.ImageIO.write(rysunek_WARTOŚĆ, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException błąd) { throw new UncheckedIOException(błąd); }
                Okno.dispose();
                확인(pole_edycji.getText().equals(tekst), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
