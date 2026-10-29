// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALOR(); }
class Fons_VALOR { static int Prepara = 7; int 수; String Nom; Fons_VALOR(int 수) { this.수 = 수; Nom = "Fons_VALOR"; } int VALOR() { return 수; } }
class branca_VALOR extends Fons_VALOR implements 계산가능 { branca_VALOR(int 수) { super(수); Nom = "branca_VALOR"; } public int VALOR() { return 수 * Prepara; } }
public class 객체시험 {
    static int 초기 = Fons_VALOR.Prepara + 2;
    static int branca(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        branca_VALOR 나 = new branca_VALOR(6); Fons_VALOR 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Nom + ":" + 다.VALOR() + ":" + 라.VALOR());
        System.out.println((다 instanceof branca_VALOR) + ":" + (다 instanceof 계산가능) + ":" + branca(2) + ":" + 띄엄(100));
        Object[] MATRIU_VALOR = new Object[3]; MATRIU_VALOR[0] = 나; MATRIU_VALOR[1] = "한글😀"; System.gc();
        System.out.println(((branca_VALOR)MATRIU_VALOR[0]).VALOR()); System.out.println((String)MATRIU_VALOR[1]);
        int[] COMPT_Llista = {1, 2, 3, 4}; System.arraycopy(COMPT_Llista, 0, COMPT_Llista, 1, 3); System.out.println(COMPT_Llista[3]);
        byte[] byte_VALOR = new byte[1]; byte_VALOR[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] booleà_VALOR = {true};
        System.out.println(byte_VALOR[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + booleà_VALOR[0]);
    }
}
