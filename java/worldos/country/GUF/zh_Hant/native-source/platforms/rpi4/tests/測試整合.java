// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 中文.Java.*;
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

public class 測試整合 {
    interface 值 { long 讀取(); }
    static class 父值 { protected long 值 = 42; }
    static class 子值 extends 父值 implements 值 { public long 讀取() { return 值; } }
    private static void 驗證(boolean 條件, String 名稱) {
        if (!條件) throw new AssertionError(名稱);
        System.out.println("PASS " + 名稱);
    }
    public static void main(String[] 實參) throws Exception {
        String 文本 = "한글 日本語 العربية हिन्दी 😀";
        Path 存儲值 = Path.of(System.getProperty("user.home"), "有效性驗證資料.txt");
        檔案.寫入(存儲值, 文本);
        驗證(檔案.讀取(存儲值).equals(文本), "UTF8_FILE");
        驗證(字元.程式碼分個數("한😀") == 2, "UNICODE");
        驗證(字元.正規化值("\u1100\u1161").equals("가"), "NORMALIZATION");
        值 物件值 = new 子值();
        驗證(物件值.讀取() == 42 && (long)子值.class.getMethod("讀取").invoke(物件值) == 42, "OBJECT_INHERITANCE_REFLECTION");
        驗證(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("有效性校驗"); }
        catch (IOException 異常) { 驗證(異常.getMessage().equals("有效性校驗"), "EXCEPTION"); }
        AtomicInteger 總和值 = new AtomicInteger();
        Thread 執行緒值 = 任務.運行("한글 執行緒值", () -> 總和值.set(123));
        任務.等待(執行緒值);
        驗證(總和值.get() == 123, "THREAD");
        ExecutorService 後臺任務值 = Executors.newSingleThreadExecutor();
        try (ServerSocket 服務器值 = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> 回覆 = 後臺任務值.submit(() -> {
                try (Socket 通訊端值 = 服務器值.accept()) {
                    BufferedReader 讀取 = new BufferedReader(new InputStreamReader(通訊端值.getInputStream()));
                    String 行;
                    while ((行 = 讀取.readLine()) != null && !行.isEmpty()) {}
                    byte[] 主體文本 = 字元.編碼(文本);
                    通訊端值.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + 主體文本.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    通訊端值.getOutputStream().write(主體文本);
                } catch (IOException 錯誤) { throw new UncheckedIOException(錯誤); }
            });
            驗證(通信.取用值(URI.create("http://127.0.0.1:" + 服務器值.getLocalPort()), Duration.ofSeconds(30)).body().equals(文本), "HTTP_TCP");
            回覆.get(30, TimeUnit.SECONDS);
        } finally { 後臺任務值.shutdownNow(); }
        驗證(new ProcessBuilder("/bin/echo", "程序值").start().waitFor() == 0, "PROCESS");
        if (實參.length > 0 && 實參[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font 字體值 = new Font("Dialog", Font.PLAIN, 18);
                驗證(字體值.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                驗證(字體值.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea 文本框 = new JTextArea(文本);
                文本框.setFont(字體值);
                JFrame 窗口 = 屏幕.窗口("그래픽 有效性校驗", 文本框, 800, 240);
                BufferedImage 繪圖 = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 畫筆值 = 繪圖.createGraphics();
                窗口.paint(畫筆值); 畫筆值.dispose();
                try { javax.imageio.ImageIO.write(繪圖, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException 錯誤) { throw new UncheckedIOException(錯誤); }
                窗口.dispose();
                驗證(文本框.getText().equals(文本), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
