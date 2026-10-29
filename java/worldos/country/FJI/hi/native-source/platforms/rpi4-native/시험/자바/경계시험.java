// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int विफलता_मान() { throw new IllegalStateException("작업 중 अपवाद"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] अमान्य_परिणाम = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("सरणी_मान रूपांतरित_करें_मान 검사"); }
        Object[] पाठ_सूची = new String[2];
        try { पाठ_सूची[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("सरणी_मान लिखें_मान 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, पाठ_सूची, 0, 2); } catch (ArrayStoreException e) { System.out.println("आवृत्ति_मान लिखें_मान 검사"); }
        System.out.println((String)पाठ_सूची[0]);
        try { "पाठ".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 क्लिप"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object लॉक_मान = new Object(); try { synchronized (लॉक_मान) { विफलता_मान(); } } catch (IllegalStateException e) { System.out.println("लॉक_मान अपवाद"); }
        synchronized (लॉक_मान) { System.out.println("लॉक_मान 회수"); }
        byte[] आँकड़े = {0, (byte)128, (byte)255, 10};
        FileOutputStream निर्गम = new FileOutputStream("बाइट_मान.bin"); निर्गम.write(आँकड़े); निर्गम.flush(); निर्गम.close();
        FileInputStream 입력 = new FileInputStream("बाइट_मान.bin"); byte[] पढें_परिणाम = new byte[8];
        System.out.println(입력.read(पढें_परिणाम, 2, 4)); System.out.println(पढें_परिणाम[3] + ":" + पढें_परिणाम[4]);
        System.out.println(입력.read(पढें_परिणाम)); System.out.println(입력.read(पढें_परिणाम, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 संचिका"); }
    }
}
