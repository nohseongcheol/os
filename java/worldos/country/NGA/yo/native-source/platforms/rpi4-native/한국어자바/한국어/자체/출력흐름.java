// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 Stream_iye: 순서를 보존해 내보내는 바이트의 òpónà_ìgbéwọlé. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Kọ(int iye) throws 입출력예외 {
        try { 표준흐름.write(iye);
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public void Kọ(byte[] détà) throws 입출력예외 {
        try { 표준흐름.write(détà);
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public void Kọ(byte[] détà, int Rọ́ọ̀nù, int gígùn_iye) throws 입출력예외 {
        try { 표준흐름.write(détà, Rọ́ọ̀nù, gígùn_iye);
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public void Ti() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
}
