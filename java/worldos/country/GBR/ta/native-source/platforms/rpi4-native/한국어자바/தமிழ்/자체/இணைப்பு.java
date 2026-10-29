// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;

/** இணைக்க(連結)·சேனல்_உள்ளீடு(通路): 상대와 이어진 TCP பைட்_மதிப்பு 흐름의 முடிவுப்_புள்ளி. */
public final class இணைப்பு {
    private final java.net.Socket 표준연결;
    இணைப்பு(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static இணைப்பு திற(String முகவரி, int முனைய_எண்) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try {
            return new இணைப்பு(new java.net.Socket(முகவரி, முனைய_எண்));
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public உள்ளீடு_ஓட்டம் 입력() throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return new உள்ளீடு_ஓட்டம்(표준연결.getInputStream());
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public வெளியீடு_ஓட்டம் வெளியீட்டு_இடம்() throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return new வெளியீடு_ஓட்டம்(표준연결.getOutputStream());
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public void 대기시간(int 밀리초) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public int முனைய_எண்() { return 표준연결.getPort(); }
    public int தனி_முனைய_எண்() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void மூடு() throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { 표준연결.close();
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
}
