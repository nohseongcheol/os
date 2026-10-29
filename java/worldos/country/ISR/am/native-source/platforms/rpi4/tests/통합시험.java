// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import አማርኛ.자바.*;
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
    interface እሴት { long ማንበቢያ(); }
    static class 부모 { protected long እሴት = 42; }
    static class ልጅ_እሴት extends 부모 implements እሴት { public long ማንበቢያ() { return እሴት; } }
    private static void አረጋግጥ(boolean ሁኔታ, String ስም) {
        if (!ሁኔታ) throw new AssertionError(ስም);
        System.out.println("PASS " + ስም);
    }
    public static void main(String[] 인수) throws Exception {
        String ጽሁፍ = "한글 日本語 العربية हिन्दी 😀";
        Path ማከማቻ_እሴት = Path.of(System.getProperty("user.home"), "ማረጋገጥ_ውሂብ.txt");
        ፋይል.መጻፊያ(ማከማቻ_እሴት, ጽሁፍ);
        አረጋግጥ(ፋይል.ማንበቢያ(ማከማቻ_እሴት).equals(ጽሁፍ), "UTF8_FILE");
        አረጋግጥ(문자.코드포인트수("한😀") == 2, "UNICODE");
        አረጋግጥ(문자.አጠናቅር_እሴት("\u1100\u1161").equals("가"), "NORMALIZATION");
        እሴት ነገር_እሴት = new ልጅ_እሴት();
        አረጋግጥ(ነገር_እሴት.ማንበቢያ() == 42 && (long)ልጅ_እሴት.class.getMethod("ማንበቢያ").invoke(ነገር_እሴት) == 42, "OBJECT_INHERITANCE_REFLECTION");
        አረጋግጥ(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("ትክክለኛነት_አረጋግጥ"); }
        catch (IOException ልዩነት) { አረጋግጥ(ልዩነት.getMessage().equals("ትክክለኛነት_አረጋግጥ"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread ክር_እሴት = 작업.ማስኬጃ("한글 ክር_እሴት", () -> 합.set(123));
        작업.기다리기(ክር_እሴት);
        አረጋግጥ(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket አገልጋይ_እሴት = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> መልስ = 일꾼.submit(() -> {
                try (Socket 소켓 = አገልጋይ_እሴት.accept()) {
                    BufferedReader ማንበቢያ = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String መስመር;
                    while ((መስመር = ማንበቢያ.readLine()) != null && !መስመር.isEmpty()) {}
                    byte[] የጽሁፍ_አካል = 문자.부호화(ጽሁፍ);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + የጽሁፍ_አካል.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(የጽሁፍ_አካል);
                } catch (IOException ስህተት) { throw new UncheckedIOException(ስህተት); }
            });
            አረጋግጥ(통신.가져오기(URI.create("http://127.0.0.1:" + አገልጋይ_እሴት.getLocalPort()), Duration.ofSeconds(30)).body().equals(ጽሁፍ), "HTTP_TCP");
            መልስ.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        አረጋግጥ(new ProcessBuilder("/bin/echo", "ሂደት_እሴት").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ቅርጸ_ቁምፊ_እሴት = new Font("Dialog", Font.PLAIN, 18);
                አረጋግጥ(ቅርጸ_ቁምፊ_እሴት.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                አረጋግጥ(ቅርጸ_ቁምፊ_እሴት.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea የጽሑፍ_ሳጥን = new JTextArea(ጽሁፍ);
                የጽሑፍ_ሳጥን.setFont(ቅርጸ_ቁምፊ_እሴት);
                JFrame መስኮት = 화면.መስኮት("그래픽 ትክክለኛነት_አረጋግጥ", የጽሑፍ_ሳጥን, 800, 240);
                BufferedImage ስዕል_እሴት = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = ስዕል_እሴት.createGraphics();
                መስኮት.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(ስዕል_እሴት, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ስህተት) { throw new UncheckedIOException(ስህተት); }
                መስኮት.dispose();
                አረጋግጥ(የጽሑፍ_ሳጥን.getText().equals(ጽሁፍ), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
