// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class सीमा_चाचणी {
    static int बिघाड_मूल्य() { throw new IllegalStateException("पारपाडा_कार्य 중 अपवाद"); }
    public static void main(String[] a) throws Exception {
        Object साधे_ऍरे = new Object[2]; System.out.println(साधे_ऍरे instanceof String[]);
        try { String[] अवैध_मोजमाप = (String[])साधे_ऍरे; } catch (ClassCastException e) { System.out.println("ऍरे_मूल्य रूपांतरकरा_मूल्य पडताळण्या"); }
        Object[] मजकूर_यादी = new String[2];
        try { मजकूर_यादी[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("ऍरे_मूल्य टाइप_करा_मूल्य पडताळण्या"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, मजकूर_यादी, 0, 2); } catch (ArrayStoreException e) { System.out.println("इन्स्टन्स_मूल्य टाइप_करा_मूल्य पडताळण्या"); }
        System.out.println((String)मजकूर_यादी[0]);
        try { "पाठ्य".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("वर्ण क्लिप"); }
        Integer एक_मूल्य = Integer.valueOf(127), दोन_मूल्य = Integer.valueOf(127); System.out.println(एक_मूल्य == दोन_मूल्य);
        Object कुलूप_मूल्य = new Object(); try { synchronized (कुलूप_मूल्य) { बिघाड_मूल्य(); } } catch (IllegalStateException e) { System.out.println("कुलूप_मूल्य अपवाद"); }
        synchronized (कुलूप_मूल्य) { System.out.println("कुलूप_मूल्य 회수"); }
        byte[] डेटा = {0, (byte)128, (byte)255, 10};
        FileOutputStream आउटपुट = new FileOutputStream("बाइट_मूल्य.bin"); आउटपुट.write(डेटा); आउटपुट.flush(); आउटपुट.close();
        FileInputStream आदान_मूल्य = new FileInputStream("बाइट_मूल्य.bin"); byte[] मोजमाप_वाचा = new byte[8];
        System.out.println(आदान_मूल्य.read(मोजमाप_वाचा, 2, 4)); System.out.println(मोजमाप_वाचा[3] + ":" + मोजमाप_वाचा[4]);
        System.out.println(आदान_मूल्य.read(मोजमाप_वाचा)); System.out.println(आदान_मूल्य.read(मोजमाप_वाचा, 0, 0)); आदान_मूल्य.close();
        try { आदान_मूल्य.read(); } catch (IOException e) { System.out.println("닫힌 फाइल"); }
    }
}
