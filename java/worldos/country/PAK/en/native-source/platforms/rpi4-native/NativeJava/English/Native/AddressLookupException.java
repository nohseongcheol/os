// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** AddressLookupException: an exception that can be declared, thrown and caught through the English API. */
public class AddressLookupException extends InputOutputException {
    public AddressLookupException() { super(); }
    public AddressLookupException(String description) { super(description); }
    public String description() { return getMessage(); }
}
