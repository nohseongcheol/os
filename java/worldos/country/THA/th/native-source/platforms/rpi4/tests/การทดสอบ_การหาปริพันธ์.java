// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import ไทย.자바.*;
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

public class การทดสอบ_การหาปริพันธ์ {
    interface ค่า { long อ่าน(); }
    static class แม่_ค่า { protected long ค่า = 42; }
    static class ลูก_ค่า extends แม่_ค่า implements ค่า { public long อ่าน() { return ค่า; } }
    private static void ยืนยัน(boolean โรค, String ชื่อ) {
        if (!โรค) throw new AssertionError(ชื่อ);
        System.out.println("PASS " + ชื่อ);
    }
    public static void main(String[] อาร์กิวเมนต์) throws Exception {
        String ข้อความ = "한글 日本語 العربية हिन्दी 😀";
        Path เก็บ_ค่า = Path.of(System.getProperty("user.home"), "การตรวจสอบความถูกต้อง_ข้อมูล.txt");
        แฟ้ม.เขียน(เก็บ_ค่า, ข้อความ);
        ยืนยัน(แฟ้ม.อ่าน(เก็บ_ค่า).equals(ข้อความ), "UTF8_FILE");
        ยืนยัน(문자.코드포인트수("한😀") == 2, "UNICODE");
        ยืนยัน(문자.นอร์มัลไลซ์_ค่า("\u1100\u1161").equals("가"), "NORMALIZATION");
        ค่า วัตถุ_ค่า = new ลูก_ค่า();
        ยืนยัน(วัตถุ_ค่า.อ่าน() == 42 && (long)ลูก_ค่า.class.getMethod("อ่าน").invoke(วัตถุ_ค่า) == 42, "OBJECT_INHERITANCE_REFLECTION");
        ยืนยัน(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("ตรวจสอบความถูกต้อง"); }
        catch (IOException ข้อยกเว้น) { ยืนยัน(ข้อยกเว้น.getMessage().equals("ตรวจสอบความถูกต้อง"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread เธรด_ค่า = 작업.เรียกใช้งาน("한글 เธรด_ค่า", () -> 합.set(123));
        작업.기다리기(เธรด_ค่า);
        ยืนยัน(합.get() == 123, "THREAD");
        ExecutorService ผู้ปฏิบัติงาน_ค่า = Executors.newSingleThreadExecutor();
        try (ServerSocket เซิร์ฟเวอร์_ค่า = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> ตอบกลับ = ผู้ปฏิบัติงาน_ค่า.submit(() -> {
                try (Socket 소켓 = เซิร์ฟเวอร์_ค่า.accept()) {
                    BufferedReader อ่าน = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String บรรทัด;
                    while ((บรรทัด = อ่าน.readLine()) != null && !บรรทัด.isEmpty()) {}
                    byte[] เนื้อความ = 문자.เข้ารหัส(ข้อความ);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + เนื้อความ.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(เนื้อความ);
                } catch (IOException ข้อผิดพลาด) { throw new UncheckedIOException(ข้อผิดพลาด); }
            });
            ยืนยัน(통신.가져오기(URI.create("http://127.0.0.1:" + เซิร์ฟเวอร์_ค่า.getLocalPort()), Duration.ofSeconds(30)).body().equals(ข้อความ), "HTTP_TCP");
            ตอบกลับ.get(30, TimeUnit.SECONDS);
        } finally { ผู้ปฏิบัติงาน_ค่า.shutdownNow(); }
        ยืนยัน(new ProcessBuilder("/bin/echo", "กระบวนการ_ค่า").start().waitFor() == 0, "PROCESS");
        if (อาร์กิวเมนต์.length > 0 && อาร์กิวเมนต์[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font ฟอนต์_ค่า = new Font("Dialog", Font.PLAIN, 18);
                ยืนยัน(ฟอนต์_ค่า.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                ยืนยัน(ฟอนต์_ค่า.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea กล่องข้อความ = new JTextArea(ข้อความ);
                กล่องข้อความ.setFont(ฟอนต์_ค่า);
                JFrame หน้าต่าง = 화면.หน้าต่าง("그래픽 ตรวจสอบความถูกต้อง", กล่องข้อความ, 800, 240);
                BufferedImage รูปวาด_ค่า = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = รูปวาด_ค่า.createGraphics();
                หน้าต่าง.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(รูปวาด_ค่า, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ข้อผิดพลาด) { throw new UncheckedIOException(ข้อผิดพลาด); }
                หน้าต่าง.dispose();
                ยืนยัน(กล่องข้อความ.getText().equals(ข้อความ), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
