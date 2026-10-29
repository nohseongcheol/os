// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
/** Confie un travail à la file d’événements de l’affichage du projet. */
public final class FileAttenteÉvènement {
    private FileAttenteÉvènement() {}
    public static native void invoquerUltérieur(TâcheTâcheExécutable ActionTâche);
    public static native boolean estDistributionEnCoursÉvènement();
}
