// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ: 순서대로 들어오는 바이트를 읽는 ᎦᎳᏅᏛ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int 읽기() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public int 읽기(byte[] ᎦᏟᏌᏅᎯ) throws 입출력예외 {
        try { return 표준흐름.read(ᎦᏟᏌᏅᎯ);
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public int 읽기(byte[] ᎦᏟᏌᏅᎯ, int ᎠᎢᏎᏍᏗ, int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) throws 입출력예외 {
        try { return 표준흐름.read(ᎦᏟᏌᏅᎯ, ᎠᎢᏎᏍᏗ, ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public void ᎯᏍᏚᎲᎦ() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
}
