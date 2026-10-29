// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 aṣàmúlò 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fáìlì {
    private Fáìlì() {}
    public static byte[] 바이트읽기(String Orúkọ) throws 입출력예외 {
        try {
        FileInputStream Stream_iye = new FileInputStream(Orúkọ);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, iye;
            while ((iye = Stream_iye.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("Fáìlì Ìwọ̀n 제한"); 임시[수++] = (byte)iye; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { Stream_iye.close(); }
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public static void kọ_báìtì_iye(String Orúkọ, byte[] Àkóónú_iye) throws 입출력예외 {
        try {
        FileOutputStream Stream_iye = new FileOutputStream(Orúkọ);
        try { for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < Àkóónú_iye.length; ṣetúnṣe_wá_atọ̀ka_àkóónú++) Stream_iye.write(Àkóónú_iye[ṣetúnṣe_wá_atọ̀ka_àkóónú] & 255); } finally { Stream_iye.close(); }
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public static String Kàá(String Orúkọ) throws 입출력예외 {
        try { return 문자.ṣàtúpalẹ̀_àrokò_détà(바이트읽기(Orúkọ));
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public static void Kọ(String Orúkọ, String Àkóónú_iye) throws 입출력예외 {
        try { kọ_báìtì_iye(Orúkọ, 문자.부호화(Àkóónú_iye));
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
}
