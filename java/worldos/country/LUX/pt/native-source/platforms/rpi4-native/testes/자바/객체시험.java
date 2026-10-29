// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALOR(); }
class Tela_de_fundo_VALOR { static int Preparar = 7; int número; String Nome; Tela_de_fundo_VALOR(int número) { this.número = número; Nome = "Tela_de_fundo_VALOR"; } int VALOR() { return número; } }
class branch_VALOR extends Tela_de_fundo_VALOR implements 계산가능 { branch_VALOR(int número) { super(número); Nome = "branch_VALOR"; } public int VALOR() { return número * Preparar; } }
public class 객체시험 {
    static int estado_inicial = Tela_de_fundo_VALOR.Preparar + 2;
    static int branch(int número) { switch (número) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int número) { switch (número) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] argumentos) {
        branch_VALOR SEGUNDO_operando = new branch_VALOR(6); Tela_de_fundo_VALOR 다 = SEGUNDO_operando; 계산가능 라 = SEGUNDO_operando;
        System.out.println(estado_inicial + ":" + SEGUNDO_operando.Nome + ":" + 다.VALOR() + ":" + 라.VALOR());
        System.out.println((다 instanceof branch_VALOR) + ":" + (다 instanceof 계산가능) + ":" + branch(2) + ":" + 띄엄(100));
        Object[] MATRIZ_VALOR = new Object[3]; MATRIZ_VALOR[0] = SEGUNDO_operando; MATRIZ_VALOR[1] = "한글😀"; System.gc();
        System.out.println(((branch_VALOR)MATRIZ_VALOR[0]).VALOR()); System.out.println((String)MATRIZ_VALOR[1]);
        int[] CONT_NÚM_Lista = {1, 2, 3, 4}; System.arraycopy(CONT_NÚM_Lista, 0, CONT_NÚM_Lista, 1, 3); System.out.println(CONT_NÚM_Lista[3]);
        byte[] byte_VALOR = new byte[1]; byte_VALOR[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] booliano_VALOR = {true};
        System.out.println(byte_VALOR[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + booliano_VALOR[0]);
    }
}
