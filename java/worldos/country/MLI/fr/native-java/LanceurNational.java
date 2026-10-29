// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** Outil Java hôte chargé de vérifier et restaurer les dépendances, construire et exécuter une édition nationale indépendante. */
public final class LanceurNational {
    static final class AnalyseurDonnées {
        final String source; int position;
        AnalyseurDonnées(String texte) { source = texte; }
        void sauterEspacesBlancs() { while (position < source.length() && Character.isWhitespace(source.charAt(position))) position++; }
        Object lire() {
            sauterEspacesBlancs(); char valeurCaractère = source.charAt(position++);
            if (valeurCaractère == '{') {
                Map<String,Object> résultat = new LinkedHashMap<>(); sauterEspacesBlancs();
                if (source.charAt(position) == '}') { position++; return résultat; }
                while (true) {
                    String nom = (String)lire(); sauterEspacesBlancs(); if (source.charAt(position++) != ':') throw new IllegalArgumentException("Données valeurDélimiteur erreur");
                    résultat.put(nom, lire()); sauterEspacesBlancs(); char valeurDélimiteur = source.charAt(position++);
                    if (valeurDélimiteur == '}') return résultat; if (valeurDélimiteur != ',') throw new IllegalArgumentException("Données valeurDélimiteur erreur");
                }
            }
            if (valeurCaractère == '[') {
                List<Object> résultat = new ArrayList<>(); sauterEspacesBlancs();
                if (source.charAt(position) == ']') { position++; return résultat; }
                while (true) {
                    résultat.add(lire()); sauterEspacesBlancs(); char valeurDélimiteur = source.charAt(position++);
                    if (valeurDélimiteur == ']') return résultat; if (valeurDélimiteur != ',') throw new IllegalArgumentException("Données valeurDélimiteur erreur");
                }
            }
            if (valeurCaractère == '"') {
                StringBuilder résultat = new StringBuilder();
                while (true) {
                    char élémentListeSuivant = source.charAt(position++); if (élémentListeSuivant == '"') return résultat.toString();
                    if (élémentListeSuivant == '\\') {
                        élémentListeSuivant = source.charAt(position++);
                        if (élémentListeSuivant == 'u') { résultat.append((char)Integer.parseInt(source.substring(position, position + 4),16)); position += 4; continue; }
                        if (élémentListeSuivant == 'n') élémentListeSuivant = '\n'; else if (élémentListeSuivant == 'r') élémentListeSuivant = '\r'; else if (élémentListeSuivant == 't') élémentListeSuivant = '\t';
                        else if (élémentListeSuivant == 'b') élémentListeSuivant = '\b'; else if (élémentListeSuivant == 'f') élémentListeSuivant = '\f';
                        else if (élémentListeSuivant != '"' && élémentListeSuivant != '\\' && élémentListeSuivant != '/') throw new IllegalArgumentException("Caractères 이스케이프 erreur");
                    }
                    résultat.append(élémentListeSuivant);
                }
            }
            int lancer = position - 1;
            while (position < source.length() && ",]} \t\r\n".indexOf(source.charAt(position)) < 0) position++;
            String valeur = source.substring(lancer, position);
            if (valeur.equals("true")) return Boolean.TRUE; if (valeur.equals("false")) return Boolean.FALSE; if (valeur.equals("null")) return null;
            return Double.valueOf(valeur);
        }
    }
    static String fichierHachage(Path chemin) throws Exception {
        MessageDigest calculRésultat = MessageDigest.getInstance("SHA-256"); byte[] Données = new byte[1024 * 1024];
        try (InputStream valeurEntrée = Files.newInputStream(chemin)) { for (int longueur; (longueur = valeurEntrée.read(Données)) >= 0;) calculRésultat.update(Données,0,longueur); }
        return texteHachage(calculRésultat.digest());
    }
    static String texteHachage(byte[] Données) {
        StringBuilder texte = new StringBuilder(); for (byte valeur : Données) texte.append(String.format(Locale.ROOT,"%02x",valeur & 255)); return texte.toString();
    }
    static Path cheminIntérieur(Path racineProjet, String nom) {
        Path résultat = racineProjet.resolve(nom).normalize();
        if (nom.isEmpty() || Paths.get(nom).isAbsolute() || !résultat.startsWith(racineProjet) || nom.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 chemin: " + nom);
        for (Path valeurSousPartie : Paths.get(nom)) if (valeurSousPartie.toString().equals("..")) throw new IllegalArgumentException("상위 chemin valeurProhibé: " + nom);
        for (Path élémentListeActuel = résultat; élémentListeActuel != null && élémentListeActuel.startsWith(racineProjet); élémentListeActuel = élémentListeActuel.getParent())
            if (Files.isSymbolicLink(élémentListeActuel)) throw new IllegalArgumentException("dépendances 경로의 링크 valeurProhibé: " + nom);
        return résultat;
    }
    static String sortieCommande(List<String> commande) throws Exception {
        Process valeurProcessus = new ProcessBuilder(commande).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String résultat = new String(valeurProcessus.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (valeurProcessus.waitFor() != 0) throw new IOException("commande valeurÉchec: " + commande.get(0)); return résultat;
    }
    static void extraire(Path valeurArchive, Path valeurDestination) throws Exception {
        for (String nom : sortieCommande(Arrays.asList("tar","-tzf",valeurArchive.toString())).split("\n")) cheminIntérieur(valeurDestination, nom);
        for (String ligne : sortieCommande(Arrays.asList("tar","-tvzf",valeurArchive.toString())).split("\n"))
            if (!ligne.isEmpty() && ligne.charAt(0) != '-' && ligne.charAt(0) != 'd') throw new IOException("valeurExtérieur 링크 또는 valeurSpécial 파일을 포함한 dépendances");
        Files.createDirectories(valeurDestination);
        int valeurÉtatValeur = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",valeurArchive.toString(),"-C",valeurDestination.toString()).inheritIO().start().waitFor();
        if (valeurÉtatValeur != 0) throw new IOException("dépendances valeurArchive libérerStockage valeurÉchec");
    }
    static void invoquer(Path cheminTravailEnCours, Path Outils, List<String> arguments, Map<String,String> environnement) throws Exception {
        List<String> commande = new ArrayList<>(Arrays.asList("python3", Outils.toString())); commande.addAll(arguments);
        ProcessBuilder exécuterCommande = new ProcessBuilder(commande).directory(cheminTravailEnCours.toFile()).inheritIO(); exécuterCommande.environment().putAll(environnement);
        int valeurÉtatValeur = exécuterCommande.start().waitFor(); if (valeurÉtatValeur != 0) throw new IOException("Outils valeurÉchec: " + Outils + " (" + valeurÉtatValeur + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] arguments) throws Exception {
        if (arguments.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String action = arguments[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(action)) throw new IllegalArgumentException("알 nombre 없는 action");
        Path racineProjet = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> réglages = (Map<String,Object>)new AnalyseurDonnées(Files.readString(racineProjet.resolve("native.json"),StandardCharsets.UTF_8)).lire();
        Path arbreSource = cheminIntérieur(racineProjet,(String)réglages.get("source")), valeurNoyau = cheminIntérieur(arbreSource,(String)réglages.get("native"));
        List<String> fichiersPossédé = (List<String>)(List<?>)réglages.get("owned_files");
        for (String nom : fichiersPossédé) if (!Files.isRegularFile(cheminIntérieur(arbreSource,nom))) throw new IOException("arbreSource méthodeManquant: " + nom);
        if (action.equals("check")) { System.out.println(réglages.get("country") + " " + réglages.get("language") + " 독립 arbreSource vérifier estTerminé"); return; }
        String cheminRelatifRessource = (String)réglages.getOrDefault("resource_root", ".");
        if (!cheminRelatifRessource.equals(".") && !cheminRelatifRessource.equals("..")) throw new IllegalArgumentException("dépendances racineProjet chemin erreur");
        Path valeurRessource = racineProjet.resolve(cheminRelatifRessource).normalize(); Path valeurArchive = valeurRessource.resolve("native-vendor.tar.gz");
        String hachageAttendu = (String)réglages.get("vendor_sha256");
        if (!fichierHachage(valeurArchive).equals(hachageAttendu)) throw new IOException("dépendances SHA-256 불일치");
        Path valeurMarqueur = arbreSource.resolve(".vendor-sha256");
        if (!Files.isRegularFile(valeurMarqueur) || !Files.readString(valeurMarqueur).trim().equals(hachageAttendu)) { extraire(valeurArchive, arbreSource); Files.writeString(valeurMarqueur,hachageAttendu + "\n"); }
        Map<String,String> environnement = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (environnement.containsKey("IP_CONFIG")) ipConfig = Paths.get(environnement.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = racineProjet; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = arbreSource.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        environnement.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(action) && !environnement.containsKey("QEMU_AARCH64")) {
            Path LanceurProgramme = valeurRessource.resolve("host/qemu"), marqueurLanceur = valeurRessource.resolve("host/.qemu-sha256");
            String hachageLanceur = (String)réglages.get("qemu_sha256");
            if (!Files.isRegularFile(LanceurProgramme) || !Files.isRegularFile(marqueurLanceur) || !Files.readString(marqueurLanceur).trim().equals(hachageLanceur)) {
                Path archiveLanceur = valeurRessource.resolve("qemu-host.tar.gz"); if (!fichierHachage(archiveLanceur).equals(hachageLanceur)) throw new IOException("QEMU SHA-256 불일치");
                extraire(archiveLanceur,valeurRessource.resolve("host")); Files.writeString(marqueurLanceur,hachageLanceur + "\n");
            }
            environnement.put("QEMU_AARCH64",LanceurProgramme.toString());
        }
        MessageDigest calculRésultat = MessageDigest.getInstance("SHA-256"); Collections.sort(fichiersPossédé);
        for (String nom : fichiersPossédé) { calculRésultat.update(nom.getBytes(StandardCharsets.UTF_8)); calculRésultat.update(Files.readAllBytes(cheminIntérieur(arbreSource,nom))); }
        calculRésultat.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); calculRésultat.update(Files.readAllBytes(ipConfig));
        String hachageSource = texteHachage(calculRésultat.digest()); Path construireMarqueur = valeurNoyau.resolve("build/worldos-source.sha256");
        if (action.equals("build") || !Files.isRegularFile(construireMarqueur) || !Files.readString(construireMarqueur).trim().equals(hachageSource)) {
            invoquer(valeurNoyau,cheminIntérieur(valeurNoyau,(String)réglages.get("builder")),Collections.emptyList(),environnement);
            Files.writeString(construireMarqueur,hachageSource + "\n");
        }
        List<String> argumentsLanceur = new ArrayList<>(Arrays.asList(arguments).subList(1,arguments.length));
        if (action.equals("run") || action.equals("desktop")) {
            if (action.equals("desktop")) argumentsLanceur.add(0,"--desktop");
            invoquer(valeurNoyau,cheminIntérieur(valeurNoyau,(String)réglages.get("runner")),argumentsLanceur,environnement);
        } else if (action.equals("image")) invoquer(valeurNoyau,cheminIntérieur(valeurNoyau,(String)réglages.get("image_builder")),argumentsLanceur,environnement);
        else if (action.equals("test-system")) {
            argumentsLanceur.add(0,racineProjet.toString()); argumentsLanceur.add(0,"--edition");
            invoquer(valeurNoyau,cheminIntérieur(valeurNoyau,(String)réglages.get("system_tester")),argumentsLanceur,environnement);
        }
    }
}
