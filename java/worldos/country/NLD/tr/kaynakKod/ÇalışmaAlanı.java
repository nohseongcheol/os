// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NLD.l_tr;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.List;
import java.util.concurrent.*;
import javax.swing.*;

/** WorldOS project-owned source. Standard Java API names are preserved. */
public final class ÇalışmaAlanı {
    private final JFrame Pencere = new JFrame();
    private final JTextArea kaynakKod = new JTextArea();
    private final JTextArea metinÇıktısı = new JTextArea();
    private final JTextField yol = new JTextField("kaynakKod.java", 26);
    private final JTextField İsim = new JTextField("kaynakKod", 15);
    private final JTextField bağımsız_değişkenler = new JTextField(25);
    private final Properties iletiler = new Properties();
    private final Path dizin = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService arkaPlanGörevi = Executors.newSingleThreadExecutor();
    private volatile Process Süreç;

    private String Etiket(String Anahtar) {
        return iletiler.getProperty(Anahtar, Anahtar);
    }

    private void listenin_sonuna_ekle(String metin) {
        SwingUtilities.invokeLater(() -> {
            metinÇıktısı.append(metin);
            metinÇıktısı.setCaretPosition(metinÇıktısı.getDocument().getLength());
        });
    }

    private void hata(Exception exception) {
        listenin_sonuna_ekle(Etiket("error") + ": " + exception.toString() + "\n");
    }

    private void düğme(JPanel Tabla, String Anahtar, Runnable Eylem) {
        JButton düğme = new JButton(Etiket(Anahtar));
        düğme.addActionListener(Olay -> Eylem.run());
        Tabla.add(düğme);
    }

    private void kaynakYükle() {
        try {
            kaynakKod.setText(Files.readString(dizin.resolve(yol.getText()), StandardCharsets.UTF_8));
            kaynakKod.setCaretPosition(0);
        } catch (Exception exception) { hata(exception); }
    }

    private boolean Kaydet() {
        try {
            Path dosya = dizin.resolve(yol.getText()).normalize();
            Files.createDirectories(dosya.getParent());
            Files.writeString(dosya, kaynakKod.getText(), StandardCharsets.UTF_8);
            listenin_sonuna_ekle(Etiket("save") + ": " + dosya + "\n");
            return true;
        } catch (Exception exception) { hata(exception); return false; }
    }

    private int Çalıştır(List<String> komut) throws Exception {
        Süreç = new ProcessBuilder(komut).directory(dizin.toFile()).redirectErrorStream(true).start();
        try (BufferedReader metinOkuyucu = new BufferedReader(new InputStreamReader(Süreç.getInputStream(), StandardCharsets.UTF_8))) {
            String girdi_satırı;
            while ((girdi_satırı = metinOkuyucu.readLine()) != null) listenin_sonuna_ekle(girdi_satırı + "\n");
        }
        int sonuç = Süreç.waitFor();
        Süreç = null;
        listenin_sonuna_ekle(Etiket("result") + ": " + sonuç + "\n");
        return sonuç;
    }

