// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface kannBerechnen { int Wert(); }
class hintergrundWert { static int vorbereiten = 7; int Zahl; String Name; hintergrundWert(int Zahl) { this.Zahl = Zahl; Name = "hintergrundWert"; } int Wert() { return Zahl; } }
class verzweigungWert extends hintergrundWert implements kannBerechnen { verzweigungWert(int Zahl) { super(Zahl); Name = "verzweigungWert"; } public int Wert() { return Zahl * vorbereiten; } }
public class objektePrüfung {
    static int anfänglichStatuswert = hintergrundWert.vorbereiten + 2;
    static int verzweigung(int Zahl) { switch (Zahl) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int dünnbesetztWert(int Zahl) { switch (Zahl) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] argumente) {
        verzweigungWert zweiterOperand = new verzweigungWert(6); hintergrundWert dritterOperand = zweiterOperand; kannBerechnen vierterOperand = zweiterOperand;
        System.out.println(anfänglichStatuswert + ":" + zweiterOperand.Name + ":" + dritterOperand.Wert() + ":" + vierterOperand.Wert());
        System.out.println((dritterOperand instanceof verzweigungWert) + ":" + (dritterOperand instanceof kannBerechnen) + ":" + verzweigung(2) + ":" + dünnbesetztWert(100));
        Object[] datenfeldWert = new Object[3]; datenfeldWert[0] = zweiterOperand; datenfeldWert[1] = "한글😀"; System.gc();
        System.out.println(((verzweigungWert)datenfeldWert[0]).Wert()); System.out.println((String)datenfeldWert[1]);
        int[] anzahlListe = {1, 2, 3, 4}; System.arraycopy(anzahlListe, 0, anzahlListe, 1, 3); System.out.println(anzahlListe[3]);
        byte[] byteWert = new byte[1]; byteWert[0] = (byte)255; char[] Zeichen = {'한'}; short[] istKurz = {(short)65535}; boolean[] wahrheitswertWert = {true};
        System.out.println(byteWert[0] + ":" + Zeichen[0] + ":" + istKurz[0] + ":" + wahrheitswertWert[0]);
    }
}
