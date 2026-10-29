// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static njikọ Mepee(String àdreèsì, int 접속번호) throws 입출력예외 {
        try { return njikọ.Mepee(àdreèsì, 접속번호);
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.Mepee(접속번호);
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public static Socket Banye(String àdreèsì, int pọọt_valuu) throws 입출력예외 {
        try { return new Socket(àdreèsì, pọọt_valuu);
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public static ServerSocket 듣기(int pọọt_valuu) throws 입출력예외 {
        try { return new ServerSocket(pọọt_valuu);
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public static Socket 받기(ServerSocket savà_valuu) throws 입출력예외 {
        try { return savà_valuu.accept();
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
}
