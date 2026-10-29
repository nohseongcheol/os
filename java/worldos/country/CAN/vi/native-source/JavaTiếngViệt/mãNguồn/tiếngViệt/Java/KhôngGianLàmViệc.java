// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.Java;

import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.List;
import java.util.concurrent.*;
import javax.swing.*;
import javax.swing.plaf.FontUIResource;

/** Không gian làm việc Swing nhỏ để sửa, biên dịch và chạy mã Java trong thư mục nhà của người dùng. */
public final class KhôngGianLàmViệc {
    private final JFrame cửaSổ = new JFrame("jkoros — Java KhôngGianLàmViệc");
    private final JTextArea mãNguồn = new JTextArea();
    private final JTextArea ĐầuRa = new JTextArea(8, 80);
    private final JTextField tênMụcTệp = new JTextField("LờiChào.java", 20);
    private final JTextField tênMụcLớp = new JTextField("LờiChào", 16);
    private final Path thưMụcĐangLàmViệc = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService giáTrịBộLàmViệc = Executors.newSingleThreadExecutor();
    private volatile Process giáTrịTiếnTrình;
    private final String thưViện = "/opt/jkoros/lib/JavaTiếngViệt.jar";

    private void thôngBáo(String vănBản) { SwingUtilities.invokeLater(() -> ĐầuRa.append(vănBản + "\n")); }
    private void nút(JPanel giáTrịPhiênBản, String tên, Runnable giáTrịHànhVi) {
        JButton nút = new JButton(tên);
        nút.addActionListener(sựKiện -> giáTrịHànhVi.run());
        giáTrịPhiênBản.add(nút);
    }
    private boolean giáTrịCất() {
        try {
            Path đườngDẫn = thưMụcĐangLàmViệc.resolve(tênMụcTệp.getText());
            Files.createDirectories(đườngDẫn.getParent());
            Tệp.ghi(đườngDẫn, mãNguồn.getText());
            thôngBáo("giáTrịCất: " + đườngDẫn);
            return true;
        } catch (Exception lỗi) { thôngBáo(lỗi.toString()); return false; }
    }
    private void mở() {
        try { mãNguồn.setText(Tệp.đọc(thưMụcĐangLàmViệc.resolve(tênMụcTệp.getText()))); }
        catch (Exception lỗi) { thôngBáo(lỗi.toString()); }
    }
    private int lệnh(List<String> lệnh) throws Exception {
        giáTrịTiếnTrình = new ProcessBuilder(lệnh).directory(thưMụcĐangLàmViệc.toFile()).redirectErrorStream(true).start();
        try (BufferedReader dòng = new BufferedReader(new InputStreamReader(giáTrịTiếnTrình.getInputStream(), StandardCharsets.UTF_8))) {
            String vănBản;
            while ((vănBản = dòng.readLine()) != null) thôngBáo(vănBản);
        }
        int giáTrịTrạngThái = giáTrịTiếnTrình.waitFor(); giáTrịTiếnTrình = null;
        thôngBáo("chươngTrìnhRa giáTrịMã: " + giáTrịTrạngThái);
        return giáTrịTrạngThái;
    }
    private void dịchThuậtNguồn(boolean thựcThiLệnh, boolean tệpTệpThựcThi) {
        if (!giáTrịCất()) return;
        String giáTrịVào = tênMụcTệp.getText(), giáTrịĐiểmMục = tênMụcLớp.getText();
        giáTrịBộLàmViệc.submit(() -> {
            try {
                Files.createDirectories(thưMụcĐangLàmViệc.resolve("classes"));
                if (tệpTệpThựcThi) {
                    lệnh(Arrays.asList("jclassc", "--target", "openjdk", "--entry", giáTrịĐiểmMục,
                        "--classpath", thưViện, "-o", "실행프로그램", giáTrịVào));
                } else if (lệnh(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", thưViện,
                        "-d", "classes", giáTrịVào)) == 0 && thựcThiLệnh) {
                    lệnh(Arrays.asList("java", "-cp", "classes:" + thưViện, giáTrịĐiểmMục));
                }
            } catch (Exception lỗi) { thôngBáo(lỗi.toString()); }
        });
    }
    private void việcThựcThiTạmDừng() {
        Process phầnMụcHiệnTại = giáTrịTiếnTrình;
        if (phầnMụcHiệnTại != null) { phầnMụcHiệnTại.descendants().forEach(ProcessHandle::destroy); phầnMụcHiệnTại.destroy(); }
    }
    private KhôngGianLàmViệc() throws IOException {
        Files.createDirectories(thưMụcĐangLàmViệc);
        Font giáTrịPhôngChữ = new Font("Monospaced", Font.PLAIN, 16);
        mãNguồn.setFont(giáTrịPhôngChữ); ĐầuRa.setFont(giáTrịPhôngChữ); ĐầuRa.setEditable(false);
        mãNguồn.setTabSize(4);
        mãNguồn.setMargin(new Insets(10, 12, 10, 12));
        ĐầuRa.setMargin(new Insets(8, 12, 8, 12));
        mãNguồn.setBackground(new Color(250, 251, 252));
        mãNguồn.setForeground(new Color(32, 43, 58));
        JPanel bảngLệnh = new JPanel();
        bảngLệnh.add(new JLabel("Tệp")); bảngLệnh.add(tênMụcTệp);
        bảngLệnh.add(new JLabel("주 giáTrịLớp")); bảngLệnh.add(tênMụcLớp);
        nút(bảngLệnh, "mở", this::mở); nút(bảngLệnh, "giáTrịCất", this::giáTrịCất);
        nút(bảngLệnh, "biênDịchNguồn", () -> dịchThuậtNguồn(false, false));
        nút(bảngLệnh, "thựcThiLệnh", () -> dịchThuậtNguồn(true, false));
        nút(bảngLệnh, "thựcThiLệnh Tệp tạoMục", () -> dịchThuậtNguồn(false, true));
        nút(bảngLệnh, "việcThựcThiTạmDừng", this::việcThựcThiTạmDừng);
        JSplitPane kếtQuảPhépChia = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(mãNguồn), new JScrollPane(ĐầuRa));
        kếtQuảPhépChia.setResizeWeight(0.75);
        cửaSổ.add(bảngLệnh, BorderLayout.NORTH); cửaSổ.add(kếtQuảPhépChia, BorderLayout.CENTER);
        cửaSổ.setSize(1200, 750); cửaSổ.setLocationRelativeTo(null);
        cửaSổ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        cửaSổ.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent sựKiện) { việcThựcThiTạmDừng(); giáTrịBộLàmViệc.shutdownNow(); }
        });
        mở(); cửaSổ.setVisible(true);
    }
    public static void main(String[] cácĐốiSố) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource phôngChữMặcĐịnh = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object giáTrịMục : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(giáTrịMục) instanceof Font) UIManager.put(giáTrịMục, phôngChữMặcĐịnh);
                }
                new KhôngGianLàmViệc();
            } catch (Exception lỗi) { lỗi.printStackTrace(); }
        });
    }
}
