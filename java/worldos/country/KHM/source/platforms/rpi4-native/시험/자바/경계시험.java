// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int បរាជ័យ_តំលៃ() { throw new IllegalStateException("작업 중 ការលើកលែង"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] មិនត្រឹមត្រូវ_ការវាស់វែង = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("អារេ_តំលៃ 변환 검사"); }
        Object[] អត្ថបទ_បញ្ជី = new String[2];
        try { អត្ថបទ_បញ្ជី[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("អារេ_តំលៃ វាយបញ្ចូល_តំលៃ 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, អត្ថបទ_បញ្ជី, 0, 2); } catch (ArrayStoreException e) { System.out.println("ចំលង_តំលៃ វាយបញ្ចូល_តំលៃ 검사"); }
        System.out.println((String)អត្ថបទ_បញ្ជី[0]);
        try { "អត្ថបទ".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 មេឌៀខ្លីៗ"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object 잠금 = new Object(); try { synchronized (잠금) { បរាជ័យ_តំលៃ(); } } catch (IllegalStateException e) { System.out.println("잠금 ការលើកលែង"); }
        synchronized (잠금) { System.out.println("잠금 회수"); }
        byte[] ទិន្នន័យ = {0, (byte)128, (byte)255, 10};
        FileOutputStream លទ្ធផល = new FileOutputStream("បៃ_តំលៃ.bin"); លទ្ធផល.write(ទិន្នន័យ); លទ្ធផល.flush(); លទ្ធផល.close();
        FileInputStream 입력 = new FileInputStream("បៃ_តំលៃ.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 ឯកសារ"); }
    }
}
