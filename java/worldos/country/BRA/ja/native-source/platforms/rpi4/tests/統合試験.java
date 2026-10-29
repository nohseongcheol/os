// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 日本語.Java.*;
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

public class 統合試験 {
    interface 値 { long 読取(); }
    static class 親値 { protected long 値 = 42; }
    static class 子値 extends 親値 implements 値 { public long 読取() { return 値; } }
    private static void 検証(boolean 条件, String 名前) {
        if (!条件) throw new AssertionError(名前);
        System.out.println("PASS " + 名前);
    }
    public static void main(String[] 引数) throws Exception {
        String 文 = "한글 日本語 العربية हिन्दी 😀";
        Path 格納値 = Path.of(System.getProperty("user.home"), "妥当性データ.txt");
        ファイル.書込(格納値, 文);
        検証(ファイル.読取(格納値).equals(文), "UTF8_FILE");
        検証(文字.コード点個数("한😀") == 2, "UNICODE");
        検証(文字.値正規化("\u1100\u1161").equals("가"), "NORMALIZATION");
        値 オブジェクト値 = new 子値();
        検証(オブジェクト値.読取() == 42 && (long)子値.class.getMethod("読取").invoke(オブジェクト値) == 42, "OBJECT_INHERITANCE_REFLECTION");
        検証(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("妥当性検査"); }
        catch (IOException 例外) { 検証(例外.getMessage().equals("妥当性検査"), "EXCEPTION"); }
        AtomicInteger 総和値 = new AtomicInteger();
        Thread スレッド値 = 作業.起動処理("한글 スレッド値", () -> 総和値.set(123));
        作業.待機(スレッド値);
        検証(総和値.get() == 123, "THREAD");
        ExecutorService 作業担当値 = Executors.newSingleThreadExecutor();
        try (ServerSocket サーバー値 = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> 返答 = 作業担当値.submit(() -> {
                try (Socket ソケット値 = サーバー値.accept()) {
                    BufferedReader 読取 = new BufferedReader(new InputStreamReader(ソケット値.getInputStream()));
                    String 行;
                    while ((行 = 読取.readLine()) != null && !行.isEmpty()) {}
                    byte[] 本体本文 = 文字.符号化(文);
                    ソケット値.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + 本体本文.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    ソケット値.getOutputStream().write(本体本文);
                } catch (IOException エラー) { throw new UncheckedIOException(エラー); }
            });
            検証(通信.取得処理値(URI.create("http://127.0.0.1:" + サーバー値.getLocalPort()), Duration.ofSeconds(30)).body().equals(文), "HTTP_TCP");
            返答.get(30, TimeUnit.SECONDS);
        } finally { 作業担当値.shutdownNow(); }
        検証(new ProcessBuilder("/bin/echo", "プロセス値").start().waitFor() == 0, "PROCESS");
        if (引数.length > 0 && 引数[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font 書体値 = new Font("Dialog", Font.PLAIN, 18);
                検証(書体値.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                検証(書体値.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea 本文枠 = new JTextArea(文);
                本文枠.setFont(書体値);
                JFrame 窓 = 画面.窓("그래픽 妥当性検査", 本文枠, 800, 240);
                BufferedImage 描画 = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 筆値 = 描画.createGraphics();
                窓.paint(筆値); 筆値.dispose();
                try { javax.imageio.ImageIO.write(描画, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException エラー) { throw new UncheckedIOException(エラー); }
                窓.dispose();
                検証(本文枠.getText().equals(文), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
