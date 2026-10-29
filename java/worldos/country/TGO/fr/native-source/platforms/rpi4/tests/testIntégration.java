// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import français.Java.*;
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

public class testIntégration {
    interface valeur { long lire(); }
    static class valeurParent { protected long valeur = 42; }
    static class valeurEnfant extends valeurParent implements valeur { public long lire() { return valeur; } }
    private static void vérifier(boolean condition, String nom) {
        if (!condition) throw new AssertionError(nom);
        System.out.println("PASS " + nom);
    }
    public static void main(String[] arguments) throws Exception {
        String texte = "한글 日本語 العربية हिन्दी 😀";
        Path valeurStocker = Path.of(System.getProperty("user.home"), "donnéesValidation.txt");
        Fichier.écrire(valeurStocker, texte);
        vérifier(Fichier.lire(valeurStocker).equals(texte), "UTF8_FILE");
        vérifier(Caractères.nombreÉlémentsPointCode("한😀") == 2, "UNICODE");
        vérifier(Caractères.normaliserValeur("\u1100\u1161").equals("가"), "NORMALIZATION");
        valeur valeurObjet = new valeurEnfant();
        vérifier(valeurObjet.lire() == 42 && (long)valeurEnfant.class.getMethod("lire").invoke(valeurObjet) == 42, "OBJECT_INHERITANCE_REFLECTION");
        vérifier(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("valider"); }
        catch (IOException exception) { vérifier(exception.getMessage().equals("valider"), "EXCEPTION"); }
        AtomicInteger valeurSomme = new AtomicInteger();
        Thread valeurFilExécution = Tâche.lancer("한글 valeurFilExécution", () -> valeurSomme.set(123));
        Tâche.attendreFin(valeurFilExécution);
        vérifier(valeurSomme.get() == 123, "THREAD");
        ExecutorService valeurTâcheFond = Executors.newSingleThreadExecutor();
        try (ServerSocket valeurServeur = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> réponse = valeurTâcheFond.submit(() -> {
                try (Socket valeurPriseRéseau = valeurServeur.accept()) {
                    BufferedReader lire = new BufferedReader(new InputStreamReader(valeurPriseRéseau.getInputStream()));
                    String ligne;
                    while ((ligne = lire.readLine()) != null && !ligne.isEmpty()) {}
                    byte[] texteCorps = Caractères.encoder(texte);
                    valeurPriseRéseau.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + texteCorps.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    valeurPriseRéseau.getOutputStream().write(texteCorps);
                } catch (IOException erreur) { throw new UncheckedIOException(erreur); }
            });
            vérifier(Communication.valeurPrendre(URI.create("http://127.0.0.1:" + valeurServeur.getLocalPort()), Duration.ofSeconds(30)).body().equals(texte), "HTTP_TCP");
            réponse.get(30, TimeUnit.SECONDS);
        } finally { valeurTâcheFond.shutdownNow(); }
        vérifier(new ProcessBuilder("/bin/echo", "valeurProcessus").start().waitFor() == 0, "PROCESS");
        if (arguments.length > 0 && arguments[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font valeurPolice = new Font("Dialog", Font.PLAIN, 18);
                vérifier(valeurPolice.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                vérifier(valeurPolice.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea BoîteTexte = new JTextArea(texte);
                BoîteTexte.setFont(valeurPolice);
                JFrame fenêtre = Écran.fenêtre("그래픽 valider", BoîteTexte, 800, 240);
                BufferedImage Dessin = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D valeurPinceau = Dessin.createGraphics();
                fenêtre.paint(valeurPinceau); valeurPinceau.dispose();
                try { javax.imageio.ImageIO.write(Dessin, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException erreur) { throw new UncheckedIOException(erreur); }
                fenêtre.dispose();
                vérifier(BoîteTexte.getText().equals(texte), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
