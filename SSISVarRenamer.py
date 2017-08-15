import argparse
import SSIS


argparser = argparse.ArgumentParser(prog='SSISVarRenamer',description='Rename,Delete variables in *.dtsx files')
argparser.add_argument('path',nargs='?', help='Path to SSIS project')
# argparser.add_argument('action',choices=['rename','delete'], help='Action to do with variable')
subparser = argparser.add_subparsers()

parserRename = subparser.add_parser('rename', help = 'rename help')
parserRename.add_argument('FromName', nargs='?', help = 'Variable old name')
parserRename.add_argument('ToName', nargs='?', help = 'Variable new name')

parserDelete = subparser.add_parser('delete', help = 'rename help')
parserDelete.add_argument('Name', nargs='?', help = 'Variable name')

args = argparser.parse_args()

#print(args)

SSISProj = SSIS.SSIS(args.path)

try:
    if args.FromName != None and args.ToName != None:
        SSISProj.renameVar(args.FromName,args.ToName)
    else:
        print('From and To Name not setted!')
except Exception:
    try:
        if args.Name != None:
            raise NotImplementedError
        else:
            raise NotImplementedError
    except NotImplementedError:
        print('Not implemented')



# for file in files:


