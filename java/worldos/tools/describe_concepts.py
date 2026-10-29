#!/usr/bin/env python3
"""Attach function semantics and documented concept history without invented etymologies."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MEANINGS={
'action':'A callback invoked when a user activates a control.', 'address':'The host name or IP address of a network endpoint.',
'api':'The project facade exposing selected JDK operations; it is not a replacement POSIX ABI.',
'append':'Add text after existing output without replacing previous output.', 'arguments':'Arguments supplied to a class main method.',
'button':'A visible Swing control activated by the user.', 'choose':'Select an existing source file.', 'chooser':'The file selection dialog instance.',
'class':'The fully qualified name of the Java class containing main.', 'close':'Release an open file handle.',
'command':'An ordered process argument vector, without shell interpolation.', 'compile':'Translate Java source to JVM class files using javac.',
'connect':'Establish a TCP socket connection to an address and port.', 'current':'The process instance selected for cancellation.',
'data':'Bytes transferred to or from a file.', 'datagram':'An independently addressed UDP message endpoint.',
'directory':'The directory containing the user workspace files.', 'error':'Report a failed operation and its exception.',
'event':'A notification delivered by the graphical event system.', 'exception':'A Java object describing exceptional completion.',
'execute':'Create and wait for an operating system process.', 'file':'A persistent named byte sequence or an open handle to it.',
'initialize':'Construct the workbench controls and load resources.', 'key':'A resource lookup key, not a cryptographic key.',
'label':'Resolve the visible wording of a user interface control.', 'line':'One line of child-process output.',
'load':'Read UTF-8 source text into the editor.', 'messages':'The edition user interface resource dictionary.',
'mode':'RandomAccessFile access mode, such as r or rw.', 'name':'The main class name entered by the user.',
'open':'Obtain a RandomAccessFile handle for a path.', 'output':'The workbench area displaying compilation and process output.',
'panel':'A Swing container grouping related controls.', 'parser':'The tokenizer for quoted process arguments.',
'path':'The filesystem location of a source or data file.', 'port':'The transport protocol endpoint number.',
'position':'The byte offset within an open file.', 'process':'A running operating system subprocess.',
'read':'Transfer available bytes from the current file position into a buffer.', 'reader':'Decode a character stream as UTF-8.',
'remove':'Delete a named filesystem entry using Files.delete.', 'result':'The exit status of a child process.',
'run':'Compile and launch the user-selected Java main class.', 'save':'Write current editor text to a persistent UTF-8 file.',
'seek':'Set the next byte position of a random-access file.', 'settings':'The controls for class name and arguments.',
'size':'The length of a filesystem file, measured in bytes.', 'source':'The editable Java source text and source directory.',
'split':'The Swing split pane separating source from output.', 'stop':'Terminate the launched process and its descendants.',
'sync':'Request durable synchronization of a file descriptor.', 'terminal':'Launch an interactive command interpreter in an X terminal.',
'text':'A sequence of Unicode characters.', 'thread':'A Java execution thread.', 'toolbar':'A row of action controls.',
'window':'A top-level graphical application window.', 'worker':'The execution thread used for compilation and child processes.',
'workspace':'The complete source editor and compile/run workbench.', 'write':'Write bytes at the current random-access file position.'}
UNIX='https://cm-bell-labs.github.io/who/dmr/cacm.html'
JDK='https://docs.oracle.com/en/java/javase/25/docs/api/'
HISTORY={
'file':('Unix file system descriptions provide a historical computing context for named byte storage.',UNIX),
'directory':('The Unix account describes directories as mappings of names to file-system entries.',UNIX),
'process':('The Unix account describes process creation and execution as distinct system operations.',UNIX),
'execute':('The Unix account separates process creation with fork from program replacement with exec.',UNIX),
'read':('Unix exposes file reads through descriptors; the Java wrapper here uses RandomAccessFile.',UNIX),
'write':('Unix exposes file writes through descriptors; the Java wrapper here uses RandomAccessFile.',UNIX),
'seek':('Unix describes random file positioning with seek; the C alias targets modern lseek.',UNIX),
'port':('RFC 147 discusses ports and socket names in the ARPANET. This is historical context, not an assertion of identical modern semantics.','https://www.rfc-editor.org/info/rfc147/'),
'connect':('RFC 147 documents early socket concepts; the implementation uses modern Java TCP sockets.','https://www.rfc-editor.org/info/rfc147/'),
'datagram':('RFC 768 (1980) specifies UDP; the proposed wording emphasizes independent messages, not guaranteed delivery.','https://www.rfc-editor.org/info/rfc768/'),
}
concepts={key:{'current_meaning':meaning,'history':HISTORY.get(key,('No claim about the first coinage or the native-language etymology. Functional naming proposal.',JDK))[0],
                  'reference':HISTORY.get(key,('',JDK))[1],'native_etymology_review':'pending'} for key,meaning in MEANINGS.items()}
(ROOT/'naming/concepts.json').write_text(json.dumps(concepts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
