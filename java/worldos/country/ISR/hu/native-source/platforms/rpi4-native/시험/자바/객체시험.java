// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int ÉRTÉK(); }
class Háttér_ÉRTÉK { static int Előkészítés = 7; int szám; String Név; Háttér_ÉRTÉK(int szám) { this.szám = szám; Név = "Háttér_ÉRTÉK"; } int ÉRTÉK() { return szám; } }
class ág_ÉRTÉK extends Háttér_ÉRTÉK implements 계산가능 { ág_ÉRTÉK(int szám) { super(szám); Név = "ág_ÉRTÉK"; } public int ÉRTÉK() { return szám * Előkészítés; } }
public class 객체시험 {
    static int kiinduló_állapot = Háttér_ÉRTÉK.Előkészítés + 2;
    static int ág(int szám) { switch (szám) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int szám) { switch (szám) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Argumentumok) {
        ág_ÉRTÉK MPERC_operandus = new ág_ÉRTÉK(6); Háttér_ÉRTÉK 다 = MPERC_operandus; 계산가능 라 = MPERC_operandus;
        System.out.println(kiinduló_állapot + ":" + MPERC_operandus.Név + ":" + 다.ÉRTÉK() + ":" + 라.ÉRTÉK());
        System.out.println((다 instanceof ág_ÉRTÉK) + ":" + (다 instanceof 계산가능) + ":" + ág(2) + ":" + 띄엄(100));
        Object[] TÖMB_ÉRTÉK = new Object[3]; TÖMB_ÉRTÉK[0] = MPERC_operandus; TÖMB_ÉRTÉK[1] = "한글😀"; System.gc();
        System.out.println(((ág_ÉRTÉK)TÖMB_ÉRTÉK[0]).ÉRTÉK()); System.out.println((String)TÖMB_ÉRTÉK[1]);
        int[] DARAB_Lista = {1, 2, 3, 4}; System.arraycopy(DARAB_Lista, 0, DARAB_Lista, 1, 3); System.out.println(DARAB_Lista[3]);
        byte[] bájt_ÉRTÉK = new byte[1]; bájt_ÉRTÉK[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] logikai_ÉRTÉK = {true};
        System.out.println(bájt_ÉRTÉK[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + logikai_ÉRTÉK[0]);
    }
}
