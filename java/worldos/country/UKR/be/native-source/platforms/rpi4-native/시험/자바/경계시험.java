// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int няўдача_значэнне() { throw new IllegalStateException("작업 중 выключэнне"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] 잘못 = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("масіў_значэнне 변환 검사"); }
        Object[] Тэкст_Спіс = new String[2];
        try { Тэкст_Спіс[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("масіў_значэнне друкаваць_значэнне 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, Тэкст_Спіс, 0, 2); } catch (ArrayStoreException e) { System.out.println("капіяваць_значэнне друкаваць_значэнне 검사"); }
        System.out.println((String)Тэкст_Спіс[0]);
        try { "Тэкст".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 кліп"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object 잠금 = new Object(); try { synchronized (잠금) { няўдача_значэнне(); } } catch (IllegalStateException e) { System.out.println("잠금 выключэнне"); }
        synchronized (잠금) { System.out.println("잠금 회수"); }
        byte[] дадзеныя = {0, (byte)128, (byte)255, 10};
        FileOutputStream Выхад = new FileOutputStream("байт_значэнне.bin"); Выхад.write(дадзеныя); Выхад.flush(); Выхад.close();
        FileInputStream 입력 = new FileInputStream("байт_значэнне.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 Файл"); }
    }
}
