// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Verwaltet Beschnitt, Streifenzusammensetzung und Zeigerhintergrund. Tatsächliche Bildspeicherzugriffe übernimmt der Boardcode. */
public final class BildpufferZusammensetzer {
    static int breiteWert, höheWert, istZusammensetzend, linksGrenzstelleWert, obererGrenzstelle, rechtsGrenzstelleWert, untererGrenzstelleWert;
    static int zeigerWaagerechteKoordinate, zeigerSenkrechteKoordinate, zeigerForm;
    static int zählerNiedrig, zählerHoch;
    static int[] zusammengesetztBildpunkte = new int[32 * 1920];
    static int[] zeigerHintergrund = new int[21 * 21];
    static int[] beschnittenGrenzen = new int[4];
    public static void vorbereiten(int breiteSpannweite, int Länge) {
        breiteWert = breiteSpannweite; höheWert = Länge; istZusammensetzend = 0; zeigerForm = 0;
        zählerNiedrig = 0; zählerHoch = 0;
    }
    public static int breiteHolen() { return breiteWert; }
    public static int höheHolen() { return höheWert; }
    public static int zählerNiedrigHolen() { return zählerNiedrig; }
    public static int zählerHochHolen() { return zählerHoch; }
    public static int beschneidenWert(int ordnungszahlIndex) { return beschnittenGrenzen[ordnungszahlIndex]; }
    static int positivLängeHinzufügen(int wertStarten, int Länge) {
        if (wertStarten > 2147483647 - Länge) return 2147483647;
        return wertStarten + Länge;
    }
    public static int beschneiden(int waagerechtPosition, int senkrechtPosition, int breiteSpannweite, int Länge) {
        if (breiteWert == 0 || breiteSpannweite <= 0 || Länge <= 0) return 0;
        int rechts = positivLängeHinzufügen(waagerechtPosition, breiteSpannweite), untererSeiteRand = positivLängeHinzufügen(senkrechtPosition, Länge);
        int linksSeiteRand = istZusammensetzend != 0 ? linksGrenzstelleWert : 0, obererSeiteRand = istZusammensetzend != 0 ? obererGrenzstelle : 0;
        int höchstwertWaagerechtPosition = istZusammensetzend != 0 ? rechtsGrenzstelleWert : breiteWert, höchstwertSenkrechtPosition = istZusammensetzend != 0 ? untererGrenzstelleWert : höheWert;
        if (waagerechtPosition < linksSeiteRand) waagerechtPosition = linksSeiteRand;
        if (senkrechtPosition < obererSeiteRand) senkrechtPosition = obererSeiteRand;
        if (rechts > höchstwertWaagerechtPosition) rechts = höchstwertWaagerechtPosition;
        if (untererSeiteRand > höchstwertSenkrechtPosition) untererSeiteRand = höchstwertSenkrechtPosition;
        if (rechts <= waagerechtPosition || untererSeiteRand <= senkrechtPosition) return 0;
        beschnittenGrenzen[0] = waagerechtPosition; beschnittenGrenzen[1] = senkrechtPosition;
        beschnittenGrenzen[2] = rechts - waagerechtPosition; beschnittenGrenzen[3] = untererSeiteRand - senkrechtPosition;
        return 1;
    }
    public static int ausführenVorgang(int waagerechtPosition, int senkrechtPosition, int breiteSpannweite, int Länge) {
        if (istZusammensetzend != 0 || Länge > 32 || beschneiden(waagerechtPosition, senkrechtPosition, breiteSpannweite, Länge) == 0) return 0;
        linksGrenzstelleWert = beschnittenGrenzen[0]; obererGrenzstelle = beschnittenGrenzen[1];
        rechtsGrenzstelleWert = linksGrenzstelleWert + beschnittenGrenzen[2]; untererGrenzstelleWert = obererGrenzstelle + beschnittenGrenzen[3];
        istZusammensetzend = 1; return 1;
    }
    static boolean zeigerBit(int waagerechtPosition, int senkrechtPosition, int formWert) {
        if (formWert == 1) return waagerechtPosition >= 0 && waagerechtPosition <= senkrechtPosition / 2 && senkrechtPosition < 16;
        if (formWert == 3) waagerechtPosition = 20 - waagerechtPosition;
        int unterschiedWert = waagerechtPosition - senkrechtPosition; if (unterschiedWert < 0) unterschiedWert = -unterschiedWert;
        return (unterschiedWert <= 1 && waagerechtPosition >= 3 && waagerechtPosition <= 17) ||
            (waagerechtPosition >= 2 && waagerechtPosition <= 8 && senkrechtPosition >= 2 && senkrechtPosition <= 8 && (waagerechtPosition <= 3 || senkrechtPosition <= 3)) ||
            (waagerechtPosition >= 12 && waagerechtPosition <= 18 && senkrechtPosition >= 12 && senkrechtPosition <= 18 && (waagerechtPosition >= 17 || senkrechtPosition >= 17));
    }
    static int zeigerBildpunkt(int waagerechtPosition, int senkrechtPosition) {
        if (zeigerBit(waagerechtPosition, senkrechtPosition, zeigerForm)) return 2;
        for (int zeile = -1; zeile <= 1; zeile++) for (int platzEintrag = -1; platzEintrag <= 1; platzEintrag++)
            if (zeigerBit(waagerechtPosition + platzEintrag, senkrechtPosition + zeile, zeigerForm)) return 1;
        return 0;
    }
    static void darstellenBildpunkt(int waagerechtPosition, int senkrechtPosition, int farbeWert) {
        int platzEintrag = waagerechtPosition - zeigerWaagerechteKoordinate, zeile = senkrechtPosition - zeigerSenkrechteKoordinate;
        if (zeigerForm != 0 && platzEintrag >= 0 && zeile >= 0 && platzEintrag < 21 && zeile < 21) {
            zeigerHintergrund[zeile * 21 + platzEintrag] = farbeWert;
            int punktWert = zeigerBildpunkt(platzEintrag, zeile); if (punktWert != 0) farbeWert = punktWert == 2 ? 0xffffff : 0x101010;
        }
        if (Platine.darstellenBildpunktLesen(waagerechtPosition, senkrechtPosition) != farbeWert) {
            Platine.darstellenBildpunktSchreiben(waagerechtPosition, senkrechtPosition, farbeWert);
            zählerNiedrig++; if (zählerNiedrig == 0) zählerHoch++;
        }
    }
    public static void beenden() {
        if (istZusammensetzend == 0) return;
        for (int zeile = obererGrenzstelle; zeile < untererGrenzstelleWert; zeile++) for (int platzEintrag = linksGrenzstelleWert; platzEintrag < rechtsGrenzstelleWert; platzEintrag++)
            darstellenBildpunkt(platzEintrag, zeile, zusammengesetztBildpunkte[(zeile - obererGrenzstelle) * 1920 + platzEintrag]);
        istZusammensetzend = 0;
    }
    public static int bildpunkt(int waagerechtPosition, int senkrechtPosition, int farbeWert) {
        if (waagerechtPosition < 0 || senkrechtPosition < 0 || waagerechtPosition >= breiteWert || senkrechtPosition >= höheWert) return 0;
        if (istZusammensetzend != 0) {
            if (waagerechtPosition >= linksGrenzstelleWert && waagerechtPosition < rechtsGrenzstelleWert && senkrechtPosition >= obererGrenzstelle && senkrechtPosition < untererGrenzstelleWert)
                zusammengesetztBildpunkte[(senkrechtPosition - obererGrenzstelle) * 1920 + waagerechtPosition] = farbeWert;
        } else darstellenBildpunkt(waagerechtPosition, senkrechtPosition, farbeWert);
        return 0;
    }
    public static void rechteckFüllen(int waagerechtPosition, int senkrechtPosition, int breiteSpannweite, int Länge, int farbeWert) {
        if (beschneiden(waagerechtPosition, senkrechtPosition, breiteSpannweite, Länge) == 0) return;
        waagerechtPosition = beschnittenGrenzen[0]; senkrechtPosition = beschnittenGrenzen[1]; breiteSpannweite = beschnittenGrenzen[2]; Länge = beschnittenGrenzen[3];
        for (int zeile = senkrechtPosition; zeile < senkrechtPosition + Länge; zeile++) for (int platzEintrag = waagerechtPosition; platzEintrag < waagerechtPosition + breiteSpannweite; platzEintrag++) {
            if (istZusammensetzend != 0) zusammengesetztBildpunkte[(zeile - obererGrenzstelle) * 1920 + platzEintrag] = farbeWert;
            else darstellenBildpunkt(platzEintrag, zeile, farbeWert);
        }
    }
    public static void zeiger(int waagerechtPosition, int senkrechtPosition, int formWert) {
        if (breiteWert == 0) return;
        int neuWaagerechtPosition = waagerechtPosition - (formWert >= 2 ? 10 : 0), neuSenkrechtPosition = senkrechtPosition - (formWert >= 2 ? 10 : 0);
        if (zeigerForm == formWert && zeigerWaagerechteKoordinate == neuWaagerechtPosition && zeigerSenkrechteKoordinate == neuSenkrechtPosition) return;
        if (zeigerForm != 0) for (int zeile = 0; zeile < 21; zeile++) for (int platzEintrag = 0; platzEintrag < 21; platzEintrag++) {
            int ersterOperand = zeigerWaagerechteKoordinate + platzEintrag, dreiWert = zeigerSenkrechteKoordinate + zeile;
            if (ersterOperand >= 0 && dreiWert >= 0 && ersterOperand < breiteWert && dreiWert < höheWert) Platine.darstellenBildpunktSchreiben(ersterOperand, dreiWert, zeigerHintergrund[zeile * 21 + platzEintrag]);
        }
        zeigerForm = formWert; zeigerWaagerechteKoordinate = neuWaagerechtPosition; zeigerSenkrechteKoordinate = neuSenkrechtPosition;
        if (formWert != 0) for (int zeile = 0; zeile < 21; zeile++) for (int platzEintrag = 0; platzEintrag < 21; platzEintrag++) {
            int ersterOperand = zeigerWaagerechteKoordinate + platzEintrag, dreiWert = zeigerSenkrechteKoordinate + zeile;
            if (ersterOperand >= 0 && dreiWert >= 0 && ersterOperand < breiteWert && dreiWert < höheWert) {
                zeigerHintergrund[zeile * 21 + platzEintrag] = Platine.darstellenBildpunktLesen(ersterOperand, dreiWert);
                int punktWert = zeigerBildpunkt(platzEintrag, zeile); if (punktWert != 0) Platine.darstellenBildpunktSchreiben(ersterOperand, dreiWert, punktWert == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
