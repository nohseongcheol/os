// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static Ìsomọ́ Ṣi(String àdírẹ́ẹ̀sì, int 접속번호) throws 입출력예외 {
        try { return Ìsomọ́.Ṣi(àdírẹ́ẹ̀sì, 접속번호);
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.Ṣi(접속번호);
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public static Socket Darapọ̀(String àdírẹ́ẹ̀sì, int ojú_iye) throws 입출력예외 {
        try { return new Socket(àdírẹ́ẹ̀sì, ojú_iye);
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public static ServerSocket 듣기(int ojú_iye) throws 입출력예외 {
        try { return new ServerSocket(ojú_iye);
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public static Socket 받기(ServerSocket apèsè_iye) throws 입출력예외 {
        try { return apèsè_iye.accept();
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
}
