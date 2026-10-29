// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
/** Arguments de ligne de commande fournis par la JVM du projet à la méthode d’entrée, sans le nom de classe. */
public final class Arguments {
    private Arguments() {}
    public static native int nombreÉlémentsÉlémentListe();
    public static native String texte(int indiceOrdinal) throws ExceptionBornes;
}
