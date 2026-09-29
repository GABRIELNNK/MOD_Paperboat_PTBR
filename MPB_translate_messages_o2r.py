#!/usr/bin/env python3
"""Compile the editable Star Rod JSON into a text-only Paperboat O2R mod and export errors to CSV."""

from __future__ import annotations

import argparse
import csv
import json
import re
import struct
import zipfile
from pathlib import Path

# ==============================================================================
# CONFIGURAÇÃO DOS CAMINHOS DAS PASTAS DE DEPENDÊNCIA
# ==============================================================================
# Pasta com os binários de referência extraídos do PM64.o2r (ex: MSG_Intro_0001)
MESSAGES_DIR_PATH = "translate/messages"

# Pasta com os arquivos de texto (.str) extraídos do Star Rod
SRC_DIR_PATH = "translate/src"
# ==============================================================================

FONTS_XML = '''<?xml version="1.0" encoding="UTF-8"?>
<Fonts>
	<Font name="Normal" lineHeight="16" unk="14" fullspaceWidth="10,10,10,10" baseHeightOffset="0,-2,0,0"/>
	<Font name="Menus" lineHeight="16" unk="14" fullspaceWidth="9,9,9,9" baseHeightOffset="-2,0,0,0"/>
	<Font name="Title" lineHeight="16" unk="14" fullspaceWidth="14" baseHeightOffset="0"/>
	<Font name="Subtitle" lineHeight="10" unk="10" fullspaceWidth="10" baseHeightOffset="0"/>
	<CharSet name="normal">
		<Character width="11"/> <!-- id = 00, val = "NOTE" -->
		<Character width="8"/> <!--  id = 01, val = "!" -->
		<Character width="8"/> <!--  id = 02, val = """ -->
		<Character width="10"/> <!-- id = 03, val = "#" -->
		<Character width="9"/> <!--  id = 04, val = "$" -->
		<Character width="9"/> <!--  id = 05, val = "%" -->
		<Character width="9"/> <!--  id = 06, val = "&" -->
		<Character width="4"/> <!--  id = 07, val = "'" -->
		<Character width="8"/> <!--  id = 08, val = "(" -->
		<Character width="8"/> <!--  id = 09, val = ")" -->
		<Character width="9"/> <!--  id = 0A, val = "*" -->
		<Character width="9"/> <!--  id = 0B, val = "+" -->
		<Character width="5"/> <!--  id = 0C, val = "," -->
		<Character width="9"/> <!--  id = 0D, val = "-" -->
		<Character width="5"/> <!--  id = 0E, val = "." -->
		<Character width="10"/> <!-- id = 0F, val = "/" -->
		<Character width="9"/> <!--  id = 10, val = "0" -->
		<Character width="7"/> <!--  id = 11, val = "1" -->
		<Character width="9"/> <!--  id = 12, val = "2" -->
		<Character width="9"/> <!--  id = 13, val = "3" -->
		<Character width="9"/> <!--  id = 14, val = "4" -->
		<Character width="9"/> <!--  id = 15, val = "5" -->
		<Character width="9"/> <!--  id = 16, val = "6" -->
		<Character width="9"/> <!--  id = 17, val = "7" -->
		<Character width="9"/> <!--  id = 18, val = "8" -->
		<Character width="9"/> <!--  id = 19, val = "9" -->
		<Character width="5"/> <!--  id = 1A, val = ":" -->
		<Character width="5"/> <!--  id = 1B, val = ";" -->
		<Character width="8"/> <!--  id = 1C, val = "<" -->
		<Character width="9"/> <!--  id = 1D, val = "=" -->
		<Character width="8"/> <!--  id = 1E, val = ">" -->
		<Character width="9"/> <!--  id = 1F, val = "?" -->
		<Character width="10"/> <!-- id = 20, val = "@" -->
		<Character width="9"/> <!--  id = 21, val = "A" -->
		<Character width="9"/> <!--  id = 22, val = "B" -->
		<Character width="9"/> <!--  id = 23, val = "C" -->
		<Character width="9"/> <!--  id = 24, val = "D" -->
		<Character width="9"/> <!--  id = 25, val = "E" -->
		<Character width="9"/> <!--  id = 26, val = "F" -->
		<Character width="9"/> <!--  id = 27, val = "G" -->
		<Character width="9"/> <!--  id = 28, val = "H" -->
		<Character width="7"/> <!--  id = 29, val = "I" -->
		<Character width="9"/> <!--  id = 2A, val = "J" -->
		<Character width="9"/> <!--  id = 2B, val = "K" -->
		<Character width="9"/> <!--  id = 2C, val = "L" -->
		<Character width="9"/> <!--  id = 2D, val = "M" -->
		<Character width="9"/> <!--  id = 2E, val = "N" -->
		<Character width="9"/> <!--  id = 2F, val = "O" -->
		<Character width="9"/> <!--  id = 30, val = "P" -->
		<Character width="9"/> <!--  id = 31, val = "Q" -->
		<Character width="9"/> <!--  id = 32, val = "R" -->
		<Character width="9"/> <!--  id = 33, val = "S" -->
		<Character width="9"/> <!--  id = 34, val = "T" -->
		<Character width="9"/> <!--  id = 35, val = "U" -->
		<Character width="9"/> <!--  id = 36, val = "V" -->
		<Character width="9"/> <!--  id = 37, val = "W" -->
		<Character width="9"/> <!--  id = 38, val = "X" -->
		<Character width="9"/> <!--  id = 39, val = "Y" -->
		<Character width="9"/> <!--  id = 3A, val = "Z" -->
		<Character width="7"/> <!--  id = 3B, val = "[" -->
		<Character width="9"/> <!--  id = 3C, val = "¥" -->
		<Character width="6"/> <!--  id = 3D, val = "]" -->
		<Character width="7"/> <!--  id = 3E, val = "^" -->
		<Character width="9"/> <!--  id = 3F, val = "_" -->
		<Character width="6"/> <!--  id = 40, val = "`" -->
		<Character width="9"/> <!--  id = 41, val = "a" -->
		<Character width="8"/> <!--  id = 42, val = "b" -->
		<Character width="8"/> <!--  id = 43, val = "c" -->
		<Character width="9"/> <!--  id = 44, val = "d" -->
		<Character width="8"/> <!--  id = 45, val = "e" -->
		<Character width="8"/> <!--  id = 46, val = "f" -->
		<Character width="8"/> <!--  id = 47, val = "g" -->
		<Character width="7"/> <!--  id = 48, val = "h" -->
		<Character width="4"/> <!--  id = 49, val = "i" -->
		<Character width="7"/> <!--  id = 4A, val = "j" -->
		<Character width="8"/> <!--  id = 4B, val = "k" -->
		<Character width="4"/> <!--  id = 4C, val = "l" -->
		<Character width="9"/> <!--  id = 4D, val = "m" -->
		<Character width="8"/> <!--  id = 4E, val = "n" -->
		<Character width="7"/> <!--  id = 4F, val = "o" -->
		<Character width="9"/> <!--  id = 50, val = "p" -->
		<Character width="8"/> <!--  id = 51, val = "q" -->
		<Character width="8"/> <!--  id = 52, val = "r" -->
		<Character width="8"/> <!--  id = 53, val = "s" -->
		<Character width="8"/> <!--  id = 54, val = "t" -->
		<Character width="8"/> <!--  id = 55, val = "u" -->
		<Character width="8"/> <!--  id = 56, val = "v" -->
		<Character width="9"/> <!--  id = 57, val = "w" -->
		<Character width="8"/> <!--  id = 58, val = "x" -->
		<Character width="8"/> <!--  id = 59, val = "y" -->
		<Character width="8"/> <!--  id = 5A, val = "z" -->
		<Character width="7"/> <!--  id = 5B, val = "{" -->
		<Character width="3"/> <!--  id = 5C, val = "|" -->
		<Character width="7"/> <!--  id = 5D, val = "}" -->
		<Character width="10"/> <!-- id = 5E, val = "~" -->
		<Character width="7"/> <!--  id = 5F, val = "°" -->
		<Character width="9"/> <!--  id = 60, val = "À" -->
		<Character width="9"/> <!--  id = 61, val = "Á" -->
		<Character width="9"/> <!--  id = 62, val = "Â" -->
		<Character width="9"/> <!--  id = 63, val = "Ä" -->
		<Character width="9"/> <!--  id = 64, val = "Ç" -->
		<Character width="9"/> <!--  id = 65, val = "È" -->
		<Character width="9"/> <!--  id = 66, val = "É" -->
		<Character width="9"/> <!--  id = 67, val = "Ê" -->
		<Character width="9"/> <!--  id = 68, val = "Ë" -->
		<Character width="7"/> <!--  id = 69, val = "Ì" -->
		<Character width="7"/> <!--  id = 6A, val = "Í" -->
		<Character width="7"/> <!--  id = 6B, val = "Î" -->
		<Character width="8"/> <!--  id = 6C, val = "Ï" -->
		<Character width="9"/> <!--  id = 6D, val = "Ñ" -->
		<Character width="9"/> <!--  id = 6E, val = "Ò" -->
		<Character width="9"/> <!--  id = 6F, val = "Ó" -->
		<Character width="9"/> <!--  id = 70, val = "Ô" -->
		<Character width="9"/> <!--  id = 71, val = "Ö" -->
		<Character width="9"/> <!--  id = 72, val = "Ù" -->
		<Character width="9"/> <!--  id = 73, val = "Ú" -->
		<Character width="9"/> <!--  id = 74, val = "Û" -->
		<Character width="9"/> <!--  id = 75, val = "Ü" -->
		<Character width="9"/> <!--  id = 76, val = "ß" -->
		<Character width="9"/> <!--  id = 77, val = "à" -->
		<Character width="9"/> <!--  id = 78, val = "á" -->
		<Character width="9"/> <!--  id = 79, val = "â" -->
		<Character width="9"/> <!--  id = 7A, val = "ä" -->
		<Character width="8"/> <!--  id = 7B, val = "ç" -->
		<Character width="8"/> <!--  id = 7C, val = "è" -->
		<Character width="8"/> <!--  id = 7D, val = "é" -->
		<Character width="8"/> <!--  id = 7E, val = "ê" -->
		<Character width="8"/> <!--  id = 7F, val = "ë" -->
		<Character width="6"/> <!--  id = 80, val = "ì" -->
		<Character width="6"/> <!--  id = 81, val = "í" -->
		<Character width="6"/> <!--  id = 82, val = "î" -->
		<Character width="7"/> <!--  id = 83, val = "ï" -->
		<Character width="9"/> <!--  id = 84, val = "ñ" -->
		<Character width="7"/> <!--  id = 85, val = "ò" -->
		<Character width="7"/> <!--  id = 86, val = "ó" -->
		<Character width="7"/> <!--  id = 87, val = "ô" -->
		<Character width="8"/> <!--  id = 88, val = "ö" -->
		<Character width="8"/> <!--  id = 89, val = "ù" -->
		<Character width="8"/> <!--  id = 8A, val = "ú" -->
		<Character width="8"/> <!--  id = 8B, val = "û" -->
		<Character width="8"/> <!--  id = 8C, val = "ü" -->
		<Character width="6"/> <!--  id = 8D, val = "¡" -->
		<Character width="9"/> <!--  id = 8E, val = "¿" -->
		<Character width="7"/> <!--  id = 8F, val = "ª" -->
		<Character width="11"/> <!-- id = 90, val = "HEART" -->
		<Character width="11"/> <!-- id = 91, val = "STAR" -->
		<Character width="11"/> <!-- id = 92, val = "UP" -->
		<Character width="11"/> <!-- id = 93, val = "DOWN" -->
		<Character width="12"/> <!-- id = 94, val = "LEFT" -->
		<Character width="12"/> <!-- id = 95, val = "RIGHT" -->
		<Character width="11"/> <!-- id = 96, val = "CIRCLE" -->
		<Character width="11"/> <!-- id = 97, val = "CROSS" -->
		<Character width="13"/> <!-- id = 98, val = "A" -->
		<Character width="13"/> <!-- id = 99, val = "B" -->
		<Character width="14"/> <!-- id = 9A, val = "L" -->
		<Character width="14"/> <!-- id = 9B, val = "R" -->
		<Character width="12"/> <!-- id = 9C, val = "Z" -->
		<Character width="13"/> <!-- id = 9D, val = "C-UP" -->
		<Character width="13"/> <!-- id = 9E, val = "C-DOWN" -->
		<Character width="13"/> <!-- id = 9F, val = "C-LEFT" -->
		<Character width="13"/> <!-- id = A0, val = "C-RIGHT" -->
		<Character width="16"/> <!-- id = A1, val = "START" -->
		<Character width="9"/> <!--  id = A2, val = "“" -->
		<Character width="9"/> <!--  id = A3, val = "”" -->
		<Character width="5"/> <!--  id = A4, val = "‘" -->
		<Character width="5"/> <!--  id = A5, val = "’" -->
	</CharSet>
	<CharSet name="credits-title">
		<Character width="8"/> <!--  id = 00, val = "A" -->
		<Character width="8"/> <!--  id = 01, val = "B" -->
		<Character width="8"/> <!--  id = 02, val = "C" -->
		<Character width="9"/> <!--  id = 03, val = "D" -->
		<Character width="8"/> <!--  id = 04, val = "E" -->
		<Character width="8"/> <!--  id = 05, val = "F" -->
		<Character width="8"/> <!--  id = 06, val = "G" -->
		<Character width="8"/> <!--  id = 07, val = "H" -->
		<Character width="5"/> <!--  id = 08, val = "I" -->
		<Character width="8"/> <!--  id = 09, val = "J" -->
		<Character width="9"/> <!--  id = 0A, val = "K" -->
		<Character width="8"/> <!--  id = 0B, val = "L" -->
		<Character width="10"/> <!-- id = 0C, val = "M" -->
		<Character width="8"/> <!--  id = 0D, val = "N" -->
		<Character width="8"/> <!--  id = 0E, val = "O" -->
		<Character width="9"/> <!--  id = 0F, val = "P" -->
		<Character width="8"/> <!--  id = 10, val = "Q" -->
		<Character width="9"/> <!--  id = 11, val = "R" -->
		<Character width="8"/> <!--  id = 12, val = "S" -->
		<Character width="8"/> <!--  id = 13, val = "T" -->
		<Character width="8"/> <!--  id = 14, val = "U" -->
		<Character width="8"/> <!--  id = 15, val = "V" -->
		<Character width="10"/> <!-- id = 16, val = "W" -->
		<Character width="9"/> <!--  id = 17, val = "X" -->
		<Character width="9"/> <!--  id = 18, val = "Y" -->
		<Character width="8"/> <!--  id = 19, val = "Z" -->
		<Character width="4"/> <!--  id = 1A, val = "'" -->
		<Character width="3"/> <!--  id = 1B, val = "." -->
		<Character width="4"/> <!--  id = 1C, val = "," -->
		<Character width="9"/> <!--  id = 1D, val = "0" -->
		<Character width="9"/> <!--  id = 1E, val = "1" -->
		<Character width="9"/> <!--  id = 1F, val = "2" -->
		<Character width="9"/> <!--  id = 20, val = "3" -->
		<Character width="9"/> <!--  id = 21, val = "4" -->
		<Character width="9"/> <!--  id = 22, val = "5" -->
		<Character width="9"/> <!--  id = 23, val = "6" -->
		<Character width="9"/> <!--  id = 24, val = "7" -->
		<Character width="9"/> <!--  id = 25, val = "8" -->
		<Character width="9"/> <!--  id = 26, val = "9" -->
		<Character width="10"/> <!-- id = 27, val = "©" -->
		<Character width="10"/> <!-- id = 28, val = "&" -->
	</CharSet>
	<CharSet name="credits-name">
		<Character width="9"/> <!--  id = 00, val = "A" -->
		<Character width="9"/> <!--  id = 01, val = "B" -->
		<Character width="8"/> <!--  id = 02, val = "C" -->
		<Character width="8"/> <!--  id = 03, val = "D" -->
		<Character width="7"/> <!--  id = 04, val = "E" -->
		<Character width="7"/> <!--  id = 05, val = "F" -->
		<Character width="8"/> <!--  id = 06, val = "G" -->
		<Character width="7"/> <!--  id = 07, val = "H" -->
		<Character width="3"/> <!--  id = 08, val = "I" -->
		<Character width="7"/> <!--  id = 09, val = "J" -->
		<Character width="7"/> <!--  id = 0A, val = "K" -->
		<Character width="7"/> <!--  id = 0B, val = "L" -->
		<Character width="8"/> <!--  id = 0C, val = "M" -->
		<Character width="7"/> <!--  id = 0D, val = "N" -->
		<Character width="8"/> <!--  id = 0E, val = "O" -->
		<Character width="8"/> <!--  id = 0F, val = "P" -->
		<Character width="8"/> <!--  id = 10, val = "Q" -->
		<Character width="7"/> <!--  id = 11, val = "R" -->
		<Character width="7"/> <!--  id = 12, val = "S" -->
		<Character width="8"/> <!--  id = 13, val = "T" -->
		<Character width="7"/> <!--  id = 14, val = "U" -->
		<Character width="7"/> <!--  id = 15, val = "V" -->
		<Character width="8"/> <!--  id = 16, val = "W" -->
		<Character width="8"/> <!--  id = 17, val = "X" -->
		<Character width="8"/> <!--  id = 18, val = "Y" -->
		<Character width="7"/> <!--  id = 19, val = "Z" -->
		<Character width="4"/> <!--  id = 1A, val = "'" -->
		<Character width="3"/> <!--  id = 1B, val = "." -->
		<Character width="4"/> <!--  id = 1C, val = "," -->
		<Character width="8"/> <!--  id = 1D, val = "0" -->
		<Character width="8"/> <!--  id = 1E, val = "1" -->
		<Character width="8"/> <!--  id = 1F, val = "2" -->
		<Character width="8"/> <!--  id = 20, val = "3" -->
		<Character width="8"/> <!--  id = 21, val = "4" -->
		<Character width="8"/> <!--  id = 22, val = "5" -->
		<Character width="8"/> <!--  id = 23, val = "6" -->
		<Character width="8"/> <!--  id = 24, val = "7" -->
		<Character width="8"/> <!--  id = 25, val = "8" -->
		<Character width="8"/> <!--  id = 26, val = "9" -->
		<Character width="8"/> <!--  id = 27, val = "©" -->
		<Character width="8"/> <!--  id = 28, val = "&" -->
	</CharSet>
</Fonts>
'''

