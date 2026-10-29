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
    interface ຄ່າ { long 읽기(); }
    static class 부모 { protected long ຄ່າ = 42; }
    static class ເດັກ_ນ້ອຍ_ຄ່າ extends 부모 implements ຄ່າ { public long 읽기() { return ຄ່າ; } }
    private static void 확인(boolean ເງື່ອນໄຂ, String ຊື່) {
        if (!ເງື່ອນໄຂ) throw new AssertionError(ຊື່);
        System.out.println("PASS " + ຊື່);
    }
    public static void main(String[] 인수) throws Exception {
        String ຂໍ້ຄວາມ = "한글 日本語 العربية हिन्दी 😀";
        Path ຮ້ານຄ້າ_ຄ່າ = Path.of(System.getProperty("user.home"), "ໃຊ້ໄດ້_ຂໍ້ມູນ.txt");
        ຟາຍ.ຂຽນ(ຮ້ານຄ້າ_ຄ່າ, ຂໍ້ຄວາມ);
        확인(ຟາຍ.읽기(ຮ້ານຄ້າ_ຄ່າ).equals(ຂໍ້ຄວາມ), "UTF8_FILE");
        확인(문자.코드포인트수("한😀") == 2, "UNICODE");
        확인(문자.ເຮັດ_ເປັນ_ທໍາ_ມະ_ດາ_ຄ່າ("\u1100\u1161").equals("가"), "NORMALIZATION");
        ຄ່າ ວັດ_ຖຸ_ຄ່າ = new ເດັກ_ນ້ອຍ_ຄ່າ();
        확인(ວັດ_ຖຸ_ຄ່າ.읽기() == 42 && (long)ເດັກ_ນ້ອຍ_ຄ່າ.class.getMethod("읽기").invoke(ວັດ_ຖຸ_ຄ່າ) == 42, "OBJECT_INHERITANCE_REFLECTION");
        확인(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("ຮັບ_ຮອງ"); }
        catch (IOException ຂໍ້ຍົກເວັ້ນ) { 확인(ຂໍ້ຍົກເວັ້ນ.getMessage().equals("ຮັບ_ຮອງ"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread ສອດຕໍ່_ຄ່າ = 작업.ແລ່ນ("한글 ສອດຕໍ່_ຄ່າ", () -> 합.set(123));
        작업.기다리기(ສອດຕໍ່_ຄ່າ);
        확인(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket 서버 = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> ຕອບກັບ = 일꾼.submit(() -> {
                try (Socket 소켓 = 서버.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String ສາຍ;
                    while ((ສາຍ = 읽기.readLine()) != null && !ສາຍ.isEmpty()) {}
                    byte[] ເນື້ອໃນເອກະສານ = 문자.부호화(ຂໍ້ຄວາມ);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + ເນື້ອໃນເອກະສານ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(ເນື້ອໃນເອກະສານ);
                } catch (IOException ຂໍ້ຜິດພາດ) { throw new UncheckedIOException(ຂໍ້ຜິດພາດ); }
            });
            확인(통신.가져오기(URI.create("http://127.0.0.1:" + 서버.getLocalPort()), Duration.ofSeconds(30)).body().equals(ຂໍ້ຄວາມ), "HTTP_TCP");
            ຕອບກັບ.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        확인(new ProcessBuilder("/bin/echo", "ຂະ_ບວນ_ການ_ຄ່າ").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ຮູບແບບຕົວຫນັງສື_ຄ່າ = new Font("Dialog", Font.PLAIN, 18);
                확인(ຮູບແບບຕົວຫນັງສື_ຄ່າ.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                확인(ຮູບແບບຕົວຫນັງສື_ຄ່າ.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea ກ່ອງ_ຂໍ້_ຄວາມ = new JTextArea(ຂໍ້ຄວາມ);
                ກ່ອງ_ຂໍ້_ຄວາມ.setFont(ຮູບແບບຕົວຫນັງສື_ຄ່າ);
                JFrame ວິນໂດ = 화면.ວິນໂດ("그래픽 ຮັບ_ຮອງ", ກ່ອງ_ຂໍ້_ຄວາມ, 800, 240);
                BufferedImage ການ_ແຕ້ມ_ຄ່າ = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = ການ_ແຕ້ມ_ຄ່າ.createGraphics();
                ວິນໂດ.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(ການ_ແຕ້ມ_ຄ່າ, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ຂໍ້ຜິດພາດ) { throw new UncheckedIOException(ຂໍ້ຜິດພາດ); }
                ວິນໂດ.dispose();
                확인(ກ່ອງ_ຂໍ້_ຄວາມ.getText().equals(ຂໍ້ຄວາມ), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
