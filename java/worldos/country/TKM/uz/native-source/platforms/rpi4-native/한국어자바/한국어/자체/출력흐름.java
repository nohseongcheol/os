// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 oqim_VALUE: 순서를 보존해 내보내는 바이트의 kanal_kiritish. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Yozish(int VALUE) throws I_O_istisno {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public void Yozish(byte[] ma_lumotlar) throws I_O_istisno {
        try { 표준흐름.write(ma_lumotlar);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public void Yozish(byte[] ma_lumotlar, int Bajarish, int uzunlik_VALUE) throws I_O_istisno {
        try { 표준흐름.write(ma_lumotlar, Bajarish, uzunlik_VALUE);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public void 내보내기() throws I_O_istisno {
        try { 표준흐름.flush();
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public void Yopish() throws I_O_istisno {
        try { 표준흐름.close();
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
}
