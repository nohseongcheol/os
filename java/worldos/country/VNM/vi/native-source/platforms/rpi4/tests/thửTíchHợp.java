// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import tiếngViệt.Java.*;
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

public class thửTíchHợp {
    interface giáTrị { long đọc(); }
    static class giáTrịCha { protected long giáTrị = 42; }
    static class giáTrịCon extends giáTrịCha implements giáTrị { public long đọc() { return giáTrị; } }
    private static void xácMinh(boolean điềuKiện, String tên) {
        if (!điềuKiện) throw new AssertionError(tên);
        System.out.println("PASS " + tên);
    }
    public static void main(String[] cácĐốiSố) throws Exception {
        String vănBản = "한글 日本語 العربية हिन्दी 😀";
        Path giáTrịCất = Path.of(System.getProperty("user.home"), "dữLiệuViệcThẩmĐịnh.txt");
        Tệp.ghi(giáTrịCất, vănBản);
        xácMinh(Tệp.đọc(giáTrịCất).equals(vănBản), "UTF8_FILE");
        xácMinh(KýTự.sốLượngĐiểmMã("한😀") == 2, "UNICODE");
        xácMinh(KýTự.chuẩnHóaGiáTrị("\u1100\u1161").equals("가"), "NORMALIZATION");
        giáTrị giáTrịĐốiTượng = new giáTrịCon();
        xácMinh(giáTrịĐốiTượng.đọc() == 42 && (long)giáTrịCon.class.getMethod("đọc").invoke(giáTrịĐốiTượng) == 42, "OBJECT_INHERITANCE_REFLECTION");
        xácMinh(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("thẩmĐịnh"); }
        catch (IOException ngoạiLệ) { xácMinh(ngoạiLệ.getMessage().equals("thẩmĐịnh"), "EXCEPTION"); }
        AtomicInteger giáTrịTổng = new AtomicInteger();
        Thread giáTrịLuồngChạy = TácVụ.chạy("한글 giáTrịLuồngChạy", () -> giáTrịTổng.set(123));
        TácVụ.đợi(giáTrịLuồngChạy);
        xácMinh(giáTrịTổng.get() == 123, "THREAD");
        ExecutorService giáTrịBộLàmViệc = Executors.newSingleThreadExecutor();
        try (ServerSocket giáTrịMáyChủ = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> lờiĐáp = giáTrịBộLàmViệc.submit(() -> {
                try (Socket giáTrịỔCắmMạng = giáTrịMáyChủ.accept()) {
                    BufferedReader đọc = new BufferedReader(new InputStreamReader(giáTrịỔCắmMạng.getInputStream()));
                    String dòng;
                    while ((dòng = đọc.readLine()) != null && !dòng.isEmpty()) {}
                    byte[] vănBảnThân = KýTự.mãHóa(vănBản);
                    giáTrịỔCắmMạng.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + vănBảnThân.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    giáTrịỔCắmMạng.getOutputStream().write(vănBảnThân);
                } catch (IOException lỗi) { throw new UncheckedIOException(lỗi); }
            });
            xácMinh(TruyềnThông.giáTrịThu(URI.create("http://127.0.0.1:" + giáTrịMáyChủ.getLocalPort()), Duration.ofSeconds(30)).body().equals(vănBản), "HTTP_TCP");
            lờiĐáp.get(30, TimeUnit.SECONDS);
        } finally { giáTrịBộLàmViệc.shutdownNow(); }
        xácMinh(new ProcessBuilder("/bin/echo", "giáTrịTiếnTrình").start().waitFor() == 0, "PROCESS");
        if (cácĐốiSố.length > 0 && cácĐốiSố[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font giáTrịPhôngChữ = new Font("Dialog", Font.PLAIN, 18);
                xácMinh(giáTrịPhôngChữ.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                xácMinh(giáTrịPhôngChữ.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea HộpVănBản = new JTextArea(vănBản);
                HộpVănBản.setFont(giáTrịPhôngChữ);
                JFrame cửaSổ = MànHình.cửaSổ("그래픽 thẩmĐịnh", HộpVănBản, 800, 240);
                BufferedImage HìnhVẽ = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D giáTrịBútVẽ = HìnhVẽ.createGraphics();
                cửaSổ.paint(giáTrịBútVẽ); giáTrịBútVẽ.dispose();
                try { javax.imageio.ImageIO.write(HìnhVẽ, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException lỗi) { throw new UncheckedIOException(lỗi); }
                cửaSổ.dispose();
                xácMinh(HộpVănBản.getText().equals(vănBản), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
