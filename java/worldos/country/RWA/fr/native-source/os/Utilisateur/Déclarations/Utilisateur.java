// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** API réservée aux ELF utilisateur de jkoros ; ni JNI Linux/JVM ni API java.net. */
public final class Utilisateur {
    public static native int ouvrirDescripteurFichier(int[] nomEntréeÉlémentFichier, int ouvrirRéglages);
    public static native int lireOctetFichierUn(int descripteurFichier);
    public static native int écrireOctetFichierUn(int descripteurFichier, int valeurOctet);
    public static native int fermerDescripteurFichier(int descripteurFichier);
    public static native int stockageFichierConfirmer(int descripteurFichier);
    public static native int lireFichier(int[] nom, int[] Données);
    public static native int écrireValeurCaractère(int Caractères);
    public static native int écrireFichier(int[] nom, int[] Données, int longueur);
    public static native int écrire(String valeurContenuValeur);
    public static native int nombreÉlémentsArguments();
    public static native String arguments(int numéro);
    public static native int permissionExécution();
    public static native int ouvrirRéseau(int portLocal);
    public static native int envoyerDonnées(int valeurPoignée, int adresse, int portDestination, int[] Données, int longueur);
    public static native int recevoirDonnées(int valeurPoignée, int[] Données, int millisecondesLimite);
    public static native int fermerRéseau(int valeurPoignée);
    public static native int adressePropre();
    public static native int adresseEnvoyé(int valeurPoignée);
    public static native int portEnvoyé(int valeurPoignée);
}
