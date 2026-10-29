// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Indonesia.자바.*;
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

public class 통합시험 {
    interface VALUE { long Baca(); }
    static class induk_VALUE { protected long VALUE = 42; }
    static class turunan_VALUE extends induk_VALUE implements VALUE { public long Baca() { return VALUE; } }
    private static void periksa(boolean kondisi, String Nama_2) {
        if (!kondisi) throw new AssertionError(Nama_2);
        System.out.println("PASS " + Nama_2);
    }
    public static void main(String[] argumen) throws Exception {
        String teks = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "validasi_data.txt");
        berkas.Tulis(Store_VALUE, teks);
        periksa(berkas.Baca(Store_VALUE).equals(teks), "UTF8_FILE");
        periksa(문자.poin_kode_COUNT("한😀") == 2, "UNICODE");
        periksa(문자.normalkan_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE objek_VALUE = new turunan_VALUE();
        periksa(objek_VALUE.Baca() == 42 && (long)turunan_VALUE.class.getMethod("Baca").invoke(objek_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        periksa(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("validasi"); }
        catch (IOException pengecualian) { periksa(pengecualian.getMessage().equals("validasi"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread alur_VALUE = 작업.jalankan("한글 alur_VALUE", () -> SUM_VALUE.set(123));
        작업.기다리기(alur_VALUE);
        periksa(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket server_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> balas = 일꾼.submit(() -> {
                try (Socket 소켓 = server_VALUE.accept()) {
                    BufferedReader Baca = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String baris_masukan;
                    while ((baris_masukan = Baca.readLine()) != null && !baris_masukan.isEmpty()) {}
                    byte[] teks_isi = 문자.부호화(teks);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + teks_isi.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(teks_isi);
                } catch (IOException galat) { throw new UncheckedIOException(galat); }
            });
            periksa(komunikasi.TAKE_VALUE(URI.create("http://127.0.0.1:" + server_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(teks), "HTTP_TCP");
            balas.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        periksa(new ProcessBuilder("/bin/echo", "Proses_VALUE").start().waitFor() == 0, "PROCESS");
        if (argumen.length > 0 && argumen[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font font_VALUE = new Font("Dialog", Font.PLAIN, 18);
                periksa(font_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                periksa(font_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea area_teks = new JTextArea(teks);
                area_teks.setFont(font_VALUE);
                JFrame Jendela = 화면.Jendela("그래픽 validasi", area_teks, 800, 240);
                BufferedImage gambar_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = gambar_VALUE.createGraphics();
                Jendela.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(gambar_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException galat) { throw new UncheckedIOException(galat); }
                Jendela.dispose();
                periksa(area_teks.getText().equals(teks), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
