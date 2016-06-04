#!/usr/bin/env python
"""
Migrate data from WTS to PWTS

NOTE: must source ../Configuration before use
"""

import argparse


def parseArgs():
    """
    Return script arguments
    """
    parser = argparse.ArgumentParser(description='Migrate WTS data to PWTS database')
    parser.add_argument('source_wts_server', help='wts server')
    parser.add_argument('source_wts_db', help='wts dbname')
    parser.add_argument('target_server', help='pwts server')
    parser.add_argument('target_pwts_db', help='pwts dbname')
    parser.add_argument('-k','--key', nargs="?", help='migrate single _tr_key')

    args = parser.parse_args()
    return args

def migrateWTS(
    source_server,
    source_dbname,
    target_server,
    target_dbname,
    _tr_key = None
    ):
    """
    Migrates data from source_server:source_dbname
	to target_server:target_dbname
    
    Optional: migrate only _tr_key
    """

    print "source server = %s" % source_server
    print "source dbname = %s" % source_dbname
    print "target server = %s" % target_server
    print "target dbname = %s" % target_dbname
    if _tr_key:
        print "_tr_key = %s" % _tr_key


if __name__ == "__main__":
    args = parseArgs() 

    migrateWTS(
      source_server=args.source_wts_server,
      source_dbname=args.source_wts_db,
      target_server=args.target_server,
      target_dbname=args.target_pwts_db,
      _tr_key = args.key
    )
