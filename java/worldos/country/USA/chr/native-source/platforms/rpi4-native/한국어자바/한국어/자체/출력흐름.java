// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ: 순서를 보존해 내보내는 바이트의 ᎦᎳᏅᏛ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void ᎪᏪᎶᏗ(int ᏧᎬᏩᎶᏗᏯ) throws 입출력예외 {
        try { 표준흐름.write(ᏧᎬᏩᎶᏗᏯ);
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public void ᎪᏪᎶᏗ(byte[] ᎦᏟᏌᏅᎯ) throws 입출력예외 {
        try { 표준흐름.write(ᎦᏟᏌᏅᎯ);
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public void ᎪᏪᎶᏗ(byte[] ᎦᏟᏌᏅᎯ, int ᎠᎢᏎᏍᏗ, int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) throws 입출력예외 {
        try { 표준흐름.write(ᎦᏟᏌᏅᎯ, ᎠᎢᏎᏍᏗ, ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public void ᎯᏍᏚᎲᎦ() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
}
