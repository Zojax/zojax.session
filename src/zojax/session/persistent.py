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
from zope import interface, event
from zope.proxy import sameProxiedObjects
from zope.component import queryUtility, getSiteManager
from zope.component.interfaces import IComponentLookup
from zope.lifecycleevent import ObjectCreatedEvent
from zope.session.interfaces import ISessionDataContainer
from zope.session.session import PersistentSessionDataContainer

from interfaces import ISessionDataFactory


class PersistentSessionFactory(object):
    interface.implements(ISessionDataFactory)

    name = u'session.persistent'
    title = u'Persistent Session'
    description = u'A Session data container that stores data in ZODB.'

    @property
    def session(self):
        sm = getSiteManager()
        return sm.get(self.name)

    def install(self):
        if self.session is not None:
            raise ValueError(u'Session data container already installed.')

        sm = getSiteManager()

        data = PersistentSessionDataContainer()
        event.notify(ObjectCreatedEvent(data))

        sm[self.name] = data

        sm.registerUtility(data, ISessionDataContainer)

    def uninstall(self):
        sm = getSiteManager()

        if self.name in sm:
            sm.unregisterUtility(sm[self.name], ISessionDataContainer)
            del sm[self.name]

    def isInstalled(self):
        container = queryUtility(ISessionDataContainer)
        if container is not None:
            if container.__class__ == PersistentSessionDataContainer and \
                    sameProxiedObjects(
                IComponentLookup(container), getSiteManager()):
                return True

        return False

    def isAvailable(self):
        return True
