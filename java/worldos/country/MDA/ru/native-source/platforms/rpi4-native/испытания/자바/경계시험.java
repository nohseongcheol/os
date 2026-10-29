// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int сбой_ЗНАЧЕН() { throw new IllegalStateException("작업 중 исключение"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] неверный_KR = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("МАССИВ_ЗНАЧЕН ПРЕОБР_ЗНАЧЕН 검사"); }
        Object[] SMS_Список = new String[2];
        try { SMS_Список[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("МАССИВ_ЗНАЧЕН ТИП_ЗНАЧЕН 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Список, 0, 2); } catch (ArrayStoreException e) { System.out.println("экземпляр_ЗНАЧЕН ТИП_ЗНАЧЕН 검사"); }
        System.out.println((String)SMS_Список[0]);
        try { "текст".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 клип"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object блокировка_ЗНАЧЕН = new Object(); try { synchronized (блокировка_ЗНАЧЕН) { сбой_ЗНАЧЕН(); } } catch (IllegalStateException e) { System.out.println("блокировка_ЗНАЧЕН исключение"); }
        synchronized (блокировка_ЗНАЧЕН) { System.out.println("блокировка_ЗНАЧЕН 회수"); }
        byte[] данные = {0, (byte)128, (byte)255, 10};
        FileOutputStream текстовыйВывод = new FileOutputStream("байт_ЗНАЧЕН.bin"); текстовыйВывод.write(данные); текстовыйВывод.flush(); текстовыйВывод.close();
        FileInputStream входные_данные_ЗНАЧЕН = new FileInputStream("байт_ЗНАЧЕН.bin"); byte[] чтение_KR = new byte[8];
        System.out.println(входные_данные_ЗНАЧЕН.read(чтение_KR, 2, 4)); System.out.println(чтение_KR[3] + ":" + чтение_KR[4]);
        System.out.println(входные_данные_ЗНАЧЕН.read(чтение_KR)); System.out.println(входные_данные_ЗНАЧЕН.read(чтение_KR, 0, 0)); входные_данные_ЗНАЧЕН.close();
        try { входные_данные_ЗНАЧЕН.read(); } catch (IOException e) { System.out.println("닫힌 файл"); }
    }
}
