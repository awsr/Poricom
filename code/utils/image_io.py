"""
Poricom Image Processing Utility

Copyright (C) `2021-2022` `<Alarcon Ace Belen>`

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from io import BytesIO
from os.path import splitext, basename
from pathlib import Path

from PyQt5.QtCore import QBuffer
from PyQt5.QtGui import QGuiApplication
from tesserocr import PyTessBaseAPI
from PIL import Image
import zipfile
import rarfile
import pdf2image

from utils.config import config
from TextHandler import (formatter)


def mangaFileToImageDir(filepath):
    extractPath, extension = splitext(filepath)
    cachePath = f"./poricom_cache/{basename(extractPath)}"

    if extension in [".cbz", ".zip"]:
        with zipfile.ZipFile(filepath, 'r') as zipRef:
            zipRef.extractall(cachePath)

    rarfile.UNRAR_TOOL = "utils/unrar.exe"
    if extension in [".cbr", ".rar"]:
        with rarfile.RarFile(filepath) as zipRef:
            zipRef.extractall(cachePath)

    if extension in [".pdf"]:
        try:
            images = pdf2image.convert_from_path(filepath)
        except pdf2image.exceptions.PDFInfoNotInstalledError:
            images = pdf2image.convert_from_path(
                filepath, poppler_path="poppler/Library/bin")
        for i, image in enumerate(images):
            filename = basename(extractPath)
            Path(cachePath).mkdir(parents=True, exist_ok=True)
            image.save(
                f"{cachePath}/{i+1}_{filename}.png", 'PNG')

    return cachePath


def pixboxToText(pixmap, lang="jpn_vert", model=None):

    buffer = QBuffer()
    buffer.open(QBuffer.ReadWrite)
    pixmap.save(buffer, "PNG")
    byte_data = BytesIO(buffer.data())

    if byte_data.getbuffer().nbytes == 0:
        return

    pillowImage = Image.open(byte_data)
    text = ""

    if model is not None:
        text = model(pillowImage)

    # PSM = 1 works most of the time except on smaller bounding boxes.
    # By smaller, we mean textboxes with less text. Usually these
    # boxes have at most one vertical line of text.
    else:
        with PyTessBaseAPI(path=config["LANG_PATH"], lang=lang, oem=1, psm=1) as api:
            api.SetImage(pillowImage)
            text = api.GetUTF8Text()

    return formatter.process(text.strip())


def logText(text, mode=False, path="."):
    clipboard = QGuiApplication.clipboard()
    clipboard.setText(text)

    if mode:
        with open(path, 'a', encoding="utf-8") as fh:
            fh.write(text + "\n")
