// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 Stream_मोल: 순서대로 들어오는 바이트를 읽는 चॅनल_प्रवेश. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int 읽기() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public int 읽기(byte[] डेटा) throws 입출력예외 {
        try { return 표준흐름.read(डेटा);
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public int 읽기(byte[] डेटा, int चलोवप, int लांबाय_मोल) throws 입출력예외 {
        try { return 표준흐름.read(डेटा, चलोवप, लांबाय_मोल);
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public void शेवट() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
}
