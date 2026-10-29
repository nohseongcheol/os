// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;

/** வெளியீட்டு_இடம்(出力)과 தொடரோடி_மதிப்பு: 순서를 보존해 내보내는 바이트의 சேனல்_உள்ளீடு. */
public final class வெளியீடு_ஓட்டம் {
    private final java.io.OutputStream 표준흐름;
    வெளியீடு_ஓட்டம்(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void எழுது(int மதிப்பு) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { 표준흐름.write(மதிப்பு);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public void எழுது(byte[] தரவு) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { 표준흐름.write(தரவு);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public void எழுது(byte[] தரவு, int செயல்படுத்துக, int நீளம்_மதிப்பு) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { 표준흐름.write(தரவு, செயல்படுத்துக, நீளம்_மதிப்பு);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public void 내보내기() throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { 표준흐름.flush();
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public void மூடு() throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { 표준흐름.close();
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
}
