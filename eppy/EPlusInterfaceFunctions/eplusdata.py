"""Legacy code from EPlusInterface"""
# EPlusInterface (EPI) - An interface for EnergyPlus
# Copyright (C) 2004 Santosh Philip

# This file is part of EPlusInterface.
#
# EPlusInterface is free software; you can redistribute it and/or modify
# the Free Software Foundation; either version 2 of the License, or
#
# EPlusInterface is distributed in the hope that it will be useful,
#
# along with EPlusInterface; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


# Santosh Philip, the author of EPlusInterface, can be contacted at the following email address:
# santosh_philip AT yahoo DOT com
# Please send all bug reports, enhancement proposals, questions and comments to that address.
#
# VERSION: 0.004
#last update 21 Apr 2004


#this is a test version ... not for real use
#dammit i am using it

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy



import eppy.EPlusInterfaceFunctions.mylib3 as mylib3
import eppy.EPlusInterfaceFunctions.mylib2 as mylib2



def removecomment(astr, cphrase):
    """
    the comment is similar to that in python.
    any charachter after the # is treated as a comment
    until the end of the line
    astr is the string to be de-commented
    cphrase is the comment phrase"""
    linesep = mylib3.getlinesep(astr)
    alist = astr.split(linesep)
    for i in range(len(alist)):
        alist1 = alist[i].split(cphrase)
        alist[i] = alist1[0]

    # return string.join(alist, linesep)
    return linesep.join(alist)


class Idd(object):
    """Idd object"""
    def __init__(self, dictfile, version=2):
        if version == 2:
            # version == 2. This is a just a flag I am using
            # it may wind up being the only type... then I can clean this up
            # and not use the other option
            self.dt, self.dtls = self.initdict2(dictfile)
            return
        self.dt, self.dtls = self.initdict(dictfile)
    def initdict2(self, dictfile):
        """initdict2"""
        dt = {}
        dtls = []
        adict = dictfile
        for element in adict:
            dt[element[0].upper()] = [] #dict keys for objects always in caps
            dtls.append(element[0].upper())
        return dt, dtls

    def initdict(self, fname):
        """initdict"""
        astr = mylib2.readfile(fname)
        nocom = removecomment(astr, '!')
        idfst = nocom
        alist = idfst.split(';')
        lss = []
        for element in alist:
            lst = element.split(',')
            lss.append(lst)

        for i in range(0, len(lss)):
            for j in range(0, len(lss[i])):
                lss[i][j] = lss[i][j].strip()

        dt = {}
        dtls = []
        for element in lss:
            if element[0] == '':
                continue
            dt[element[0].upper()] = []
            dtls.append(element[0].upper())

        return dt, dtls



