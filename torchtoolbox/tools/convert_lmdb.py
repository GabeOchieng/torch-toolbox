# -*- coding: utf-8 -*-
# @Author  : DevinYang(pistonyang@gmail.com)
import lmdb
import os
import pyarrow
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm


# parser = argparse.ArgumentParser(description='Convert a ImageFolder dataset to LMDB format.')
# parser.add_argument('--data-dir', type=str, required=True,
#                     help='ImageFolder path, this param will give to ImageFolder Dataset.')
# parser.add_argument('--save-dir', type=str, required=True,
#                     help='Save dir.')
# parser.add_argument('--name', type=str, required=True,
#                     help='Save file name, need not to add `.lmdb`')
# parser.add_argument('-j', dest='num_workers', type=int, default=0)
# parser.add_argument('--write-frequency', type=int, default=5000)
# parser.add_argument('--max-size', type=float, default=1.0,
#                     help='Maximum size database, this is a rate, default is 1T, final setting would be '
#                          '1T * `this param`')

# args = parser.parse_args()


def get_key(index):
    return u'{}'.format(index).encode('ascii')


def raw_reader(path):
    with open(path, 'rb') as f:
        bin_data = f.read()
    return bin_data


def dumps_pyarrow(obj):
    return pyarrow.serialize(obj).to_buffer()


def load_pyarrow(buf):
    return pyarrow.deserialize(buf)


def generate_lmdb_dataset(data_set: Dataset, save_dir: str, name: str,
                          num_workers=0, max_size_rate=1.0, write_frequency=5000):
    data_loader = DataLoader(data_set, num_workers=num_workers, collate_fn=lambda x: x)
    num_samples = len(data_set)

    lmdb_path = os.path.join(save_dir, '{}.lmdb'.format(name))
    isdir = os.path.isdir(lmdb_path)
    db = lmdb.open(lmdb_path, subdir=isdir,
                   map_size=int(1099511627776 * max_size_rate),
                   readonly=False, meminit=True, map_async=True)
    txn = db.begin(write=True)
    for idx, data in enumerate(tqdm(data_loader)):
        txn.put(get_key(idx), dumps_pyarrow(data[0]))
        if idx % write_frequency == 0 and idx > 0:
            txn.commit()
            txn = db.begin(write=True)
    txn.put(b'__len__', dumps_pyarrow(num_samples))
    txn.commit()
    db.sync()
    db.close()
