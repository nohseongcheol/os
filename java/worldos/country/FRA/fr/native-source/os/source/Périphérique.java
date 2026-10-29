// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Frontière native restreinte du compilateur, réservée aux instructions x86 et à l’accès aux adresses physiques. */
public final class Périphérique {
    public static native int mémoireFichier();
    public static native int lotFichierJava();
    public static native int tailleLotFichierJava();
    public static native int lireOctetEntréeSortie(int numéro);
    public static native void écrireOctetEntréeSortie(int numéro, int valeur);
    public static native int lireMémoire(int adresse);
    public static native void écrireMémoire(int adresse, int valeur);
    public static native int marqueurAmorçage();
    public static native int informationAmorçage();
    public static native int utilisationTableau();
    public static native void céderBrièvement();
    public static native void exécutionArrêterMachine();
    public static native void terminerTest(int valeur);
    public static native int lireEntierEntréeSortie(int numéro);
    public static native void écrireEntierEntréeSortie(int numéro, int valeur);
    public static native void écrireCourtEntréeSortie(int numéro, int valeur);
    public static native int lireCourtEntréeSortie(int numéro);
    public static native void préparerProgrammeUtilisateur();
    public static native void contenuEffacerContenuUtilisateur();
    public static native int lancerProgrammeUtilisateur(int adresseEntréeÉlément, int adressePileOpérande);
    public static native int millisecondes();
    public static native int millisecondesRestantUtilisateur();
    public static native int LotCodeExécutable();
    public static native int tailleLotCodeExécutable();
    public static native int mémoireRéseau();
}
