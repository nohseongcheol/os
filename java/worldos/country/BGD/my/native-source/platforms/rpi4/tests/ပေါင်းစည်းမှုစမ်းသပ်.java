// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import မြန်မာ.Java.*;
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

public class ပေါင်းစည်းမှုစမ်းသပ် {
    interface တန်ဖိုး { long ဖတ်(); }
    static class မိဘတန်ဖိုး { protected long တန်ဖိုး = 42; }
    static class သားသမီးတန်ဖိုး extends မိဘတန်ဖိုး implements တန်ဖိုး { public long ဖတ်() { return တန်ဖိုး; } }
    private static void အတည်ပြု(boolean အခြေအနေစည်းကမ်း, String အမည်) {
        if (!အခြေအနေစည်းကမ်း) throw new AssertionError(အမည်);
        System.out.println("PASS " + အမည်);
    }
    public static void main(String[] အချက်များ) throws Exception {
        String စာသား = "한글 日本語 العربية हिन्दी 😀";
        Path သိုလှောင်တန်ဖိုး = Path.of(System.getProperty("user.home"), "검증자료.txt");
        ဖိုင်.ရေး(သိုလှောင်တန်ဖိုး, စာသား);
        အတည်ပြု(ဖိုင်.ဖတ်(သိုလှောင်တန်ဖိုး).equals(စာသား), "UTF8_FILE");
        အတည်ပြု(အက္ခရာ.ကုဒ်အမှတ်တစ်ခုအရေအတွက်("한😀") == 2, "UNICODE");
        အတည်ပြု(အက္ခရာ.စံပုံစံပြောင်း("\u1100\u1161").equals("가"), "NORMALIZATION");
        တန်ဖိုး အရာဝတ္ထုတန်ဖိုး = new သားသမီးတန်ဖိုး();
        အတည်ပြု(အရာဝတ္ထုတန်ဖိုး.ဖတ်() == 42 && (long)သားသမီးတန်ဖိုး.class.getMethod("ဖတ်").invoke(အရာဝတ္ထုတန်ဖိုး) == 42, "OBJECT_INHERITANCE_REFLECTION");
        အတည်ပြု(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("မှန်ကန်ကြောင်းစစ်"); }
        catch (IOException ခြွင်းချက်) { အတည်ပြု(ခြွင်းချက်.getMessage().equals("မှန်ကန်ကြောင်းစစ်"), "EXCEPTION"); }
        AtomicInteger စုစုပေါင်းတန်ဖိုး = new AtomicInteger();
        Thread အလုပ်ကြိုးတန်ဖိုး = အလုပ်.လုပ်ဆောင်("한글 အလုပ်ကြိုးတန်ဖိုး", () -> စုစုပေါင်းတန်ဖိုး.set(123));
        အလုပ်.စောင့်(အလုပ်ကြိုးတန်ဖိုး);
        အတည်ပြု(စုစုပေါင်းတန်ဖိုး.get() == 123, "THREAD");
        ExecutorService အလုပ်သမားတန်ဖိုး = Executors.newSingleThreadExecutor();
        try (ServerSocket ဝန်ဆောင်စက်တန်ဖိုး = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> အကြောင်းပြန်ချက် = အလုပ်သမားတန်ဖိုး.submit(() -> {
                try (Socket ကွန်ရက်ပေါက်တန်ဖိုး = ဝန်ဆောင်စက်တန်ဖိုး.accept()) {
                    BufferedReader ဖတ် = new BufferedReader(new InputStreamReader(ကွန်ရက်ပေါက်တန်ဖိုး.getInputStream()));
                    String စာကြောင်း;
                    while ((စာကြောင်း = ဖတ်.readLine()) != null && !စာကြောင်း.isEmpty()) {}
                    byte[] ကိုယ်ထည်စာသား = အက္ခရာ.ကုဒ်သွင်း(စာသား);
                    ကွန်ရက်ပေါက်တန်ဖိုး.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + ကိုယ်ထည်စာသား.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    ကွန်ရက်ပေါက်တန်ဖိုး.getOutputStream().write(ကိုယ်ထည်စာသား);
                } catch (IOException အမှား) { throw new UncheckedIOException(အမှား); }
            });
            အတည်ပြု(ဆက်သွယ်မှု.တန်ဖိုးယူ(URI.create("http://127.0.0.1:" + ဝန်ဆောင်စက်တန်ဖိုး.getLocalPort()), Duration.ofSeconds(30)).body().equals(စာသား), "HTTP_TCP");
            အကြောင်းပြန်ချက်.get(30, TimeUnit.SECONDS);
        } finally { အလုပ်သမားတန်ဖိုး.shutdownNow(); }
        အတည်ပြု(new ProcessBuilder("/bin/echo", "လုပ်ငန်းစဉ်").start().waitFor() == 0, "PROCESS");
        if (အချက်များ.length > 0 && အချက်များ[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font စာလုံးပုံစံတန်ဖိုး = new Font("Dialog", Font.PLAIN, 18);
                အတည်ပြု(စာလုံးပုံစံတန်ဖိုး.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                အတည်ပြု(စာလုံးပုံစံတန်ဖိုး.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea စာသားသေတ္တာ = new JTextArea(စာသား);
                စာသားသေတ္တာ.setFont(စာလုံးပုံစံတန်ဖိုး);
                JFrame ဝင်း = မျက်နှာပြင်.ဝင်း("그래픽 မှန်ကန်ကြောင်းစစ်", စာသားသေတ္တာ, 800, 240);
                BufferedImage ပုံဆွဲမှု = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D စုတ်တံ = ပုံဆွဲမှု.createGraphics();
                ဝင်း.paint(စုတ်တံ); စုတ်တံ.dispose();
                try { javax.imageio.ImageIO.write(ပုံဆွဲမှု, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException အမှား) { throw new UncheckedIOException(အမှား); }
                ဝင်း.dispose();
                အတည်ပြု(စာသားသေတ္တာ.getText().equals(စာသား), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
