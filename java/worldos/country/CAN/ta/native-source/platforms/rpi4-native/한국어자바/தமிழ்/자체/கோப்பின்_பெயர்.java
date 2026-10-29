// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 பயனர் 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class கோப்பின்_பெயர் {
    private கோப்பின்_பெயர்() {}
    public static byte[] 바이트읽기(String பெயர்) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try {
        FileInputStream தொடரோடி_மதிப்பு = new FileInputStream(பெயர்);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, மதிப்பு;
            while ((மதிப்பு = தொடரோடி_மதிப்பு.read()) != -1) { if (수 == 임시.length) throw new உள்ளீடு_வெளியீடு_விதிவிலக்கு("கோப்பின்_பெயர் அளவு 제한"); 임시[수++] = (byte)மதிப்பு; }
            byte[] அளவிடக்கூடியது = new byte[수]; System.arraycopy(임시, 0, அளவிடக்கூடியது, 0, 수); return அளவிடக்கூடியது;
        } finally { தொடரோடி_மதிப்பு.close(); }
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public static void எழுது_பைட்_மதிப்பு(String பெயர், byte[] உள்ளடக்கம்_மதிப்பு) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try {
        FileOutputStream தொடரோடி_மதிப்பு = new FileOutputStream(பெயர்);
        try { for (int சுழற்சி_அடைவு = 0; சுழற்சி_அடைவு < உள்ளடக்கம்_மதிப்பு.length; சுழற்சி_அடைவு++) தொடரோடி_மதிப்பு.write(உள்ளடக்கம்_மதிப்பு[சுழற்சி_அடைவு] & 255); } finally { தொடரோடி_மதிப்பு.close(); }
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public static String படி(String பெயர்) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return 문자.குறிநீக்கு_தரவு(바이트읽기(பெயர்));
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public static void எழுது(String பெயர், String உள்ளடக்கம்_மதிப்பு) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { எழுது_பைட்_மதிப்பு(பெயர், 문자.부호화(உள்ளடக்கம்_மதிப்பு));
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
}
