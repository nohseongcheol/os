// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;

/** 전문(電文)·சேனல்_உள்ளீடு(通路): 경계를 가진 UDP 자료를 주고받는 முடிவுப்_புள்ளி. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int முனைய_எண்) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { 표준종단 = 통신.திற(முனைய_எண்);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public static 전문통로 திற(int முனைய_எண்) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return new 전문통로(முனைய_எண்);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public void அனுப்பு(String முகவரி, int முனைய_எண், String தரவு) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { 통신.அனுப்பு(표준종단, முகவரி, முனைய_எண், தரவு);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public String 받기() throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public void 대기시간(int 밀리초) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public int முனைய_எண்() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void மூடு() { 통신.மூடு(표준종단); }
}
