// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** అవుట్పుట్(出力)과 ధార_మూల్యం: 순서를 보존해 내보내는 바이트의 ఛానల్_ప్రవేశం. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void వ్రాయుము(int మూల్యం) throws మూ_ఫ_మినహాయింపు {
        try { 표준흐름.write(మూల్యం);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public void వ్రాయుము(byte[] డేటా) throws మూ_ఫ_మినహాయింపు {
        try { 표준흐름.write(డేటా);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public void వ్రాయుము(byte[] డేటా, int నడుపుము, int పొడవు_మూల్యం) throws మూ_ఫ_మినహాయింపు {
        try { 표준흐름.write(డేటా, నడుపుము, పొడవు_మూల్యం);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public void 내보내기() throws మూ_ఫ_మినహాయింపు {
        try { 표준흐름.flush();
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public void మూసివేయి() throws మూ_ఫ_మినహాయింపు {
        try { 표준흐름.close();
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
}
