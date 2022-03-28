import argparse
import sys
import json
from collections import defaultdict


def caesar(data, key):
    res = ''
    for i in range(len(data)):
        c = data[i]
        if c in "0123456789 -.,;:!?\n\t":
            res += c
        elif c.isupper():
            res += chr((ord(c) + key-65) % 26 + 65)
        else:
            res += chr((ord(c) + key-97) % 26 + 97)
    return res

def vigenere(data, key, cmd):
    row = [chr(x) for x in range(65, 91)]
    row.extend([chr(x) for x in range(97, 123)])

    data_code = []
    key_code = []
    for c in key:
        key_code.append(row.index(c))
    it = 0
    for c in data:
        if c in "0123456789 -.,;:!?\n\t":
            data_code.append((c, -1))
        else:
            data_code.append((row.index(c), key_code[it]))
            it+=1
        if it >= len(key):
            it = 0
    cip = ''
    for c, k in data_code:
        if k < 0:
            cip+=c
        else:
            if cmd == 'encode':
                cip+=row[(c+k) % len(row)]
            elif cmd == 'decode':
                cip+=row[(c-k+len(row) % len(row))]
    return cip

def encode_decode(args):
    # get text to encode/decode
    if args.input_file:
        f = open(args.input_file,'r')
        data = f.read()
        f.close()
    else:
        data = input()
    # call cipher/decode function
    res = ''
    if args.cipher == 'caesar':
        if args.cmd == 'encode':
            res = caesar(data, int(args.key)) # caesar encode call
        else:
            res = caesar(data, int(args.key)*-1) # caesar decode call
    elif args.cipher == 'vigenere':
        res = vigenere(data, args.key, args.cmd) # vigenere encode/decode call

    # write or print encoded/decoded text
    if args.output_file:
        f2 = open(args.output_file, 'w')
        f2.write(res)
        f2.close()
    else:
        print(res)

def get_hist(data):
    dic = {}
    l = 0
    for c in data:
        if c.isalpha():
            c = c.lower()
            if c in dic.keys():
                dic[c]+=1
            else:
                dic[c]=1
            l+=1
    for k, v in dic.items():
        dic[k] = v/l
    return dic

def train(args):
    # get text to analyse
    if args.text_file:
        f = open(args.text_file,'r')
        data = f.read()
        f.close()
    else:
        data = input()
    # make histogram
    dic = get_hist(data)
    # write histogram to file as json
    f2 = open(args.model_file, 'w')
    f2.write(json.dumps(dic))
    f2.close()

def hack(args):
    # get text to hack
    if args.input_file:
        f = open(args.input_file,'r')
        data = f.read()
        f.close()
    else:
        data = input()
    # get model
    f2 = open(args.model_file,'r')
    model = json.load(f2)
    f2.close()
    model = defaultdict(float, model)
    # hacking
    difs = []
    for i in range(0, 26):
        t = caesar(data, i)
        h = get_hist(t)
        h = defaultdict(float, h)
        #calc dif
        sum = 0
        for k in model.keys():
            sum+=pow(model[k]-h[k], 2)
        difs.append(sum)
    key = difs.index(min(difs))
    hacked = caesar(data, key)
    # write or print hacked text
    if args.output_file:
        f3 = open(args.output_file, 'w')
        f3.write(hacked)
        f3.close()
    else:
        print(hacked)

if __name__ == "__main__":
    cmd = sys.argv[1]
    parser = argparse.ArgumentParser()

    parser.add_argument('cmd', type=str)
    #args = parser.parse_args()

    if cmd == 'encode' or cmd == 'decode':
        # handle arguments parsing for encode and decode
        parser.add_argument('--cipher', type=str, required=True)
        parser.add_argument('--key', required=True)
        parser.add_argument('--input-file', type=str)
        parser.add_argument('--output-file', type=str)
        args = parser.parse_args()
        # check vaild arguments
        if args.cipher != 'caesar' and args.cipher != 'vigenere':
            raise ValueError("cipher can only be caesar or vigenere")
        if args.cipher == 'caesar':
            if not args.key.isnumeric():
                raise ValueError("for caesar key should be an int")
        else:
            if not isinstance(args.key, str):
                raise ValueError("for vigenere key should be a str")
        # call function
        encode_decode(args)
    elif cmd == 'train':
        # handle arguments parsing for train
        parser.add_argument('--text-file', type=str)
        parser.add_argument('--model-file', type=str, required=True)
        args = parser.parse_args()
        train(args)
    elif cmd == 'hack':
        # handle arguments parsing for hack
        parser.add_argument('--input-file', type=str)
        parser.add_argument('--output-file', type=str)
        parser.add_argument('--model-file', type=str, required=True)
        args = parser.parse_args()
        hack(args)