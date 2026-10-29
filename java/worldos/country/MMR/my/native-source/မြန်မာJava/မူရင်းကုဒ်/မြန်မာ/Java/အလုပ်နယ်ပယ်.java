// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.Java;

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

/** သုံးစွဲသူအိမ်တွဲ၌ Java ကုဒ်ပြင်ဆင်၊ ဘာသာပြန်၊ လုပ်ဆောင်နိုင်သော သေးငယ်သည့် Swing အလုပ်နယ်ပယ်။ */
public final class အလုပ်နယ်ပယ် {
    private final JFrame ဝင်း = new JFrame("jkoros — Java အလုပ်နယ်ပယ်");
    private final JTextArea မူရင်းကုဒ် = new JTextArea();
    private final JTextArea အထွက် = new JTextArea(8, 80);
    private final JTextField ဖိုင်အချက်အမည် = new JTextField("နှုတ်ဆက်.java", 20);
    private final JTextField အတန်းအချက်အမည် = new JTextField("နှုတ်ဆက်", 16);
    private final Path လုပ်ဆောင်ဖိုင်တွဲ = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService အလုပ်သမားတန်ဖိုး = Executors.newSingleThreadExecutor();
    private volatile Process လုပ်ငန်းစဉ်;
    private final String စာကြည့်တိုက် = "/opt/jkoros/lib/မြန်မာJava.jar";

