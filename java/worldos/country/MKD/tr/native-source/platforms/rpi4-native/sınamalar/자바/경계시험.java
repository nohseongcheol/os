// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int hata_değer() { throw new IllegalStateException("작업 중 özel_durum"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] geçersiz_KR = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("DİZİ_değer ÇEVİR_değer 검사"); }
        Object[] SMS_Liste = new String[2];
        try { SMS_Liste[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("DİZİ_değer TÜR_değer 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Liste, 0, 2); } catch (ArrayStoreException e) { System.out.println("örnek_değer TÜR_değer 검사"); }
        System.out.println((String)SMS_Liste[0]);
        try { "metin".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 klip"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object kilit_değer = new Object(); try { synchronized (kilit_değer) { hata_değer(); } } catch (IllegalStateException e) { System.out.println("kilit_değer özel_durum"); }
        synchronized (kilit_değer) { System.out.println("kilit_değer 회수"); }
        byte[] veri = {0, (byte)128, (byte)255, 10};
        FileOutputStream metinÇıktısı = new FileOutputStream("bayt_değer.bin"); metinÇıktısı.write(veri); metinÇıktısı.flush(); metinÇıktısı.close();
        FileInputStream artış_değer = new FileInputStream("bayt_değer.bin"); byte[] 읽음 = new byte[8];
        System.out.println(artış_değer.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(artış_değer.read(읽음)); System.out.println(artış_değer.read(읽음, 0, 0)); artış_değer.close();
        try { artış_değer.read(); } catch (IOException e) { System.out.println("닫힌 dosya"); }
    }
}
