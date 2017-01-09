#!/usr/bin/env python

from __future__ import print_function, division, unicode_literals
try:
    input = raw_input
except NameError:
    pass

from collections import defaultdict

import m3u8
import requests


###################
# USTVnow API calls
###################

def get_auth_token(username, password, include_resp=False):
    params = {
        'username': username,
        'password': password,
        'device': 'gtv',
        'redir': '0'
    }
    resp = requests.get('https://m.ustvnow.com/gtv/1/live/login',
                        params=params)
    resp.raise_for_status()

    try:
        token = resp.json()['token']
        if not token:
            raise RuntimeError('No token was returned')
    except Exception as e:
        setattr(e, 'response', resp)
        raise e
    return (token, resp) if include_resp else token


def get_channel_list(auth_token, include_resp=False):
    params = {
        'token': auth_token
    }
    resp = requests.get('https://m.ustvnow.com/gtv/1/live/listchannels',
                        params=params)
    resp.raise_for_status()

    try:
        channels = [{
            'name': channel['sname'],
            'img': 'https://m.ustvnow.com/' + channel['img'],
            'code': channel['scode'],
            'callsign': channel['callsign'],
            'available': bool(channel['t'])
        } for channel in resp.json()['results']['streamnames']]
    except Exception as e:
        setattr(e, 'response', resp)
        raise e
    return (channels, resp) if include_resp else channels


def get_channel_playlist_url(auth_token, channel_code, include_resp=False):
    params = {
        'token': auth_token,
        'scode': channel_code
    }
    resp = requests.get('https://m.ustvnow.com/stream/1/live/view',
                        params=params)
    resp.raise_for_status()

    try:
        url = resp.json()['stream']
    except Exception as e:
        setattr(e, 'response', resp)
        raise e
    return (url, resp) if include_resp else url


###############################
# M3U8 playlist-related helpers
###############################

def get_playlist(url, include_resp=False):
    resp = requests.get(url)
    resp.raise_for_status()

    try:
        playlist = m3u8.loads(resp.text)
    except Exception as e:
        setattr(e, 'response', resp)
        raise e
    return (playlist, resp) if include_resp else playlist


def group_playlists_by_quality(playlist):
    qualities = defaultdict(list)

    for p in playlist.playlists:
        qualities[p.stream_info].append(p)

    return qualities


def make_playlist(stream_playlists):
    playlist = m3u8.M3U8()

    for p in stream_playlists:
        playlist.add_playlist(p)

    return playlist.dumps()


#####
# CLI
#####

