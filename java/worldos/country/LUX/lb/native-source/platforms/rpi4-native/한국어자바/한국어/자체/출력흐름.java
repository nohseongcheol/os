// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 Stream_VALUE: 순서를 보존해 내보내는 바이트의 Kanal_Agab. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void schreiwen(int VALUE) throws 입출력예외 {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public void schreiwen(byte[] Daten) throws 입출력예외 {
        try { 표준흐름.write(Daten);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public void schreiwen(byte[] Daten, int Laf, int Längt_VALUE) throws 입출력예외 {
        try { 표준흐름.write(Daten, Laf, Längt_VALUE);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public void Clôture() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
}
