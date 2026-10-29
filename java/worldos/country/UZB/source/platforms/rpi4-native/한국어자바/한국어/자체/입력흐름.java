// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 oqim_VALUE: 순서대로 들어오는 바이트를 읽는 kanal_kiritish. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Oʻqish() throws I_O_istisno {
        try { return 표준흐름.read();
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public int Oʻqish(byte[] ma_lumotlar) throws I_O_istisno {
        try { return 표준흐름.read(ma_lumotlar);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public int Oʻqish(byte[] ma_lumotlar, int Bajarish, int uzunlik_VALUE) throws I_O_istisno {
        try { return 표준흐름.read(ma_lumotlar, Bajarish, uzunlik_VALUE);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public void Yopish() throws I_O_istisno {
        try { 표준흐름.close();
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
}
