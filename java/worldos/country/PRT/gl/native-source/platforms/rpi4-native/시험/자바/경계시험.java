// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int erro_VALOR() { throw new IllegalStateException("작업 중 excepción"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] non_válido_medida = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("MATRIZ_VALOR CONVERTER_VALOR 검사"); }
        Object[] SMS_Lista = new String[2];
        try { SMS_Lista[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("MATRIZ_VALOR TIPO_VALOR 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Lista, 0, 2); } catch (ArrayStoreException e) { System.out.println("copiar_VALOR TIPO_VALOR 검사"); }
        System.out.println((String)SMS_Lista[0]);
        try { "Texto".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 clip"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object bloquear_VALOR = new Object(); try { synchronized (bloquear_VALOR) { erro_VALOR(); } } catch (IllegalStateException e) { System.out.println("bloquear_VALOR excepción"); }
        synchronized (bloquear_VALOR) { System.out.println("bloquear_VALOR 회수"); }
        byte[] datos = {0, (byte)128, (byte)255, 10};
        FileOutputStream Saída = new FileOutputStream("byte_VALOR.bin"); Saída.write(datos); Saída.flush(); Saída.close();
        FileInputStream 입력 = new FileInputStream("byte_VALOR.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 Ficheiro"); }
    }
}