class Eplusdata(object):
    """Eplusdata"""
    def __init__(self, dictfile=None, fname=None):
        # import pdb; pdb.set_trace()
        if fname == None and dictfile == None:
            self.dt, self.dtls = {}, []
        if isinstance(dictfile, str) and fname == None:
            self.initdict(dictfile)
        if isinstance(dictfile, Idd) and fname == None:
            self.initdict(dictfile)
        if isinstance(fname, str) and isinstance(dictfile, str):
            fnamefobject = open(fname, 'rb')
            self.makedict(dictfile, fnamefobject)
        if isinstance(fname, str) and isinstance(dictfile, Idd):
            fnamefobject = open(fname, 'rb')
            self.makedict(dictfile, fnamefobject)
        from StringIO import StringIO
        try:
            # will fial in python3 because of file
            if isinstance(
                    fname, (file, StringIO)) and isinstance(dictfile, str):
                self.makedict(dictfile, fname)
            if isinstance(
                    fname, (file, StringIO)) and isinstance(dictfile, Idd):
                self.makedict(dictfile, fname)
        except NameError:
            from io import IOBase
            if isinstance(
                    fname, (IOBase, StringIO)) and isinstance(dictfile, str):
                self.makedict(dictfile, fname)
            if isinstance(
                    fname, (IOBase, StringIO)) and isinstance(dictfile, Idd):
                self.makedict(dictfile, fname)

    def __repr__(self):
        #print dictionary
        dt = self.dt
        dtls = self.dtls
        DOSSEP = mylib3.UNIXSEP # using a unix EOL
        astr = ''
        for node in dtls:
            nodedata = dt[node.upper()]
            for block in nodedata:
                for i in range(len(block)):
                    fformat = '     %s,'+ DOSSEP
                    if i == 0:
                        fformat = '%s,'+ DOSSEP
                    if i == len(block)-1:
                        fformat = '     %s;'+ DOSSEP*2
                    astr = astr+ fformat %block[i]

        return astr

    #------------------------------------------
    def initdict(self, fname):
        """create a blank dictionary"""
        if isinstance(fname, Idd):
            self.dt, self.dtls = fname.dt, fname.dtls
            return self.dt, self.dtls

        astr = mylib2.readfile(fname)
        nocom = removecomment(astr, '!')
        idfst = nocom
        alist = idfst.split(';')
        lss = []
        for element in alist:
            lst = element.split(',')
            lss.append(lst)

        for i in range(0, len(lss)):
            for j in range(0, len(lss[i])):
                lss[i][j] = lss[i][j].strip()

        dt = {}
        dtls = []
        for element in lss:
            if element[0] == '':
                continue
            dt[element[0].upper()] = []
            dtls.append(element[0].upper())

        self.dt, self.dtls = dt, dtls
        return dt, dtls

    #------------------------------------------
    def makedict(self, dictfile, fnamefobject):
        """stuff file data into the blank dictionary"""
        #fname = './exapmlefiles/5ZoneDD.idf'
        #fname = './1ZoneUncontrolled.idf'
        if isinstance(dictfile, Idd):
            localidd = copy.deepcopy(dictfile)
            dt, dtls = localidd.dt, localidd.dtls
        else:
            dt, dtls = self.initdict(dictfile)
        # astr = mylib2.readfile(fname)
        astr = fnamefobject.read()
        try:
            astr = astr.decode('ISO-8859-2')
        except AttributeError:
            pass
        fnamefobject.close()
        nocom = removecomment(astr, '!')
        idfst = nocom
        # alist = string.split(idfst, ';')
        alist = idfst.split(';')
        lss = []
        for element in alist:
            # lst = string.split(element, ',')
            lst = element.split(',')
            lss.append(lst)

        for i in range(0, len(lss)):
            for j in range(0, len(lss[i])):
                lss[i][j] = lss[i][j].strip()

        for element in lss:
            node = element[0].upper()
            if dt.has_key(node):
                #stuff data in this key
                dt[node.upper()].append(element)
            else:
                #scream
                if node == '':
                    continue
                print('this node -%s-is not present in base dictionary'%(node))

        self.dt, self.dtls = dt, dtls
        return dt, dtls

    def replacenode(self, othereplus, node):
        """replace the node here with the node from othereplus"""
        node = node.upper()
        self.dt[node.upper()] = othereplus.dt[node.upper()]

    def add2node(self, othereplus, node):
        """add the node here with the node from othereplus
        this will potentially have duplicates"""
        node = node.upper()
        self.dt[node.upper()] = self.dt[node.upper()] + othereplus.dt[node.upper()]

    def addinnode(self, otherplus, node, objectname):
        """add an item to the node.
        example: add a new zone to the element 'ZONE' """
        # do a test for unique object here
        newelement = otherplus.dt[node.upper()]

    def getrefs(self, reflist):
        """
        reflist is got from getobjectref in parse_idd.py
        getobjectref returns a dictionary.
        reflist is an item in the dictionary
        getrefs gathers all the fields refered by reflist
        """
        alist = []
        for element in reflist:
            if self.dt.has_key(element[0].upper()):
                for elm in self.dt[element[0].upper()]:
                    alist.append(elm[element[1]])
        return alist


#------------------------------------------

