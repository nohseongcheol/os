// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALORE(); }
class sfondo_VALORE { static int Prepara = 7; int numero; String Nome; sfondo_VALORE(int numero) { this.numero = numero; Nome = "sfondo_VALORE"; } int VALORE() { return numero; } }
class ramo_VALORE extends sfondo_VALORE implements 계산가능 { ramo_VALORE(int numero) { super(numero); Nome = "ramo_VALORE"; } public int VALORE() { return numero * Prepara; } }
public class 객체시험 {
    static int stato_iniziale = sfondo_VALORE.Prepara + 2;
    static int ramo(int numero) { switch (numero) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int numero) { switch (numero) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] argomenti) {
        ramo_VALORE SECONDO_operando = new ramo_VALORE(6); sfondo_VALORE 다 = SECONDO_operando; 계산가능 라 = SECONDO_operando;
        System.out.println(stato_iniziale + ":" + SECONDO_operando.Nome + ":" + 다.VALORE() + ":" + 라.VALORE());
        System.out.println((다 instanceof ramo_VALORE) + ":" + (다 instanceof 계산가능) + ":" + ramo(2) + ":" + 띄엄(100));
        Object[] array_VALORE = new Object[3]; array_VALORE[0] = SECONDO_operando; array_VALORE[1] = "한글😀"; System.gc();
        System.out.println(((ramo_VALORE)array_VALORE[0]).VALORE()); System.out.println((String)array_VALORE[1]);
        int[] CONTA_NUMERI_elenco = {1, 2, 3, 4}; System.arraycopy(CONTA_NUMERI_elenco, 0, CONTA_NUMERI_elenco, 1, 3); System.out.println(CONTA_NUMERI_elenco[3]);
        byte[] byte_VALORE = new byte[1]; byte_VALORE[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] booleano_VALORE = {true};
        System.out.println(byte_VALORE[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + booleano_VALORE[0]);
    }
}
