// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int 실패() { throw new IllegalStateException("작업 중 예외"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] 잘못 = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("배열 변환 검사"); }
        Object[] 글들 = new String[2];
        try { 글들[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("배열 형 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, 글들, 0, 2); } catch (ArrayStoreException e) { System.out.println("복사 형 검사"); }
        System.out.println((String)글들[0]);
        try { "Текст".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 범위"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object 잠금 = new Object(); try { synchronized (잠금) { 실패(); } } catch (IllegalStateException e) { System.out.println("잠금 예외"); }
        synchronized (잠금) { System.out.println("잠금 회수"); }
        byte[] 자료 = {0, (byte)128, (byte)255, 10};
        FileOutputStream Излаз = new FileOutputStream("바이트.bin"); Излаз.write(자료); Излаз.flush(); Излаз.close();
        FileInputStream 입력 = new FileInputStream("바이트.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 Датотека"); }
    }
}
