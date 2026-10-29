// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NLD.l_id;
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
public final class RuangKerja {
    private final JFrame Jendela = new JFrame();
    private final JTextArea kodeSumber = new JTextArea();
    private final JTextArea keluaranTeks = new JTextArea();
    private final JTextField jalur = new JTextField("kodeSumber.java", 26);
    private final JTextField Nama_2 = new JTextField("kodeSumber", 15);
    private final JTextField argumen = new JTextField(25);
    private final Properties pesan = new Properties();
    private final Path direktori = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService tugasLatar = Executors.newSingleThreadExecutor();
    private volatile Process Proses;

    private String Nama(String Kunci) {
        return pesan.getProperty(Kunci, Kunci);
    }

    private void tambah_di_akhir_daftar(String teks) {
        SwingUtilities.invokeLater(() -> {
            keluaranTeks.append(teks);
            keluaranTeks.setCaretPosition(keluaranTeks.getDocument().getLength());
        });
    }

    private void galat(Exception exception) {
        tambah_di_akhir_daftar(Nama("error") + ": " + exception.toString() + "\n");
    }

    private void tombol(JPanel panel, String Kunci, Runnable Aksi) {
        JButton tombol = new JButton(Nama(Kunci));
        tombol.addActionListener(Even -> Aksi.run());
        panel.add(tombol);
    }

    private void muatSumber() {
        try {
            kodeSumber.setText(Files.readString(direktori.resolve(jalur.getText()), StandardCharsets.UTF_8));
            kodeSumber.setCaretPosition(0);
        } catch (Exception exception) { galat(exception); }
    }

    private boolean Simpan() {
        try {
            Path berkas = direktori.resolve(jalur.getText()).normalize();
            Files.createDirectories(berkas.getParent());
            Files.writeString(berkas, kodeSumber.getText(), StandardCharsets.UTF_8);
            tambah_di_akhir_daftar(Nama("save") + ": " + berkas + "\n");
            return true;
        } catch (Exception exception) { galat(exception); return false; }
    }

    private int Eksekusi(List<String> perintah) throws Exception {
        Proses = new ProcessBuilder(perintah).directory(direktori.toFile()).redirectErrorStream(true).start();
        try (BufferedReader pembacaTeks = new BufferedReader(new InputStreamReader(Proses.getInputStream(), StandardCharsets.UTF_8))) {
            String baris_masukan;
            while ((baris_masukan = pembacaTeks.readLine()) != null) tambah_di_akhir_daftar(baris_masukan + "\n");
        }
        int hasil = Proses.waitFor();
        Proses = null;
        tambah_di_akhir_daftar(Nama("result") + ": " + hasil + "\n");
        return hasil;
    }

    private void kompilasi(boolean jalankan) {
        if (!Simpan()) return;
        String berkas = direktori.resolve(jalur.getText()).toString();
        String Kelas = Nama_2.getText().trim();
        String teks = argumen.getText();
        tugasLatar.submit(() -> {
            try {
                Files.createDirectories(direktori.resolve("classes"));
                int hasil = Eksekusi(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", direktori.resolve("classes").toString(), berkas));
                if (jalankan && hasil == 0) {
                    List<String> perintah = new ArrayList<>(Arrays.asList("java", "-cp", direktori.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Kelas));
                    StreamTokenizer penguraiArgumen = new StreamTokenizer(new StringReader(teks));
                    penguraiArgumen.resetSyntax(); penguraiArgumen.wordChars(33, 65535); penguraiArgumen.whitespaceChars(0, 32);
                    penguraiArgumen.quoteChar('"'); penguraiArgumen.quoteChar('\'');
                    while (penguraiArgumen.nextToken() != StreamTokenizer.TT_EOF) perintah.add(penguraiArgumen.sval);
                    Eksekusi(perintah);
                }
            } catch (Exception exception) { galat(exception); }
        });
    }

    private void Hentikan() {
        Process prosesAktif = Proses;
        if (prosesAktif != null) {
            prosesAktif.descendants().forEach(ProcessHandle::destroyForcibly);
            prosesAktif.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(direktori.toFile()).start(); }
        catch (Exception exception) { galat(exception); }
    }

    private void pilih() {
        JFileChooser chooser = new JFileChooser(direktori.toFile());
        if (chooser.showOpenDialog(Jendela) == JFileChooser.APPROVE_OPTION) {
            jalur.setText(chooser.getSelectedFile().getAbsolutePath());
            muatSumber();
        }
    }

    private void inisialisasi() {
        try (Reader pembacaTeks = new InputStreamReader(RuangKerja.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            pesan.load(pembacaTeks);
            Files.createDirectories(direktori);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Jendela.setTitle(Nama("workspace") + " · WorldOS " + Nama("identity"));
        Jendela.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Jendela.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Even) {
                Hentikan(); tugasLatar.shutdownNow(); System.exit(0);
            }
        });
        kodeSumber.setFont(new Font("Monospaced", Font.PLAIN, 17));
        kodeSumber.setTabSize(4);
        keluaranTeks.setFont(new Font("Monospaced", Font.PLAIN, 14));
        keluaranTeks.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel berkas = new JPanel(new FlowLayout(FlowLayout.LEADING));
        berkas.add(new JLabel(Nama("file"))); berkas.add(jalur);
        panel.add(berkas);
        JPanel Bilah_Alat = new JPanel(new FlowLayout(FlowLayout.LEADING));
        tombol(Bilah_Alat, "open", () -> pilih());
        tombol(Bilah_Alat, "save", () -> Simpan());
        tombol(Bilah_Alat, "compile", () -> kompilasi(false));
        tombol(Bilah_Alat, "run", () -> kompilasi(true));
        tombol(Bilah_Alat, "stop", () -> Hentikan());
        tombol(Bilah_Alat, "terminal", () -> terminal());
        panel.add(Bilah_Alat);
        JPanel Konfigurasi = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Konfigurasi.add(new JLabel(Nama("class"))); Konfigurasi.add(Nama_2);
        Konfigurasi.add(new JLabel(Nama("arguments"))); Konfigurasi.add(argumen);
        panel.add(Konfigurasi);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(kodeSumber), new JScrollPane(keluaranTeks));
        split.setResizeWeight(0.72);
        Jendela.add(panel, BorderLayout.NORTH);
        Jendela.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Nama("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        kodeSumber.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        keluaranTeks.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Ukuran = Toolkit.getDefaultToolkit().getScreenSize();
        Jendela.setSize(Math.min(1240, Ukuran.width - 40), Math.min(760, Ukuran.height - 60));
        Jendela.setLocationRelativeTo(null);
        Jendela.setVisible(true);
        muatSumber();
        split.setDividerLocation(0.72);
        tambah_di_akhir_daftar("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        tambah_di_akhir_daftar(Nama("help") + "\n");
    }

    public static void main(String[] argumen) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new RuangKerja().inisialisasi());
    }
}
