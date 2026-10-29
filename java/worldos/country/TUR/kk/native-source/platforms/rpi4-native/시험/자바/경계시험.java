// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int қате_мән() { throw new IllegalStateException("작업 중 ерекшелік"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] дұрыс_емес_өлшем = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("массив_мән Түрлендіру_мән 검사"); }
        Object[] Мәтін_Тізім = new String[2];
        try { Мәтін_Тізім[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("массив_мән Түрі_мән 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, Мәтін_Тізім, 0, 2); } catch (ArrayStoreException e) { System.out.println("дана_мән Түрі_мән 검사"); }
        System.out.println((String)Мәтін_Тізім[0]);
        try { "Мәтін".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 клип"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object блоктау_мән = new Object(); try { synchronized (блоктау_мән) { қате_мән(); } } catch (IllegalStateException e) { System.out.println("блоктау_мән ерекшелік"); }
        synchronized (блоктау_мән) { System.out.println("блоктау_мән 회수"); }
        byte[] деректер = {0, (byte)128, (byte)255, 10};
        FileOutputStream Шығысы = new FileOutputStream("байт_мән.bin"); Шығысы.write(деректер); Шығысы.flush(); Шығысы.close();
        FileInputStream 입력 = new FileInputStream("байт_мән.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 Файл"); }
    }
}
