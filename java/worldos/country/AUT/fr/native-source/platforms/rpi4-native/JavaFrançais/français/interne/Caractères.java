// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
/** Conversion entre octets UTF-8 et chaînes UTF-16. La normalisation et la saisie composée sont traitées séparément. */
public final class Caractères {
    public static int nombreÉlémentsOctet(byte[] Données) { return Données.length; }
    private Caractères() {}
    public static int longueur(String texte) { return texte.length(); }
    public static boolean texteÉgal(String valeurAvantCôté, String valeurRetourArrièreCôté) { return valeurAvantCôté == null ? valeurRetourArrièreCôté == null : valeurAvantCôté.equals(valeurRetourArrièreCôté); }
    public static String texteColler(String valeurAvantCôté, String valeurRetourArrièreCôté) { return valeurAvantCôté.concat(valeurRetourArrièreCôté); }
    public static String valeurCouper(String texte, int lancer, int terminaison) { return texte.substring(lancer, terminaison); }
    public static int analyserEntier(String texte) { try { return Integer.parseInt(texte); } catch (NumberFormatException erreur) { throw new ÉchecFormatNuméro("Vérifiez le format et la plage du nombre."); } }
    public static String écrireValeurEntier(int nombre) { return Integer.toString(nombre); }
    public static int nombreÉlémentsPointCode(String texte) {
        int nombre = 0;
        for (int indiceBoucle = 0; indiceBoucle < texte.length(); indiceBoucle++, nombre++) {
            int codeCaractère = texte.charAt(indiceBoucle);
            if (codeCaractère >= 0xd800 && codeCaractère <= 0xdbff && indiceBoucle + 1 < texte.length() && texte.charAt(indiceBoucle + 1) >= 0xdc00 && texte.charAt(indiceBoucle + 1) <= 0xdfff) indiceBoucle++;
        }
        return nombre;
    }
    public static byte[] encoder(String texte) {
        byte[] valeurTemporaire = new byte[texte.length() * 3]; int écrit = 0;
        for (int indiceBoucle = 0; indiceBoucle < texte.length(); indiceBoucle++) {
            int codeCaractère = texte.charAt(indiceBoucle);
            if (codeCaractère >= 0xd800 && codeCaractère <= 0xdbff && indiceBoucle + 1 < texte.length() && texte.charAt(indiceBoucle + 1) >= 0xdc00 && texte.charAt(indiceBoucle + 1) <= 0xdfff) codeCaractère = 0x10000 + ((codeCaractère - 0xd800) << 10) + texte.charAt(++indiceBoucle) - 0xdc00;
            else if (codeCaractère >= 0xd800 && codeCaractère <= 0xdfff) codeCaractère = '?';
            if (codeCaractère < 128) valeurTemporaire[écrit++] = (byte)codeCaractère;
            else if (codeCaractère < 2048) { valeurTemporaire[écrit++] = (byte)(192 | codeCaractère >> 6); valeurTemporaire[écrit++] = (byte)(128 | codeCaractère & 63); }
            else if (codeCaractère < 65536) { valeurTemporaire[écrit++] = (byte)(224 | codeCaractère >> 12); valeurTemporaire[écrit++] = (byte)(128 | codeCaractère >> 6 & 63); valeurTemporaire[écrit++] = (byte)(128 | codeCaractère & 63); }
            else { valeurTemporaire[écrit++] = (byte)(240 | codeCaractère >> 18); valeurTemporaire[écrit++] = (byte)(128 | codeCaractère >> 12 & 63); valeurTemporaire[écrit++] = (byte)(128 | codeCaractère >> 6 & 63); valeurTemporaire[écrit++] = (byte)(128 | codeCaractère & 63); }
        }
        byte[] résultat = new byte[écrit]; System.arraycopy(valeurTemporaire, 0, résultat, 0, écrit); return résultat;
    }
    /** Refuse l’UTF-8 mal formé avec l’exception d’argument incorrect de l’API. */
    public static String déchiffrerDonnées(byte[] valeurOctet) {
        StringBuilder résultat = new StringBuilder();
        for (int indiceBoucle = 0; indiceBoucle < valeurOctet.length;) {
            int codeCaractère = valeurOctet[indiceBoucle++] & 255, nombre = codeCaractère < 128 ? 0 : codeCaractère >= 194 && codeCaractère < 224 ? 1 : codeCaractère >= 224 && codeCaractère < 240 ? 2 : codeCaractère >= 240 && codeCaractère <= 244 ? 3 : -1;
            if (nombre < 0 || valeurOctet.length - indiceBoucle < nombre) throw new ExceptionArgumentInvalide("UTF-8 invalide");
            int valeurMinimal = nombre == 1 ? 128 : nombre == 2 ? 2048 : nombre == 3 ? 65536 : 0;
            if (nombre > 0) codeCaractère &= (1 << (6 - nombre)) - 1;
            for (int positionInterne = 0; positionInterne < nombre; positionInterne++) { int valeurRetourArrièreCôté = valeurOctet[indiceBoucle++] & 255; if ((valeurRetourArrièreCôté & 192) != 128) throw new ExceptionArgumentInvalide("UTF-8 invalide"); codeCaractère = codeCaractère << 6 | valeurRetourArrièreCôté & 63; }
            if (codeCaractère < valeurMinimal || codeCaractère > 0x10ffff || codeCaractère >= 0xd800 && codeCaractère <= 0xdfff) throw new ExceptionArgumentInvalide("UTF-8 invalide");
            if (codeCaractère < 65536) résultat.append((char)codeCaractère);
            else { codeCaractère -= 65536; résultat.append((char)(0xd800 | codeCaractère >> 10)); résultat.append((char)(0xdc00 | codeCaractère & 1023)); }
        }
        return résultat.toString();
    }
}
