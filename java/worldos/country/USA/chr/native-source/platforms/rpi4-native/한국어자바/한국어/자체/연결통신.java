// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static ᎫᏓᎸᎢ ᎯᏍᏚᎢ(String ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, int 접속번호) throws 입출력예외 {
        try { return ᎫᏓᎸᎢ.ᎯᏍᏚᎢ(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, 접속번호);
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.ᎯᏍᏚᎢ(접속번호);
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public static Socket ᎫᏓᎳ(String ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, int ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ) throws 입출력예외 {
        try { return new Socket(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ);
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public static ServerSocket 듣기(int ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ) throws 입출력예외 {
        try { return new ServerSocket(ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ);
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public static Socket 받기(ServerSocket ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ) throws 입출력예외 {
        try { return ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.accept();
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
}
