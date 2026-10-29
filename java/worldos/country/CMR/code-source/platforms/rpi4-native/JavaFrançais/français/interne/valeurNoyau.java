// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
/** ABI fixe reliée par la JVM du projet ; ni JNI ni chargeur de méthodes native arbitraires. */
public final class valeurNoyau {
    private valeurNoyau() {}
    public static native int millisecondes();
    public static native int attendreImagePour();
    public static native int largeurÉcran();
    public static native int hauteurÉcran();
    public static native int rectangle(int positionHorizontal, int positionVertical, int étendueLargeur, int valeurHauteur, int valeurCouleur);
}
