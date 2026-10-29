// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;

/** 수신(受信)·முணையம்_மதிப்பு(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int முனைய_எண்) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { 표준창구 = new java.net.ServerSocket(முனைய_எண்);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public static 수신창구 திற(int முனைய_எண்) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return new 수신창구(முனைய_எண்);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public இணைப்பு 받기() throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return new இணைப்பு(표준창구.accept());
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public int முனைய_எண்() { return 표준창구.getLocalPort(); }
    public void 대기시간(int 밀리초) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void மூடு() throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { 표준창구.close();
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
}
