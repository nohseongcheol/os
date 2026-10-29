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
    interface តំលៃ { long អាន(); }
    static class 부모 { protected long តំលៃ = 42; }
    static class កូន_តំលៃ extends 부모 implements តំលៃ { public long អាន() { return តំលៃ; } }
    private static void ផ្ទៀងផ្ទាត់(boolean លក្ខខណ្ឌ, String ឈ្មោះ) {
        if (!លក្ខខណ្ឌ) throw new AssertionError(ឈ្មោះ);
        System.out.println("PASS " + ឈ្មោះ);
    }
    public static void main(String[] អាគុយម៉ង់) throws Exception {
        String អត្ថបទ = "한글 日本語 العربية हिन्दी 😀";
        Path ផ្ទុក_តំលៃ = Path.of(System.getProperty("user.home"), "សុពលភាព_ទិន្នន័យ.txt");
        ឯកសារ.សរសេរ(ផ្ទុក_តំលៃ, អត្ថបទ);
        ផ្ទៀងផ្ទាត់(ឯកសារ.អាន(ផ្ទុក_តំលៃ).equals(អត្ថបទ), "UTF8_FILE");
        ផ្ទៀងផ្ទាត់(문자.코드포인트수("한😀") == 2, "UNICODE");
        ផ្ទៀងផ្ទាត់(문자.ធ្វើអោយប្រក្រតី_តំលៃ("\u1100\u1161").equals("가"), "NORMALIZATION");
        តំលៃ វត្ថុ_តំលៃ = new កូន_តំលៃ();
        ផ្ទៀងផ្ទាត់(វត្ថុ_តំលៃ.អាន() == 42 && (long)កូន_តំលៃ.class.getMethod("អាន").invoke(វត្ថុ_តំលៃ) == 42, "OBJECT_INHERITANCE_REFLECTION");
        ផ្ទៀងផ្ទាត់(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("ធ្វើអោយមានសុពលភាព"); }
        catch (IOException ការលើកលែង) { ផ្ទៀងផ្ទាត់(ការលើកលែង.getMessage().equals("ធ្វើអោយមានសុពលភាព"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread ស្រេត_តំលៃ = 작업.រត់("한글 ស្រេត_តំលៃ", () -> 합.set(123));
        작업.기다리기(ស្រេត_តំលៃ);
        ផ្ទៀងផ្ទាត់(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket ម៉ាស៊ីនមេ_តំលៃ = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> ឆ្លើយតប = 일꾼.submit(() -> {
                try (Socket 소켓 = ម៉ាស៊ីនមេ_តំលៃ.accept()) {
                    BufferedReader អាន = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String បន្ទាត់;
                    while ((បន្ទាត់ = អាន.readLine()) != null && !បន្ទាត់.isEmpty()) {}
                    byte[] តួអត្ថបទ = 문자.부호화(អត្ថបទ);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + តួអត្ថបទ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(តួអត្ថបទ);
                } catch (IOException កំហុស) { throw new UncheckedIOException(កំហុស); }
            });
            ផ្ទៀងផ្ទាត់(통신.가져오기(URI.create("http://127.0.0.1:" + ម៉ាស៊ីនមេ_តំលៃ.getLocalPort()), Duration.ofSeconds(30)).body().equals(អត្ថបទ), "HTTP_TCP");
            ឆ្លើយតប.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        ផ្ទៀងផ្ទាត់(new ProcessBuilder("/bin/echo", "ដំណើរការ_តំលៃ").start().waitFor() == 0, "PROCESS");
        if (អាគុយម៉ង់.length > 0 && អាគុយម៉ង់[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ពុម្ពអក្សរ_តំលៃ = new Font("Dialog", Font.PLAIN, 18);
                ផ្ទៀងផ្ទាត់(ពុម្ពអក្សរ_តំលៃ.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                ផ្ទៀងផ្ទាត់(ពុម្ពអក្សរ_តំលៃ.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea ប្រអប់អត្ថបទ = new JTextArea(អត្ថបទ);
                ប្រអប់អត្ថបទ.setFont(ពុម្ពអក្សរ_តំលៃ);
                JFrame វីនដូ = 화면.វីនដូ("그래픽 ធ្វើអោយមានសុពលភាព", ប្រអប់អត្ថបទ, 800, 240);
                BufferedImage ការគូរ_តំលៃ = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = ការគូរ_តំលៃ.createGraphics();
                វីនដូ.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(ការគូរ_តំលៃ, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException កំហុស) { throw new UncheckedIOException(កំហុស); }
                វីនដូ.dispose();
                ផ្ទៀងផ្ទាត់(ប្រអប់អត្ថបទ.getText().equals(អត្ថបទ), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
