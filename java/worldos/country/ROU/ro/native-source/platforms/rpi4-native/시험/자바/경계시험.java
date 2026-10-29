// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int eroare_VALUE() { throw new IllegalStateException("작업 중 excepție"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] nul_KR = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("ARRAY_VALUE CONVERT_VALUE 검사"); }
        Object[] SMS_Listă = new String[2];
        try { SMS_Listă[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("ARRAY_VALUE Tip_VALUE 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Listă, 0, 2); } catch (ArrayStoreException e) { System.out.println("copia_VALUE Tip_VALUE 검사"); }
        System.out.println((String)SMS_Listă[0]);
        try { "글".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 clip"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object blocare_VALUE = new Object(); try { synchronized (blocare_VALUE) { eroare_VALUE(); } } catch (IllegalStateException e) { System.out.println("blocare_VALUE excepție"); }
        synchronized (blocare_VALUE) { System.out.println("blocare_VALUE 회수"); }
        byte[] date = {0, (byte)128, (byte)255, 10};
        FileOutputStream Rezultat = new FileOutputStream("byte_VALUE.bin"); Rezultat.write(date); Rezultat.flush(); Rezultat.close();
        FileInputStream 입력 = new FileInputStream("byte_VALUE.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 Fișier"); }
    }
}
