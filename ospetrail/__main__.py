#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''

'''

from argparse import ArgumentParser

import ospetrail as app

if __name__ == "__main__":
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', title='sub-commands')
    parser_add = subparsers.add_parser('add', help='Add new record')
    parser_list = subparsers.add_parser('list', help='List existing records')
    parser_add.add_argument('message', type=str,
                            help='The message you want to associate with.')
    args = parser.parse_args()
    if args.command == 'add':
        app.add_new_record(args.message)
    elif args.command == 'list':
        app.list_records()

