// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class EntréeSortieTerminal {
    static void Caractères(int valeur) {
        if (valeur < 0x80) CarteMatérielle.écrireSériel(valeur);
        else if (valeur < 0x800) {
            CarteMatérielle.écrireSériel(0xc0 | (valeur >> 6)); CarteMatérielle.écrireSériel(0x80 | (valeur & 63));
        } else if (valeur < 0x10000) {
            CarteMatérielle.écrireSériel(0xe0 | (valeur >> 12)); CarteMatérielle.écrireSériel(0x80 | ((valeur >> 6) & 63)); CarteMatérielle.écrireSériel(0x80 | (valeur & 63));
        } else {
            CarteMatérielle.écrireSériel(0xf0 | (valeur >> 18)); CarteMatérielle.écrireSériel(0x80 | ((valeur >> 12) & 63));
            CarteMatérielle.écrireSériel(0x80 | ((valeur >> 6) & 63)); CarteMatérielle.écrireSériel(0x80 | (valeur & 63));
        }
    }
    static void écrire(String texte) {
        for (int numéro = 0; numéro < texte.length(); numéro++) {
            int valeur = texte.charAt(numéro);
            if (valeur >= 0xd800 && valeur <= 0xdbff && numéro + 1 < texte.length()) {
                int valeurBasExtrémité = texte.charAt(numéro + 1);
                if (valeurBasExtrémité >= 0xdc00 && valeurBasExtrémité <= 0xdfff) {
                    valeur = 0x10000 + ((valeur - 0xd800) << 10) + valeurBasExtrémité - 0xdc00; numéro++;
                }
            }
            if (valeur >= 0xd800 && valeur <= 0xdfff) valeur = 0xfffd;
            Caractères(valeur);
        }
    }
    static void nombre(int valeur) {
        if (valeur < 0) Caractères('-'); else valeur = -valeur;
        int indicePosition = 1000000000;
        boolean lancer = false;
        while (indicePosition > 0) {
            int valeurChiffre = -(valeur / indicePosition);
            if (valeurChiffre != 0 || lancer || indicePosition == 1) { Caractères('0' + valeurChiffre); lancer = true; }
            valeur %= indicePosition; indicePosition /= 10;
        }
    }
}
