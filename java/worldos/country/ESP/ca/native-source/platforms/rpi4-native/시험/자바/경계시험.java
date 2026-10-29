// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int error_VALOR() { throw new IllegalStateException("작업 중 excepció"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] invàlid_mesura = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("MATRIU_VALOR CONVERT_VALOR 검사"); }
        Object[] SMS_Llista = new String[2];
        try { SMS_Llista[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("MATRIU_VALOR TIPUS_VALOR 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Llista, 0, 2); } catch (ArrayStoreException e) { System.out.println("copiar_VALOR TIPUS_VALOR 검사"); }
        System.out.println((String)SMS_Llista[0]);
        try { "글".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 clip"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object blocar_VALOR = new Object(); try { synchronized (blocar_VALOR) { error_VALOR(); } } catch (IllegalStateException e) { System.out.println("blocar_VALOR excepció"); }
        synchronized (blocar_VALOR) { System.out.println("blocar_VALOR 회수"); }
        byte[] dades = {0, (byte)128, (byte)255, 10};
        FileOutputStream Sortida = new FileOutputStream("byte_VALOR.bin"); Sortida.write(dades); Sortida.flush(); Sortida.close();
        FileInputStream 입력 = new FileInputStream("byte_VALOR.bin"); byte[] tancar_mesura = new byte[8];
        System.out.println(입력.read(tancar_mesura, 2, 4)); System.out.println(tancar_mesura[3] + ":" + tancar_mesura[4]);
        System.out.println(입력.read(tancar_mesura)); System.out.println(입력.read(tancar_mesura, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 Fitxer"); }
    }
}
