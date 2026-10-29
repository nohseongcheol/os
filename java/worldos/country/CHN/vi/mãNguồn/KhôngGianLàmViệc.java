// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.CHN.l_vi;
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
public final class KhôngGianLàmViệc {
    private final JFrame window = new JFrame();
    private final JTextArea mãNguồn = new JTextArea();
    private final JTextArea đầuRaVănBản = new JTextArea();
    private final JTextField đườngDẫn = new JTextField("mãNguồn.java", 26);
    private final JTextField Tên = new JTextField("mãNguồn", 15);
    private final JTextField đối_số = new JTextField(25);
    private final Properties thôngBáo = new Properties();
    private final Path thưMục = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService tácVụNền = Executors.newSingleThreadExecutor();
    private volatile Process Tiến_trình;

    private String Nhãn(String key) {
        return thôngBáo.getProperty(key, key);
    }

    private void thêm_vào_cuối_danh_sách(String văn_bản) {
        SwingUtilities.invokeLater(() -> {
            đầuRaVănBản.append(văn_bản);
            đầuRaVănBản.setCaretPosition(đầuRaVănBản.getDocument().getLength());
        });
    }

    private void lỗi(Exception exception) {
        thêm_vào_cuối_danh_sách(Nhãn("error") + ": " + exception.toString() + "\n");
    }

    private void nút(JPanel Bảng, String key, Runnable Hành_động) {
        JButton nút = new JButton(Nhãn(key));
        nút.addActionListener(Sự_kiện -> Hành_động.run());
        Bảng.add(nút);
    }

    private void nạpNguồn() {
        try {
            mãNguồn.setText(Files.readString(thưMục.resolve(đườngDẫn.getText()), StandardCharsets.UTF_8));
            mãNguồn.setCaretPosition(0);
        } catch (Exception exception) { lỗi(exception); }
    }

    private boolean Lưu() {
        try {
            Path tậpTin = thưMục.resolve(đườngDẫn.getText()).normalize();
            Files.createDirectories(tậpTin.getParent());
            Files.writeString(tậpTin, mãNguồn.getText(), StandardCharsets.UTF_8);
            thêm_vào_cuối_danh_sách(Nhãn("save") + ": " + tậpTin + "\n");
            return true;
        } catch (Exception exception) { lỗi(exception); return false; }
    }

    private int Chạy(List<String> lệnh) throws Exception {
        Tiến_trình = new ProcessBuilder(lệnh).directory(thưMục.toFile()).redirectErrorStream(true).start();
        try (BufferedReader bộĐọcVănBản = new BufferedReader(new InputStreamReader(Tiến_trình.getInputStream(), StandardCharsets.UTF_8))) {
            String dòng_nhập;
            while ((dòng_nhập = bộĐọcVănBản.readLine()) != null) thêm_vào_cuối_danh_sách(dòng_nhập + "\n");
        }
        int kếtQuả = Tiến_trình.waitFor();
        Tiến_trình = null;
        thêm_vào_cuối_danh_sách(Nhãn("result") + ": " + kếtQuả + "\n");
        return kếtQuả;
    }

    private void biênDịch(boolean khởiChạy) {
        if (!Lưu()) return;
        String tậpTin = thưMục.resolve(đườngDẫn.getText()).toString();
        String Hạng = Tên.getText().trim();
        String văn_bản = đối_số.getText();
        tácVụNền.submit(() -> {
            try {
                Files.createDirectories(thưMục.resolve("classes"));
                int kếtQuả = Chạy(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", thưMục.resolve("classes").toString(), tậpTin));
                if (khởiChạy && kếtQuả == 0) {
                    List<String> lệnh = new ArrayList<>(Arrays.asList("java", "-cp", thưMục.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Hạng));
                    StreamTokenizer bộPhânTíchĐốiSố = new StreamTokenizer(new StringReader(văn_bản));
                    bộPhânTíchĐốiSố.resetSyntax(); bộPhânTíchĐốiSố.wordChars(33, 65535); bộPhânTíchĐốiSố.whitespaceChars(0, 32);
                    bộPhânTíchĐốiSố.quoteChar('"'); bộPhânTíchĐốiSố.quoteChar('\'');
                    while (bộPhânTíchĐốiSố.nextToken() != StreamTokenizer.TT_EOF) lệnh.add(bộPhânTíchĐốiSố.sval);
                    Chạy(lệnh);
                }
            } catch (Exception exception) { lỗi(exception); }
        });
    }

    private void Dừng() {
        Process tiếnTrìnhHiệnTại = Tiến_trình;
        if (tiếnTrìnhHiệnTại != null) {
            tiếnTrìnhHiệnTại.descendants().forEach(ProcessHandle::destroyForcibly);
            tiếnTrìnhHiệnTại.destroyForcibly();
        }
    }

    private void thiếtBịĐầuCuối() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(thưMục.toFile()).start(); }
        catch (Exception exception) { lỗi(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(thưMục.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            đườngDẫn.setText(chooser.getSelectedFile().getAbsolutePath());
            nạpNguồn();
        }
    }

    private void khởiTạo() {
        try (Reader bộĐọcVănBản = new InputStreamReader(KhôngGianLàmViệc.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            thôngBáo.load(bộĐọcVănBản);
            Files.createDirectories(thưMục);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Nhãn("workspace") + " · WorldOS " + Nhãn("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Sự_kiện) {
                Dừng(); tácVụNền.shutdownNow(); System.exit(0);
            }
        });
        mãNguồn.setFont(new Font("Monospaced", Font.PLAIN, 17));
        mãNguồn.setTabSize(4);
        đầuRaVănBản.setFont(new Font("Monospaced", Font.PLAIN, 14));
        đầuRaVănBản.setEditable(false);
        JPanel Bảng = new JPanel(new GridLayout(0, 1));
        JPanel tậpTin = new JPanel(new FlowLayout(FlowLayout.LEADING));
        tậpTin.add(new JLabel(Nhãn("file"))); tậpTin.add(đườngDẫn);
        Bảng.add(tậpTin);
        JPanel Thanh_công_cụ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        nút(Thanh_công_cụ, "open", () -> choose());
        nút(Thanh_công_cụ, "save", () -> Lưu());
        nút(Thanh_công_cụ, "compile", () -> biênDịch(false));
        nút(Thanh_công_cụ, "run", () -> biênDịch(true));
        nút(Thanh_công_cụ, "stop", () -> Dừng());
        nút(Thanh_công_cụ, "terminal", () -> thiếtBịĐầuCuối());
        Bảng.add(Thanh_công_cụ);
        JPanel Thiết_lập = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Thiết_lập.add(new JLabel(Nhãn("class"))); Thiết_lập.add(Tên);
        Thiết_lập.add(new JLabel(Nhãn("arguments"))); Thiết_lập.add(đối_số);
        Bảng.add(Thiết_lập);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(mãNguồn), new JScrollPane(đầuRaVănBản));
        split.setResizeWeight(0.72);
        window.add(Bảng, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Bảng.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Nhãn("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        mãNguồn.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        đầuRaVănBản.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Kích_cỡ = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Kích_cỡ.width - 40), Math.min(760, Kích_cỡ.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        nạpNguồn();
        split.setDividerLocation(0.72);
        thêm_vào_cuối_danh_sách("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        thêm_vào_cuối_danh_sách(Nhãn("help") + "\n");
    }

    public static void main(String[] đối_số) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new KhôngGianLàmViệc().khởiTạo());
    }
}
