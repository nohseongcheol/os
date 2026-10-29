// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.Java;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** Outil de fichiers UTF-8 utilisant directement Path et IOException standard. */
public final class Fichier {
    private Fichier() {}
    public static Path chemin(String nom) { return Path.of(nom); }
    public static String lire(Path chemin) throws IOException {
        return Files.readString(chemin, StandardCharsets.UTF_8);
    }
    public static Path écrire(Path chemin, String valeurContenuValeur) throws IOException {
        return Files.writeString(chemin, valeurContenuValeur, StandardCharsets.UTF_8);
    }
    public static byte[] lireValeurOctet(Path chemin) throws IOException { return Files.readAllBytes(chemin); }
    public static Path écrireValeurOctet(Path chemin, byte[] valeurContenuValeur) throws IOException { return Files.write(chemin, valeurContenuValeur); }
    public static Path créerRépertoire(Path chemin) throws IOException { return Files.createDirectories(chemin); }
    public static boolean effectueExistence(Path chemin) { return Files.exists(chemin); }
    public static boolean effacerEntréeÉlément(Path chemin) throws IOException { return Files.deleteIfExists(chemin); }
    public static List<Path> listeEntréeÉlément(Path chemin) throws IOException {
        try (Stream<Path> valeurEntréeÉlément = Files.list(chemin)) { return valeurEntréeÉlément.sorted().collect(Collectors.toList()); }
    }
}
