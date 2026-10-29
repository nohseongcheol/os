// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** Endpoint for sending and receiving UDP datagrams with preserved message boundaries. */
public final class DatagramChannel {
    private final java.net.DatagramSocket standardEndpoint;
    private DatagramChannel(int portNumber) throws InputOutputException {
        try { standardEndpoint = communication.open(portNumber);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public static DatagramChannel open(int portNumber) throws InputOutputException {
        try { return new DatagramChannel(portNumber);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public void send(String address, int portNumber, String data) throws InputOutputException {
        try { communication.send(standardEndpoint, address, portNumber, data);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public String receive() throws InputOutputException {
        try { return communication.receive(standardEndpoint);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public void timeout(int milliseconds) throws InputOutputException {
        try { communication.timeout(standardEndpoint, milliseconds);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public int portNumber() { return standardEndpoint.getLocalPort(); }
    public boolean isClosed() { return standardEndpoint.isClosed(); }
    public void close() { communication.close(standardEndpoint); }
}
