// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import español.propio.Caracteres;
import español.propio.Archivo;
import español.propio.listaEntradaElemento;
import español.propio.Diccionario;
import español.propio.Salida;
public class pruebaHangul {
    public static void main(String[] a) throws Exception {
        String Saludo = "안녕하세요 · 日本語 · العربية · 😀";
        Salida.escribirLínea(Caracteres.descifrarDatos(Caracteres.codificar(Saludo))); Salida.escribirNúmero(Caracteres.númeroElementosPuntoCódigo("한글😀"));
        Archivo.escribir("한글자료.txt", Saludo); Salida.escribirLínea(Archivo.leer("한글자료.txt"));
        listaEntradaElemento listaNombres = new listaEntradaElemento(); listaNombres.añadirValores("가람"); listaNombres.añadirValores("누리"); Salida.escribirLínea(listaNombres.leer(1));
        Diccionario valorSignificado = new Diccionario(); valorSignificado.ponerValor("가람", "강"); System.gc(); Salida.escribirLínea(valorSignificado.encontrarEntradaElemento("가람"));
        try { Caracteres.descifrarDatos(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Salida.escribirLínea("UTF-8 error rechazarValor"); }
        Salida.escribirLínea("español biblioteca esTerminado");
    }
}
