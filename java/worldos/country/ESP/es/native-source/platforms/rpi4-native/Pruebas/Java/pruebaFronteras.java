// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class pruebaFronteras {
    static int valorFallo() { throw new IllegalStateException("Tarea 중 excepción"); }
    public static void main(String[] a) throws Exception {
        Object arregloTextoClaro = new Object[2]; System.out.println(arregloTextoClaro instanceof String[]);
        try { String[] resultadoInválido = (String[])arregloTextoClaro; } catch (ClassCastException e) { System.out.println("valorArreglo convertirValor Comprobaciones"); }
        Object[] listaTexto = new String[2];
        try { listaTexto[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("valorArreglo valorTipo Comprobaciones"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, listaTexto, 0, 2); } catch (ArrayStoreException e) { System.out.println("copiarValor valorTipo Comprobaciones"); }
        System.out.println((String)listaTexto[0]);
        try { "texto".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("Caracteres recortar"); }
        Integer valorUno = Integer.valueOf(127), valorDos = Integer.valueOf(127); System.out.println(valorUno == valorDos);
        Object valorCerrojo = new Object(); try { synchronized (valorCerrojo) { valorFallo(); } } catch (IllegalStateException e) { System.out.println("valorCerrojo excepción"); }
        synchronized (valorCerrojo) { System.out.println("valorCerrojo 회수"); }
        byte[] Datos = {0, (byte)128, (byte)255, 10};
        FileOutputStream Salida = new FileOutputStream("valorByte.bin"); Salida.write(Datos); Salida.flush(); Salida.close();
        FileInputStream valorEntrada = new FileInputStream("valorByte.bin"); byte[] leerResultado = new byte[8];
        System.out.println(valorEntrada.read(leerResultado, 2, 4)); System.out.println(leerResultado[3] + ":" + leerResultado[4]);
        System.out.println(valorEntrada.read(leerResultado)); System.out.println(valorEntrada.read(leerResultado, 0, 0)); valorEntrada.close();
        try { valorEntrada.read(); } catch (IOException e) { System.out.println("닫힌 Archivo"); }
    }
}
