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
    interface മൂല്യം { long വായന(); }
    static class 부모 { protected long മൂല്യം = 42; }
    static class കുട്ടി_മൂല്യം extends 부모 implements മൂല്യം { public long വായന() { return മൂല്യം; } }
    private static void പരിശോധിക്കുക(boolean അവസ്ഥ, String പേരു്) {
        if (!അവസ്ഥ) throw new AssertionError(പേരു്);
        System.out.println("PASS " + പേരു്);
    }
    public static void main(String[] 인수) throws Exception {
        String പദാവലി = "한글 日本語 العربية हिन्दी 😀";
        Path സ്_റ്റോർ_മൂല്യം = Path.of(System.getProperty("user.home"), "నిర్ధారణ_ഡാറ്റാ.txt");
        ഫയല്.എഴുത്തു്(സ്_റ്റോർ_മൂല്യം, പദാവലി);
        പരിശോധിക്കുക(ഫയല്.വായന(സ്_റ്റോർ_മൂല്യം).equals(പദാവലി), "UTF8_FILE");
        പരിശോധിക്കുക(문자.코드포인트수("한😀") == 2, "UNICODE");
        പരിശോധിക്കുക(문자.ക്രമാനുസരണമാക്കുക_മൂല്യം("\u1100\u1161").equals("가"), "NORMALIZATION");
        മൂല്യം ഓബ്ജക്റ്റ്_മൂല്യം = new കുട്ടി_മൂല്യം();
        പരിശോധിക്കുക(ഓബ്ജക്റ്റ്_മൂല്യം.വായന() == 42 && (long)കുട്ടി_മൂല്യം.class.getMethod("വായന").invoke(ഓബ്ജക്റ്റ്_മൂല്യം) == 42, "OBJECT_INHERITANCE_REFLECTION");
        പരിശോധിക്കുക(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("സാധൂകരിക്കുക"); }
        catch (IOException ഒഴിവാക്കൽ) { പരിശോധിക്കുക(ഒഴിവാക്കൽ.getMessage().equals("സാധൂകരിക്കുക"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread ത്രെഡ്_മൂല്യം = 작업.നടപ്പിലാക്കുക("한글 ത്രെഡ്_മൂല്യം", () -> 합.set(123));
        작업.기다리기(ത്രെഡ്_മൂല്യം);
        പരിശോധിക്കുക(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket സെര്_വര്_മൂല്യം = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> മറുപടി_നൽകുക = 일꾼.submit(() -> {
                try (Socket 소켓 = സെര്_വര്_മൂല്യം.accept()) {
                    BufferedReader വായന = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String ലൈൻ;
                    while ((ലൈൻ = വായന.readLine()) != null && !ലൈൻ.isEmpty()) {}
                    byte[] മുഖ്യ_പാഠം = 문자.부호화(പദാവലി);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + മുഖ്യ_പാഠം.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(മുഖ്യ_പാഠം);
                } catch (IOException പിശക്) { throw new UncheckedIOException(പിശക്); }
            });
            പരിശോധിക്കുക(통신.가져오기(URI.create("http://127.0.0.1:" + സെര്_വര്_മൂല്യം.getLocalPort()), Duration.ofSeconds(30)).body().equals(പദാവലി), "HTTP_TCP");
            മറുപടി_നൽകുക.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        പരിശോധിക്കുക(new ProcessBuilder("/bin/echo", "പ്രോസസ്_മൂല്യം").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ഫോണ്ട്_മൂല്യം = new Font("Dialog", Font.PLAIN, 18);
                പരിശോധിക്കുക(ഫോണ്ട്_മൂല്യം.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                പരിശോധിക്കുക(ഫോണ്ട്_മൂല്യം.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea ടെക്_സ്റ്റ്_ഏരിയ = new JTextArea(പദാവലി);
                ടെക്_സ്റ്റ്_ഏരിയ.setFont(ഫോണ്ട്_മൂല്യം);
                JFrame ജാലകം = 화면.ജാലകം("그래픽 സാധൂകരിക്കുക", ടെക്_സ്റ്റ്_ഏരിയ, 800, 240);
                BufferedImage ഡ്രോയിംഗ്_മൂല്യം = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = ഡ്രോയിംഗ്_മൂല്യം.createGraphics();
                ജാലകം.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(ഡ്രോയിംഗ്_മൂല്യം, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException പിശക്) { throw new UncheckedIOException(പിശക്); }
                ജാലകം.dispose();
                പരിശോധിക്കുക(ടെക്_സ്റ്റ്_ഏരിയ.getText().equals(പദാവലി), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
