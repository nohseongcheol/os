#!/usr/bin/env python3
"""Merge Korean input defaults once, preserving a copy of previous settings."""
import configparser
import hashlib
from pathlib import Path
import shutil


def main():
    home = Path.home()
    version = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:16]
    state = home / '.local/state/jkoros/desktop-settings'
    stamp = state / 'version'
    if stamp.exists() and stamp.read_text().strip() == version:
        return
    backup = state / version
    backup.mkdir(parents=True, exist_ok=True)

    def read(name):
        path = home / '.config/fcitx5' / name
        config = configparser.ConfigParser(interpolation=None, strict=False)
        config.optionxform = str
        if path.exists():
            shutil.copy2(str(path), str(backup / name))
            config.read(str(path), encoding='utf-8')
        return path, config

    def section(config, name):
        if not config.has_section(name):
            config.add_section(name)
        return config[name]

    def write(path, config):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as stream:
            config.write(stream, space_around_delimiters=False)

    path, config = read('profile')
    group = section(config, 'Groups/0')
    group.setdefault('Name', 'Default')
    group.setdefault('Default Layout', 'us')
    group['DefaultIM'] = 'hangul'
    items = [name for name in config.sections() if name.startswith('Groups/0/Items/')]
    names = [config[name].get('Name') for name in items]
    for method in ['keyboard-us', 'hangul']:
        if method not in names:
            index = 0
            while config.has_section('Groups/0/Items/' + str(index)):
                index += 1
            item = section(config, 'Groups/0/Items/' + str(index))
            item['Name'] = method
            item['Layout'] = ''
    section(config, 'GroupOrder').setdefault('0', group['Name'])
    write(path, config)

    path, config = read('config')
    keys = section(config, 'Hotkey/TriggerKeys')
    for key in ['Control+space', 'Hangul']:
        if key not in keys.values():
            index = 0
            while str(index) in keys:
                index += 1
            keys[str(index)] = key
    write(path, config)

    # Java caches its fontconfig matches by locale/JDK version. Preserve the
    # old cache and let the new locale/font preferences create fresh matches.
    fonts = home / '.java/fonts'
    if fonts.exists() and not (backup / 'java-fonts').exists():
        fonts.rename(backup / 'java-fonts')
    stamp.write_text(version + '\n')


if __name__ == '__main__':
    main()
