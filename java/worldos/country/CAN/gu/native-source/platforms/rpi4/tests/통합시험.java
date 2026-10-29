// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import ગુજરાતી.자바.*;
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
    interface મૂલ્ય { long વાંચો(); }
    static class 부모 { protected long મૂલ્ય = 42; }
    static class બાળક_મૂલ્ય extends 부모 implements મૂલ્ય { public long વાંચો() { return મૂલ્ય; } }
    private static void ચકાસવું(boolean શરત, String નામ) {
        if (!શરત) throw new AssertionError(નામ);
        System.out.println("PASS " + નામ);
    }
    public static void main(String[] દલીલો) throws Exception {
        String લખાણ = "한글 日本語 العربية हिन्दी 😀";
        Path સંગ્રહ_કરવો_મૂલ્ય = Path.of(System.getProperty("user.home"), "માન્યતા_ડેટા.txt");
        ફાઈલ.લખો(સંગ્રહ_કરવો_મૂલ્ય, લખાણ);
        ચકાસવું(ફાઈલ.વાંચો(સંગ્રહ_કરવો_મૂલ્ય).equals(લખાણ), "UTF8_FILE");
        ચકાસવું(문자.코드포인트수("한😀") == 2, "UNICODE");
        ચકાસવું(문자.સામાન્ય_બનાવો_મૂલ્ય("\u1100\u1161").equals("가"), "NORMALIZATION");
        મૂલ્ય ઑબ્જેક્ટ_મૂલ્ય = new બાળક_મૂલ્ય();
        ચકાસવું(ઑબ્જેક્ટ_મૂલ્ય.વાંચો() == 42 && (long)બાળક_મૂલ્ય.class.getMethod("વાંચો").invoke(ઑબ્જેક્ટ_મૂલ્ય) == 42, "OBJECT_INHERITANCE_REFLECTION");
        ચકાસવું(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("માન્ય_કરો"); }
        catch (IOException 예외) { ચકાસવું(예외.getMessage().equals("માન્ય_કરો"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread થ્રેડ_મૂલ્ય = 작업.ચલાવો_2("한글 થ્રેડ_મૂલ્ય", () -> 합.set(123));
        작업.기다리기(થ્રેડ_મૂલ્ય);
        ચકાસવું(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket સર્વર_મૂલ્ય = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> જવાબ = 일꾼.submit(() -> {
                try (Socket 소켓 = સર્વર_મૂલ્ય.accept()) {
                    BufferedReader વાંચો = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String લાઇન;
                    while ((લાઇન = વાંચો.readLine()) != null && !લાઇન.isEmpty()) {}
                    byte[] મુખ્ય_પાઠ = 문자.부호화(લખાણ);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + મુખ્ય_પાઠ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(મુખ્ય_પાઠ);
                } catch (IOException ભૂલ) { throw new UncheckedIOException(ભૂલ); }
            });
            ચકાસવું(통신.가져오기(URI.create("http://127.0.0.1:" + સર્વર_મૂલ્ય.getLocalPort()), Duration.ofSeconds(30)).body().equals(લખાણ), "HTTP_TCP");
            જવાબ.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        ચકાસવું(new ProcessBuilder("/bin/echo", "પ્રક્રિયા_મૂલ્ય").start().waitFor() == 0, "PROCESS");
        if (દલીલો.length > 0 && દલીલો[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ફૉન્ટ_મૂલ્ય = new Font("Dialog", Font.PLAIN, 18);
                ચકાસવું(ફૉન્ટ_મૂલ્ય.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                ચકાસવું(ફૉન્ટ_મૂલ્ય.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea પાઠ_બૉક્સ = new JTextArea(લખાણ);
                પાઠ_બૉક્સ.setFont(ફૉન્ટ_મૂલ્ય);
                JFrame વિંડો = 화면.વિંડો("그래픽 માન્ય_કરો", પાઠ_બૉક્સ, 800, 240);
                BufferedImage રેખાંકન_મૂલ્ય = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = રેખાંકન_મૂલ્ય.createGraphics();
                વિંડો.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(રેખાંકન_મૂલ્ય, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ભૂલ) { throw new UncheckedIOException(ભૂલ); }
                વિંડો.dispose();
                ચકાસવું(પાઠ_બૉક્સ.getText().equals(લખાણ), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
