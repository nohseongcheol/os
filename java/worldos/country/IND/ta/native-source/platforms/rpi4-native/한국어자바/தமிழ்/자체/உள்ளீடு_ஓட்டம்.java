// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;

/** 입력(入力)과 தொடரோடி_மதிப்பு: 순서대로 들어오는 바이트를 읽는 சேனல்_உள்ளீடு. */
public final class உள்ளீடு_ஓட்டம் {
    private final java.io.InputStream 표준흐름;
    உள்ளீடு_ஓட்டம்(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int படி() throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return 표준흐름.read();
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public int படி(byte[] தரவு) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return 표준흐름.read(தரவு);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public int படி(byte[] தரவு, int செயல்படுத்துக, int நீளம்_மதிப்பு) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return 표준흐름.read(தரவு, செயல்படுத்துக, நீளம்_மதிப்பு);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public void மூடு() throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { 표준흐름.close();
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
}