COMMAND_RE = re.compile(r"\[([^\]]+)\]")
CHAR_RE = re.compile(r'id\s*=\s*([0-9A-Fa-f]{2}),\s*val\s*=\s*"(.*?)"')
EFFECT_CODES = {"Shake": 0x00, "Wave": 0x01, "PrintRising": 0x0A}
ICON_BYTES = {
    "HEART": 0x90, "STAR": 0x91, "UP": 0x92, "DOWN": 0x93,
    "LEFT": 0x94, "RIGHT": 0x95, "CIRCLE": 0x96, "CROSS": 0x97,
    "A": 0x98, "B": 0x99, "L": 0x9A, "R": 0x9B, "Z": 0x9C,
    "C-UP": 0x9D, "C-DOWN": 0x9E, "C-LEFT": 0x9F, "C-RIGHT": 0xA0,
    "START": 0xA1,
}

def load_charset(xml_data: str = FONTS_XML) -> dict[str, int]:
    """Load character mappings from embedded fonts XML string."""
    normal = re.search(r'<CharSet name="normal">(.*?)</CharSet>', xml_data, re.DOTALL)
    if normal is None:
        raise ValueError("normal charset not found in embedded fonts XML")
    text = normal.group(1)
    chars: dict[str, int] = {" ": 0xF7}
    for match in CHAR_RE.finditer(text):
        if int(match.group(1), 16) >= 0x90:
            continue
        value = match.group(2)
        if value in {"NOTE", "HEART", "STAR", "UP", "DOWN", "LEFT", "RIGHT", "CIRCLE", "CROSS", "C-UP", "C-DOWN", "C-LEFT", "C-RIGHT", "START"}:
            continue
        if len(value) == 1:
            chars[value] = int(match.group(1), 16)
    chars.update({
        '"': 0x02,
        "'": 0x07,
        ",": 0x0C,
        ".": 0x0E,
    })
    return chars

