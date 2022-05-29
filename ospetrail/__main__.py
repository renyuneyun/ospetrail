#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''

'''

from argparse import ArgumentParser

from ospetrail import add_new_record

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('message', type=str,
                        help='The message you want to associate with.')
    args = parser.parse_args()
    add_new_record(args.message)
