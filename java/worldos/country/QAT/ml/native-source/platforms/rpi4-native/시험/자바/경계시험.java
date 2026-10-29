// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int പരാജയം_മൂല്യം() { throw new IllegalStateException("작업 중 ഒഴിവാക്കൽ"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] അസാധുവായ_അളവ് = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("അരേ_മൂല്യം 변환 검사"); }
        Object[] ലിഖിതം_ലിസ്റ്റ് = new String[2];
        try { ലിഖിതം_ലിസ്റ്റ്[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("അരേ_മൂല്യം ടൈപ്പ്_ചെയ്യുക_മൂല്യം 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, ലിഖിതം_ലിസ്റ്റ്, 0, 2); } catch (ArrayStoreException e) { System.out.println("ദൃഷ്ടാന്തം_മൂല്യം ടൈപ്പ്_ചെയ്യുക_മൂല്യം 검사"); }
        System.out.println((String)ലിഖിതം_ലിസ്റ്റ്[0]);
        try { "പദാവലി".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 ക്ലിപ്പ്"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object ലോക്ക്_മൂല്യം = new Object(); try { synchronized (ലോക്ക്_മൂല്യം) { പരാജയം_മൂല്യം(); } } catch (IllegalStateException e) { System.out.println("ലോക്ക്_മൂല്യം ഒഴിവാക്കൽ"); }
        synchronized (ലോക്ക്_മൂല്യം) { System.out.println("ലോക്ക്_മൂല്യം 회수"); }
        byte[] ഡാറ്റാ = {0, (byte)128, (byte)255, 10};
        FileOutputStream ഫലം = new FileOutputStream("బైట్_മൂല്യം.bin"); ഫലം.write(ഡാറ്റാ); ഫലം.flush(); ഫലം.close();
        FileInputStream 입력 = new FileInputStream("బైట్_മൂല്യം.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 ഫയല്"); }
    }
}
