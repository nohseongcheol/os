// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int awaria_WARTOŚĆ() { throw new IllegalStateException("작업 중 wyjątek"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] nieważny_KR = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("TABLICA_WARTOŚĆ KONWERTUJ_WARTOŚĆ 검사"); }
        Object[] SMS_Lista = new String[2];
        try { SMS_Lista[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("TABLICA_WARTOŚĆ TYP_WARTOŚĆ 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Lista, 0, 2); } catch (ArrayStoreException e) { System.out.println("kopiować_WARTOŚĆ TYP_WARTOŚĆ 검사"); }
        System.out.println((String)SMS_Lista[0]);
        try { "tekst".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 obcinać"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object blokada_WARTOŚĆ = new Object(); try { synchronized (blokada_WARTOŚĆ) { awaria_WARTOŚĆ(); } } catch (IllegalStateException e) { System.out.println("blokada_WARTOŚĆ wyjątek"); }
        synchronized (blokada_WARTOŚĆ) { System.out.println("blokada_WARTOŚĆ 회수"); }
        byte[] dane = {0, (byte)128, (byte)255, 10};
        FileOutputStream pozycja_wyjścia = new FileOutputStream("bajt_WARTOŚĆ.bin"); pozycja_wyjścia.write(dane); pozycja_wyjścia.flush(); pozycja_wyjścia.close();
        FileInputStream wejście_WARTOŚĆ = new FileInputStream("bajt_WARTOŚĆ.bin"); byte[] 읽음 = new byte[8];
        System.out.println(wejście_WARTOŚĆ.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(wejście_WARTOŚĆ.read(읽음)); System.out.println(wejście_WARTOŚĆ.read(읽음, 0, 0)); wejście_WARTOŚĆ.close();
        try { wejście_WARTOŚĆ.read(); } catch (IOException e) { System.out.println("닫힌 nazwa_pliku"); }
    }
}
