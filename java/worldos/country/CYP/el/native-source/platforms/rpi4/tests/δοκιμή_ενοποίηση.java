// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import ελληνικά.자바.*;
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

public class δοκιμή_ενοποίηση {
    interface τιμή { long Ανάγνωση(); }
    static class γονικός_τιμή { protected long τιμή = 42; }
    static class παιδί_τιμή extends γονικός_τιμή implements τιμή { public long Ανάγνωση() { return τιμή; } }
    private static void επαληθεύω(boolean πάθηση, String Όνομα) {
        if (!πάθηση) throw new AssertionError(Όνομα);
        System.out.println("PASS " + Όνομα);
    }
    public static void main(String[] Παράμετροι) throws Exception {
        String Κείμενο = "한글 日本語 العربية हिन्दी 😀";
        Path αποθηκεύω_τιμή = Path.of(System.getProperty("user.home"), "επικύρωση_δεδομένα.txt");
        Αρχείο.Εγγραφή(αποθηκεύω_τιμή, Κείμενο);
        επαληθεύω(Αρχείο.Ανάγνωση(αποθηκεύω_τιμή).equals(Κείμενο), "UTF8_FILE");
        επαληθεύω(문자.코드포인트수("한😀") == 2, "UNICODE");
        επαληθεύω(문자.κανονικοποίηση_τιμή("\u1100\u1161").equals("가"), "NORMALIZATION");
        τιμή αντικείμενο_τιμή = new παιδί_τιμή();
        επαληθεύω(αντικείμενο_τιμή.Ανάγνωση() == 42 && (long)παιδί_τιμή.class.getMethod("Ανάγνωση").invoke(αντικείμενο_τιμή) == 42, "OBJECT_INHERITANCE_REFLECTION");
        επαληθεύω(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("επικυρώνω"); }
        catch (IOException εξαίρεση) { επαληθεύω(εξαίρεση.getMessage().equals("επικυρώνω"), "EXCEPTION"); }
        AtomicInteger Διαχείριση_ενημερώσεων_λογισμικού_τιμή = new AtomicInteger();
        Thread νήμα_τιμή = 작업.Εκτέλεση_2("한글 νήμα_τιμή", () -> Διαχείριση_ενημερώσεων_λογισμικού_τιμή.set(123));
        작업.기다리기(νήμα_τιμή);
        επαληθεύω(Διαχείριση_ενημερώσεων_λογισμικού_τιμή.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket διακομιστής_τιμή = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> απαντώ = 일꾼.submit(() -> {
                try (Socket υποδοχή_τιμή = διακομιστής_τιμή.accept()) {
                    BufferedReader Ανάγνωση = new BufferedReader(new InputStreamReader(υποδοχή_τιμή.getInputStream()));
                    String Γραμμή;
                    while ((Γραμμή = Ανάγνωση.readLine()) != null && !Γραμμή.isEmpty()) {}
                    byte[] σώμα_κειμένου = 문자.κωδικοποιώ(Κείμενο);
                    υποδοχή_τιμή.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + σώμα_κειμένου.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    υποδοχή_τιμή.getOutputStream().write(σώμα_κειμένου);
                } catch (IOException ΣΦΑΛΜΑ) { throw new UncheckedIOException(ΣΦΑΛΜΑ); }
            });
            επαληθεύω(통신.가져오기(URI.create("http://127.0.0.1:" + διακομιστής_τιμή.getLocalPort()), Duration.ofSeconds(30)).body().equals(Κείμενο), "HTTP_TCP");
            απαντώ.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        επαληθεύω(new ProcessBuilder("/bin/echo", "διεργασία_τιμή").start().waitFor() == 0, "PROCESS");
        if (Παράμετροι.length > 0 && Παράμετροι[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font γραμματοσειρά_τιμή = new Font("Dialog", Font.PLAIN, 18);
                επαληθεύω(γραμματοσειρά_τιμή.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                επαληθεύω(γραμματοσειρά_τιμή.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea πλαίσιο_κειμένου = new JTextArea(Κείμενο);
                πλαίσιο_κειμένου.setFont(γραμματοσειρά_τιμή);
                JFrame Παράθυρο = 화면.Παράθυρο("그래픽 επικυρώνω", πλαίσιο_κειμένου, 800, 240);
                BufferedImage σχέδιο_τιμή = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D πινέλο_τιμή = σχέδιο_τιμή.createGraphics();
                Παράθυρο.paint(πινέλο_τιμή); πινέλο_τιμή.dispose();
                try { javax.imageio.ImageIO.write(σχέδιο_τιμή, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException ΣΦΑΛΜΑ) { throw new UncheckedIOException(ΣΦΑΛΜΑ); }
                Παράθυρο.dispose();
                επαληθεύω(πλαίσιο_κειμένου.getText().equals(Κείμενο), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