    private void အသိပေးချက်(String စာသား) { SwingUtilities.invokeLater(() -> အထွက်.append(စာသား + "\n")); }
    private void ခလုတ်(JPanel ထုတ်ဝေမှုတန်ဖိုး, String အမည်, Runnable အပြုအမူ) {
        JButton ခလုတ် = new JButton(အမည်);
        ခလုတ်.addActionListener(ဖြစ်ရပ် -> အပြုအမူ.run());
        ထုတ်ဝေမှုတန်ဖိုး.add(ခလုတ်);
    }
    private boolean သိုလှောင်တန်ဖိုး() {
        try {
            Path လမ်း = လုပ်ဆောင်ဖိုင်တွဲ.resolve(ဖိုင်အချက်အမည်.getText());
            Files.createDirectories(လမ်း.getParent());
            ဖိုင်.ရေး(လမ်း, မူရင်းကုဒ်.getText());
            အသိပေးချက်("သိုလှောင်တန်ဖိုး: " + လမ်း);
            return true;
        } catch (Exception အမှား) { အသိပေးချက်(အမှား.toString()); return false; }
    }
    private void ဖွင့်() {
        try { မူရင်းကုဒ်.setText(ဖိုင်.ဖတ်(လုပ်ဆောင်ဖိုင်တွဲ.resolve(ဖိုင်အချက်အမည်.getText()))); }
        catch (Exception အမှား) { အသိပေးချက်(အမှား.toString()); }
    }
    private int အမိန့်(List<String> အမိန့်) throws Exception {
        လုပ်ငန်းစဉ် = new ProcessBuilder(အမိန့်).directory(လုပ်ဆောင်ဖိုင်တွဲ.toFile()).redirectErrorStream(true).start();
        try (BufferedReader စာကြောင်း = new BufferedReader(new InputStreamReader(လုပ်ငန်းစဉ်.getInputStream(), StandardCharsets.UTF_8))) {
            String စာသား;
            while ((စာသား = စာကြောင်း.readLine()) != null) အသိပေးချက်(စာသား);
        }
        int အခြေအနေတန်ဖိုး = လုပ်ငန်းစဉ်.waitFor(); လုပ်ငန်းစဉ် = null;
        အသိပေးချက်("ထွက်ပရိုဂရမ် ကုဒ်တန်ဖိုး: " + အခြေအနေတန်ဖိုး);
        return အခြေအနေတန်ဖိုး;
    }
    private void မူရင်းကုဒ်ဘာသာပြန်ဆို(boolean စက်မောင်း, boolean စက်ဖိုင်ဖိုင်) {
        if (!သိုလှောင်တန်ဖိုး()) return;
        String ဝင်ဒေတာ = ဖိုင်အချက်အမည်.getText(), အချက်အမှတ်တစ်ခုတန်ဖိုး = အတန်းအချက်အမည်.getText();
        အလုပ်သမားတန်ဖိုး.submit(() -> {
            try {
                Files.createDirectories(လုပ်ဆောင်ဖိုင်တွဲ.resolve("classes"));
                if (စက်ဖိုင်ဖိုင်) {
                    အမိန့်(Arrays.asList("jclassc", "--target", "openjdk", "--entry", အချက်အမှတ်တစ်ခုတန်ဖိုး,
                        "--classpath", စာကြည့်တိုက်, "-o", "실행프로그램", ဝင်ဒေတာ));
                } else if (အမိန့်(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", စာကြည့်တိုက်,
                        "-d", "classes", ဝင်ဒေတာ)) == 0 && စက်မောင်း) {
                    အမိန့်(Arrays.asList("java", "-cp", "classes:" + စာကြည့်တိုက်, အချက်အမှတ်တစ်ခုတန်ဖိုး));
                }
            } catch (Exception အမှား) { အသိပေးချက်(အမှား.toString()); }
        });
    }
    private void ခဏရပ်လုပ်ဆောင်မှု() {
        Process လက်ရှိအချက်အလက်တစ်ခု = လုပ်ငန်းစဉ်;
        if (လက်ရှိအချက်အလက်တစ်ခု != null) { လက်ရှိအချက်အလက်တစ်ခု.descendants().forEach(ProcessHandle::destroy); လက်ရှိအချက်အလက်တစ်ခု.destroy(); }
    }
    private အလုပ်နယ်ပယ်() throws IOException {
        Files.createDirectories(လုပ်ဆောင်ဖိုင်တွဲ);
        Font စာလုံးပုံစံတန်ဖိုး = new Font("Monospaced", Font.PLAIN, 16);
        မူရင်းကုဒ်.setFont(စာလုံးပုံစံတန်ဖိုး); အထွက်.setFont(စာလုံးပုံစံတန်ဖိုး); အထွက်.setEditable(false);
        မူရင်းကုဒ်.setTabSize(4);
        မူရင်းကုဒ်.setMargin(new Insets(10, 12, 10, 12));
        အထွက်.setMargin(new Insets(8, 12, 8, 12));
        မူရင်းကုဒ်.setBackground(new Color(250, 251, 252));
        မူရင်းကုဒ်.setForeground(new Color(32, 43, 58));
        JPanel အမိန့်ဘောင်ကွက် = new JPanel();
        အမိန့်ဘောင်ကွက်.add(new JLabel("ဖိုင်")); အမိန့်ဘောင်ကွက်.add(ဖိုင်အချက်အမည်);
        အမိန့်ဘောင်ကွက်.add(new JLabel("주 အတန်းတန်ဖိုး")); အမိန့်ဘောင်ကွက်.add(အတန်းအချက်အမည်);
        ခလုတ်(အမိန့်ဘောင်ကွက်, "ဖွင့်", this::ဖွင့်); ခလုတ်(အမိန့်ဘောင်ကွက်, "သိုလှောင်တန်ဖိုး", this::သိုလှောင်တန်ဖိုး);
        ခလုတ်(အမိန့်ဘောင်ကွက်, "မူရင်းကုဒ်ဘာသာပြန်", () -> မူရင်းကုဒ်ဘာသာပြန်ဆို(false, false));
        ခလုတ်(အမိန့်ဘောင်ကွက်, "စက်မောင်း", () -> မူရင်းကုဒ်ဘာသာပြန်ဆို(true, false));
        ခလုတ်(အမိန့်ဘောင်ကွက်, "စက်မောင်း ဖိုင် အချက်ဖန်တီး", () -> မူရင်းကုဒ်ဘာသာပြန်ဆို(false, true));
        ခလုတ်(အမိန့်ဘောင်ကွက်, "ခဏရပ်လုပ်ဆောင်မှု", this::ခဏရပ်လုပ်ဆောင်မှု);
        JSplitPane စားလဒ် = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(မူရင်းကုဒ်), new JScrollPane(အထွက်));
        စားလဒ်.setResizeWeight(0.75);
        ဝင်း.add(အမိန့်ဘောင်ကွက်, BorderLayout.NORTH); ဝင်း.add(စားလဒ်, BorderLayout.CENTER);
        ဝင်း.setSize(1200, 750); ဝင်း.setLocationRelativeTo(null);
        ဝင်း.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ဝင်း.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ဖြစ်ရပ်) { ခဏရပ်လုပ်ဆောင်မှု(); အလုပ်သမားတန်ဖိုး.shutdownNow(); }
        });
        ဖွင့်(); ဝင်း.setVisible(true);
    }
    public static void main(String[] အချက်များ) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource မူလသတ်မှတ်စာလုံးပုံစံ = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object အချက်တန်ဖိုး : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(အချက်တန်ဖိုး) instanceof Font) UIManager.put(အချက်တန်ဖိုး, မူလသတ်မှတ်စာလုံးပုံစံ);
                }
                new အလုပ်နယ်ပယ်();
            } catch (Exception အမှား) { အမှား.printStackTrace(); }
        });
    }
}
