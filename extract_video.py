import json
import os
import urllib.parse
import urllib.request

def ensure_exist(dir_name):
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    return

def get_meta(metafile, work_dir, debugging=False):
    with open(metafile, 'r') as f:
        meta = json.load(f)
    meta_url = urllib.parse.unquote(meta['vurl'])

    if debugging:
        print('[ DEBUG ] raw request URL:\n         ', meta_url)
    
    request_url = meta_url.split('?', 1)[0]
    request_url, meta_name = request_url.rsplit('/', 1)
    request_url = request_url + '/'

    print('[ INFO ] get request URL:\n        ', request_url)
    print('[ INFO ] get metafile name: ', meta_name)
    
    ensure_exist(work_dir)
    meta_path = os.path.join(work_dir, meta_name)
    if not os.path.exists(meta_path):
        print('[ INFO ] meta file not found. Automatically downloading...')
        urllib.request.urlretrieve(meta_url, meta_path)
        print('[ INFO ] meta file downloaded: ', meta_path)
    return request_url, meta_name

def get_param_list(metafile, work_dir, debugging=False):
    ensure_exist(work_dir)
    filepath = os.path.join(work_dir, metafile)
    param_list = []
    with open(filepath, 'r') as f:
        while True:
            s = f.readline()
            if 'ENDLIST' in s:
                break
            if s[:7] == '#EXTINF':
                param_list.append(f.readline()[:-1])
    return param_list

def download(metafile, work_dir, offset=0, debugging=False):
    print("[ INFO ] Getting video information...")
    request_url, info_file = get_meta(metafile, work_dir, debugging=debugging)
    print("[ INFO ] parsing request parameters...")
    param_list = get_param_list(info_file, work_dir, debugging=debugging)
    print("[ INFO ] start to download video segments... (#files={})".format(len(param_list)-offset))
    for idx, param in enumerate(param_list[offset:]):
        print('        ', param)
        urllib.request.urlretrieve (request_url+param, os.path.join(work_dir, "{:03}.ts".format(offset+idx)))

if __name__=='__main__':
    # parse arguments
    import argparse
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('meta', type=str, metavar='metafile', help='metafile storing segment info')
        parser.add_argument('-d', '--work_dir', nargs='?', type=str, default='videos', help='location of downloaded .ts files ')
        parser.add_argument('--offset', type=int, default=0, help='start downloading from the offset-th segment file')
        parser.add_argument('-m', '--merge', action='store_true', help='merge downloaded .ts files')
        parser.add_argument('--debug', action='store_true', help='debug mode')
        return parser.parse_args()
    args = parse_args()

    download(args.meta, args.work_dir, offset=args.offset, debugging=args.debug)

    if args.merge:
        import ts_concat
        ts_concat.concat_all(args.work_dir, '*.ts')
    