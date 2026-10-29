// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static konnessjoni fetaħ(String ADDRESS, int 접속번호) throws 입출력예외 {
        try { return konnessjoni.fetaħ(ADDRESS, 접속번호);
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.fetaħ(접속번호);
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public static Socket AQBAD(String ADDRESS, int port_VALUE) throws 입출력예외 {
        try { return new Socket(ADDRESS, port_VALUE);
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public static ServerSocket 듣기(int port_VALUE) throws 입출력예외 {
        try { return new ServerSocket(port_VALUE);
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public static Socket 받기(ServerSocket server_VALUE) throws 입출력예외 {
        try { return server_VALUE.accept();
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
}
