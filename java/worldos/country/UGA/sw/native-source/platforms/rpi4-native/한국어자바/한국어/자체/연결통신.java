// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static muunganisho unda(String anwani, int namba_ya_kituo) throws I_T_vighairi {
        try { return muunganisho.unda(anwani, namba_ya_kituo);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public static 수신창구 수신열기(int namba_ya_kituo) throws I_T_vighairi {
        try { return 수신창구.unda(namba_ya_kituo);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public static Socket UNGANISHA(String anwani, int kituo_thamani) throws I_T_vighairi {
        try { return new Socket(anwani, kituo_thamani);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public static ServerSocket 듣기(int kituo_thamani) throws I_T_vighairi {
        try { return new ServerSocket(kituo_thamani);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public static Socket 받기(ServerSocket seva_thamani) throws I_T_vighairi {
        try { return seva_thamani.accept();
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
}
