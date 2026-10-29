#!/usr/bin/env python3
"""ഹോസ്റ്റ് 루프백 주소에만 바인딩하는 UDP 시험 സെര്_വര്_മൂല്യം. Ctrl+C로 종료한다."""
import argparse
import socket

def നടപ്പാക്കുക_കമാന്_ഡ്():
    പാര്_സ്_ചെയ്യുക_മൂല്യം = argparse.ArgumentParser(description='jkoros ഉപയോക്താവ് UDP 예제의 로컬 되돌림 സെര്_വര്_മൂല്യം')
    പാര്_സ്_ചെയ്യുക_മൂല്യം.add_argument('--port', type=int, default=9000)
    പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ് = പാര്_സ്_ചെയ്യുക_മൂല്യം.parse_args()
    if not 1 <= പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.port <= 65535: പാര്_സ്_ചെയ്യുക_മൂല്യം.error('പോര്_ട്ട്_മൂല്യം 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as സെര്_വര്_മൂല്യം:
        സെര്_വര്_മൂല്യം.bind(('127.0.0.1', പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.port))
        print('UDP 127.0.0.1:{} തയ്യാറാക്കുക. Ctrl+C로 പുറത്തുകടക്കൽ_പ്രോഗ്രാം.'.format(പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.port), flush=True)
        while True:
            ഡാറ്റാ, പീര്_മൂല്യം = സെര്_വര്_മൂല്യം.recvfrom(65535)
            സെര്_വര്_മൂല്യം.sendto(ഡാറ്റാ, പീര്_മൂല്യം)

if __name__ == '__main__':
    try: നടപ്പാക്കുക_കമാന്_ഡ്()
    except KeyboardInterrupt: pass
