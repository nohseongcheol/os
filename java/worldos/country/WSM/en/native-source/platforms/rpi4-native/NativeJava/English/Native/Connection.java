// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** Endpoint of a TCP byte stream connected to a peer. */
public final class Connection {
    private final java.net.Socket standardLibraryBridge;
    Connection(java.net.Socket standardLibraryBridge) { this.standardLibraryBridge = standardLibraryBridge; }
    public static Connection open(String address, int portNumber) throws InputOutputException {
        try {
            return new Connection(new java.net.Socket(address, portNumber));
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public InputStream inputValue() throws InputOutputException {
        try { return new InputStream(standardLibraryBridge.getInputStream());
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public OutputStream Output() throws InputOutputException {
        try { return new OutputStream(standardLibraryBridge.getOutputStream());
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public void timeout(int milliseconds) throws InputOutputException {
        try { standardLibraryBridge.setSoTimeout(milliseconds);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public int portNumber() { return standardLibraryBridge.getPort(); }
    public int localPortNumber() { return standardLibraryBridge.getLocalPort(); }
    public boolean isClosed() { return standardLibraryBridge.isClosed(); }
    public boolean connected() { return standardLibraryBridge.isConnected(); }
    public void close() throws InputOutputException {
        try { standardLibraryBridge.close();
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
}
