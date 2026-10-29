// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import বাংলা.자바.*;
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
    interface মান { long পড়া(); }
    static class 부모 { protected long মান = 42; }
    static class শিশু_মান extends 부모 implements মান { public long পড়া() { return মান; } }
    private static void যাচাই_করা(boolean শর্ত, String নাম) {
        if (!শর্ত) throw new AssertionError(নাম);
        System.out.println("PASS " + নাম);
    }
    public static void main(String[] আর্গুমেন্ট_তালিকা) throws Exception {
        String পাঠ = "한글 日本語 العربية हिन्दी 😀";
        Path ভাণ্ডার_মান = Path.of(System.getProperty("user.home"), "বৈধকরণ_ডাটা.txt");
        নথির_নাম.লেখা(ভাণ্ডার_মান, পাঠ);
        যাচাই_করা(নথির_নাম.পড়া(ভাণ্ডার_মান).equals(পাঠ), "UTF8_FILE");
        যাচাই_করা(문자.코드포인트수("한😀") == 2, "UNICODE");
        যাচাই_করা(문자.সাধারণকরণ_মান("\u1100\u1161").equals("가"), "NORMALIZATION");
        মান বস্তু_মান = new শিশু_মান();
        যাচাই_করা(বস্তু_মান.পড়া() == 42 && (long)শিশু_মান.class.getMethod("পড়া").invoke(বস্তু_মান) == 42, "OBJECT_INHERITANCE_REFLECTION");
        যাচাই_করা(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("বৈধ_করুন"); }
        catch (IOException ব্যতিক্রম) { যাচাই_করা(ব্যতিক্রম.getMessage().equals("বৈধ_করুন"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread থ্রেড_মান = 작업.চালনা("한글 থ্রেড_মান", () -> 합.set(123));
        작업.기다리기(থ্রেড_মান);
        যাচাই_করা(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket সার্ভার_মান = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> উত্তর_দিন = 일꾼.submit(() -> {
                try (Socket 소켓 = সার্ভার_মান.accept()) {
                    BufferedReader পড়া = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String নিবেশের_পঙ্_ক্তি;
                    while ((নিবেশের_পঙ্_ক্তি = পড়া.readLine()) != null && !নিবেশের_পঙ্_ক্তি.isEmpty()) {}
                    byte[] মুখ্য_পাঠ = 문자.부호화(পাঠ);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + মুখ্য_পাঠ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(মুখ্য_পাঠ);
                } catch (IOException ত্রুটি) { throw new UncheckedIOException(ত্রুটি); }
            });
            যাচাই_করা(통신.가져오기(URI.create("http://127.0.0.1:" + সার্ভার_মান.getLocalPort()), Duration.ofSeconds(30)).body().equals(পাঠ), "HTTP_TCP");
            উত্তর_দিন.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        যাচাই_করা(new ProcessBuilder("/bin/echo", "প্রসেসর_মান").start().waitFor() == 0, "PROCESS");
        if (আর্গুমেন্ট_তালিকা.length > 0 && আর্গুমেন্ট_তালিকা[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font হরফ_মান = new Font("Dialog", Font.PLAIN, 18);
                যাচাই_করা(হরফ_মান.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                যাচাই_করা(হরফ_মান.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea পাঠ_এলাকা = new JTextArea(পাঠ);
                পাঠ_এলাকা.setFont(হরফ_মান);
                JFrame উইন্ডো = 화면.উইন্ডো("그래픽 বৈধ_করুন", পাঠ_এলাকা, 800, 240);
                BufferedImage অঙ্কন_মান = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = অঙ্কন_মান.createGraphics();
                উইন্ডো.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(অঙ্কন_মান, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ত্রুটি) { throw new UncheckedIOException(ত্রুটি); }
                উইন্ডো.dispose();
                যাচাই_করা(পাঠ_এলাকা.getText().equals(পাঠ), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
