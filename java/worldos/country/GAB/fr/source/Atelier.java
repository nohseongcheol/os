// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.GAB.l_fr;
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
public final class Atelier {
    private final JFrame fenêtre = new JFrame();
    private final JTextArea source = new JTextArea();
    private final JTextArea sortie = new JTextArea();
    private final JTextField chemin = new JTextField("source.java", 26);
    private final JTextField nom = new JTextField("source", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path répertoire = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService filTravail = Executors.newSingleThreadExecutor();
    private volatile Process processus;

    private String étiquette(String clé) {
        return messages.getProperty(clé, clé);
    }

    private void ajouter(String texte) {
        SwingUtilities.invokeLater(() -> {
            sortie.append(texte);
            sortie.setCaretPosition(sortie.getDocument().getLength());
        });
    }

    private void erreur(Exception exception) {
        ajouter(étiquette("error") + ": " + exception.toString() + "\n");
    }

    private void bouton(JPanel panneau, String clé, Runnable action) {
        JButton bouton = new JButton(étiquette(clé));
        bouton.addActionListener(événement -> action.run());
        panneau.add(bouton);
    }

    private void charger() {
        try {
            source.setText(Files.readString(répertoire.resolve(chemin.getText()), StandardCharsets.UTF_8));
            source.setCaretPosition(0);
        } catch (Exception exception) { erreur(exception); }
    }

    private boolean enregistrer() {
        try {
            Path fichier = répertoire.resolve(chemin.getText()).normalize();
            Files.createDirectories(fichier.getParent());
            Files.writeString(fichier, source.getText(), StandardCharsets.UTF_8);
            ajouter(étiquette("save") + ": " + fichier + "\n");
            return true;
        } catch (Exception exception) { erreur(exception); return false; }
    }

    private int exécuter(List<String> commande) throws Exception {
        processus = new ProcessBuilder(commande).directory(répertoire.toFile()).redirectErrorStream(true).start();
        try (BufferedReader lecteur = new BufferedReader(new InputStreamReader(processus.getInputStream(), StandardCharsets.UTF_8))) {
            String ligne;
            while ((ligne = lecteur.readLine()) != null) ajouter(ligne + "\n");
        }
        int résultat = processus.waitFor();
        processus = null;
        ajouter(étiquette("result") + ": " + résultat + "\n");
        return résultat;
    }

    private void compiler(boolean lancer) {
        if (!enregistrer()) return;
        String fichier = répertoire.resolve(chemin.getText()).toString();
        String nomClasse = nom.getText().trim();
        String texte = arguments.getText();
        filTravail.submit(() -> {
            try {
                Files.createDirectories(répertoire.resolve("classes"));
                int résultat = exécuter(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", répertoire.resolve("classes").toString(), fichier));
                if (lancer && résultat == 0) {
                    List<String> commande = new ArrayList<>(Arrays.asList("java", "-cp", répertoire.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", nomClasse));
                    StreamTokenizer analyseur = new StreamTokenizer(new StringReader(texte));
                    analyseur.resetSyntax(); analyseur.wordChars(33, 65535); analyseur.whitespaceChars(0, 32);
                    analyseur.quoteChar('"'); analyseur.quoteChar('\'');
                    while (analyseur.nextToken() != StreamTokenizer.TT_EOF) commande.add(analyseur.sval);
                    exécuter(commande);
                }
            } catch (Exception exception) { erreur(exception); }
        });
    }

    private void arrêter() {
        Process processusCourant = processus;
        if (processusCourant != null) {
            processusCourant.descendants().forEach(ProcessHandle::destroyForcibly);
            processusCourant.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(répertoire.toFile()).start(); }
        catch (Exception exception) { erreur(exception); }
    }

    private void choisir() {
        JFileChooser sélecteur = new JFileChooser(répertoire.toFile());
        if (sélecteur.showOpenDialog(fenêtre) == JFileChooser.APPROVE_OPTION) {
            chemin.setText(sélecteur.getSelectedFile().getAbsolutePath());
            charger();
        }
    }

    private void initialiser() {
        try (Reader lecteur = new InputStreamReader(Atelier.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(lecteur);
            Files.createDirectories(répertoire);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        fenêtre.setTitle(étiquette("workspace") + " · WorldOS " + étiquette("identity"));
        fenêtre.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        fenêtre.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent événement) {
                arrêter(); filTravail.shutdownNow(); System.exit(0);
            }
        });
        source.setFont(new Font("Monospaced", Font.PLAIN, 17));
        source.setTabSize(4);
        sortie.setFont(new Font("Monospaced", Font.PLAIN, 14));
        sortie.setEditable(false);
        JPanel panneau = new JPanel(new GridLayout(0, 1));
        JPanel fichier = new JPanel(new FlowLayout(FlowLayout.LEADING));
        fichier.add(new JLabel(étiquette("file"))); fichier.add(chemin);
        panneau.add(fichier);
        JPanel barreOutils = new JPanel(new FlowLayout(FlowLayout.LEADING));
        bouton(barreOutils, "open", () -> choisir());
        bouton(barreOutils, "save", () -> enregistrer());
        bouton(barreOutils, "compile", () -> compiler(false));
        bouton(barreOutils, "run", () -> compiler(true));
        bouton(barreOutils, "stop", () -> arrêter());
        bouton(barreOutils, "terminal", () -> terminal());
        panneau.add(barreOutils);
        JPanel réglages = new JPanel(new FlowLayout(FlowLayout.LEADING));
        réglages.add(new JLabel(étiquette("class"))); réglages.add(nom);
        réglages.add(new JLabel(étiquette("arguments"))); réglages.add(arguments);
        panneau.add(réglages);
        JSplitPane séparer = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(source), new JScrollPane(sortie));
        séparer.setResizeWeight(0.72);
        fenêtre.add(panneau, BorderLayout.NORTH);
        fenêtre.add(séparer, BorderLayout.CENTER);
        panneau.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(étiquette("locale"))));
        séparer.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        source.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        sortie.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension taille = Toolkit.getDefaultToolkit().getScreenSize();
        fenêtre.setSize(Math.min(1240, taille.width - 40), Math.min(760, taille.height - 60));
        fenêtre.setLocationRelativeTo(null);
        fenêtre.setVisible(true);
        charger();
        séparer.setDividerLocation(0.72);
        ajouter("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        ajouter(étiquette("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Atelier().initialiser());
    }
}
