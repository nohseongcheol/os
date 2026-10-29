// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** Accepts incoming TCP connections. */
public final class receivePort {
    private final java.net.ServerSocket standardPort;
    private receivePort(int portNumber) throws InputOutputException {
        try { standardPort = new java.net.ServerSocket(portNumber);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public static receivePort open(int portNumber) throws InputOutputException {
        try { return new receivePort(portNumber);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public Connection receive() throws InputOutputException {
        try { return new Connection(standardPort.accept());
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public int portNumber() { return standardPort.getLocalPort(); }
    public void timeout(int milliseconds) throws InputOutputException {
        try { standardPort.setSoTimeout(milliseconds);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public boolean isClosed() { return standardPort.isClosed(); }
    public void close() throws InputOutputException {
        try { standardPort.close();
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
}
