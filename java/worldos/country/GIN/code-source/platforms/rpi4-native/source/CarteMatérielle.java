// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Frontière machine ARM64. Ne jamais tronquer un pointeur en int Java. */
public final class CarteMatérielle {
    public static native int lirePixelPrésenter(int positionHorizontal, int positionVertical);
    public static native void écrirePixelPrésenter(int positionHorizontal, int positionVertical, int valeurCouleur);
    public static native int contrôleDistant(int valeurGenre, int action);
    public static native void commandeDistantFin(int valeurÉtatValeur);
    public static native void attendreDistant(int valeurÉtatValeur);
    public static native void écrireSériel(int valeur);
    public static native int lireSériel();
    public static native int millisecondes();
    public static native int niveauPrivilègeCPU();
    public static native int préparerÉcran();
    public static native int largeurÉcran();
    public static native int hauteurÉcran();
    public static native void placerPixelÉcran(int positionHorizontal, int positionVertical, int valeurCouleur);
    public static native void céderProcesseur();
    public static native int créerTâche(int numéro);
    public static native int étatValeurTâche(int numéro);
    public static native void arrêter(int valeurÉtatValeur);
    public static native int testCpp();
    public static native int lancerProgrammeUtilisateur(int numéro);
    public static native int contrôlerProgrammeUtilisateur();
    public static native int préparerArguments(int nombreÉlémentsÉlémentListe);
    public static native int exécuterFichierUtilisateur();
    public static native int exécuterFichierLinux();
    public static native int octetArgument(int numéro, int position, int valeur);
    public static native int terminal(int action);
    public static native int programmeUtilisateurContrôle(int action);
    public static native void entréeSortieCommuter(int action);
    public static native int serviceTransfertFichier(int action);
    public static native int étatRéseau(int valeurEntréeÉlément, int numéro);
    public static native int réglagesRéseau(int action, int adresse, int valeurMasque, int valeurPasserelle);
    public static native int envoyerRéponseRetour(int adresse, int valeurOrdre);
    public static native int lireRéponseRetour(int valeurEntréeÉlément);
    public static native int systèmeInterroger(int valeurEntréeÉlément, int numéro);
    public static native void désactivéAlimentation();
}
