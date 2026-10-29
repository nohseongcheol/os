// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Melayu.자바.*;
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

public class ujian_pengamiran {
    interface VALUE { long Baca(); }
    static class 부모 { protected long VALUE = 42; }
    static class anak_VALUE extends 부모 implements VALUE { public long Baca() { return VALUE; } }
    private static void tentu_sahkan(boolean syarat, String Nama) {
        if (!syarat) throw new AssertionError(Nama);
        System.out.println("PASS " + Nama);
    }
    public static void main(String[] 인수) throws Exception {
        String Teks = "한글 日本語 العربية हिन्दी 😀";
        Path stor_VALUE = Path.of(System.getProperty("user.home"), "pensahihan_data.txt");
        Fail.Tulis(stor_VALUE, Teks);
        tentu_sahkan(Fail.Baca(stor_VALUE).equals(Teks), "UTF8_FILE");
        tentu_sahkan(문자.titik_kod_COUNT("한😀") == 2, "UNICODE");
        tentu_sahkan(문자.menormalkan_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE objek_VALUE = new anak_VALUE();
        tentu_sahkan(objek_VALUE.Baca() == 42 && (long)anak_VALUE.class.getMethod("Baca").invoke(objek_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        tentu_sahkan(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("sahkan"); }
        catch (IOException pengecualian) { tentu_sahkan(pengecualian.getMessage().equals("sahkan"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread urutan_VALUE = 작업.Jalan("한글 urutan_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(urutan_VALUE);
        tentu_sahkan(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket pelayan_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> balas = 일꾼.submit(() -> {
                try (Socket 소켓 = pelayan_VALUE.accept()) {
                    BufferedReader Baca = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String baris;
                    while ((baris = Baca.readLine()) != null && !baris.isEmpty()) {}
                    byte[] teks_jasad = 문자.부호화(Teks);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + teks_jasad.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(teks_jasad);
                } catch (IOException RALAT) { throw new UncheckedIOException(RALAT); }
            });
            tentu_sahkan(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + pelayan_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Teks), "HTTP_TCP");
            balas.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        tentu_sahkan(new ProcessBuilder("/bin/echo", "Proses_VALUE").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font fon_VALUE = new Font("Dialog", Font.PLAIN, 18);
                tentu_sahkan(fon_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                tentu_sahkan(fon_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea kotak_teks = new JTextArea(Teks);
                kotak_teks.setFont(fon_VALUE);
                JFrame Tetingkap = 화면.Tetingkap("그래픽 sahkan", kotak_teks, 800, 240);
                BufferedImage lukisan_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = lukisan_VALUE.createGraphics();
                Tetingkap.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(lukisan_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException RALAT) { throw new UncheckedIOException(RALAT); }
                Tetingkap.dispose();
                tentu_sahkan(kotak_teks.getText().equals(Teks), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
