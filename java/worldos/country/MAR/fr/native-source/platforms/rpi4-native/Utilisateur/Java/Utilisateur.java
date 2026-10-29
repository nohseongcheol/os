// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Liaison SVC réservée aux outils Java ARM64 EL0, construite avec les sources des outils x86 existants. */
public final class Utilisateur {
    public static native int ouvrirDescripteurFichier(int[] nom, int réglages);
    public static native int lireOctetFichierUn(int entréeÉlémentDescripteur);
    public static native int écrireOctetFichierUn(int entréeÉlémentDescripteur, int valeur);
    public static native int fermerDescripteurFichier(int entréeÉlémentDescripteur);
    public static native int lireFichier(int[] nom, int[] Données);
    public static native int écrireFichier(int[] nom, int[] Données, int longueur);
    public static native int écrire(String texte);
    public static native int écrireValeurCaractère(int valeur);
    public static native int nombreÉlémentsArguments();
    public static native String arguments(int numéro);
    public static native int numéroOutil();
    public static native int connexionÉcran(int action, int numéro, int opérandePremier, int opérandeDeuxième, int opérandeTroisième, int opérandeQuatrième);
    public static native int texteÉcran(int numéro, int[] texte, int longueur);
    public static native int largeurÉcran();
    public static native int hauteurÉcran();
    public static native int contrôleFlux(int action, int entréeÉlémentDescripteur, int valeur);
    public static native int connecterFlux(int entréeÉlémentDescripteur, int adresse, int valeurPort);
    public static native int ouvrirRéseau(int valeurPort);
    public static native int envoyerRéseau(int entréeÉlémentDescripteur, int adresse, int valeurPort, int[] Données, int longueur);
    public static native int recevoirRéseau(int entréeÉlémentDescripteur, int[] Données, int longueur);
    public static native int portRéseau(int entréeÉlémentDescripteur);
    public static native int millisecondes();
    public static native int attendreImagePour();
    public static native int rectangle(int positionHorizontal, int positionVertical, int étendueLargeur, int valeurHauteur, int valeurCouleur);
}
