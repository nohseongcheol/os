// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Sortie commune des outils invités et traitement des noms de fichiers ASCII. */
public final class OutilJava {
    /** Convertit un tableau d’octets UTF-8 en unités UTF-16 dans le même tableau. Refuse les entrées mal formées. */
    static int décoderSource(int[] Données, int longueur) {
        int lire = 0, écrire = 0;
        if (longueur >= 3 && Données[0] == 239 && Données[1] == 187 && Données[2] == 191) lire = 3;
        while (lire < longueur) {
            int valeur = Données[lire++], nombre = 0, valeurMinimal = 0;
            if (valeur >= 194 && valeur <= 223) { nombre = 1; valeurMinimal = 128; valeur &= 31; }
            else if (valeur >= 224 && valeur <= 239) { nombre = 2; valeurMinimal = 2048; valeur &= 15; }
            else if (valeur >= 240 && valeur <= 244) { nombre = 3; valeurMinimal = 65536; valeur &= 7; }
            else if (valeur >= 128 || valeur < 0) return -1;
            if (nombre > longueur - lire) return -1;
            for (int i = 0; i < nombre; i++) {
                int élémentListeSuivant = Données[lire++]; if ((élémentListeSuivant & 192) != 128) return -1;
                valeur = (valeur << 6) | (élémentListeSuivant & 63);
            }
            if (valeur < valeurMinimal || valeur > 0x10ffff || (valeur >= 0xd800 && valeur <= 0xdfff)) return -1;
            if (valeur >= 65536) { valeur -= 65536; Données[écrire++] = 0xd800 | (valeur >> 10); Données[écrire++] = 0xdc00 | (valeur & 1023); }
            else Données[écrire++] = valeur;
        }
        return écrire;
    }
    static void écrireNuméro(int valeur) {
        if (valeur < 0) Utilisateur.écrireValeurCaractère('-'); else valeur = -valeur;
        int indicePosition = 1000000000;
        boolean lancer = false;
        while (indicePosition != 0) {
            int nombre = -(valeur / indicePosition);
            if (nombre != 0 || lancer || indicePosition == 1) { Utilisateur.écrireValeurCaractère('0' + nombre); lancer = true; }
            valeur %= indicePosition; indicePosition /= 10;
        }
    }
    static int nom(int[] valeurDestination, String original) {
        if (original.length() >= valeurDestination.length) return -1;
        for (int nombre = 0; nombre < valeurDestination.length; nombre++) valeurDestination[nombre] = nombre < original.length() ? original.charAt(nombre) : 0;
        return original.length();
    }
    static boolean texteÉgal(String opérandePremier, String opérandeDeuxième) {
        if (opérandePremier.length() != opérandeDeuxième.length()) return false;
        for (int nombre = 0; nombre < opérandePremier.length(); nombre++) if (opérandePremier.charAt(nombre) != opérandeDeuxième.charAt(nombre)) return false;
        return true;
    }
}
