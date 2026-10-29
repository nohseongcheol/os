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

public class 测试整合 {
    interface 值 { long 读取(); }
    static class 父值 { protected long 值 = 42; }
    static class 子值 extends 父值 implements 值 { public long 读取() { return 值; } }
    private static void 验证(boolean 条件, String 名称) {
        if (!条件) throw new AssertionError(名称);
        System.out.println("PASS " + 名称);
    }
    public static void main(String[] 实参) throws Exception {
        String 文本 = "한글 日本語 العربية हिन्दी 😀";
        Path 存储值 = Path.of(System.getProperty("user.home"), "有效性验证数据.txt");
        文件.写入(存储值, 文本);
        验证(文件.读取(存储值).equals(文本), "UTF8_FILE");
        验证(字符.代码分个数("한😀") == 2, "UNICODE");
        验证(字符.正规化值("\u1100\u1161").equals("가"), "NORMALIZATION");
        值 对象值 = new 子值();
        验证(对象值.读取() == 42 && (long)子值.class.getMethod("读取").invoke(对象值) == 42, "OBJECT_INHERITANCE_REFLECTION");
        验证(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("有效性校验"); }
        catch (IOException 异常) { 验证(异常.getMessage().equals("有效性校验"), "EXCEPTION"); }
        AtomicInteger 总和值 = new AtomicInteger();
        Thread 线程值 = 任务.运行("한글 线程值", () -> 总和值.set(123));
        任务.等待(线程值);
        验证(总和值.get() == 123, "THREAD");
        ExecutorService 后台任务值 = Executors.newSingleThreadExecutor();
        try (ServerSocket 服务器值 = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> 回复 = 后台任务值.submit(() -> {
                try (Socket 套接字值 = 服务器值.accept()) {
                    BufferedReader 读取 = new BufferedReader(new InputStreamReader(套接字值.getInputStream()));
                    String 行;
                    while ((行 = 读取.readLine()) != null && !行.isEmpty()) {}
                    byte[] 主体文本 = 字符.编码(文本);
                    套接字值.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + 主体文本.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    套接字值.getOutputStream().write(主体文本);
                } catch (IOException 错误) { throw new UncheckedIOException(错误); }
            });
            验证(通信.取用值(URI.create("http://127.0.0.1:" + 服务器值.getLocalPort()), Duration.ofSeconds(30)).body().equals(文本), "HTTP_TCP");
            回复.get(30, TimeUnit.SECONDS);
        } finally { 后台任务值.shutdownNow(); }
        验证(new ProcessBuilder("/bin/echo", "进程值").start().waitFor() == 0, "PROCESS");
        if (实参.length > 0 && 实参[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font 字体值 = new Font("Dialog", Font.PLAIN, 18);
                验证(字体值.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                验证(字体值.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea 文本框 = new JTextArea(文本);
                文本框.setFont(字体值);
                JFrame 窗口 = 屏幕.窗口("그래픽 有效性校验", 文本框, 800, 240);
                BufferedImage 绘图 = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 画笔值 = 绘图.createGraphics();
                窗口.paint(画笔值); 画笔值.dispose();
                try { javax.imageio.ImageIO.write(绘图, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException 错误) { throw new UncheckedIOException(错误); }
                窗口.dispose();
                验证(文本框.getText().equals(文本), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