def command_bytes(command: str, active_effect: str | None = None) -> bytes | None:
    """Map text command tags to byte representations."""
    if command == "BR":
        return b"\xF0"
    if command == "End":
        return b"\xFD"
    if command == "Wait":
        return b"\xF1"
    if command == "Next":
        return b"\xFB"
    if command.startswith("Pause "):
        return b"\xF2" + bytes([int(command.split()[1], 0)])
    if command == "Style Right":
        return b"\xFC\x01"
    if command == "Style Inspect":
        return b"\xFC\x06"
    if command == "Style Sign":
        return b"\xFC\x07"
    if command == "Voice Star":
        return b"\xFF\x2F\x02"
    if command == "Voice Bowser":
        return b"\xFF\x2F\x01"
    if command in EFFECT_CODES:
        return b"\xFF\x26" + bytes([EFFECT_CODES[command]])
    if command.startswith("/") and command[1:] in EFFECT_CODES:
        return b"\xFF\x27" + bytes([EFFECT_CODES[command[1:]]])
    if command == "/fx":
        if active_effect in EFFECT_CODES:
            return b"\xFF\x27" + bytes([EFFECT_CODES[active_effect]])
        return None
    if command == "SizeReset":
        return b"\xFF\x0E"
    if command == "SavePos":
        return b"\xFF\x22"
    if command == "RestorePos":
        return b"\xFF\x23"
    if command.startswith("Style Choice "):
        parts = command.replace("=", " ").replace(",", " ").split()
        x, y = int(parts[3]), int(parts[4])
        w, h = int(parts[6]), int(parts[7])
        return b"\xFC\x05" + bytes([x, y, w, h])
    if command == "StartChoice":
        return b"\xFF\x09"

    if command.startswith("Option "):
        val = int(command.split()[1], 0)
        return b"\xFF\x1E" + bytes([val]) + b"\xFF\x21" + bytes([val])
    if command.startswith("Volume percent="):
        percent = float(command.split("=")[1])
        val = int(round((percent / 100.0) * 255)) & 0xFF
        return b"\xFF\x2E" + bytes([val])
    if command == "DelayOff":
        return b"\xFF\x09"
    if command == "DelayOn":
        return b"\xFF\x0A"
    if command == "InputOff":
        return b"\xFF\x07"
    if command == "InputOn":
        return b"\xFF\x08"
    if command == "EnableCDownNext":
        return b"\xFF\x2B"
    if command.startswith("Right "):
        return b"\xFF\x12" + bytes([int(command.split()[1], 0)])
    if command.startswith("Down "):
        return b"\xFF\x13" + bytes([int(command.split()[1], 0)])
    if command.startswith("Up "):
        return b"\xFF\x14" + bytes([int(command.split()[1], 0)])
    if command.startswith("Scroll "):
        return b"\xFF\x0C" + bytes([int(command.split()[1], 0)])
    if command.startswith("Size "):
        val = int(command.split()[1], 0)
        return b"\xFF\x0D" + bytes([val, val])
    if command.startswith("SetPosX "):
        val = int(command.split()[1], 0)
        return b"\xFF\x10" + val.to_bytes(2, byteorder='big')
    if command.startswith("SetPosY "):
        return b"\xFF\x11" + bytes([int(command.split()[1], 0)])
    if command.startswith("InlineImage index="):
        return b"\xFF\x15" + bytes([int(command.split("=")[1], 0)])
    if command in ICON_BYTES:
        return bytes([ICON_BYTES[command]])
    if command.startswith("CenterX "):
        return b"\xFF\x29" + bytes([int(command.split()[1], 0)])
    if command.startswith("Color "):
        return b"\xFF\x05" + bytes([int(command.split()[1], 0)])
    if command.startswith("Var "):
        return b"\xFF\x28" + bytes([int(command.split()[1], 0)])
    if command == "Yield":
        return b"\xFF\x04"
    return None

