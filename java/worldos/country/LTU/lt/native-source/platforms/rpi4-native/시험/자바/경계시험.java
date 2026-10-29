// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int triktis_VALUE() { throw new IllegalStateException("작업 중 išimtis"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] neleistinas_KR = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("ARRAY_VALUE CONVERT_VALUE 검사"); }
        Object[] SMS_Sąrašas = new String[2];
        try { SMS_Sąrašas[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("ARRAY_VALUE TYPE_VALUE 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Sąrašas, 0, 2); } catch (ArrayStoreException e) { System.out.println("kopijuoti_VALUE TYPE_VALUE 검사"); }
        System.out.println((String)SMS_Sąrašas[0]);
        try { "Tekstas".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 klipas"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object užraktas_VALUE = new Object(); try { synchronized (užraktas_VALUE) { triktis_VALUE(); } } catch (IllegalStateException e) { System.out.println("užraktas_VALUE išimtis"); }
        synchronized (užraktas_VALUE) { System.out.println("užraktas_VALUE 회수"); }
        byte[] duomenys = {0, (byte)128, (byte)255, 10};
        FileOutputStream Išvestis = new FileOutputStream("baitas_VALUE.bin"); Išvestis.write(duomenys); Išvestis.flush(); Išvestis.close();
        FileInputStream 입력 = new FileInputStream("baitas_VALUE.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 Failas"); }
    }
}
