// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import ਪੰਜਾਬੀ.자바.*;
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
    interface ਕੀਮਤ { long ਪੜ੍ਹਨ(); }
    static class 부모 { protected long ਕੀਮਤ = 42; }
    static class ਚਾਈਲਡ_ਕੀਮਤ extends 부모 implements ਕੀਮਤ { public long ਪੜ੍ਹਨ() { return ਕੀਮਤ; } }
    private static void ਤਸਦੀਕ(boolean ਸ਼ਰਤ, String ਨਾਂ) {
        if (!ਸ਼ਰਤ) throw new AssertionError(ਨਾਂ);
        System.out.println("PASS " + ਨਾਂ);
    }
    public static void main(String[] ਆਰਗੂਮੈਂਟ) throws Exception {
        String ਟੈਕਸਟ = "한글 日本語 العربية हिन्दी 😀";
        Path ਸੰਭਾਲੋ_ਕੀਮਤ = Path.of(System.getProperty("user.home"), "ਮਾਨਤਾ_ਸਮੱਗਰੀ.txt");
        ਫਾਇਲ.ਲਿਖਣ(ਸੰਭਾਲੋ_ਕੀਮਤ, ਟੈਕਸਟ);
        ਤਸਦੀਕ(ਫਾਇਲ.ਪੜ੍ਹਨ(ਸੰਭਾਲੋ_ਕੀਮਤ).equals(ਟੈਕਸਟ), "UTF8_FILE");
        ਤਸਦੀਕ(문자.코드포인트수("한😀") == 2, "UNICODE");
        ਤਸਦੀਕ(문자.ਸਧਾਰਨ_ਬਨਾਉਣਾ_ਕੀਮਤ("\u1100\u1161").equals("가"), "NORMALIZATION");
        ਕੀਮਤ ਔਬਜੈਕਟ_ਕੀਮਤ = new ਚਾਈਲਡ_ਕੀਮਤ();
        ਤਸਦੀਕ(ਔਬਜੈਕਟ_ਕੀਮਤ.ਪੜ੍ਹਨ() == 42 && (long)ਚਾਈਲਡ_ਕੀਮਤ.class.getMethod("ਪੜ੍ਹਨ").invoke(ਔਬਜੈਕਟ_ਕੀਮਤ) == 42, "OBJECT_INHERITANCE_REFLECTION");
        ਤਸਦੀਕ(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("ਪ੍ਰਮਾਣਿਤ"); }
        catch (IOException 예외) { ਤਸਦੀਕ(예외.getMessage().equals("ਪ੍ਰਮਾਣਿਤ"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread ਥ੍ਰੈਡ_ਕੀਮਤ = 작업.ਚਲਾਓ_2("한글 ਥ੍ਰੈਡ_ਕੀਮਤ", () -> 합.set(123));
        작업.기다리기(ਥ੍ਰੈਡ_ਕੀਮਤ);
        ਤਸਦੀਕ(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket ਸਰਵਰ_ਕੀਮਤ = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> ਜਵਾਬ_ਦਿਓ = 일꾼.submit(() -> {
                try (Socket 소켓 = ਸਰਵਰ_ਕੀਮਤ.accept()) {
                    BufferedReader ਪੜ੍ਹਨ = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String ਲਾਈਨ;
                    while ((ਲਾਈਨ = ਪੜ੍ਹਨ.readLine()) != null && !ਲਾਈਨ.isEmpty()) {}
                    byte[] ਮੁੱਖ_ਪਾਠ = 문자.부호화(ਟੈਕਸਟ);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + ਮੁੱਖ_ਪਾਠ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(ਮੁੱਖ_ਪਾਠ);
                } catch (IOException ਗਲਤੀ) { throw new UncheckedIOException(ਗਲਤੀ); }
            });
            ਤਸਦੀਕ(통신.가져오기(URI.create("http://127.0.0.1:" + ਸਰਵਰ_ਕੀਮਤ.getLocalPort()), Duration.ofSeconds(30)).body().equals(ਟੈਕਸਟ), "HTTP_TCP");
            ਜਵਾਬ_ਦਿਓ.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        ਤਸਦੀਕ(new ProcessBuilder("/bin/echo", "ਕਾਰਵਾਈ_ਕੀਮਤ").start().waitFor() == 0, "PROCESS");
        if (ਆਰਗੂਮੈਂਟ.length > 0 && ਆਰਗੂਮੈਂਟ[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ਫੌਂਟ_ਕੀਮਤ = new Font("Dialog", Font.PLAIN, 18);
                ਤਸਦੀਕ(ਫੌਂਟ_ਕੀਮਤ.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                ਤਸਦੀਕ(ਫੌਂਟ_ਕੀਮਤ.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea ਟੈਕਸਟ_ਖੇਤਰ_d6e55852 = new JTextArea(ਟੈਕਸਟ);
                ਟੈਕਸਟ_ਖੇਤਰ_d6e55852.setFont(ਫੌਂਟ_ਕੀਮਤ);
                JFrame ਵਿੰਡੋ = 화면.ਵਿੰਡੋ("그래픽 ਪ੍ਰਮਾਣਿਤ", ਟੈਕਸਟ_ਖੇਤਰ_d6e55852, 800, 240);
                BufferedImage ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ.createGraphics();
                ਵਿੰਡੋ.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ਗਲਤੀ) { throw new UncheckedIOException(ਗਲਤੀ); }
                ਵਿੰਡੋ.dispose();
                ਤਸਦੀਕ(ਟੈਕਸਟ_ਖੇਤਰ_d6e55852.getText().equals(ਟੈਕਸਟ), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