def encode_text(text: str, charset: dict[str, int]) -> bytes:
    """Encode string containing commands and characters into bytes."""
    output = bytearray()
    position = 0
    effect_stack: list[str] = []
    for match in COMMAND_RE.finditer(text):
        encode_chars(text[position:match.start()], charset, output)
        command = match.group(1)
        active_effect = effect_stack[-1] if effect_stack else None
        encoded = command_bytes(command, active_effect)
        if encoded is None:
            if command in charset:
                output.append(charset[command])
            else:
                raise ValueError(f"Unsupported Star Rod command: [{command}]")
        else:
            output.extend(encoded)
            if command in EFFECT_CODES:
                effect_stack.append(command)
            elif command == "/fx" and effect_stack:
                effect_stack.pop()
        position = match.end()
    encode_chars(text[position:], charset, output)
    return bytes(output)

def preserve_effects(
    translated: str,
    original_text: str,
    reference_payload: bytes,
    charset: dict[str, int],
) -> bytes:
    """Encode translated text while copying unknown command bytes from English."""
    original_commands = list(COMMAND_RE.finditer(original_text))
    translated_commands = list(COMMAND_RE.finditer(translated))
    if [m.group(1) for m in original_commands] != [m.group(1) for m in translated_commands]:
        raise ValueError("effect commands were changed; keep existing [effects] unchanged")

    effects: list[bytes] = []
    cursor = 0
    text_position = 0
    effect_stack: list[str] = []
    for index, match in enumerate(original_commands):
        literal = original_text[text_position:match.start()].replace("\n", "")
        encoded_literal = encode_chars_bytes(literal, charset)
        start = reference_payload.find(encoded_literal, cursor) if encoded_literal else cursor
        if start < cursor:
            raise ValueError("could not align original text with reference payload")
        cursor = start + len(encoded_literal)
        active_effect = effect_stack[-1] if effect_stack else None
        known = command_bytes(match.group(1), active_effect)
        if known is not None:
            match_idx = reference_payload.find(known, cursor, cursor + 16)
            if match_idx == -1:
                raise ValueError(f"reference bytes do not match [{match.group(1)}]")
            cursor = match_idx + len(known)
            if match.group(1) in EFFECT_CODES:
                effect_stack.append(match.group(1))
            elif match.group(1) == "/fx" and effect_stack:
                effect_stack.pop()
            elif match.group(1).startswith("/") and match.group(1)[1:] in EFFECT_CODES:
                if effect_stack and effect_stack[-1] == match.group(1)[1:]:
                    effect_stack.pop()
        else:
            next_match = next((m for m in original_commands[index + 1:] if m.start() >= match.end()), None)
            next_text = original_text[match.end():next_match.start() if next_match else len(original_text)]
            next_bytes = encode_chars_bytes(next_text, charset)
            if next_bytes:
                end = reference_payload.find(next_bytes, cursor)
            else:
                next_command = next(
                    (command_bytes(item.group(1)) for item in original_commands[index + 1:]
                     if command_bytes(item.group(1)) is not None),
                    None,
                )
                end = reference_payload.find(next_command, cursor) if next_command else len(reference_payload)
            if end < cursor:
                raise ValueError(f"could not locate effect [{match.group(1)}]")
            effects.append(reference_payload[cursor:end])
            cursor = end
        text_position = match.end()

    tail = encode_chars_bytes(original_text[text_position:], charset)
    if tail and reference_payload.find(tail, cursor) < 0:
        raise ValueError("could not align text after the last effect")

    output = bytearray()
    effect_index = 0
    position = 0
    effect_stack = []
    for match in translated_commands:
        output.extend(encode_chars_bytes(translated[position:match.start()], charset))
        active_effect = effect_stack[-1] if effect_stack else None
        known = command_bytes(match.group(1), active_effect)
        if known is not None:
            output.extend(known)
        else:
            output.extend(effects[effect_index])
            effect_index += 1
        if match.group(1) in EFFECT_CODES:
            effect_stack.append(match.group(1))
        elif match.group(1) == "/fx" and effect_stack:
            effect_stack.pop()
        elif match.group(1).startswith("/") and match.group(1)[1:] in EFFECT_CODES:
            if effect_stack and effect_stack[-1] == match.group(1)[1:]:
                effect_stack.pop()
        position = match.end()
    output.extend(encode_chars_bytes(translated[position:], charset))
    return bytes(output)

