#!/usr/bin/env python3

import sys
import string

class Rotation:
    digits = "0123456789"

    def __extendMap(self, letters):
        for position, ch in enumerate(letters):
            self.__char_map[ch] = (position, letters)

    def __init__(self):
        self.__char_map = {}
        self.__extendMap(string.ascii_uppercase)
        self.__extendMap(string.ascii_lowercase)
        self.__extendMap(self.digits)

    def __rotateCharacter(self, char, offset, decrypt):
        position, source = self.__char_map[char]
        source_length = len(source)
        if decrypt:
            offset = source_length - offset
        new_position = (position + offset) % source_length
        return source[new_position]

    def __transformCharacter(self, char, offset, decrypt):
        if char in self.__char_map:
            return self.__rotateCharacter(char, offset, decrypt)
        return char

    def isDigit(self, char):
        return char in self.digits

    def isChar(self, char):
        return char in string.ascii_lowercase or char in string.ascii_uppercase

    def rotate(self, text, char_offset, digit_offset = 0, decrypt = False):
        result = ""
        for char in text:
            offset = char_offset
            if self.isDigit(char):
                offset = digit_offset
            result += self.__transformCharacter(char, offset, decrypt)
        return result


    def __keyOffsets(self, key):
        while True:
            for char in key:
                position, source = self.__char_map[char]
                yield position

    def vigenereTransform(self, text, key, decrypt = False):
        result = ""
        offset_generator = self.__keyOffsets(key)
        for char in text:
            new_char = char
            if self.isChar(char):
                offset = next(offset_generator)
                new_char = self.__transformCharacter(char, offset, decrypt)
            result += new_char
        return result
