// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int неполадка_значення() { throw new IllegalStateException("작업 중 виняток"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] недійсний_КР = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("масив_значення перетворити_значення 검사"); }
        Object[] Текст_список = new String[2];
        try { Текст_список[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("масив_значення Тип_значення 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, Текст_список, 0, 2); } catch (ArrayStoreException e) { System.out.println("екземпляр_значення Тип_значення 검사"); }
        System.out.println((String)Текст_список[0]);
        try { "текст".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 кліп"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object блокувати_значення = new Object(); try { synchronized (блокувати_значення) { неполадка_значення(); } } catch (IllegalStateException e) { System.out.println("блокувати_значення виняток"); }
        synchronized (блокувати_значення) { System.out.println("блокувати_значення 회수"); }
        byte[] дані = {0, (byte)128, (byte)255, 10};
        FileOutputStream Вивід = new FileOutputStream("байт_значення.bin"); Вивід.write(дані); Вивід.flush(); Вивід.close();
        FileInputStream 입력 = new FileInputStream("байт_значення.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 файл"); }
    }
}