def encode_chars_bytes(text: str, charset: dict[str, int]) -> bytes:
    output = bytearray()
    encode_chars(text, charset, output)
    return bytes(output)


def encode_chars(text: str, charset: dict[str, int], output: bytearray) -> None:
    for char in text.replace("\n", "").replace("\\%", "%"):
        # Transliteração para caracteres equivalentes aceitos no charset original
        char = "Ä" if char == "Ã" else char
        char = "Ö" if char == "Õ" else char        
        char = "ä" if char == "ã" else char
        char = "ö" if char == "õ" else char
        if char not in charset:
            raise ValueError(f"Character is not present in charset: {char!r}")
        output.append(charset[char])

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("messages", type=Path, help="Editable JSON generated from Star Rod")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output .o2r path (default: JSON path with .o2r extension)",
    )
    parser.add_argument(
        "--csv-errors",
        type=Path,
        default=Path("errors.csv"),
        help="Output CSV file path for recorded errors (default: errors.csv)",
    )
    parser.add_argument(
        "-y",
        "--ignore-errors",
        action="store_true",
        help="Generate .o2r file ignoring messages with errors without prompting",
    )
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent

    # Resolution order for messages_dir (binary files):
    # 1. Directly from CWD or absolute path configured at top of script
    # 2. Relative to script directory
    reference_dir = Path(MESSAGES_DIR_PATH)
    if not reference_dir.is_dir():
        reference_dir = script_dir / MESSAGES_DIR_PATH

    src_dir = Path(SRC_DIR_PATH)
    if not src_dir.is_dir():
        src_dir = script_dir / SRC_DIR_PATH

    # Diagnostic verification before starting iteration
    if not reference_dir.is_dir():
        print(f"ERRO CRÍTICO: Pasta de mensagens binárias não foi localizada!")
        print(f"  Caminho procurado: {reference_dir.resolve()}")
        print(f"  Por favor, extraia a pasta 'messages' do PM64.o2r para '{MESSAGES_DIR_PATH}'")
        return 1

    output = args.output or args.messages.with_suffix(".o2r")
    document = json.loads(args.messages.read_text(encoding="utf-8"))
    charset = load_charset()
    compiled = 0

    error_entries: list[tuple[str, str, int | str]] = []

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for message in document["messages"]:
            resource = message.get("resource")
            if not resource or message.get("text") == message.get("original_text"):
                continue
            reference = reference_dir / resource
            if not reference.is_file():
                err_msg = f"{message['id']}: missing reference {resource}"
                error_entries.append((f"{err_msg} - N/A", err_msg, "N/A"))
                continue
            original = reference.read_bytes()
            try:
                if any(command_bytes(match.group(1)) is None for match in COMMAND_RE.finditer(message["text"])):
                    original_text = message.get("original_text")
                    if not original_text:
                        raise ValueError("JSON lacks original_text needed to preserve effects")
                    payload = preserve_effects(message["text"], original_text, original[0x44:], charset)
                else:
                    payload = encode_text(message["text"], charset)
            except ValueError as error:
                err_msg = f"{message['id']}: {error}"
                error_entries.append((f"{err_msg} - N/A", err_msg, "N/A"))
                continue

            limit = struct.unpack_from("<I", original, 0x40)[0]
            if len(payload) > limit:
                diff = len(payload) - limit
                err_msg = f"{message['id']}: encoded size 0x{len(payload):X} exceeds 0x{limit:X}"
                formatted = f"{err_msg} - {diff}"
                error_entries.append((formatted, err_msg, diff))
                continue

            resource_data = bytearray(original[:0x44])
            resource_data[0x40:0x44] = struct.pack("<I", len(payload))
            resource_data.extend(payload)
            archive.writestr(f"messages/{resource}", resource_data)
            compiled += 1

    if error_entries:
        csv_path: Path = args.csv_errors
        with csv_path.open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Error Entry"])
            for entry, _, _ in error_entries:
                writer.writerow([entry])

        print(f"Recorded {len(error_entries)} errors into '{csv_path}'.")

        for entry, _, _ in error_entries[:20]:
            print(f"error: {entry}")
        if len(error_entries) > 20:
            print(f"error: ... and {len(error_entries) - 20} more")

        ignore = False
        if args.ignore_errors:
            ignore = True
        else:
            try:
                response = input("\nDeseja gerar o arquivo .o2r ignorando as mensagens com erro? (s/N): ").strip().lower()
                if response in ("s", "sim", "y", "yes"):
                    ignore = True
            except (EOFError, KeyboardInterrupt):
                ignore = False

        if ignore:
            print(f"\nGerado {output} ignorando {len(error_entries)} erro(s) ({compiled} mensagens compiladas com sucesso).")
            return 0

        output.unlink(missing_ok=True)
        return 1

    print(f"Compiled {compiled} messages into {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())