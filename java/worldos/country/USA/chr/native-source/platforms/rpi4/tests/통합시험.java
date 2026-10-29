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
    interface ᏧᎬᏩᎶᏗᏯ { long 읽기(); }
    static class 부모 { protected long ᏧᎬᏩᎶᏗᏯ = 42; }
    static class 자식 extends 부모 implements ᏧᎬᏩᎶᏗᏯ { public long 읽기() { return ᏧᎬᏩᎶᏗᏯ; } }
    private static void ᎰᎯᏳᏓ(boolean ᎤᏍᏗᏓᏅ, String ᏚᏙᎥᎢ) {
        if (!ᎤᏍᏗᏓᏅ) throw new AssertionError(ᏚᏙᎥᎢ);
        System.out.println("PASS " + ᏚᏙᎥᎢ);
    }
    public static void main(String[] 인수) throws Exception {
        String ᎠᎪᎵᏰᏗ = "한글 日本語 العربية हिन्दी 😀";
        Path Store_ᏧᎬᏩᎶᏗᏯ = Path.of(System.getProperty("user.home"), "ᎤᏙᎯᏳᏒᎢ_ᎦᏟᏌᏅᎯ.txt");
        ᎠᏍᏆᏂᎪᏙᏗ.ᎪᏪᎶᏗ(Store_ᏧᎬᏩᎶᏗᏯ, ᎠᎪᎵᏰᏗ);
        ᎰᎯᏳᏓ(ᎠᏍᏆᏂᎪᏙᏗ.읽기(Store_ᏧᎬᏩᎶᏗᏯ).equals(ᎠᎪᎵᏰᏗ), "UTF8_FILE");
        ᎰᎯᏳᏓ(문자.코드포인트수("한😀") == 2, "UNICODE");
        ᎰᎯᏳᏓ(문자.정규화("\u1100\u1161").equals("가"), "NORMALIZATION");
        ᏧᎬᏩᎶᏗᏯ ᎪᎱᏍᏗ_ᏧᎬᏩᎶᏗᏯ = new 자식();
        ᎰᎯᏳᏓ(ᎪᎱᏍᏗ_ᏧᎬᏩᎶᏗᏯ.읽기() == 42 && (long)자식.class.getMethod("읽기").invoke(ᎪᎱᏍᏗ_ᏧᎬᏩᎶᏗᏯ) == 42, "OBJECT_INHERITANCE_REFLECTION");
        ᎰᎯᏳᏓ(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("ᎪᎯᏳᏙᏗ"); }
        catch (IOException 예외) { ᎰᎯᏳᏓ(예외.getMessage().equals("ᎪᎯᏳᏙᏗ"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ = 작업.ᎠᎢᏎᏍᏗ("한글 ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ", () -> 합.set(123));
        작업.기다리기(ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ);
        ᎰᎯᏳᏓ(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> 응답 = 일꾼.submit(() -> {
                try (Socket 소켓 = ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String ᏚᏓᏅᏅᎢ;
                    while ((ᏚᏓᏅᏅᎢ = 읽기.readLine()) != null && !ᏚᏓᏅᏅᎢ.isEmpty()) {}
                    byte[] 본문 = 문자.부호화(ᎠᎪᎵᏰᏗ);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + 본문.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(본문);
                } catch (IOException ᎦᎵᏓᏍᏔᏅ) { throw new UncheckedIOException(ᎦᎵᏓᏍᏔᏅ); }
            });
            ᎰᎯᏳᏓ(통신.가져오기(URI.create("http://127.0.0.1:" + ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.getLocalPort()), Duration.ofSeconds(30)).body().equals(ᎠᎪᎵᏰᏗ), "HTTP_TCP");
            응답.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        ᎰᎯᏳᏓ(new ProcessBuilder("/bin/echo", "ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ = new Font("Dialog", Font.PLAIN, 18);
                ᎰᎯᏳᏓ(ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                ᎰᎯᏳᏓ(ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea 글상자 = new JTextArea(ᎠᎪᎵᏰᏗ);
                글상자.setFont(ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ);
                JFrame ᏦᎳᏂ = 화면.ᏦᎳᏂ("그래픽 ᎪᎯᏳᏙᏗ", 글상자, 800, 240);
                BufferedImage ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ.createGraphics();
                ᏦᎳᏂ.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ᎦᎵᏓᏍᏔᏅ) { throw new UncheckedIOException(ᎦᎵᏓᏍᏔᏅ); }
                ᏦᎳᏂ.dispose();
                ᎰᎯᏳᏓ(글상자.getText().equals(ᎠᎪᎵᏰᏗ), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
