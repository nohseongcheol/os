// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class testBoundaries {
    static int failureValue() { throw new IllegalStateException("performTask 중 exception"); }
    public static void main(String[] a) throws Exception {
        Object plainArray = new Object[2]; System.out.println(plainArray instanceof String[]);
        try { String[] invalidResult = (String[])plainArray; } catch (ClassCastException e) { System.out.println("arrayValue convertValue Checks"); }
        Object[] textList = new String[2];
        try { textList[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("arrayValue typeValue Checks"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, textList, 0, 2); } catch (ArrayStoreException e) { System.out.println("copyValue typeValue Checks"); }
        System.out.println((String)textList[0]);
        try { "text".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("Characters clip"); }
        Integer oneValue = Integer.valueOf(127), twoValue = Integer.valueOf(127); System.out.println(oneValue == twoValue);
        Object lockValue = new Object(); try { synchronized (lockValue) { failureValue(); } } catch (IllegalStateException e) { System.out.println("lockValue exception"); }
        synchronized (lockValue) { System.out.println("lockValue 회수"); }
        byte[] data = {0, (byte)128, (byte)255, 10};
        FileOutputStream Output = new FileOutputStream("byteValue.bin"); Output.write(data); Output.flush(); Output.close();
        FileInputStream inputValue = new FileInputStream("byteValue.bin"); byte[] readResult = new byte[8];
        System.out.println(inputValue.read(readResult, 2, 4)); System.out.println(readResult[3] + ":" + readResult[4]);
        System.out.println(inputValue.read(readResult)); System.out.println(inputValue.read(readResult, 0, 0)); inputValue.close();
        try { inputValue.read(); } catch (IOException e) { System.out.println("닫힌 file"); }
    }
}
