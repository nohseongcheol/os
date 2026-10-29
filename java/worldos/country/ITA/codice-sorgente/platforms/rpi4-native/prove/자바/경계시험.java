// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int errore_VALORE() { throw new IllegalStateException("작업 중 eccezione"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] non_valida_KR = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("array_VALORE CONVERTI_VALORE 검사"); }
        Object[] SMS_elenco = new String[2];
        try { SMS_elenco[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("array_VALORE TIPO_VALORE 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_elenco, 0, 2); } catch (ArrayStoreException e) { System.out.println("copiare_VALORE TIPO_VALORE 검사"); }
        System.out.println((String)SMS_elenco[0]);
        try { "testo".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 ritagliare"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object blocco_VALORE_978a15a5 = new Object(); try { synchronized (blocco_VALORE_978a15a5) { errore_VALORE(); } } catch (IllegalStateException e) { System.out.println("blocco_VALORE_978a15a5 eccezione"); }
        synchronized (blocco_VALORE_978a15a5) { System.out.println("blocco_VALORE_978a15a5 회수"); }
        byte[] dati = {0, (byte)128, (byte)255, 10};
        FileOutputStream uscitaTesto = new FileOutputStream("byte_VALORE.bin"); uscitaTesto.write(dati); uscitaTesto.flush(); uscitaTesto.close();
        FileInputStream input_VALORE = new FileInputStream("byte_VALORE.bin"); byte[] 읽음 = new byte[8];
        System.out.println(input_VALORE.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(input_VALORE.read(읽음)); System.out.println(input_VALORE.read(읽음, 0, 0)); input_VALORE.close();
        try { input_VALORE.read(); } catch (IOException e) { System.out.println("닫힌 file"); }
    }
}
