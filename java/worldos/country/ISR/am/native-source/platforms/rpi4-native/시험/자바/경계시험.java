// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int ተስኖት_እሴት() { throw new IllegalStateException("작업 중 ልዩነት"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] ልክ_ያልኾነ_ልኬት = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("ድርድር_እሴት 변환 검사"); }
        Object[] ጽሁፍ_ዝርዝር = new String[2];
        try { ጽሁፍ_ዝርዝር[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("ድርድር_እሴት ተይብ_እሴት 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, ጽሁፍ_ዝርዝር, 0, 2); } catch (ArrayStoreException e) { System.out.println("ቅዳ_እሴት ተይብ_እሴት 검사"); }
        System.out.println((String)ጽሁፍ_ዝርዝር[0]);
        try { "ጽሁፍ".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 ቅንጥብ"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object 잠금 = new Object(); try { synchronized (잠금) { ተስኖት_እሴት(); } } catch (IllegalStateException e) { System.out.println("잠금 ልዩነት"); }
        synchronized (잠금) { System.out.println("잠금 회수"); }
        byte[] ውሂብ = {0, (byte)128, (byte)255, 10};
        FileOutputStream ውጤት = new FileOutputStream("ባይት_እሴት.bin"); ውጤት.write(ውሂብ); ውጤት.flush(); ውጤት.close();
        FileInputStream 입력 = new FileInputStream("ባይት_እሴት.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 ፋይል"); }
    }
}