    private void derle(boolean çalıştır) {
        if (!Kaydet()) return;
        String dosya = dizin.resolve(yol.getText()).toString();
        String Sınıf = İsim.getText().trim();
        String metin = bağımsız_değişkenler.getText();
        arkaPlanGörevi.submit(() -> {
            try {
                Files.createDirectories(dizin.resolve("classes"));
                int sonuç = Çalıştır(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", dizin.resolve("classes").toString(), dosya));
                if (çalıştır && sonuç == 0) {
                    List<String> komut = new ArrayList<>(Arrays.asList("java", "-cp", dizin.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Sınıf));
                    StreamTokenizer bağımsızDeğişkenÇözümleyici = new StreamTokenizer(new StringReader(metin));
                    bağımsızDeğişkenÇözümleyici.resetSyntax(); bağımsızDeğişkenÇözümleyici.wordChars(33, 65535); bağımsızDeğişkenÇözümleyici.whitespaceChars(0, 32);
                    bağımsızDeğişkenÇözümleyici.quoteChar('"'); bağımsızDeğişkenÇözümleyici.quoteChar('\'');
                    while (bağımsızDeğişkenÇözümleyici.nextToken() != StreamTokenizer.TT_EOF) komut.add(bağımsızDeğişkenÇözümleyici.sval);
                    Çalıştır(komut);
                }
            } catch (Exception exception) { hata(exception); }
        });
    }

    private void Durdur() {
        Process geçerliSüreç = Süreç;
        if (geçerliSüreç != null) {
            geçerliSüreç.descendants().forEach(ProcessHandle::destroyForcibly);
            geçerliSüreç.destroyForcibly();
        }
    }

    private void uçbirim() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(dizin.toFile()).start(); }
        catch (Exception exception) { hata(exception); }
    }

    private void seç() {
        JFileChooser chooser = new JFileChooser(dizin.toFile());
        if (chooser.showOpenDialog(Pencere) == JFileChooser.APPROVE_OPTION) {
            yol.setText(chooser.getSelectedFile().getAbsolutePath());
            kaynakYükle();
        }
    }

    private void başlat() {
        try (Reader metinOkuyucu = new InputStreamReader(ÇalışmaAlanı.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            iletiler.load(metinOkuyucu);
            Files.createDirectories(dizin);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Pencere.setTitle(Etiket("workspace") + " · WorldOS " + Etiket("identity"));
        Pencere.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Pencere.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Olay) {
                Durdur(); arkaPlanGörevi.shutdownNow(); System.exit(0);
            }
        });
        kaynakKod.setFont(new Font("Monospaced", Font.PLAIN, 17));
        kaynakKod.setTabSize(4);
        metinÇıktısı.setFont(new Font("Monospaced", Font.PLAIN, 14));
        metinÇıktısı.setEditable(false);
        JPanel Tabla = new JPanel(new GridLayout(0, 1));
        JPanel dosya = new JPanel(new FlowLayout(FlowLayout.LEADING));
        dosya.add(new JLabel(Etiket("file"))); dosya.add(yol);
        Tabla.add(dosya);
        JPanel Araç_Çubuğu = new JPanel(new FlowLayout(FlowLayout.LEADING));
        düğme(Araç_Çubuğu, "open", () -> seç());
        düğme(Araç_Çubuğu, "save", () -> Kaydet());
        düğme(Araç_Çubuğu, "compile", () -> derle(false));
        düğme(Araç_Çubuğu, "run", () -> derle(true));
        düğme(Araç_Çubuğu, "stop", () -> Durdur());
        düğme(Araç_Çubuğu, "terminal", () -> uçbirim());
        Tabla.add(Araç_Çubuğu);
        JPanel Ayarlar = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Ayarlar.add(new JLabel(Etiket("class"))); Ayarlar.add(İsim);
        Ayarlar.add(new JLabel(Etiket("arguments"))); Ayarlar.add(bağımsız_değişkenler);
        Tabla.add(Ayarlar);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(kaynakKod), new JScrollPane(metinÇıktısı));
        split.setResizeWeight(0.72);
        Pencere.add(Tabla, BorderLayout.NORTH);
        Pencere.add(split, BorderLayout.CENTER);
        Tabla.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etiket("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        kaynakKod.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        metinÇıktısı.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Boyut = Toolkit.getDefaultToolkit().getScreenSize();
        Pencere.setSize(Math.min(1240, Boyut.width - 40), Math.min(760, Boyut.height - 60));
        Pencere.setLocationRelativeTo(null);
        Pencere.setVisible(true);
        kaynakYükle();
        split.setDividerLocation(0.72);
        listenin_sonuna_ekle("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        listenin_sonuna_ekle(Etiket("help") + "\n");
    }

    public static void main(String[] bağımsız_değişkenler) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new ÇalışmaAlanı().başlat());
    }
}
