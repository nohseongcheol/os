// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** IPv4 UDP datagrams. External peers use numeric addresses. */
public final class communication {
    private communication() {}
    public static DatagramSocket open(int portValue) throws InputOutputException {
        try { return new DatagramSocket(portValue);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public static void send(DatagramSocket endpoint, int portValue, String contentValue) throws InputOutputException {
        try {
        send(endpoint, "127.0.0.1", portValue, contentValue);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public static void send(DatagramSocket endpoint, String address, int portValue, String contentValue) throws InputOutputException {
        try {
        byte[] byteValue = Characters.encode(contentValue);
        endpoint.send(new DatagramPacket(byteValue, byteValue.length, InetAddress.getByName(address), portValue));
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public static String receive(DatagramSocket endpoint) throws InputOutputException {
        try {
        byte[] byteValue = new byte[512]; DatagramPacket datagram = new DatagramPacket(byteValue, byteValue.length); endpoint.receive(datagram);
        byte[] result = new byte[datagram.getLength()]; System.arraycopy(byteValue, 0, result, 0, result.length); return Characters.decryptData(result);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public static void timeout(DatagramSocket endpoint, int milliseconds) throws InputOutputException {
        try { endpoint.setSoTimeout(milliseconds);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public static void close(DatagramSocket endpoint) { endpoint.close(); }
}
