// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int falha_VALOR() { throw new IllegalStateException("작업 중 exceção"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] inválido_RC = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("MATRIZ_VALOR CONVERTER_VALOR 검사"); }
        Object[] SMS_Lista = new String[2];
        try { SMS_Lista[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("MATRIZ_VALOR TIPO_VALOR 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Lista, 0, 2); } catch (ArrayStoreException e) { System.out.println("copiar_VALOR TIPO_VALOR 검사"); }
        System.out.println((String)SMS_Lista[0]);
        try { "texto".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 recortar"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object bloquear_VALOR = new Object(); try { synchronized (bloquear_VALOR) { falha_VALOR(); } } catch (IllegalStateException e) { System.out.println("bloquear_VALOR exceção"); }
        synchronized (bloquear_VALOR) { System.out.println("bloquear_VALOR 회수"); }
        byte[] dados = {0, (byte)128, (byte)255, 10};
        FileOutputStream saídaTexto = new FileOutputStream("byte_VALOR.bin"); saídaTexto.write(dados); saídaTexto.flush(); saídaTexto.close();
        FileInputStream entrada_VALOR = new FileInputStream("byte_VALOR.bin"); byte[] leitura_RC = new byte[8];
        System.out.println(entrada_VALOR.read(leitura_RC, 2, 4)); System.out.println(leitura_RC[3] + ":" + leitura_RC[4]);
        System.out.println(entrada_VALOR.read(leitura_RC)); System.out.println(entrada_VALOR.read(leitura_RC, 0, 0)); entrada_VALOR.close();
        try { entrada_VALOR.read(); } catch (IOException e) { System.out.println("닫힌 ficheiro"); }
    }
}
