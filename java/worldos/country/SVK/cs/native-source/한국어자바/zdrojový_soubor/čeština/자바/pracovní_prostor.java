// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.자바;

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

/** uživatelský_prostor 홈에서 Java 원문을 úprava_HODNOTA·kompilovat_zdroj·실행하는 작은 Swing pracovní_prostor. */
public final class pracovní_prostor {
    private final JFrame Okno = new JFrame("jkoros — 자바 pracovní_prostor");
    private final JTextArea zdrojový_soubor = new JTextArea();
    private final JTextArea výstupní_pozice = new JTextArea(8, 80);
    private final JTextField Soubor_položka_název = new JTextField("인사.java", 20);
    private final JTextField Třída_položka_název = new JTextField("인사", 16);
    private final Path pracovní_adresář = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService pracovník_HODNOTA = Executors.newSingleThreadExecutor();
    private volatile Process Proces_HODNOTA;
    private final String knihovna = "/opt/jkoros/lib/한국어자바.jar";

    private void povinnost_zvěřejnit(String text) { SwingUtilities.invokeLater(() -> výstupní_pozice.append(text + "\n")); }
    private void tlačítko(JPanel verze_HODNOTA, String Název, Runnable 행동) {
        JButton tlačítko = new JButton(Název);
        tlačítko.addActionListener(Události -> 행동.run());
        verze_HODNOTA.add(tlačítko);
    }
    private boolean Store_HODNOTA() {
        try {
            Path cesta_2 = pracovní_adresář.resolve(Soubor_položka_název.getText());
            Files.createDirectories(cesta_2.getParent());
            název_souboru.Zápis(cesta_2, zdrojový_soubor.getText());
            povinnost_zvěřejnit("Store_HODNOTA: " + cesta_2);
            return true;
        } catch (Exception chyba) { povinnost_zvěřejnit(chyba.toString()); return false; }
    }
    private void Otevřít() {
        try { zdrojový_soubor.setText(název_souboru.Čtení(pracovní_adresář.resolve(Soubor_položka_název.getText()))); }
        catch (Exception chyba) { povinnost_zvěřejnit(chyba.toString()); }
    }
    private int příkaz(List<String> příkaz) throws Exception {
        Proces_HODNOTA = new ProcessBuilder(příkaz).directory(pracovní_adresář.toFile()).redirectErrorStream(true).start();
        try (BufferedReader vstupní_řádek = new BufferedReader(new InputStreamReader(Proces_HODNOTA.getInputStream(), StandardCharsets.UTF_8))) {
            String text;
            while ((text = vstupní_řádek.readLine()) != null) povinnost_zvěřejnit(text);
        }
        int Stav_HODNOTA = Proces_HODNOTA.waitFor(); Proces_HODNOTA = null;
        povinnost_zvěřejnit("Konec_program KÓD_HODNOTA: " + Stav_HODNOTA);
        return Stav_HODNOTA;
    }
    private void převést_zdroj(boolean Provést_příkaz, boolean spustitelný_soubor) {
        if (!Store_HODNOTA()) return;
        String vstup_HODNOTA = Soubor_položka_název.getText(), vstupní_bod_HODNOTA = Třída_položka_název.getText();
        pracovník_HODNOTA.submit(() -> {
            try {
                Files.createDirectories(pracovní_adresář.resolve("classes"));
                if (spustitelný_soubor) {
                    příkaz(Arrays.asList("jclassc", "--target", "openjdk", "--entry", vstupní_bod_HODNOTA,
                        "--classpath", knihovna, "-o", "실행프로그램", vstup_HODNOTA));
                } else if (příkaz(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", knihovna,
                        "-d", "classes", vstup_HODNOTA)) == 0 && Provést_příkaz) {
                    příkaz(Arrays.asList("java", "-cp", "classes:" + knihovna, vstupní_bod_HODNOTA));
                }
            } catch (Exception chyba) { povinnost_zvěřejnit(chyba.toString()); }
        });
    }
    private void Pozastavit_spuštění() {
        Process dobrá_zboží = Proces_HODNOTA;
        if (dobrá_zboží != null) { dobrá_zboží.descendants().forEach(ProcessHandle::destroy); dobrá_zboží.destroy(); }
    }
    private pracovní_prostor() throws IOException {
        Files.createDirectories(pracovní_adresář);
        Font písmo_HODNOTA = new Font("Monospaced", Font.PLAIN, 16);
        zdrojový_soubor.setFont(písmo_HODNOTA); výstupní_pozice.setFont(písmo_HODNOTA); výstupní_pozice.setEditable(false);
        zdrojový_soubor.setTabSize(4);
        zdrojový_soubor.setMargin(new Insets(10, 12, 10, 12));
        výstupní_pozice.setMargin(new Insets(8, 12, 8, 12));
        zdrojový_soubor.setBackground(new Color(250, 251, 252));
        zdrojový_soubor.setForeground(new Color(32, 43, 58));
        JPanel příkaz_panel = new JPanel();
        příkaz_panel.add(new JLabel("název_souboru")); příkaz_panel.add(Soubor_položka_název);
        příkaz_panel.add(new JLabel("주 Třída_HODNOTA")); příkaz_panel.add(Třída_položka_název);
        tlačítko(příkaz_panel, "Otevřít", this::Otevřít); tlačítko(příkaz_panel, "Store_HODNOTA", this::Store_HODNOTA);
        tlačítko(příkaz_panel, "kompilovat_zdroj", () -> převést_zdroj(false, false));
        tlačítko(příkaz_panel, "Provést_příkaz", () -> převést_zdroj(true, false));
        tlačítko(příkaz_panel, "Provést_příkaz název_souboru Create_položka", () -> převést_zdroj(false, true));
        tlačítko(příkaz_panel, "Pozastavit_spuštění", this::Pozastavit_spuštění);
        JSplitPane podíl_KV = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(zdrojový_soubor), new JScrollPane(výstupní_pozice));
        podíl_KV.setResizeWeight(0.75);
        Okno.add(příkaz_panel, BorderLayout.NORTH); Okno.add(podíl_KV, BorderLayout.CENTER);
        Okno.setSize(1200, 750); Okno.setLocationRelativeTo(null);
        Okno.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Okno.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Události) { Pozastavit_spuštění(); pracovník_HODNOTA.shutdownNow(); }
        });
        Otevřít(); Okno.setVisible(true);
    }
    public static void main(String[] argumenty) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource výchozí_písmo = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object položka_HODNOTA : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(položka_HODNOTA) instanceof Font) UIManager.put(položka_HODNOTA, výchozí_písmo);
                }
                new pracovní_prostor();
            } catch (Exception chyba) { chyba.printStackTrace(); }
        });
    }
}
