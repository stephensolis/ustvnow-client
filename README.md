# ustvnow-client

[![Build Status](https://travis-ci.org/stephensolis/ustvnow-client.svg?branch=master)](https://travis-ci.org/stephensolis/ustvnow-client)

A simple, unofficial, command-line client for [USTVnow](https://www.ustvnow.com/).

Just run `pip install -r requirements.txt` to setup, then `python ustvnow.py`, or try (for example) `python ustvnow.py -u <email> -p <password> -c wgal -q 2383872`.

## Requirements

- A [USTVnow](https://www.ustvnow.com/) account ([sign up here](https://watch.ustvnow.com/subscription/free-channels))
- Something capable of playing [HLS/M3U](https://en.wikipedia.org/wiki/HTTP_Live_Streaming) streams (like [VLC](https://www.videolan.org/vlc/) or [PotPlayer](http://potplayer.daum.net/))

## Usage

	usage: ustvnow.py [-h] [-u USERNAME] [-p PASSWORD] [-c CHANNEL] [-q QUALITY]
	                  [-d] [-o OUTPUT_FILENAME] [-v]

	A simple command-line client for USTVnow.

	optional arguments:
	  -h, --help            show this help message and exit
	  -u USERNAME, --username USERNAME
	                        USTVnow username (email address)
	  -p PASSWORD, --password PASSWORD
	                        USTVnow password
	  -c CHANNEL, --channel CHANNEL
	                        channel code (run without this argument to see a list)
	  -q QUALITY, --quality QUALITY
	                        channel bitrate (run without this argument to see a
	                        list)
	  -d, --download-only   just download the m3u8 file for the channel without
	                        playing
	  -o OUTPUT_FILENAME, --output-filename OUTPUT_FILENAME
	                        override the output m3u8 filename
	  -v, --verbose         show some debugging information

## Disclaimer

This is not endorsed by or affiliated with USTVnow or DutchPhone Holdings Inc. in any way, shape or form. USTVnow is a trademark or registered trademark of DutchPhone Holdings Inc., © 2010-2015 USTVnow, All Rights Reserved.

## License ![License](http://img.shields.io/:license-mit-blue.svg)

    The MIT License (MIT)

    Copyright (c) 2017 Stephen

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
