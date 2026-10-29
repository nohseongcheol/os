// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static இணைப்பு திற(String முகவரி, int முனைய_எண்) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return இணைப்பு.திற(முகவரி, முனைய_எண்);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public static 수신창구 수신열기(int முனைய_எண்) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return 수신창구.திற(முனைய_எண்);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public static Socket இணைக்க(String முகவரி, int முணையம்_மதிப்பு) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return new Socket(முகவரி, முணையம்_மதிப்பு);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public static ServerSocket கவனி_முடிவுப்_புள்ளி(int முணையம்_மதிப்பு) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return new ServerSocket(முணையம்_மதிப்பு);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public static Socket 받기(ServerSocket சேவையகம்_மதிப்பு) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return சேவையகம்_மதிப்பு.accept();
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
}
