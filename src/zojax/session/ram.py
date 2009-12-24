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
"""

$Id$
"""
from rwproperty import getproperty, setproperty
from zope import interface, event
from zope.proxy import sameProxiedObjects
from zope.component import getUtility, queryUtility, getSiteManager
from zope.component.interfaces import IComponentLookup
from zope.lifecycleevent import ObjectCreatedEvent
from zope.session.interfaces import ISessionDataContainer
from zope.session.session import RAMSessionDataContainer

from interfaces import ISessionDataFactory


class RamSessionFactory(object):
    interface.implements(ISessionDataFactory)

    name = u'session.ram'
    title = u'RAM Session'
    description = u'A Session data container that stores data in RAM.'

    @property
    def session(self):
        sm = getSiteManager()
        return sm.get(self.name)

    def install(self):
        if self.session is not None:
            raise ValueError(u'Session data container already installed.')

        sm = getSiteManager()

        ram = RAMSessionDataContainer()
        event.notify(ObjectCreatedEvent(ram))

        sm[self.name] = ram

        sm.registerUtility(ram, ISessionDataContainer)

    def uninstall(self):
        sm = getSiteManager()

        if self.name in sm:
            sm.unregisterUtility(sm[self.name], ISessionDataContainer)
            del sm[self.name]

    def isInstalled(self):
        container = queryUtility(ISessionDataContainer)
        if container is not None:
            if isinstance(container, RAMSessionDataContainer) and \
                    sameProxiedObjects(
                IComponentLookup(container), getSiteManager()):
                return True

        return False

    def isAvailable(self):
        return True
