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
    interface মান { long পড়া(); }
    static class 부모 { protected long মান = 42; }
    static class শিশু_মান extends 부모 implements মান { public long পড়া() { return মান; } }
    private static void প্ৰমাণিত_কৰক(boolean চৰ্ত, String নাম) {
        if (!চৰ্ত) throw new AssertionError(নাম);
        System.out.println("PASS " + নাম);
    }
    public static void main(String[] 인수) throws Exception {
        String টেক্সট = "한글 日本語 العربية हिन्दी 😀";
        Path জমা_কৰক_মান = Path.of(System.getProperty("user.home"), "বৈধতা_ডাটা.txt");
        নথিপত্ৰ.লিখা(জমা_কৰক_মান, টেক্সট);
        প্ৰমাণিত_কৰক(নথিপত্ৰ.পড়া(জমা_কৰক_মান).equals(টেক্সট), "UTF8_FILE");
        প্ৰমাণিত_কৰক(문자.코드포인트수("한😀") == 2, "UNICODE");
        প্ৰমাণিত_কৰক(문자.সাধাৰণীকৰণ_কৰক_মান("\u1100\u1161").equals("가"), "NORMALIZATION");
        মান অবজেক্ট_মান = new শিশু_মান();
        প্ৰমাণিত_কৰক(অবজেক্ট_মান.পড়া() == 42 && (long)শিশু_মান.class.getMethod("পড়া").invoke(অবজেক্ট_মান) == 42, "OBJECT_INHERITANCE_REFLECTION");
        প্ৰমাণিত_কৰক(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("বৈধকৰণ_কৰক"); }
        catch (IOException 예외) { প্ৰমাণিত_কৰক(예외.getMessage().equals("বৈধকৰণ_কৰক"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread আঁহ_মান = 작업.সঞ্চালন("한글 আঁহ_মান", () -> 합.set(123));
        작업.기다리기(আঁহ_মান);
        প্ৰমাণিত_কৰক(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket ছাৰ্ভাৰ_মান = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> প্ৰত্যুত্তৰ_দিয়ক = 일꾼.submit(() -> {
                try (Socket 소켓 = ছাৰ্ভাৰ_মান.accept()) {
                    BufferedReader পড়া = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String লাইন;
                    while ((লাইন = পড়া.readLine()) != null && !লাইন.isEmpty()) {}
                    byte[] মূল_পাঠ = 문자.부호화(টেক্সট);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + মূল_পাঠ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(মূল_পাঠ);
                } catch (IOException ত্ৰুটি) { throw new UncheckedIOException(ত্ৰুটি); }
            });
            প্ৰমাণিত_কৰক(통신.가져오기(URI.create("http://127.0.0.1:" + ছাৰ্ভাৰ_মান.getLocalPort()), Duration.ofSeconds(30)).body().equals(টেক্সট), "HTTP_TCP");
            প্ৰত্যুত্তৰ_দিয়ক.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        প্ৰমাণিত_কৰক(new ProcessBuilder("/bin/echo", "প্ৰক্ৰিয়া_মান").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ফ_ন্ট_মান = new Font("Dialog", Font.PLAIN, 18);
                প্ৰমাণিত_কৰক(ফ_ন্ট_মান.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                প্ৰমাণিত_কৰক(ফ_ন্ট_মান.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea পাঠ_বাকচ = new JTextArea(টেক্সট);
                পাঠ_বাকচ.setFont(ফ_ন্ট_মান);
                JFrame উইণ্ড = 화면.উইণ্ড("그래픽 বৈধকৰণ_কৰক", পাঠ_বাকচ, 800, 240);
                BufferedImage অংকন_মান = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = অংকন_মান.createGraphics();
                উইণ্ড.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(অংকন_মান, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ত্ৰুটি) { throw new UncheckedIOException(ত্ৰুটি); }
                উইণ্ড.dispose();
                প্ৰমাণিত_কৰক(পাঠ_বাকচ.getText().equals(টেক্সট), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
