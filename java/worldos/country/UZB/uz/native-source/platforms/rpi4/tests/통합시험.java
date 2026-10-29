// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자바.*;
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
    interface VALUE { long Oʻqish(); }
    static class 부모 { protected long VALUE = 42; }
    static class farzand_VALUE extends 부모 implements VALUE { public long Oʻqish() { return VALUE; } }
    private static void tasdiqlamoq(boolean holat, String Nomi) {
        if (!holat) throw new AssertionError(Nomi);
        System.out.println("PASS " + Nomi);
    }
    public static void main(String[] 인수) throws Exception {
        String Matn = "한글 日本語 العربية हिन्दी 😀";
        Path Store_VALUE = Path.of(System.getProperty("user.home"), "tasdiq_ma_lumotlar.txt");
        Fayl.Yozish(Store_VALUE, Matn);
        tasdiqlamoq(Fayl.Oʻqish(Store_VALUE).equals(Matn), "UTF8_FILE");
        tasdiqlamoq(문자.belgi_kodi_COUNT("한😀") == 2, "UNICODE");
        tasdiqlamoq(문자.normallashtirmoq_VALUE("\u1100\u1161").equals("가"), "NORMALIZATION");
        VALUE obyekt_VALUE = new farzand_VALUE();
        tasdiqlamoq(obyekt_VALUE.Oʻqish() == 42 && (long)farzand_VALUE.class.getMethod("Oʻqish").invoke(obyekt_VALUE) == 42, "OBJECT_INHERITANCE_REFLECTION");
        tasdiqlamoq(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("tasdiqlash"); }
        catch (IOException istisno) { tasdiqlamoq(istisno.getMessage().equals("tasdiqlash"), "EXCEPTION"); }
        AtomicInteger SUM_VALUE = new AtomicInteger();
        Thread oqim_VALUE_5b72a632 = 작업.Bajarish("한글 oqim_VALUE_5b72a632", () -> SUM_VALUE.set(123));
        작업.기다리기(oqim_VALUE_5b72a632);
        tasdiqlamoq(SUM_VALUE.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket server_VALUE = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> javob_berish = 일꾼.submit(() -> {
                try (Socket 소켓 = server_VALUE.accept()) {
                    BufferedReader Oʻqish = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String satr;
                    while ((satr = Oʻqish.readLine()) != null && !satr.isEmpty()) {}
                    byte[] asosiy_matn = 문자.부호화(Matn);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + asosiy_matn.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(asosiy_matn);
                } catch (IOException Xato) { throw new UncheckedIOException(Xato); }
            });
            tasdiqlamoq(통신.TAKE_VALUE(URI.create("http://127.0.0.1:" + server_VALUE.getLocalPort()), Duration.ofSeconds(30)).body().equals(Matn), "HTTP_TCP");
            javob_berish.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        tasdiqlamoq(new ProcessBuilder("/bin/echo", "Jarayon_VALUE").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font shrift_VALUE = new Font("Dialog", Font.PLAIN, 18);
                tasdiqlamoq(shrift_VALUE.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                tasdiqlamoq(shrift_VALUE.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea matn_oynasi = new JTextArea(Matn);
                matn_oynasi.setFont(shrift_VALUE);
                JFrame oyna = 화면.oyna("그래픽 tasdiqlash", matn_oynasi, 800, 240);
                BufferedImage chizish_VALUE = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = chizish_VALUE.createGraphics();
                oyna.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(chizish_VALUE, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Xato) { throw new UncheckedIOException(Xato); }
                oyna.dispose();
                tasdiqlamoq(matn_oynasi.getText().equals(Matn), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
