// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int ARVO(); }
class Tausta_ARVO { static int Valmistele = 7; int numero; String Nimi; Tausta_ARVO(int numero) { this.numero = numero; Nimi = "Tausta_ARVO"; } int ARVO() { return numero; } }
class haara_ARVO extends Tausta_ARVO implements 계산가능 { haara_ARVO(int numero) { super(numero); Nimi = "haara_ARVO"; } public int ARVO() { return numero * Valmistele; } }
public class 객체시험 {
    static int alkutila = Tausta_ARVO.Valmistele + 2;
    static int haara(int numero) { switch (numero) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int numero) { switch (numero) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] argumentit) {
        haara_ARVO SEKUNNIT_operandi = new haara_ARVO(6); Tausta_ARVO 다 = SEKUNNIT_operandi; 계산가능 라 = SEKUNNIT_operandi;
        System.out.println(alkutila + ":" + SEKUNNIT_operandi.Nimi + ":" + 다.ARVO() + ":" + 라.ARVO());
        System.out.println((다 instanceof haara_ARVO) + ":" + (다 instanceof 계산가능) + ":" + haara(2) + ":" + 띄엄(100));
        Object[] MATRIISI_ARVO = new Object[3]; MATRIISI_ARVO[0] = SEKUNNIT_operandi; MATRIISI_ARVO[1] = "한글😀"; System.gc();
        System.out.println(((haara_ARVO)MATRIISI_ARVO[0]).ARVO()); System.out.println((String)MATRIISI_ARVO[1]);
        int[] LASKE_luettelo = {1, 2, 3, 4}; System.arraycopy(LASKE_luettelo, 0, LASKE_luettelo, 1, 3); System.out.println(LASKE_luettelo[3]);
        byte[] tavu_ARVO = new byte[1]; tavu_ARVO[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] totuusarvo_ARVO = {true};
        System.out.println(tavu_ARVO[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + totuusarvo_ARVO[0]);
    }
}
