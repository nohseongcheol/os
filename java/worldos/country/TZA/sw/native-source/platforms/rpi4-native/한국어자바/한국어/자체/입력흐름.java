// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 Stream_thamani: 순서대로 들어오는 바이트를 읽는 mkondo_ingizo. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int 읽기() throws I_T_vighairi {
        try { return 표준흐름.read();
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public int 읽기(byte[] data) throws I_T_vighairi {
        try { return 표준흐름.read(data);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public int 읽기(byte[] data, int endesha, int urefu_thamani) throws I_T_vighairi {
        try { return 표준흐름.read(data, endesha, urefu_thamani);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public void funga() throws I_T_vighairi {
        try { 표준흐름.close();
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
}
