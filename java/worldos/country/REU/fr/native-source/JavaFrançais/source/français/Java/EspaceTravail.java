// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.Java;

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

/** Petit atelier Swing pour éditer, compiler et exécuter les sources Java dans le répertoire personnel. */
public final class EspaceTravail {
    private final JFrame fenêtre = new JFrame("jkoros — Java EspaceTravail");
    private final JTextArea source = new JTextArea();
    private final JTextArea Sortie = new JTextArea(8, 80);
    private final JTextField nomEntréeÉlémentFichier = new JTextField("Salutation.java", 20);
    private final JTextField nomEntréeÉlémentClasse = new JTextField("Salutation", 16);
    private final Path répertoireTravailEnCours = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService valeurTâcheFond = Executors.newSingleThreadExecutor();
    private volatile Process valeurProcessus;
    private final String bibliothèque = "/opt/jkoros/lib/JavaFrançais.jar";

    private void notification(String texte) { SwingUtilities.invokeLater(() -> Sortie.append(texte + "\n")); }
    private void bouton(JPanel valeurVersion, String nom, Runnable valeurComportement) {
        JButton bouton = new JButton(nom);
        bouton.addActionListener(évènement -> valeurComportement.run());
        valeurVersion.add(bouton);
    }
    private boolean valeurStocker() {
        try {
            Path chemin = répertoireTravailEnCours.resolve(nomEntréeÉlémentFichier.getText());
            Files.createDirectories(chemin.getParent());
            Fichier.écrire(chemin, source.getText());
            notification("valeurStocker: " + chemin);
            return true;
        } catch (Exception erreur) { notification(erreur.toString()); return false; }
    }
    private void ouvrir() {
        try { source.setText(Fichier.lire(répertoireTravailEnCours.resolve(nomEntréeÉlémentFichier.getText()))); }
        catch (Exception erreur) { notification(erreur.toString()); }
    }
    private int commande(List<String> commande) throws Exception {
        valeurProcessus = new ProcessBuilder(commande).directory(répertoireTravailEnCours.toFile()).redirectErrorStream(true).start();
        try (BufferedReader ligne = new BufferedReader(new InputStreamReader(valeurProcessus.getInputStream(), StandardCharsets.UTF_8))) {
            String texte;
            while ((texte = ligne.readLine()) != null) notification(texte);
        }
        int valeurÉtatValeur = valeurProcessus.waitFor(); valeurProcessus = null;
        notification("programmeQuitter valeurCode: " + valeurÉtatValeur);
        return valeurÉtatValeur;
    }
    private void traduireSource(boolean exécuterCommande, boolean fichierCodeExécutable) {
        if (!valeurStocker()) return;
        String valeurEntrée = nomEntréeÉlémentFichier.getText(), valeurPointEntréeÉlément = nomEntréeÉlémentClasse.getText();
        valeurTâcheFond.submit(() -> {
            try {
                Files.createDirectories(répertoireTravailEnCours.resolve("classes"));
                if (fichierCodeExécutable) {
                    commande(Arrays.asList("jclassc", "--target", "openjdk", "--entry", valeurPointEntréeÉlément,
                        "--classpath", bibliothèque, "-o", "실행프로그램", valeurEntrée));
                } else if (commande(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", bibliothèque,
                        "-d", "classes", valeurEntrée)) == 0 && exécuterCommande) {
                    commande(Arrays.asList("java", "-cp", "classes:" + bibliothèque, valeurPointEntréeÉlément));
                }
            } catch (Exception erreur) { notification(erreur.toString()); }
        });
    }
    private void exécutionMettreEnPause() {
        Process élémentListeActuel = valeurProcessus;
        if (élémentListeActuel != null) { élémentListeActuel.descendants().forEach(ProcessHandle::destroy); élémentListeActuel.destroy(); }
    }
    private EspaceTravail() throws IOException {
        Files.createDirectories(répertoireTravailEnCours);
        Font valeurPolice = new Font("Monospaced", Font.PLAIN, 16);
        source.setFont(valeurPolice); Sortie.setFont(valeurPolice); Sortie.setEditable(false);
        source.setTabSize(4);
        source.setMargin(new Insets(10, 12, 10, 12));
        Sortie.setMargin(new Insets(8, 12, 8, 12));
        source.setBackground(new Color(250, 251, 252));
        source.setForeground(new Color(32, 43, 58));
        JPanel panneauCommande = new JPanel();
        panneauCommande.add(new JLabel("Fichier")); panneauCommande.add(nomEntréeÉlémentFichier);
        panneauCommande.add(new JLabel("주 valeurClasse")); panneauCommande.add(nomEntréeÉlémentClasse);
        bouton(panneauCommande, "ouvrir", this::ouvrir); bouton(panneauCommande, "valeurStocker", this::valeurStocker);
        bouton(panneauCommande, "compilerSource", () -> traduireSource(false, false));
        bouton(panneauCommande, "exécuterCommande", () -> traduireSource(true, false));
        bouton(panneauCommande, "exécuterCommande Fichier créerEntréeÉlément", () -> traduireSource(false, true));
        bouton(panneauCommande, "exécutionMettreEnPause", this::exécutionMettreEnPause);
        JSplitPane résultatDivision = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(source), new JScrollPane(Sortie));
        résultatDivision.setResizeWeight(0.75);
        fenêtre.add(panneauCommande, BorderLayout.NORTH); fenêtre.add(résultatDivision, BorderLayout.CENTER);
        fenêtre.setSize(1200, 750); fenêtre.setLocationRelativeTo(null);
        fenêtre.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        fenêtre.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent évènement) { exécutionMettreEnPause(); valeurTâcheFond.shutdownNow(); }
        });
        ouvrir(); fenêtre.setVisible(true);
    }
    public static void main(String[] arguments) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource policeDéfaut = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object valeurEntréeÉlément : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(valeurEntréeÉlément) instanceof Font) UIManager.put(valeurEntréeÉlément, policeDéfaut);
                }
                new EspaceTravail();
            } catch (Exception erreur) { erreur.printStackTrace(); }
        });
    }
}
