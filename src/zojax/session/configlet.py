##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from zope.app.folder.interfaces import IFolder
"""

$Id$
"""
from rwproperty import setproperty, getproperty
from zope.component import getUtility, getUtilitiesFor
from zope.app.component.hooks import getSite
from zope.traversing.interfaces import IContainmentRoot

from interfaces import ISessionDataFactory


class SessionConfiglet(object):

    @property
    def session(self):
        for name, factory in getUtilitiesFor(ISessionDataFactory):
            if factory.isInstalled():
                return factory.session

    @getproperty
    def sessiontype(self):
        for name, factory in getUtilitiesFor(ISessionDataFactory):
            if factory.isInstalled():
                return name

    @setproperty
    def sessiontype(self, value):
        old = self.sessiontype
        if old is not None:
            getUtility(ISessionDataFactory, old).uninstall()

        getUtility(ISessionDataFactory, value).install()

    def isAvailable(self):
        if not IContainmentRoot.providedBy(getSite()) and not \
            IFolder.providedBy(getSite().__parent__):
            return False

        return super(SessionConfiglet, self).isAvailable()
