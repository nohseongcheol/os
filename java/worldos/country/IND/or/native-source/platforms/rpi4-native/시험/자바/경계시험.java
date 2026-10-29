// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int ବିଫଳତା_ମୂଲ୍ୟ() { throw new IllegalStateException("작업 중 ବ୍ୟତିକ୍ରମ"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] ଅବୈଧ_ମାପ = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("ଆରେ_ମୂଲ୍ୟ 변환 검사"); }
        Object[] ପାଠ_ତାଲିକା = new String[2];
        try { ପାଠ_ତାଲିକା[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("ଆରେ_ମୂଲ୍ୟ ଟାଇପ୍_କରିବା_ମୂଲ୍ୟ 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, ପାଠ_ତାଲିକା, 0, 2); } catch (ArrayStoreException e) { System.out.println("କପି_ମୂଲ୍ୟ ଟାଇପ୍_କରିବା_ମୂଲ୍ୟ 검사"); }
        System.out.println((String)ପାଠ_ତାଲିକା[0]);
        try { "ପାଠ୍ଯ".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 କ୍ଲିପ୍"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object 잠금 = new Object(); try { synchronized (잠금) { ବିଫଳତା_ମୂଲ୍ୟ(); } } catch (IllegalStateException e) { System.out.println("잠금 ବ୍ୟତିକ୍ରମ"); }
        synchronized (잠금) { System.out.println("잠금 회수"); }
        byte[] ଡାଟା = {0, (byte)128, (byte)255, 10};
        FileOutputStream ନିର୍ଗମ = new FileOutputStream("ବାଇଟ୍_ମୂଲ୍ୟ.bin"); ନିର୍ଗମ.write(ଡାଟା); ନିର୍ଗମ.flush(); ନିର୍ଗମ.close();
        FileInputStream 입력 = new FileInputStream("ବାଇଟ୍_ମୂଲ୍ୟ.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 ଫାଇଲ"); }
    }
}
