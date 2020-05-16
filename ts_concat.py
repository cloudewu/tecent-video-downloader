import glob
import os.path
import argparse

def concat_files(filenames, output_file):
    if os.path.exists(output_file):
        print('[ WARNING ] Overwriting existing file: ', output_file)
    
    print('[ INFO ] merging {} files...'.format(len(filenames)))
    output = open(output_file, 'wb+')
    for name in filenames:
        print('\t', name)
        with open(name, 'rb') as f:
            output.write(f.read())
    print('[ INFO ] Finished. Merged file: ', output_file)
    return

def concat_all(work_dir='.', pattern='*.ts', output_file='merge.ts'):
    from glob import glob
    filenames = glob(os.path.join(work_dir, pattern))
    concat_files(filenames, os.path.join(work_dir, output_file))
    return

if __name__=='__main__':
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('work_dir', nargs=1, default='.', type=str)
        parser.add_argument('-o', '--output', nargs='?', default='merge.ts', type=str)
        args = parser.parse_args()
        return args.work_dir[0], args.output
    
    work_dir, output = parse_args()
    concat_all(work_dir, output_file=output)
