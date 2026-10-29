// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALOR(); }
class Fondo_VALOR { static int 준비 = 7; int 수; String Nome; Fondo_VALOR(int 수) { this.수 = 수; Nome = "Fondo_VALOR"; } int VALOR() { return 수; } }
class ramificación_VALOR extends Fondo_VALOR implements 계산가능 { ramificación_VALOR(int 수) { super(수); Nome = "ramificación_VALOR"; } public int VALOR() { return 수 * 준비; } }
public class 객체시험 {
    static int 초기 = Fondo_VALOR.준비 + 2;
    static int ramificación(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Argumentos) {
        ramificación_VALOR 나 = new ramificación_VALOR(6); Fondo_VALOR 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Nome + ":" + 다.VALOR() + ":" + 라.VALOR());
        System.out.println((다 instanceof ramificación_VALOR) + ":" + (다 instanceof 계산가능) + ":" + ramificación(2) + ":" + 띄엄(100));
        Object[] MATRIZ_VALOR = new Object[3]; MATRIZ_VALOR[0] = 나; MATRIZ_VALOR[1] = "한글😀"; System.gc();
        System.out.println(((ramificación_VALOR)MATRIZ_VALOR[0]).VALOR()); System.out.println((String)MATRIZ_VALOR[1]);
        int[] CONTAR_Lista = {1, 2, 3, 4}; System.arraycopy(CONTAR_Lista, 0, CONTAR_Lista, 1, 3); System.out.println(CONTAR_Lista[3]);
        byte[] byte_VALOR = new byte[1]; byte_VALOR[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] booleano_VALOR = {true};
        System.out.println(byte_VALOR[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + booleano_VALOR[0]);
    }
}
