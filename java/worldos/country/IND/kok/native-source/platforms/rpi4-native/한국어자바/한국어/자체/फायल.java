// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 उपेगकर्तो 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class फायल {
    private फायल() {}
    public static byte[] 바이트읽기(String नांव) throws 입출력예외 {
        try {
        FileInputStream Stream_मोल = new FileInputStream(नांव);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, मोल;
            while ((मोल = Stream_मोल.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("फायल आवाठ 제한"); 임시[수++] = (byte)मोल; }
            byte[] मेजप = new byte[수]; System.arraycopy(임시, 0, मेजप, 0, 수); return मेजप;
        } finally { Stream_मोल.close(); }
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public static void बरोवचें_बायट_मोल(String नांव, byte[] अनुक्रमणिका_मोल) throws 입출력예외 {
        try {
        FileOutputStream Stream_मोल = new FileOutputStream(नांव);
        try { for (int लूप_INDEX = 0; लूप_INDEX < अनुक्रमणिका_मोल.length; लूप_INDEX++) Stream_मोल.write(अनुक्रमणिका_मोल[लूप_INDEX] & 255); } finally { Stream_मोल.close(); }
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public static String 읽기(String नांव) throws 입출력예외 {
        try { return 문자.डिक्रिप्ट_डेटा(바이트읽기(नांव));
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public static void बरोवचें(String नांव, String अनुक्रमणिका_मोल) throws 입출력예외 {
        try { बरोवचें_बायट_मोल(नांव, 문자.부호화(अनुक्रमणिका_मोल));
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
}
