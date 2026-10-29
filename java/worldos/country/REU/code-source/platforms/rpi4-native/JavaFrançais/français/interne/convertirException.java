// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** Convertit les erreurs Java standard à la frontière de l’API française, sans modifier le sens des clauses catch standard. */
final class convertirException {
    private convertirException() {}
    public static ExceptionSortieEntrée sortieEntrée(java.io.IOException erreur) {
        if (erreur instanceof ExceptionSortieEntrée) return (ExceptionSortieEntrée)erreur;
        if (erreur instanceof java.net.SocketTimeoutException) return new ExceptionDélaiExpirationAttendre("Le délai d’attente de communication est dépassé.");
        if (erreur instanceof java.net.UnknownHostException) return new ExceptionRechercherAdresse("Impossible de résoudre l’adresse. Utilisez pour le moment une adresse IPv4 numérique.");
        if (erreur instanceof java.io.FileNotFoundException) return new ExceptionFichierManquant("Impossible d’ouvrir le fichier.");
        if (erreur instanceof java.net.SocketException) return new ExceptionCommunication("Échec de la connexion: " + erreur.getMessage());
        return new ExceptionSortieEntrée("Échec de l’opération d’entrée-sortie: " + erreur.getMessage());
    }
    public static RuntimeException exécuterCommande(RuntimeException erreur) {
        if (erreur instanceof java.lang.NumberFormatException) return new ÉchecFormatNuméro("Vérifiez le format et la plage du nombre.");
        if (erreur instanceof java.lang.IllegalArgumentException) return new ExceptionArgumentInvalide("Vérifiez la valeur et la plage de l’argument.");
        if (erreur instanceof java.lang.ArrayIndexOutOfBoundsException) return new ExceptionBornesTableau("L’indice dépasse les limites du tableau.");
        if (erreur instanceof java.lang.StringIndexOutOfBoundsException) return new ExceptionBornesChaîne("L’indice dépasse les limites de la chaîne.");
        if (erreur instanceof java.lang.IndexOutOfBoundsException) return new ExceptionBornes("La plage autorisée est dépassée.");
        if (erreur instanceof java.lang.NullPointerException) return new ExceptionRéférenceRéférenceNulle("La référence est nulle.");
        return new ExceptionExécution(erreur.getMessage());
    }
}
