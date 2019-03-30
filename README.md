# ustvnow-client

**This client no longer works because of changes to ustvnow.com**

The project is currently unmaintained but please feel free to fork!

![Unmaintained](https://img.shields.io/badge/project-unmaintained-red.svg)
[![Travis](https://travis-ci.org/stephensolis/ustvnow-client.svg?branch=master)](https://travis-ci.org/stephensolis/ustvnow-client)
[![Codacy](https://api.codacy.com/project/badge/Grade/2c282b2727354d809f47f2d3b085387f)](https://www.codacy.com/app/stephensolis/ustvnow-client)
[![Codebeat](https://codebeat.co/badges/636662a6-916d-4d8f-a7da-3298a58ca426)](https://codebeat.co/projects/github-com-stephensolis-ustvnow-client-master)
[![CodeClimate](https://api.codeclimate.com/v1/badges/937226aa5b7a8dab2717/maintainability)](https://codeclimate.com/github/stephensolis/ustvnow-client/maintainability)

A simple, unofficial, command-line client for [USTVnow](https://www.ustvnow.com/).

Just run `pip install -r requirements.txt` to setup, then `python ustvnow.py`, or try (for example) `python ustvnow.py -u <email> -p <password> -c wgal -q highest`.

## Requirements

- A [USTVnow](https://www.ustvnow.com/) account ([sign up here](https://watch.ustvnow.com/subscription/free-channels))
- Something capable of playing [HLS/M3U](https://en.wikipedia.org/wiki/HTTP_Live_Streaming) streams (like [VLC](https://www.videolan.org/vlc/) or [PotPlayer](http://potplayer.daum.net/))

Note: USTVnow blocks the default VLC user-agent string. Try using `--download-only` and running VLC with this argument:

```
:http-user-agent="AppleCoreMedia/1.0.0.8C148 (iPad; U; CPU OS 4_2_1 like Mac OS X; en_us)"
```

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
	                        channel bitrate in bps (run without this argument to
	                        see a list, or use 'highest' to use the highest-
	                        bitrate stream available)
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
