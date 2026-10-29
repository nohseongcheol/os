// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 ధార_మూల్యం: 순서대로 들어오는 바이트를 읽는 ఛానల్_ప్రవేశం. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int చదువు() throws మూ_ఫ_మినహాయింపు {
        try { return 표준흐름.read();
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public int చదువు(byte[] డేటా) throws మూ_ఫ_మినహాయింపు {
        try { return 표준흐름.read(డేటా);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public int చదువు(byte[] డేటా, int నడుపుము, int పొడవు_మూల్యం) throws మూ_ఫ_మినహాయింపు {
        try { return 표준흐름.read(డేటా, నడుపుము, పొడవు_మూల్యం);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public void మూసివేయి() throws మూ_ఫ_మినహాయింపు {
        try { 표준흐름.close();
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
}
