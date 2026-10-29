// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface puedeCalcular { int valor(); }
class valorFondo { static int preparar = 7; int númeroValor; String nombre; valorFondo(int númeroValor) { this.númeroValor = númeroValor; nombre = "valorFondo"; } int valor() { return númeroValor; } }
class valorRama extends valorFondo implements puedeCalcular { valorRama(int númeroValor) { super(númeroValor); nombre = "valorRama"; } public int valor() { return númeroValor * preparar; } }
public class pruebaObjetos {
    static int estadoValorInicialValor = valorFondo.preparar + 2;
    static int rama(int númeroValor) { switch (númeroValor) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int valorDisperso(int númeroValor) { switch (númeroValor) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] argumentos) {
        valorRama operandoSegundo = new valorRama(6); valorFondo operandoTercero = operandoSegundo; puedeCalcular operandoCuarto = operandoSegundo;
        System.out.println(estadoValorInicialValor + ":" + operandoSegundo.nombre + ":" + operandoTercero.valor() + ":" + operandoCuarto.valor());
        System.out.println((operandoTercero instanceof valorRama) + ":" + (operandoTercero instanceof puedeCalcular) + ":" + rama(2) + ":" + valorDisperso(100));
        Object[] valorArreglo = new Object[3]; valorArreglo[0] = operandoSegundo; valorArreglo[1] = "한글😀"; System.gc();
        System.out.println(((valorRama)valorArreglo[0]).valor()); System.out.println((String)valorArreglo[1]);
        int[] listaNúmeroElementos = {1, 2, 3, 4}; System.arraycopy(listaNúmeroElementos, 0, listaNúmeroElementos, 1, 3); System.out.println(listaNúmeroElementos[3]);
        byte[] valorByte = new byte[1]; valorByte[0] = (byte)255; char[] Caracteres = {'한'}; short[] esCorto = {(short)65535}; boolean[] valorBooleano = {true};
        System.out.println(valorByte[0] + ":" + Caracteres[0] + ":" + esCorto[0] + ":" + valorBooleano[0]);
    }
}