if __name__ == '__main__':
    import argparse
    from getpass import getpass
    import os
    from pprint import pformat
    import subprocess
    import sys

    from codec_names import codec_names

    def indent(str, columns):
        return '\n'.join(' '*columns + line for line in str.splitlines())

    def format_si(num):
        for unit in ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024:
                return '{:3.1f}{}'.format(num, unit)
            num /= 1024
        return '{:.1f}{}'.format(num, 'Y')

    def describe_codecs(codecs_str):
        descriptions = []
        for c in codecs_str.split(','):
            c = c.strip().lower()
            if c in codec_names:
                descriptions.append(codec_names[c])
            else:
                descriptions.append('Unknown Codec ({})'.format(c))
        return ', '.join(descriptions)

    def prompt_number(min, max):
        while True:
            num = input('({}-{}): '.format(min, max))
            try:
                num = int(num)
                if num >= min and num <= max:
                    return num
                else:
                    raise ValueError()
            except ValueError:
                print('Invalid selection. ', end='')

    def prompt_yes_no():
        while True:
            val = input('(Y/N): ').lower()
            if val == 'y':
                return True
            elif val == 'n':
                return False
            else:
                print('Invalid selection. ', end='')

    def prompt_username_password(username, password):
        if not username or not password:
            print('[i] Enter your USTVnow login credentials:')

            if username:
                print(indent('Using username {}'.format(username), 6))
            while not username:
                username = input(indent('Username: ', 6))

            if password:
                print(indent('Using password from arguments', 6))
            while not password:
                password = getpass(str(indent('Password: ', 6)))
        return (username, password)

    def prompt_channel_code(channel_list, channel_code):
        if channel_code is not None:
            try:
                channel = next(channel for channel in channel_list
                               if channel['code'] == channel_code)
                if channel['available']:
                    return channel_code
                else:
                    print("[!] Channel '{}' exists but is marked as "
                          "unavailable. Use anyway? "
                          .format(channel_code), end='')
                    if prompt_yes_no():
                        return channel_code
            except StopIteration:
                print("[!] Unknown channel '{}'.".format(channel_code))

        available_channels = [channel for channel in channel_list
                              if channel['available']]
        print('[i] Select a channel:')
        for i, channel in enumerate(available_channels):
            print(indent('{}) {}: {} ({})'
                         .format(i + 1, channel['code'], channel['name'],
                                 channel['callsign']), 6))
        print('    ', end='')
        channel_num = prompt_number(1, len(available_channels))
        return available_channels[channel_num - 1]['code']

    def prompt_channel_bitrate(qualities, bitrate):
        if bitrate is not None:
            if any(quality.bandwidth == bitrate for quality in qualities):
                return bitrate
            else:
                print('[!] Channel bitrate {} does not exist.'
                      .format(bitrate))

        qualities.sort(key=lambda quality: quality.bandwidth, reverse=True)
        print('[i] Select desired quality:')
        for i, quality in enumerate(qualities):
            print(indent('{}) {}: {}x{}, {}bps, codecs: {}'
                         .format(i + 1, quality.bandwidth,
                                 quality.resolution[0], quality.resolution[1],
                                 format_si(quality.bandwidth),
                                 describe_codecs(quality.codecs)), 6))
        print('    ', end='')
        quality_num = prompt_number(1, len(qualities))
        return qualities[quality_num - 1].bandwidth

    def prompt_filename_if_needed(filename):
        if os.path.isfile(filename):
            print("[!] File '{}' already exists, overwrite? "
                  .format(filename), end='')
            if not prompt_yes_no():
                filename = ''
                while not filename:
                    filename = input('[i] Enter new filename: ').strip()
        return filename

    def format_request(req):
        head = '{} {}\n{}'.format(
            req.method, req.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items())
        )
        return (head + '\n\n{}'.format(req.body)) if req.body else head

    def format_response(resp):
        head = '{} {}\n{}'.format(
            resp.status_code, resp.reason,
            '\n'.join('{}: {}'.format(k, v) for k, v in resp.headers.items())
        )
        return (head + '\n\n{}'.format(resp.text)) if resp.text else head

    def format_playlist_qualities(playlists_by_quality):
        output = ''
        for quality in playlists_by_quality:
            output += str(quality) + '\n'
            for playlist in playlists_by_quality[quality]:
                output += indent('- ' + playlist.uri, 2) + '\n'
        return output

    def print_request_response(resp):
        print('[*] Sent request:')
        print(indent(format_request(resp.request), 6))
        print('[*] Received response:')
        print(indent(format_response(resp), 6))

    def make_api_request(api_func, *params):
        try:
            (value, resp) = api_func(*params, include_resp=True)
        except Exception as e:
            print('failed.')
            print('[!] Error: {}.'.format(e))
            print_request_response(e.response)
            sys.exit(1)
        print('done.')
        if args.verbose:
            print_request_response(resp)
        return value

    def open_with_default_program(filename):
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', filename))
        elif os.name == 'nt':
            os.startfile(filename)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', filename))

    #
    # read command-line arguments
    #

    parser = argparse.ArgumentParser(description='A simple command-line '
                                                 'client for USTVnow.')
    parser.add_argument('-u', '--username',
                        help='USTVnow username (email address)')
    parser.add_argument('-p', '--password', help='USTVnow password')
    parser.add_argument('-c', '--channel',
                        help='channel code '
                             '(run without this argument to see a list)')
    parser.add_argument('-q', '--quality', type=int,
                        help='channel bitrate '
                             '(run without this argument to see a list)')
    parser.add_argument('-d', '--download-only', action='store_true',
                        help='just download the m3u8 file for the channel '
                             'without playing')
    parser.add_argument('-o', '--output-filename',
                        help='override the output m3u8 filename')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show some debugging information')
    args = parser.parse_args()

    #
    # login, get token
    #

    (username, password) = prompt_username_password(args.username,
                                                    args.password)

    print('[+] Logging in... ', end='')
    token = make_api_request(get_auth_token, username, password)
    if args.verbose:
        print('[*] Got token: {}'.format(token))

    #
    # get channel list
    #

    print('[+] Retrieving channel list... ', end='')
    channel_list = make_api_request(get_channel_list, token)
    num_avail_channels = sum(channel['available'] for channel in channel_list)
    if args.verbose:
        print('[*] Got channel data ({} available, {} total):'
              .format(num_avail_channels, len(channel_list)))
        print(indent(pformat(channel_list), 6))
    else:
        print('[*] Got {} available channels ({} total).'
              .format(num_avail_channels, len(channel_list)))

    #
    # select channel, get playlist data
    #

    channel_code = prompt_channel_code(channel_list, args.channel)

    print('[+] Retrieving channel playlist URL... ', end='')
    playlist_url = make_api_request(get_channel_playlist_url, token,
                                    channel_code)
    if args.verbose:
        print('[*] Got playlist URL (for channel {}): {}'
              .format(channel_code, playlist_url))

    print('[+] Retrieving channel playlist... ', end='')
    playlist = make_api_request(get_playlist, playlist_url)
    playlists_by_quality = group_playlists_by_quality(playlist)
    if args.verbose:
        print('[*] Got playlists by quality (for channel {}):'
              .format(channel_code))
        print(indent(format_playlist_qualities(playlists_by_quality), 6))

    #
    # select playlists, create m3u8 file
    #

    selected_bitrate = prompt_channel_bitrate(list(playlists_by_quality
                                                   .keys()), args.quality)
    selected_playlists = next(playlists_by_quality[quality]
                              for quality in playlists_by_quality
                              if quality.bandwidth == selected_bitrate)

    output_data = make_playlist(selected_playlists)
    if args.verbose:
        print('[*] Created output m3u8 data:')
        print(indent(output_data, 6))

    default_filename = '{}_{}.m3u8'.format(channel_code, selected_bitrate)
    output_filename = prompt_filename_if_needed(args.output_filename or
                                                default_filename)
    with open(output_filename, 'wb') as f:
        f.write(output_data.encode('utf-8'))
    print("[+] Wrote channel playlist as '{}'.".format(output_filename))

    #
    # play output file
    #

    if not args.download_only:
        print("[+] Opening '{}'... ".format(output_filename), end='')
        open_with_default_program(output_filename)
        print('done.')
