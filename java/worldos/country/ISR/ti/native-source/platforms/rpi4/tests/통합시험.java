// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import ትግርኛ.자바.*;
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
    interface ዋጋ { long 읽기(); }
    static class 부모 { protected long ዋጋ = 42; }
    static class ቆልዓ_ዋጋ extends 부모 implements ዋጋ { public long 읽기() { return ዋጋ; } }
    private static void ኣረጋግጽ(boolean ኩነታት, String ሽም) {
        if (!ኩነታት) throw new AssertionError(ሽም);
        System.out.println("PASS " + ሽም);
    }
    public static void main(String[] 인수) throws Exception {
        String ጽሑፍ = "한글 日本語 العربية हिन्दी 😀";
        Path ከዝን_ዋጋ = Path.of(System.getProperty("user.home"), "ምርግጋፅ_ሓበሬታ.txt");
        ፋይል.ጸሓፍ(ከዝን_ዋጋ, ጽሑፍ);
        ኣረጋግጽ(ፋይል.읽기(ከዝን_ዋጋ).equals(ጽሑፍ), "UTF8_FILE");
        ኣረጋግጽ(문자.코드포인트수("한😀") == 2, "UNICODE");
        ኣረጋግጽ(문자.ኖርማላይዝ_ዋጋ("\u1100\u1161").equals("가"), "NORMALIZATION");
        ዋጋ ነገር_ዋጋ = new ቆልዓ_ዋጋ();
        ኣረጋግጽ(ነገር_ዋጋ.읽기() == 42 && (long)ቆልዓ_ዋጋ.class.getMethod("읽기").invoke(ነገር_ዋጋ) == 42, "OBJECT_INHERITANCE_REFLECTION");
        ኣረጋግጽ(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("አረጋግፅ"); }
        catch (IOException 예외) { ኣረጋግጽ(예외.getMessage().equals("አረጋግፅ"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread ፈትሊ_ዋጋ = 작업.ኣኺድ("한글 ፈትሊ_ዋጋ", () -> 합.set(123));
        작업.기다리기(ፈትሊ_ዋጋ);
        ኣረጋግጽ(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket ኣገልጋሊ_ዋጋ = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> መልስ = 일꾼.submit(() -> {
                try (Socket 소켓 = ኣገልጋሊ_ዋጋ.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String መስመር;
                    while ((መስመር = 읽기.readLine()) != null && !መስመር.isEmpty()) {}
                    byte[] ዋና_ጽሑፍ = 문자.부호화(ጽሑፍ);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + ዋና_ጽሑፍ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(ዋና_ጽሑፍ);
                } catch (IOException ጌጋ) { throw new UncheckedIOException(ጌጋ); }
            });
            ኣረጋግጽ(통신.가져오기(URI.create("http://127.0.0.1:" + ኣገልጋሊ_ዋጋ.getLocalPort()), Duration.ofSeconds(30)).body().equals(ጽሑፍ), "HTTP_TCP");
            መልስ.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        ኣረጋግጽ(new ProcessBuilder("/bin/echo", "መስርሕ_ዋጋ").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ቅርጺ_ፊደል_ዋጋ = new Font("Dialog", Font.PLAIN, 18);
                ኣረጋግጽ(ቅርጺ_ፊደል_ዋጋ.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                ኣረጋግጽ(ቅርጺ_ፊደል_ዋጋ.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea ቦታ_ጽሑፍ = new JTextArea(ጽሑፍ);
                ቦታ_ጽሑፍ.setFont(ቅርጺ_ፊደል_ዋጋ);
                JFrame መስኮት = 화면.መስኮት("그래픽 አረጋግፅ", ቦታ_ጽሑፍ, 800, 240);
                BufferedImage ስእሊ_ዋጋ = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = ስእሊ_ዋጋ.createGraphics();
                መስኮት.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(ስእሊ_ዋጋ, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ጌጋ) { throw new UncheckedIOException(ጌጋ); }
                መስኮት.dispose();
                ኣረጋግጽ(ቦታ_ጽሑፍ.getText().equals(ጽሑፍ), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
