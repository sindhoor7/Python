#!/usr/bin/python
'''
Python Version - 2.7
OS- RHEL71
'''

import platform
import datetime
import subprocess


def take_action(action, src, dest, logdir, srd):
    # INSTALL process
    if action.lower() == 'install':
        # Check if paths are valid
        if not os.path.exists(src + "/repository.config"):
            print(src + "/repository.config not found. Please check the Installable Dir "
                        "to make sure repository.config exits ")
        elif logdir:
            if not os.path.exists(logdir):
                if not os.listdir(logdir):
                    os.makedirs(logdir)

            logfile = platform.node() + "_ibmim_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".xml"
            if logdir:
                logfile = logdir + '/' + logfile
            cmd = src + '/tools/imcl com.ibm.cic.agent -repositories ' \
                  + src + '/repository.config -acceptLicense -accessRights nonAdmin -log ' \
                  + logfile + ' -silent -sVP -installationDirectory ' + dest + ' -sharedResourcesDirectory ' \
                  + srd
            child = subprocess.Popen([cmd], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            if child.returncode != 0:
                print('IBM IM installation failed. Please find the more information at ' + logfile)
            elif child.returncode == 0:
                print("IBM IM installed successfully.")

    # UNINSTALL process
    elif action.lower() == 'uninstall':
        # TODO: implementation of uninstall process
        print('Uninstalling  IIM is not supported yet with this tool. '
              'Consider upgrading to the newer version of the utility if available.')


import ConfigParser
import sys
import os


def start():
    iim_config = ConfigParser.ConfigParser()
    try:
        cfg_file = sys.argv[1]
        if cfg_file != 'generateConfig':
            iim_config.read(cfg_file)
            if os.path.exists(cfg_file):
                action = iim_config.get('InstallationManager', 'Action')
                src = iim_config.get('InstallationManager', 'InstallableDir')
                dest = iim_config.get('InstallationManager', 'InstallationDir')
                logdir = iim_config.get('InstallationManager', 'LogDir')
                srd = iim_config.get('InstallationManager', 'SharedResourcesDir')
                if action and src:
                    if dest is None:
                        dest = '/opt/IBM/InstallationManager'
                    if not srd:
                        srd = '/opt/IBM/IMShared'
                    take_action(action, src, dest, logdir, srd)

                else:
                    print('Action and InstallableDir are required values... Please modify cfg file and try again.')
            else:
                print('Config file cannot be found at the path specified. To generate a config file, use - '
                      'InstallationManager.py generateConfig')
        else:
            fo = open('IIM.cfg', 'w')
            fo.write('[InstallationManager]\n'
                     'Action = Install\n'
                     'InstallableDir = \n'
                     'InstallationDir = /opt/IBM/InstallationManager\n'
                     'LogDir = \n'
                     'SharedResourcesDir = /opt/IBM/IMShared')
            print('IIM.cfg generated successfully.')
            fo.close()

    except IndexError:
        print('Usage: InstallationManager.py CFG_FILE')
        print('To generate a config file, use - InstallationManager.py generateConfig')

if __name__ == '__main__':
    start()
