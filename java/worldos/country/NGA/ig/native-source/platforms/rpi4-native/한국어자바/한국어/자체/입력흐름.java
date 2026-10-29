// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 agịrị_valuu: 순서대로 들어오는 바이트를 읽는 ọwa_ndebà. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Wepụta_ọzi() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public int Wepụta_ọzi(byte[] datà) throws 입출력예외 {
        try { return 표준흐름.read(datà);
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public int Wepụta_ọzi(byte[] datà, int Bido, int ogologo_valuu) throws 입출력예외 {
        try { return 표준흐름.read(datà, Bido, ogologo_valuu);
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public void Mechie() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
}
