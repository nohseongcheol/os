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
    interface valuu { long Wepụta_ọzi(); }
    static class 부모 { protected long valuu = 42; }
    static class njìmebe_nnwā_valuu extends 부모 implements valuu { public long Wepụta_ọzi() { return valuu; } }
    private static void nkwàdo_eziokwū(boolean ọnọdụ, String Aha) {
        if (!ọnọdụ) throw new AssertionError(Aha);
        System.out.println("PASS " + Aha);
    }
    public static void main(String[] 인수) throws Exception {
        String SMS = "한글 日本語 العربية हिन्दी 😀";
        Path Store_valuu = Path.of(System.getProperty("user.home"), "nkwèputaonòdù_datà.txt");
        Faịlụ.Chekwaa_ozi(Store_valuu, SMS);
        nkwàdo_eziokwū(Faịlụ.Wepụta_ọzi(Store_valuu).equals(SMS), "UTF8_FILE");
        nkwàdo_eziokwū(문자.코드포인트수("한😀") == 2, "UNICODE");
        nkwàdo_eziokwū(문자.mèzima_valuu("\u1100\u1161").equals("가"), "NORMALIZATION");
        valuu ihe_valuu = new njìmebe_nnwā_valuu();
        nkwàdo_eziokwū(ihe_valuu.Wepụta_ọzi() == 42 && (long)njìmebe_nnwā_valuu.class.getMethod("Wepụta_ọzi").invoke(ihe_valuu) == 42, "OBJECT_INHERITANCE_REFLECTION");
        nkwàdo_eziokwū(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("mee_ịbanihe"); }
        catch (IOException 예외) { nkwàdo_eziokwū(예외.getMessage().equals("mee_ịbanihe"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread treèd_valuu = 작업.Bido("한글 treèd_valuu", () -> 합.set(123));
        작업.기다리기(treèd_valuu);
        nkwàdo_eziokwū(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket savà_valuu = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> nzaghachi = 일꾼.submit(() -> {
                try (Socket 소켓 = savà_valuu.accept()) {
                    BufferedReader Wepụta_ọzi = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String ahịrī;
                    while ((ahịrī = Wepụta_ọzi.readLine()) != null && !ahịrī.isEmpty()) {}
                    byte[] àhụngwè = 문자.부호화(SMS);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + àhụngwè.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(àhụngwè);
                } catch (IOException mmejọ) { throw new UncheckedIOException(mmejọ); }
            });
            nkwàdo_eziokwū(통신.가져오기(URI.create("http://127.0.0.1:" + savà_valuu.getLocalPort()), Duration.ofSeconds(30)).body().equals(SMS), "HTTP_TCP");
            nzaghachi.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        nkwàdo_eziokwū(new ProcessBuilder("/bin/echo", "ùsòrò_valuu_6712bde7").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ọnụndèe_valuu = new Font("Dialog", Font.PLAIN, 18);
                nkwàdo_eziokwū(ọnụndèe_valuu.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                nkwàdo_eziokwū(ọnụndèe_valuu.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea igbe_ngwe = new JTextArea(SMS);
                igbe_ngwe.setFont(ọnụndèe_valuu);
                JFrame windò = 화면.windò("그래픽 mee_ịbanihe", igbe_ngwe, 800, 240);
                BufferedImage osise_valuu = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = osise_valuu.createGraphics();
                windò.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(osise_valuu, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException mmejọ) { throw new UncheckedIOException(mmejọ); }
                windò.dispose();
                nkwàdo_eziokwū(igbe_ngwe.getText().equals(SMS), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
