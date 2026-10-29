// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 agịrị_valuu: 순서를 보존해 내보내는 바이트의 ọwa_ndebà. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Chekwaa_ozi(int valuu) throws 입출력예외 {
        try { 표준흐름.write(valuu);
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public void Chekwaa_ozi(byte[] datà) throws 입출력예외 {
        try { 표준흐름.write(datà);
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public void Chekwaa_ozi(byte[] datà, int Bido, int ogologo_valuu) throws 입출력예외 {
        try { 표준흐름.write(datà, Bido, ogologo_valuu);
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public void Mechie() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
}
