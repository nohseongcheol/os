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
    interface thamani { long 읽기(); }
    static class 부모 { protected long thamani = 42; }
    static class mtoto_thamani extends 부모 implements thamani { public long 읽기() { return thamani; } }
    private static void thibitisha(boolean sharti, String Jina) {
        if (!sharti) throw new AssertionError(Jina);
        System.out.println("PASS " + Jina);
    }
    public static void main(String[] 인수) throws Exception {
        String SMS = "한글 日本語 العربية हिन्दी 😀";
        Path Store_thamani = Path.of(System.getProperty("user.home"), "uhakikishi_data.txt");
        faili.andika(Store_thamani, SMS);
        thibitisha(faili.읽기(Store_thamani).equals(SMS), "UTF8_FILE");
        thibitisha(문자.코드포인트수("한😀") == 2, "UNICODE");
        thibitisha(문자.kawaidisha_thamani("\u1100\u1161").equals("가"), "NORMALIZATION");
        thamani kipengee_thamani = new mtoto_thamani();
        thibitisha(kipengee_thamani.읽기() == 42 && (long)mtoto_thamani.class.getMethod("읽기").invoke(kipengee_thamani) == 42, "OBJECT_INHERITANCE_REFLECTION");
        thibitisha(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("hakikisha"); }
        catch (IOException vighairi) { thibitisha(vighairi.getMessage().equals("hakikisha"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread mtungo_thamani = 작업.endesha("한글 mtungo_thamani", () -> 합.set(123));
        작업.기다리기(mtungo_thamani);
        thibitisha(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket seva_thamani = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> jibu = 일꾼.submit(() -> {
                try (Socket 소켓 = seva_thamani.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String laini;
                    while ((laini = 읽기.readLine()) != null && !laini.isEmpty()) {}
                    byte[] Matini_kiini = 문자.부호화(SMS);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + Matini_kiini.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(Matini_kiini);
                } catch (IOException kosa) { throw new UncheckedIOException(kosa); }
            });
            thibitisha(통신.가져오기(URI.create("http://127.0.0.1:" + seva_thamani.getLocalPort()), Duration.ofSeconds(30)).body().equals(SMS), "HTTP_TCP");
            jibu.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        thibitisha(new ProcessBuilder("/bin/echo", "Mchakato_thamani").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font fonti_thamani = new Font("Dialog", Font.PLAIN, 18);
                thibitisha(fonti_thamani.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                thibitisha(fonti_thamani.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea eneo_la_matini = new JTextArea(SMS);
                eneo_la_matini.setFont(fonti_thamani);
                JFrame dirisha = 화면.dirisha("그래픽 hakikisha", eneo_la_matini, 800, 240);
                BufferedImage mchoro_thamani = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = mchoro_thamani.createGraphics();
                dirisha.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(mchoro_thamani, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException kosa) { throw new UncheckedIOException(kosa); }
                dirisha.dispose();
                thibitisha(eneo_la_matini.getText().equals(SMS), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
