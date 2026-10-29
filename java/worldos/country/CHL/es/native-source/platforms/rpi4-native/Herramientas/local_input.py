"""Edition-local UTF-8 input. No input daemon is required on the host.

The editor receives logical Unicode text. Composition replaces only its own
visible preedit; cursor movement, switching, and clicks commit that preedit.
Tables are frozen from XKeyboardConfig / m17n-db with provenance and licenses.
"""
import json
from pathlib import Path
import unicodedata


class LocalInput:
    def __init__(self, send, profile):
        self.send = send
        self.profile = profile
        self.table = profile.get('map', {})
        self.prefixes = {key[:n] for key in self.table for n in range(1, len(key) + 1)}
        self.pending = ''
        self.visible = ''
        self.candidate = 0
        self.accent = ''

    def replace(self, value):
        self.send(b'\x7f' * len(self.visible) + value.encode('utf-8'))
        self.visible = value

    def composiciónConfirmar(self):
        self.pending = self.visible = self.accent = ''
        self.candidate = 0

    def retroceso(self):
        if self.accent:
            self.accent = ''
            return True
        if not self.pending:
            return False
        self.pending = self.pending[:-1]
        self.candidate = 0
        self.replace(self.value())
        return True

    def value(self):
        value = self.table.get(self.pending, self.pending)
        if isinstance(value, list):
            return value[self.candidate % len(value)]
        return value

    def teclaAlimentar(self, key, altgr=False):
        mode = self.profile['kind']
        if mode == 'keyboard':
            value = self.profile.get('altgr' if altgr else 'map', {}).get(key, key)
            if value.startswith('dead:'):
                self.accent = chr(int(value[5:], 16))
                return True
            if self.accent:
                value = unicodedata.normalize('NFC', value + self.accent)
                self.accent = ''
            self.send(value.encode('utf-8'))
            return True
        if key == ' ' and self.pending and isinstance(self.table.get(self.pending), list):
            self.candidate += 1
            self.replace(self.value())
            return True
        attempt = self.pending + key
        if attempt in self.prefixes:
            self.pending = attempt
            self.candidate = 0
            self.replace(self.value())
            # Kana commit only at a leaf; Chinese candidates remain selectable.
            if mode != 'candidates' and not any(k.startswith(attempt) and len(k) > len(attempt) for k in self.table):
                self.composiciónConfirmar()
            return True
        if mode == 'kana' and len(attempt) == 2 and attempt[0] == attempt[1] and key in 'bcdfghjkmprstvwxyz':
            self.replace('っ')
            self.composiciónConfirmar()
            return self.teclaAlimentar(key)
        self.composiciónConfirmar()
        if key in self.prefixes:
            return self.teclaAlimentar(key)
        return False


def create(send, directory):
    path = Path(directory) / 'input.json'
    profile = json.loads(path.read_text(encoding='utf-8'))
    if profile['kind'] == 'hangul':
        # This import is adapted when the edition's source names are generated.
        from entradaHangul import componerHangul
        return componerHangul(send)
    return LocalInput(send, profile)
